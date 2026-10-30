"""Validación del provisionador con Docker simulado; no arranca contenedores."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from uuid import UUID

scripts = Path(__file__).resolve().parents[1] / 'scripts'
if not (scripts / 'provision_performance_qa.py').exists():
    scripts = Path(__file__).parent
sys.path.insert(0, str(scripts))
import provision_performance_qa as provision
import performance_seed as seed


def normalized(config):
    config = copy.deepcopy(config)
    port = config['services']['api']['ports'][0].split(':')[1]
    config['services']['api']['ports'] = [{'mode': 'ingress', 'host_ip': '127.0.0.1',
        'target': 8000, 'published': port, 'protocol': 'tcp'}]
    for service in config['services'].values():
        if 'volumes' in service:
            service['volumes'] = [{'type': 'volume', 'source': mount.split(':')[0],
                                   'target': mount.split(':')[1]} for mount in service['volumes']]
    return config


class ProvisionTests(unittest.TestCase):
    def test_spec_has_only_own_resources_and_loopback_api(self):
        repo = Path.cwd()
        config = provision.specification(repo, 'qa123456', 18080)
        provision.validate_resolved(normalized(config), 'plurione-qa-perf-qa123456', 18080, repo)
        self.assertEqual(set(config['services']), {'api', 'postgres', 'redis'})
        self.assertTrue(config['networks']['default']['internal'])
        self.assertFalse(config['networks']['entry']['internal'])
        self.assertEqual(config['services']['api']['networks'], ['default', 'entry'])
        self.assertNotIn('ports', config['services']['postgres'])
        self.assertNotIn('ports', config['services']['redis'])

    def test_resolved_config_rejects_external_volume_and_bind_mount(self):
        repo = Path.cwd()
        original = normalized(provision.specification(repo, 'qa123456', 18080))
        for mutate in [lambda conf: conf['volumes']['pgdata'].update(external=True),
                       lambda conf: conf['services']['api'].update(volumes=[{'type': 'bind', 'source': '/private'}]),
                       lambda conf: conf['services']['api']['ports'][0].update(host_ip='0.0.0.0')]:
            config = copy.deepcopy(original)
            mutate(config)
            with self.assertRaises(provision.ProvisionError):
                provision.validate_resolved(config, 'plurione-qa-perf-qa123456', 18080, repo)

    def test_remote_docker_endpoints_rejected(self):
        self.assertTrue(provision.local_endpoint('npipe:////./pipe/dockerDesktopLinuxEngine'))
        self.assertTrue(provision.local_endpoint('unix:///var/run/docker.sock'))
        self.assertFalse(provision.local_endpoint('tcp://127.0.0.1:2375'))
        self.assertFalse(provision.local_endpoint('ssh://host'))

    def test_command_failure_does_not_expose_input_or_stderr(self):
        with patch.object(provision.subprocess, 'run') as run:
            run.return_value.returncode = 1
            run.return_value.stderr = 'PRIVATE_PASSWORD'
            with self.assertRaisesRegex(provision.ProvisionError, '^STAGE_SALIDA_1$'):
                provision.command(['docker'], {}, 'STAGE', payload='PRIVATE_PASSWORD')

    def test_command_distinguishes_timeout_and_invocation_without_private_details(self):
        failures = [
            (provision.subprocess.TimeoutExpired(['PRIVATE_ARG'], 900,
                output='PRIVATE_OUTPUT', stderr='PRIVATE_PASSWORD'), 'ARRANQUE_QA_TIEMPO_AGOTADO'),
            (OSError('PRIVATE_PASSWORD'), 'ARRANQUE_QA_ERROR_INVOCACION'),
        ]
        for failure, code in failures:
            with self.subTest(code=code), patch.object(provision.subprocess, 'run', side_effect=failure):
                with self.assertRaises(provision.ProvisionError) as caught:
                    provision.command(['docker'], {}, 'ARRANQUE_QA', payload='PRIVATE_INPUT', timeout=900)
                self.assertEqual(str(caught.exception), code)

    def test_startup_timing_retained_on_success_and_failure(self):
        for stage, expected in [(None, 'OK'), ('ARRANQUE_QA', 'ARRANQUE_QA_SALIDA_1')]:
            with self.subTest(stage=stage):
                result, report, calls = self.simulate(fail_stage=stage)
                startup = report['arranque_qa']
                self.assertEqual(startup['resultado'], expected)
                self.assertEqual(startup['limite_s'], 900)
                self.assertGreaterEqual(startup['duracion_s'], 0)
                self.assertTrue(startup['inicio_utc'])
                self.assertTrue(startup['fin_utc'])
                if stage:
                    self.assertEqual(report['error_codigo'], expected)
                    self.assertTrue(report['contenedores_detenidos'])
                    self.assertFalse(any(name == 'MIGRACIONES' for _, name in calls))

    def test_seed_guard_checks_database_identity_and_disabled_providers(self):
        env = {'POSTGRES_DB': 'plurione_test_perf_qa123456', 'POSTGRES_USER': 'qa_perf_qa123456',
               'POSTGRES_HOST': 'postgres', 'AI_ENABLED': 'false', 'MAIL_ENABLED': 'false'}
        with patch.dict(os.environ, env):
            self.assertEqual(seed.guard({'run_id': 'qa123456'}), 'qa123456')
        for change in ({'POSTGRES_DB': 'plurione'}, {'AI_ENABLED': 'true'}):
            with patch.dict(os.environ, dict(env, **change)), self.assertRaises(ValueError):
                seed.guard({'run_id': 'qa123456'})

    def simulate(self, fail_stage=None, endpoint='npipe:////./pipe/dockerDesktopLinuxEngine', diagnostic=False, preflight=None, db_probe=False, server_stats=False, api_workers=1):
        temp = tempfile.TemporaryDirectory(prefix='qa-perf-unit-', dir=Path.cwd())
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        (repo / 'backend').mkdir()
        (repo / 'backend/Dockerfile').write_text('FROM fake', encoding='utf-8')
        (repo / 'backend/requirements.txt').write_text('', encoding='utf-8')
        calls, sent_passwords = [], []
        state = {}
        def command(argv, env, stage, payload=None, timeout=60):
            calls.append((argv, stage))
            if stage == fail_stage:
                raise provision.ProvisionError(stage + '_SALIDA_1')
            if stage == 'CONTEXTO': return 'desktop-linux'
            if stage == 'CONTEXTO_INSPECT': return json.dumps([{'Endpoints': {'docker': {'Host': endpoint}}}])
            if stage in {'COLISION_CONTENEDORES', 'LISTAR_VOLUMENES', 'LISTAR_REDES'}: return ''
            if stage == 'COMPOSE_CONFIG':
                source = json.loads(Path(argv[argv.index('-f') + 1]).read_text(encoding='utf-8'))
                state['config'] = source
                state['project'] = source['name']
                return json.dumps(normalized(source))
            if stage == 'ID_API_WORKERS': return 'one'
            if stage == 'COMANDO_API_WORKERS': return json.dumps(state['config']['services']['api']['command'])
            if stage in {'ARRANQUE_QA', 'MIGRACIONES', 'PARADA_QA'}: return ''
            if stage in {'IDS_QA', 'IDS_PARADA'}: return 'one two three'
            if stage == 'INSPECT':
                project = state['project']
                return json.dumps([{'Config': {'Labels': {'com.docker.compose.project': project,
                    'com.docker.compose.service': service, 'plurione.qa.scope': 'performance'}},
                    'Image': 'sha256:fake', 'State': {'Health': {'Status': 'healthy'}},
                    'NetworkSettings': {'Networks': {name: {} for name in
                        ([project + '_net', project + '_entry'] if service == 'api' else [project + '_net'])}}, 'Mounts': []}
                    for service in ('api', 'postgres', 'redis')])
            if stage == 'FIXTURE':
                values = json.loads(payload)
                sent_passwords.extend(values['passwords'])
                return json.dumps({'department_id': str(UUID(int=1000)), 'users': [
                    {'email': f"qa-perf-{values['run_id']}-{index}@example.invalid",
                     'password_env': f'PLURIONE_PERF_PASSWORD_{index}',
                     'case_ids': [str(UUID(int=1 + index * 10 + offset)) for offset in range(10)]}
                    for index in range(10)]})
            if stage == 'INFO_DOCKER': return json.dumps({'NCPU': 4, 'MemTotal': 8_000_000_000})
            if stage == 'STATS': return json.dumps({'Name': state['project'] + '-api-1', 'CPUPerc': '1%'})
            if stage == 'VERIFICACION_SQL': return json.dumps({'incidencias': 100, 'eventos_creado': 100,
                'eventos_editado': 2 if diagnostic else 0, 'entregas_encoladas': 1000, 'intentos_smtp': 0, 'trabajos_ia': 0})
            if stage in {'SQL_STATS_ANTES', 'SQL_STATS_DESPUES'}:
                data = json.loads(payload)
                return json.dumps(dict(version=1, run_id=data['run_id'], dealloc=0, reset='2026-10-29T12:00:00+00:00',
                    rows=[dict(key='1', family='SELECT/users', calls=10 if stage == 'SQL_STATS_ANTES' else 12, exec_ms=5 if stage == 'SQL_STATS_ANTES' else 6, rows=10 if stage == 'SQL_STATS_ANTES' else 12, since='2026-10-29T12:00:00+00:00')]))
            if stage == 'SONDEO_DB':
                return json.dumps({'version':1,'estado':'OK','limites':'Control ficticio',
                    'grupos':{name:{'clientes':clients,'muestras':clients*5,
                        'metricas':{field:{'media':0,'min':0,'max':0,'p95':0} for field in
                                   ('driver_ms','worker_cpu_ms','plan_ms','execution_ms')}}
                              for name,clients in (('solo',1),('concurrente',10))}})
            if stage == 'DIAGNOSTICO_LOG':
                groups = {phase + '/' + op: {'solicitudes': 1, 'errores': 0,
                    'metricas': {field: {'media': 1} for field in ('total', 'auth', 'endpoint', 'sql', 'consultas')}, 'familias_sql': {'SELECT/users': {'consultas': 1, 'ms': 1}}}
                    for phase in ('calentamiento', 'medicion') for op in provision.runner.OPS}
                for group in groups.values():
                    for field in ('thread_calls','thread_wait','thread_run','thread_resume'):
                        group['metricas'][field]={'media':1}
                    group['metricas']['thread_incomplete']={'media':0}
                    group['thread_stages']={'other':{'calls':1,'wait_ms':1,'run_ms':1,'resume_ms':1,'incomplete':0}}
                return 'QA_PERF_DIAGNOSTICS_JSON=' + json.dumps({'version': 3, 'limite_excedido': False, 'grupos': groups})
            if stage == 'ESTADO_PARADA': return json.dumps([{'State': {'Running': False}}] * 3)
            raise AssertionError(stage)
        measured = {'estado': 'SMOKE_SIN_ACREDITAR_RNF2', 'conteo_final': 100,
                    'calentamiento': {'metricas': {'actualizacion': {'exitos': 0}}},
                    'medicion': {'metricas': {'actualizacion': {'exitos': 0}}}}
        if diagnostic:
            for phase in ('calentamiento', 'medicion'):
                measured[phase]['metricas'] = {op: {'intentos': 1, 'exitos': 1} for op in provision.runner.OPS}
        def probe(port, diagnostics):
            diagnostics.update(resultado='OK', intentos=1, errores={})
        def execute(*args, **kwargs):
            if server_stats: calls.append(([], 'HTTP_EJECUTADO'))
            return measured
        with patch.object(provision, 'command', side_effect=command), patch.object(provision, 'wait_http', side_effect=probe), patch.object(provision.runner, 'execute', side_effect=execute), contextlib.redirect_stdout(io.StringIO()):
            options = {'diagnostic': diagnostic}
            if db_probe:
                options['db_probe'] = True
            if api_workers == 2:
                options['api_workers'] = 2
            if server_stats:
                options['server_stats'] = True
            if preflight is not None:
                options['preflight'] = preflight
            result = provision.run(repo, 'smoke', 'docker', **options)
        folder = next((repo / '.pgdata').iterdir())
        report = json.loads((folder / 'report.json').read_text(encoding='utf-8'))
        for path in folder.iterdir():
            content = path.read_text(encoding='utf-8')
            self.assertTrue(all(password not in content for password in sent_passwords))
        return result, report, calls

    def test_db_probe_is_opt_in_and_retained_before_shutdown(self):
        result, report, calls = self.simulate(diagnostic=True, db_probe=True)
        self.assertEqual(result, 0)
        self.assertEqual(report['sondeo_db']['grupos']['concurrente']['muestras'], 50)
        stages = [stage for _, stage in calls]
        self.assertLess(stages.index('VERIFICACION_SQL'), stages.index('SONDEO_DB'))
        self.assertLess(stages.index('SONDEO_DB'), stages.index('PARADA_QA'))
        self.assertTrue(report['contenedores_detenidos'])

    def test_db_probe_failure_keeps_http_sql_and_stops_resources(self):
        result, report, calls = self.simulate(fail_stage='SONDEO_DB', diagnostic=True, db_probe=True)
        self.assertEqual(result, 1)
        self.assertEqual(report['estado'], 'INCOMPLETA')
        self.assertEqual(report['error_codigo'], 'SONDEO_DB_SALIDA_1')
        self.assertIn('http', report)
        self.assertIn('comprobacion_sql', report)
        self.assertTrue(report['contenedores_detenidos'])

    def test_server_statistics_are_between_seed_and_probe_with_numeric_report_only(self):
        result, report, calls = self.simulate(diagnostic=True, db_probe=True, server_stats=True)
        self.assertEqual(result, 0)
        self.assertEqual(report['servidor_sql']['totales']['calls'], 2)
        stages = [stage for _, stage in calls]
        for before, after in [('FIXTURE','SQL_STATS_ANTES'), ('SQL_STATS_ANTES','HTTP_EJECUTADO'),
                ('VERIFICACION_SQL','SQL_STATS_DESPUES'), ('SQL_STATS_DESPUES','SONDEO_DB'), ('SONDEO_DB','PARADA_QA')]:
            self.assertLess(stages.index(before), stages.index(after))
        self.assertTrue(report['contenedores_detenidos'])
        self.assertNotIn('key', report['servidor_sql'])

    def test_server_statistics_failure_preserves_http_sql_and_stops_owned_resources(self):
        for stage in ('SQL_STATS_ANTES', 'SQL_STATS_DESPUES'):
            with self.subTest(stage=stage):
                result, report, calls = self.simulate(fail_stage=stage, diagnostic=True, server_stats=True)
                self.assertEqual(result, 1)
                self.assertTrue(report['contenedores_detenidos'])
                self.assertEqual(report['error_codigo'], stage + '_SALIDA_1')
                if stage == 'SQL_STATS_DESPUES':
                    self.assertIn('http', report); self.assertIn('comprobacion_sql', report)
                else:
                    self.assertNotIn('http', report)

    def test_two_workers_smoke_checks_real_container_command_and_stops(self):
        result, report, calls = self.simulate(api_workers=2)
        self.assertEqual(result, 0)
        self.assertEqual(report['api_workers_declarados'], 2)
        self.assertTrue(report['comando_api_workers_verificado'])
        self.assertFalse(report['instrumentacion_diagnostica'])
        self.assertTrue(report['contenedores_detenidos'])
        stages = [stage for _, stage in calls]
        self.assertLess(stages.index('COMANDO_API_WORKERS'), stages.index('MIGRACIONES'))
        self.assertNotIn('SQL_STATS_ANTES', stages)
        self.assertNotIn('DIAGNOSTICO_LOG', stages)

    def test_two_workers_command_failure_stops_before_migration(self):
        result, report, calls = self.simulate(api_workers=2, fail_stage='COMANDO_API_WORKERS')
        self.assertEqual(result, 1)
        self.assertTrue(report['contenedores_detenidos'])
        self.assertNotIn('http', report)
        self.assertFalse(any(stage == 'MIGRACIONES' for _, stage in calls))

    def test_report_retains_supplied_preflight_without_changing_verdict(self):
        preflight = {'cpu_previa': {'media_cpu_global_porcentaje': 15},
                     'redes_qa_liberadas': ['one', 'two']}
        result, report, calls = self.simulate(preflight=preflight)
        self.assertEqual(result, 0)
        self.assertEqual(report['precondiciones_arranque'], preflight)
        self.assertEqual(report['estado'], 'SMOKE_SIN_ACREDITAR_RNF2')

    def test_orchestration_stops_only_generated_project_and_keeps_report_private(self):
        result, report, calls = self.simulate()
        self.assertEqual(result, 0)
        self.assertTrue(report['contenedores_detenidos'])
        self.assertEqual(report['comprobacion_sql']['entregas_encoladas'], 1000)
        self.assertTrue(any(stage == 'PARADA_QA' for _, stage in calls))
        self.assertFalse(any('down' in argv or 'rm' in argv for argv, _ in calls))

    def test_diagnostic_collects_only_after_stop_and_uses_distinct_verdict(self):
        result, report, calls = self.simulate(diagnostic=True)
        self.assertEqual(result, 0)
        self.assertEqual(report['estado'], 'DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2')
        self.assertEqual(len(report['diagnostico']['grupos']), 8)
        stages = [stage for _, stage in calls]
        self.assertLess(stages.index('PARADA_QA'), stages.index('DIAGNOSTICO_LOG'))

    def test_diagnostic_log_failure_cannot_pass(self):
        result, report, calls = self.simulate(diagnostic=True, fail_stage='DIAGNOSTICO_LOG')
        self.assertEqual(result, 1)
        self.assertEqual(report['estado'], 'INCOMPLETA_DIAGNOSTICO')
        self.assertTrue(report['contenedores_detenidos'])

    def test_diagnostic_stop_failure_does_not_read_live_logs(self):
        result, report, calls = self.simulate(diagnostic=True, fail_stage='PARADA_QA')
        self.assertEqual(result, 1)
        self.assertFalse(any(stage == 'DIAGNOSTICO_LOG' for _, stage in calls))

    def test_fixture_failure_retains_report_and_stops_qa(self):
        result, report, calls = self.simulate(fail_stage='FIXTURE')
        self.assertEqual(result, 1)
        self.assertEqual(report['estado'], 'INCOMPLETA')
        self.assertTrue(report['contenedores_detenidos'])

    def test_remote_context_is_rejected_before_creating_containers(self):
        result, report, calls = self.simulate(endpoint='ssh://example.invalid')
        self.assertEqual(result, 1)
        self.assertFalse(any(stage == 'ARRANQUE_QA' for _, stage in calls))
        self.assertFalse(report['recursos_iniciados'])

    def test_stop_failure_cannot_return_success(self):
        result, report, calls = self.simulate(fail_stage='PARADA_QA')
        self.assertEqual(result, 1)
        self.assertEqual(report['estado'], 'INCOMPLETA_PARADA_QA')
        self.assertTrue(report['parada_requiere_revision'])

    def test_data_services_cannot_join_entry_network(self):
        config = normalized(provision.specification(Path.cwd(), 'qa123456', 18080))
        config['services']['postgres']['networks'] = {'default': {}, 'entry': {}}
        with self.assertRaisesRegex(provision.ProvisionError, 'DATOS_EN_RED_ENTRADA'):
            provision.validate_resolved(config, 'plurione-qa-perf-qa123456', 18080, Path.cwd())

    def test_http_probe_retries_only_health_reads(self):
        with patch.object(provision.runner, 'Client') as client, patch.object(provision.time, 'sleep'):
            client.return_value.request.side_effect = [ConnectionRefusedError(),
                                                       (200, {'status': 'ok'}), (200, {'status': 'ok'})]
            diagnostics = {}
            provision.wait_http(18080, diagnostics)
            self.assertEqual(diagnostics['intentos'], 2)
            self.assertEqual(diagnostics['errores'], {'ConnectionRefusedError': 1})
            self.assertEqual(diagnostics['resultado'], 'OK')
            self.assertEqual([call.args for call in client.return_value.request.call_args_list],
                             [('GET', '/health'), ('GET', '/health'), ('GET', '/health/db')])

    def test_http_probe_timeout_reports_failure(self):
        with patch.object(provision.time, 'perf_counter', side_effect=[0, 31]):
            diagnostics = {}
            with self.assertRaisesRegex(provision.ProvisionError, 'API_QA_NO_ACCESIBLE_DESDE_HOST'):
                provision.wait_http(18080, diagnostics, timeout=30)
            self.assertEqual(diagnostics['resultado'], 'NO_ACCESIBLE')


if __name__ == '__main__':
    unittest.main()
