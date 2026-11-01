"""Operaciones de gestión serializadas por expediente y auditadas atómicamente."""
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models import AuditEvent, Category, Department, Incident, User
from app.services.incidents import MANAGERS, case_access_for_current_role, role_name


def eligible_manager(db, case, user_id):
    person = db.scalar(select(User).where(User.id == user_id).with_for_update())
    if person is None or not person.is_active:
        raise HTTPException(422, "Responsable no habilitado para gestionar")
    role = role_name(db, person)
    if role not in MANAGERS:
        raise HTTPException(422, "Responsable no habilitado para gestionar")
    department = db.get(Department, person.departamento_id)
    if department is None or not department.is_active:
        raise HTTPException(422, "Responsable no habilitado para gestionar")
    if not case_access_for_current_role(db, person, case.id, role):
        raise HTTPException(422, "Responsable sin acceso independiente al caso")
    return person


def snapshot(case):
    def stamp(value):
        return value.isoformat() if value else None
    return {"status": case.status, "assigned_to": str(case.assigned_to) if case.assigned_to else None,
            "category_id": case.category_id, "priority": case.priority,
            "classification_valid": case.classification_valid,
            "validated_by": str(case.validated_by) if case.validated_by else None,
            "validated_at": stamp(case.validated_at), "cycle_start_at": stamp(case.cycle_start_at),
            "resolution_text": case.resolution_text, "resolved_at": stamp(case.resolved_at),
            "closed_at": stamp(case.closed_at)}


def manage_case(db, actor, case_id, operation, body, *, presenter=None):
    try:
        from app.services.administration_lock import administration_lock
        role = administration_lock(db, actor, include_role=True)
        if role not in MANAGERS:
            raise HTTPException(403, "Solo gestores autorizados")
        # Lock first, then reevaluate visibility on the refreshed row. PostgreSQL
        # serializes competing transitions; SQLite tests cannot prove that lock.
        case = db.scalar(select(Incident).where(Incident.id == case_id)
                         .with_for_update().execution_options(populate_existing=True))
        if case is None or not case_access_for_current_role(db, actor, case_id, role):
            raise HTTPException(404, "Incidencia no encontrada")
        before = snapshot(case)
        now = datetime.now(timezone.utc)
        action = "ESTADO_CAMBIADO"
        if operation in {"classification", "assignment", "content"} and case.status not in {"PENDIENTE", "EN_REVISION"}:
            raise HTTPException(409, "Reabre el caso antes de modificarlo")
        if operation == "classification":
            if db.get(Category, body.category_id) is None or (case.scope == "ENTORNO" and body.category_id != 4):
                raise HTTPException(422, "Categoría no válida para el caso")
            case.category_id, case.priority = body.category_id, body.priority
            case.classification_valid = True
            case.validated_by, case.validated_at = actor.id, now
            action = "VALIDACION_IA"  # Evento existente, también para decisión manual.
        elif operation == "assignment":
            eligible_manager(db, case, body.assigned_to)
            case.assigned_to = body.assigned_to
            action = "ASIGNADO"
        elif operation == "content":
            before.update(titulo=case.titulo, descripcion=case.descripcion)
            if body.descripcion != case.descripcion:
                case.classification_valid = False
                case.content_revision += 1
                case.ai_input_text = case.ai_input_reviewed_by = case.ai_input_reviewed_at = None
                if case.ai_status == 'PENDIENTE':
                    case.ai_status = 'OMITIDA'
                    case.ai_skip_reason = 'Contenido editado; requiere una nueva revisión del texto IA'
            case.titulo, case.descripcion = body.titulo, body.descripcion
            action = "CONTENIDO_EDITADO"
        elif operation == "transition":
            target = body.status
            pair = (case.status, target)
            if pair not in {("PENDIENTE", "EN_REVISION"), ("EN_REVISION", "RESUELTA"),
                            ("RESUELTA", "CERRADA"), ("RESUELTA", "EN_REVISION"), ("CERRADA", "EN_REVISION")}:
                raise HTTPException(409, "Transición no permitida")
            reopening = case.status in {"RESUELTA", "CERRADA"} and target == "EN_REVISION"
            if body.reason is not None and not reopening:
                raise HTTPException(422, "El motivo solo aplica a reapertura")
            if (reopening or target == "CERRADA") and role != "ADMIN_RH":
                raise HTTPException(403, "Operación reservada a Admin RH independiente")
            if reopening:
                if not body.reason:
                    raise HTTPException(422, "Indica el motivo de reapertura")
                assignee = body.assigned_to or case.assigned_to
                eligible_manager(db, case, assignee)
                case.assigned_to = assignee
                case.resolution_text = case.resolved_at = case.closed_at = None
                case.cycle_start_at = now
                action = "REAPERTURA"
            elif target == "EN_REVISION":
                if not case.classification_valid:
                    raise HTTPException(409, "Se requiere clasificación validada vigente")
                assignee = body.assigned_to or case.assigned_to
                eligible_manager(db, case, assignee)
                case.assigned_to, case.cycle_start_at = assignee, now
            elif target == "RESUELTA":
                if not case.classification_valid:
                    raise HTTPException(409, "Revalida la clasificación antes de resolver")
                eligible_manager(db, case, case.assigned_to)
                if not body.resolution_text:
                    raise HTTPException(422, "Indica la resolución")
                case.resolution_text, case.resolved_at = body.resolution_text, now
            else:
                case.closed_at = now
            case.status = target
        after = snapshot(case)
        if operation == "content":
            after.update(titulo=case.titulo, descripcion=case.descripcion)
        case.updated_at = now
        event = AuditEvent(incidencia_id=case.id, usuario_id=actor.id, accion=action,
                         detalle={"operation": operation, "before": before, "after": after,
                                  "reason": getattr(body, "reason", None), "source": "HUMANA"})
        db.add(event)
        from app.services.mail import queue_event
        queue_event(db, case, event, before)
        # La API captura su esquema mientras la fila sigue cargada. Los demás
        # llamadores conservan el retorno ORM y la expiración habitual del commit.
        if presenter is None:
            result = case
        else:
            db.flush()
            result = presenter(case)
        db.commit()
        return result
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503, "No fue posible guardar la operación; no se guardaron cambios parciales") from None
    except Exception:
        # Un fallo al preparar la respuesta no debe dejar escritura parcial.
        db.rollback()
        raise
