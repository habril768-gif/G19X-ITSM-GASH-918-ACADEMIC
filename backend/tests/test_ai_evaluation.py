from copy import deepcopy
import pytest
from app.ai.evaluate import evaluate
from test_ai import RESULT


def fixture():
    references = [{'id': str(i), 'kind': 'reference', 'category_id': 2, 'priority': 2} for i in range(50)]
    references += [{'id': str(i), 'kind': 'abstention'} for i in range(50, 55)]
    predictions = [{'id': str(i), 'output': dict(RESULT)} for i in range(50)]
    abstain = dict(RESULT, result='SIN_CLASIFICACION', category_id=None, priority=None)
    predictions += [{'id': str(i), 'output': abstain} for i in range(50, 55)]
    return references, predictions


def test_failures_and_abstentions_stay_in_denominator():
    refs, predictions = fixture()
    predictions[0] = {'id': '0', 'error': 'FALLIDA'}
    predictions[1]['output'] = dict(predictions[-1]['output'])
    report = evaluate(refs, predictions)
    assert report['category_accuracy'] == 48/50 and report['priority_accuracy'] == 48/50


def test_high_as_low_blocks_target_despite_high_overall_score():
    refs, predictions = fixture(); refs[0]['priority'] = 1; predictions[0]['output']['priority'] = 3
    result = evaluate(refs, predictions)
    assert result['category_correct'] == 50 and result['priority_correct'] == 49
    assert result['high_as_low_ids'] == ['0'] and not result['automated_targets_met']
    assert result['high_false_negative_ids'] == ['0']


def test_missing_prediction_cannot_improve_accuracy():
    refs, predictions = fixture()
    with pytest.raises(ValueError): evaluate(refs, predictions[:-1])
    predictions[-1]['output'] = dict(RESULT)
    assert not evaluate(refs, predictions)['automated_targets_met']
