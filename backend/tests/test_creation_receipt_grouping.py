"""Destinatarios y permiso del recibo en una lectura, incluso sin destinatarios."""
from uuid import UUID

import pytest
from fastapi import HTTPException
from sqlalchemy import event

from app.models import Incident, IncidentParticipant
from app.services.incidents import visible_case
from app.services.mail import creation_recipient_ids, creation_recipients_and_access
from test_incidents import create, payload, world


@pytest.mark.parametrize('actor', ['employee', 'super', 'admin'])
@pytest.mark.parametrize('scope', ['PERSONA', 'ENTORNO'])
@pytest.mark.parametrize('confidential', [False, True])
def test_receipt_matches_authorized_detail_for_roles_and_scopes(world, actor, scope, confidential):
    client, db, actors, selected, one, _ = world
    selected['user'] = actors[actor]
    body = payload(scope=scope, is_confidential=confidential)
    if scope == 'ENTORNO':
        body['reported_department_id'] = str(one.id)
    elif actor != 'employee':
        body['affected_employee_id'] = str(actors['employee'].id)
    response = client.post('/incidents', json=body)
    assert response.status_code == 201, response.text
    receipt = response.json()
    try:
        visible_case(db, actors[actor], UUID(receipt['id']))
        expected = True
    except HTTPException as error:
        assert error.status_code == 404
        expected = False
    assert receipt['can_view'] is expected


def test_combined_read_fresh_conflicts_and_zero_recipients(world):
    client, db, actors, *_ = world
    case = db.get(Incident, UUID(create(client)))
    recipients, access = creation_recipients_and_access(db, case, actors['admin'], 'ADMIN_RH')
    assert recipients == creation_recipient_ids(db, case) and access
    relation = IncidentParticipant(incidencia_id=case.id, user_id=actors['admin'].id,
                                   declaration_reason='Conflicto ficticio')
    db.add(relation)
    actors['admin2'].is_active = False
    db.flush()
    recipients, access = creation_recipients_and_access(db, case, actors['admin'], 'ADMIN_RH')
    assert recipients == set() and not access
    # Un gestor implicado también restringe el acceso del empleado.
    assert creation_recipients_and_access(db, case, actors['employee'], 'EMPLEADO') == (set(), False)
    db.delete(relation)
    actors['admin'].is_active = False
    db.flush()
    recipients, access = creation_recipients_and_access(db, case, actors['employee'], 'EMPLEADO')
    assert recipients == set() and access
    case.is_confidential = True
    db.flush()
    assert creation_recipients_and_access(db, case, actors['employee'], 'EMPLEADO') == (set(), False)


def test_environment_creation_reads_actor_and_combined_recipients_receipt_only(world):
    client, db, actors, selected, one, _ = world
    queries = []
    def observe(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith('SELECT'):
            queries.append(statement)
    event.listen(db.bind, 'before_cursor_execute', observe)
    try:
        response = client.post('/incidents', json=payload(scope='ENTORNO', reported_department_id=str(one.id)))
    finally:
        event.remove(db.bind, 'before_cursor_execute', observe)
    assert response.status_code == 201, response.text
    assert response.json()['can_view'] is True
    assert len(queries) == 2, queries
    assert 'mail' not in response.json()
