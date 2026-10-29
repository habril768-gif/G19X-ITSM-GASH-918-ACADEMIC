from pathlib import Path
from shutil import copyfile
from unittest.mock import Mock
import json
import pytest
from app.ai import run_evaluation as runner
from app.ai.evaluate import evaluate
from test_ai_evaluation import fixture

DATA = Path(__file__).resolve().parents[2] / 'docs' / 'evaluacion_ia'
ORIGINAL_DATA = DATA
RESULT = {'result': 'CLASIFICADA', 'category_id': 4, 'priority': 2,
          'suggestion': 'Revisar el caso ficticio.', 'reason': 'Salida de prueba, no predicción real.'}


@pytest.fixture(autouse=True)
def dataset_fixture(tmp_path, monkeypatch):
    folder = tmp_path / 'fixture-dataset'; folder.mkdir()
    for name in ('manifest.json', 'referencias.json', 'entradas.json', 'catalogo.json'):
        copyfile(ORIGINAL_DATA/'candidato-v4'/name, folder/name)
    manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
    # Aprobación simulada exclusiva de tests; nunca modifica la referencia candidata.
    manifest.update(labels_frozen=True, author_conformity={'reported': True, 'source': 'TEST_FIXTURE'})
    (folder/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    monkeypatch.setitem(globals(), 'DATA', folder)


def provider():
    def classify(text, catalog, model, *, metadata_sink):
        assert isinstance(text, str) and text and 'EVAL-' not in text
        assert all(set(c) == {'id', 'nombre'} for c in catalog)
        metadata_sink.update(effective_model='fixture-model', usage={'total_tokens': 12})
        return dict(RESULT)
    return Mock(classify=Mock(side_effect=classify))


def test_default_preview_never_constructs_provider_or_creates_output(tmp_path, monkeypatch, capsys):
    constructor = Mock(side_effect=AssertionError('No provider'))
    monkeypatch.setattr(runner, 'OpenAIClassifier', constructor)
    monkeypatch.setattr('sys.argv', ['eval', '--dataset', str(DATA), '--output', str(tmp_path/'absent')])
    assert runner.main() == 0
    assert 'Sin llamadas' in capsys.readouterr().out
    assert not (tmp_path/'absent').exists()
    constructor.assert_not_called()


def test_frozen_hash_rejects_modified_input_before_calls(tmp_path):
    copy = tmp_path/'data'; copy.mkdir()
    for name in ('manifest.json', 'entradas.json', 'referencias.json', 'catalogo.json'):
        copyfile(DATA/name, copy/name)
    with (copy/'entradas.json').open('a', encoding='utf-8') as f: f.write(' ')
    fake = provider()
    with pytest.raises(ValueError, match='versión congelada'):
        runner.run(copy, tmp_path/'run', 'fixture-model', fake)
    fake.classify.assert_not_called()


def test_full_run_no_labels_sent_and_resume_never_repeats(tmp_path):
    fake = provider()
    report = runner.run(DATA, tmp_path, 'fixture-model', fake)
    assert report['execution_complete'] and report['attempted_cases'] == 55
    assert not report['human_acceptance'] and not report['automated_targets_met']
    assert fake.classify.call_count == 55
    saved = json.loads((tmp_path/'predicciones.json').read_text(encoding='utf-8'))
    assert len(saved) == 55 and all(row['metadata']['effective_model'] == 'fixture-model' for row in saved)
    assert sum(sum(row.values()) for row in report['category_confusion_matrix'].values()) == 50
    runner.run(DATA, tmp_path, 'fixture-model', fake)
    assert fake.classify.call_count == 55
    with pytest.raises(ValueError, match='mezclar'):
        runner.run(DATA, tmp_path, 'different-model', fake)
    assert fake.classify.call_count == 55


def test_lifetime_call_limit_partial_cannot_pass_targets(tmp_path):
    fake = provider()
    report = runner.run(DATA, tmp_path, 'fixture-model', fake, max_calls=1)
    assert report['attempted_cases'] == 1 and not report['execution_complete']
    assert not report['automated_targets_met']
    runner.run(DATA, tmp_path, 'fixture-model', fake, max_calls=1)
    assert fake.classify.call_count == 1
    rows = json.loads((tmp_path/'predicciones.json').read_text(encoding='utf-8'))
    assert sum(row.get('error') == 'NO_EJECUTADA' for row in rows) == 54


def test_provider_failure_stops_and_does_not_leak_exception_or_retry(tmp_path):
    fake = Mock(classify=Mock(side_effect=RuntimeError('fixture-secret-do-not-persist')))
    result = runner.run(DATA, tmp_path, 'fixture-model', fake)
    assert result['attempted_cases'] == 1
    assert 'fixture-secret' not in (tmp_path/'journal.jsonl').read_text(encoding='utf-8')
    good = provider()
    report = runner.run(DATA, tmp_path, 'fixture-model', good)
    assert good.classify.call_count == 54 and report['execution_complete']
    rows = json.loads((tmp_path/'predicciones.json').read_text(encoding='utf-8'))
    assert rows[0]['error'] == 'FALLO_PROVEEDOR_O_SALIDA'


def test_interrupted_dispatch_not_resent_on_resume(tmp_path):
    fake = Mock(classify=Mock(side_effect=KeyboardInterrupt))
    with pytest.raises(KeyboardInterrupt):
        runner.run(DATA, tmp_path, 'fixture-model', fake)
    good = provider()
    report = runner.run(DATA, tmp_path, 'fixture-model', good)
    assert good.classify.call_count == 54 and report['attempted_cases'] == 55
    rows = json.loads((tmp_path/'predicciones.json').read_text(encoding='utf-8'))
    assert rows[0]['error'] == 'ENVIO_INCIERTO_NO_REINTENTADO'


def test_overlapping_run_and_corrupt_journal_make_no_calls(tmp_path):
    fake = provider()
    (tmp_path/'execution.lock').write_text('fixture', encoding='utf-8')
    with pytest.raises(FileExistsError):
        runner.run(DATA, tmp_path, 'fixture-model', fake)
    (tmp_path/'execution.lock').unlink()
    (tmp_path/'journal.jsonl').write_text('{"partial":', encoding='utf-8')
    with pytest.raises(ValueError):
        runner.run(DATA, tmp_path, 'fixture-model', fake)
    fake.classify.assert_not_called()


def test_out_of_scope_category_recorded_as_failure(tmp_path):
    fake = Mock(classify=Mock(return_value=dict(RESULT, category_id=99)))
    report = runner.run(DATA, tmp_path, 'fixture-model', fake)
    assert report['attempted_cases'] == 1
    rows = json.loads((tmp_path/'predicciones.json').read_text(encoding='utf-8'))
    assert rows[0]['error'] == 'FALLO_PROVEEDOR_O_SALIDA'


def test_confusion_matrices_keep_abstentions_failures_and_high_errors():
    refs, rows = fixture()
    refs[0]['priority'] = 1
    rows[0]['output']['priority'] = 3
    rows[1] = {'id':'1', 'error':'fixture'}
    rows[2]['output'] = dict(rows[-1]['output'])
    report = evaluate(refs, rows)
    assert report['priority_confusion_matrix']['1']['3'] == 1
    assert report['category_confusion_matrix']['2']['FALLO'] == 1
    assert report['category_confusion_matrix']['2']['ABSTENCION'] == 1
    assert {r['id'] for r in report['mismatches']} == {'0','1','2'}
    assert report['high_as_low_ids'] == ['0'] and not report['automated_targets_met']


def test_execution_requires_local_configuration_and_confirmation(tmp_path, monkeypatch):
    fake = Mock()
    monkeypatch.setattr(runner, 'OpenAIClassifier', fake)
    monkeypatch.setenv('AI_ENABLED', 'true')
    monkeypatch.setenv('OPENAI_MODEL', 'fixture-model')
    monkeypatch.setenv('OPENAI_API_KEY', 'fixture-key')
    monkeypatch.setattr('sys.argv', ['eval','--dataset',str(DATA),'--output',str(tmp_path/'absent'),'--execute'])
    assert runner.main() == 2
    fake.assert_not_called()
    assert not (tmp_path/'absent').exists()
def test_candidate_preview_allowed_but_execution_not_approved(tmp_path):
    candidate = ORIGINAL_DATA/'candidato-v4'
    manifest, refs, _, _ = runner.load_dataset(candidate, require_frozen=False)
    assert not manifest['labels_frozen'] and len(refs) == 55
    fake = provider()
    with pytest.raises(ValueError, match='conformidad'):
        runner.run(candidate, tmp_path/'not-created', 'fixture-model', fake)
    fake.classify.assert_not_called()
    assert not (tmp_path/'not-created').exists()


@pytest.mark.parametrize('previous', ['', 'aceptacion-v2', 'aceptacion-v3'])
def test_old_frozen_baseline_not_silently_reused_with_new_prompt(tmp_path, previous):
    fake = provider()
    with pytest.raises(ValueError, match='proveedor o prompt'):
        runner.run(ORIGINAL_DATA/previous, tmp_path/'absent', 'fixture-model', fake)
    fake.classify.assert_not_called()


def test_manifest_rejects_traversal_and_changed_instruction_hash():
    path = DATA/'manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    manifest['files']['references'] = '../referencias.json'
    path.write_text(json.dumps(manifest), encoding='utf-8')
    with pytest.raises(ValueError, match='Nombres'):
        runner.load_dataset(DATA)
    manifest['files']['references'] = 'referencias.json'
    manifest['prompt_sha256'] = 'fixture-mismatch'
    path.write_text(json.dumps(manifest), encoding='utf-8')
    with pytest.raises(ValueError, match='instrucciones'):
        runner.load_dataset(DATA)
def test_partial_run_cannot_claim_combined_priority_checks_with_enough_correct_predictions(tmp_path):
    refs = json.loads((DATA/'referencias.json').read_text(encoding='utf-8'))
    inputs = json.loads((DATA/'entradas.json').read_text(encoding='utf-8'))
    by_id = {r['id']:r for r in refs}; by_text = {r['text']:r for r in refs}
    last = next(r for r in inputs if by_id[r['id']].get('priority') == 3)
    inputs = [r for r in inputs if r['id'] != last['id']] + [last]
    (DATA/'entradas.json').write_text(json.dumps(inputs,ensure_ascii=False),encoding='utf-8')
    manifest_path = DATA/'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['sha256']['entradas.json'] = runner.digest(DATA/'entradas.json')
    manifest_path.write_text(json.dumps(manifest),encoding='utf-8')
    def classify(text, catalog, model, *, metadata_sink):
        row = by_text[text]
        return dict(RESULT, result='SIN_CLASIFICACION' if row['kind']=='abstention' else 'CLASIFICADA',
                    category_id=row.get('category_id'), priority=row.get('priority'))
    report = runner.run(DATA,tmp_path/'partial-run','fixture-model',Mock(classify=Mock(side_effect=classify)),max_calls=54)
    assert report['priority_correct'] == 49
    assert report['media_baja_targets_met'] is True and report['all_high_priority_identified'] is True
    assert report['execution_complete'] is False
    assert report['automated_targets_met'] is False and report['priority_checks_met'] is False
