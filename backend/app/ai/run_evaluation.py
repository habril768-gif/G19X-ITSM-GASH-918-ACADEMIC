"""Evaluación externa optativa: vista previa por defecto, sin base de datos ni Redis."""
import argparse
import hashlib
import json
import os
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from app.ai.contracts import AIInput, AIResult, PROMPT_VERSION
from app.ai.evaluate import evaluate
from app.ai.provider import OpenAIClassifier


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_text(encoding='utf-8').encode('utf-8')).hexdigest()


def load_dataset(folder, *, require_frozen=True):
    folder = Path(folder)
    canonical = folder / 'manifest.json'
    manifest = json.loads((canonical if canonical.exists() else folder / 'manifest-congelado-v1.json').read_text(encoding='utf-8'))
    if require_frozen and (manifest.get('labels_frozen') is not True or not manifest.get('author_conformity', {}).get('reported')):
        raise ValueError('Se requiere una versión congelada con conformidad registrada')
    files = manifest.get('files', {'references': 'referencias-congeladas-v1.json',
                                 'inputs': 'entradas-congeladas-v1.json', 'catalog': 'catalogo-v1.json'})
    if (set(files) != {'references', 'inputs', 'catalog'} or len(set(files.values())) != 3
            or any(not isinstance(n, str) or not n.endswith('.json') or '/' in n or '\\' in n or ':' in n or n in {'.', '..'}
                   for n in files.values())):
        raise ValueError('Nombres de archivo no válidos')
    required = set(files.values())
    if set(manifest.get('sha256', {})) != required:
        raise ValueError('Manifiesto incompleto')
    if any(digest(folder / name) != manifest['sha256'][name] for name in required):
        raise ValueError('Los archivos no coinciden con la versión congelada')
    if manifest.get('prompt_version') != PROMPT_VERSION or manifest.get('provider_sha256') != digest(Path(__file__).with_name('provider.py')):
        raise ValueError('Cambió el proveedor o prompt; documentar otra evaluación')
    if manifest.get('prompt_sha256') != digest(Path(__file__).with_name('prompts.py')):
        raise ValueError('Cambió el contenido de las instrucciones')
    refs = json.loads((folder / files['references']).read_text(encoding='utf-8'))
    inputs = json.loads((folder / files['inputs']).read_text(encoding='utf-8'))
    catalog = json.loads((folder / files['catalog']).read_text(encoding='utf-8'))
    regular = [r for r in refs if r['kind'] == 'reference']
    evaluate(refs, [{'id': r['id'], 'error': 'NO_EJECUTADA'} for r in refs])
    if Counter(r['category_id'] for r in regular) != dict.fromkeys(range(1, 6), 10):
        raise ValueError('Se requieren diez referencias por categoría')
    if any(Counter(r['priority'] for r in regular)[p] < 10 for p in (1, 2, 3)):
        raise ValueError('Se requieren al menos diez referencias por prioridad')
    if len(inputs) != 55 or len({r['id'] for r in inputs}) != 55:
        raise ValueError('Entradas incompletas o repetidas')
    if {r['id']: (r['text'], r['scope']) for r in refs} != {r['id']: (r['text'], r['scope']) for r in inputs}:
        raise ValueError('Entradas y referencias no coinciden')
    if catalog != [{'id': i, 'nombre': name} for i, name in enumerate(
            ['Ausencias', 'Conflictos', 'Incumplimientos', 'Riesgos', 'Solicitudes Administrativas'], 1)]:
        raise ValueError('Catálogo distinto al previsto')
    for r in inputs:
        if set(r) != {'id', 'text', 'scope'} or r['scope'] not in {'PERSONA', 'ENTORNO'}:
            raise ValueError('Entrada con campos inesperados')
        AIInput(ai_input_text=r['text'], confirmed_simulated=True, confirmed_no_identifiers=True)
    if any(r['scope'] == 'ENTORNO' and r.get('category_id') != 4 for r in regular):
        raise ValueError('Etiqueta incompatible con ámbito')
    return manifest, refs, inputs, catalog


def write_json(path, value):
    # Reemplazo atómico para informes; el diario fsync conserva la fuente primaria.
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('w', encoding='utf-8', newline='\n') as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write('\n'); file.flush(); os.fsync(file.fileno())
    os.replace(temporary, path)


@contextmanager
def exclusive_run(folder):
    folder.mkdir(parents=True, exist_ok=True)
    lock = folder / 'execution.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.write(fd, str(os.getpid()).encode('ascii')); os.close(fd); fd = None
        yield
    finally:
        if fd is not None:
            os.close(fd)
        lock.unlink()


def append_event(file, value):
    file.write(json.dumps(value, ensure_ascii=False) + '\n')
    file.flush(); os.fsync(file.fileno())


