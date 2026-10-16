from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import get_session
from app.core.security import current_user
from app.main import create_app
from app.models import AuditEvent, Base, Category, Department, Incident, IncidentParticipant, Role, User

@pytest.fixture
def world():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    @event.listens_for(engine,"connect")
    def fk(connection,_):connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    with Session(engine,expire_on_commit=False) as db:
        db.add_all([Role(id=1,nombre="ADMIN_RH"),Role(id=2,nombre="SUPERVISOR"),Role(id=3,nombre="EMPLEADO")])
        one=Department(nombre="Uno",is_active=True);two=Department(nombre="Dos",is_active=True)
        db.add_all([one,two]);db.flush()
        actors={}
        for name,role,dep in [("admin",1,one),("admin2",1,two),("super",2,one),("super2",2,two),("employee",3,one),("peer",3,one),("outsider",3,two)]:
            actors[name]=User(email=name+"@example.invalid",nombre_completo=name,rol_id=role,departamento_id=dep.id,is_active=True)
        db.add_all(list(actors.values()));db.add_all([Category(id=4,nombre="Riesgos",descripcion="QA"),Category(id=2,nombre="Conflictos",descripcion="QA")]);db.commit()
        selected={"user":actors["employee"]}
        app=create_app()
        def session():yield db
        app.dependency_overrides[get_session]=session
        app.dependency_overrides[current_user]=lambda:selected["user"]
        with TestClient(app) as client:
            yield client,db,actors,selected,one,two
    engine.dispose()

def payload(**extra):
    return {"titulo":"Caso de prueba","descripcion":"Solo datos simulados","incident_date":"2026-10-16",**extra}

def create(client,**extra):
    result=client.post("/incidents",json=payload(**extra))
    assert result.status_code==201,result.text
    return result.json()["id"]

def test_personal_registration_and_redacted_employee_history(world):
    c,db,a,selected,one,two=world
    case_id=create(c)
    response=c.get("/incidents/"+case_id)
    assert response.status_code==200
    assert response.json()["affected_employee_id"]==str(a["employee"].id)
    assert response.json()["classification_valid"] is False
    assert response.headers["cache-control"]=="no-store"
    events=c.get(f"/incidents/{case_id}/history").json()
    assert events["total"]==1
    assert "detalle" not in events["items"][0]
    assert db.scalar(select(func.count()).select_from(AuditEvent))==1
    assert c.get(f"/incidents/{case_id}/participants").json()=={"items":[]}

def test_employee_cannot_report_for_peer_or_spoof_author(world):
    c,db,a,s,one,two=world
    assert c.post("/incidents",json=payload(affected_employee_id=str(a["peer"].id))).status_code==403
    assert c.post("/incidents",json=payload(created_by=str(a["admin"].id))).status_code==422
    assert db.scalar(select(func.count()).select_from(Incident))==0

def test_environment_without_victim_and_scope_limits(world):
    c,db,a,s,one,two=world
    case=create(c,scope="ENTORNO",reported_department_id=str(one.id))
    detail=c.get("/incidents/"+case).json()
    assert detail["affected_employee_id"] is None and detail["category_id"]==4
    assert c.post("/incidents",json=payload(scope="ENTORNO",reported_department_id=str(two.id))).status_code==403
    assert c.post("/incidents",json=payload(scope="ENTORNO",reported_department_id=str(one.id),affected_employee_id=str(a["employee"].id))).status_code==422

def test_visibility_idor_and_counts(world):
    c,db,a,s,one,two=world
    own=create(c,titulo="Visible")
    s["user"]=a["peer"];hidden=create(c,titulo="Hidden search needle")
    s["user"]=a["employee"]
    assert c.get("/incidents").json()["total"]==1
    assert c.get("/incidents",params={"q":"Hidden search needle"}).json()["total"]==0
    assert c.get("/incidents/"+hidden).status_code==404
    assert c.get(f"/incidents/{hidden}/history").status_code==404
    assert c.get(f"/incidents/{hidden}/participants").status_code==404
    assert c.get("/incidents/"+str(uuid4())).status_code==404
    s["user"]=a["super"];assert c.get("/incidents").json()["total"]==2
    s["user"]=a["super2"];assert c.get("/incidents").json()["total"]==0
    assert c.get("/incidents/"+own).status_code==404

