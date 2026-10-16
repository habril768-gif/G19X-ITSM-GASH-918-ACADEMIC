"""API de registro, listado y detalle con filtros sobre el conjunto autorizado."""
from datetime import date, datetime, time, timedelta, timezone
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.core.security import current_user
from app.models import AuditEvent, Category, Department, Incident, IncidentParticipant, Role, User
from app.services.incidents import create_case, role_name, visibility, visible_case

router=APIRouter(prefix="/incidents",tags=["Incidencias"])


class ParticipantInput(BaseModel):
    model_config=ConfigDict(extra="forbid")
    user_id: UUID
    declaration_reason: str=Field(min_length=1,max_length=2000)
    @field_validator("declaration_reason")
    @classmethod
    def reason_not_blank(cls,value):
        if not value.strip(): raise ValueError("El motivo no puede estar vacío")
        return value.strip()


class IncidentInput(BaseModel):
    model_config=ConfigDict(extra="forbid")
    titulo: str=Field(min_length=1,max_length=200)
    descripcion: str=Field(min_length=1,max_length=10000)
    incident_date: date
    scope: Literal["PERSONA","ENTORNO"]="PERSONA"
    affected_employee_id: UUID|None=None
    reported_department_id: UUID|None=None
    is_confidential: bool=False
    participants: list[ParticipantInput]=Field(default_factory=list,max_length=20)
    @field_validator("titulo","descripcion")
    @classmethod
    def not_blank(cls,value):
        if not value.strip(): raise ValueError("El texto no puede estar vacío")
        return value.strip()


class Receipt(BaseModel):
    id: UUID
    received: bool
    can_view: bool


class CaseSummary(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: UUID
    titulo: str
    scope: str
    status: str
    priority: int|None
    category_id: int|None
    assigned_to: UUID|None
    is_confidential: bool
    classification_valid: bool
    created_at: datetime


class CaseDetail(CaseSummary):
    descripcion: str
    incident_date: date
    affected_employee_id: UUID|None
    created_by: UUID
    reported_department_id: UUID
    department_id_at_creation: UUID
    ai_status: str
    ai_suggestion: dict|None
    ai_skip_reason: str|None
    validated_by: UUID|None
    validated_at: datetime|None
    resolution_text: str|None
    resolved_at: datetime|None
    closed_at: datetime|None


class CasePage(BaseModel):
    items: list[CaseSummary]
    total: int
    page: int
    page_size: int


@router.get("/options")
def options(response:Response,user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    role=role_name(db,user)
    base=select(User.id,User.nombre_completo,User.departamento_id,Role.nombre.label("rol")).join(Role,User.rol_id==Role.id).join(Department,User.departamento_id==Department.id).where(User.is_active.is_(True),Department.is_active.is_(True))
    people=db.execute(base.where(or_(role=="ADMIN_RH",User.departamento_id==user.departamento_id,Role.nombre.in_(["ADMIN_RH","SUPERVISOR"])))).mappings().all()
    affected=[r for r in people if role=="ADMIN_RH" or (role=="SUPERVISOR" and r["departamento_id"]==user.departamento_id) or (role=="EMPLEADO" and r["id"]==user.id)]
    deps=db.execute(select(Department.id,Department.nombre).where(Department.is_active.is_(True),or_(role=="ADMIN_RH",Department.id==user.departamento_id))).mappings().all()
    categories=db.execute(select(Category.id,Category.nombre).order_by(Category.id)).mappings().all()
    return {"affected_employees":affected,"participants":people,"departments":deps,"categories":categories}


@router.post("",status_code=201,response_model=Receipt)
def register(body:IncidentInput,response:Response,user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    return create_case(db,user,body)


@router.get("",response_model=CasePage)
def list_cases(response:Response,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100),
               status:Literal["PENDIENTE","EN_REVISION","RESUELTA","CERRADA"]|None=None,
               priority:int|None=Query(None,ge=1,le=3),category_id:int|None=Query(None,ge=1),assigned_to:UUID|None=None,
               created_from:date|None=None,created_to:date|None=None,q:str|None=Query(None,max_length=200),
               user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    conditions=[visibility(db,user)]
    for field,value in [(Incident.status,status),(Incident.priority,priority),(Incident.category_id,category_id),(Incident.assigned_to,assigned_to)]:
        if value is not None: conditions.append(field==value)
    if created_from and created_to and created_from>created_to:raise HTTPException(422,"Rango de fechas inválido")
    if created_from:conditions.append(Incident.created_at>=datetime.combine(created_from,time.min,tzinfo=timezone.utc))
    if created_to:conditions.append(Incident.created_at<=datetime.combine(created_to,time.max,tzinfo=timezone.utc))
    if q and q.strip():
        title=Incident.titulo.icontains(q.strip(),autoescape=True)
        try:match=or_(Incident.id==UUID(q.strip()),title)
        except ValueError:match=title
        conditions.append(match)
    total=db.scalar(select(func.count()).select_from(Incident).where(*conditions))
    items=db.scalars(select(Incident).where(*conditions).order_by(Incident.created_at.desc(),Incident.id.desc()).offset((page-1)*page_size).limit(page_size)).all()
    return {"items":items,"total":total,"page":page,"page_size":page_size}


@router.get("/{case_id}",response_model=CaseDetail)
def detail(case_id:UUID,response:Response,user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    return visible_case(db,user,case_id)


@router.get("/{case_id}/participants")
def participants(case_id:UUID,response:Response,user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    visible_case(db,user,case_id)
    # Un empleado no recibe relaciones de terceros ni motivos de revisión.
    if role_name(db,user)=="EMPLEADO":return {"items":[]}
    rows=db.scalars(select(IncidentParticipant).where(IncidentParticipant.incidencia_id==case_id).order_by(IncidentParticipant.user_id)).all()
    return {"items":[{"user_id":r.user_id,"review_status":r.review_status,"declaration_reason":r.declaration_reason,"reviewed_by":r.reviewed_by,"reviewed_at":r.reviewed_at,"review_reason":r.review_reason} for r in rows]}


@router.get("/{case_id}/history")
def history(case_id:UUID,response:Response,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100),user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    visible_case(db,user,case_id)
    # Las copias anteriores pueden contener participantes o texto ya restringido.
    limited=role_name(db,user)=="EMPLEADO"
    predicate=AuditEvent.incidencia_id==case_id
    total=db.scalar(select(func.count()).select_from(AuditEvent).where(predicate))
    rows=db.scalars(select(AuditEvent).where(predicate).order_by(AuditEvent.fecha.desc(),AuditEvent.id.desc()).offset((page-1)*page_size).limit(page_size)).all()
    return {"items":[({"id":r.id,"accion":r.accion,"fecha":r.fecha} if limited else {"id":r.id,"accion":r.accion,"usuario_id":r.usuario_id,"detalle":r.detalle,"fecha":r.fecha}) for r in rows],"total":total,"page":page,"page_size":page_size}
