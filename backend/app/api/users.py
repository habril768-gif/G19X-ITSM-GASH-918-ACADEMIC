"""Administración de cuentas: directorio limitado a RH y actualización auditada."""
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import admin_user
from app.models import Department, Role, User
from app.services.users import update_user

router = APIRouter(prefix="/users", tags=["Usuarios"])


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre_completo: str = Field(min_length=1, max_length=200)
    departamento_id: UUID
    rol_id: int = Field(ge=1, le=3)
    is_active: bool
    reason: str = Field(min_length=1, max_length=2000)

    @field_validator("nombre_completo", "reason")
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError("El texto no puede estar vacío")
        return value.strip()


@router.get("/options")
def options(response: Response, admin: User = Depends(admin_user), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    return {"roles": db.execute(select(Role.id, Role.nombre).order_by(Role.id)).mappings().all(),
            "departments": db.execute(select(Department.id, Department.nombre)
                                      .where(Department.is_active.is_(True)).order_by(Department.nombre)).mappings().all()}


@router.get("")
def users(response: Response, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
          admin: User = Depends(admin_user), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    people = db.scalars(select(User).order_by(User.nombre_completo, User.id)
                        .offset((page-1)*page_size).limit(page_size)).all()
    return {"items": [{"id": p.id, "email": p.email, "nombre_completo": p.nombre_completo,
                       "departamento_id": p.departamento_id, "rol_id": p.rol_id, "is_active": p.is_active}
                      for p in people],
            "total": db.scalar(select(func.count()).select_from(User)), "page": page, "page_size": page_size}


@router.put("/{user_id}")
def edit_user(user_id: UUID, body: UserUpdate, response: Response,
              admin: User = Depends(admin_user), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    return update_user(db, admin, user_id, body)
