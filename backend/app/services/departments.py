"""Administración auditada sin eliminación ni traslado masivo de personal."""
from fastapi import HTTPException
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import Department, DepartmentAudit, Incident, Role, User
from app.services.administration_lock import administration_lock


def gate(db, actor, exclusive=False):
    administration_lock(db, actor, exclusive=exclusive)
    if db.get(Role, actor.rol_id).nombre != "ADMIN_RH":
        raise HTTPException(403, "Se requiere Admin RH")


def view(row):
    return {"id": str(row.id), "nombre": row.nombre, "is_active": row.is_active}


def save_department(db, actor, body, department_id=None):
    try:
        gate(db, actor, exclusive=True)
        row = None
        if department_id is not None:
            row = db.scalar(select(Department).where(Department.id == department_id).with_for_update()
                            .execution_options(populate_existing=True))
            if row is None:
                raise HTTPException(404, "Departamento no encontrado")
        before = view(row) if row else None
        duplicate = select(Department.id).where(func.lower(Department.nombre) == func.lower(body.nombre))
        if row:
            duplicate = duplicate.where(Department.id != row.id)
        if db.scalar(duplicate) is not None:
            raise HTTPException(409, "Ya existe un departamento con ese nombre")
        if row and row.is_active and not body.is_active:
            if db.scalar(select(User.id).where(User.departamento_id == row.id, User.is_active.is_(True)).limit(1)):
                raise HTTPException(409, "Traslada o desactiva los usuarios activos antes de dar de baja el departamento")
            people = select(User.id).where(User.departamento_id == row.id)
            open_case = select(Incident.id).where(
                Incident.status.in_(["PENDIENTE", "EN_REVISION"]),
                or_(and_(Incident.scope == "ENTORNO", Incident.reported_department_id == row.id),
                    and_(Incident.scope == "PERSONA", Incident.affected_employee_id.in_(people)))
            ).limit(1)
            if db.scalar(open_case):
                raise HTTPException(409, "Atiende las incidencias abiertas vinculadas antes de dar de baja el departamento")
        if row is None:
            row = Department(nombre=body.nombre, is_active=True)
            db.add(row)
        else:
            row.nombre, row.is_active = body.nombre, body.is_active
        db.flush()
        result = view(row)
        db.add(DepartmentAudit(department_id=row.id, actor_id=actor.id, detalle={
            "operation": "CREADO" if before is None else "ACTUALIZADO",
            "reason": body.reason, "before": before, "after": result}))
        db.commit()
        return result
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Conflicto al guardar el departamento") from None
    except (HTTPException, SQLAlchemyError):
        db.rollback()
        raise
