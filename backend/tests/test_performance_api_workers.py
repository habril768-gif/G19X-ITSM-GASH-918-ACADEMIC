"""Comparación QA de procesos API: configuración explícita y guardas."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import provision_performance_qa as provision
import test_performance_provisioner as fixtures


class APIWorkersTests(unittest.TestCase):
    def test_only_integer_one_two_or_three_is_accepted(self):
        for value in (0, -1, 4, True, False, 1.0, '2', None):
            with self.subTest(value=value), self.assertRaises(provision.ProvisionError):
                provision.validate_workers(value)
        provision.validate_workers(1, True, 'smoke')
        provision.validate_workers(1, False, 'full')
        provision.validate_workers(2, False, 'smoke')
        provision.validate_workers(2, False, 'full')

    def test_two_only_changes_api_in_new_smoke_config(self):
        repo = Path.cwd()
        original = provision.specification(repo, 'qa123456', 18080)
        candidate = provision.specification(repo, 'qa123456', 18080, api_workers=2)
        self.assertEqual(candidate['services']['api']['command'], provision.workers_command())
        self.assertEqual(candidate['services']['api']['environment']['QA_PERF_API_WORKERS'], '2')
        self.assertEqual(candidate['services']['postgres'], original['services']['postgres'])
        self.assertEqual(candidate['services']['redis'], original['services']['redis'])
        self.assertEqual(candidate['volumes'], original['volumes'])
        self.assertEqual(provision.specification(repo, 'qa123456', 18080), original)
        self.assertNotIn('command', original['services']['api'])
        self.assertNotIn('QA_PERF_DIAGNOSTIC_RUN_ID', candidate['services']['api']['environment'])
        provision.validate_resolved(fixtures.normalized(candidate), 'plurione-qa-perf-qa123456', 18080, repo)

    def test_diagnostic_and_invalid_modes_reject_before_creation(self):
        for mode, diagnostic in (('invalid',False), ('full',True), ('smoke',True)):
            with self.subTest(mode=mode,diagnostic=diagnostic), self.assertRaises(provision.ProvisionError):
                provision.run(Path.cwd(), mode, 'docker', diagnostic=diagnostic, api_workers=2)
        with self.assertRaises(provision.ProvisionError):
            provision.specification(Path.cwd(), 'qa123456', 18080, diagnostic=True, api_workers=2)

    def test_marker_and_command_cannot_select_other_entrypoint_or_count(self):
        repo = Path.cwd()
        source = fixtures.normalized(provision.specification(repo, 'qa123456', 18080, api_workers=2))
        for mutate in (lambda c:c['services']['api']['command'].__setitem__(-1,'4'),
                lambda c:c['services']['api']['command'].__setitem__(3,'app.core.performance_diagnostics:app'),
                lambda c:c['services']['api']['environment'].pop('QA_PERF_API_WORKERS'),
                lambda c:c['services']['api']['environment'].update(QA_PERF_API_WORKERS='4'),
                lambda c:c['services']['api']['environment'].update(QA_PERF_DIAGNOSTIC_RUN_ID='qa123456')):
            value=copy.deepcopy(source);mutate(value)
            with self.assertRaises(provision.ProvisionError):
                provision.validate_resolved(value, 'plurione-qa-perf-qa123456', 18080, repo)

    def test_cli_plan_has_two_workers_without_docker_or_diagnostic(self):
        script=Path(provision.__file__)
        result=subprocess.run([sys.executable,'-B',str(script),'--mode','smoke','--api-workers','2','--plan'],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(result.stdout)
        self.assertEqual(value['api_workers'],2)
        self.assertFalse(value['diagnostic'])
        self.assertFalse(value['server_stats'])
        self.assertEqual(value['users'],10)
        self.assertEqual(value['initial_cases'],100)

    def test_full_plan_accepts_two_without_docker_or_diagnostic(self):
        result=subprocess.run([sys.executable,'-B',str(Path(provision.__file__)),'--mode','full','--api-workers','2','--plan'],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(result.stdout)
        self.assertEqual(value['mode'],'full')
        self.assertEqual(value['api_workers'],2)
        self.assertEqual(value['users'],10)
        self.assertFalse(value['diagnostic'])

    def test_full_two_rejects_diagnostic_cli(self):
        result=subprocess.run([sys.executable,'-B',str(Path(provision.__file__)),'--mode','full','--api-workers','2','--diagnostic','--plan'],capture_output=True,text=True,timeout=20)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('API_WORKERS_SIN_DIAGNOSTICO',result.stdout)

    def test_three_uses_own_exact_command_and_rejects_mismatched_marker(self):
        repo=Path.cwd()
        source=fixtures.normalized(provision.specification(repo,'qa123456',18080,api_workers=3))
        self.assertEqual(source['services']['api']['command'][-2:],['--workers','3'])
        self.assertEqual(source['services']['api']['environment']['QA_PERF_API_WORKERS'],'3')
        provision.validate_resolved(source,'plurione-qa-perf-qa123456',18080,repo)
        source['services']['api']['environment']['QA_PERF_API_WORKERS']='2'
        with self.assertRaises(provision.ProvisionError):
            provision.validate_resolved(source,'plurione-qa-perf-qa123456',18080,repo)
        with self.assertRaises(provision.ProvisionError):
            provision.validate_workers(3,True,'full')

    def test_three_cli_full_plan(self):
        result=subprocess.run([sys.executable,'-B',str(Path(provision.__file__)),'--mode','full','--api-workers','3','--plan'],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(result.stdout)
        self.assertEqual(value['api_workers'],3)
        self.assertEqual(value['mode'],'full')
        self.assertFalse(value['diagnostic'])
