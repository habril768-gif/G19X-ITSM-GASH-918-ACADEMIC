"""Control SELECT1 de solo lectura dentro de QA nuevo; sin consultas arbitrarias."""
from concurrent.futures import ThreadPoolExecutor
import json
import math
import os
import re
import sys
import threading
import time

EXPLAIN = 'EXPLAIN (ANALYZE, TIMING OFF, FORMAT JSON) SELECT 1'
METRICS = ('driver_ms', 'worker_cpu_ms', 'plan_ms', 'execution_ms')


def guard(payload, env):
    if not isinstance(payload, dict):
        raise ValueError('SONDEO_DB_FUERA_QA')
    run_id = payload.get('run_id')
    if not (set(payload) == {'run_id'} and isinstance(run_id, str)
            and re.fullmatch(r'[a-z0-9]{8,24}', run_id)
            and env.get('QA_PERF_DIAGNOSTIC_RUN_ID') == run_id
            and env.get('QA_PERF_DB_PROBE') == 'true'
            and env.get('POSTGRES_DB') == 'plurione_test_perf_' + run_id
            and env.get('POSTGRES_USER') == 'qa_perf_' + run_id
            and env.get('POSTGRES_HOST') == 'postgres'
            and env.get('AI_ENABLED') == env.get('MAIL_ENABLED') == 'false'):
        raise ValueError('SONDEO_DB_FUERA_QA')
    return run_id


def number(value):
    if not isinstance(value, (float, int)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
        raise ValueError('SONDEO_DB_MEDICION_INVALIDA')
    return value


def measure(connection):
    start = time.perf_counter()
    cpu_start = time.thread_time()
    plan = connection.exec_driver_sql(EXPLAIN).scalar_one()
    cpu = time.thread_time() - cpu_start
    elapsed = time.perf_counter() - start
    if not isinstance(plan, list) or len(plan) != 1 or not isinstance(plan[0], dict):
        raise ValueError('SONDEO_DB_PLAN_INVALIDO')
    return dict(driver_ms=number(elapsed * 1000), worker_cpu_ms=number(cpu * 1000),
                plan_ms=number(plan[0].get('Planning Time')), execution_ms=number(plan[0].get('Execution Time')))


def phase(engine, clients):
    barrier = threading.Barrier(clients)
    def work():
        with engine.connect() as connection:
            # Solo esta transaccion de control, nunca conexiones de la API.
            connection.exec_driver_sql('SET LOCAL statement_timeout = 3000')
            barrier.wait(timeout=15)
            return [measure(connection) for _ in range(5)]
    with ThreadPoolExecutor(max_workers=clients) as workers:
        futures = [workers.submit(work) for _ in range(clients)]
        rows = [row for future in futures for row in future.result()]
    metrics = {}
    for key in METRICS:
        values = sorted(number(row[key]) for row in rows)
        metrics[key] = {'media': sum(values)/len(values), 'p95': values[math.ceil(.95*len(values))-1],
                        'min': values[0], 'max': values[-1]}
    return {'clientes': clients, 'muestras': len(rows), 'metricas': metrics}


def validate(value):
    if not isinstance(value, dict) or set(value) != {'version', 'estado', 'grupos', 'limites'} or value['version'] != 1 or value['estado'] != 'OK':
        raise ValueError('SONDEO_DB_RESULTADO_INVALIDO')
    if set(value['grupos']) != {'solo', 'concurrente'}:
        raise ValueError('SONDEO_DB_RESULTADO_INVALIDO')
    for name, clients in (('solo', 1), ('concurrente', 10)):
        group = value['grupos'][name]
        if set(group) != {'clientes', 'muestras', 'metricas'} or group['clientes'] != clients or group['muestras'] != clients*5 or set(group['metricas']) != set(METRICS):
            raise ValueError('SONDEO_DB_RESULTADO_INVALIDO')
        for stats in group['metricas'].values():
            if set(stats) != {'media','p95','min','max'}:
                raise ValueError('SONDEO_DB_RESULTADO_INVALIDO')
            for item in stats.values(): number(item)
            if not (stats['min'] - 1e-9 <= stats['media'] <= stats['max'] + 1e-9 and stats['min'] - 1e-9 <= stats['p95'] <= stats['max'] + 1e-9):
                raise ValueError('SONDEO_DB_RESULTADO_INVALIDO')
    return value


def run(engine):
    value = {'version': 1, 'estado': 'OK', 'grupos': {'solo': phase(engine, 1), 'concurrente': phase(engine, 10)},
        'limites': 'Control SELECT1 despues de carga HTTP, 5 muestras con1conexion y50con10conexiones; no reproduce consultas de negocio ni acredita RNF-2. driver incluye espera, transporte y JSON; plan/exec no incluyen todo el trabajo del servidor. No restar p95. Checkout,conexion,ping ySET LOCAL fuera del intervalo de cada muestra.'}
    return validate(value)


def main():
    payload = json.load(sys.stdin)
    run_id = guard(payload, os.environ)
    from app.core.database import get_engine
    engine = get_engine()
    try:
        with engine.connect() as connection:
            identity = tuple(connection.exec_driver_sql('SELECT current_database(), current_user').one())
        if identity != ('plurione_test_perf_' + run_id, 'qa_perf_' + run_id):
            raise ValueError('SONDEO_DB_IDENTIDAD_INVALIDA')
        result = run(engine)
    finally:
        engine.dispose()
    print(json.dumps(result, separators=(',', ':')), flush=True)


if __name__ == '__main__':
    main()
