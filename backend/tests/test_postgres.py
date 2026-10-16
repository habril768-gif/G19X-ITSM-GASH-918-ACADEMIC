"""IntegraciÃ³n optativa: usar solo una base de pruebas previamente migrada."""
import os
import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from app.core.database import get_engine

pytestmark = pytest.mark.skipif(os.environ.get("RUN_DB_TESTS") != "1", reason="Requiere PostgreSQL de pruebas migrado")


def test_migrated_database_and_catalogs():
    engine = get_engine()
    assert {"users", "incidencias", "historial_incidencias", "departamentos"} <= set(inspect(engine).get_table_names())
    with engine.connect() as c:
        assert c.execute(text("SELECT version_num FROM alembic_version")).scalar_one() == "0002"
        assert c.execute(text("SELECT count(*) FROM roles")).scalar_one() == 3
        assert c.execute(text("SELECT count(*) FROM categorias_incidencia")).scalar_one() == 5


def test_entra_identity_is_unique():
    # TransacciÃ³n revertida siempre; identificadores ficticios, sin datos personales.
    engine = get_engine()
    with engine.connect() as c:
        tx = c.begin()
        try:
            c.execute(text("INSERT INTO departamentos (id,nombre) VALUES ('11111111-1111-1111-1111-111111111111','QA temporal')"))
            sql = text("INSERT INTO users (id,email,external_id,tenant_id,nombre_completo,departamento_id,rol_id) VALUES (:id,'qa@example.invalid','22222222-2222-2222-2222-222222222222','33333333-3333-3333-3333-333333333333','QA','11111111-1111-1111-1111-111111111111',3)")
            c.execute(sql, {"id": "44444444-4444-4444-4444-444444444444"})
            with pytest.raises(IntegrityError):
                c.execute(sql, {"id": "55555555-5555-5555-5555-555555555555"})
        finally:
            tx.rollback()
