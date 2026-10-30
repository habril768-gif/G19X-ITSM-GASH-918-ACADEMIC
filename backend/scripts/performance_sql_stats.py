"""Estadísticas agregadas de ejecución SQL solo en PostgreSQL QA nuevo."""
import json
import math
import os
import re
import sys

PG_COMMAND = ['postgres', '-c', 'shared_preload_libraries=pg_stat_statements',
    '-c', 'compute_query_id=on', '-c', 'pg_stat_statements.track=top',
    '-c', 'pg_stat_statements.track_planning=off']
TABLES = {'users', 'departamentos', 'roles', 'auth_sessions', 'incidencias',
    'incident_involved_users', 'historial_incidencias', 'mail_deliveries',
    'local_credentials', 'login_throttles', 'ai_jobs', 'categorias_incidencia'}
LIMITS = ('Solo QA nuevo e instrumentado. Ventana desde antes del login hasta despues de '
    'verificacion SQL: incluye login/logout, calentamiento, carga y lecturas finales; excluye seed '
    'y control SELECT1 posterior. Medias agregadas de ejecucion servidor, sin p95 ni planificacion '
    '(track_planning=off), red o tiempo total HTTP. La extension agrega coste; no acredita RNF-2. '
    'Sin SQL, parametros o IDs de consulta en el reporte. Sin reset de estadisticas.')


def guard(payload, env):
    if not isinstance(payload, dict) or set(payload) != {'action', 'run_id'}:
        raise ValueError('SQL_STATS_FUERA_QA')
    run_id = payload.get('run_id')
    if not (payload.get('action') in {'before', 'after'} and isinstance(run_id, str)
            and re.fullmatch('[a-z0-9]{8,24}', run_id)
            and env.get('QA_PERF_DIAGNOSTIC_RUN_ID') == run_id
            and env.get('QA_PERF_SQL_STATS') == 'true'
            and env.get('POSTGRES_HOST') == 'postgres'
            and env.get('POSTGRES_DB') == 'plurione_test_perf_' + run_id
            and env.get('POSTGRES_USER') == 'qa_perf_' + run_id
            and env.get('AI_ENABLED') == env.get('MAIL_ENABLED') == 'false'):
        raise ValueError('SQL_STATS_FUERA_QA')
    return run_id


def number(value, integer=False):
    if (not isinstance(value, (int, float)) or isinstance(value, bool)
            or not math.isfinite(value) or value < 0 or (integer and int(value) != value)):
        raise ValueError('SQL_STATS_NUMERO_INVALIDO')
    return value


def family(query):
    if not isinstance(query, str) or not query.strip() or query == '<insufficient privilege>':
        raise ValueError('SQL_STATS_TEXTO_NO_DISPONIBLE')
    # Solo clasificar estructura; nunca guardar ni devolver el texto recibido.
    source = re.sub(r"'(?:''|[^'])*'", "''", query)
    source = re.sub(r'/\*.*?\*/|--[^\n]*', '', source, flags=re.S)
    if re.search(r'\bpg_stat_statements(?:_info)?\b|\bcurrent_database\s*\(', source, re.I):
        return None  # Consultas fijas del propio control.
    op = re.match(r'\s*(SELECT|INSERT|UPDATE|DELETE|BEGIN|COMMIT|ROLLBACK)\b', source, re.I)
    op = op.group(1).upper() if op else 'OTHER'
    if re.search(r'\bpg_advisory_xact_lock(?:_shared)?\s*\(', source, re.I):
        return 'SELECT/advisory_lock'
    tables = {name.lower() for name in re.findall(r'\b(?:FROM|JOIN|INTO|UPDATE)\s+(?:public\.)?"?([a-z_]+)"?', source, re.I)} & TABLES
    return op + '/' + ('+'.join(sorted(tables)) if tables else 'other')


