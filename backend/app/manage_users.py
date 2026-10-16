"""Operaciones locales del administrador del servidor, con contraseña interactiva."""
import argparse
from getpass import getpass

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_engine
from app.core.security import hash_password, normalize_email, revoke_sessions
from app.models import AuditEvent, Department, LocalCredential, LoginThrottle, Role, User


def main():
    parser = argparse.ArgumentParser(description="Provisionar primer Admin RH o restablecer contraseña local")
    parser.add_argument("action", choices=["bootstrap-admin", "set-password"])
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", default="Administrador RH")
    parser.add_argument("--department", default="Recursos Humanos")
    args = parser.parse_args()
    try:
        email = normalize_email(args.email)
        raw = getpass("Nueva contraseña (12-128 caracteres; no se muestra): ")
        if raw != getpass("Repetir contraseña: "):
            print("Las contraseñas no coinciden; no hubo cambios.")
            return 1
        encoded = hash_password(raw)
        del raw
        with Session(get_engine()) as db, db.begin():
            if args.action == "bootstrap-admin":
                # Serializa el bootstrap en PostgreSQL para evitar dos administradores iniciales concurrentes.
                if db.bind.dialect.name == "postgresql":
                    from sqlalchemy import text
                    db.execute(text("SELECT pg_advisory_xact_lock(71419322)"))
                existing = db.scalar(select(LocalCredential.user_id).join(User).join(Role, User.rol_id == Role.id).where(Role.nombre == "ADMIN_RH").limit(1))
                if existing is not None:
                    raise ValueError("Ya existe un administrador local; usa la sesión de Admin RH")
                role = db.scalar(select(Role).where(Role.nombre == "ADMIN_RH"))
                if role is None:
                    raise ValueError("Primero aplica las migraciones")
                user = db.scalar(select(User).where(func.lower(User.email) == email))
                if user is not None:
                    raise ValueError("El correo ya existe; bootstrap no modifica cuentas existentes")
                department = db.scalar(select(Department).where(Department.nombre == args.department))
                if department is None:
                    department = Department(nombre=args.department, is_active=True)
                    db.add(department)
                    db.flush()
                if not department.is_active:
                    raise ValueError("Departamento inactivo")
                user = User(email=email, nombre_completo=args.name, departamento_id=department.id, rol_id=role.id, is_active=True)
                db.add(user)
                db.flush()
            else:
                user = db.scalar(select(User).where(func.lower(User.email) == email))
                if user is None or not user.is_active:
                    raise ValueError("Usuario no encontrado o inactivo")
            credential = db.get(LocalCredential, user.id)
            if credential is None:
                db.add(LocalCredential(user_id=user.id, password_hash=encoded))
            else:
                credential.password_hash = encoded
            revoke_sessions(db, user.id)
            throttle = db.get(LoginThrottle, email)
            if throttle:
                throttle.failures = 0
                throttle.locked_until = None
            db.add(AuditEvent(affected_user_id=user.id, usuario_id=None, accion="USUARIO_ACTUALIZADO", detalle={"operacion": args.action, "origen": "OPERADOR_SERVIDOR"}))
        print("Operación completada. Contraseña no mostrada; sesiones previas revocadas.")
        return 0
    except ValueError as exc:
        print(str(exc))
        return 1
    except SQLAlchemyError:
        print("Operación revertida. Verifica migración, conexión y conflictos de datos; no hubo cambios parciales.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
