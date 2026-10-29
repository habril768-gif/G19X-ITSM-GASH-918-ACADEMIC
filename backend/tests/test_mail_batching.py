"""Regresiones de destinatarios y consultas del encolado, sin enviar correo."""
from uuid import UUID
import pytest
from sqlalchemy import event, select
from app.core.security import utcnow
from app.models import AuditEvent, Incident, IncidentParticipant, MailDelivery, Role, User
from app.services.mail import allowed, queue_event
from test_incidents import world, create


@pytest.mark.parametrize('additional', [0, 8, 28])
def test_creation_queue_has_two_selects_independent_of_recipient_count(world, additional):
    client, db, actors, chosen, department, _ = world
    case_id = create(client)
    db.add_all([User(email=f'batch-rh-{index}@example.invalid', nombre_completo='RH ficticio',
                     rol_id=1, departamento_id=department.id, is_active=True) for index in range(additional)])
    db.commit()
    case = db.get(Incident, UUID(case_id))
    audit = AuditEvent(incidencia_id=case.id, usuario_id=actors['employee'].id, accion='CREADO', detalle={})
    db.add(audit)
    db.flush()
    selects = []
    def observe(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith('SELECT'):
            selects.append(statement)
    event.listen(db.bind, 'before_cursor_execute', observe)
    try:
        queue_event(db, case, audit)
        db.flush()
    finally:
        event.remove(db.bind, 'before_cursor_execute', observe)
    assert len(selects) == 2
    rows = db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id)).all()
    assert len(rows) == 2 + additional
    assert all(row.recipient_id is not None and row.status == 'PENDIENTE' for row in rows)
    first_ids = {row.id for row in rows}
    queue_event(db, case, audit)
    db.flush()
    assert {row.id for row in db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id))} == first_ids


@pytest.mark.parametrize('change', [
    'confidential', 'declared', 'confirmed', 'discarded', 'affected_rh',
    'inactive_user', 'inactive_department', 'changed_role', 'no_recipients',
])
def test_batched_creation_recipients_match_existing_access_check(world, change):
    client, db, actors, chosen, department, other_department = world
    case_id = create(client)
    case = db.get(Incident, UUID(case_id))
    if change == 'confidential':
        case.is_confidential = True
    elif change in {'declared', 'confirmed', 'discarded'}:
        status = {'declared': 'DECLARADO', 'confirmed': 'CONFIRMADO', 'discarded': 'DESCARTADO'}[change]
        relation = IncidentParticipant(incidencia_id=case.id, user_id=actors['admin'].id,
                                       declaration_reason='Relación ficticia', review_status=status)
        if status != 'DECLARADO':
            relation.reviewed_by = actors['admin2'].id
            relation.reviewed_at = utcnow()
            relation.review_reason = 'Revisión ficticia independiente'
        db.add(relation)
    elif change == 'affected_rh':
        case.affected_employee_id = actors['admin'].id
    elif change == 'inactive_user':
        actors['admin'].is_active = False
    elif change == 'inactive_department':
        other_department.is_active = False
    elif change == 'changed_role':
        actors['admin'].rol_id = 2
    elif change == 'no_recipients':
        actors['admin'].is_active = actors['admin2'].is_active = False
    db.flush()
    candidates = db.scalars(select(User).join(Role, User.rol_id == Role.id).where(Role.nombre == 'ADMIN_RH')).all()
    expected = {person.id for person in candidates if allowed(db, case, person)}
    if change in {'declared', 'confirmed', 'affected_rh', 'inactive_user', 'changed_role'}:
        assert expected == {actors['admin2'].id}
    elif change == 'inactive_department':
        assert expected == {actors['admin'].id}
    elif change == 'no_recipients':
        assert expected == set()
    else:
        assert expected == {actors['admin'].id, actors['admin2'].id}
    audit = AuditEvent(incidencia_id=case.id, usuario_id=actors['employee'].id, accion='CREADO', detalle={})
    db.add(audit)
    queue_event(db, case, audit)
    db.flush()
    rows = db.scalars(select(MailDelivery).where(MailDelivery.event_id == audit.id)).all()
    assert {row.recipient_id for row in rows} == (expected or {None})
    assert all(row.status == ('PENDIENTE' if row.recipient_id else 'OMITIDA') for row in rows)


def test_batch_deliveries_share_the_event_transaction(world):
    client, db, actors, *_ = world
    case_id = create(client)
    case = db.get(Incident, UUID(case_id))
    audit = AuditEvent(incidencia_id=case.id, usuario_id=actors['employee'].id, accion='CREADO', detalle={})
    db.add(audit)
    queue_event(db, case, audit)
    db.flush()
    event_id = audit.id
    assert db.scalars(select(MailDelivery).where(MailDelivery.event_id == event_id)).all()
    db.rollback()
    assert db.get(AuditEvent, event_id) is None
    assert not db.scalars(select(MailDelivery).where(MailDelivery.event_id == event_id)).all()