def valid_family(value):
    if not isinstance(value, str) or '/' not in value:
        return False
    op, tables = value.split('/', 1)
    if op not in {'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'BEGIN', 'COMMIT', 'ROLLBACK', 'OTHER'}:
        return False
    if tables == 'advisory_lock':
        return op == 'SELECT'
    if tables == 'other':
        return True
    names = tables.split('+')
    return names == sorted(set(names)) and set(names) <= TABLES


def snapshot(connection, run_id):
    info = connection.exec_driver_sql('SELECT dealloc, stats_reset FROM pg_stat_statements_info').one()
    rows = connection.exec_driver_sql('''SELECT queryid, query, calls, total_exec_time, rows, stats_since
        FROM pg_stat_statements
        WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
          AND userid = (SELECT oid FROM pg_roles WHERE rolname = current_user)
          AND toplevel''').all()
    values = []
    for key, query, calls, elapsed, count, since in rows:
        name = family(query)
        if name is not None:
            values.append(dict(key=str(key), family=name, calls=number(calls, True),
                               exec_ms=number(elapsed), rows=number(count, True), since=since.isoformat()))
    value = dict(version=1, run_id=run_id, dealloc=number(info[0], True),
                 reset=info[1].isoformat(), rows=values)
    return validate_snapshot(value, run_id)


def validate_snapshot(value, run_id):
    if (not isinstance(value, dict) or set(value) != {'version', 'run_id', 'dealloc', 'reset', 'rows'}
            or value['version'] != 1 or value['run_id'] != run_id
            or not isinstance(value['reset'], str) or not value['reset']
            or len(value['reset']) > 50 or not isinstance(value['rows'], list) or len(value['rows']) > 5000):
        raise ValueError('SQL_STATS_SNAPSHOT_INVALIDO')
    number(value['dealloc'], True)
    seen = set()
    for row in value['rows']:
        if (not isinstance(row, dict) or set(row) != {'key', 'family', 'calls', 'exec_ms', 'rows', 'since'}
                or not isinstance(row['key'], str) or not re.fullmatch('-?[0-9]{1,20}', row['key'])
                or row['key'] in seen or not valid_family(row['family'])
                or not isinstance(row['since'], str) or not row['since'] or len(row['since']) > 50):
            raise ValueError('SQL_STATS_FILA_INVALIDA')
        seen.add(row['key'])
        number(row['calls'], True); number(row['rows'], True); number(row['exec_ms'])
    return value


def difference(before, after, run_id):
    validate_snapshot(before, run_id); validate_snapshot(after, run_id)
    if before['reset'] != after['reset'] or before['dealloc'] != after['dealloc']:
        raise ValueError('SQL_STATS_RESET_O_DESALOJO')
    old = {row['key']: row for row in before['rows']}
    new = {row['key']: row for row in after['rows']}
    if set(old) - set(new):
        raise ValueError('SQL_STATS_RESET_O_DESALOJO')
    groups = {}
    for key, row in new.items():
        previous = old.get(key, dict(family=row['family'], calls=0, exec_ms=0, rows=0, since=row['since']))
        if row['since'] != previous['since']:
            raise ValueError('SQL_STATS_RESET_O_DESALOJO')
        if row['family'] != previous['family']:
            raise ValueError('SQL_STATS_FAMILIA_CAMBIADA')
        delta = {f: row[f] - previous[f] for f in ('calls', 'exec_ms', 'rows')}
        if any(v < -1e-8 for v in delta.values()) or (delta['calls'] == 0 and abs(delta['exec_ms']) > 1e-8):
            raise ValueError('SQL_STATS_CONTADOR_DISMINUIDO')
        if not delta['calls']:
            continue
        target = groups.setdefault(row['family'], dict(calls=0, exec_ms=0.0, rows=0))
        for field, v in delta.items(): target[field] += max(0, v)
    if not groups:
        raise ValueError('SQL_STATS_SIN_LLAMADAS')
    for values in groups.values(): values['exec_ms_per_call'] = values['exec_ms'] / values['calls']
    totals = {field: sum(g[field] for g in groups.values()) for field in ('calls', 'exec_ms', 'rows')}
    return dict(version=1, estado='OK', familias=groups, totales=totals, limites=LIMITS)


def main():
    payload = json.load(sys.stdin)
    run_id = guard(payload, os.environ)  # Antes de importar/configurar motor o conectar.
    from app.core.database import get_engine
    engine = get_engine()
    try:
        with engine.begin() as connection:
            identity = tuple(connection.exec_driver_sql('SELECT current_database(), current_user').one())
            if identity != ('plurione_test_perf_' + run_id, 'qa_perf_' + run_id):
                raise ValueError('SQL_STATS_IDENTIDAD_INVALIDA')
            settings = tuple(connection.exec_driver_sql('''SELECT current_setting('shared_preload_libraries'),
                current_setting('pg_stat_statements.track'), current_setting('pg_stat_statements.track_planning')''').one())
            if settings != ('pg_stat_statements', 'top', 'off'):
                raise ValueError('SQL_STATS_CONFIG_INVALIDA')
            if payload['action'] == 'before':
                connection.exec_driver_sql('CREATE EXTENSION IF NOT EXISTS pg_stat_statements')
            value = snapshot(connection, run_id)
    finally:
        engine.dispose()
    print(json.dumps(value, separators=(',', ':')), flush=True)


if __name__ == '__main__':
    main()
