"""Autenticación local: Argon2id y sesiones revocables con token opaco."""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.models import AuthSession, Department, LocalCredential, LoginThrottle, Role, User

password_hasher = PasswordHash.recommended()
DUMMY_HASH = password_hasher.hash("dummy-verification-only-not-an-account")
bearer = HTTPBearer(auto_error=False)
SESSION_LIFETIME = timedelta(hours=1)


def utcnow():
    return datetime.now(timezone.utc)


def aware(value):
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def normalize_email(email: str) -> str:
    value = email.strip().lower()
    if len(value) > 320 or value.count("@") != 1 or any(c.isspace() for c in value):
        raise ValueError("Correo no válido")
    local, domain = value.split("@")
    if not local or not domain or "." not in domain:
        raise ValueError("Correo no válido")
    return value


def hash_password(password: str) -> str:
    if not 12 <= len(password) <= 128 or password.isspace():
        raise ValueError("La contraseña debe tener entre 12 y 128 caracteres")
    return password_hasher.hash(password)


def token_digest(token: str) -> str:
    return sha256(token.encode()).hexdigest()


def revoke_sessions(db: Session, user_id):
    db.execute(update(AuthSession).where(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None)).values(revoked_at=utcnow()))


def login(db: Session, email: str, password: str) -> str:
    email = normalize_email(email)
    # La fila de intentos se crea de forma concurrente sin sobrescribir contadores.
    insert = pg_insert if db.bind.dialect.name == "postgresql" else sqlite_insert
    db.execute(insert(LoginThrottle).values(email=email, failures=0).on_conflict_do_nothing(index_elements=["email"]))
    throttle = db.scalar(select(LoginThrottle).where(LoginThrottle.email == email).with_for_update())
    now = utcnow()
    if throttle.locked_until:
        if aware(throttle.locked_until) > now:
            db.commit()
            raise HTTPException(401, "Credenciales inválidas o acceso temporalmente bloqueado")
        throttle.locked_until = None
        throttle.failures = 0
    user = db.scalar(select(User).where(func.lower(User.email) == email))
    credential = db.get(LocalCredential, user.id) if user else None
    valid, updated_hash = password_hasher.verify_and_update(password, credential.password_hash if credential else DUMMY_HASH)
    department = db.get(Department, user.departamento_id) if user else None
    role = db.get(Role, user.rol_id) if user else None
    if not valid or not user or not user.is_active or not credential or not department or not department.is_active or not role:
        throttle.failures += 1
        if throttle.failures >= 5:
            throttle.locked_until = now + timedelta(minutes=15)
        db.commit()
        raise HTTPException(401, "Credenciales inválidas o acceso temporalmente bloqueado")
    if updated_hash is not None:
        credential.password_hash = updated_hash
    throttle.failures = 0
    throttle.locked_until = None
    raw = secrets.token_urlsafe(32)
    db.add(AuthSession(token_hash=token_digest(raw), user_id=user.id, expires_at=now + SESSION_LIFETIME))
    db.commit()
    return raw


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_session)) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer" or len(credentials.credentials) > 256:
        raise HTTPException(401, "Sesión requerida", headers={"WWW-Authenticate": "Bearer"})
    session = db.get(AuthSession, token_digest(credentials.credentials))
    if session is None or session.revoked_at is not None or aware(session.expires_at) <= utcnow():
        raise HTTPException(401, "Sesión inválida o expirada", headers={"WWW-Authenticate": "Bearer"})
    user = db.get(User, session.user_id)
    department = db.get(Department, user.departamento_id) if user else None
    if not user or not user.is_active or not department or not department.is_active:
        raise HTTPException(403, "Cuenta no habilitada")
    return user


def admin_user(user: User = Depends(current_user), db: Session = Depends(get_session)) -> User:
    role = db.get(Role, user.rol_id)
    if role is None or role.nombre != "ADMIN_RH":
        raise HTTPException(403, "Se requiere Admin RH")
    return user
