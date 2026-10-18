"""Servidor PostgreSQL temporal: migrar, comprobar, probar y retirar recursos propios."""
import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
from test_support import validate_test_database


def find_bin(explicit=None):
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    elif os.name == 'nt':
        root = Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'PostgreSQL'
        if root.is_dir():
            candidates.extend(p / 'bin' for p in sorted(root.iterdir(), key=lambda p: p.name, reverse=True) if p.is_dir())
    else:
        executable = shutil.which('initdb')
        if executable:
            candidates.append(Path(executable).parent)
    suffix = '.exe' if os.name == 'nt' else ''
    for candidate in candidates:
        if all((candidate / (name + suffix)).is_file() for name in ('initdb', 'pg_ctl', 'createdb', 'postgres')):
            return candidate.resolve(), suffix
    raise RuntimeError('No se encontraron binarios PostgreSQL. Indica --pg-bin con su carpeta bin.')


def run(command, environment, quiet=False):
    result = subprocess.run(command, cwd=BACKEND, env=environment,
                            stdout=subprocess.DEVNULL if quiet else sys.stdout, stderr=subprocess.DEVNULL if quiet else sys.stderr,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    if result.returncode:
        # No se vuelcan entorno, comandos, archivos de contraseña ni logs de servidor.
        raise RuntimeError('Falló una etapa de prueba: ' + Path(str(command[0])).name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pg-bin', help='Carpeta de binarios PostgreSQL; detección automática en Windows')
    args = parser.parse_args()
    folder = None; started = False; stopped = True; exit_code = 0
    try:
        pg_bin, suffix = find_bin(args.pg_bin)
        version = subprocess.run([str(pg_bin / ('postgres' + suffix)), '--version'], capture_output=True, text=True, check=True)
        print(version.stdout.strip(), flush=True)
        root = (BACKEND.parent / '.pgdata').resolve(); root.mkdir(exist_ok=True)
        folder = Path(tempfile.mkdtemp(prefix='run-', dir=root)).resolve()
        (folder / 'isolated-test-run').write_text(folder.name, encoding='utf-8')
        data = folder / 'data'; password_file = folder / 'password'
        password = secrets.token_urlsafe(32)
        password_file.write_text(password + '\n', encoding='utf-8'); password_file.chmod(0o600)
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0)); port = listener.getsockname()[1]
        environment = os.environ.copy()
        environment.update(POSTGRES_HOST='127.0.0.1', POSTGRES_PORT=str(port), POSTGRES_USER='plurione_test_owner',
                           POSTGRES_PASSWORD=password, POSTGRES_DB='plurione_test_' + secrets.token_hex(6), RUN_DB_TESTS='1',
                           PGPASSWORD=password, PGCONNECT_TIMEOUT='5', PYTHONIOENCODING='utf-8')
        validate_test_database(environment)
        print('Inicializando un servidor nuevo sin conexión a la base de desarrollo…', flush=True)
        run([str(pg_bin / ('initdb' + suffix)), '-D', str(data), '-U', environment['POSTGRES_USER'],
             '--pwfile=' + str(password_file), '--encoding=UTF8', '--locale=C', '--auth-host=scram-sha-256', '--auth-local=scram-sha-256'], environment, quiet=True)
        password_file.unlink()
        # Se marca antes del arranque para intentar detener incluso un inicio parcial.
        started = True; stopped = False
        run([str(pg_bin / ('pg_ctl' + suffix)), '-D', str(data), '-l', str(folder / 'server.log'),
             '-o', '-h 127.0.0.1 -p ' + str(port), '-w', '-t', '30', 'start'], environment, quiet=True)
        run([str(pg_bin / ('createdb' + suffix)), '-h', '127.0.0.1', '-p', str(port), '-U', environment['POSTGRES_USER'], environment['POSTGRES_DB']], environment, quiet=True)
        for arguments in (['-m', 'alembic', 'upgrade', 'head'], ['-m', 'alembic', 'upgrade', 'head'], ['-m', 'alembic', 'check'],
                          ['-m', 'pytest', 'tests', '-q', '-o', 'faulthandler_timeout=30', '--junitxml=' + str(folder / 'results.xml')]):
            print('Ejecutando ' + ' '.join(arguments[1:]) + '…', flush=True)
            run([sys.executable, *arguments], environment)
        suites = ET.parse(folder / 'results.xml').getroot().findall('testsuite')
        totals = {key: sum(int(suite.attrib.get(key, 0)) for suite in suites) for key in ('tests', 'failures', 'errors', 'skipped')}
        if not suites or totals['tests'] == 0 or any(totals[key] for key in ('failures', 'errors', 'skipped')):
            raise RuntimeError('La ejecución aislada requiere pruebas ejecutadas sin fallos, errores ni omisiones')
        print('Resultado PostgreSQL aislado: ' + json.dumps(totals), flush=True)
    except (RuntimeError, OSError, subprocess.SubprocessError):
        print('No se completó la ejecución aislada. Revisa la última etapa mostrada; no se utilizó la base de desarrollo.', file=sys.stderr, flush=True)
        exit_code = 1
    finally:
        if started:
            try:
                run([str(pg_bin / ('pg_ctl' + suffix)), '-D', str(data), '-m', 'fast', '-w', '-t', '30', 'stop'], environment, quiet=True)
                stopped = True
            except (RuntimeError, OSError):
                print('No se confirmó la parada del servidor de pruebas; se conserva su carpeta temporal.', file=sys.stderr)
                exit_code = 1
        if folder and stopped:
            root = (BACKEND.parent / '.pgdata').resolve()
            # La eliminación solo alcanza la carpeta propia validada dentro de .pgdata.
            if folder.parent == root and folder.name.startswith('run-') and (folder / 'isolated-test-run').read_text(encoding='utf-8') == folder.name:
                shutil.rmtree(folder)
                print('Servidor temporal detenido y archivos propios retirados.', flush=True)
            else:
                print('No se eliminó una ruta que no pudo verificarse.', file=sys.stderr); exit_code = 1
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