def read_journal(path, valid_ids):
    started, finished = {}, {}
    if path.exists():
        for line in path.read_text(encoding='utf-8').splitlines():
            item = json.loads(line)
            ident = item['id']
            if ident not in valid_ids:
                raise ValueError('Diario ajeno al conjunto')
            if item['event'] == 'START' and ident not in started:
                started[ident] = item
            elif item['event'] == 'END' and ident in started and ident not in finished:
                finished[ident] = item['prediction']
                if finished[ident]['id'] != ident:
                    raise ValueError('ID de respuesta incoherente')
            else:
                raise ValueError('Secuencia de diario inválida')
    # Un envío interrumpido se conserva como incierto: no se vuelve a cobrar automáticamente.
    predictions = {ident: finished.get(ident, {'id': ident, 'error': 'ENVIO_INCIERTO_NO_REINTENTADO'})
                   for ident in started}
    return started, predictions


def run(folder, output, model, provider, max_calls=55):
    if type(max_calls) is not int or not 1 <= max_calls <= 55 or not model or len(model) > 120:
        raise ValueError('Modelo o límite no válido')
    manifest, refs, inputs, catalog = load_dataset(folder)
    output = Path(output)
    identity = {'dataset_sha256': manifest['sha256'], 'provider_sha256': manifest['provider_sha256'],
                'prompt_sha256': manifest['prompt_sha256'],
                'requested_model': model, 'prompt_version': PROMPT_VERSION, 'max_calls': max_calls}
    with exclusive_run(output):
        config = output / 'run.json'
        if config.exists():
            recorded = json.loads(config.read_text(encoding='utf-8'))
            if any(recorded.get(k) != v for k, v in identity.items()):
                raise ValueError('No mezclar modelo, prompt, conjunto o límite en una ejecución')
        else:
            write_json(config, dict(identity, created_at=stamp(), source='external_provider',
                                    review_scope='Conformidad general de la autora; no revisión independiente de terceros'))
        journal = output / 'journal.jsonl'
        started, predictions = read_journal(journal, {r['id'] for r in inputs})
        with journal.open('a', encoding='utf-8', newline='\n') as file:
            for row in inputs:
                if row['id'] in started:
                    continue
                if len(started) >= max_calls:
                    break
                append_event(file, {'event': 'START', 'id': row['id'], 'at': stamp()})
                started[row['id']] = True
                selected = [c for c in catalog if row['scope'] != 'ENTORNO' or c['id'] == 4]
                metadata = {}
                try:
                    result = AIResult.model_validate(provider.classify(row['text'], selected, model, metadata_sink=metadata))
                    if result.result == 'CLASIFICADA' and result.category_id not in {c['id'] for c in selected}:
                        raise ValueError('Fuera del catálogo')
                    prediction = {'id': row['id'], 'output': result.model_dump(), 'metadata': metadata}
                except Exception:
                    # No persistir excepciones crudas, cabeceras, claves ni cuerpo del proveedor.
                    prediction = {'id': row['id'], 'error': 'FALLO_PROVEEDOR_O_SALIDA', 'metadata': metadata}
                append_event(file, {'event': 'END', 'id': row['id'], 'at': stamp(), 'prediction': prediction})
                predictions[row['id']] = prediction
                print('Registrados ' + str(len(started)) + '/55 intentos', flush=True)
                if prediction.get('error'):
                    break  # No consumir el resto del límite tras un fallo; reanudar no repite el caso.
        rows = [predictions.get(r['id'], {'id': r['id'], 'error': 'NO_EJECUTADA'}) for r in inputs]
        report = evaluate(refs, rows)
        report.update(attempted_cases=len(started), execution_complete=len(started) == 55,
                      source='external_provider', requested_model=model, prompt_version=PROMPT_VERSION,
                      human_acceptance=False, generated_at=stamp())
        if not report['execution_complete']:
            report['automated_targets_met'] = False
            report['priority_checks_met'] = False
        write_json(output / 'predicciones.json', rows)
        write_json(output / 'reporte.json', report)
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output')
    parser.add_argument('--max-calls', type=int, default=55)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--confirm-reviewed-simulated', action='store_true')
    args = parser.parse_args()
    try:
        manifest, _, _, _ = load_dataset(args.dataset, require_frozen=args.execute)
        if not args.execute:
            state = 'versión fijada' if manifest.get('labels_frozen') else 'borrador; requiere revisión y congelación antes de enviar'
            print('Vista previa: 50 referencias + 5 abstenciones; hashes correctos; ' + state + '. Sin llamadas.')
            return 0
        model = os.environ.get('OPENAI_MODEL', '').strip()
        key = os.environ.get('OPENAI_API_KEY', '').strip()
        if not args.output or not args.confirm_reviewed_simulated or not key or not model:
            raise ValueError('Falta confirmación, salida o configuración local')
        if os.environ.get('AI_ENABLED', 'false').lower() not in {'true', '1'}:
            raise ValueError('IA desactivada')
        report = run(args.dataset, args.output, model, OpenAIClassifier(key), args.max_calls)
        print('Evaluación registrada. Revisa reporte.json y todos los falsos negativos de Alta.')
        return 0 if report['execution_complete'] else 2
    except (ValueError, OSError, KeyError, TypeError):
        print('No se completó la evaluación. Verifica archivos congelados, configuración y bloqueo de ejecución; no compartas credenciales.')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
