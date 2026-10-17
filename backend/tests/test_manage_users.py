"""CLI del operador sobre SQLite aislado; nunca conecta al proyecto real."""
import sys
import warnings
from getpass import GetPassWarning

import pytest
from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import manage_users
from app.core.security import password_hasher
from app.models import AuditEvent, Base, Department, LocalCredential, Role, User
from app.models import Incident, IncidentParticipant
from app.services.incidents import visibility
from datetime import date

PASSWORD = "OnlyForCliTests-LongPassword42"


@pytest.fixture
def operator(monkeypatch):
    engine = create_engine("sqlite://")
    @event.listens_for(engine, "connect")
    def fk(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    with Session(engine) as db, db.begin():
        db.add(Role(id=1, nombre="ADMIN_RH"))
    monkeypatch.setattr(manage_users, "get_engine", lambda: engine)
    monkeypatch.setattr(manage_users, "getpass", lambda _: PASSWORD)
    def run(action, email="independent@example.invalid", **options):
        args = ["manage_users", action, "--email", email]
        for key, value in options.items():
            args += ["--" + key, value]
        monkeypatch.setattr(sys, "argv", args)
        return manage_users.main()
    yield engine, run
    engine.dispose()


def bootstrap(run):
    assert run("bootstrap-admin", email="initial@example.invalid") == 0


def test_additional_admin_is_new_hashed_and_audited(operator, capsys):
    engine, run = operator
    bootstrap(run)
    assert run("provision-independent-admin", reason="Gestor independiente de prueba") == 0
    with Session(engine) as db:
        people = db.scalars(select(User)).all()
        assert len(people) == 2
        person = next(p for p in people if p.email == "independent@example.invalid")
        assert person.rol_id == 1 and person.is_active
        credential = db.get(LocalCredential, person.id)
        assert password_hasher.verify(PASSWORD, credential.password_hash)
        audit = db.scalar(select(AuditEvent).where(AuditEvent.affected_user_id == person.id))
        assert audit.usuario_id is None and audit.incidencia_id is None
        assert audit.detalle["motivo"] == "Gestor independiente de prueba"
        assert audit.detalle["operacion"] == "provision-independent-admin"
        assert PASSWORD not in str(audit.detalle)
    assert PASSWORD not in capsys.readouterr().out


def test_reason_required_and_bootstrap_cannot_be_repeated(operator):
    engine, run = operator
    bootstrap(run)
    assert run("provision-independent-admin") == 1
    assert run("provision-independent-admin", reason=" ") == 1
    assert run("bootstrap-admin") == 1
    with Session(engine) as db:
        assert len(db.scalars(select(User)).all()) == 1


def test_cannot_repurpose_existing_account_or_inactive_department(operator):
    engine, run = operator
    bootstrap(run)
    assert run("provision-independent-admin", email=" INITIAL@example.invalid ", reason="Prueba") == 1
    with Session(engine) as db, db.begin():
        db.scalar(select(Department)).is_active = False
    assert run("provision-independent-admin", reason="Prueba") == 1
    with Session(engine) as db:
        assert len(db.scalars(select(User)).all()) == 1
        assert len(db.scalars(select(AuditEvent)).all()) == 1


def test_additional_requires_initial_admin(operator):
    engine, run = operator
    assert run("provision-independent-admin", reason="Prueba") == 1
    with Session(engine) as db:
        assert db.scalars(select(User)).all() == []
        assert db.scalars(select(Department)).all() == []


def test_audit_failure_rolls_back_new_user_credential_and_department(operator):
    engine, run = operator
    bootstrap(run)
    def fail(session, context, instances):
        if any(isinstance(row, AuditEvent) and row.detalle.get("operacion") == "provision-independent-admin" for row in session.new):
            raise SQLAlchemyError("simulated audit failure")
    event.listen(Session, "before_flush", fail)
    try:
        assert run("provision-independent-admin", reason="Prueba", department="Otro departamento") == 1
    finally:
        event.remove(Session, "before_flush", fail)
    with Session(engine) as db:
        assert len(db.scalars(select(User)).all()) == 1
        assert len(db.scalars(select(LocalCredential)).all()) == 1
        assert len(db.scalars(select(Department)).all()) == 1
        assert len(db.scalars(select(AuditEvent)).all()) == 1


def test_password_mismatch_and_unsafe_terminal_make_no_changes(operator, monkeypatch):
    engine, run = operator
    answers = iter([PASSWORD, "AnotherPassword42"])
    monkeypatch.setattr(manage_users, "getpass", lambda _: next(answers))
    assert run("bootstrap-admin") == 1
    def unsafe(_):
        warnings.warn("Cannot control echo", GetPassWarning)
        raise AssertionError("No debe ejecutarse fallback con eco")
    monkeypatch.setattr(manage_users, "getpass", unsafe)
    assert run("bootstrap-admin") == 1
    with Session(engine) as db:
        assert db.scalars(select(User)).all() == []


def test_provisioning_preserves_exclusion_and_does_not_assign_case(operator):
    engine, run = operator
    bootstrap(run)
    with Session(engine) as db, db.begin():
        original = db.scalar(select(User))
        case = Incident(titulo="Caso simulado", descripcion="Prueba de independencia",
                        incident_date=date(2026, 10, 16), scope="ENTORNO",
                        created_by=original.id, affected_employee_id=None,
                        reported_department_id=original.departamento_id,
                        department_id_at_creation=original.departamento_id,
                        is_confidential=True, ai_status="OMITIDA", ai_skip_reason="Prueba")
        db.add(case)
        db.flush()
        case_id, original_id = case.id, original.id
        db.add(IncidentParticipant(incidencia_id=case.id, user_id=original.id,
                                  declaration_reason="Administrador involucrado simulado"))
    assert run("provision-independent-admin", reason="Atención independiente simulada") == 0
    with Session(engine) as db:
        original = db.get(User, original_id)
        independent = db.scalar(select(User).where(User.email == "independent@example.invalid"))
        assert db.scalar(select(Incident.id).where(Incident.id == case_id, visibility(db, original))) is None
        assert db.scalar(select(Incident.id).where(Incident.id == case_id, visibility(db, independent))) == case_id
        case = db.get(Incident, case_id)
        assert case.status == "PENDIENTE" and case.assigned_to is None and case.is_confidential
        assert db.get(IncidentParticipant, (case_id, original_id)).review_status == "DECLARADO"
