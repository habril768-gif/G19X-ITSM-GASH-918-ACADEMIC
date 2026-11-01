"""Registro auditado y autorización SQL compartida por consultas de incidencias."""
from uuid import UUID
from functools import lru_cache
from types import SimpleNamespace
from fastapi import HTTPException
from sqlalchemy import and_, bindparam, exists, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased

from app.models import AuditEvent, Department, Incident, IncidentParticipant, Role, User

ACTIVE_RELATIONS = ("DECLARADO", "CONFIRMADO")
MANAGERS = ("ADMIN_RH", "SUPERVISOR")


def role_name(db: Session, user: User) -> str:
    role = db.get(Role, user.rol_id)
    if role is None or role.nombre not in {"ADMIN_RH", "SUPERVISOR", "EMPLEADO"}:
        raise HTTPException(403, "Rol no habilitado")
    return role.nombre


def independent_rh_visibility(actor_id):
    """Predicado compartido para consulta y selección de RH destinatarios."""
    related = exists(select(1).where(
        IncidentParticipant.incidencia_id == Incident.id,
        IncidentParticipant.user_id == actor_id,
        IncidentParticipant.review_status.in_(ACTIVE_RELATIONS),
    ))
    return and_(or_(Incident.affected_employee_id.is_(None), Incident.affected_employee_id != actor_id), ~related)


def visibility(db: Session, actor: User):
    """Lee el rol vigente y construye el predicado sin cachear autorización."""
    return _visibility_for_role(actor, role_name(db, actor))


def _visibility_for_role(actor: User, role: str):
    """Uso interno con rol ya validado en esta operación; no guarda estado."""
    if role not in {"ADMIN_RH", "SUPERVISOR", "EMPLEADO"}:
        raise HTTPException(403, "Rol no habilitado")
    if role == "ADMIN_RH":
        return independent_rh_visibility(actor.id)
    related = exists(select(1).where(
        IncidentParticipant.incidencia_id == Incident.id,
        IncidentParticipant.user_id == actor.id,
        IncidentParticipant.review_status.in_(ACTIVE_RELATIONS),
    ))
    affected = aliased(User)
    affected_role = aliased(Role)
    participant = aliased(IncidentParticipant)
    participant_user = aliased(User)
    participant_role = aliased(Role)
    manager_affected = exists(select(1).select_from(affected).join(affected_role, affected.rol_id == affected_role.id).where(
        affected.id == Incident.affected_employee_id, affected_role.nombre.in_(MANAGERS)))
    manager_related = exists(select(1).select_from(participant).join(participant_user, participant.user_id == participant_user.id).join(participant_role, participant_user.rol_id == participant_role.id).where(
        participant.incidencia_id == Incident.id, participant.review_status.in_(ACTIVE_RELATIONS), participant_role.nombre.in_(MANAGERS)))
    public = and_(Incident.is_confidential.is_(False), ~manager_affected, ~manager_related)
    if role == "SUPERVISOR":
        affected_department = exists(select(1).where(affected.id == Incident.affected_employee_id, affected.departamento_id == actor.departamento_id))
        return and_(public, ~related, or_(
            and_(Incident.scope == "PERSONA", affected_department, Incident.affected_employee_id != actor.id),
            and_(Incident.scope == "ENTORNO", Incident.reported_department_id == actor.departamento_id),
        ))
    return and_(public, or_(
        and_(Incident.scope == "PERSONA", Incident.affected_employee_id == actor.id),
        and_(Incident.scope == "ENTORNO", Incident.created_by == actor.id, Incident.reported_department_id == actor.departamento_id),
    ))


@lru_cache(maxsize=1)
def _visible_case_statement():
    # Solo estructura SQL: nunca recibe ni guarda usuario, rol vigente,
    # Session, UUID reales, resultados o decisiones de autorización.
    actor = SimpleNamespace(
        id=bindparam("detail_actor_id", type_=User.id.type),
        departamento_id=bindparam("detail_department_id", type_=User.departamento_id.type),
    )
    predicate = or_(*(and_(Role.nombre == role, _visibility_for_role(actor, role))
                      for role in ("ADMIN_RH", "SUPERVISOR", "EMPLEADO")))
    return (select(Role.nombre, Incident).select_from(Role)
        .outerjoin(Incident, and_(Incident.id == bindparam("detail_case_id", type_=Incident.id.type), predicate))
        .where(Role.id == bindparam("detail_role_id", type_=User.rol_id.type)))


def visible_case(db: Session, actor: User, case_id: UUID) -> Incident:
    # Rol y expediente autorizado se vuelven a leer en cada ejecución.
    # LEFT JOIN conserva 403 de rol y 404 de caso ausente/no visible.
    row = db.execute(_visible_case_statement(), {
        "detail_actor_id": actor.id,
        "detail_department_id": actor.departamento_id,
        "detail_case_id": case_id,
        "detail_role_id": actor.rol_id,
    }).one_or_none()
    role, case = row if row is not None else (None, None)
    if role not in {"ADMIN_RH", "SUPERVISOR", "EMPLEADO"}:
        raise HTTPException(403, "Rol no habilitado")
    if case is None:
        raise HTTPException(404, "Incidencia no encontrada")
    return case


