"""INSERT multirregistro: forma efectiva, estado conservado y fallo entre lotes."""
from math import ceil
from uuid import UUID, NAMESPACE_URL, uuid5
import pytest
from sqlalchemy import event, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import SQLAlchemyError
from app.core.security import utcnow
from app.models import AuditEvent, Incident, MailDelivery, User
from app.services.mail import queue_event
from test_incidents import create, world


def prepare(world, size):
    client, db, actors, selected, department, other = world
    cid = UUID(create(client))
    db.add_all([User(email=f'multi-rh-{index}@example.invalid', nombre_completo='RH ficticio',
        rol_id=1, departamento_id=department.id, is_active=True) for index in range(size - 2)])
    db.commit()
    case = db.get(Incident, cid)
    audit = AuditEvent(incidencia_id=cid, usuario_id=actors['employee'].id, accion='CREADO', detalle={})
    db.add(audit); db.flush()
    return db, case, audit


def is_delivery_insert(statement, context):
    table = getattr(getattr(getattr(context, 'compiled', None), 'statement', None), 'table', None)
    return table is not None and table.name == 'mail_deliveries' and statement.lstrip().upper().startswith('INSERT')


@pytest.mark.parametrize('size', [2, 10, 30, 123])
def test_values_insert_has_bounded_statements_and_preserves_rows(world, size):
    db, case, audit = prepare(world, size)
    calls = []
    def observe(conn, cursor, statement, parameters, context, executemany):
        if is_delivery_insert(statement, context):
            compiled_pg = context.compiled.statement.compile(dialect=postgresql.dialect())
            calls.append((context.execute_style.name, len(parameters), len(compiled_pg.params)))
    event.listen(db.bind, 'before_cursor_execute', observe)
    try:
        queue_event(db, case, audit)
        db.flush()
    finally:
        event.remove(db.bind, 'before_cursor_execute', observe)
    assert len(calls) == ceil(size / 50)
    # executemany del contexto indica varios parametros logicos; insertmanyvalues
    # usa cursor.execute por lote (comprobado en test_outbox_cached_insert).
    assert all(style == 'INSERTMANYVALUES' and sqlite_parameters <= 600 and pg_parameters <= 999
               for style, sqlite_parameters, pg_parameters in calls)
    rows = db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id)).all()
    expected = set(db.scalars(select(User.id).where(User.rol_id == 1, User.is_active.is_(True))))
    assert len(rows) == size and {row.recipient_id for row in rows} == expected
    for row in rows:
        assert row.id == uuid5(NAMESPACE_URL, f'plurione-mail:{audit.id}:{row.recipient_id}')
        assert row.case_id == case.id and row.kind == 'CREACION'
        assert row.status == 'PENDIENTE' and row.attempts == 0
        assert row.context == {'assigned_to': None, 'resolved_at': None, 'cycle_start_at': None}
        assert row.error is None and row.completed_at is None
        assert row.lease_until is None and row.lease_token is None
    first_ids = {row.id for row in rows}
    calls.clear()
    event.listen(db.bind, 'before_cursor_execute', observe)
    try:
        queue_event(db, case, audit)
        db.flush()
    finally:
        event.remove(db.bind, 'before_cursor_execute', observe)
    assert calls == []
    assert {row.id for row in db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id))} == first_ids


def test_partial_retry_preserves_sent_row_and_only_fills_missing(world):
    db, case, audit = prepare(world, 2)
    queue_event(db, case, audit); db.commit()
    rows = db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id)).all()
    sent, missing = rows
    sent.status, sent.attempts, sent.completed_at = 'ENVIADA', 2, utcnow()
    missing_id = missing.id
    db.delete(missing); db.commit()
    expected = (sent.status, sent.attempts, sent.completed_at, sent.created_at, sent.available_at, sent.context.copy())
    queue_event(db, case, audit); db.commit()
    db.refresh(sent)
    # SQLite normaliza zona horaria al leer; comparar instantes sin zona aquí.
    assert (sent.status, sent.attempts) == expected[:2]
    for actual, previous in ((sent.completed_at, expected[2]), (sent.created_at, expected[3]), (sent.available_at, expected[4])):
        assert actual.replace(tzinfo=None) == previous.replace(tzinfo=None)
    assert sent.context == expected[5]
    restored = db.get(MailDelivery, missing_id)
    assert restored is not None and restored.status == 'PENDIENTE' and restored.attempts == 0
    assert len(db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id)).all()) == 2


def test_failure_in_second_chunk_can_roll_back_prior_chunk_and_audit(world):
    db, case, audit = prepare(world, 123)
    event_id, cid = audit.id, case.id
    before = set(db.scalars(select(MailDelivery.id)))
    calls = []
    def fail_second(conn, cursor, statement, parameters, context, executemany):
        if is_delivery_insert(statement, context):
            calls.append(statement)
            if len(calls) == 2:
                raise SQLAlchemyError('Fallo simulado en segundo lote')
    event.listen(db.bind, 'before_cursor_execute', fail_second)
    try:
        with pytest.raises(SQLAlchemyError):
            queue_event(db, case, audit)
        db.rollback()
    finally:
        event.remove(db.bind, 'before_cursor_execute', fail_second)
    assert len(calls) == 2
    assert db.get(Incident, cid) is not None
    assert db.get(AuditEvent, event_id) is None
    assert not db.scalars(select(MailDelivery).where(MailDelivery.event_id == event_id)).all()
    assert set(db.scalars(select(MailDelivery.id))) == before
