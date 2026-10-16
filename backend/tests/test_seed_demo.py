"""Verifica fixtures y transacción en SQLite; integración PostgreSQL por separado."""
import pytest
from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import Session
from app.models import Department, Role, User
from app.seed_demo import seed_demo


@pytest.fixture
def engine():
    engine = create_engine("sqlite://")
    @event.listens_for(engine, "connect")
    def foreign_keys(dbapi_connection, _):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
    Role.__table__.create(engine)
    Department.__table__.create(engine)
    User.__table__.create(engine)
    yield engine
    engine.dispose()


def add_roles(session):
    session.add_all([Role(id=1,nombre="ADMIN_RH"),Role(id=2,nombre="SUPERVISOR"),Role(id=3,nombre="EMPLEADO")])
    session.flush()


def test_seed_is_repeatable_and_preserves_changes(engine):
    with Session(engine) as s, s.begin():
        add_roles(s)
        assert seed_demo(s) == {"departamentos_creados": 2, "usuarios_creados": 6}
        user = s.scalars(select(User).where(User.rol_id == 3)).first()
        user.is_active = False
        s.flush()
        assert seed_demo(s) == {"departamentos_creados": 0, "usuarios_creados": 0}
        assert user.is_active is False
        assert s.scalar(select(func.count()).select_from(User)) == 6
        assert s.scalar(select(func.count()).select_from(User).where(User.rol_id == 2)) == 2


def test_missing_roles_does_not_create_users(engine):
    with Session(engine) as s:
        with pytest.raises(ValueError), s.begin():
            seed_demo(s)
        assert s.scalar(select(func.count()).select_from(User)) == 0


def test_seed_can_be_rolled_back_atomically(engine):
    with Session(engine) as s:
        with pytest.raises(RuntimeError), s.begin():
            add_roles(s)
            seed_demo(s)
            raise RuntimeError("Falla simulada")
        assert s.scalar(select(func.count()).select_from(User)) == 0
        assert s.scalar(select(func.count()).select_from(Department)) == 0
