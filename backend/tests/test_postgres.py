"""Integración optativa: usar solo una base de pruebas previamente migrada."""
import os
import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from test_support import validate_test_database
from app.core.database import get_engine

pytestmark = pytest.mark.skipif(os.environ.get("RUN_DB_TESTS") != "1", reason="Requiere PostgreSQL de pruebas migrado")


@pytest.fixture(autouse=True)
def dedicated_database():
    validate_test_database(os.environ)
    with get_engine().connect() as connection:
        assert connection.scalar(text('SELECT current_database()')) == os.environ['POSTGRES_DB']


def test_migrated_database_and_catalogs():
    engine = get_engine()
    assert {"users", "incidencias", "historial_incidencias", "departamentos", "department_audit_events", "ai_jobs", "mail_deliveries"} <= set(inspect(engine).get_table_names())
    with engine.connect() as c:
        assert c.execute(text("SELECT version_num FROM alembic_version")).scalar_one() == "0008"
        assert c.execute(text("SELECT count(*) FROM roles")).scalar_one() == 3
        assert c.execute(text("SELECT count(*) FROM categorias_incidencia")).scalar_one() == 5


def test_entra_identity_is_unique():
    # Transacción revertida siempre; identificadores ficticios, sin datos personales.
    engine = get_engine()
    with engine.connect() as c:
        tx = c.begin()
        try:
            c.execute(text("INSERT INTO departamentos (id,nombre) VALUES ('11111111-1111-1111-1111-111111111111','QA temporal')"))
            sql = text("INSERT INTO users (id,email,external_id,tenant_id,nombre_completo,departamento_id,rol_id) VALUES (:id,:email,'22222222-2222-2222-2222-222222222222','33333333-3333-3333-3333-333333333333','QA','11111111-1111-1111-1111-111111111111',3)")
            c.execute(sql, {"id": "44444444-4444-4444-4444-444444444444", "email": "qa-a@example.invalid"})
            with pytest.raises(IntegrityError) as exc:
                c.execute(sql, {"id": "55555555-5555-5555-5555-555555555555", "email": "qa-b@example.invalid"})
            assert exc.value.orig.diag.constraint_name == 'uq_users_entra'
        finally:
            tx.rollback()


def test_ai_durable_job_and_late_privacy_response_on_postgres(monkeypatch):
    from datetime import date
    from types import SimpleNamespace
    from uuid import UUID, uuid4
    from sqlalchemy import select
    from sqlalchemy.orm import Session
    from app.ai.contracts import AIInput
    from app.models import AIJob, Department, Incident, User
    from app.services.ai import enqueue, process_one
    monkeypatch.setenv('AI_ENABLED', 'true'); monkeypatch.setenv('OPENAI_MODEL', 'fixture-model')
    monkeypatch.setattr('app.services.ai.notify', lambda *_: False)
    with get_engine().connect() as connection:
        outer = connection.begin()
        def factory(): return Session(bind=connection, join_transaction_mode='create_savepoint', expire_on_commit=False)
        try:
            with factory() as db:
                home = Department(nombre='IA-QA-'+uuid4().hex, is_active=True); db.add(home); db.flush()
                admin = User(email=uuid4().hex+'@example.invalid', nombre_completo='RH QA', departamento_id=home.id, rol_id=1, is_active=True)
                employee = User(email=uuid4().hex+'@example.invalid', nombre_completo='Empleado QA', departamento_id=home.id, rol_id=3, is_active=True)
                db.add_all([admin, employee]); db.flush()
                case = Incident(titulo='QA IA', descripcion='Descripción original no enviada', incident_date=date(2026,10,17),
                                created_by=employee.id, affected_employee_id=employee.id, scope='PERSONA',
                                reported_department_id=home.id, department_id_at_creation=home.id)
                db.add(case); db.commit(); ident = case.id
                body = AIInput(ai_input_text='Dos colaboradores ficticios discrepan sobre una tarea.', confirmed_simulated=True, confirmed_no_identifiers=True)
                enqueue(db, admin, ident, body)
                def classify(*_):
                    with factory() as other:
                        row = other.get(Incident, ident); row.is_confidential = True
                        row.ai_status, row.ai_skip_reason = 'OMITIDA', 'Protección QA'; other.commit()
                    return {'result': 'CLASIFICADA', 'category_id': 2, 'priority': 2, 'suggestion': 'Revisión humana.', 'reason': 'Simulado.'}
                assert process_one(factory, SimpleNamespace(classify=classify))
                db.expire_all()
                result = db.scalar(select(AIJob).where(AIJob.case_id == ident))
                assert result.status == 'OMITIDA' and result.dispatched_at is not None and result.result is None
                assert db.get(Incident, ident).ai_suggestion is None and not db.get(Incident, ident).classification_valid
        finally:
            outer.rollback()


