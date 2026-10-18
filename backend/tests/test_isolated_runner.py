"""Guardas y retirada de recursos del ejecutor, sin lanzar servidores en pruebas unitarias."""
import os
from pathlib import Path
from types import SimpleNamespace
import pytest
from test_support import validate_test_database
from scripts import test_postgres_isolated as runner

ENVIRONMENT = {'RUN_DB_TESTS': '1', 'POSTGRES_DB': 'plurione_test', 'POSTGRES_HOST': '127.0.0.1', 'POSTGRES_PASSWORD': 'test-only'}


@pytest.mark.parametrize('change', [
    {'RUN_DB_TESTS': '0'}, {'POSTGRES_DB': 'plurione'}, {'POSTGRES_DB': 'plurione_test_;drop'},
    {'POSTGRES_HOST': 'remote.example.invalid'}, {'POSTGRES_PASSWORD': ''},
])
def test_guard_rejects_unsafe_targets(change):
    with pytest.raises(RuntimeError): validate_test_database({**ENVIRONMENT, **change})


def test_guard_accepts_dedicated_ci_and_generated_names():
    validate_test_database(ENVIRONMENT)
    validate_test_database({**ENVIRONMENT, 'POSTGRES_DB': 'plurione_test_a123'})


@pytest.mark.parametrize('stop_fails', [False, True])
def test_failed_migration_stops_only_own_server_and_preserves_parent_environment(tmp_path, monkeypatch, stop_fails):
    backend = tmp_path / 'project' / 'backend'; backend.mkdir(parents=True)
    pg_bin = tmp_path / 'bin'; pg_bin.mkdir()
    monkeypatch.setattr(runner, 'BACKEND', backend)
    monkeypatch.setattr(runner, 'find_bin', lambda *_: (pg_bin, ''))
    monkeypatch.setattr(runner.sys, 'argv', ['runner'])
    monkeypatch.setenv('POSTGRES_DB', 'plurione')
    calls = []
    def fake(command, **kwargs):
        if '--version' in command: return SimpleNamespace(returncode=0, stdout='postgres QA')
        environment = kwargs['env']; validate_test_database(environment)
        assert environment['POSTGRES_DB'] != 'plurione'
        calls.append(list(command))
        return SimpleNamespace(returncode=1 if ('alembic' in command or (stop_fails and command[-1] == 'stop')) else 0)
    monkeypatch.setattr(runner.subprocess, 'run', fake)
    assert runner.main() == 1
    assert any(command[-1] == 'stop' for command in calls)
    assert os.environ['POSTGRES_DB'] == 'plurione'
    leftovers = list((backend.parent / '.pgdata').iterdir())
    assert bool(leftovers) is stop_fails
    if leftovers:
        assert leftovers[0].parent == (backend.parent / '.pgdata').resolve()
        assert (leftovers[0] / 'isolated-test-run').is_file()
