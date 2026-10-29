"""Coordina cambios administrativos con mutaciones de expedientes en PostgreSQL."""
from fastapi import HTTPException
from sqlalchemy import inspect as sa_inspect, select, text
from app.models import Department, Role, User


def administration_lock(db, actor=None, exclusive=False, *, include_role=False, include_department=False):
    # Los llamadores anteriores conservan retorno None. Solo quien lo solicita
    # recibe el rol leído bajo este mismo bloqueo, sin caché entre operaciones.
    if include_department and not include_role:
        raise ValueError("El departamento requiere incluir el rol validado")
    if include_role and actor is None:
        raise ValueError("Se requiere actor para releer el rol")
    if db.bind.dialect.name == "postgresql":
        function = "pg_advisory_xact_lock" if exclusive else "pg_advisory_xact_lock_shared"
        db.execute(text(f"SELECT {function}(71419322)"))
    if actor is not None:
        # Leer después de adquirir el bloqueo. populate_existing descarta los
        # valores obsoletos de usuario/departamento que hubiera en la sesión.
        state = sa_inspect(actor)
        identity = state.identity
        if identity is None or state.session is not db:
            raise HTTPException(403, "Cuenta no habilitada")
        columns = (User, Department, Role.nombre) if include_role else (User, Department)
        statement = select(*columns).select_from(User).outerjoin(Department, Department.id == User.departamento_id)
        if include_role:
            statement = statement.outerjoin(Role, Role.id == User.rol_id)
        row = db.execute(statement.where(User.id == identity[0])
                         .execution_options(populate_existing=True)).one_or_none()
        person, department = row[:2] if row is not None else (None, None)
        if person is None or not person.is_active or department is None or not department.is_active:
            raise HTTPException(403, "Cuenta no habilitada")
        if include_role:
            role = row[2]
            if role not in {"ADMIN_RH", "SUPERVISOR", "EMPLEADO"}:
                raise HTTPException(403, "Rol no habilitado")
            # Referencia local al departamento recién revalidado, bajo el mismo
            # bloqueo. No se conserva en sesión.info ni entre operaciones.
            return (role, department) if include_department else role
