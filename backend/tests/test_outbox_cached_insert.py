"""Outbox: lotes reales, cache de compilacion y atomicidad, sin HTTP/SMTP."""
from math import ceil
import unittest
from uuid import NAMESPACE_URL,uuid5
from sqlalchemy import event,select
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import SQLAlchemyError
from app.core.security import utcnow
from app.models import AuditEvent,IncidentParticipant,MailDelivery,Role,User
from app.services.mail import allowed,queue_event
import test_read_query_grouping as fixtures


def delivery_insert(statement,context):
    table=getattr(getattr(getattr(context,'compiled',None),'statement',None),'table',None)
    return table is not None and table.name=='mail_deliveries' and statement.lstrip().upper().startswith('INSERT')


class OutboxCachedInsertTests(unittest.TestCase):
    def setUp(self):
        self.world=fixtures.ReadQueryGroupingTests('test_detail_one_query_and_no_sql_when_capturing_dto')
        self.world.setUp()
        self.addCleanup(self.world.tearDown)
        self.db=self.world.db

    def configure_recipients(self,size):
        admins=self.db.scalars(select(User).join(Role,User.rol_id==Role.id).where(Role.nombre=='ADMIN_RH')).all()
        for index,person in enumerate(admins):person.is_active=index<size
        for index in range(max(0,size-len(admins))):
            self.db.add(User(email=f'cached-rh-{index}@example.invalid',nombre_completo='Ficticio',
                rol_id=1,departamento_id=self.world.one.id,is_active=True))
        self.db.commit()

    def audit(self,case=None):
        case=case or self.world.cases[0]
        audit=AuditEvent(incidencia_id=case.id,usuario_id=self.world.actors['employee'].id,accion='CREADO',detalle={})
        self.db.add(audit);self.db.flush()
        return case,audit

    def deliveries(self,audit):
        return self.db.scalars(select(MailDelivery).where(MailDelivery.event_id==audit.id)).all()

    def test_effective_batches_preserve_all_fields_without_dbapi_executemany(self):
        self.configure_recipients(123)
        case,audit=self.audit();calls=[];many=[]
        def execute(cursor,statement,parameters,context):
            if delivery_insert(statement,context):calls.append((len(parameters),context.execute_style.name))
        def executemany(cursor,statement,parameters,context):
            if delivery_insert(statement,context):many.append(statement)
        event.listen(self.db.bind,'do_execute',execute);event.listen(self.db.bind,'do_executemany',executemany)
        try:queue_event(self.db,case,audit)
        finally:
            event.remove(self.db.bind,'do_execute',execute);event.remove(self.db.bind,'do_executemany',executemany)
        self.assertEqual(len(calls),ceil(123/50));self.assertFalse(many)
        self.assertTrue(all(count<=600 and style=='INSERTMANYVALUES' for count,style in calls))
        rows=self.deliveries(audit);self.assertEqual(len(rows),123)
        self.assertEqual({row.recipient_id for row in rows},set(self.db.scalars(select(User.id).where(User.rol_id==1,User.is_active.is_(True)))))
        for row in rows:
            self.assertEqual(row.id,uuid5(NAMESPACE_URL,f'plurione-mail:{audit.id}:{row.recipient_id}'))
            self.assertEqual((row.case_id,row.event_id,row.kind,row.status,row.attempts),(case.id,audit.id,'CREACION','PENDIENTE',0))
            self.assertEqual(row.context,{'assigned_to':None,'resolved_at':None,'cycle_start_at':None})
            self.assertIsNone(row.error);self.assertIsNone(row.completed_at)
            self.assertIsNone(row.lease_token);self.assertIsNone(row.lease_until)
            self.assertIsNotNone(row.created_at);self.assertIsNotNone(row.available_at)

    def test_compilation_reused_without_leaking_event_or_case_values(self):
        self.configure_recipients(10);calls=[]
        def observe(conn,cursor,statement,parameters,context,executemany):
            if delivery_insert(statement,context):calls.append((str(context.cache_hit),context.compiled.statement))
        event.listen(self.db.bind,'before_cursor_execute',observe)
        try:
            one,event_one=self.audit(self.world.cases[0]);queue_event(self.db,one,event_one)
            two,event_two=self.audit(self.world.cases[1]);queue_event(self.db,two,event_two)
        finally:event.remove(self.db.bind,'before_cursor_execute',observe)
        self.assertEqual(len(calls),2);self.assertTrue(calls[1][0].endswith('CACHE_HIT'))
        self.assertIsNotNone(calls[0][1]._generate_cache_key())
        self.assertIn('RETURNING',str(calls[0][1].compile(dialect=postgresql.dialect())))
        self.assertEqual({r.case_id for r in self.deliveries(event_one)},{one.id})
        self.assertEqual({r.case_id for r in self.deliveries(event_two)},{two.id})
        self.assertTrue({r.id for r in self.deliveries(event_one)}.isdisjoint({r.id for r in self.deliveries(event_two)}))

    def test_empty_recipient_set_records_omission(self):
        self.configure_recipients(0);case,audit=self.audit();queue_event(self.db,case,audit)
        rows=self.deliveries(audit);self.assertEqual(len(rows),1)
        row=rows[0];self.assertIsNone(row.recipient_id)
        self.assertEqual((row.status,row.error,row.attempts),('OMITIDA','Sin destinatario autorizado',0))
        self.assertIsNotNone(row.completed_at)

    def test_permissions_requeried_after_warm_insert(self):
        self.configure_recipients(2);case,first=self.audit();queue_event(self.db,case,first)
        self.assertEqual(len(self.deliveries(first)),2)
        admin=self.world.actors['admin'];other=self.world.actors['admin2']
        self.db.add(IncidentParticipant(incidencia_id=case.id,user_id=admin.id,declaration_reason='Ficticio',review_status='DECLARADO'))
        self.db.flush();case,second=self.audit();queue_event(self.db,case,second)
        self.assertEqual({r.recipient_id for r in self.deliveries(second)},{other.id})
        other.is_active=False;self.db.flush();case,third=self.audit();queue_event(self.db,case,third)
        self.assertEqual({r.recipient_id for r in self.deliveries(third)},{None})

    def test_retry_preserves_existing_sent_delivery(self):
        self.configure_recipients(2);case,audit=self.audit();queue_event(self.db,case,audit);self.db.commit()
        sent,missing=self.deliveries(audit);missing_id=missing.id
        sent.status='ENVIADA';sent.attempts=2;sent.completed_at=utcnow()
        self.db.delete(missing);self.db.commit()
        previous=(sent.id,sent.status,sent.attempts,sent.created_at,sent.available_at,sent.completed_at,sent.context.copy())
        queue_event(self.db,case,audit);self.db.commit()
        self.assertEqual((sent.id,sent.status,sent.attempts,sent.created_at,sent.available_at,sent.completed_at,sent.context),previous)
        self.assertEqual(self.db.get(MailDelivery,missing_id).status,'PENDIENTE')
        self.assertEqual(len(self.deliveries(audit)),2)

    def test_second_batch_failure_rolls_back_first_and_audit(self):
        self.configure_recipients(123);case,audit=self.audit();ident=audit.id;calls=[]
        def fail(conn,cursor,statement,parameters,context,executemany):
            if delivery_insert(statement,context):
                calls.append(statement)
                if len(calls)==2:raise SQLAlchemyError('Fallo ficticio')
        event.listen(self.db.bind,'before_cursor_execute',fail)
        try:
            with self.assertRaises(SQLAlchemyError):queue_event(self.db,case,audit)
            self.db.rollback()
        finally:event.remove(self.db.bind,'before_cursor_execute',fail)
        self.assertEqual(len(calls),2)
        self.assertIsNone(self.db.get(AuditEvent,ident))
        self.assertEqual(list(self.db.scalars(select(MailDelivery))),[])

    def test_repeated_queue_does_not_insert_or_commit(self):
        self.configure_recipients(1);case,audit=self.audit();queue_event(self.db,case,audit)
        before={r.id for r in self.deliveries(audit)};calls=[];commits=[]
        def observe(conn,cursor,statement,parameters,context,executemany):
            if delivery_insert(statement,context):calls.append(statement)
        def commit(session):commits.append(True)
        event.listen(self.db.bind,'before_cursor_execute',observe);event.listen(self.db,'after_commit',commit)
        try:queue_event(self.db,case,audit)
        finally:
            event.remove(self.db.bind,'before_cursor_execute',observe);event.remove(self.db,'after_commit',commit)
        self.assertFalse(calls);self.assertFalse(commits)
        self.assertEqual({r.id for r in self.deliveries(audit)},before)

    def test_create_case_failure_rolls_back_incident_audit_and_deliveries(self):
        from datetime import date
        from types import SimpleNamespace
        from fastapi import HTTPException
        from sqlalchemy import func
        from app.models import Incident
        from app.services.incidents import create_case
        self.configure_recipients(123)
        models=(Incident,AuditEvent,MailDelivery)
        before=tuple(self.db.scalar(select(func.count()).select_from(model)) for model in models)
        body=SimpleNamespace(titulo='Ficticio',descripcion='Sin datos reales',scope='ENTORNO',
            affected_employee_id=None,participants=[],reported_department_id=self.world.one.id,
            incident_date=date(2026,10,27),is_confidential=False)
        calls=[]
        def fail(conn,cursor,statement,parameters,context,executemany):
            if delivery_insert(statement,context):
                calls.append(statement)
                if len(calls)==2:raise SQLAlchemyError('Fallo ficticio')
        event.listen(self.db.bind,'before_cursor_execute',fail)
        try:
            with self.assertRaises(HTTPException) as caught:
                create_case(self.db,self.world.actors['admin'],body)
        finally:event.remove(self.db.bind,'before_cursor_execute',fail)
        self.assertEqual(caught.exception.status_code,503)
        self.assertEqual(len(calls),2)
        self.assertEqual(tuple(self.db.scalar(select(func.count()).select_from(model)) for model in models),before)
