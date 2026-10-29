"""Carga HTTP de QA: requiere manifiesto y fixture ajenos a la instalación de uso."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone
import http.client
import json
import math
import os
from pathlib import Path
import re
import statistics
import threading
import time
from urllib.parse import urlsplit
from uuid import UUID
from performance_host import stamp as host_stamp, summarize as host_summary


OPS = ('listado', 'detalle', 'creacion', 'actualizacion')


class InvalidRun(Exception):
    """Los mensajes son códigos fijos; nunca cuerpos HTTP o secretos."""


def require(condition, code):
    if not condition:
        raise InvalidRun(code)


def percentile(values, fraction):
    if not values:
        return None
    return sorted(values)[math.ceil(fraction * len(values)) - 1]


def metrics(samples, seconds):
    result = {}
    for operation in OPS:
        rows = [s for s in samples if s[0] == operation]
        good = [s[1] for s in rows if s[3]]
        all_times = [s[1] for s in rows]
        result[operation] = {
            'intentos': len(rows), 'exitos': len(good), 'errores': len(rows) - len(good),
            'estados': dict(Counter(str(s[2]) for s in rows)),
            'tasa_error': (len(rows) - len(good)) / len(rows) if rows else None,
            'solicitudes_por_segundo': len(rows) / seconds,
            'min_ms': min(good) if good else None,
            'mediana_ms': statistics.median(good) if good else None,
            'p95_exitos_ms': percentile(good, .95), 'p99_exitos_ms': percentile(good, .99),
            'max_ms': max(good) if good else None,
            'p95_todos_ms': percentile(all_times, .95),
            'finalizadas_fuera_ventana': sum(s[4] for s in rows),
        }
    return result


def verdict(summary, complete, smoke):
    if any(row['errores'] for row in summary.values()):
        return 'FALLIDA'
    if not complete or any(not row['intentos'] for row in summary.values()):
        return 'INCOMPLETA'
    if smoke:
        return 'SMOKE_SIN_ACREDITAR_RNF2'
    return 'APROBADA_ALCANCE_HTTP_QA' if all(
        row['p95_exitos_ms'] < 200 for row in summary.values()) else 'FALLIDA_UMBRAL'


def validate_manifest(manifest):
    require(manifest.get('scope') == 'plurione-performance-isolated', 'MANIFIESTO_SCOPE')
    run_id = manifest.get('run_id', '')
    require(re.fullmatch(r'[a-z0-9]{8,24}', run_id) is not None, 'RUN_ID')
    url = urlsplit(manifest.get('base_url', ''))
    require(url.scheme == 'http' and url.hostname == '127.0.0.1' and
            not url.username and not url.password and not url.query and not url.fragment and
            url.path in ('', '/') and url.port is not None and 1024 <= url.port <= 65535 and
            url.port not in {8000, 5173, 5432, 5433, 6379, 8025}, 'DESTINO_NO_QA')
    require(manifest.get('compose_project') == 'plurione-qa-perf-' + run_id, 'PROYECTO_QA')
    require(manifest.get('isolated_resources_confirmed') is True, 'AISLAMIENTO_NO_CONFIRMADO')
    for key in ('hardware', 'code_identity', 'images', 'provider_queue_mode'):
        require(isinstance(manifest.get(key), dict) and manifest[key], 'METADATOS_FALTANTES')
    UUID(manifest['department_id'])
    users = manifest.get('users', [])
    require(len(users) == 10, 'DIEZ_USUARIOS_REQUERIDOS')
    all_ids = []
    for index, user in enumerate(users):
        require(user['email'] == f'qa-perf-{run_id}-{index}@example.invalid', 'CUENTA_NO_QA')
        require(user['password_env'] == f'PLURIONE_PERF_PASSWORD_{index}', 'ENV_PASSWORD')
        require(len(user['case_ids']) == 10, 'DIEZ_CASOS_POR_USUARIO')
        all_ids.extend(str(UUID(value)) for value in user['case_ids'])
    require(len(set(all_ids)) == 100, 'CASOS_DUPLICADOS')
    return url.port


class Client:
    def __init__(self, port):
        self.port = port
        self.connection = None
        self.token = None
        self.diagnostic = False
        self.phase = None

    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None

    def request(self, method, path, payload=None):
        if self.connection is None:
            self.connection = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        headers = {'Accept': 'application/json'}
        if self.diagnostic and self.phase in ('calentamiento', 'medicion'):
            headers['X-QA-Performance-Phase'] = self.phase
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        body = None if payload is None else json.dumps(payload).encode('utf-8')
        if body is not None:
            headers['Content-Type'] = 'application/json'
        try:
            self.connection.request(method, path, body=body, headers=headers)
            response = self.connection.getresponse()
            raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise InvalidRun('RESPUESTA_EXCESIVA')
            value = json.loads(raw) if raw else None
            return response.status, value
        except Exception:
            self.close()
            raise

    def checked(self, method, path, payload=None, status=200):
        actual, value = self.request(method, path, payload)
        require(actual == status, 'HTTP_PRE_POST_NO_ESPERADO')
        return value


def preflight(manifest, clients):
    require(clients[0].checked('GET', '/health').get('status') == 'ok', 'SALUD_API')
    require(clients[0].checked('GET', '/health/db').get('status') == 'ok', 'SALUD_DB')
    identities = []
    prefix = 'QA-PERF-' + manifest['run_id'] + '-'
    for account, client in zip(manifest['users'], clients):
        password = os.environ.get(account['password_env'])
        require(bool(password), 'PASSWORD_QA_AUSENTE')
        login = client.checked('POST', '/auth/login',
                               {'email': account['email'], 'password': password})
        client.token = login.get('access_token')
        require(isinstance(client.token, str) and bool(client.token), 'TOKEN_AUSENTE')
        actor = client.checked('GET', '/auth/me')
        require(actor['email'] == account['email'] and actor['rol'] == 'ADMIN_RH' and
                actor['departamento_id'] == manifest['department_id'], 'IDENTIDAD_QA_INVALIDA')
        identities.append(actor['id'])
        page = client.checked('GET', '/incidents?page=1&page_size=100')
        require(page['total'] == 100 and len(page['items']) == 100, 'POBLACION_INICIAL')
        require(all(row['titulo'].startswith(prefix) for row in page['items']), 'POBLACION_NO_QA')
        for case_id in account['case_ids']:
            case = client.checked('GET', '/incidents/' + case_id)
            require(case['id'] == case_id and case['created_by'] == actor['id'] and
                    case['reported_department_id'] == manifest['department_id'] and
                    case['scope'] == 'ENTORNO' and case['status'] == 'PENDIENTE' and
                    case['is_confidential'] is False and case['affected_employee_id'] is None and
                    case['titulo'].startswith(prefix), 'FIXTURE_NO_VALIDO')
            relations = client.checked('GET', '/incidents/' + case_id + '/participants')
            require(relations == {'items': []}, 'RELACIONES_EN_FIXTURE')
    require(len(set(identities)) == 10, 'SESIONES_NO_DISTINTAS')


def operation(client, account, manifest, sequence, phase):
    op = OPS[sequence % 4]
    case_id = account['case_ids'][(sequence // 4) % 10]
    title = f"QA-PERF-{manifest['run_id']}-{phase}-{sequence}"
    text = 'Ensayo simulado de rendimiento; sin datos personales. ' + title
    if op == 'listado':
        status, body = client.request('GET', '/incidents?page=1&page_size=20')
        valid = isinstance(body, dict) and isinstance(body.get('items'), list) and len(body['items']) <= 20
        return op, status, status == 200 and valid, None
    if op == 'detalle':
        status, body = client.request('GET', '/incidents/' + case_id)
        return op, status, status == 200 and isinstance(body, dict) and body.get('id') == case_id, None
    if op == 'creacion':
        status, body = client.request('POST', '/incidents', {
            'titulo': title, 'descripcion': text, 'incident_date': manifest['incident_date'],
            'scope': 'ENTORNO', 'reported_department_id': manifest['department_id']})
        valid = (status == 201 and isinstance(body, dict) and body.get('received') is True
                 and body.get('can_view') is True)
        if valid:
            try:
                UUID(body['id'])
            except (ValueError, KeyError, TypeError):
                valid = False
        return op, status, valid, body['id'] if valid else None
    status, body = client.request('PUT', '/incidents/' + case_id + '/content',
                                  {'titulo': title, 'descripcion': text})
    valid = (status == 200 and isinstance(body, dict) and body.get('id') == case_id and
             body.get('titulo') == title and body.get('descripcion') == text)
    return op, status, valid, None


def phase_run(clients, manifest, duration, phase):
    # La preparación secuencial puede superar el keep-alive de clientes anteriores.
    # Conservar tokens, pero iniciar cada fase con sockets nuevos; no repetir peticiones.
    for client in clients:
        client.close()
        client.phase = phase
    stop = threading.Event()
    window = {}
    diagnostic = any(getattr(client, "diagnostic", False) for client in clients)
    def start_window():
        if diagnostic:
            window['cpu_start'] = host_stamp()
        window['start'] = time.perf_counter()
        window['deadline'] = window['start'] + duration
        window['inicio_utc'] = datetime.now(timezone.utc).isoformat()
    gate = threading.Barrier(11, action=start_window)
    def worker(index):
        samples = []
        creates = 0
        last_created = None
        gate.wait(timeout=30)
        first = time.perf_counter()
        sequence = 0
        while not stop.is_set() and time.perf_counter() < window['deadline'] and sequence < 100_000:
            started = time.perf_counter()
            op = OPS[sequence % 4]
            status, valid, created_id = 'EXCEPTION', False, None
            try:
                op, status, valid, created_id = operation(clients[index], manifest['users'][index],
                                                         manifest, sequence, phase)
            except Exception as exc:
                status = 'EXCEPTION:' + type(exc).__name__
                # No guardar mensajes, cuerpos o credenciales ni repetir la petición.
            ended = time.perf_counter()
            samples.append((op, (ended - started) * 1000, status, valid, ended > window['deadline']))
            if created_id:
                creates += 1
                last_created = created_id
            if not valid:
                stop.set()
            sequence += 1
        return {'samples': samples, 'creados': creates, 'ultimo_creado': last_created,
                'inicio_offset_ms': (first - window['start']) * 1000,
                'fin_offset_s': time.perf_counter() - window['start'],
                'limite_solicitudes': sequence == 100_000}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, index) for index in range(10)]
        gate.wait(timeout=30)
        try:
            rows = [future.result() for future in futures]
        except BaseException:
            stop.set()
            raise
    cpu_end = host_stamp() if diagnostic else None
    for client in clients:
        client.phase = None
    samples = [sample for row in rows for sample in row['samples']]
    summary = metrics(samples, duration)
    complete = not stop.is_set() and all(
        row['fin_offset_s'] >= duration and not row['limite_solicitudes'] and row['samples'] for row in rows)
    result = {'inicio_utc': window['inicio_utc'], 'fin_utc': datetime.now(timezone.utc).isoformat(),
        'duracion_objetivo_s': duration, 'duracion_hasta_ultima_respuesta_s': max(
        row['fin_offset_s'] for row in rows), 'clientes': len(rows), 'completa': complete,
        'metricas': summary, 'creados': sum(row['creados'] for row in rows),
        'inicio_clientes_offset_ms': [row['inicio_offset_ms'] for row in rows]}
    if diagnostic:
        result['cpu_generador_host'] = host_summary(window['cpu_start'], cpu_end)
    return result, rows


def execute(manifest, smoke, diagnostic=False):
    port = validate_manifest(manifest)
    date.fromisoformat(manifest['incident_date'])
    require(not diagnostic or smoke, 'DIAGNOSTICO_SOLO_SMOKE')
    clients = [Client(port) for _ in range(10)]
    for client in clients:
        client.diagnostic = diagnostic
    report = {'fecha_utc': datetime.now(timezone.utc).isoformat(), 'run_id': manifest['run_id'],
              'estado': 'INCOMPLETA', 'modo': 'smoke' if smoke else 'RNF2',
              'hardware_declarado': manifest['hardware'], 'codigo_declarado': manifest['code_identity'],
              'imagenes_declaradas': manifest['images'], 'proveedores_encolado_declarados': manifest['provider_queue_mode'],
              'aislamiento': 'Declarado en manifiesto, puerto no operativo y fixture comprobados; no inspecciona recursos Docker.',
              'limites': ['No mide CPU/memoria de contenedores automáticamente; registro externo pendiente.',
                         'Comprobación de muestras HTTP y conteos; no inspecciona auditoría ni trabajos en SQL.',
                         'Sin proveedor externo medido. Configuración de proveedor/cola declarada por operador.',
                         'No crea ni detiene infraestructura, ni borra datos. QA debe ser exclusiva para esta corrida.']}
    try:
        preflight(manifest, clients)
        report['conteo_inicial'] = 100
        warmup, warm_rows = phase_run(clients, manifest, 2 if smoke else 30, 'calentamiento')
        report['calentamiento'] = warmup
        require(warmup['completa'], 'CALENTAMIENTO_INCOMPLETO')
        after_warm = clients[0].checked('GET', '/incidents?page=1&page_size=20')['total']
        require(after_warm == 100 + warmup['creados'], 'CONTEO_CALENTAMIENTO')
        report['conteo_tras_calentamiento'] = after_warm
        measurement, rows = phase_run(clients, manifest, 5 if smoke else 300, 'medicion')
        report['medicion'] = measurement
        report['estado'] = verdict(measurement['metricas'], measurement['completa'], smoke)
        for client in clients:
            client.close()
        final = clients[0].checked('GET', '/incidents?page=1&page_size=20')['total']
        report['conteo_final'] = final
        require(final == after_warm + measurement['creados'], 'CONTEO_FINAL')
        for client, account, warm, measured in zip(clients, manifest['users'], warm_rows, rows):
            for created in (warm['ultimo_creado'], measured['ultimo_creado']):
                if created:
                    require(client.checked('GET', '/incidents/' + created)['id'] == created, 'MUESTRA_CREADA')
            case_id = account['case_ids'][0]
            require(client.checked('GET', '/incidents/' + case_id)['id'] == case_id, 'MUESTRA_RESERVADA')
        require(clients[0].checked('GET', '/health/db')['status'] == 'ok', 'SALUD_FINAL')
        report['comprobaciones_http_posteriores'] = 'OK'
    except KeyboardInterrupt:
        report['estado'] = 'INTERRUMPIDA'
    except Exception as exc:
        report['estado'] = 'INCOMPLETA'
        report['error_codigo'] = str(exc) if isinstance(exc, InvalidRun) else type(exc).__name__
    finally:
        logout = Counter()
        for client in clients:
            if client.token:
                try:
                    client.close()
                    status, _ = client.request('POST', '/auth/logout')
                    logout[str(status)] += 1
                except Exception:
                    logout['EXCEPTION'] += 1
            client.close()
            client.token = None
        report['revocacion_sesiones'] = dict(logout)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--confirm-isolated-qa', action='store_true', required=True)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    # Reservar salida antes de cualquier HTTP; nunca sobrescribir evidencia.
    with args.report.open('x', encoding='utf-8') as output:
        try:
            manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
            result = execute(manifest, args.smoke)
        except Exception as exc:
            result = {'estado': 'CONFIGURACION_RECHAZADA',
                      'error_codigo': str(exc) if isinstance(exc, InvalidRun) else type(exc).__name__}
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print(result['estado'])
    return 0 if result['estado'] in {'APROBADA_ALCANCE_HTTP_QA', 'SMOKE_SIN_ACREDITAR_RNF2'} else 1


if __name__ == '__main__':
    raise SystemExit(main())
