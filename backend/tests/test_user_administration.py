from datetime import date
from types import SimpleNamespace
from uuid import uuid4
import pytest
from fastapi import HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.api.users import UserUpdate, options, users
from app.core.security import current_user, token_digest, utcnow, SESSION_LIFETIME
from app.models import (AuditEvent, AuthSession, Base, Category, Department, Incident,
                        IncidentParticipant, LocalCredential, Role, User)
from app.services.users import update_user


@pytest.fixture
def world():
    engine = create_engine("sqlite://")
    @event.listens_for(engine, "connect")
    def foreign_keys(c, _): c.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as db:
        db.add_all([Role(id=1,nombre="ADMIN_RH"),Role(id=2,nombre="SUPERVISOR"),Role(id=3,nombre="EMPLEADO")])
        one,two=Department(nombre="Uno",is_active=True),Department(nombre="Dos",is_active=True)
        db.add_all([one,two]);db.flush()
        actors={name:User(email=name+"@example.invalid",nombre_completo=name,departamento_id=one.id,rol_id=role,is_active=True)
                for name,role in [("admin",1),("admin2",1),("super",2),("employee",3),("peer",3)]}
        db.add_all(actors.values());db.add(Category(id=2,nombre="Conflicto",descripcion="Prueba"));db.flush()
        db.add(LocalCredential(user_id=actors['admin'].id,password_hash='fixture-no-login'))
        db.commit()
        yield db,actors,one,two
    engine.dispose()


def body(user, **extra):
    return UserUpdate(nombre_completo=user.nombre_completo,departamento_id=extra.get('departamento_id',user.departamento_id),
                      rol_id=extra.get('rol_id',user.rol_id),is_active=extra.get('is_active',user.is_active),
                      reason='Cambio administrativo simulado')


def case(db,a,one,**extra):
    row=Incident(titulo='Prueba',descripcion='Datos simulados',incident_date=date(2026,10,16),
                 created_by=a['employee'].id,affected_employee_id=a['employee'].id,scope='PERSONA',
                 department_id_at_creation=one.id,reported_department_id=one.id,
                 **extra)
    db.add(row);db.commit();return row


def revision(db,a,one,**extra):
    return case(db,a,one,status='EN_REVISION',assigned_to=a['super'].id,category_id=2,priority=2,
                classification_valid=True,validated_by=a['admin'].id,validated_at=utcnow(),cycle_start_at=utcnow(),**extra)


def session_for(db,user):
    raw='only-for-test-'+uuid4().hex
    row=AuthSession(token_hash=token_digest(raw),user_id=user.id,expires_at=utcnow()+SESSION_LIFETIME)
    db.add(row);db.commit();return row,raw


def test_deactivation_revokes_sessions_and_reassigns_review(world):
    db,a,one,two=world
    row=revision(db,a,one);session,raw=session_for(db,a['super'])
    result=update_user(db,a['admin'],a['super'].id,body(a['super'],is_active=False))
    assert result['sessions_revoked'] and result['cases_adjusted']==1
    assert row.assigned_to in {a['admin'].id,a['admin2'].id} and row.status=='EN_REVISION'
    persisted = db.scalar(select(AuthSession.revoked_at).where(AuthSession.token_hash==session.token_hash))
    assert persisted is not None
    db.refresh(session)
    assert session.revoked_at is not None
    with pytest.raises(HTTPException) as exc: current_user(HTTPAuthorizationCredentials(scheme='Bearer',credentials=raw),db)
    assert exc.value.status_code==401


def test_last_local_admin_cannot_be_removed(world):
    db,a,one,two=world
    for change in [{'is_active':False},{'rol_id':3}]:
        with pytest.raises(HTTPException) as exc: update_user(db,a['admin'],a['admin'].id,body(a['admin'],**change))
        assert exc.value.status_code==409
        assert a['admin'].is_active and a['admin'].rol_id==1
    # Otro Admin RH sin credencial local no basta para evitar el bloqueo.
    assert db.get(LocalCredential,a['admin2'].id) is None


def test_promotion_protects_cases_and_clears_pending_assignment(world):
    db,a,one,two=world
    pending=case(db,a,one,assigned_to=a['super'].id)
    active=revision(db,a,one)
    result=update_user(db,a['admin'],a['employee'].id,body(a['employee'],rol_id=2))
    assert result['cases_adjusted']==2
    assert pending.is_confidential and pending.assigned_to is None
    assert active.is_confidential and active.assigned_to in {a['admin'].id,a['admin2'].id}
    assert active.ai_status=='OMITIDA'


def test_department_change_reassigns_case_and_preserves_history(world):
    db,a,one,two=world
    row=revision(db,a,one)
    update_user(db,a['admin'],a['employee'].id,body(a['employee'],departamento_id=two.id))
    assert row.assigned_to in {a['admin'].id,a['admin2'].id}
    assert row.department_id_at_creation==one.id and row.reported_department_id==one.id
    assert a['employee'].departamento_id==two.id


