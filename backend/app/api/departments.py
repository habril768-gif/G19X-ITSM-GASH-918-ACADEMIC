"""Catálogo e historial de departamentos exclusivos de Admin RH."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import admin_user
from app.models import Department, DepartmentAudit
from app.services.departments import gate, save_department, view

router = APIRouter(prefix="/departments", tags=["Departamentos"])


class DepartmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre: str = Field(min_length=1, max_length=120)
    reason: str = Field(min_length=1, max_length=2000)

    @field_validator("nombre", "reason")
    @classmethod
    def not_blank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El texto no puede estar vacío")
        return value


class DepartmentUpdate(DepartmentCreate):
    is_active: bool


@router.get("")
def listing(response: Response, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
            admin=Depends(admin_user), db: Session = Depends(get_session)):
    gate(db, admin)
    response.headers["Cache-Control"] = "no-store"
    rows = db.scalars(select(Department).order_by(Department.nombre, Department.id)
                      .offset((page - 1) * page_size).limit(page_size)).all()
    return {"items": [view(row) for row in rows], "total": db.scalar(select(func.count()).select_from(Department)), "page": page, "page_size": page_size}


@router.post("", status_code=201)
def create(body: DepartmentCreate, response: Response, admin=Depends(admin_user), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    return save_department(db, admin, body)


@router.put("/{department_id}")
def update(department_id: UUID, body: DepartmentUpdate, response: Response,
           admin=Depends(admin_user), db: Session = Depends(get_session)):
    response.headers["Cache-Control"] = "no-store"
    return save_department(db, admin, body, department_id)


@router.get("/{department_id}/history")
def history(department_id: UUID, response: Response, page: int = Query(1, ge=1),
            page_size: int = Query(20, ge=1, le=100), admin=Depends(admin_user), db: Session = Depends(get_session)):
    gate(db, admin)
    response.headers["Cache-Control"] = "no-store"
    if db.get(Department, department_id) is None:
        raise HTTPException(404, "Departamento no encontrado")
    condition = DepartmentAudit.department_id == department_id
    rows = db.scalars(select(DepartmentAudit).where(condition).order_by(DepartmentAudit.fecha.desc(), DepartmentAudit.id.desc())
                      .offset((page - 1) * page_size).limit(page_size)).all()
    return {"items": [{"id": row.id, "actor_id": row.actor_id, "fecha": row.fecha, "detalle": row.detalle} for row in rows],
            "total": db.scalar(select(func.count()).select_from(DepartmentAudit).where(condition)), "page": page, "page_size": page_size}
