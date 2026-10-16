"""Carga explícita de datos ficticios; no configura autenticación."""
import argparse
import os
from uuid import UUID, uuid5

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_engine
from app.models import Department, Role, User

NAMESPACE = UUID("0fc81ca4-5a74-4d8c-bb44-a6cdd9c96e42")
TENANT = uuid5(NAMESPACE, "demo-tenant")
DEPARTMENTS = ["DEMO - Recursos Humanos", "DEMO - Operaciones"]
ACCOUNTS = [
    ("admin", "Admin RH Demo", 1, 0),
    ("supervisor-rh", "Supervisor RH Demo", 2, 0),
    ("supervisor-operaciones", "Supervisor Operaciones Demo", 2, 1),
    ("empleado-rh", "Empleado RH Demo", 3, 0),
    ("empleado-operaciones-1", "Empleado Operaciones Uno Demo", 3, 1),
    ("empleado-operaciones-2", "Empleado Operaciones Dos Demo", 3, 1),
]


def seed_demo(session: Session) -> dict[str, int]:
    """El llamador administra la transacción; no modifica registros existentes."""
    for role_id, name in [(1, "ADMIN_RH"), (2, "SUPERVISOR"), (3, "EMPLEADO")]:
        role = session.get(Role, role_id)
        if role is None or role.nombre != name:
            raise ValueError("Primero aplica la migración con los roles iniciales")
    created_departments = created_users = 0
    department_ids = []
    for name in DEPARTMENTS:
        key = uuid5(NAMESPACE, name)
        department_ids.append(key)
        current = session.get(Department, key)
        if current is None:
            session.add(Department(id=key, nombre=name, is_active=True))
            created_departments += 1
        elif current.nombre != name:
            raise ValueError("Conflicto con un identificador reservado para DEMO")
    session.flush()
    for slug, name, role_id, department_index in ACCOUNTS:
        key = uuid5(NAMESPACE, slug)
        external_id = uuid5(NAMESPACE, "oid:" + slug)
        current = session.get(User, key)
        if current is not None:
            if current.tenant_id != TENANT or current.external_id != external_id:
                raise ValueError("Conflicto con un identificador reservado para DEMO")
            continue
        session.add(User(
            id=key, email=slug + "@example.invalid", external_id=external_id,
            tenant_id=TENANT, nombre_completo=name,
            departamento_id=department_ids[department_index], rol_id=role_id,
            is_active=True,
        ))
        created_users += 1
    session.flush()
    return {"departamentos_creados": created_departments, "usuarios_creados": created_users}


def main() -> int:
    parser = argparse.ArgumentParser(description="Cargar dos departamentos y seis usuarios ficticios de QA")
    parser.add_argument("--confirm-demo", action="store_true", required=True,
                        help="Confirmar que la base es de desarrollo/pruebas")
    parser.parse_args()
    if os.environ.get("APP_ENV", "development").lower() not in {"development", "test"}:
        print("Carga rechazada: entorno no habilitado para datos DEMO")
        return 1
    try:
        with Session(get_engine()) as session, session.begin():
            result = seed_demo(session)
    except (ValueError, SQLAlchemyError):
        print("No se cargaron datos: verifica configuración, migración y conflictos DEMO. Transacción revertida.")
        return 1
    print("Carga DEMO completada: " + ", ".join(f"{k}={v}" for k, v in result.items()))
    print("Datos ficticios; no permiten iniciar sesión con Microsoft Entra ID.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