def test_confidential_receipt_hides_case_from_creator(world):
    c,db,a,s,one,two=world
    response=c.post("/incidents",json=payload(is_confidential=True))
    assert response.status_code==201
    assert set(response.json())=={"id","received","can_view"}
    assert response.json()["can_view"] is False
    case=response.json()["id"]
    assert c.get("/incidents/"+case).status_code==404
    assert c.get("/incidents").json()["total"]==0
    s["user"]=a["super"];assert c.get("/incidents/"+case).status_code==404
    s["user"]=a["admin"];assert c.get("/incidents/"+case).json()["ai_status"]=="OMITIDA"

def test_declared_admin_cannot_access_even_with_global_role(world):
    c,db,a,s,one,two=world
    case=create(c,participants=[{"user_id":str(a["admin"].id),"declaration_reason":"Relación simulada"}])
    s["user"]=a["admin"]
    assert c.get("/incidents/"+case).status_code==404
    assert c.get("/incidents").json()["total"]==0
    s["user"]=a["admin2"]
    assert c.get("/incidents/"+case).status_code==200
    assert c.get(f"/incidents/{case}/participants").json()["items"][0]["review_status"]=="DECLARADO"
    assert c.get(f"/incidents/{case}/history").json()["items"][0]["detalle"]["participants"]

def test_supervisor_subject_and_changed_roles_are_protected(world):
    c,db,a,s,one,two=world
    s["user"]=a["admin"]
    case=create(c,affected_employee_id=str(a["super"].id))
    s["user"]=a["super"];assert c.get("/incidents/"+case).status_code==404
    s["user"]=a["employee"]
    ordinary=create(c)
    a["employee"].rol_id=2;db.commit()
    # Aunque la marca almacenada aún sea false, no expone el caso de un gestor.
    s["user"]=a["super"];assert c.get("/incidents/"+ordinary).status_code==404
    s["user"]=a["admin"];assert c.get("/incidents/"+ordinary).status_code==200

def test_participants_are_bounded_and_authorized(world):
    c,db,a,s,one,two=world
    participant={"user_id":str(a["peer"].id),"declaration_reason":"Prueba"}
    assert c.post("/incidents",json=payload(participants=[participant,participant])).status_code==422
    assert c.post("/incidents",json=payload(participants=[{"user_id":str(a["outsider"].id),"declaration_reason":"Prueba"}])).status_code==403
    assert c.post("/incidents",json=payload(participants=[{"user_id":str(a["peer"].id),"declaration_reason":" "}])).status_code==422

def test_supervisor_registration_and_admin_scope(world):
    c,db,a,s,one,two=world
    s["user"]=a["super"]
    assert c.post("/incidents",json=payload(affected_employee_id=str(a["outsider"].id))).status_code==403
    own=create(c,affected_employee_id=str(a["employee"].id))
    assert c.get("/incidents/"+own).status_code==200
    s["user"]=a["admin"]
    other=create(c,affected_employee_id=str(a["outsider"].id))
    assert c.get("/incidents/"+other).status_code==200
    assert c.post("/incidents",json=payload(affected_employee_id=str(a["outsider"].id),reported_department_id=str(one.id))).status_code==422

def test_creation_is_atomic_if_audit_fails(world,monkeypatch):
    c,db,a,s,one,two=world
    original=db.add
    def reject_audit(record,*args,**kwargs):
        if isinstance(record,AuditEvent):raise SQLAlchemyError("Falla simulada")
        return original(record,*args,**kwargs)
    monkeypatch.setattr(db,"add",reject_audit)
    response=c.post("/incidents",json=payload(participants=[{"user_id":str(a["peer"].id),"declaration_reason":"Prueba"}]))
    assert response.status_code==503
    assert db.scalar(select(func.count()).select_from(Incident))==0
    assert db.scalar(select(func.count()).select_from(IncidentParticipant))==0

