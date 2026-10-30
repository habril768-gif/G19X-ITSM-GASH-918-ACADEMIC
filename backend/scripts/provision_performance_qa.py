"""Provisiona QA Docker nuevo, mide y detiene solo sus recursos; sin borrar volúmenes."""
import argparse
from datetime import date, datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import secrets
import shutil
import socket
import subprocess
import threading
import time
from uuid import uuid4

import performance_runner as runner
import performance_db_probe as db_probe_helper
import performance_sql_stats as sql_stats_helper


class ProvisionError(Exception):
    pass


def ensure(condition, code):
    if not condition:
        raise ProvisionError(code)


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def local_endpoint(endpoint):
    return endpoint in {'npipe:////./pipe/dockerDesktopLinuxEngine', 'npipe:////./pipe/docker_engine'} or (
        endpoint.startswith('unix:///') and '..' not in endpoint)


def validate_workers(workers, diagnostic=False, mode='smoke'):
    ensure(isinstance(workers, int) and not isinstance(workers, bool) and workers in (1, 2), 'API_WORKERS_INVALIDOS')
    ensure(workers == 1 or (not diagnostic and mode == 'smoke'), 'API_WORKERS_SOLO_SMOKE_SIN_DIAGNOSTICO')


def workers_command():
    return ['python', '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000', '--workers', '2']


def specification(repo, run_id, port, diagnostic=False, db_probe=False, server_stats=False, api_workers=1):
    validate_workers(api_workers, diagnostic)
    ensure(not db_probe or diagnostic, 'SONDEO_SOLO_DIAGNOSTICO_SMOKE')
    ensure(not server_stats or diagnostic, 'SQL_STATS_SOLO_DIAGNOSTICO_SMOKE')
    project = 'plurione-qa-perf-' + run_id
    db_name, db_user = 'plurione_test_perf_' + run_id, 'qa_perf_' + run_id
    labels = {'plurione.qa.scope': 'performance', 'plurione.qa.run_id': run_id}
    database = {'POSTGRES_HOST': 'postgres', 'POSTGRES_PORT': '5432', 'POSTGRES_DB': db_name,
                'POSTGRES_USER': db_user, 'POSTGRES_PASSWORD': '${QA_PERF_PG_PASSWORD:?}' }
    health = {'interval': '5s', 'timeout': '3s', 'retries': 24, 'start_period': '10s'}
    config = {'name': project, 'services': {
        'postgres': {'image': 'postgres:17-bookworm', 'labels': labels,
                     'environment': {key: database[key] for key in ('POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD')},
                     'volumes': ['pgdata:/var/lib/postgresql/data'],
                     'healthcheck': dict(health, test=['CMD', 'pg_isready', '-h', '127.0.0.1', '-U', db_user, '-d', db_name])},
        'redis': {'image': 'redis:7.4-bookworm', 'labels': labels,
                  'volumes': ['redisdata:/data'],
                  'healthcheck': dict(health, test=['CMD', 'redis-cli', 'ping'])},
        'api': {'build': {'context': str(repo / 'backend')}, 'image': project + '-api', 'labels': labels,
                'ports': [f'127.0.0.1:{port}:8000'],
                'networks': ['default', 'entry'],
                'environment': dict(database, REDIS_URL='redis://redis:6379/0', AI_ENABLED='false', MAIL_ENABLED='false'),
                'depends_on': {key: {'condition': 'service_healthy'} for key in ('postgres', 'redis')},
                'healthcheck': dict(health, test=['CMD', 'python', '-c',
                    "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).close()"])}},
        'volumes': {'pgdata': {'name': project + '_postgres'}, 'redisdata': {'name': project + '_redis'}},
        'networks': {'default': {'name': project + '_net', 'internal': True},
                     'entry': {'name': project + '_entry', 'internal': False}}}

    if api_workers == 2:
        config['services']['api']['environment']['QA_PERF_API_WORKERS'] = '2'
        config['services']['api']['command'] = workers_command()
    if diagnostic:
        config['services']['api']['environment']['QA_PERF_DIAGNOSTIC_RUN_ID'] = run_id
        config['services']['api']['command'] = ['python', '-m', 'uvicorn',
            'app.core.performance_diagnostics:app', '--host', '0.0.0.0', '--port', '8000']
    if db_probe:
        config['services']['api']['environment']['QA_PERF_DB_PROBE'] = 'true'
    if server_stats:
        config['services']['api']['environment']['QA_PERF_SQL_STATS'] = 'true'
        config['services']['postgres']['command'] = list(sql_stats_helper.PG_COMMAND)
    return config


