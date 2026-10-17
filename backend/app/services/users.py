"""Cambios de usuario y protección de casos en una única transacción."""
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.security import revoke_sessions, utcnow
from app.models import AuditEvent, Department, Incident, LocalCredential, Role, User
from app.services.administration_lock import administration_lock
from app.services.incidents import role_name, visibility
from app.services.lifecycle import snapshot
from app.services.protection import eligible, manager_involved


def update_user(db, actor, user_id, body):
    try:
        administration_lock(db, actor, exclusive=True)
        if role_name(db, actor) != "ADMIN_RH":
            raise HTTPException(403, "Se requiere Admin RH")
        target = db.scalar(select(User).where(User.id == user_id).with_for_update()
                           .execution_options(populate_existing=True))
        if target is None:
            raise HTTPException(404, "Usuario no encontrado")
        department = db.get(Department, body.departamento_id)
        if department is None or not department.is_active or db.get(Role, body.rol_id) is None:
            raise HTTPException(422, "Departamento o rol no válido")
        before = {"nombre_completo": target.nombre_completo, "rol_id": target.rol_id,
                  "departamento_id": str(target.departamento_id), "is_active": target.is_active}
        access_changed = (target.rol_id != body.rol_id or target.departamento_id != body.departamento_id
                          or target.is_active != body.is_active)
        cases = []
        visible_before = set()
        if access_changed:
            # En el MVP se recorren todos los casos bajo bloqueo administrativo.
            # No se expone su contenido en la respuesta de administración.
            visible_before = set(db.scalars(select(Incident.id).where(visibility(db, actor))).all())
            cases = db.scalars(select(Incident).order_by(Incident.id).with_for_update()
                               .execution_options(populate_existing=True)).all()
        target.nombre_completo = body.nombre_completo
        target.rol_id, target.departamento_id, target.is_active = body.rol_id, body.departamento_id, body.is_active
        db.flush()
        local_admin = db.scalar(select(User.id).join(Role, User.rol_id == Role.id)
                                .join(Department, User.departamento_id == Department.id)
                                .join(LocalCredential, LocalCredential.user_id == User.id)
                                .where(User.is_active.is_(True), Department.is_active.is_(True),
                                       Role.nombre == "ADMIN_RH").limit(1))
        if local_admin is None:
            raise HTTPException(409, "Debe conservarse al menos un Admin RH activo con acceso local")
        if access_changed:
            revoke_sessions(db, target.id)
        now = utcnow()
        adjusted = 0
        for case in cases:
            previous = snapshot(case)
            previous["is_confidential"] = case.is_confidential
            make_private = manager_involved(db, case) and not case.is_confidential
            if make_private:
                case.is_confidential = True
                case.ai_status = "OMITIDA"
                case.ai_skip_reason = "Cambio administrativo: gestor involucrado; clasificación manual"
                db.flush()
            assigned = db.get(User, case.assigned_to) if case.assigned_to else None
            invalid_assignment = case.assigned_to is not None and not eligible(db, case, assigned)
            if not make_private and not invalid_assignment:
                continue
            # Nunca se corrigen restricciones de un caso oculto al administrador.
            if case.id not in visible_before:
                raise HTTPException(409, "El cambio requiere un Admin RH independiente para revisar casos restringidos")
            if case.status in {"RESUELTA", "CERRADA"}:
                raise HTTPException(409, "Reabre y revisa los casos finalizados afectados antes del cambio")
            if invalid_assignment:
                if case.status == "PENDIENTE":
                    case.assigned_to = None
                else:
                    admins = db.scalars(select(User).join(Role, User.rol_id == Role.id)
                                        .where(Role.nombre == "ADMIN_RH", User.is_active.is_(True)).order_by(User.id)).all()
                    replacement = next((user for user in admins if eligible(db, case, user)), None)
                    if replacement:
                        case.assigned_to = replacement.id
                    elif case.is_confidential:
                        case.status, case.assigned_to, case.cycle_start_at = "PENDIENTE", None, None
                    else:
                        raise HTTPException(409, "Asigna un responsable elegible antes de realizar este cambio")
            case.updated_at = now
            after = snapshot(case)
            after["is_confidential"] = case.is_confidential
            db.add(AuditEvent(incidencia_id=case.id, affected_user_id=target.id, usuario_id=actor.id,
                              accion="CAMBIO_CONFIDENCIALIDAD" if make_private else "ASIGNADO",
                              detalle={"operation": "USER_ACCESS_REVIEW", "reason": body.reason,
                                       "before": previous, "after": after}))
            db.flush()
            adjusted += 1
        after_user = {"nombre_completo": target.nombre_completo, "rol_id": target.rol_id,
                      "departamento_id": str(target.departamento_id), "is_active": target.is_active}
        db.add(AuditEvent(affected_user_id=target.id, usuario_id=actor.id, accion="USUARIO_ACTUALIZADO",
                          detalle={"operacion": "ACTUALIZACION_ADMIN", "reason": body.reason,
                                   "before": before, "after": after_user, "sessions_revoked": access_changed,
                                   "cases_adjusted": adjusted}))
        result = {"id": target.id, "updated": True, "sessions_revoked": access_changed,
                  "cases_adjusted": adjusted}
        db.commit()
        return result
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503, "No fue posible actualizar el usuario; no se guardaron cambios parciales") from None
