"""Inicia una formal QA solo tras CPU previa baja y liberación acotada de redes."""
import argparse
import json
import math
from pathlib import Path
import shutil

import performance_host as host
import provision_performance_qa as provision
import release_performance_networks as networks

MAX_AVERAGE_CPU = 30.0
MAX_INTERVAL_CPU = 50.0


def baseline_ready(value):
    try:
        rows = value['intervalos']
        if value['intervalos_validos'] != 3 or value['intervalos_totales'] != 3 or len(rows) != 3:
            return False
        for row in rows:
            cpu, seconds = row['cpu_global_porcentaje'], row['duracion_s']
            if (row['estado'] != 'OK' or not math.isfinite(cpu) or not 0 <= cpu <= MAX_INTERVAL_CPU
                    or not math.isfinite(seconds) or seconds <= 0):
                return False
        weighted = sum(row['cpu_global_porcentaje'] * row['duracion_s'] for row in rows) / sum(row['duracion_s'] for row in rows)
        average = value['media_cpu_global_porcentaje']
        return (math.isfinite(average) and math.isclose(average, weighted, abs_tol=1e-6)
                and 0 <= average <= MAX_AVERAGE_CPU)
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def guarded_run(repo, executable):
    # No tocar Docker o redes antes de aprobar la lectura de CPU sin carga.
    baseline = host.baseline()
    preflight = {'cpu_previa': baseline,
        'umbrales_operativos': {'media_cpu_max_porcentaje': MAX_AVERAGE_CPU,
                               'intervalo_cpu_max_porcentaje': MAX_INTERVAL_CPU},
        'limites': 'Condición operativa previa, no criterio RNF-2. No garantiza carga constante durante construcción o medición. Mantiene diez clientes y p95 menor de 200 ms.'}
    if not baseline_ready(baseline):
        print(json.dumps({'estado': 'NO_INICIADA_CPU_PREVIA', **preflight}, ensure_ascii=False, indent=2))
        return 2
    context = networks.command([executable, 'context', 'show']).strip()
    contexts = json.loads(networks.command([executable, 'context', 'inspect', context]))
    if len(contexts) != 1 or not provision.local_endpoint(contexts[0]['Endpoints']['docker']['Host']):
        raise networks.ReleaseError('DOCKER_NO_LOCAL')
    cleanup = networks.release(repo, [executable, '--context', context], apply=True, limit=2)
    ready = (len(cleanup['eliminadas']) == 2 and not cleanup['fallidas']
             and not cleanup['omitidas_al_revalidar'])
    print(json.dumps({'estado': 'PRECONDICIONES_OK' if ready else 'NO_INICIADA_REDES_QA',
                     **preflight, 'limpieza_redes': cleanup}, ensure_ascii=False, indent=2), flush=True)
    if not ready:
        return 2
    preflight['redes_qa_liberadas'] = cleanup['eliminadas']
    # Sin diagnóstico de API: protocolo formal original 30 + 300 s.
    return provision.run(repo, 'full', executable, preflight=preflight)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirm-isolated-qa', action='store_true', required=True,
        help='Autoriza liberar hasta dos redes QA vacías registradas y crear el proyecto formal aislado.')
    parser.parse_args(argv)
    executable = shutil.which('docker')
    if not executable:
        raise networks.ReleaseError('DOCKER_CLI_NO_ENCONTRADO')
    return guarded_run(Path(__file__).resolve().parents[2], executable)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (networks.ReleaseError, provision.ProvisionError, ValueError, KeyError, TypeError) as error:
        print(str(error) if isinstance(error, (networks.ReleaseError, provision.ProvisionError)) else 'PRECONDICIONES_NO_VALIDADAS')
        raise SystemExit(1)
