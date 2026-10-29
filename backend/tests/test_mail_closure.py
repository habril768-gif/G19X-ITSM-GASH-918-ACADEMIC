"""Avisos de cierre: ciclo vigente, permisos y atomicidad en servicios reales."""
from datetime import date
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
from uuid import UUID

from alembic import command
from alembic.config import Config
from fastapi import HTTPException
from sqlalchemy import event, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import AuditEvent, Category, Incident, MailDelivery
from app.services.incidents import create_case
from app.services.lifecycle import manage_case
from app.services.mail import process_one, queue_event
import test_read_query_grouping as fixtures


class MailClosureTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.ReadQueryGroupingTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.db = self.fixture.db
        self.actors = self.fixture.actors
        self.db.add(Category(id=2, nombre='Conflicto ficticio', descripcion='QA'))
        self.db.commit()

    def resolved(self, confidential=False, different_reporter=False):
        creator = self.actors['admin'] if different_reporter else self.actors['employee']
        body = SimpleNamespace(titulo='Ficticio', descripcion='Sin datos reales', scope='PERSONA',
            affected_employee_id=self.actors['employee'].id, participants=[],
            reported_department_id=self.fixture.one.id, incident_date=date(2026, 10, 29),
            is_confidential=confidential)
        ident = create_case(self.db, creator, body)['id']
        ident = UUID(str(ident))
        self.transition(ident, 'classification', category_id=2, priority=2)
        assignee = self.actors['admin2'] if confidential else self.actors['super']
        self.transition(ident, 'transition', status='EN_REVISION', assigned_to=assignee.id)
        self.transition(ident, 'transition', status='RESUELTA', resolution_text='Resolución ficticia')
        # Consumir los demás trabajos lógicamente para aislar únicamente el cierre.
        for row in self.db.scalars(select(MailDelivery)):
            row.status = 'OMITIDA'
        self.db.commit()
        return ident

    def transition(self, ident, operation='transition', **values):
        defaults = dict(reason=None, assigned_to=None, resolution_text=None)
        defaults.update(values)
        return manage_case(self.db, self.actors['admin'], ident, operation, SimpleNamespace(**defaults))

    def closures(self, ident):
        self.db.expire_all()
        return self.db.scalars(select(MailDelivery).where(
            MailDelivery.case_id == ident, MailDelivery.kind == 'CIERRE')).all()

    def dispatch(self):
        transport = Mock()
        from unittest.mock import patch
        with patch.dict('os.environ', {'MAIL_ENABLED': 'true'}):
            while process_one(lambda: Session(self.db.bind, expire_on_commit=False), transport):
                pass
        return transport

    def test_close_deduplicates_and_queues_once_per_event(self):
        ident = self.resolved()
        case = self.transition(ident, status='CERRADA')
        row, = self.closures(ident)
        self.assertEqual(row.recipient_id, self.actors['employee'].id)
        audit = self.db.get(AuditEvent, row.event_id)
        queue_event(self.db, case, audit, {'status': 'RESUELTA'}); self.db.commit()
        self.assertEqual(len(self.closures(ident)), 1)
        transport = self.dispatch()
        self.assertEqual(transport.send.call_count, 1)
        self.assertEqual(transport.send.call_args.args[0], 'employee@example.invalid')
        self.assertEqual(self.closures(ident)[0].status, 'ENVIADA')

    def test_different_reporter_and_affected_each_receive_one(self):
        ident = self.resolved(different_reporter=True)
        self.transition(ident, status='CERRADA')
        self.assertEqual({row.recipient_id for row in self.closures(ident)},
                         {self.actors['admin'].id, self.actors['employee'].id})
        self.assertEqual(self.dispatch().send.call_count, 2)

    def test_confidential_close_records_omission_without_recipient(self):
        ident = self.resolved(confidential=True)
        self.transition(ident, status='CERRADA')
        row, = self.closures(ident)
        self.assertEqual((row.status, row.recipient_id), ('OMITIDA', None))
        self.dispatch().send.assert_not_called()

    def test_permission_is_rechecked_at_dispatch(self):
        ident = self.resolved()
        self.transition(ident, status='CERRADA')
        self.actors['employee'].is_active = False; self.db.commit()
        self.dispatch().send.assert_not_called()
        self.assertEqual(self.closures(ident)[0].status, 'OMITIDA')

    def test_reopening_omits_queued_close(self):
        ident = self.resolved()
        self.transition(ident, status='CERRADA')
        self.transition(ident, status='EN_REVISION', reason='Revisión ficticia')
        self.dispatch()
        self.assertEqual(self.closures(ident)[0].status, 'OMITIDA')

    def test_second_cycle_does_not_send_stale_first_close(self):
        ident = self.resolved()
        self.transition(ident, status='CERRADA')
        self.transition(ident, status='EN_REVISION', reason='Revisión ficticia')
        self.transition(ident, status='RESUELTA', resolution_text='Nueva resolución ficticia')
        self.transition(ident, status='CERRADA')
        transport = self.dispatch()
        rows = self.closures(ident)
        self.assertEqual(sorted(row.status for row in rows), ['ENVIADA', 'OMITIDA'])
        # Otros eventos del ciclo pueden enviarse; solo el cierre vigente debe hacerlo.
        closure_ids = {row.id for row in rows}
        sent_closures = [call.args[2] for call in transport.send.call_args_list if call.args[2] in closure_ids]
        self.assertEqual(len(sent_closures), 1)

    def test_outbox_failure_rolls_back_close_and_audit(self):
        ident = self.resolved()
        count = self.db.scalar(select(func.count()).select_from(AuditEvent))
        def fail(conn, cursor, statement, parameters, context, executemany):
            if statement.lstrip().upper().startswith('INSERT INTO MAIL_DELIVERIES'):
                raise SQLAlchemyError('Fallo simulado')
        event.listen(self.db.bind, 'before_cursor_execute', fail)
        try:
            with self.assertRaises(HTTPException) as error:
                self.transition(ident, status='CERRADA')
            self.assertEqual(error.exception.status_code, 503)
        finally:
            event.remove(self.db.bind, 'before_cursor_execute', fail)
        case = self.db.get(Incident, ident)
        self.assertEqual(case.status, 'RESUELTA')
        self.assertIsNone(case.closed_at)
        self.assertEqual(self.db.scalar(select(func.count()).select_from(AuditEvent)), count)
        self.assertEqual(self.closures(ident), [])

    def test_migration_extends_constraint_without_data_update(self):
        backend = Path(__file__).resolve().parents[1]
        output = StringIO()
        config = Config(str(backend / 'alembic.ini'), output_buffer=output)
        config.set_main_option('script_location', str(backend / 'migrations'))
        command.upgrade(config, '0007:head', sql=True)
        sql = output.getvalue()
        self.assertIn('DROP CONSTRAINT ck_mail_kind', sql)
        self.assertIn("'CIERRE'", sql)
        self.assertNotIn('UPDATE mail_deliveries', sql)
        self.assertNotIn('DELETE FROM mail_deliveries', sql)
