"""Pruebas locales del generador; no constituyen carga de PluriOne."""
import importlib.util
import json
from pathlib import Path
import time
import unittest
from unittest.mock import Mock, patch
from uuid import UUID

candidate = Path(__file__).resolve().parents[1] / 'scripts/performance_runner.py'
if not candidate.exists():
    candidate = Path(__file__).with_name('performance_runner.py')
spec = importlib.util.spec_from_file_location('performance_runner', candidate)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def fixture():
    return {'scope': 'plurione-performance-isolated', 'run_id': 'qa123456',
            'base_url': 'http://127.0.0.1:18080', 'compose_project': 'plurione-qa-perf-qa123456',
            'isolated_resources_confirmed': True,
            'department_id': str(UUID(int=1000)), 'incident_date': '2026-10-21',
            'hardware': {'cpu': 'simulada'}, 'code_identity': {'ref': 'unit-test'},
            'images': {'api': 'fake'}, 'provider_queue_mode': {'mode': 'fake'},
            'users': [{'email': f'qa-perf-qa123456-{index}@example.invalid',
                       'password_env': f'PLURIONE_PERF_PASSWORD_{index}',
                       'case_ids': [str(UUID(int=1 + index * 10 + offset)) for offset in range(10)]}
                      for index in range(10)]}


