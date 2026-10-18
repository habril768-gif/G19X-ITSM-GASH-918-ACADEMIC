from uuid import UUID
from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.ai.contracts import AIInput
from app.core.database import get_session
from app.core.security import current_user
from app.models import AIJob, User
from app.services.ai import _authorized_case, enabled, enqueue
from app.services.protection import manager_involved

router = APIRouter(prefix='/incidents', tags=['Asistencia IA'])


@router.post('/{case_id}/ai', status_code=202)
def request_ai(case_id: UUID, body: AIInput, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers['Cache-Control'] = 'no-store'
    return enqueue(db, user, case_id, body)


@router.get('/{case_id}/ai')
def status(case_id: UUID, response: Response, user: User = Depends(current_user), db: Session = Depends(get_session)):
    response.headers['Cache-Control'] = 'no-store'
    case = _authorized_case(db, user, case_id)
    job = db.scalar(select(AIJob).where(AIJob.case_id == case.id).order_by(AIJob.content_revision.desc(), AIJob.created_at.desc(), AIJob.id.desc()).limit(1))
    private = case.is_confidential or manager_involved(db, case)
    current = bool(job and job.content_revision == case.content_revision)
    return {'enabled': enabled(), 'ai_status': case.ai_status, 'reason': case.ai_skip_reason or case.ai_error,
            'eligible': not private and not case.classification_valid and case.status in {'PENDIENTE', 'EN_REVISION'},
            'suggestion': case.ai_suggestion if current and not private and job.status == 'COMPLETADA' else None,
            'reviewed_text': job.input_text if current and not private else None,
            'job': None if not job else {'id': job.id, 'status': job.status, 'attempts': job.attempts,
                'model': job.model, 'prompt_version': job.prompt_version, 'current': current,
                'dispatched_at': job.dispatched_at, 'error': job.error}}
