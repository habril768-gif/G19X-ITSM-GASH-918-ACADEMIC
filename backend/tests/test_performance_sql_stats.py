"""Contadores SQL QA: privacidad, deltas y rechazo fuera de aislamiento."""
from datetime import datetime, timezone
from pathlib import Path
import copy
import json
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import performance_sql_stats as stats
import provision_performance_qa as provision
import test_performance_provisioner as fixtures


class SQLStatsTests(unittest.TestCase):
    def env(self):
        return dict(QA_PERF_DIAGNOSTIC_RUN_ID='qa123456', QA_PERF_SQL_STATS='true',
            POSTGRES_HOST='postgres', POSTGRES_DB='plurione_test_perf_qa123456',
            POSTGRES_USER='qa_perf_qa123456', AI_ENABLED='false', MAIL_ENABLED='false')

    def sample(self, calls=10, elapsed=5):
        return dict(version=1, run_id='qa123456', dealloc=0, reset='2026-10-29T12:00:00+00:00',
            rows=[dict(key='123', family='SELECT/users', calls=calls, exec_ms=elapsed, rows=calls, since='2026-10-29T12:00:00+00:00')])

    def test_exact_environment_guard_and_no_arbitrary_sql_payload(self):
        payload = dict(action='before', run_id='qa123456')
        self.assertEqual(stats.guard(payload, self.env()), 'qa123456')
        for key, value in [('POSTGRES_DB', 'plurione'), ('POSTGRES_USER', 'operator'),
                ('POSTGRES_HOST', 'localhost'), ('QA_PERF_SQL_STATS', 'false'),
                ('QA_PERF_DIAGNOSTIC_RUN_ID', 'wrong123'), ('AI_ENABLED', 'true'), ('MAIL_ENABLED', 'true')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                stats.guard(payload, dict(self.env(), **{key: value}))
        for invalid in ([], None, dict(payload, sql='PRIVATE'), dict(payload, action='reset'), dict(payload, run_id='../wrong')):
            with self.assertRaises(ValueError): stats.guard(invalid, self.env())

    def test_family_discards_values_comments_and_private_names(self):
        self.assertEqual(stats.family("SELECT * FROM users WHERE email='PRIVATE' /* FROM mail_deliveries */"), 'SELECT/users')
        self.assertEqual(stats.family('SELECT pg_advisory_xact_lock_shared($1)'), 'SELECT/advisory_lock')
        self.assertEqual(stats.family('INSERT INTO mail_deliveries VALUES ($1)'), 'INSERT/mail_deliveries')
        self.assertEqual(stats.family('SELECT * FROM private_table'), 'SELECT/other')
        self.assertIsNone(stats.family('SELECT * FROM pg_stat_statements'))
        self.assertIsNone(stats.family('SELECT current_database(), current_user'))
        for value in (None, '', '<insufficient privilege>'):
            with self.assertRaises(ValueError): stats.family(value)

    def test_snapshot_filters_introspection_without_leaking_query(self):
        class Connection:
            def exec_driver_sql(self, sql): self.sql = sql; return self
            def one(self): return (0, datetime(2026, 10, 29, tzinfo=timezone.utc))
            def all(self): return [(123, "SELECT * FROM users WHERE email='PRIVATE'", 10, 5, 10, datetime(2026, 10, 29, tzinfo=timezone.utc)),
                                  (456, 'SELECT * FROM pg_stat_statements', 1, .1, 1, datetime(2026, 10, 29, tzinfo=timezone.utc))]
        snapshot = stats.snapshot(Connection(), 'qa123456')
        self.assertEqual(len(snapshot['rows']), 1)
        self.assertEqual(snapshot['rows'][0]['family'], 'SELECT/users')
        self.assertNotIn('PRIVATE', json.dumps(snapshot))
        self.assertNotIn('SELECT *', json.dumps(snapshot))

    def test_deltas_remove_seed_and_compute_weighted_server_mean(self):
        before = self.sample(10, 5); after = self.sample(12, 6)
        after['rows'].append(dict(key='789', family='SELECT/users', calls=3, exec_ms=3, rows=3, since='2026-10-29T12:00:00+00:00'))
        result = stats.difference(before, after, 'qa123456')
        self.assertEqual(result['familias']['SELECT/users'], dict(calls=5, exec_ms=4, rows=5, exec_ms_per_call=.8))
        self.assertEqual(result['totales']['calls'], 5)
        self.assertNotIn('key', json.dumps(result))
        self.assertNotIn('p95', result['familias']['SELECT/users'])

    def test_rejects_reset_eviction_decreasing_and_changed_counters(self):
        for mutate in (lambda x:x.update(reset='2026-10-29T13:00:00+00:00'), lambda x:x.update(dealloc=1),
                lambda x:x.update(rows=[]), lambda x:x['rows'][0].update(calls=9), lambda x:x['rows'][0].update(since='2026-10-29T13:00:00+00:00'),
                lambda x:x['rows'][0].update(exec_ms=4), lambda x:x['rows'][0].update(family='SELECT/roles'),
                lambda x:x['rows'][0].update(calls=10, exec_ms=6)):
            after = self.sample(12, 6); mutate(after)
            with self.assertRaises(ValueError): stats.difference(self.sample(), after, 'qa123456')

    def test_rejects_foreign_rows_private_fields_nan_and_duplicate_identity(self):
        for mutate in (lambda x:x.update(run_id='wrong123'), lambda x:x.update(query='PRIVATE'),
                lambda x:x['rows'][0].update(query='PRIVATE'), lambda x:x['rows'][0].update(key='PRIVATE'),
                lambda x:x['rows'][0].update(family='SELECT/private_table'),
                lambda x:x['rows'][0].update(exec_ms=float('nan')), lambda x:x['rows'][0].update(calls=True),
                lambda x:x['rows'].append(copy.deepcopy(x['rows'][0]))):
            sample = self.sample(); mutate(sample)
            with self.assertRaises(ValueError): stats.validate_snapshot(sample, 'qa123456')

    def test_empty_delta_is_not_reported_as_success(self):
        with self.assertRaisesRegex(ValueError, 'SIN_LLAMADAS'):
            stats.difference(self.sample(), self.sample(), 'qa123456')

    def test_opt_in_configuration_leaves_normal_and_full_path_unchanged(self):
        repo = Path.cwd()
        normal = provision.specification(repo, 'qa123456', 18080)
        self.assertNotIn('command', normal['services']['postgres'])
        self.assertNotIn('QA_PERF_SQL_STATS', normal['services']['api']['environment'])
        config = provision.specification(repo, 'qa123456', 18080, diagnostic=True, server_stats=True)
        self.assertEqual(config['services']['postgres']['command'], stats.PG_COMMAND)
        provision.validate_resolved(fixtures.normalized(config), 'plurione-qa-perf-qa123456', 18080, repo)
        for mode, diagnostic in (('full', True), ('smoke', False)):
            with self.assertRaisesRegex(provision.ProvisionError, 'SOLO'):
                provision.run(repo, mode, 'docker', diagnostic=diagnostic, server_stats=True)

    def test_configuration_rejects_marker_without_diagnostic_and_arbitrary_pg_command(self):
        repo = Path.cwd()
        valid = fixtures.normalized(provision.specification(repo, 'qa123456', 18080, diagnostic=True, server_stats=True))
        for mutate in (lambda c:c['services']['postgres'].update(command=['postgres', '-c', 'fsync=off']),
                lambda c:c['services']['api']['environment'].update(QA_PERF_SQL_STATS='yes'),
                lambda c:c['services']['api']['environment'].pop('QA_PERF_DIAGNOSTIC_RUN_ID')):
            config = copy.deepcopy(valid); mutate(config)
            with self.assertRaises(provision.ProvisionError):
                provision.validate_resolved(config, 'plurione-qa-perf-qa123456', 18080, repo)