def validate_resolved(config, project, port, repo):
    ensure(set(config['services']) == {'api', 'postgres', 'redis'}, 'SERVICIOS_INESPERADOS')
    expected_volumes = {project + '_postgres', project + '_redis'}
    ensure({value['name'] for value in config['volumes'].values()} == expected_volumes, 'VOLUMENES_AJENOS')
    ensure(all(not value.get('external') for value in config['volumes'].values()), 'VOLUMEN_EXTERNO')
    network = config['networks']['default']
    ensure(network['name'] == project + '_net' and network.get('internal') is True and not network.get('external'), 'RED_AJENA')
    ensure(set(config['networks']) == {'default', 'entry'}, 'REDES_INESPERADAS')
    entry = config['networks']['entry']
    ensure(entry['name'] == project + '_entry' and not entry.get('internal') and not entry.get('external'), 'RED_ENTRADA_AJENA')
    api = config['services']['api']
    ensure(set(api['networks']) == {'default', 'entry'}, 'REDES_API')
    ensure(Path(api['build']['context']).resolve() == (repo / 'backend').resolve(), 'CONTEXTO_BUILD')
    ensure(api['ports'] == [{'mode': 'ingress', 'host_ip': '127.0.0.1', 'target': 8000,
                             'published': str(port), 'protocol': 'tcp'}], 'PUERTO_NO_AISLADO')
    for service in config['services'].values():
        ensure(service.get('labels', {}).get('plurione.qa.run_id') == project.removeprefix('plurione-qa-perf-'), 'ETIQUETAS_QA')
        ensure(not service.get('privileged') and not service.get('network_mode'), 'PRIVILEGIOS_RED')
        ensure(all(mount['type'] == 'volume' and mount['source'] in {'pgdata', 'redisdata'}
                   for mount in service.get('volumes', [])), 'MONTAJE_AJENO')
    diagnostic_id = api['environment'].get('QA_PERF_DIAGNOSTIC_RUN_ID')
    expected_command = ['python', '-m', 'uvicorn', 'app.core.performance_diagnostics:app', '--host', '0.0.0.0', '--port', '8000']
    worker_marker = api['environment'].get('QA_PERF_API_WORKERS')
    ensure(worker_marker in (None, '2') and not (worker_marker and diagnostic_id is not None), 'API_WORKERS_CONFIG_INVALIDA')
    if diagnostic_id is not None:
        ensure(diagnostic_id == project.removeprefix('plurione-qa-perf-') and api.get('command') == expected_command, 'ENTRADA_DIAGNOSTICO_INVALIDA')
    else:
        ensure(api.get('command') == workers_command() if worker_marker else not api.get('command'), 'COMANDO_API_INESPERADO')
    ensure(api['environment'].get('QA_PERF_DB_PROBE') in (None, 'true') and
           (not api['environment'].get('QA_PERF_DB_PROBE') or diagnostic_id is not None), 'SONDEO_DB_CONFIG_INVALIDA')
    stats_enabled = api['environment'].get('QA_PERF_SQL_STATS')
    ensure(stats_enabled in (None, 'true') and (not stats_enabled or diagnostic_id is not None), 'SQL_STATS_CONFIG_INVALIDA')
    pg_command = config['services']['postgres'].get('command')
    ensure(pg_command == sql_stats_helper.PG_COMMAND if stats_enabled else not pg_command, 'SQL_STATS_COMANDO_PG_INVALIDO')
    ensure(not api.get('volumes'), 'MONTAJE_API')
    ensure(all(not config['services'][name].get('ports') for name in ('postgres', 'redis')), 'PUERTO_DB_PUBLICADO')
    ensure(all(set(config['services'][name].get('networks', {'default': None})) == {'default'}
               for name in ('postgres', 'redis')), 'DATOS_EN_RED_ENTRADA')
    ensure(api['environment'].get('AI_ENABLED') == 'false' and api['environment'].get('MAIL_ENABLED') == 'false', 'PROVEEDORES_ACTIVOS')


