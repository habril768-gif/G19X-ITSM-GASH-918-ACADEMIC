"""Eventos atómicos, destinatarios mínimos y despacho con permisos vigentes."""
import os
from datetime import timedelta, datetime
from uuid import NAMESPACE_URL, uuid4, uuid5
from sqlalchemy import select, and_, or_
from app.core.security import utcnow, aware
from app.models import MailDelivery, Incident, User, Department, Role
from app.services.incidents import independent_rh_visibility, role_name, visibility
from app.services.administration_lock import administration_lock

def enabled():
    return os.environ.get('MAIL_ENABLED', 'false').lower() in {'true', '1'}

def allowed(db, case, person):
    if person is None or not person.is_active:
        return False
    department = db.get(Department, person.departamento_id)
    return bool(department and department.is_active and db.scalar(
        select(Incident.id).where(Incident.id == case.id, visibility(db, person))))

def creation_recipient_ids(db, case):
    """Selecciona RH activos e independientes en una consulta, sin carga por persona."""
    if case.assigned_to is not None:
        return set()
    return set(db.scalars(
        select(User.id).select_from(User)
        .join(Role, User.rol_id == Role.id)
        .join(Department, User.departamento_id == Department.id)
        .join(Incident, Incident.id == case.id)
        .where(Role.nombre == 'ADMIN_RH', User.is_active.is_(True), Department.is_active.is_(True),
               independent_rh_visibility(User.id))))


def queue_event(db, case, event, before=None):
    """Misma transacción del evento. Nunca conecta a SMTP/Redis ni hace commit."""
    before = before or {}
    kind = None
    if event.accion == 'CREADO': kind = 'CREACION'
    elif event.accion == 'REAPERTURA': kind = 'REAPERTURA'
    elif before.get('status') != 'CERRADA' and case.status == 'CERRADA': kind = 'CIERRE'
    elif before.get('status') != 'RESUELTA' and case.status == 'RESUELTA': kind = 'RESOLUCION'
    elif before.get('assigned_to') != (str(case.assigned_to) if case.assigned_to else None) and case.assigned_to:
        kind = 'ASIGNACION'
    if not kind: return
    db.flush()
    if kind == 'CREACION':
        recipients = creation_recipient_ids(db, case)
    else:
        if kind in {'ASIGNACION', 'REAPERTURA'}:
            people = [db.get(User, case.assigned_to)] if case.assigned_to else []
        else:
            people = [db.get(User, ident) for ident in {case.created_by, case.affected_employee_id} if ident]
        recipients = {person.id for person in people if allowed(db, case, person)}
    now = utcnow()
    context = {key: (getattr(case,key).isoformat() if key != 'assigned_to' and getattr(case,key)
                       else str(getattr(case,key)) if getattr(case,key) else None)
               for key in ('assigned_to','resolved_at','cycle_start_at')}
    if kind == 'CIERRE':
        context['closed_at'] = case.closed_at.isoformat() if case.closed_at else None
    keys = {ident: uuid5(NAMESPACE_URL, f'plurione-mail:{event.id}:{ident}')
            for ident in list(recipients) or [None]}
    existing = set(db.scalars(select(MailDelivery.id).where(MailDelivery.id.in_(list(keys.values())))))
    pending = [dict(id=key, event_id=event.id, case_id=case.id, recipient_id=ident,
                kind=kind, context=context, status='PENDIENTE' if ident else 'OMITIDA', attempts=0,
                error=None if ident else 'Sin destinatario autorizado', available_at=now, created_at=now,
                completed_at=None if ident else now)
               for ident, key in keys.items() if key not in existing]
    # Core INSERT..RETURNING activa insertmanyvalues en PostgreSQL/SQLite:
    # SQLAlchemy reutiliza la compilación y envía VALUES múltiples por lote,
    # sin ORM por entrega ni commit. No necesitamos ordenar las filas devueltas.
    table = MailDelivery.__table__
    statement = table.insert().returning(table.c.id).execution_options(insertmanyvalues_page_size=50)
    for start in range(0, len(pending), 50):
        db.execute(statement, pending[start:start + 50]).close()

