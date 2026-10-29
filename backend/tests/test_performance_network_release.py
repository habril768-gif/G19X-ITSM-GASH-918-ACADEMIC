"""Limpieza acotada: propiedad, uso, revalidación y límite; Docker simulado."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import release_performance_networks as release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.run_id = '1234567890abcdef'
        self.project = 'plurione-qa-perf-' + self.run_id
        folder = self.repo / '.pgdata' / ('performance-' + self.run_id)
        folder.mkdir(parents=True)
        (folder / 'report.json').write_text(json.dumps({'run_id': self.run_id,
            'recursos_retenidos': {'project': self.project}}), encoding='utf-8')
        (folder / 'compose.json').write_text(json.dumps({'name': self.project, 'networks': {
            'default': {'name': self.project + '_net'}, 'entry': {'name': self.project + '_entry'}}}), encoding='utf-8')
        self.network = {'Name': self.project + '_net', 'Id': 'a' * 64,
            'Labels': {'com.docker.compose.project': self.project, 'com.docker.compose.network': 'default'},
            'Driver': 'bridge', 'Scope': 'local', 'Internal': True, 'Containers': {}}

    def test_own_recorded_empty_network_is_eligible(self):
        self.assertTrue(release.eligible(self.network, self.repo))
        entry = copy.deepcopy(self.network)
        entry.update(Name=self.project + '_entry', Internal=False)
        entry['Labels']['com.docker.compose.network'] = 'entry'
        self.assertTrue(release.eligible(entry, self.repo))

    def test_rejects_connected_missing_or_nonlocal_metadata(self):
        for changes in ({'Containers': {'container': {}}}, {'Containers': None},
                        {'Driver': 'overlay'}, {'Scope': 'swarm'}, {'Ingress': True},
                        {'Internal': False}, {'Name': 'plurione_default'}, {'Id': 'bad'},
                        {'Labels': {}}, {'ConfigOnly': True}):
            with self.subTest(changes=changes):
                self.assertFalse(release.eligible(dict(self.network, **changes), self.repo))
        missing = dict(self.network)
        del missing['Containers']
        self.assertFalse(release.eligible(missing, self.repo))

    def test_rejects_unrecorded_project_and_mismatched_manifest(self):
        self.assertFalse(release.eligible(self.network, self.repo / 'unknown'))
        folder = self.repo / '.pgdata' / ('performance-' + self.run_id)
        (folder / 'compose.json').write_text('{}', encoding='utf-8')
        self.assertFalse(release.eligible(self.network, self.repo))

    def simulate(self, *, apply=False, changed=False, fail=False, limit=2):
        calls = []
        def command(argv):
            calls.append(argv)
            if argv[2] == 'ls':
                return 'a b'
            if argv[2] == 'inspect':
                value = copy.deepcopy(self.network)
                if argv[-1] == 'b':
                    value.update(Name=self.project + '_entry', Id='b' * 64, Internal=False)
                    value['Labels']['com.docker.compose.network'] = 'entry'
                if len(argv[-1]) == 64:
                    if argv[-1].startswith('b'):
                        value.update(Name=self.project + '_entry', Id='b' * 64, Internal=False)
                        value['Labels']['com.docker.compose.network'] = 'entry'
                    if changed:
                        value['Containers'] = {'connected': {}}
                return json.dumps([value])
            if argv[2] == 'rm':
                if fail:
                    raise release.ReleaseError('DOCKER_SALIDA_1')
                return argv[-1]
            raise AssertionError(argv)
        with patch.object(release, 'command', side_effect=command):
            result = release.release(self.repo, ['docker'], apply=apply, limit=limit)
        self.assertTrue(all(call[1:3] in (['network', 'ls'], ['network', 'inspect'], ['network', 'rm']) for call in calls))
        return result, calls

    def test_default_only_reviews(self):
        result, calls = self.simulate()
        self.assertEqual(len(result['redes_elegibles']), 2)
        self.assertEqual(result['eliminadas'], [])
        self.assertFalse(any('rm' in call for call in calls))

    def test_apply_limits_deletion_and_uses_full_id(self):
        result, calls = self.simulate(apply=True, limit=1)
        self.assertEqual(len(result['eliminadas']), 1)
        removals = [call for call in calls if 'rm' in call]
        self.assertEqual(len(removals), 1)
        self.assertEqual(len(removals[0][-1]), 64)

    def test_revalidation_skips_network_that_gained_container(self):
        result, calls = self.simulate(apply=True, changed=True)
        self.assertEqual(len(result['omitidas_al_revalidar']), 2)
        self.assertFalse(any('rm' in call for call in calls))

    def test_daemon_failure_does_not_report_removal(self):
        result, calls = self.simulate(apply=True, fail=True)
        self.assertEqual(result['eliminadas'], [])
        self.assertEqual(len(result['fallidas']), 2)


if __name__ == '__main__':
    unittest.main()