def command(argv, env, stage, payload=None, timeout=60):
    try:
        result = subprocess.run(argv, input=payload, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise ProvisionError(stage + '_TIEMPO_AGOTADO') from None
    except OSError:
        raise ProvisionError(stage + '_ERROR_INVOCACION') from None
    ensure(result.returncode == 0, stage + '_SALIDA_' + str(result.returncode))
    return result.stdout


def inspect_owned(docker, ids, env, project):
    ensure(len(ids) == 3, 'CONTENEDORES_INCOMPLETOS')
    containers = json.loads(command(docker + ['inspect', *ids], env, 'INSPECT'))
    services = set()
    for row in containers:
        labels = row['Config']['Labels']
        ensure(labels.get('com.docker.compose.project') == project and
               labels.get('plurione.qa.scope') == 'performance', 'CONTENEDOR_AJENO')
        service = labels['com.docker.compose.service']
        services.add(service)
        expected_networks = {project + '_net', project + '_entry'} if service == 'api' else {project + '_net'}
        ensure(set(row['NetworkSettings']['Networks']) == expected_networks, 'RED_CONTENEDOR_AJENA')
        ensure(all(mount.get('Type') == 'volume' and mount.get('Name') in {
            project + '_postgres', project + '_redis'} for mount in row['Mounts']), 'VOLUMEN_CONTENEDOR_AJENO')
    ensure(services == {'api', 'postgres', 'redis'}, 'SERVICIOS_CONTENEDORES')
    return {row['Config']['Labels']['com.docker.compose.service']: {
        'image_id': row['Image'], 'health': row['State'].get('Health', {}).get('Status'),
        'ports': row['NetworkSettings'].get('Ports'), 'networks': sorted(row['NetworkSettings']['Networks'])}
        for row in containers}


def wait_http(port, diagnostics, timeout=30):
    """Solo reintenta lecturas de salud; nunca escrituras o logins."""
    deadline = time.perf_counter() + timeout
    diagnostics.update(intentos=0, errores={})
    while time.perf_counter() < deadline:
        client = runner.Client(port)
        diagnostics['intentos'] += 1
        try:
            for path in ('/health', '/health/db'):
                status, body = client.request('GET', path)
                ensure(status == 200 and isinstance(body, dict) and body.get('status') == 'ok', 'SALUD_HTTP_NO_OK')
            diagnostics['resultado'] = 'OK'
            return
        except Exception as exc:
            name = type(exc).__name__
            diagnostics['errores'][name] = diagnostics['errores'].get(name, 0) + 1
        finally:
            client.close()
        time.sleep(min(1, max(0, deadline - time.perf_counter())))
    diagnostics['resultado'] = 'NO_ACCESIBLE'
    raise ProvisionError('API_QA_NO_ACCESIBLE_DESDE_HOST')


def run(repo, mode, docker_exe, diagnostic=False, *, preflight=None, db_probe=False, server_stats=False, api_workers=1):
    validate_workers(api_workers, diagnostic, mode)
    ensure(not diagnostic or mode == 'smoke', 'DIAGNOSTICO_SOLO_SMOKE')
    ensure(not db_probe or (diagnostic and mode == 'smoke'), 'SONDEO_SOLO_DIAGNOSTICO_SMOKE')
    ensure(not server_stats or (diagnostic and mode == 'smoke'), 'SQL_STATS_SOLO_DIAGNOSTICO_SMOKE')
    run_id = uuid4().hex[:16]
    project = 'plurione-qa-perf-' + run_id
    port = free_port()
    report = {'fecha_utc': datetime.now(timezone.utc).isoformat(), 'run_id': run_id, 'modo': mode,
              'estado': 'INCOMPLETA', 'api_workers_declarados': api_workers, 'limites': ['No es una instalación de producción ni recuperación de datos operativos.',
                'Recursos QA retenidos y detenidos cuando es posible; sin borrar volúmenes.',
                'Contraseñas aleatorias no guardadas en manifiesto/reporte; metadatos de contenedores contienen configuración privada.',
                'Muestreo docker stats añade carga al mismo equipo.']}
    if preflight is not None:
        report['precondiciones_arranque'] = preflight
    folder = repo / '.pgdata' / ('performance-' + run_id)
    folder.mkdir(parents=True, exist_ok=False)
    config_path = folder / 'compose.json'
    config_path.write_text(json.dumps(specification(repo, run_id, port, diagnostic, db_probe, server_stats, api_workers), indent=2), encoding='utf-8')
    env_path = folder / 'empty.env'
    env_path.write_text('', encoding='utf-8')
    env = {key: value for key, value in os.environ.items() if not key.startswith('COMPOSE_')}
    env['QA_PERF_PG_PASSWORD'] = secrets.token_urlsafe(32)
    passwords = [secrets.token_urlsafe(24) for _ in range(10)]
    old_passwords = {f'PLURIONE_PERF_PASSWORD_{i}': os.environ.get(f'PLURIONE_PERF_PASSWORD_{i}') for i in range(10)}
    base = None
    docker = None
    started = False
    stop_sampling = threading.Event()
    sampler = None
    samples = []
    seed_code = Path(__file__).with_name('performance_seed.py').read_text(encoding='utf-8')
    try:
        print('Verificando Docker y recursos QA nuevos...', flush=True)
        context = command([docker_exe, 'context', 'show'], env, 'CONTEXTO').strip()
        contexts = json.loads(command([docker_exe, 'context', 'inspect', context], env, 'CONTEXTO_INSPECT'))
        ensure(len(contexts) == 1 and local_endpoint(contexts[0]['Endpoints']['docker']['Host']), 'DOCKER_NO_LOCAL')
        docker = [docker_exe, '--context', context]
        base = docker + ['compose', '--project-directory', str(folder), '--env-file', str(env_path),
                         '-p', project, '-f', str(config_path)]
        ensure(not command(docker + ['ps', '-aq', '--filter', 'label=com.docker.compose.project=' + project], env, 'COLISION_CONTENEDORES').strip(), 'PROYECTO_EXISTENTE')
        volumes = command(docker + ['volume', 'ls', '--format', '{{.Name}}'], env, 'LISTAR_VOLUMENES').splitlines()
        ensure(not ({project + '_postgres', project + '_redis'} & set(volumes)), 'VOLUMEN_EXISTENTE')
        networks = command(docker + ['network', 'ls', '--format', '{{.Name}}'], env, 'LISTAR_REDES').splitlines()
        ensure(not ({project + '_net', project + '_entry'} & set(networks)), 'RED_EXISTENTE')
        resolved = json.loads(command(base + ['config', '--format', 'json'], env, 'COMPOSE_CONFIG'))
        validate_resolved(resolved, project, port, repo)
        report['configuracion_validada'] = True
        print('Construyendo e iniciando tres servicios QA; puede tardar varios minutos...', flush=True)
        started = True
        report['arranque_qa'] = {'inicio_utc': datetime.now(timezone.utc).isoformat(),
                                'limite_s': 900, 'resultado': 'EN_CURSO'}
        startup_origin = time.perf_counter()
        try:
            command(base + ['up', '-d', '--build', '--wait'], env, 'ARRANQUE_QA', timeout=900)
        except ProvisionError as exc:
            report['arranque_qa']['resultado'] = str(exc)
            raise
        else:
            report['arranque_qa']['resultado'] = 'OK'
        finally:
            report['arranque_qa']['duracion_s'] = time.perf_counter() - startup_origin
            report['arranque_qa']['fin_utc'] = datetime.now(timezone.utc).isoformat()
        ids = command(base + ['ps', '-aq'], env, 'IDS_QA').split()
        report['contenedores'] = inspect_owned(docker, ids, env, project)
        if api_workers == 2:
            api_id = command(base + ['ps', '-q', 'api'], env, 'ID_API_WORKERS').strip()
            ensure(api_id in ids, 'ID_API_WORKERS_AJENO')
            actual_command = json.loads(command(docker + ['inspect', '--format', '{{json .Config.Cmd}}', api_id], env, 'COMANDO_API_WORKERS'))
            ensure(actual_command == workers_command(), 'COMANDO_API_WORKERS_DISTINTO')
            report['comando_api_workers_verificado'] = True
        print('Aplicando migraciones y comprobando acceso HTTP desde el host...', flush=True)
        command(base + ['exec', '-T', 'api', 'python', '-m', 'alembic', 'upgrade', 'head'], env, 'MIGRACIONES', timeout=120)
        report['comprobacion_http_previa'] = {}
        wait_http(port, report['comprobacion_http_previa'])
        print('Creando diez cuentas/cien casos ficticios...', flush=True)
        fixture = json.loads(command(base + ['exec', '-T', 'api', 'python', '-c', seed_code], env, 'FIXTURE',
            payload=json.dumps({'action': 'seed', 'run_id': run_id, 'passwords': passwords,
                                'incident_date': date.today().isoformat()}), timeout=180))
        info = json.loads(command(docker + ['info', '--format', '{{json .}}'], env, 'INFO_DOCKER'))
        manifest = dict(fixture, scope='plurione-performance-isolated', run_id=run_id,
            base_url=f'http://127.0.0.1:{port}', compose_project=project, isolated_resources_confirmed=True,
            incident_date=date.today().isoformat(),
            hardware={'os': platform.platform(), 'cpu': platform.processor(), 'cpu_logicas_host': os.cpu_count(),
                      'docker_cpus': info.get('NCPU'), 'docker_mem_bytes': info.get('MemTotal'),
                      'docker_server': info.get('ServerVersion'), 'docker_os': info.get('OSType'),
                      'generador': 'mismo host que Docker; sin limite de recursos por contenedor'},
            images=report['contenedores'], code_identity={'sha256': {
                path.relative_to(repo).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(list((repo / 'backend' / 'app').rglob('*.py')) +
                                   [path for path in (repo / 'backend' / 'migrations').rglob('*')
                                    if path.is_file() and path.suffix in {'.py', '.sql'}] +
                                   [repo / 'backend' / 'Dockerfile', repo / 'backend' / 'requirements.txt'])}},
            provider_queue_mode={'AI_ENABLED': False, 'MAIL_ENABLED': False, 'workers': 'ninguno',
                                 'creacion': 'queue_event del producto; se verifica conteo de MailDelivery sin intentos SMTP'})
        runner.validate_manifest(manifest)
        (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        for index, password in enumerate(passwords):
            os.environ[f'PLURIONE_PERF_PASSWORD_{index}'] = password
        if server_stats:
            print('Activando estadisticas SQL solo en PostgreSQL QA nuevo...', flush=True)
            stats_code = Path(__file__).with_name('performance_sql_stats.py').read_text(encoding='utf-8-sig')
            stats_before = json.loads(command(base + ['exec', '-T', 'api', 'python', '-c', stats_code], env,
                'SQL_STATS_ANTES', payload=json.dumps({'action': 'before', 'run_id': run_id}), timeout=60))
            sql_stats_helper.validate_snapshot(stats_before, run_id)
        def sample_resources():
            origin = time.perf_counter()
            while not stop_sampling.is_set():
                try:
                    rows = command(docker + ['stats', '--no-stream', '--format', '{{json .}}', *ids],
                                   env, 'STATS', timeout=15)
                    samples.append({'fecha_utc': datetime.now(timezone.utc).isoformat(),
                                    'elapsed_s': time.perf_counter() - origin,
                                    'containers': [json.loads(line) for line in rows.splitlines() if line.strip()]})
                except Exception:
                    samples.append({'elapsed_s': time.perf_counter() - origin, 'error': 'STATS_NO_DISPONIBLE'})
                stop_sampling.wait(5)
        sampler = threading.Thread(target=sample_resources, daemon=True)
        sampler.start()
        print('Ejecutando ' + ('smoke de 2 + 5 segundos...' if mode == 'smoke' else '30 s de calentamiento y 300 s de medición...'), flush=True)
        measured = runner.execute(manifest, mode == 'smoke', diagnostic=True) if diagnostic else runner.execute(manifest, mode == 'smoke')
        report['instrumentacion_diagnostica'] = diagnostic
        report['http'] = measured
        stop_sampling.set()
        sampler.join(timeout=20)
        report['recursos'] = samples
        print('Verificando auditoría y colas en PostgreSQL QA...', flush=True)
        sql = json.loads(command(base + ['exec', '-T', 'api', 'python', '-c', seed_code], env, 'VERIFICACION_SQL',
                                 payload=json.dumps({'action': 'verify', 'run_id': run_id}), timeout=60))
        report['comprobacion_sql'] = sql
        if 'conteo_final' in measured:
            ensure(sql['incidencias'] == measured['conteo_final'], 'CONTEO_SQL_HTTP')
            expected_edits = sum(measured[phase]['metricas']['actualizacion']['exitos']
                                 for phase in ('calentamiento', 'medicion') if phase in measured)
            ensure(sql['eventos_editado'] == expected_edits, 'AUDITORIA_EDICION')
        report['estado'] = measured['estado']
        if mode == 'full' and report['estado'] == 'APROBADA_ALCANCE_HTTP_QA':
            # Aún requiere revisión del equipo/generador y de las muestras, no aprobación automática integral.
            report['revision_recursos_pendiente'] = True
        if server_stats:
            stats_after = json.loads(command(base + ['exec', '-T', 'api', 'python', '-c', stats_code], env,
                'SQL_STATS_DESPUES', payload=json.dumps({'action': 'after', 'run_id': run_id}), timeout=60))
            report['servidor_sql'] = sql_stats_helper.difference(stats_before, stats_after, run_id)
        if db_probe:
            print('Control breve SELECT1: tiempos de driver y servidor, sin carga HTTP...', flush=True)
            probe_code = Path(__file__).with_name('performance_db_probe.py').read_text(encoding='utf-8-sig')
            probe = json.loads(command(base + ['exec', '-T', 'api', 'python', '-c', probe_code], env,
                'SONDEO_DB', payload=json.dumps({'run_id': run_id}), timeout=60))
            report['sondeo_db'] = db_probe_helper.validate(probe)
    except KeyboardInterrupt:
        report['estado'] = 'INTERRUMPIDA'
    except Exception as exc:
        report['estado'] = 'INCOMPLETA'
        report['error_codigo'] = str(exc) if isinstance(exc, ProvisionError) else type(exc).__name__
    finally:
        stop_sampling.set()
        if sampler:
            sampler.join(timeout=20)
        report['recursos'] = samples
        for key, previous in old_passwords.items():
            if previous is None: os.environ.pop(key, None)
            else: os.environ[key] = previous
        if started and base:
            try:
                # El archivo generado solo contiene el proyecto y recursos propios ya validados.
                command(base + ['stop', '-t', '10'], env, 'PARADA_QA', timeout=60)
                states = json.loads(command(docker + ['inspect', *command(base + ['ps', '-aq'], env, 'IDS_PARADA').split()], env, 'ESTADO_PARADA'))
                report['contenedores_detenidos'] = bool(states) and all(not row['State']['Running'] for row in states)
            except Exception:
                report['contenedores_detenidos'] = False
                report['parada_requiere_revision'] = True
        else:
            report['recursos_iniciados'] = False
        if started and not report.get('contenedores_detenidos') and report['estado'] in {
                'APROBADA_ALCANCE_HTTP_QA', 'SMOKE_SIN_ACREDITAR_RNF2'}:
            report['estado_antes_parada'] = report['estado']
            report['estado'] = 'INCOMPLETA_PARADA_QA'
        report['recursos_retenidos'] = {'project': project, 'folder': str(folder), 'sin_borrado_volumenes': True}
        if diagnostic and report.get('contenedores_detenidos'):
            try:
                logs = command(base + ['logs', '--no-color', '--no-log-prefix', 'api'], env, 'DIAGNOSTICO_LOG', timeout=30)
                report['diagnostico'] = read_diagnostics(logs, report.get('http', {}))
                if report['estado'] == 'SMOKE_SIN_ACREDITAR_RNF2':
                    report['estado'] = 'DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2'
            except Exception:
                report['diagnostico_error'] = 'DIAGNOSTICO_NO_VALIDADO'
                report['estado'] = 'INCOMPLETA_DIAGNOSTICO'
        with (folder / 'report.json').open('x', encoding='utf-8') as output:
            json.dump(report, output, ensure_ascii=False, indent=2)
            output.write('\n')
    print('Reporte local: ' + str(folder / 'report.json'), flush=True)
    print(report['estado'], flush=True)
    return 0 if report['estado'] in {'APROBADA_ALCANCE_HTTP_QA', 'SMOKE_SIN_ACREDITAR_RNF2', 'DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2'} and report.get('contenedores_detenidos') else 1



def read_diagnostics(logs, measured):
    prefix = 'QA_PERF_DIAGNOSTICS_JSON='
    lines = [line[len(prefix):] for line in logs.splitlines() if line.startswith(prefix)]
    ensure(len(lines) == 1 and len(lines[0]) < 200000, 'DIAGNOSTICO_AUSENTE_O_DUPLICADO')
    value = json.loads(lines[0])
    ensure(value.get('version') in (3, 4, 5) and value.get('limite_excedido') is False, 'DIAGNOSTICO_INCOMPLETO')
    if value['version'] in (4, 5):
        ensure(value.get('pool_ping_instrumentado') is True, 'DIAGNOSTICO_POOL_PING_AUSENTE')
    if value['version'] == 5:
        ensure(value.get('thread_cpu_instrumentado') is True, 'DIAGNOSTICO_CPU_HILO_AUSENTE')
    expected = {phase + '/' + op for phase in ('calentamiento', 'medicion') for op in runner.OPS}
    ensure(set(value['grupos']) == expected, 'DIAGNOSTICO_GRUPOS')
    for key, group in value['grupos'].items():
        phase, op = key.split('/')
        ensure(group['solicitudes'] == measured[phase]['metricas'][op]['intentos'] and group['solicitudes'] > 0
               and group['errores'] == 0, 'DIAGNOSTICO_CONTEO')
        for field in ('total', 'auth', 'endpoint', 'sql', 'consultas'):
            ensure(group['metricas'][field]['media'] > 0, 'DIAGNOSTICO_ETAPA_AUSENTE')
        if value['version'] in (4, 5):
            for field in ('pool_ping', 'pool_ping_calls', 'pool_ping_errors'):
                stats = group['metricas'].get(field, {})
                ensure(all(isinstance(stats.get(k), (int, float)) and not isinstance(stats[k], bool)
                           and math.isfinite(stats[k]) and stats[k] >= 0 for k in ('media', 'p95', 'max')),
                       'DIAGNOSTICO_POOL_PING_INVALIDO')
                ensure(stats['media'] <= stats['max'] + 1e-9 and stats['p95'] <= stats['max'] + 1e-9,
                       'DIAGNOSTICO_POOL_PING_INVALIDO')
            calls = group['metricas']['pool_ping_calls']['media'] * group['solicitudes']
            errors = group['metricas']['pool_ping_errors']['media'] * group['solicitudes']
            ensure(math.isclose(calls, round(calls), abs_tol=1e-6)
                   and math.isclose(errors, round(errors), abs_tol=1e-6) and errors <= calls,
                   'DIAGNOSTICO_POOL_PING_INVALIDO')
            if calls == 0:
                ensure(all(group['metricas'][field][k] == 0 for field in
                           ('pool_ping', 'pool_ping_calls', 'pool_ping_errors') for k in ('media', 'p95', 'max')),
                       'DIAGNOSTICO_POOL_PING_INVALIDO')
        families = group.get('familias_sql', {})
        ensure(bool(families), 'DIAGNOSTICO_FAMILIAS_AUSENTES')
        expected_count = group['metricas']['consultas']['media'] * group['solicitudes']
        expected_ms = group['metricas']['sql']['media'] * group['solicitudes']
        ensure(math.isclose(sum(f['consultas'] for f in families.values()), expected_count, abs_tol=1e-6), 'DIAGNOSTICO_FAMILIAS_CONTEO')
        ensure(math.isclose(sum(f['ms'] for f in families.values()), expected_ms, rel_tol=1e-8, abs_tol=1e-6), 'DIAGNOSTICO_FAMILIAS_TIEMPO')
        stages = group.get('thread_stages', {})
        ensure(bool(stages) and set(stages) <= {'auth', 'endpoint', 'response_validation', 'dependency_enter', 'dependency_exit', 'other'}, 'DIAGNOSTICO_HILOS_AUSENTES')
        ensure(group['metricas']['thread_calls']['media'] > 0 and group['metricas']['thread_incomplete']['media'] == 0, 'DIAGNOSTICO_HILOS_INCOMPLETOS')
        for field, item in (('thread_calls', 'calls'), ('thread_wait', 'wait_ms'), ('thread_run', 'run_ms'), ('thread_resume', 'resume_ms'), ('thread_incomplete', 'incomplete')):
            expected_value = group['metricas'][field]['media'] * group['solicitudes']
            ensure(math.isclose(sum(s[item] for s in stages.values()), expected_value, rel_tol=1e-8, abs_tol=1e-6), 'DIAGNOSTICO_HILOS_SUMAS')
        if value['version'] == 5:
            stats = group['metricas'].get('thread_cpu', {})
            ensure(isinstance(stats, dict) and all(isinstance(stats.get(k), (int, float))
                   and not isinstance(stats[k], bool) and math.isfinite(stats[k]) and stats[k] >= 0
                   for k in ('media', 'p95', 'max')), 'DIAGNOSTICO_CPU_HILO_INVALIDO')
            ensure(stats['media'] <= stats['max'] + 1e-9 and stats['p95'] <= stats['max'] + 1e-9,
                   'DIAGNOSTICO_CPU_HILO_INVALIDO')
            ensure(all(isinstance(stage.get('cpu_ms'), (int, float)) and not isinstance(stage['cpu_ms'], bool)
                       and math.isfinite(stage['cpu_ms']) and stage['cpu_ms'] >= 0 for stage in stages.values()),
                   'DIAGNOSTICO_CPU_HILO_INVALIDO')
            ensure(math.isclose(sum(stage['cpu_ms'] for stage in stages.values()),
                                stats['media'] * group['solicitudes'], rel_tol=1e-8, abs_tol=1e-6),
                   'DIAGNOSTICO_CPU_HILO_SUMAS')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['smoke', 'full'], default='smoke')
    parser.add_argument('--diagnostic', action='store_true', help='Solo smoke: tiempos por etapas en API QA; no acredita RNF-2.')
    parser.add_argument('--db-probe', action='store_true', help='Solo smoke diagnostico: control SELECT1 despues de la carga, sin extensiones.')
    parser.add_argument('--server-stats', action='store_true', help='Solo smoke diagnostico: pg_stat_statements en PostgreSQL QA nuevo; no modifica el sitio.')
    parser.add_argument('--api-workers', type=int, choices=[1, 2], default=1, help='Dos procesos solo para smoke sin diagnostico; no cambia el sitio.')
    parser.add_argument('--confirm-isolated-qa', action='store_true')
    parser.add_argument('--plan', action='store_true', help='Muestra plan sin Docker, archivos o contraseñas.')
    args = parser.parse_args()
    validate_workers(args.api_workers, args.diagnostic, args.mode)
    ensure(not args.diagnostic or args.mode == 'smoke', 'DIAGNOSTICO_SOLO_SMOKE')
    ensure(not args.db_probe or (args.diagnostic and args.mode == 'smoke'), 'SONDEO_SOLO_DIAGNOSTICO_SMOKE')
    ensure(not args.server_stats or (args.diagnostic and args.mode == 'smoke'), 'SQL_STATS_SOLO_DIAGNOSTICO_SMOKE')
    repo = Path(__file__).resolve().parents[2]
    if args.plan:
        print(json.dumps({'services': ['api', 'postgres', 'redis'], 'users': 10, 'initial_cases': 100,
                          'mode': args.mode, 'diagnostic': args.diagnostic, 'db_probe': args.db_probe, 'server_stats': args.server_stats, 'api_workers': args.api_workers, 'resources': 'project/volumes/network/port nuevos',
                          'external_workers': False, 'cleanup': 'stop sin eliminar volúmenes'}, indent=2))
        return 0
    ensure(args.confirm_isolated_qa, 'CONFIRMACION_QA_REQUERIDA')
    docker = shutil.which('docker')
    ensure(bool(docker), 'DOCKER_CLI_NO_ENCONTRADO')
    if args.api_workers == 2:
        return run(repo, args.mode, docker, api_workers=2)
    if args.server_stats:
        return run(repo, args.mode, docker, diagnostic=True, db_probe=args.db_probe, server_stats=True)
    if args.db_probe:
        return run(repo, args.mode, docker, diagnostic=True, db_probe=True)
    return run(repo, args.mode, docker, diagnostic=True) if args.diagnostic else run(repo, args.mode, docker)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except ProvisionError as exc:
        print(str(exc))
        raise SystemExit(1)
