"""Relectura fresca tras bloqueo, sin cachear autorización administrativa."""
from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, delete, event, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import TextClause
from app.models import Base, Department, Role, User
from app.services.administration_lock import administration_lock


@pytest.fixture
def administrative_world():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as db:
        db.add_all([Role(id=1, nombre="ADMIN_RH"), Role(id=3, nombre="EMPLEADO")])
        one = Department(nombre="Uno QA", is_active=True)
        two = Department(nombre="Dos QA", is_active=True)
        db.add_all([one, two]); db.flush()
        actor = User(email="qa@example.invalid", nombre_completo="Ficticio", rol_id=1,
                     departamento_id=one.id, is_active=True)
        db.add(actor); db.commit()
        yield db, actor, one, two
    engine.dispose()


@pytest.mark.parametrize("scenario,denied", [
    ("active", False), ("expired", False), ("inactive_user", True),
    ("inactive_department", True), ("moved_active", False), ("moved_inactive", True),
    ("changed_role", False), ("deleted_user", True), ("missing_department", True),
])
def test_one_fresh_read_updates_preloaded_state(administrative_world, scenario, denied):
    db, actor, one, two = administrative_world
    uid, original_department = actor.id, one.id
    # UPDATE/DELETE sin sincronizar el identity map simula valores precargados
    # obsoletos; no demuestra concurrencia ni aislamiento PostgreSQL.
    if scenario == "inactive_user":
        db.execute(update(User).where(User.id == uid).values(is_active=False), execution_options={"synchronize_session": False})
    elif scenario == "inactive_department":
        db.execute(update(Department).where(Department.id == one.id).values(is_active=False), execution_options={"synchronize_session": False})
    elif scenario in {"moved_active", "moved_inactive"}:
        if scenario == "moved_inactive":
            db.execute(update(Department).where(Department.id == two.id).values(is_active=False), execution_options={"synchronize_session": False})
        db.execute(update(User).where(User.id == uid).values(departamento_id=two.id), execution_options={"synchronize_session": False})
    elif scenario == "changed_role":
        db.execute(update(User).where(User.id == uid).values(rol_id=3), execution_options={"synchronize_session": False})
    elif scenario == "deleted_user":
        db.execute(delete(User).where(User.id == uid), execution_options={"synchronize_session": False})
    elif scenario == "missing_department":
        # SQLite sin FK para simular la fila ausente: debe denegar, nunca autorizar.
        db.execute(delete(Department).where(Department.id == one.id), execution_options={"synchronize_session": False})
    db.commit()
    assert actor.is_active and actor.departamento_id == original_department and actor.rol_id == 1
    if scenario == "expired":
        db.expire(actor)
    statements = []
    def observe(conn, cursor, statement, parameters, context, executemany):
        statements.append(statement)
    event.listen(db.bind, "before_cursor_execute", observe)
    try:
        if denied:
            with pytest.raises(HTTPException) as exc:
                administration_lock(db, actor)
            assert exc.value.status_code == 403 and exc.value.detail == "Cuenta no habilitada"
        else:
            assert administration_lock(db, actor) is None
    finally:
        event.remove(db.bind, "before_cursor_execute", observe)
    assert len(statements) == 1
    if scenario == "changed_role":
        assert actor.rol_id == 3
    if scenario in {"moved_active", "moved_inactive"}:
        assert actor.departamento_id == two.id
    if scenario == "inactive_department":
        assert one.is_active is False
    if scenario == "moved_inactive":
        assert two.is_active is False


@pytest.mark.parametrize("exclusive,function", [(False, "pg_advisory_xact_lock_shared"), (True, "pg_advisory_xact_lock")])
def test_advisory_lock_is_requested_before_refresh(administrative_world, exclusive, function):
    db, actor, one, two = administrative_world
    calls = []
    original_bind, original_execute = db.bind, db.execute
    fake_bind = SimpleNamespace(dialect=SimpleNamespace(name="postgresql"))
    def execute(statement):
        db.bind = original_bind
        try:
            if isinstance(statement, TextClause):
                calls.append(str(statement))
                # Cambio visible solo después de la adquisición simulada.
                original_execute(update(User).where(User.id == actor.id).values(rol_id=3), execution_options={"synchronize_session": False})
                return None
            calls.append("REFRESH")
            return original_execute(statement)
        finally:
            db.bind = fake_bind
    db.bind, db.execute = fake_bind, execute
    try:
        assert administration_lock(db, actor, exclusive) is None
    finally:
        db.bind, db.execute = original_bind, original_execute
    assert calls == [f"SELECT {function}(71419322)", "REFRESH"]
    assert actor.rol_id == 3


def test_without_actor_does_not_query_identity(administrative_world):
    db, actor, one, two = administrative_world
    statements = []
    def observe(conn, cursor, statement, parameters, context, executemany): statements.append(statement)
    event.listen(db.bind, "before_cursor_execute", observe)
    try:
        assert administration_lock(db) is None
    finally:
        event.remove(db.bind, "before_cursor_execute", observe)
    assert statements == []


@pytest.mark.parametrize("kind", ["transient", "detached"])
def test_actor_must_belong_to_current_session(administrative_world, kind):
    db, actor, one, two = administrative_world
    if kind == "transient":
        actor = User(email="transient@example.invalid", nombre_completo="Ficticio", rol_id=1,
                     departamento_id=one.id, is_active=True)
    else:
        db.expunge(actor)
    with pytest.raises(HTTPException) as exc:
        administration_lock(db, actor)
    assert exc.value.status_code == 403