def test_terminal_case_requires_reopening_and_rolls_back_sessions(world):
    db,a,one,two=world
    row=revision(db,a,one);row.status='RESUELTA';row.resolved_at=utcnow();row.resolution_text='Prueba';db.commit()
    session,_=session_for(db,a['super'])
    with pytest.raises(HTTPException) as exc: update_user(db,a['admin'],a['super'].id,body(a['super'],is_active=False))
    assert exc.value.status_code==409
    assert a['super'].is_active and session.revoked_at is None and row.status=='RESUELTA'


def test_no_case_exposure_when_admin_involved(world):
    db,a,one,two=world
    row=case(db,a,one,assigned_to=a['super'].id,is_confidential=True,ai_status='OMITIDA',ai_skip_reason='Prueba')
    db.add(IncidentParticipant(incidencia_id=row.id,user_id=a['admin'].id,declaration_reason='Prueba'));db.commit()
    with pytest.raises(HTTPException) as exc: update_user(db,a['admin'],a['super'].id,body(a['super'],is_active=False))
    assert exc.value.status_code==409
    assert a['super'].is_active and row.assigned_to==a['super'].id


def test_rollback_all_on_audit_failure(world):
    db,a,one,two=world
    row=revision(db,a,one);session,_=session_for(db,a['super'])
    def fail(session,context,instances):
        if any(isinstance(r,AuditEvent) for r in session.new):raise SQLAlchemyError('simulated failure')
    event.listen(db,'before_flush',fail)
    try:
        with pytest.raises(HTTPException) as exc:update_user(db,a['admin'],a['super'].id,body(a['super'],is_active=False))
        assert exc.value.status_code==503
    finally:event.remove(db,'before_flush',fail)
    assert a['super'].is_active and row.assigned_to==a['super'].id and session.revoked_at is None
    assert db.scalars(select(AuditEvent)).all()==[]


def test_admin_only_validation_and_read_contracts(world):
    db,a,one,two=world
    with pytest.raises(HTTPException) as exc:update_user(db,a['employee'],a['peer'].id,body(a['peer']))
    assert exc.value.status_code==403
    with pytest.raises(HTTPException) as exc:update_user(db,a['admin'],uuid4(),body(a['peer']))
    assert exc.value.status_code==404
    two.is_active=False;db.commit()
    with pytest.raises(HTTPException) as exc:update_user(db,a['admin'],a['peer'].id,body(a['peer'],departamento_id=two.id))
    assert exc.value.status_code==422
    response=Response();result=users(response,page=1,page_size=2,admin=a['admin'],db=db)
    assert len(result['items'])==2 and result['total']==5 and response.headers['cache-control']=='no-store'
    assert len(options(Response(),a['admin'],db)['departments'])==1


def test_name_only_edit_does_not_revoke_and_audit_has_no_secret(world):
    db,a,one,two=world
    session,_=session_for(db,a['peer'])
    model=body(a['peer']);model.nombre_completo='Nombre corregido'
    result=update_user(db,a['admin'],a['peer'].id,model)
    assert not result['sessions_revoked'] and session.revoked_at is None
    entry=db.scalar(select(AuditEvent))
    assert entry.detalle['before']['nombre_completo']=='peer'
    assert entry.detalle['after']['nombre_completo']=='Nombre corregido'
    assert not any(word in str(entry.detalle) for word in ['password','token','hash'])


def test_existing_case_services_still_work_with_administration_gate(world):
    from uuid import UUID
    from app.api.incidents import IncidentInput, ClassificationInput, TransitionInput, ConfidentialityInput
    from app.services.incidents import create_case
    from app.services.lifecycle import manage_case
    from app.services.protection import protect_case
    db,a,one,two=world
    receipt=create_case(db,a['employee'],IncidentInput(titulo='Prueba gate',descripcion='Simulación',incident_date=date(2026,10,16)))
    identifier=receipt['id']
    manage_case(db,a['admin'],identifier,'classification',ClassificationInput(category_id=2,priority=2))
    manage_case(db,a['admin'],identifier,'transition',TransitionInput(status='EN_REVISION',assigned_to=a['super'].id))
    receipt=protect_case(db,a['admin'],identifier,'confidentiality',ConfidentialityInput(is_confidential=True,reason='Prueba'))
    assert receipt['can_view'] is True
    row=db.get(Incident,identifier)
    assert row.status=='EN_REVISION' and row.is_confidential and row.assigned_to in {a['admin'].id,a['admin2'].id}


def test_gate_refreshes_actor_before_using_old_privileges(world):
    from sqlalchemy import update
    from app.api.incidents import ClassificationInput
    from app.services.lifecycle import manage_case
    db,a,one,two=world
    row=case(db,a,one)
    db.execute(update(User).where(User.id==a['admin2'].id).values(rol_id=3).execution_options(synchronize_session=False))
    db.commit()
    assert a['admin2'].rol_id==1  # Caché anterior, antes de entrar al gate.
    with pytest.raises(HTTPException) as exc:
        manage_case(db,a['admin2'],row.id,'classification',ClassificationInput(category_id=2,priority=2))
    assert exc.value.status_code==403
    assert not row.classification_valid