def test_administrative_lock_serializes_exclusive_and_shared_transactions():
    from sqlalchemy.exc import DBAPIError
    from sqlalchemy.orm import Session
    from app.services.administration_lock import administration_lock
    with Session(get_engine()) as first, Session(get_engine()) as second:
        administration_lock(first, exclusive=True)
        second.execute(text("SET LOCAL lock_timeout = '300ms'"))
        with pytest.raises(DBAPIError) as exc:
            administration_lock(second)
        assert exc.value.orig.sqlstate == '55P03'
        second.rollback(); first.rollback()
        # Dos lecturas pueden coexistir, pero una escritura espera a que terminen.
        administration_lock(first); administration_lock(second)
        second.rollback()
        second.execute(text("SET LOCAL lock_timeout = '300ms'"))
        with pytest.raises(DBAPIError) as exc:
            administration_lock(second, exclusive=True)
        assert exc.value.orig.sqlstate == '55P03'
        second.rollback(); first.rollback()
        administration_lock(second, exclusive=True)


def test_department_mutation_and_audit_rollback_on_postgres():
    from sqlalchemy import event, select
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import Session
    from uuid import uuid4
    from app.api.departments import DepartmentCreate, DepartmentUpdate
    from app.models import Department, DepartmentAudit, User
    from app.services.departments import save_department
    with get_engine().connect() as connection:
        outer = connection.begin()
        try:
            with Session(bind=connection, join_transaction_mode='create_savepoint', expire_on_commit=False) as db:
                home = Department(nombre='QA-' + uuid4().hex, is_active=True)
                db.add(home); db.flush()
                actor = User(email=uuid4().hex+'@example.invalid', nombre_completo='RH QA', departamento_id=home.id, rol_id=1, is_active=True)
                db.add(actor); db.commit()
                result = save_department(db, actor, DepartmentCreate(nombre='QA-' + uuid4().hex, reason='Alta aislada'))
                from uuid import UUID
                ident = UUID(result['id'])
                assert db.scalar(select(DepartmentAudit).where(DepartmentAudit.department_id == ident)).detalle['after']['is_active']
                def fail(session, *_):
                    if any(isinstance(row, DepartmentAudit) for row in session.new):
                        raise SQLAlchemyError('Fallo simulado de auditoría QA')
                event.listen(db, 'before_flush', fail)
                try:
                    with pytest.raises(SQLAlchemyError):
                        save_department(db, actor, DepartmentUpdate(nombre='No persistir', is_active=False, reason='Prueba de rollback'), ident)
                finally:
                    event.remove(db, 'before_flush', fail)
                db.expire_all()
                row = db.get(Department, ident)
                assert row.nombre == result['nombre'] and row.is_active
                assert len(db.scalars(select(DepartmentAudit).where(DepartmentAudit.department_id == ident)).all()) == 1
        finally:
            outer.rollback()


def test_migration_0003_preserves_legacy_cases_in_isolated_schema():
    """DDL en esquema transaccional temporal, sin modificar tablas del proyecto."""
    import importlib.util
    from pathlib import Path
    from uuid import uuid4
    from alembic.migration import MigrationContext
    from alembic.operations import Operations
    schema="qa_"+uuid4().hex
    with get_engine().connect() as c:
        tx=c.begin()
        try:
            c.execute(text('CREATE SCHEMA "'+schema+'"'))
            c.execute(text('SET LOCAL search_path TO "'+schema+'"'))
            def apply(name):
                path=Path(__file__).resolve().parents[1]/"migrations"/"versions"/name
                spec=importlib.util.spec_from_file_location("migration_qa",path)
                module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                with Operations.context(MigrationContext.configure(c)):
                    module.upgrade()
            apply("0001_initial.py");apply("0002_local_auth.py")
            dep,user,first,second=[str(uuid4()) for _ in range(4)]
            c.execute(text("INSERT INTO departamentos (id,nombre) VALUES (:id,'QA aislado')"),{"id":dep})
            c.execute(text("INSERT INTO users (id,email,nombre_completo,departamento_id,rol_id) VALUES (:id,'legacy@example.invalid','QA',:dep,3)"),{"id":user,"dep":dep})
            c.execute(text("INSERT INTO incidencias (id,titulo,descripcion,incident_date,created_by,affected_employee_id,department_id_at_creation) VALUES (:id,'Pendiente original','Texto original',CURRENT_DATE,:u,:u,:d)"),{"id":first,"u":user,"d":dep})
            c.execute(text("INSERT INTO incidencias (id,titulo,descripcion,incident_date,created_by,affected_employee_id,department_id_at_creation,status,assigned_to,category_id,priority,cycle_start_at,validated_by,validated_at,resolution_text,resolved_at) VALUES (:id,'Resuelta original','Texto anterior',CURRENT_DATE,:u,:u,:d,'RESUELTA',:u,4,2,now(),:u,now(),'Resolución anterior',now())"),{"id":second,"u":user,"d":dep})
            apply("0003_incident_scope.py")
            rows=c.execute(text("SELECT id,scope,reported_department_id,classification_valid,descripcion FROM incidencias")).mappings().all()
            assert len(rows)==2
            by_id={str(row['id']):row for row in rows}
            assert by_id[first]['descripcion']=="Texto original"
            assert by_id[first]['classification_valid'] is False
            assert by_id[second]['classification_valid'] is True
            assert all(row['scope']=="PERSONA" and str(row['reported_department_id'])==dep for row in rows)
            env=str(uuid4())
            c.execute(text("INSERT INTO incidencias (id,titulo,descripcion,incident_date,created_by,affected_employee_id,department_id_at_creation,scope,reported_department_id,category_id) VALUES (:id,'Entorno','Riesgo simulado',CURRENT_DATE,:u,NULL,:d,'ENTORNO',:d,4)"),{"id":env,"u":user,"d":dep})
            assert c.execute(text("SELECT affected_employee_id FROM incidencias WHERE id=:id"),{"id":env}).scalar_one() is None
            apply("0004_department_audit.py")
            assert c.execute(text("SELECT count(*) FROM incidencias")).scalar_one() == 3
            assert c.execute(text("SELECT count(*) FROM department_audit_events")).scalar_one() == 0
            assert c.execute(text("SELECT nombre FROM departamentos WHERE id=:id"), {"id": dep}).scalar_one() == 'QA aislado'
            apply('0005_ai_jobs.py')
            assert c.execute(text('SELECT count(*) FROM ai_jobs')).scalar_one() == 0
            assert c.execute(text('SELECT count(*) FROM incidencias WHERE content_revision=0')).scalar_one() == 3
        finally:
            tx.rollback()