def _same_date(value, expected):
    return (value is None and expected is None) or bool(value and expected and aware(value) == aware(datetime.fromisoformat(expected)))

def omission(db, case, job):
    person = db.get(User, job.recipient_id) if job.recipient_id else None
    if not allowed(db, case, person): return 'Destinatario sin permiso vigente'
    role = role_name(db, person)
    if job.kind == 'CREACION' and (case.assigned_to or role != 'ADMIN_RH'):
        return 'Creación ya atendida o destinatario no elegible'
    if job.kind in {'ASIGNACION','REAPERTURA'}:
        if case.assigned_to != person.id or role not in {'ADMIN_RH','SUPERVISOR'}:
            return 'Responsable cambió o dejó de ser elegible'
        if job.kind == 'REAPERTURA' and not _same_date(case.cycle_start_at, job.context['cycle_start_at']):
            return 'El ciclo del evento ya no está vigente'
    if job.kind == 'RESOLUCION' and (case.status not in {'RESUELTA','CERRADA'} or not _same_date(case.resolved_at,job.context['resolved_at'])):
        return 'La resolución del evento ya no está vigente'
    if job.kind == 'CIERRE' and (case.status != 'CERRADA' or not _same_date(case.closed_at, job.context.get('closed_at'))):
        return 'El cierre del evento ya no está vigente'
    return None

def _due(now):
    return or_(and_(MailDelivery.status == 'PENDIENTE', MailDelivery.available_at <= now),
               and_(MailDelivery.status == 'EN_PROCESO', MailDelivery.lease_until <= now))

def process_one(factory, transport):
    if not enabled(): return False
    with factory() as db:
        administration_lock(db)
        candidate = db.execute(select(MailDelivery.id, MailDelivery.case_id).where(_due(utcnow()))
                              .order_by(MailDelivery.created_at, MailDelivery.id).limit(1)).first()
        if candidate is None: return False
        case = db.scalar(select(Incident).where(Incident.id == candidate.case_id).with_for_update())
        job = db.scalar(select(MailDelivery).where(MailDelivery.id == candidate.id, _due(utcnow())).with_for_update())
        if job is None: return False
        reason = omission(db,case,job)
        if reason:
            job.status, job.error, job.completed_at, job.lease_until = 'OMITIDA', reason, utcnow(), None
            db.commit(); return True
        if job.attempts >= 4:
            job.status, job.error, job.completed_at = 'FALLIDA', 'Se agotaron los intentos; entrega no confirmada', utcnow()
            job.lease_until=None; db.commit(); return True
        job.attempts += 1
        job.status, job.lease_token, job.lease_until = 'EN_PROCESO', uuid4(), utcnow()+timedelta(seconds=120)
        ident, case_id, token = job.id, case.id, job.lease_token
        db.commit()
    with factory() as db:
        administration_lock(db)
        case = db.scalar(select(Incident).where(Incident.id == case_id).with_for_update())
        job = db.scalar(select(MailDelivery).where(MailDelivery.id == ident).with_for_update())
        if job.status != 'EN_PROCESO' or job.lease_token != token: return True
        reason = omission(db,case,job)
        if reason:
            job.status, job.error = 'OMITIDA', reason
        else:
            # Bloqueos durante el despacho impiden cambios de permiso a mitad del envío.
            # SMTP no es transaccional: Message-ID estable no garantiza exactly-once.
            from app.mail.smtp import DeliveryError
            try:
                transport.send(db.get(User,job.recipient_id).email, case.id, job.id)
                job.status, job.error = 'ENVIADA', None
            except DeliveryError as exc:
                if exc.transient and job.attempts < 4:
                    job.status, job.error = 'PENDIENTE', 'Fallo transitorio; reintento pendiente'
                    job.available_at = utcnow()+timedelta(seconds=5*2**(job.attempts-1))
                else:
                    job.status, job.error = 'FALLIDA', 'No se confirmó la entrega; revisa configuración o servidor SMTP'
        job.lease_until = None
        if job.status != 'PENDIENTE': job.completed_at = utcnow()
        db.commit()
    return True
