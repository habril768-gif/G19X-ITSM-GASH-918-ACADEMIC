"""Contratos HTTP para sesiones locales y administración inicial de usuarios."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import admin_user, bearer, current_user, hash_password, login, normalize_email, password_hasher, revoke_sessions, token_digest, utcnow
from app.models import AuditEvent, AuthSession, Department, LocalCredential, Role, User

router = APIRouter(tags=["Autenticación"])


class LoginInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=3, max_length=320)
    password: SecretStr = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def email_normalized(cls, value):
        return normalize_email(value)


class PasswordChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_password: SecretStr = Field(min_length=1, max_length=128)
    new_password: SecretStr = Field(min_length=12, max_length=128)


class CreateUser(LoginInput):
    password: SecretStr = Field(min_length=12, max_length=128)
    nombre_completo: str = Field(min_length=1, max_length=200)
    departamento_id: UUID
    rol_id: int = Field(ge=1, le=3)


def user_view(user: User, db: Session):
    role = db.get(Role, user.rol_id)
    return {"id": str(user.id), "email": user.email, "nombre_completo": user.nombre_completo,
            "departamento_id": str(user.departamento_id), "rol": role.nombre if role else None}


@router.post("/auth/login")
def sign_in(body: LoginInput, response: Response, db: Session = Depends(get_session)):
    token = login(db, body.email, body.password.get_secret_value())
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


@router.get("/auth/me")
def me(response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    return user_view(user, db)


@router.post("/auth/logout", status_code=204)
def sign_out(user: User = Depends(current_user), credentials=Depends(bearer), db: Session = Depends(get_session)):
    session = db.get(AuthSession, token_digest(credentials.credentials))
    session.revoked_at = utcnow()
    db.commit()
    return Response(status_code=204)


@router.post("/auth/change-password", status_code=204)
def change_password(body: PasswordChange, user: User = Depends(current_user), db: Session = Depends(get_session)):
    credential = db.get(LocalCredential, user.id)
    if credential is None or not password_hasher.verify(body.current_password.get_secret_value(), credential.password_hash):
        raise HTTPException(400, "Contraseña actual incorrecta")
    try:
        credential.password_hash = hash_password(body.new_password.get_secret_value())
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
    revoke_sessions(db, user.id)
    db.add(AuditEvent(affected_user_id=user.id, usuario_id=user.id, accion="USUARIO_ACTUALIZADO", detalle={"operacion": "CAMBIO_CONTRASENA"}))
    db.commit()
    return Response(status_code=204)


@router.post("/users", status_code=201, tags=["Usuarios"])
def create_user(body: CreateUser, admin: User = Depends(admin_user), db: Session = Depends(get_session)):
    from app.services.administration_lock import administration_lock
    administration_lock(db, admin, exclusive=True)
    if db.get(Role, admin.rol_id).nombre != "ADMIN_RH":
        raise HTTPException(403, "Se requiere Admin RH")
    department = db.get(Department, body.departamento_id)
    if not department or not department.is_active or db.get(Role, body.rol_id) is None:
        raise HTTPException(422, "Departamento o rol no válido")
    try:
        encoded = hash_password(body.password.get_secret_value())
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from None
    user = User(email=body.email, nombre_completo=body.nombre_completo, departamento_id=body.departamento_id, rol_id=body.rol_id, is_active=True)
    try:
        db.add(user)
        db.flush()
        db.add(LocalCredential(user_id=user.id, password_hash=encoded))
        db.add(AuditEvent(affected_user_id=user.id, usuario_id=admin.id, accion="USUARIO_ACTUALIZADO", detalle={"operacion": "ALTA_LOCAL", "rol_id": user.rol_id}))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "El correo ya está registrado o existe un conflicto de datos") from None
    return user_view(user, db)
