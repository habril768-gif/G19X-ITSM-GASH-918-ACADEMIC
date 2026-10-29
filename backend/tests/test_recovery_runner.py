"""La comparación de recuperación no debe ocultar cambios de significado."""
import importlib.util
from pathlib import Path
import sys

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('recovery_runner',SCRIPTS/'test_recovery_isolated.py')
runner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def test_round_trip_of_varchar_literal_array_cast():
    source="CHECK (status = ANY ((ARRAY['PENDIENTE'::character varying, 'CERRADA'::character varying])::text[]))"
    restored="CHECK (status = ANY (ARRAY[('PENDIENTE'::character varying)::text, ('CERRADA'::character varying)::text]))"
    assert runner.canonical_sql(source)==runner.canonical_sql(restored)


def test_values_and_escaped_quotes_inside_literals_stay_exact():
    source="(ARRAY['valor ::character varying con  espacios'::character varying, 'texto ''citado'''::character varying])::text[]"
    normalized=runner.canonical_sql(source)
    assert normalized=="ARRAY['valor ::character varying con  espacios'::text, 'texto ''citado'''::text]"
    assert runner.canonical_sql(source.replace('espacios','cambio'))!=normalized


def test_pretty_view_deparse_and_normalization_idempotence():
    source="status::text = ANY (ARRAY['PENDIENTE'::character varying, 'CERRADA'::character varying]::text[])"
    restored="status::text = ANY (ARRAY['PENDIENTE'::character varying::text, 'CERRADA'::character varying::text])"
    result=runner.canonical_sql(source)
    assert result==runner.canonical_sql(restored)
    assert runner.canonical_sql(result)==result


def test_no_normalization_of_bounded_varchar_numeric_or_column_casts():
    for statement in ("(ARRAY['long'::character varying(2)])::text[]",
                      "(ARRAY[12::integer])::text[]", "(ARRAY[status::character varying])::text[]"):
        assert runner.canonical_sql(statement)==statement


def test_security_options_and_unrelated_definitions_are_not_erased():
    source='CREATE VIEW metrics WITH (security_barrier=true) AS SELECT 1'
    assert runner.canonical_sql(source)!=runner.canonical_sql(source.replace('true','false'))
    assert runner.canonical_sql('CHECK (attempts <= 3)')!=runner.canonical_sql('CHECK (attempts <= 4)')
