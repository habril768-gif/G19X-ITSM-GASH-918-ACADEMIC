"""Seguimiento acotado: solo RH con acceso vigente al expediente."""
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,Query,Response
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.core.security import current_user
from app.models import MailDelivery,User
from app.services.incidents import role_name,visible_case
router=APIRouter(prefix='/incidents',tags=['Correo'])

@router.get('/{case_id}/mail')
def status(case_id:UUID,response:Response,page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100),
           actor:User=Depends(current_user),db:Session=Depends(get_session)):
    response.headers['Cache-Control']='no-store'
    if role_name(db,actor)!='ADMIN_RH': raise HTTPException(403,'Solo Admin RH autorizado')
    visible_case(db,actor,case_id)
    where=MailDelivery.case_id==case_id
    total=db.scalar(select(func.count()).select_from(MailDelivery).where(where))
    rows=db.scalars(select(MailDelivery).where(where).order_by(MailDelivery.created_at.desc(),MailDelivery.id)
                    .offset((page-1)*page_size).limit(page_size)).all()
    return {'total':total,'page':page,'page_size':page_size,'items':[{
        'id':row.id,'kind':row.kind,'status':row.status,'attempts':row.attempts,
        'error':row.error,'created_at':row.created_at,'completed_at':row.completed_at} for row in rows]}
