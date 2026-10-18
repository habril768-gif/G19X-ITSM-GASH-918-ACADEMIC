"""Revisión explícita y trabajo IA durable; nunca escribe la decisión oficial."""
import hashlib
import os
from datetime import timedelta
from uuid import uuid4
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import SQLAlchemyError
from app.ai.contracts import AIResult, PROMPT_VERSION, TransientAIError
from app.ai.queue import notify
from app.core.security import aware, utcnow
from app.models import AIJob, AuditEvent, Category, Department, Incident, User
from app.services.administration_lock import administration_lock
from app.services.incidents import MANAGERS, role_name, visibility
from app.services.protection import manager_involved


def enabled():
    return os.environ.get('AI_ENABLED', 'false').lower() in {'true', '1'}


def _audit(db, case, job, operation, actor_id=None):
    db.add(AuditEvent(incidencia_id=case.id, usuario_id=actor_id, accion='VALIDACION_IA', detalle={
        'operation': operation, 'source': 'IA', 'job_id': str(job.id), 'attempts': job.attempts,
        'model': job.model, 'prompt_version': job.prompt_version, 'content_revision': job.content_revision,
        'job_status': job.status, 'reason': job.error}))


def _authorized_case(db, actor, case_id):
    administration_lock(db, actor)
    if role_name(db, actor) not in MANAGERS:
        raise HTTPException(403, 'Solo gestores autorizados')
    case = db.scalar(select(Incident).where(Incident.id == case_id).with_for_update().execution_options(populate_existing=True))
    if case is None or db.scalar(select(Incident.id).where(Incident.id == case_id, visibility(db, actor))) is None:
        raise HTTPException(404, 'Incidencia no encontrada')
    return case


def enqueue(db, actor, case_id, body):
    try:
        case = _authorized_case(db, actor, case_id)
        model = os.environ.get('OPENAI_MODEL', '').strip()
        if not enabled() or not model or len(model) > 120:
            raise HTTPException(503, 'La asistencia IA no está configurada; continúa manualmente')
        if case.is_confidential or manager_involved(db, case):
            raise HTTPException(409, 'Los casos confidenciales o con conflicto se atienden manualmente')
        if case.status not in {'PENDIENTE', 'EN_REVISION'} or case.classification_valid:
            raise HTTPException(409, 'Solo se solicita asistencia antes de la validación humana vigente')
        digest = hashlib.sha256((str(case.content_revision) + '\n' + body.ai_input_text).encode('utf-8')).hexdigest()
        existing = db.scalar(select(AIJob).where(AIJob.case_id == case.id, AIJob.input_digest == digest))
        if existing:
            if existing.status in {'FALLIDA', 'OMITIDA'}:
                raise HTTPException(409, 'Esta solicitud terminó; clasifica manualmente o revisa un texto diferente')
            job_id = existing.id; db.commit()
            return {'job_id': job_id, 'received': True, 'already_requested': True, 'queue_available': notify(job_id)}
        if db.scalar(select(AIJob.id).where(AIJob.case_id == case.id, AIJob.status.in_(['PENDIENTE', 'EN_PROCESO'])).limit(1)):
            raise HTTPException(409, 'Ya hay un trabajo pendiente; actualiza el expediente')
        if case.ai_suggestion is not None and case.ai_input_reviewed_at is not None:
            raise HTTPException(409, 'Se conserva la primera respuesta válida de esta versión; valida manualmente')
        now = utcnow()
        catalog = [{'id': row.id, 'nombre': row.nombre} for row in db.scalars(select(Category).order_by(Category.id)).all()
                   if case.scope != 'ENTORNO' or row.id == 4]
        if not catalog:
            raise HTTPException(409, 'No existe catálogo de clasificación disponible')
        job = AIJob(id=uuid4(), case_id=case.id, reviewed_by=actor.id, input_text=body.ai_input_text,
                    input_digest=digest, content_revision=case.content_revision, catalog=catalog,
                    model=model, prompt_version=PROMPT_VERSION, status='PENDIENTE', attempts=0, available_at=now, created_at=now)
        db.add(job)
        case.ai_input_text, case.ai_input_reviewed_by, case.ai_input_reviewed_at = body.ai_input_text, actor.id, now
        case.ai_status, case.ai_suggestion, case.ai_error, case.ai_skip_reason = 'PENDIENTE', None, None, None
        case.ai_model, case.ai_prompt_version = model, PROMPT_VERSION
        _audit(db, case, job, 'IA_ENCOLADA', actor.id)
        db.commit(); job_id = job.id
        return {'job_id': job_id, 'received': True, 'already_requested': False, 'queue_available': notify(job_id)}
    except (HTTPException, SQLAlchemyError):
        db.rollback(); raise


