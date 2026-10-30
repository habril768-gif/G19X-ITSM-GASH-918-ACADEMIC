"""No iniciar formal ni tocar redes si las condiciones previas no se cumplen."""
import contextlib
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_performance_full_guarded as guarded


def baseline(cpus=(10, 20, 30)):
    return {'intervalos': [{'cpu_global_porcentaje': cpu, 'duracion_s': 2.0, 'estado': 'OK'} for cpu in cpus],
        'intervalos_validos': 3, 'intervalos_totales': 3, 'media_cpu_global_porcentaje': sum(cpus)/3}


class GuardedFormalTests(unittest.TestCase):
    def run_guard(self, value=None, cleanup=None, remote=False, api_workers=1):
        if value is None:
            value = baseline()
        if cleanup is None:
            cleanup = {'eliminadas': ['qa_net', 'qa_entry'], 'fallidas': [], 'omitidas_al_revalidar': []}
        def command(argv):
            if argv[1:3] == ['context', 'show']:
                return 'desktop-linux'
            return json.dumps([{'Endpoints': {'docker': {'Host': 'ssh://remote.invalid' if remote else 'npipe:////./pipe/dockerDesktopLinuxEngine'}}}])
        with patch.object(guarded.host, 'baseline', return_value=value) as sample, \
             patch.object(guarded.networks, 'command', side_effect=command) as docker, \
             patch.object(guarded.networks, 'release', return_value=cleanup) as release, \
             patch.object(guarded.provision, 'run', return_value=0) as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            if remote:
                with self.assertRaisesRegex(guarded.networks.ReleaseError, '^DOCKER_NO_LOCAL$'):
                    guarded.guarded_run(Path.cwd(), 'docker', api_workers=api_workers)
                result = None
            else:
                result = guarded.guarded_run(Path.cwd(), 'docker', api_workers=api_workers)
        return result, sample, docker, release, run, output.getvalue()

    def test_valid_quiet_baseline_is_ready(self):
        self.assertTrue(guarded.baseline_ready(baseline()))

    def test_high_cpu_does_not_touch_docker_or_networks(self):
        result, sample, docker, release, run, output = self.run_guard(baseline((60, 80, 70)))
        self.assertEqual(result, 2)
        sample.assert_called_once()
        docker.assert_not_called()
        release.assert_not_called()
        run.assert_not_called()
        self.assertEqual(json.loads(output)['estado'], 'NO_INICIADA_CPU_PREVIA')

    def test_missing_nonfinite_or_inconsistent_samples_are_not_ready(self):
        values = [baseline(), baseline(), baseline(), baseline()]
        values[0]['intervalos'][1]['cpu_global_porcentaje'] = None
        values[1]['media_cpu_global_porcentaje'] = float('nan')
        values[2]['intervalos_validos'] = 2
        values[3]['media_cpu_global_porcentaje'] = 1
        for value in values:
            with self.subTest(value=value):
                result, _, docker, release, run, _ = self.run_guard(value)
                self.assertEqual(result, 2)
                docker.assert_not_called()
                release.assert_not_called()
                run.assert_not_called()

    def test_interval_spike_blocks_even_with_acceptable_average(self):
        self.assertFalse(guarded.baseline_ready(baseline((5, 5, 70))))

    def test_remote_docker_blocks_before_cleanup(self):
        _, _, _, release, run, _ = self.run_guard(remote=True)
        release.assert_not_called()
        run.assert_not_called()

    def test_cleanup_failure_cannot_start_formal(self):
        result, _, _, _, run, output = self.run_guard(cleanup={
            'eliminadas': ['one', 'two'], 'fallidas': ['other'], 'omitidas_al_revalidar': []})
        self.assertEqual(result, 2)
        run.assert_not_called()
        self.assertEqual(json.loads(output)['estado'], 'NO_INICIADA_REDES_QA')

    def test_fewer_than_two_released_networks_cannot_start_formal(self):
        result, _, _, _, run, _ = self.run_guard(cleanup={
            'eliminadas': ['one'], 'fallidas': [], 'omitidas_al_revalidar': []})
        self.assertEqual(result, 2)
        run.assert_not_called()

    def test_success_calls_full_without_diagnostic_and_keeps_preflight(self):
        result, _, _, release, run, output = self.run_guard()
        self.assertEqual(result, 0)
        release.assert_called_once_with(Path.cwd(), ['docker', '--context', 'desktop-linux'], apply=True, limit=2)
        self.assertEqual(run.call_args.args, (Path.cwd(), 'full', 'docker'))
        self.assertNotIn('diagnostic', run.call_args.kwargs)
        preflight = run.call_args.kwargs['preflight']
        self.assertEqual(preflight['cpu_previa'], baseline())
        self.assertEqual(preflight['redes_qa_liberadas'], ['qa_net', 'qa_entry'])
        self.assertEqual(json.loads(output)['estado'], 'PRECONDICIONES_OK')

    def test_two_workers_keeps_full_protocol_and_preflight(self):
        result, _, _, release, run, output = self.run_guard(api_workers=2)
        self.assertEqual(result, 0)
        self.assertEqual(run.call_args.args, (Path.cwd(), 'full', 'docker'))
        self.assertEqual(run.call_args.kwargs['api_workers'], 2)
        self.assertNotIn('diagnostic', run.call_args.kwargs)
        self.assertEqual(json.loads(output)['api_workers_declarados'], 2)
        self.assertEqual(run.call_args.kwargs['preflight']['cpu_previa'], baseline())
        release.assert_called_once()

    def test_two_workers_does_not_bypass_high_cpu_or_failed_cleanup(self):
        for options in ({'value':baseline((60,70,80))}, {'cleanup':{'eliminadas':[], 'fallidas':[], 'omitidas_al_revalidar':[]}}):
            with self.subTest(options=options):
                result, _, _, _, run, _ = self.run_guard(api_workers=2, **options)
                self.assertEqual(result,2)
                run.assert_not_called()

    def test_invalid_workers_rejected_before_cpu_and_docker(self):
        with patch.object(guarded.host,'baseline') as sample, patch.object(guarded.networks,'command') as docker:
            with self.assertRaises(guarded.provision.ProvisionError):
                guarded.guarded_run(Path.cwd(),'docker',api_workers=4)
            sample.assert_not_called()
            docker.assert_not_called()

    def test_three_full_uses_same_guard_and_preserves_failure(self):
        result, _, _, release, run, output=self.run_guard(api_workers=3)
        self.assertEqual(result,0)
        self.assertEqual(run.call_args.args,(Path.cwd(),'full','docker'))
        self.assertEqual(run.call_args.kwargs['api_workers'],3)
        self.assertEqual(json.loads(output)['api_workers_declarados'],3)
        result, _, docker, release, run, _=self.run_guard(value=baseline((60,70,80)),api_workers=3)
        self.assertEqual(result,2)
        docker.assert_not_called()
        release.assert_not_called()
        run.assert_not_called()

    def test_confirmation_is_required_before_any_measurement(self):
        with patch.object(guarded.host, 'baseline') as sample, \
             contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            guarded.main([])
        sample.assert_not_called()


if __name__ == '__main__':
    unittest.main()