def test_filters_options_and_input_limits(world):
    c,db,a,s,one,two=world
    create(c,titulo="literal %")
    create(c,titulo="otro")
    assert c.get("/incidents",params={"q":"%"}).json()["total"]==1
    result=c.get("/incidents",params={"page_size":1}).json()
    assert len(result["items"])==1 and result["total"]==2
    assert c.get("/incidents",params={"page_size":101}).status_code==422
    assert c.get("/incidents",params={"created_from":"2026-10-16","created_to":"2026-10-15"}).status_code==422
    assert c.get("/incidents",params={"created_to":"9999-12-31"}).status_code==200
    options=c.get("/incidents/options").json()
    assert [x["id"] for x in options["affected_employees"]]==[str(a["employee"].id)]
    assert str(a["outsider"].id) not in [x["id"] for x in options["participants"]]
    assert "email" not in str(options)
    assert c.post("/incidents",json=payload(titulo=" ")).status_code==422


def validate(c, case, **fields):
    return c.put(f'/incidents/{case}/classification', json={'category_id':2,'priority':1,**fields})


def move(c, case, status, **fields):
    return c.post(f'/incidents/{case}/transitions', json={'status':status,**fields})


def test_lifecycle_archives_cycles_and_closes(world):
    c,db,a,s,one,two=world
    case=create(c);s['user']=a['admin']
    assert validate(c,case).status_code==200
    assigned=c.put(f'/incidents/{case}/assignment',json={'assigned_to':str(a['super'].id)})
    assert assigned.status_code==200
    assert move(c,case,'EN_REVISION').status_code==200
    assert move(c,case,'RESUELTA',resolution_text='Acción simulada').status_code==200
    assert move(c,case,'CERRADA').status_code==200
    assert validate(c,case).status_code==409
    assert c.put(f'/incidents/{case}/assignment',json={'assigned_to':str(a['admin'].id)}).status_code==409
    assert move(c,case,'EN_REVISION').status_code==422
    result=move(c,case,'EN_REVISION',reason='Nueva información simulada',assigned_to=str(a['admin'].id))
    assert result.status_code==200,result.text
    assert result.json()['resolved_at'] is None and result.json()['closed_at'] is None
    assert result.json()['resolution_text'] is None
    history=c.get(f'/incidents/{case}/history').json()['items']
    reopened=next(r for r in history if r['accion']=='REAPERTURA')
    assert reopened['detalle']['before']['resolution_text']=='Acción simulada'
    assert reopened['detalle']['before']['closed_at'] is not None
    assert reopened['detalle']['reason']=='Nueva información simulada'


def test_edit_requires_revalidation_without_erasing_validator(world):
    c,db,a,s,one,two=world
    case=create(c);s['user']=a['super']
    assert move(c,case,'EN_REVISION',assigned_to=str(a['super'].id)).status_code==409
    assert validate(c,case).status_code==200
    assert move(c,case,'EN_REVISION',assigned_to=str(a['super'].id)).status_code==200
    edited=c.put(f'/incidents/{case}/content',json={'titulo':'Editado','descripcion':'Nueva descripción simulada'})
    assert edited.status_code==200,edited.text
    assert edited.json()['classification_valid'] is False
    assert edited.json()['validated_by']==str(a['super'].id)
    assert edited.json()['status']=='EN_REVISION'
    assert move(c,case,'RESUELTA',resolution_text='Prueba').status_code==409
    assert validate(c,case,priority=3).status_code==200
    assert move(c,case,'RESUELTA',resolution_text='Prueba').status_code==200
    assert move(c,case,'CERRADA').status_code==403
    assert move(c,case,'EN_REVISION',reason='Prueba').status_code==403