def _reason(db, case, job):
    if case.is_confidential or manager_involved(db, case):
        return 'Confidencialidad o conflicto de interés; no usar asistencia'
    if case.status not in {'PENDIENTE', 'EN_REVISION'} or case.classification_valid:
        return 'Decisión humana vigente o caso finalizado; no usar respuesta tardía'
    if case.content_revision != job.content_revision or case.ai_input_text != job.input_text or case.ai_input_reviewed_by != job.reviewed_by:
        return 'Cambió el contenido o su revisión; requiere nueva confirmación'
    if case.ai_status != 'PENDIENTE' or job.prompt_version != PROMPT_VERSION:
        return 'Asistencia cancelada o versión de prompt no vigente'
    person = db.get(User, job.reviewed_by)
    if person is None:
        return 'Revisor no habilitado'
    db.refresh(person)
    department = db.get(Department, person.departamento_id)
    if department:
        db.refresh(department)
    if not person.is_active or not department or not department.is_active or role_name(db, person) not in MANAGERS:
        return 'Revisor no habilitado'
    if db.scalar(select(Incident.id).where(Incident.id == case.id, visibility(db, person))) is None:
        return 'El revisor perdió acceso; no enviar texto'
    return None


def _omit(db, case, job, reason):
    job.status, job.error, job.completed_at, job.lease_until = 'OMITIDA', reason, utcnow(), None
    case.ai_status, case.ai_skip_reason = 'OMITIDA', reason
    _audit(db, case, job, 'IA_OMITIDA')


def _due(job, now):
    return ((job.status == 'PENDIENTE' and aware(job.available_at) <= now) or
            (job.status == 'EN_PROCESO' and job.lease_until is not None and aware(job.lease_until) <= now))


def process_one(factory, provider, job_id=None):
    """Despacho al menos una vez; token de intento impide aceptar respuestas duplicadas."""
    if not enabled():
        return False
    now = utcnow()
    with factory() as db:
        administration_lock(db)
        due = or_(and_(AIJob.status == 'PENDIENTE', AIJob.available_at <= now),
                  and_(AIJob.status == 'EN_PROCESO', AIJob.lease_until <= now))
        statement = select(AIJob.id, AIJob.case_id).where(due)
        if job_id is not None:
            statement = statement.where(AIJob.id == job_id)
        candidate = db.execute(statement.order_by(AIJob.created_at, AIJob.id).limit(1)).first()
        if candidate is None:
            return False
        # Siempre caso antes de trabajo: mismo orden para revisión, reclamo y respuesta.
        case = db.scalar(select(Incident).where(Incident.id == candidate.case_id).with_for_update().execution_options(populate_existing=True))
        job = db.scalar(select(AIJob).where(AIJob.id == candidate.id).with_for_update().execution_options(populate_existing=True))
        now = utcnow()
        if not _due(job, now):
            return False
        reason = _reason(db, case, job)
        if reason:
            _omit(db, case, job, reason); db.commit(); return True
        if job.attempts >= 3:
            job.status, job.error, job.completed_at = 'FALLIDA', 'Se agotaron tres intentos; continúa manualmente', now
            case.ai_status, case.ai_error = 'FALLIDA', job.error
            _audit(db, case, job, 'IA_FALLIDA'); db.commit(); return True
        job.attempts += 1
        job.status, job.lease_token, job.lease_until = 'EN_PROCESO', uuid4(), now + timedelta(seconds=120)
        job.dispatched_at = now
        _audit(db, case, job, 'IA_ENVIO')
        dispatch = {'id': job.id, 'case_id': case.id, 'token': job.lease_token, 'text': job.input_text,
                    'catalog': job.catalog, 'model': job.model}
        db.commit()
    # No se mantiene una transacción/bloqueo durante la petición externa.
    result = None; transient = False; failed = False
    try:
        result = AIResult.model_validate(provider.classify(dispatch['text'], dispatch['catalog'], dispatch['model'])).model_dump()
    except TransientAIError:
        failed = True; transient = True
    except Exception:
        # Nunca almacenar cuerpos, credenciales o excepciones crudas del proveedor.
        failed = True
    with factory() as db:
        administration_lock(db)
        case = db.scalar(select(Incident).where(Incident.id == dispatch['case_id']).with_for_update().execution_options(populate_existing=True))
        job = db.scalar(select(AIJob).where(AIJob.id == dispatch['id']).with_for_update().execution_options(populate_existing=True))
        if job.status != 'EN_PROCESO' or job.lease_token != dispatch['token']:
            return True
        reason = _reason(db, case, job)
        if reason:
            _omit(db, case, job, reason); db.commit(); return True
        if result and result['result'] == 'CLASIFICADA':
            if result['category_id'] not in {row['id'] for row in job.catalog} or db.get(Category, result['category_id']) is None:
                failed = True; result = None
        job.lease_until = None
        if not failed:
            if job.result is None:
                job.result = result
            job.status, job.error, job.completed_at = 'COMPLETADA', None, utcnow()
            case.ai_suggestion, case.ai_status, case.ai_error, case.ai_skip_reason = job.result, 'COMPLETADA', None, None
            _audit(db, case, job, 'IA_RESPUESTA')
        elif transient and job.attempts < 3:
            job.status, job.error = 'PENDIENTE', 'Fallo transitorio; se reintentará sin bloquear atención manual'
            job.available_at = utcnow() + timedelta(seconds=5 * 2 ** (job.attempts - 1))
            _audit(db, case, job, 'IA_REINTENTO')
        else:
            job.status, job.error, job.completed_at = 'FALLIDA', 'No fue posible completar la asistencia; continúa manualmente', utcnow()
            case.ai_status, case.ai_error = 'FALLIDA', job.error
            _audit(db, case, job, 'IA_FALLIDA')
        db.commit()
    return True
