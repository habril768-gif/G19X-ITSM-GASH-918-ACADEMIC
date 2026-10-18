"""Impide activar integraciones accidentalmente contra la base de desarrollo."""
import os
import pytest
from test_support import validate_test_database


def pytest_sessionstart(session):
    if os.environ.get('RUN_DB_TESTS') == '1':
        try:
            validate_test_database(os.environ)
        except RuntimeError as exc:
            raise pytest.UsageError(str(exc)) from None
