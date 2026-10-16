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
        assert c.execute(text("SELECT version_num FROM alembic_version")).scalar_one() == "0003"
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


def test_migration_0003_preserves_legacy_cases_in_isolated_schema():
    """DDL en esquema transaccional temporal, sin modificar tablas del proyecto."""
    import importlib.util
    from pathlib import Path
    from uuid import uuid4
    from alembic.migration import MigrationContext
    from alembic.operations import Operations
    schema="qa_"+uuid4().hex
    with get_engine().connect() as c:
        tx=c.begin()
        try:
            c.execute(text('CREATE SCHEMA "'+schema+'"'))
            c.execute(text('SET LOCAL search_path TO "'+schema+'"'))
            def apply(name):
                path=Path(__file__).resolve().parents[1]/"migrations"/"versions"/name
                spec=importlib.util.spec_from_file_location("migration_qa",path)
                module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                with Operations.context(MigrationContext.configure(c)):
                    module.upgrade()
            apply("0001_initial.py");apply("0002_local_auth.py")
            dep,user,first,second=[str(uuid4()) for _ in range(4)]
            c.execute(text("INSERT INTO departamentos (id,nombre) VALUES (:id,'QA aislado')"),{"id":dep})
            c.execute(text("INSERT INTO users (id,email,nombre_completo,departamento_id,rol_id) VALUES (:id,'legacy@example.invalid','QA',:dep,3)"),{"id":user,"dep":dep})
            c.execute(text("INSERT INTO incidencias (id,titulo,descripcion,incident_date,created_by,affected_employee_id,department_id_at_creation) VALUES (:id,'Pendiente original','Texto original',CURRENT_DATE,:u,:u,:d)"),{"id":first,"u":user,"d":dep})
            c.execute(text("INSERT INTO incidencias (id,titulo,descripcion,incident_date,created_by,affected_employee_id,department_id_at_creation,status,assigned_to,category_id,priority,cycle_start_at,validated_by,validated_at,resolution_text,resolved_at) VALUES (:id,'Resuelta original','Texto anterior',CURRENT_DATE,:u,:u,:d,'RESUELTA',:u,4,2,now(),:u,now(),'Resolución anterior',now())"),{"id":second,"u":user,"d":dep})
            apply("0003_incident_scope.py")
            rows=c.execute(text("SELECT id,scope,reported_department_id,classification_valid,descripcion FROM incidencias")).mappings().all()
            assert len(rows)==2
            by_id={str(row['id']):row for row in rows}
            assert by_id[first]['descripcion']=="Texto original"
            assert by_id[first]['classification_valid'] is False
            assert by_id[second]['classification_valid'] is True
            assert all(row['scope']=="PERSONA" and str(row['reported_department_id'])==dep for row in rows)
            env=str(uuid4())
            c.execute(text("INSERT INTO incidencias (id,titulo,descripcion,incident_date,created_by,affected_employee_id,department_id_at_creation,scope,reported_department_id,category_id) VALUES (:id,'Entorno','Riesgo simulado',CURRENT_DATE,:u,NULL,:d,'ENTORNO',:d,4)"),{"id":env,"u":user,"d":dep})
            assert c.execute(text("SELECT affected_employee_id FROM incidencias WHERE id=:id"),{"id":env}).scalar_one() is None
        finally:
            tx.rollback()
