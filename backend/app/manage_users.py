"""Operaciones locales del administrador del servidor, con contraseña interactiva."""
import argparse
from getpass import GetPassWarning, getpass
import warnings

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_engine
from app.core.security import hash_password, normalize_email, revoke_sessions
from app.models import AuditEvent, Department, LocalCredential, LoginThrottle, Role, User


def main():
    parser = argparse.ArgumentParser(description="Operaciones del operador: administradores locales y recuperación")
    parser.add_argument("action", choices=["bootstrap-admin", "provision-independent-admin", "set-password"])
    parser.add_argument("--email", required=True)
    parser.add_argument("--name", default="Administrador RH")
    parser.add_argument("--department", default="Recursos Humanos")
    parser.add_argument("--reason", help="Motivo administrativo obligatorio para un RH independiente adicional; sin datos del expediente")
    args = parser.parse_args()
    try:
        email = normalize_email(args.email)
        if not args.name.strip() or len(args.name.strip()) > 200 or not args.department.strip() or len(args.department.strip()) > 120:
            raise ValueError("Nombre o departamento vacío o demasiado largo")
        reason = args.reason.strip() if args.reason else None
        if args.action == "provision-independent-admin" and (not reason or len(reason) > 2000):
            raise ValueError("Indica --reason con motivo administrativo de 1 a 2000 caracteres")
        # getpass debe fallar antes del fallback que puede mostrar la contraseña.
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            raw = getpass("Nueva contraseña (12-128 caracteres; no se muestra): ")
            repeated = getpass("Repetir contraseña: ")
        if raw != repeated:
            print("Las contraseñas no coinciden; no hubo cambios.")
            return 1
        encoded = hash_password(raw)
        del raw, repeated
        with Session(get_engine()) as db, db.begin():
            if args.action in {"bootstrap-admin", "provision-independent-admin"}:
                # Serializa el bootstrap en PostgreSQL para evitar dos administradores iniciales concurrentes.
                if db.bind.dialect.name == "postgresql":
                    from sqlalchemy import text
                    db.execute(text("SELECT pg_advisory_xact_lock(71419322)"))
                existing = db.scalar(select(LocalCredential.user_id).join(User).join(Role, User.rol_id == Role.id).where(Role.nombre == "ADMIN_RH").limit(1))
                if args.action == "bootstrap-admin" and existing is not None:
                    raise ValueError("Ya existe un administrador local; usa la sesión de Admin RH")
                if args.action == "provision-independent-admin" and existing is None:
                    raise ValueError("No existe administrador local inicial; usa bootstrap-admin")
                role = db.scalar(select(Role).where(Role.nombre == "ADMIN_RH"))
                if role is None:
                    raise ValueError("Primero aplica las migraciones")
                user = db.scalar(select(User).where(func.lower(User.email) == email))
                if user is not None:
                    raise ValueError("El correo ya existe; esta operación no modifica cuentas existentes")
                department = db.scalar(select(Department).where(Department.nombre == args.department.strip()))
                if department is None:
                    department = Department(nombre=args.department.strip(), is_active=True)
                    db.add(department)
                    db.flush()
                if not department.is_active:
                    raise ValueError("Departamento inactivo")
                user = User(email=email, nombre_completo=args.name.strip(), departamento_id=department.id, rol_id=role.id, is_active=True)
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
            detail = {"operacion": args.action, "origen": "OPERADOR_SERVIDOR"}
            if args.action == "provision-independent-admin":
                detail.update(motivo=reason, rol="ADMIN_RH", departamento_id=str(user.departamento_id))
            db.add(AuditEvent(affected_user_id=user.id, usuario_id=None, accion="USUARIO_ACTUALIZADO", detalle=detail))
        print("Operación completada. Contraseña no mostrada; sesiones previas revocadas.")
        return 0
    except (GetPassWarning, EOFError, OSError):
        print("No se pudo leer una contraseña privada. Ejecuta desde una terminal interactiva; no hubo cambios.")
        return 1
    except ValueError as exc:
        print(str(exc))
        return 1
    except SQLAlchemyError:
        print("Operación revertida. Verifica migración, conexión y conflictos de datos; no hubo cambios parciales.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
