"""ConfiguraciÃ³n sin secretos y disponibilidad degradada."""
from fastapi.testclient import TestClient
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.core.database import database_ready, database_url
from app.main import create_app
from app.models import Base


def test_password_with_reserved_characters(monkeypatch):
    monkeypatch.setenv("POSTGRES_PASSWORD", "test@:/%#fake")
    monkeypatch.setenv("POSTGRES_HOST", "postgres")
    url = database_url()
    assert url.password == "test@:/%#fake"
    assert url.host == "postgres"
    assert "test@:/%#fake" not in str(url)


def test_db_readiness_failure_does_not_leak_credentials():
    app = create_app()
    app.dependency_overrides[database_ready] = lambda: False
    with TestClient(app) as client:
        response = client.get("/health/db")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable", "database": "postgresql"}
        assert client.get("/health").status_code == 200


def test_db_readiness_success():
    app = create_app()
    app.dependency_overrides[database_ready] = lambda: True
    with TestClient(app) as client:
        assert client.get("/health/db").json() == {"status": "ok", "database": "postgresql"}


def test_postgresql_schema_compiles():
    ddl = "\n".join(str(CreateTable(t).compile(dialect=postgresql.dialect())) for t in Base.metadata.sorted_tables)
    assert "JSONB" in ddl
    assert "TIMESTAMP WITH TIME ZONE" in ddl
    assert "uq_users_entra" in ddl
    assert "ck_incident_resolution" in ddl


def test_initial_migration_compiles_offline():
    from io import StringIO
    from pathlib import Path
    from alembic import command
    from alembic.config import Config
    buffer = StringIO()
    cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"), output_buffer=buffer)
    command.upgrade(cfg, "head", sql=True)
    sql = buffer.getvalue()
    assert "CREATE TABLE incidencias" in sql
    assert "INSERT INTO roles" in sql
    assert "INSERT INTO categorias_incidencia" in sql
    assert "COMMIT" in sql
    assert "CREATE TABLE department_audit_events" in sql
    assert "ix_department_audit_events_department_id" in sql
