"""Restricciones de acceso y revisión de relaciones, bajo bloqueo del caso."""
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models import AuditEvent, Department, Incident, IncidentParticipant, Role, User
from app.services.incidents import ACTIVE_RELATIONS, MANAGERS, role_name, visibility
from app.services.lifecycle import snapshot


def manager_involved(db, case):
    affected = db.get(User, case.affected_employee_id) if case.affected_employee_id else None
    if affected is not None and role_name(db, affected) in MANAGERS:
        return True
    return db.scalar(select(User.id).join(Role, User.rol_id == Role.id)
                     .join(IncidentParticipant, IncidentParticipant.user_id == User.id)
                     .where(IncidentParticipant.incidencia_id == case.id,
                            IncidentParticipant.review_status.in_(ACTIVE_RELATIONS),
                            Role.nombre.in_(MANAGERS)).limit(1)) is not None


def eligible(db, case, person):
    if person is None or not person.is_active or role_name(db, person) not in MANAGERS:
        return False
    department = db.get(Department, person.departamento_id)
    return bool(department and department.is_active and db.scalar(
        select(Incident.id).where(Incident.id == case.id, visibility(db, person))))


def protect_case(db, actor, case_id, operation, body, participant_id=None):
    try:
        from app.services.administration_lock import administration_lock
        administration_lock(db, actor)
        if role_name(db, actor) != "ADMIN_RH":
            raise HTTPException(403, "Solo Admin RH independiente")
        case = db.scalar(select(Incident).where(Incident.id == case_id).with_for_update()
                         .execution_options(populate_existing=True))
        if case is None or db.scalar(select(Incident.id).where(Incident.id == case_id, visibility(db, actor))) is None:
            raise HTTPException(404, "Incidencia no encontrada")
        if case.status not in {"PENDIENTE", "EN_REVISION"}:
            raise HTTPException(409, "Reabre el caso antes de modificar sus restricciones")
        before = snapshot(case)
        before["is_confidential"] = case.is_confidential
        now = datetime.now(timezone.utc)
        relation_before = relation_after = None
        if operation == "participant_add":
            person = db.get(User, body.user_id)
            department = db.get(Department, person.departamento_id) if person else None
            if person is None or not person.is_active or department is None or not department.is_active:
                raise HTTPException(422, "Participante no habilitado")
            if person.id == case.affected_employee_id or db.get(IncidentParticipant, (case.id, person.id)) is not None:
                raise HTTPException(409, "La relación ya existe o corresponde al afectado")
            # No permite reconstruir el expediente mediante incorporación masiva.
            from sqlalchemy import func
            count = db.scalar(select(func.count()).select_from(IncidentParticipant)
                              .where(IncidentParticipant.incidencia_id == case.id))
            if count >= 20:
                raise HTTPException(422, "Máximo de 20 participantes por caso")
            relation = IncidentParticipant(incidencia_id=case.id, user_id=person.id,
                                          declaration_reason=body.declaration_reason, review_status="DECLARADO")
            db.add(relation)
            participant_id = person.id
            relation_after = {"review_status": "DECLARADO", "declaration_reason": body.declaration_reason}
        elif operation == "participant_review":
            relation = db.get(IncidentParticipant, (case.id, participant_id))
            if relation is None:
                raise HTTPException(404, "Relación no encontrada")
            if participant_id == actor.id:
                raise HTTPException(403, "No puedes revisar tu propia relación")
            if relation.review_status == body.review_status:
                raise HTTPException(409, "La relación ya tiene ese estado")
            relation_before = {"review_status": relation.review_status,
                               "declaration_reason": relation.declaration_reason,
                               "reviewed_by": str(relation.reviewed_by) if relation.reviewed_by else None,
                               "reviewed_at": relation.reviewed_at.isoformat() if relation.reviewed_at else None,
                               "review_reason": relation.review_reason}
            relation.review_status = body.review_status
            relation.reviewed_by, relation.reviewed_at, relation.review_reason = actor.id, now, body.reason
            relation_after = {"review_status": body.review_status, "review_reason": body.reason,
                              "reviewed_by": str(actor.id), "reviewed_at": now.isoformat()}
        db.flush()
        involved = manager_involved(db, case)
        if operation == "confidentiality":
            if not body.is_confidential and involved:
                raise HTTPException(409, "No se puede retirar confidencialidad con gestor involucrado")
            case.is_confidential = body.is_confidential
        elif involved:
            case.is_confidential = True
        # Descartar una declaración nunca desmarca confidencialidad por sí solo.
        if case.is_confidential:
            case.ai_status = "OMITIDA"
            case.ai_skip_reason = "Confidencialidad o conflicto de interés; clasificación manual"
        db.flush()
        previous_assignee = db.get(User, case.assigned_to) if case.assigned_to else None
        requested_id = getattr(body, "assigned_to", None)
        if requested_id is not None:
            requested = db.get(User, requested_id)
            if not eligible(db, case, requested):
                raise HTTPException(422, "Responsable sin acceso independiente al caso")
            case.assigned_to = requested.id
        elif not eligible(db, case, previous_assignee):
            if case.status == "EN_REVISION":
                candidates = db.scalars(select(User).join(Role, User.rol_id == Role.id)
                                        .where(Role.nombre == "ADMIN_RH", User.is_active.is_(True))
                                        .order_by(User.id)).all()
                replacement = next((person for person in candidates if eligible(db, case, person)), None)
                if replacement:
                    case.assigned_to = replacement.id
                else:
                    case.status = "PENDIENTE"
                    case.assigned_to = None
                    case.cycle_start_at = None
            else:
                case.assigned_to = None
        after = snapshot(case)
        after["is_confidential"] = case.is_confidential
        case.updated_at = now
        event = AuditEvent(incidencia_id=case.id, usuario_id=actor.id, accion="CAMBIO_CONFIDENCIALIDAD",
                         detalle={"operation": operation, "reason": getattr(body, "reason", None) or getattr(body, "declaration_reason", None),
                                  "participant_id": str(participant_id) if participant_id else None,
                                  "relation_before": relation_before, "relation_after": relation_after,
                                  "before": before, "after": after})
        db.add(event)
        from app.services.mail import queue_event
        queue_event(db, case, event, before)
        db.commit()
        can_view = db.scalar(select(Incident.id).where(Incident.id == case.id, visibility(db, actor))) is not None
        return {"id": case.id, "received": True, "can_view": can_view}
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503, "No fue posible guardar la protección; no se guardaron cambios parciales") from None