@lru_cache(maxsize=3)
def _case_access_statement(role):
    # Solo tres estructuras por rol, sin identidades, sesiones ni resultados.
    actor = SimpleNamespace(
        id=bindparam("access_actor_id", type_=User.id.type),
        departamento_id=bindparam("access_department_id", type_=User.departamento_id.type),
    )
    return select(Incident.id).where(
        Incident.id == bindparam("access_case_id", type_=Incident.id.type),
        _visibility_for_role(actor, role),
    )


def case_access_for_current_role(db, actor, case_id, role):
    """Ejecuta permisos vigentes; el llamador ya refrescó actor/rol bajo bloqueo."""
    if role not in {"ADMIN_RH", "SUPERVISOR", "EMPLEADO"}:
        raise HTTPException(403, "Rol no habilitado")
    return db.scalar(_case_access_statement(role), {
        "access_actor_id": actor.id,
        "access_department_id": actor.departamento_id,
        "access_case_id": case_id,
    }) is not None


def create_case(db: Session, actor: User, body):
    from app.services.administration_lock import administration_lock
    role, actor_department = administration_lock(db, actor, include_role=True, include_department=True)
    affected = None
    if body.scope == "PERSONA":
        affected_id = body.affected_employee_id or (actor.id if role == "EMPLEADO" else None)
        if affected_id is None:
            raise HTTPException(422, "Selecciona al empleado afectado")
        affected = db.get(User, affected_id)
        if affected is None or not affected.is_active:
            raise HTTPException(422, "Empleado afectado no habilitado")
        if role == "EMPLEADO" and affected.id != actor.id:
            raise HTTPException(403, "Registro fuera del ámbito autorizado")
        if role == "SUPERVISOR" and affected.departamento_id != actor.departamento_id:
            raise HTTPException(403, "Registro fuera del ámbito autorizado")
        department_id = affected.departamento_id
        if body.reported_department_id is not None and body.reported_department_id != department_id:
            raise HTTPException(422, "El departamento se obtiene del empleado afectado")
    else:
        if body.affected_employee_id is not None:
            raise HTTPException(422, "ENTORNO no admite empleado afectado")
        department_id = body.reported_department_id
        if department_id is None:
            raise HTTPException(422, "Selecciona el departamento reportado")
        if role != "ADMIN_RH" and department_id != actor.departamento_id:
            raise HTTPException(403, "Registro fuera del ámbito autorizado")
    # El departamento del actor ya fue refrescado y validado después del bloqueo.
    # Para otro departamento se conserva la consulta/validación independiente.
    department = actor_department if department_id == actor_department.id else db.get(Department, department_id)
    if department is None or not department.is_active:
        raise HTTPException(422, "Departamento no habilitado")
    seen = set()
    participants = []
    manager_involved = affected is not None and role_name(db, affected) in MANAGERS
    for item in body.participants:
        if item.user_id in seen or (affected is not None and item.user_id == affected.id):
            raise HTTPException(422, "Participante duplicado o ya incluido como afectado")
        seen.add(item.user_id)
        person = db.get(User, item.user_id)
        if person is None or not person.is_active:
            raise HTTPException(422, "Participante no habilitado")
        person_department = db.get(Department, person.departamento_id)
        if person_department is None or not person_department.is_active:
            raise HTTPException(422, "Participante no habilitado")
        participant_role = role_name(db, person)
        if role != "ADMIN_RH" and person.departamento_id != actor.departamento_id and participant_role not in MANAGERS:
            raise HTTPException(403, "Participante fuera del ámbito autorizado")
        manager_involved = manager_involved or participant_role in MANAGERS
        participants.append(item)
    confidential = body.is_confidential or manager_involved
    case = Incident(
        titulo=body.titulo, descripcion=body.descripcion, incident_date=body.incident_date,
        scope=body.scope, affected_employee_id=affected.id if affected else None,
        reported_department_id=department_id, department_id_at_creation=department_id,
        created_by=actor.id, status="PENDIENTE", assigned_to=None,
        category_id=4 if body.scope == "ENTORNO" else None,
        is_confidential=confidential, classification_valid=False,
        ai_status="OMITIDA" if confidential else "PENDIENTE",
        ai_skip_reason="Confidencialidad o conflicto de interés; clasificación manual" if confidential else None,
    )
    try:
        db.add(case)
        db.flush()
        for item in participants:
            db.add(IncidentParticipant(incidencia_id=case.id, user_id=item.user_id, declaration_reason=item.declaration_reason))
        event = AuditEvent(incidencia_id=case.id, usuario_id=actor.id, accion="CREADO", detalle={
            "scope":case.scope, "titulo":case.titulo, "descripcion":case.descripcion,
            "affected_employee_id":str(case.affected_employee_id) if case.affected_employee_id else None,
            "reported_department_id":str(department_id), "is_confidential":confidential,
            "confidentiality_reason":"GESTOR_INVOLUCRADO" if manager_involved else ("SOLICITADA" if confidential else None),
            "participants":[{"user_id":str(i.user_id),"declaration_reason":i.declaration_reason} for i in participants],
        })
        db.add(event)
        from app.services.mail import queue_event
        # Actor/rol ya refrescados bajo bloqueo. La misma lectura obtiene
        # destinatarios y permiso del recibo, sin guardar decisiones entre llamadas.
        can_view = queue_event(db, case, event, receipt_actor=actor, receipt_role=role)
        receipt = {"id": case.id, "received": True, "can_view": can_view}
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503, "No fue posible registrar la incidencia; no se guardaron cambios parciales") from None
    return receipt
