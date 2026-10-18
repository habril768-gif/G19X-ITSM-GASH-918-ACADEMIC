"""Contratos HTTP y rollback con SQLite; no certifica concurrencia PostgreSQL."""
from datetime import date
from uuid import UUID, uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.core.database import get_session
from app.core.security import current_user
from app.core.security import utcnow
from app.main import create_app
from app.models import Base, Category, Department, DepartmentAudit, Incident, Role, User


@pytest.fixture
def world():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    @event.listens_for(engine, 'connect')
    def fk(c, _): c.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as db:
        db.add_all([Role(id=1, nombre='ADMIN_RH'), Role(id=2, nombre='SUPERVISOR'), Role(id=3, nombre='EMPLEADO')])
        home = Department(nombre='Casa', is_active=True); empty = Department(nombre='Vacío', is_active=True)
        db.add_all([home, empty]); db.flush()
        actors = {name: User(email=name+'@example.invalid', nombre_completo=name, departamento_id=home.id, rol_id=role, is_active=True)
                  for name, role in [('rh', 1), ('super', 2), ('employee', 3)]}
        db.add_all(actors.values()); db.add(Category(id=4, nombre='Riesgos', descripcion='QA')); db.commit()
        selected = {'user': actors['rh']}; app = create_app()
        def session(): yield db
        app.dependency_overrides[get_session] = session
        app.dependency_overrides[current_user] = lambda: selected['user']
        with TestClient(app) as client:
            yield client, db, actors, selected, home, empty, app
    engine.dispose()


def payload(**extra): return {'nombre': 'Nuevo', 'reason': 'Prueba académica', **extra}


def test_create_update_deactivate_reactivate_audit(world):
    c, db, a, s, home, empty, _ = world
    r = c.post('/departments', json=payload(nombre='  QA temporal  '))
    assert r.status_code == 201 and r.json()['nombre'] == 'QA temporal'
    ident = r.json()['id']
    for name, active in [('QA renombrado', True), ('QA renombrado', False), ('QA renombrado', True)]:
        r = c.put('/departments/'+ident, json=payload(nombre=name, is_active=active))
        assert r.status_code == 200 and r.json()['is_active'] is active
    r = c.get('/departments/'+ident+'/history?page=1&page_size=2')
    assert r.headers['cache-control'] == 'no-store'
    assert r.json()['total'] == 4 and len(r.json()['items']) == 2
    events = db.scalars(select(DepartmentAudit).where(DepartmentAudit.department_id == UUID(ident))).all()
    assert all(e.actor_id == a['rh'].id and e.detalle['reason'] == 'Prueba académica' for e in events)
    assert any(e.detalle['before'] is None for e in events)
    assert db.get(Department, UUID(ident)) is not None


@pytest.mark.parametrize('actor', ['super', 'employee'])
def test_non_admin_cannot_list_write_or_read_history(world, actor):
    c, db, a, s, home, empty, _ = world; s['user'] = a[actor]
    assert c.get('/departments').status_code == 403
    assert c.get(f'/departments/{empty.id}/history').status_code == 403
    assert c.post('/departments', json=payload()).status_code == 403
    assert c.put(f'/departments/{empty.id}', json=payload(is_active=False)).status_code == 403
    assert db.scalar(select(func.count()).select_from(DepartmentAudit)) == 0


def test_anonymous_is_rejected(world):
    c, db, a, s, home, empty, app = world
    del app.dependency_overrides[current_user]
    assert c.get('/departments').status_code == 401


def test_validation_duplicates_and_pagination(world):
    c, db, a, s, home, empty, _ = world
    assert c.post('/departments', json=payload(nombre=' casa ')).status_code == 409
    for body in [payload(nombre=' '), payload(reason=' '), payload(nombre='x'*121), payload(is_active=False)]:
        assert c.post('/departments', json=body).status_code == 422
    assert c.get('/departments?page=0').status_code == 422
    r = c.get('/departments?page=2&page_size=1')
    assert r.json()['total'] == 2 and len(r.json()['items']) == 1
    assert set(r.json()['items'][0]) == {'id', 'nombre', 'is_active'}
    assert c.put(f'/departments/{empty.id}', json=payload(nombre='CASA', is_active=True)).status_code == 409


