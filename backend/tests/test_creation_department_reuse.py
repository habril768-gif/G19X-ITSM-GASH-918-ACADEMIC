"""Reutilizacion local del departamento revalidado; sin HTTP ni locks PostgreSQL reales."""
from contextlib import contextmanager
from datetime import date
from types import SimpleNamespace
import unittest
from fastapi import HTTPException
from sqlalchemy import event,func,select,update
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import TextClause
from app.models import Department,Incident,User
from app.services.administration_lock import administration_lock
from app.services.incidents import create_case
import test_read_query_grouping as fixtures


class CreationDepartmentReuseTests(unittest.TestCase):
    def setUp(self):
        self.world=fixtures.ReadQueryGroupingTests('test_detail_one_query_and_no_sql_when_capturing_dto')
        self.world.setUp();self.addCleanup(self.world.tearDown)
        self.engine=self.world.engine
        self.actor_id=self.world.actors['admin'].id
        self.one_id,self.two_id=self.world.one.id,self.world.two.id

    def body(self,department_id):
        return SimpleNamespace(titulo='Ficticio',descripcion='Sin datos reales',scope='ENTORNO',
            affected_employee_id=None,participants=[],reported_department_id=department_id,
            incident_date=date(2026,10,27),is_confidential=False)

    @contextmanager
    def calls(self,db):
        result=[];state={'committed':False,'after_commit':0}
        def committed(session):state['committed']=True
        def observe(conn,cursor,sql,parameters,context,executemany):
            result.append(sql)
            if state['committed']:state['after_commit']+=1
        event.listen(self.engine,'before_cursor_execute',observe)
        event.listen(db,'after_commit',committed)
        try:yield result,state
        finally:
            event.remove(self.engine,'before_cursor_execute',observe)
            event.remove(db,'after_commit',committed)

    def test_same_department_saves_one_select_and_has_no_postcommit_sql(self):
        with Session(self.engine) as db:
            actor=db.get(User,self.actor_id)
            with self.calls(db) as (queries,state):receipt=create_case(db,actor,self.body(self.one_id))
            self.assertTrue(receipt['received'] and receipt['can_view'])
            self.assertEqual(len(queries),7)
            self.assertFalse(any(sql.startswith('SELECT departamentos.') for sql in queries))
            self.assertEqual(state['after_commit'],0)
            self.assertEqual(db.get(Incident,receipt['id']).department_id_at_creation,self.one_id)

    def test_other_department_keeps_its_select_and_actual_department(self):
        with Session(self.engine) as db:
            actor=db.get(User,self.actor_id)
            with self.calls(db) as (queries,state):receipt=create_case(db,actor,self.body(self.two_id))
            self.assertEqual(len(queries),8)
            self.assertEqual(sum(sql.startswith('SELECT departamentos.') for sql in queries),1)
            self.assertEqual(state['after_commit'],0)
            case=db.get(Incident,receipt['id'])
            self.assertEqual((case.reported_department_id,case.department_id_at_creation),(self.two_id,self.two_id))

    def test_returned_department_and_actor_are_refreshed_after_transfer(self):
        db=self.world.db;actor=self.world.actors['admin']
        db.execute(update(User).where(User.id==actor.id).values(departamento_id=self.two_id),execution_options={'synchronize_session':False})
        db.commit();self.assertEqual(actor.departamento_id,self.one_id)
        with self.calls(db) as (queries,_):
            role,department=administration_lock(db,actor,include_role=True,include_department=True)
        self.assertEqual(role,'ADMIN_RH');self.assertEqual(department.id,self.two_id)
        self.assertEqual(actor.departamento_id,self.two_id);self.assertEqual(len(queries),1)
        self.assertIs(department,self.world.two)

    def test_stale_inactive_actor_department_is_denied(self):
        db=self.world.db;actor=self.world.actors['admin']
        db.execute(update(Department).where(Department.id==self.one_id).values(is_active=False),execution_options={'synchronize_session':False})
        db.commit();self.assertTrue(self.world.one.is_active)
        with self.assertRaises(HTTPException) as caught:create_case(db,actor,self.body(self.one_id))
        self.assertEqual((caught.exception.status_code,caught.exception.detail),(403,'Cuenta no habilitada'))

    def test_inactive_other_department_keeps_422(self):
        with Session(self.engine) as db:
            db.execute(update(Department).where(Department.id==self.two_id).values(is_active=False));db.commit()
            actor=db.get(User,self.actor_id)
            before=db.scalar(select(func.count()).select_from(Incident))
            with self.assertRaises(HTTPException) as caught:create_case(db,actor,self.body(self.two_id))
            self.assertEqual((caught.exception.status_code,caught.exception.detail),(422,'Departamento no habilitado'))
            self.assertEqual(db.scalar(select(func.count()).select_from(Incident)),before)

    def test_cross_department_stays_forbidden_to_employee_and_supervisor(self):
        for name in ('employee','super'):
            with self.subTest(actor=name),Session(self.engine) as db:
                actor=db.get(User,self.world.actors[name].id)
                before=db.scalar(select(func.count()).select_from(Incident))
                with self.assertRaises(HTTPException) as caught:create_case(db,actor,self.body(self.two_id))
                self.assertEqual((caught.exception.status_code,caught.exception.detail),(403,'Registro fuera del ámbito autorizado'))
                self.assertEqual(db.scalar(select(func.count()).select_from(Incident)),before)
                db.rollback()
                receipt=create_case(db,actor,self.body(self.one_id))
                self.assertTrue(receipt['received'])

    def test_include_department_requires_role_before_sql(self):
        with self.calls(self.world.db) as (queries,_):
            with self.assertRaises(ValueError):administration_lock(self.world.db,self.world.actors['admin'],include_department=True)
        self.assertEqual(queries,[])

    def test_department_refresh_stays_after_advisory_lock(self):
        for exclusive in (False,True):
            with self.subTest(exclusive=exclusive),Session(self.engine,expire_on_commit=False) as db:
                actor=db.get(User,self.actor_id);calls=[]
                original_bind,original_execute=db.bind,db.execute
                fake_bind=SimpleNamespace(dialect=SimpleNamespace(name='postgresql'))
                def execute(statement):
                    db.bind=original_bind
                    try:
                        if isinstance(statement,TextClause):
                            calls.append(str(statement))
                            original_execute(update(User).where(User.id==self.actor_id).values(departamento_id=self.two_id),execution_options={'synchronize_session':False})
                            return None
                        calls.append('REFRESH_ROLE_DEPARTMENT')
                        return original_execute(statement)
                    finally:db.bind=fake_bind
                db.bind,db.execute=fake_bind,execute
                try:role,department=administration_lock(db,actor,exclusive,include_role=True,include_department=True)
                finally:db.bind,db.execute=original_bind,original_execute
                self.assertEqual(role,'ADMIN_RH');self.assertEqual(department.id,self.two_id)
                function='pg_advisory_xact_lock' if exclusive else 'pg_advisory_xact_lock_shared'
                self.assertEqual(calls,[f'SELECT {function}(71419322)','REFRESH_ROLE_DEPARTMENT'])
                db.rollback()