class PerformanceTests(unittest.TestCase):
    def test_preflight_checks_fixture_without_mutations(self):
        config = fixture()
        calls = []
        prefix = 'QA-PERF-' + config['run_id'] + '-'
        class FakeClient:
            token = None
            def __init__(self, index): self.index = index
            def checked(self, method, path, payload=None):
                calls.append((method, path))
                if path in ('/health', '/health/db'): return {'status': 'ok'}
                if path == '/auth/login': return {'access_token': 'not-a-real-token'}
                if path == '/auth/me':
                    return {'id': str(self.index), 'email': config['users'][self.index]['email'],
                            'rol': 'ADMIN_RH', 'departamento_id': config['department_id']}
                if path.startswith('/incidents?'):
                    return {'total': 100, 'items': [{'titulo': prefix} for _ in range(100)]}
                if path.endswith('/participants'): return {'items': []}
                return {'id': path.rsplit('/', 1)[-1], 'created_by': str(self.index),
                        'reported_department_id': config['department_id'], 'scope': 'ENTORNO',
                        'status': 'PENDIENTE', 'is_confidential': False,
                        'affected_employee_id': None, 'titulo': prefix}
        with patch.dict(runner.os.environ, {f'PLURIONE_PERF_PASSWORD_{i}': 'simulated-only' for i in range(10)}):
            runner.preflight(config, [FakeClient(index) for index in range(10)])
        self.assertEqual(sum(path.endswith('/participants') for _, path in calls), 100)
        self.assertEqual([path for method, path in calls if method != 'GET'], ['/auth/login'] * 10)

    def test_invalid_create_receipt_does_not_count_as_success(self):
        class FakeClient:
            def request(self, *args):
                return 201, {'received': True, 'can_view': True, 'id': 'invalid'}
        config = fixture()
        _, status, valid, created = runner.operation(FakeClient(), config['users'][0], config, 2, 'unit')
        self.assertEqual(status, 201)
        self.assertFalse(valid)
        self.assertIsNone(created)

    def test_missing_metadata_is_rejected_before_client_creation(self):
        config = fixture()
        config['hardware'] = {}
        with patch.object(runner, 'Client') as client:
            with self.assertRaisesRegex(runner.InvalidRun, 'METADATOS_FALTANTES'):
                runner.execute(config, True)
            client.assert_not_called()

    def test_target_requires_separate_loopback_port(self):
        config = fixture()
        self.assertEqual(runner.validate_manifest(config), 18080)
        for target in ['http://127.0.0.1:8000', 'http://127.0.0.1:5173',
                       'http://example.com:18080', 'http://localhost:18080',
                       'http://name:password@127.0.0.1:18080', 'http://127.0.0.1:18080/api']:
            config['base_url'] = target
            with self.subTest(target=target), self.assertRaises(runner.InvalidRun):
                runner.validate_manifest(config)

    def test_duplicate_cases_and_non_qa_identity_rejected(self):
        config = fixture()
        config['users'][1]['case_ids'][0] = config['users'][0]['case_ids'][0]
        with self.assertRaisesRegex(runner.InvalidRun, 'CASOS_DUPLICADOS'):
            runner.validate_manifest(config)
        config = fixture()
        config['users'][0]['email'] = 'admin@plurione.local'
        with self.assertRaisesRegex(runner.InvalidRun, 'CUENTA_NO_QA'):
            runner.validate_manifest(config)

    def test_unconfirmed_isolation_rejected(self):
        config = fixture()
        config['isolated_resources_confirmed'] = False
        with self.assertRaisesRegex(runner.InvalidRun, 'AISLAMIENTO_NO_CONFIRMADO'):
            runner.validate_manifest(config)

    def test_percentile_nearest_rank_and_empty(self):
        self.assertIsNone(runner.percentile([], .95))
        self.assertEqual(runner.percentile(list(range(1, 101)), .95), 95)
        self.assertEqual(runner.percentile([200, 1, 30], .95), 200)

    def test_failure_times_not_hidden_by_success_percentile(self):
        rows = [('listado', 10, 200, True, False), ('listado', 10000, 'EXCEPTION', False, True)]
        result = runner.metrics(rows, 5)['listado']
        self.assertEqual(result['p95_exitos_ms'], 10)
        self.assertEqual(result['p95_todos_ms'], 10000)
        self.assertEqual(result['errores'], 1)
        self.assertEqual(result['tasa_error'], .5)
        self.assertEqual(result['finalizadas_fuera_ventana'], 1)

    def test_verdict_strict_threshold_smoke_and_incomplete(self):
        summary = runner.metrics([(op, 199, 200, True, False) for op in runner.OPS], 300)
        self.assertEqual(runner.verdict(summary, True, False), 'APROBADA_ALCANCE_HTTP_QA')
        self.assertEqual(runner.verdict(summary, True, True), 'SMOKE_SIN_ACREDITAR_RNF2')
        self.assertEqual(runner.verdict(summary, False, True), 'INCOMPLETA')
        summary['detalle']['p95_exitos_ms'] = 200
        self.assertEqual(runner.verdict(summary, True, False), 'FALLIDA_UMBRAL')
        summary['detalle']['errores'] = 1
        self.assertEqual(runner.verdict(summary, True, True), 'FALLIDA')

    def test_http_does_not_retry_failed_mutation(self):
        with patch.object(runner.http.client, 'HTTPConnection') as connection:
            connection.return_value.request.side_effect = TimeoutError('private body')
            client = runner.Client(18080)
            with self.assertRaises(TimeoutError):
                client.request('POST', '/incidents', {'titulo': 'fake'})
            self.assertEqual(connection.return_value.request.call_count, 1)
            self.assertTrue(connection.return_value.close.called)
            self.assertIsNone(client.connection)

    def test_ten_clients_have_samples_in_same_window(self):
        def simulated(client, account, manifest, sequence, phase):
            time.sleep(.001)
            return runner.OPS[sequence % 4], 200, True, None
        with patch.object(runner, 'operation', side_effect=simulated):
            result, rows = runner.phase_run([Mock() for _ in range(10)], fixture(), .04, 'unit')
        self.assertTrue(result['completa'])
        self.assertEqual(result['clientes'], 10)
        self.assertTrue(all(row['samples'] for row in rows))
        self.assertTrue(all(value['intentos'] for value in result['metricas'].values()))

    def test_unexpected_http_stops_phase_as_incomplete(self):
        with patch.object(runner, 'operation', return_value=('listado', 403, False, None)):
            result, _ = runner.phase_run([Mock() for _ in range(10)], fixture(), .1, 'unit')
        self.assertFalse(result['completa'])
        self.assertEqual(runner.verdict(result['metricas'], False, False), 'FALLIDA')

    def test_preflight_failure_revokes_partial_sessions_without_secret_report(self):
        class FakeClient:
            def __init__(self, port): self.token = None
            def request(self, *args): return 204, None
            def close(self): pass
        def blocked(manifest, clients):
            clients[0].token = 'DO-NOT-STORE-TOKEN'
            raise runner.InvalidRun('FIXTURE_NO_VALIDO')
        with patch.object(runner, 'Client', FakeClient), patch.object(runner, 'preflight', side_effect=blocked):
            report = runner.execute(fixture(), True)
        self.assertEqual(report['estado'], 'INCOMPLETA')
        self.assertEqual(report['revocacion_sesiones'], {'204': 1})
        self.assertNotIn('DO-NOT-STORE-TOKEN', json.dumps(report))

    def test_phase_discards_stale_connections_but_preserves_sessions(self):
        class StaleClient:
            token = 'session-fictitious'
            stale = True
            closes = 0
            def close(self):
                self.closes += 1
                self.stale = False
        clients = [StaleClient() for _ in range(10)]
        def simulated(client, account, manifest, sequence, phase):
            if client.stale:
                raise runner.http.client.RemoteDisconnected()
            self.assertEqual(client.token, 'session-fictitious')
            time.sleep(.001)
            return runner.OPS[sequence % 4], 200, True, None
        with patch.object(runner, 'operation', side_effect=simulated):
            result, _ = runner.phase_run(clients, fixture(), .04, 'unit')
        self.assertTrue(result['completa'])
        self.assertTrue(all(client.closes == 1 for client in clients))

    def test_exception_type_is_recorded_without_sensitive_message(self):
        with patch.object(runner, 'operation', side_effect=runner.http.client.RemoteDisconnected('PRIVATE-TOKEN')):
            result, _ = runner.phase_run([Mock() for _ in range(10)], fixture(), .1, 'unit')
        states = result['metricas']['listado']['estados']
        self.assertIn('EXCEPTION:RemoteDisconnected', states)
        self.assertFalse(result['completa'])
        self.assertNotIn('PRIVATE-TOKEN', json.dumps(result))

    def test_non_diagnostic_phase_records_cpu_without_enabling_api_diagnostics(self):
        class Client:
            diagnostic=False
            phase=None
            def close(self):pass
        clients=[Client() for _ in range(10)]
        def operation(client,*args):
            self.assertFalse(client.diagnostic)
            time.sleep(.001)
            return 'listado',200,True,None
        before={'wall':100.,'process':1.,'host':(100,1000)}
        after={'wall':100.05,'process':1.01,'host':(105,1020)}
        with patch.object(runner,'operation',side_effect=operation), patch.object(runner,'host_stamp',side_effect=[before,after]) as stamps:
            report,_=runner.phase_run(clients,fixture(),.04,'unit')
        self.assertTrue(report['completa'])
        self.assertEqual(stamps.call_count,2)
        self.assertEqual(report['cpu_generador_host']['host_cpu_porcentaje'],75.)
        self.assertEqual(report['cpu_generador_host']['host_estado'],'OK')
        self.assertTrue(all(not c.diagnostic and c.phase is None for c in clients))

    def test_non_diagnostic_phase_preserves_unavailable_host_as_null(self):
        class Client:
            diagnostic=False
            def close(self):pass
        def operation(*args):
            time.sleep(.001)
            return 'listado',200,True,None
        before={'wall':10.,'process':1.,'host':None}
        after={'wall':10.05,'process':1.01,'host':None}
        with patch.object(runner,'operation',side_effect=operation),patch.object(runner,'host_stamp',side_effect=[before,after]):
            report,_=runner.phase_run([Client() for _ in range(10)],fixture(),.04,'unit')
        self.assertTrue(report['completa'])
        self.assertIsNone(report['cpu_generador_host']['host_cpu_porcentaje'])
        self.assertEqual(report['cpu_generador_host']['host_estado'],'NO_DISPONIBLE')


if __name__ == '__main__':
    unittest.main()