def test_deactivation_with_active_users_rejected_without_partial_change(world):
    c, db, a, s, home, empty, _ = world
    r = c.put(f'/departments/{home.id}', json=payload(nombre='No guardar', is_active=False))
    assert r.status_code == 409
    db.refresh(home); assert home.is_active and home.nombre == 'Casa'
    assert db.scalar(select(func.count()).select_from(DepartmentAudit)) == 0


@pytest.mark.parametrize('scope', ['PERSONA', 'ENTORNO'])
def test_open_cases_block_deactivation_even_with_inactive_affected_user(world, scope):
    c, db, a, s, home, empty, _ = world
    employee = a['employee']; employee.departamento_id = empty.id; employee.is_active = False
    case = Incident(titulo='Simulado', descripcion='QA', incident_date=date(2026,10,17), created_by=a['rh'].id,
                    scope=scope, affected_employee_id=employee.id if scope == 'PERSONA' else None,
                    reported_department_id=empty.id, department_id_at_creation=empty.id)
    db.add(case); db.commit()
    assert c.put(f'/departments/{empty.id}', json=payload(is_active=False)).status_code == 409
    db.refresh(empty); assert empty.is_active


def test_audit_failure_rolls_back_mutation(world):
    c, db, a, s, home, empty, _ = world
    def fail(session, *_):
        if any(isinstance(row, DepartmentAudit) for row in session.new): raise SQLAlchemyError('QA controlado')
    event.listen(db, 'before_flush', fail)
    try:
        assert c.put(f'/departments/{empty.id}', json=payload(is_active=False)).status_code == 503
        assert c.post('/departments', json=payload()).status_code == 503
    finally: event.remove(db, 'before_flush', fail)
    db.refresh(empty); assert empty.is_active and empty.nombre == 'Vacío'
    assert db.scalar(select(func.count()).select_from(Department)) == 2
    assert db.scalar(select(func.count()).select_from(DepartmentAudit)) == 0


def test_missing_and_soft_delete_only(world):
    c, db, a, s, home, empty, _ = world; ident = uuid4()
    assert c.put(f'/departments/{ident}', json=payload(is_active=True)).status_code == 404
    assert c.get(f'/departments/{ident}/history').status_code == 404
    assert c.delete(f'/departments/{empty.id}').status_code == 405


def test_inactive_departments_excluded_from_user_options(world):
    c, db, a, s, home, empty, _ = world
    assert c.put(f'/departments/{empty.id}', json=payload(is_active=False)).status_code == 200
    assert str(empty.id) not in {d['id'] for d in c.get('/users/options').json()['departments']}
    assert any(d['id'] == str(empty.id) and not d['is_active'] for d in c.get('/departments').json()['items'])


def test_finalized_cases_and_historical_department_are_preserved(world):
    c, db, a, s, home, empty, _ = world
    employee = a['employee']; employee.departamento_id = empty.id; employee.is_active = False
    case = Incident(titulo='Finalizado', descripcion='QA', incident_date=date(2026,10,17), created_by=a['rh'].id,
                    scope='PERSONA', affected_employee_id=employee.id, reported_department_id=empty.id,
                    department_id_at_creation=empty.id, status='RESUELTA', assigned_to=a['rh'].id,
                    category_id=4, priority=2, classification_valid=True, validated_by=a['rh'].id,
                    validated_at=utcnow(), cycle_start_at=utcnow(), resolved_at=utcnow(), resolution_text='Prueba resuelta')
    db.add(case); db.commit()
    assert c.put(f'/departments/{empty.id}', json=payload(nombre='Archivo QA', is_active=False)).status_code == 200
    db.refresh(case)
    assert case.status == 'RESUELTA' and case.resolution_text == 'Prueba resuelta'
    assert case.department_id_at_creation == empty.id and case.reported_department_id == empty.id
    assert db.get(User, employee.id).departamento_id == empty.id


def test_service_rechecks_actor_after_administrative_lock(world):
    from fastapi import HTTPException
    from app.api.departments import DepartmentCreate
    from app.services.departments import save_department
    c, db, a, s, home, empty, _ = world
    actor = a['rh']
    db.execute(update(User).where(User.id == actor.id).values(rol_id=3).execution_options(synchronize_session=False)); db.commit()
    with pytest.raises(HTTPException) as exc:
        save_department(db, actor, DepartmentCreate(**payload()))
    assert exc.value.status_code == 403
    assert db.scalar(select(func.count()).select_from(DepartmentAudit)) == 0
