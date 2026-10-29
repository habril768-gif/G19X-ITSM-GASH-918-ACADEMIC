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
def balanced_priorities():
    refs, rows = fixture()
    for i in range(50):
        priority = 1 if i < 10 else 2 if i < 30 else 3
        refs[i]['priority'] = priority
        rows[i]['output']['priority'] = priority
    return refs, rows


def test_global_threshold_does_not_hide_medium_underclassification():
    refs, rows = balanced_priorities()
    for i in range(10, 20):
        rows[i]['output']['priority'] = 3
    report = evaluate(refs, rows)
    assert report['priority_accuracy'] == 0.8 and report['automated_targets_met']
    assert report['priority_class_metrics']['2'] == {'reference_cases':20,'correct':10,'recall':0.5}
    assert report['priority_class_metrics']['3']['recall'] == 1
    assert report['medium_as_low_ids'] == [str(i) for i in range(10,20)]
    assert report['media_baja_targets_met'] is False


def test_forcing_every_non_high_to_medium_does_not_pass_media_baja_measurement():
    refs, rows = balanced_priorities()
    for i in range(30, 50):
        rows[i]['output']['priority'] = 2
    report = evaluate(refs, rows)
    assert report['priority_class_metrics']['2']['recall'] == 1
    assert report['priority_class_metrics']['3']['recall'] == 0
    assert report['media_baja_targets_met'] is False
    assert report['low_as_medium_ids'] == [str(i) for i in range(30,50)]


def test_class_metrics_count_failures_and_abstentions_without_dropping_rows():
    refs, rows = balanced_priorities()
    rows[10] = {'id':'10','error':'fixture'}
    rows[11]['output'] = dict(rows[-1]['output'])
    report = evaluate(refs, rows)
    assert report['priority_class_metrics']['2']['reference_cases'] == 20
    assert report['priority_class_metrics']['2']['recall'] == 18/20
    assert report['priority_confusion_matrix']['2']['FALLO'] == 1
    assert report['priority_confusion_matrix']['2']['ABSTENCION'] == 1


def test_absent_class_is_unknown_instead_of_perfect():
    refs, rows = fixture()
    report = evaluate(refs, rows)
    assert report['priority_class_metrics']['3']['recall'] is None
    assert report['media_baja_targets_met'] is None
    assert report['priority_contrast_pairs'] is None


def test_contrast_pair_requires_both_priorities_right_and_rejects_invalid_pair():
    refs, rows = balanced_priorities()
    refs[10]['pair_id'] = refs[30]['pair_id'] = 'fixture-pair'
    report = evaluate(refs, rows)
    assert report['priority_contrast_pairs'] == {'pairs':1,'both_priorities_correct':1,'accuracy':1,'failed_pair_ids':[]}
    rows[10]['output']['priority'] = 3
    report = evaluate(refs, rows)
    assert report['priority_contrast_pairs']['both_priorities_correct'] == 0
    assert report['priority_contrast_pairs']['failed_pair_ids'] == ['fixture-pair']
    refs[30]['priority'] = 2
    with pytest.raises(ValueError, match='Cada par'):
        evaluate(refs, rows)
def test_high_to_medium_prevents_combined_priority_checks_despite_global_success():
    refs, rows = balanced_priorities()
    for i in range(4):
        rows[i]['output']['priority'] = 2
    report = evaluate(refs, rows)
    assert report['priority_correct'] == 46 and report['automated_targets_met']
    assert report['media_baja_targets_met'] is True
    assert report['high_as_low_ids'] == []
    assert report['high_false_negative_ids'] == ['0','1','2','3']
    assert report['all_high_priority_identified'] is False
    assert report['priority_checks_met'] is False


def test_complete_correct_references_meet_combined_checks_without_human_acceptance_claim():
    refs, rows = balanced_priorities()
    report = evaluate(refs, rows)
    assert report['all_high_priority_identified'] is True
    assert report['priority_checks_met'] is True
    assert report['independent_labels_and_all_high_priority_false_negatives_require_review'] is True


def test_high_priority_insufficient_sample_is_unknown():
    refs, rows = fixture()
    report = evaluate(refs, rows)
    assert report['all_high_priority_identified'] is None
    assert report['priority_checks_met'] is None
