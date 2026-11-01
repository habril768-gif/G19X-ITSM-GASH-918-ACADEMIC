"""API de registro, listado y detalle con filtros sobre el conjunto autorizado."""
from datetime import date, datetime, time, timedelta, timezone
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import and_, func, or_, select, true
from sqlalchemy.orm import Session, aliased

from app.core.worker_response import worker_response
from app.core.database import get_session
from app.core.security import current_user
from app.models import AuditEvent, Category, Department, Incident, IncidentParticipant, Role, User
from app.services.incidents import create_case, role_name, visibility, visible_case
from app.services.lifecycle import manage_case

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


class ClassificationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category_id: int = Field(ge=1)
    priority: int = Field(ge=1, le=3)


class AssignmentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    assigned_to: UUID


class ContentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    titulo: str = Field(min_length=1, max_length=200)
    descripcion: str = Field(min_length=1, max_length=10000)

    @field_validator("titulo", "descripcion")
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError("El texto no puede estar vacío")
        return value.strip()


class TransitionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["EN_REVISION", "RESUELTA", "CERRADA"]
    assigned_to: UUID | None = None
    resolution_text: str | None = Field(None, min_length=1, max_length=10000)
    reason: str | None = Field(None, min_length=1, max_length=2000)

    @field_validator("resolution_text", "reason")
    @classmethod
    def not_blank(cls, value):
        if value is not None and not value.strip():
            raise ValueError("El texto no puede estar vacío")
        return value.strip() if value is not None else None


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
@worker_response(Receipt)
def register(body:IncidentInput,response:Response,user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    return create_case(db,user,body)


@router.get("",response_model=CasePage)
@worker_response(CasePage)
def list_cases(response:Response,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100),
               status:Literal["PENDIENTE","EN_REVISION","RESUELTA","CERRADA"]|None=None,
               priority:int|None=Query(None,ge=1,le=3),category_id:int|None=Query(None,ge=1),assigned_to:UUID|None=None,
               created_from:date|None=None,created_to:date|None=None,q:str|None=Query(None,max_length=200),unassigned:bool=False,
               user:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers["Cache-Control"]="no-store"
    if unassigned and assigned_to is not None:raise HTTPException(422,"Elige un responsable o casos sin responsable, no ambos")
    conditions=[visibility(db,user)]
    if unassigned:conditions.append(Incident.assigned_to.is_(None))
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
    # El agregado siempre produce una fila, aunque la página esté vacía.
    # Ambas ramas usan el mismo predicado y una sola instantánea SQL.
    totals = select(func.count().label("total")).select_from(Incident).where(*conditions).subquery()
    page_rows = (select(Incident).where(*conditions)
        .order_by(Incident.created_at.desc(), Incident.id.desc())
        .offset((page-1)*page_size).limit(page_size).subquery())
    page_case = aliased(Incident, page_rows)
    rows = db.execute(select(page_case, totals.c.total).select_from(totals)
        .outerjoin(page_rows, true())
        .order_by(page_rows.c.created_at.desc(), page_rows.c.id.desc())).all()
    items = [row[0] for row in rows if row[0] is not None]
    return {"items":items,"total":rows[0][1],"page":page,"page_size":page_size}


@router.get("/{case_id}",response_model=CaseDetail)
@worker_response(CaseDetail)
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


@router.put('/{case_id}/classification', response_model=CaseDetail)
def classify(case_id: UUID, body: ClassificationInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers['Cache-Control'] = 'no-store'
    return manage_case(db, user, case_id, 'classification', body, presenter=CaseDetail.model_validate)


@router.put('/{case_id}/assignment', response_model=CaseDetail)
def assign(case_id: UUID, body: AssignmentInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers['Cache-Control'] = 'no-store'
    return manage_case(db, user, case_id, 'assignment', body, presenter=CaseDetail.model_validate)


@router.put('/{case_id}/content', response_model=CaseDetail)
@worker_response(CaseDetail)
def edit_content(case_id: UUID, body: ContentInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers['Cache-Control'] = 'no-store'
    return manage_case(db, user, case_id, 'content', body, presenter=CaseDetail.model_validate)


@router.post('/{case_id}/transitions', response_model=CaseDetail)
def transition(case_id: UUID, body: TransitionInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers['Cache-Control'] = 'no-store'
    if body.status != 'EN_REVISION' and (body.assigned_to is not None or body.reason is not None):
        raise HTTPException(422, 'Responsable y motivo solo aplican a entrada en revisión')
    if body.status != 'RESUELTA' and body.resolution_text is not None:
        raise HTTPException(422, 'La resolución solo aplica al resolver')
    return manage_case(db, user, case_id, 'transition', body, presenter=CaseDetail.model_validate)


class ParticipantReviewInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    review_status: Literal['CONFIRMADO', 'DESCARTADO']
    reason: str = Field(min_length=1, max_length=2000)
    assigned_to: UUID | None = None

    @field_validator('reason')
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError('El motivo no puede estar vacío')
        return value.strip()


class ConfidentialityInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    is_confidential: bool
    reason: str = Field(min_length=1, max_length=2000)
    assigned_to: UUID | None = None

    @field_validator('reason')
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError('El motivo no puede estar vacío')
        return value.strip()


@router.post('/{case_id}/participants', status_code=201, response_model=Receipt)
def add_participant(case_id: UUID, body: ParticipantInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    from app.services.protection import protect_case
    response.headers['Cache-Control'] = 'no-store'
    return protect_case(db, user, case_id, 'participant_add', body)


@router.put('/{case_id}/participants/{participant_id}/review', response_model=Receipt)
def review_participant(case_id: UUID, participant_id: UUID, body: ParticipantReviewInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    from app.services.protection import protect_case
    response.headers['Cache-Control'] = 'no-store'
    return protect_case(db, user, case_id, 'participant_review', body, participant_id)


@router.put('/{case_id}/confidentiality', response_model=Receipt)
def change_confidentiality(case_id: UUID, body: ConfidentialityInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    from app.services.protection import protect_case
    response.headers['Cache-Control'] = 'no-store'
    return protect_case(db, user, case_id, 'confidentiality', body)
