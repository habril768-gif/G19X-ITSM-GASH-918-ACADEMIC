"""Reutilizar estructuras no debe conservar permisos ni destinatarios antiguos."""
from uuid import UUID

from sqlalchemy.dialects import postgresql

from app.models import Incident, IncidentParticipant
from app.services.incidents import _case_access_statement, case_access_for_current_role
from app.services.mail import _creation_recipients_statement, creation_recipient_ids
from test_incidents import create, world


def test_employee_access_rechecks_confidentiality_and_actor_between_calls(world):
    client, db, actors, *_ = world
    case = db.get(Incident, UUID(create(client)))
    assert case_access_for_current_role(db, actors['employee'], case.id, 'EMPLEADO')
    assert not case_access_for_current_role(db, actors['peer'], case.id, 'EMPLEADO')
    case.is_confidential = True
    db.flush()
    assert not case_access_for_current_role(db, actors['employee'], case.id, 'EMPLEADO')
    case.is_confidential = False
    db.flush()
    assert case_access_for_current_role(db, actors['employee'], case.id, 'EMPLEADO')


def test_manager_access_rechecks_conflict_after_structure_warmup(world):
    client, db, actors, *_ = world
    case = db.get(Incident, UUID(create(client)))
    assert case_access_for_current_role(db, actors['admin'], case.id, 'ADMIN_RH')
    assert case_access_for_current_role(db, actors['super'], case.id, 'SUPERVISOR')
    db.add(IncidentParticipant(incidencia_id=case.id, user_id=actors['admin'].id,
                               declaration_reason='Conflicto ficticio'))
    db.flush()
    assert not case_access_for_current_role(db, actors['admin'], case.id, 'ADMIN_RH')
    assert case_access_for_current_role(db, actors['admin2'], case.id, 'ADMIN_RH')


def test_recipients_recheck_active_role_and_conflict_after_warmup(world):
    client, db, actors, *_ = world
    case = db.get(Incident, UUID(create(client)))
    assert creation_recipient_ids(db, case) == {actors['admin'].id, actors['admin2'].id}
    actors['admin'].is_active = False
    db.flush()
    assert creation_recipient_ids(db, case) == {actors['admin2'].id}
    actors['admin'].is_active = True
    actors['admin2'].rol_id = 2
    db.flush()
    assert creation_recipient_ids(db, case) == {actors['admin'].id}
    db.add(IncidentParticipant(incidencia_id=case.id, user_id=actors['admin'].id,
                               declaration_reason='Conflicto ficticio'))
    db.flush()
    assert creation_recipient_ids(db, case) == set()


def test_templates_have_no_bound_user_department_or_case_identity():
    for role in ('ADMIN_RH', 'SUPERVISOR', 'EMPLEADO'):
        statement = _case_access_statement(role)
        params = statement.compile(dialect=postgresql.dialect()).params
        assert params['access_actor_id'] is None
        assert params['access_case_id'] is None
        if role != 'ADMIN_RH':
            assert params['access_department_id'] is None
    params = _creation_recipients_statement().compile(dialect=postgresql.dialect()).params
    assert params['recipient_case_id'] is None