def test_mail_outbox_and_smtp_permission_lock_on_postgres(monkeypatch):
    from datetime import date
    from threading import Event
    from concurrent.futures import ThreadPoolExecutor
    from types import SimpleNamespace
    from uuid import uuid4
    from sqlalchemy import delete,select
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import DBAPIError
    from app.models import Department,User,Incident,AuditEvent,MailDelivery
    from app.services.administration_lock import administration_lock
    from app.services.mail import queue_event,process_one
    monkeypatch.setenv('MAIL_ENABLED','true')
    engine=get_engine(); entered=Event(); release=Event()
    depid,adminid,empid,caseid,eventid=[uuid4() for _ in range(5)]
    def factory(): return Session(engine,expire_on_commit=False)
    try:
        with factory() as db:
            db.add(Department(id=depid,nombre='Correo-QA-'+str(depid),is_active=True)); db.flush()
            admin=User(id=adminid,email=str(adminid)+'@example.invalid',nombre_completo='RH simulado',departamento_id=depid,rol_id=1,is_active=True)
            employee=User(id=empid,email=str(empid)+'@example.invalid',nombre_completo='Persona ficticia',departamento_id=depid,rol_id=3,is_active=True)
            db.add_all([admin,employee]); db.flush()
            case=Incident(id=caseid,titulo='Correo QA',descripcion='Solo simulación',incident_date=date(2026,10,18),created_by=empid,affected_employee_id=empid,scope='PERSONA',reported_department_id=depid,department_id_at_creation=depid)
            db.add(case); db.flush()
            audit=AuditEvent(id=eventid,incidencia_id=caseid,usuario_id=empid,accion='CREADO',detalle={})
            db.add(audit); queue_event(db,case,audit); db.commit()
        def send(*_):
            entered.set()
            assert release.wait(10),'No se liberó transporte de prueba'
        with ThreadPoolExecutor(max_workers=1) as pool:
            future=pool.submit(process_one,factory,SimpleNamespace(send=send))
            try:
                assert entered.wait(10)
                # El proceso SMTP conserva bloqueo compartido administrativo y de expediente.
                with factory() as other:
                    other.execute(text("SET LOCAL lock_timeout = '300ms'"))
                    with pytest.raises(DBAPIError) as exc: administration_lock(other,exclusive=True)
                    assert exc.value.orig.sqlstate=='55P03'; other.rollback()
                    other.execute(text("SET LOCAL lock_timeout = '300ms'"))
                    with pytest.raises(DBAPIError) as exc:
                        other.execute(text('UPDATE incidencias SET is_confidential=true WHERE id=:id'),{'id':caseid})
                    assert exc.value.orig.sqlstate=='55P03'; other.rollback()
            finally: release.set()
            assert future.result(timeout=10)
        with factory() as db:
            row=db.scalar(select(MailDelivery).where(MailDelivery.case_id==caseid))
            assert row.status=='ENVIADA' and row.attempts==1
        assert not process_one(factory,SimpleNamespace(send=lambda *_:pytest.fail('Envío duplicado')))
    finally:
        release.set()
        with factory() as db:
            db.execute(delete(MailDelivery).where(MailDelivery.case_id==caseid))
            db.execute(delete(AuditEvent).where(AuditEvent.incidencia_id==caseid))
            db.execute(delete(Incident).where(Incident.id==caseid))
            db.execute(delete(User).where(User.id.in_([adminid,empid])))
            db.execute(delete(Department).where(Department.id==depid)); db.commit()
