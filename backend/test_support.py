"""Guardas de ejecución de QA, sin leer archivos .env ni mostrar credenciales."""
import re


def validate_test_database(environment):
    if environment.get('RUN_DB_TESTS') != '1':
        raise RuntimeError('Las integraciones requieren RUN_DB_TESTS=1')
    if not re.fullmatch(r'plurione_test(?:_[a-z0-9_]+)?', environment.get('POSTGRES_DB', '')):
        raise RuntimeError('Solo se permiten bases dedicadas plurione_test o plurione_test_*')
    if environment.get('POSTGRES_HOST') not in {'127.0.0.1', 'localhost'}:
        raise RuntimeError('Las pruebas requieren un servidor local dedicado')
    if not environment.get('POSTGRES_PASSWORD'):
        raise RuntimeError('Falta la credencial temporal de pruebas')