def test_management_access_and_assignment_eligibility(world):
    c,db,a,s,one,two=world
    case=create(c)
    assert validate(c,case).status_code==403
    s['user']=a['super2'];assert validate(c,case).status_code==404
    s['user']=a['admin']
    for name in ['employee','super2']:
        assert c.put(f'/incidents/{case}/assignment',json={'assigned_to':str(a[name].id)}).status_code==422
    a['super'].is_active=False;db.commit()
    assert c.put(f'/incidents/{case}/assignment',json={'assigned_to':str(a['super'].id)}).status_code==422
    confidential=create(c,affected_employee_id=str(a['employee'].id),is_confidential=True)
    assert c.put(f'/incidents/{confidential}/assignment',json={'assigned_to':str(a['super2'].id)}).status_code==422
    assert c.put(f'/incidents/{confidential}/assignment',json={'assigned_to':str(a['admin2'].id)}).status_code==200
    s['user']=a['employee'];involved=create(c,participants=[{'user_id':str(a['admin'].id),'declaration_reason':'Prueba'}])
    s['user']=a['admin'];assert validate(c,involved).status_code==404


def test_transition_validation_and_environment_category(world):
    c,db,a,s,one,two=world
    case=create(c,scope='ENTORNO',reported_department_id=str(one.id));s['user']=a['admin']
    assert validate(c,case).status_code==422
    assert validate(c,case,category_id=999).status_code==422
    assert validate(c,case,category_id=4,priority=4).status_code==422
    assert move(c,case,'RESUELTA',resolution_text='Prueba').status_code==409
    assert validate(c,case,category_id=4).status_code==200
    assert move(c,case,'EN_REVISION').status_code==422
    assert move(c,case,'EN_REVISION',assigned_to=str(a['admin'].id)).status_code==200
    assert move(c,case,'EN_REVISION',assigned_to=str(a['admin'].id)).status_code==409
    assert move(c,case,'RESUELTA').status_code==422
    assert move(c,case,'RESUELTA',resolution_text='   ').status_code==422
    assert move(c,case,'RESUELTA',resolution_text='Prueba',assigned_to=str(a['admin'].id)).status_code==422
    assert move(c,case,'RESUELTA',resolution_text='Prueba').status_code==200
    assert c.put(f'/incidents/{case}/content',json={'titulo':'Prueba','descripcion':'Cambio'}).status_code==409


def test_lifecycle_rolls_back_on_failed_audit(world):
    c,db,a,s,one,two=world
    case=create(c);s['user']=a['admin']
    def fail_audit(session,flush_context,instances):
        if any(isinstance(row,AuditEvent) and row.accion=='VALIDACION_IA' for row in session.new):
            raise SQLAlchemyError('simulated failure')
    event.listen(db,'before_flush',fail_audit)
    try:
        assert validate(c,case).status_code==503
    finally:
        event.remove(db,'before_flush',fail_audit)
    detail=c.get('/incidents/'+case).json()
    assert detail['classification_valid'] is False and detail['category_id'] is None
    assert c.get(f'/incidents/{case}/history').json()['total']==1


def test_resolve_rechecks_assignee_and_transition_rollback(world):
    c,db,a,s,one,two=world
    case=create(c);s['user']=a['admin']
    assert validate(c,case).status_code==200
    assert move(c,case,'EN_REVISION',assigned_to=str(a['super'].id)).status_code==200
    a['super'].departamento_id=two.id;db.commit()
    assert move(c,case,'RESUELTA',resolution_text='Prueba').status_code==422
    assert c.put(f'/incidents/{case}/assignment',json={'assigned_to':str(a['admin'].id)}).status_code==200
    def fail_event(session,flush_context,instances):
        if any(isinstance(row,AuditEvent) and row.accion=='ESTADO_CAMBIADO' for row in session.new):
            raise SQLAlchemyError('simulated transition failure')
    event.listen(db,'before_flush',fail_event)
    try:
        assert move(c,case,'RESUELTA',resolution_text='No debe persistir').status_code==503
    finally:
        event.remove(db,'before_flush',fail_event)
    detail=c.get('/incidents/'+case).json()
    assert detail['status']=='EN_REVISION' and detail['resolution_text'] is None
    for reason in ['Primer ciclo','Segundo ciclo']:
        assert move(c,case,'RESUELTA',resolution_text=reason).status_code==200
        assert move(c,case,'EN_REVISION',reason=reason).status_code==200
    events=c.get(f'/incidents/{case}/history').json()['items']
    assert sum(row['accion']=='REAPERTURA' for row in events)==2
