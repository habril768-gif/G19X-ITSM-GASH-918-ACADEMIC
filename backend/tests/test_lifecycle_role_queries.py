"""Lecturas de rol acotadas a cada operación; sin caché entre peticiones."""
from contextlib import contextmanager
from uuid import UUID
import pytest
from sqlalchemy import event, update
from app.models import Incident, Role, User
from app.services.lifecycle import eligible_manager
from test_incidents import create, world


@contextmanager
def role_reads(db):
    calls=[]
    def observe(conn,cursor,statement,parameters,context,executemany):
        compiled=getattr(context,'compiled',None)
        expression=getattr(compiled,'statement',None)
        if expression is not None and getattr(expression,'is_select',False):
            # Contar la lectura del rol en el SELECT conjunto o individual;
            # los subqueries del predicado de visibilidad no son otra relectura.
            entities = [item.get('entity') for item in getattr(expression, 'column_descriptions', [])]
            if Role in entities:
                calls.append(statement)
    event.listen(db.bind,'before_cursor_execute',observe)
    try:
        yield calls
    finally:
        event.remove(db.bind,'before_cursor_execute',observe)


@pytest.mark.parametrize('actor,expected_status',[('admin',200),('super',200),('employee',403)])
def test_content_operation_reads_actor_role_once(world,actor,expected_status):
    client,db,actors,selected,*_=world
    cid=create(client)
    selected['user']=actors[actor]
    with role_reads(db) as reads:
        response=client.put(f'/incidents/{cid}/content',json={'titulo':'Cambio QA','descripcion':'Cambio ficticio'})
    assert response.status_code==expected_status,response.text
    assert len(reads)==1
    assert 'JOIN roles' in reads[0]
    if expected_status==200:
        assert response.json()['titulo']=='Cambio QA'
    else:
        assert db.get(Incident,UUID(cid)).titulo=='Caso de prueba'


@pytest.mark.parametrize('target',['admin2','super'])
def test_eligible_manager_reads_target_role_once(world,target):
    client,db,actors,selected,*_=world
    cid=UUID(create(client))
    case=db.get(Incident,cid)
    with role_reads(db) as reads:
        result=eligible_manager(db,case,actors[target].id)
    assert result.id==actors[target].id
    assert len(reads)==1


def test_role_downgrade_between_requests_is_revalidated(world):
    client,db,actors,selected,*_=world
    cid=UUID(create(client))
    selected['user']=actors['admin']
    first=client.put(f'/incidents/{cid}/content',json={'titulo':'Primer cambio','descripcion':'QA uno'})
    assert first.status_code==200,first.text
    # Mantener objeto actor obsoleto en el identity map: el lock debe refrescarlo.
    uid=actors['admin'].id
    db.execute(update(User).where(User.id==uid).values(rol_id=3),execution_options={'synchronize_session':False})
    db.commit()
    assert actors['admin'].rol_id==1
    response=client.put(f'/incidents/{cid}/content',json={'titulo':'Cambio no autorizado','descripcion':'QA dos'})
    assert response.status_code==403,response.text
    assert actors['admin'].rol_id==3
    assert db.get(Incident,cid).titulo=='Primer cambio'
