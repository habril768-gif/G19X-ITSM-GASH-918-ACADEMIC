"""Libera solo redes vacías de corridas QA registradas; no toca datos ni contenedores."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

from provision_performance_qa import local_endpoint


class ReleaseError(Exception):
    pass


def command(argv):
    try:
        result = subprocess.run(argv, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        raise ReleaseError('DOCKER_NO_COMPLETADO') from None
    if result.returncode:
        raise ReleaseError('DOCKER_SALIDA_' + str(result.returncode))
    return result.stdout


def eligible(network, repo):
    """Exige nombre, etiquetas, reporte y configuración originales concordantes."""
    match = re.fullmatch(r'plurione-qa-perf-([0-9a-f]{16})_(net|entry)', network.get('Name', ''))
    if not match or not re.fullmatch(r'[0-9a-f]{64}', network.get('Id', '')):
        return False
    run_id, kind = match.groups()
    project = 'plurione-qa-perf-' + run_id
    labels = network.get('Labels') or {}
    key = 'default' if kind == 'net' else 'entry'
    if (labels.get('com.docker.compose.project') != project
            or labels.get('com.docker.compose.network') != key
            or network.get('Driver') != 'bridge' or network.get('Scope') != 'local'
            or network.get('Internal') is not (kind == 'net')
            or network.get('Ingress') or network.get('ConfigOnly')
            or not isinstance(network.get('Containers'), dict) or network['Containers']):
        return False
    folder = repo / '.pgdata' / ('performance-' + run_id)
    try:
        report = json.loads((folder / 'report.json').read_text(encoding='utf-8'))
        config = json.loads((folder / 'compose.json').read_text(encoding='utf-8'))
        return (report['run_id'] == run_id and config['name'] == project
                and report['recursos_retenidos']['project'] == project
                and config['networks'][key]['name'] == network['Name'])
    except (OSError, ValueError, KeyError, TypeError):
        return False


def release(repo, docker, *, apply=False, limit=2):
    # Solo candidatos con etiquetas Compose; no hay prune global.
    ids = command(docker + ['network', 'ls', '--filter', 'label=com.docker.compose.project',
                            '--format', '{{.ID}}']).split()
    candidates = []
    for identity in ids:
        rows = json.loads(command(docker + ['network', 'inspect', identity]))
        if len(rows) == 1 and eligible(rows[0], repo):
            candidates.append(rows[0])
    candidates.sort(key=lambda value: (value.get('Created', ''), value['Name']))
    result = {'modo': 'APLICAR' if apply else 'REVISION',
              'redes_elegibles': [value['Name'] for value in candidates],
              'limite': limit, 'eliminadas': [], 'omitidas_al_revalidar': [], 'fallidas': []}
    if apply:
        for network in candidates[:limit]:
            try:
                # Releer por ID completo: no borrar un recurso diferente por cambio de nombre.
                rows = json.loads(command(docker + ['network', 'inspect', network['Id']]))
                if (len(rows) != 1 or rows[0].get('Id') != network['Id']
                        or not eligible(rows[0], repo)):
                    result['omitidas_al_revalidar'].append(network['Name'])
                    continue
                # Si se conecta un contenedor después, el daemon rechaza network rm.
                command(docker + ['network', 'rm', network['Id']])
                result['eliminadas'].append(network['Name'])
            except (ReleaseError, ValueError):
                result['fallidas'].append(network['Name'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Sin esta opción solo revisa.')
    parser.add_argument('--limit', type=int, default=2, choices=range(1, 11))
    args = parser.parse_args()
    executable = shutil.which('docker')
    if not executable:
        raise ReleaseError('DOCKER_CLI_NO_ENCONTRADO')
    context = command([executable, 'context', 'show']).strip()
    contexts = json.loads(command([executable, 'context', 'inspect', context]))
    if len(contexts) != 1 or not local_endpoint(contexts[0]['Endpoints']['docker']['Host']):
        raise ReleaseError('DOCKER_NO_LOCAL')
    result = release(Path(__file__).resolve().parents[2],
                     [executable, '--context', context], apply=args.apply, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['fallidas'] else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ReleaseError, ValueError, KeyError, TypeError) as error:
        print(str(error) if isinstance(error, ReleaseError) else 'METADATOS_NO_VALIDOS')
        raise SystemExit(1)
