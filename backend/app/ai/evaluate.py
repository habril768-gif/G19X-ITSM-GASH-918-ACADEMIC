"""Evaluación offline: etiquetas congeladas y predicciones; no llama a OpenAI."""
import argparse
import json
from pydantic import ValidationError
from app.ai.contracts import AIResult


def evaluate(references, predictions):
    ids = [row['id'] for row in references]
    regular = [row for row in references if row['kind'] == 'reference']
    abstention = [row for row in references if row['kind'] == 'abstention']
    if len(ids) != len(set(ids)) or len(regular) != 50 or len(abstention) != 5 or len(references) != 55:
        raise ValueError('Se requieren 50 referencias y 5 casos separados de abstención con IDs únicos')
    if any(type(row.get('category_id')) is not int or type(row.get('priority')) is not int or row['category_id'] not in range(1, 6) or row['priority'] not in (1, 2, 3) for row in regular):
        raise ValueError('Etiquetas de referencia no válidas')
    pairs = {}
    for row in references:
        if 'pair_id' in row:
            if row['kind'] != 'reference' or not isinstance(row['pair_id'], str) or not row['pair_id']:
                raise ValueError('Par de contraste no válido')
            pairs.setdefault(row['pair_id'], []).append(row)
    if any(len(rows) != 2 or {r['priority'] for r in rows} != {2, 3}
           or len({r['category_id'] for r in rows}) != 1 or len({r.get('scope') for r in rows}) != 1
           for rows in pairs.values()):
        raise ValueError('Cada par requiere dos referencias Media/Baja de la misma categoría y ámbito')
    predicted_ids = [row['id'] for row in predictions]
    if len(predicted_ids) != len(set(predicted_ids)) or set(predicted_ids) != set(ids):
        raise ValueError('Registrar una predicción o fallo para cada referencia; sin omitir resultados')
    outputs = {}
    for row in predictions:
        try:
            output = AIResult.model_validate(row['output']) if not row.get('error') else None
            outputs[row['id']] = output if not output or output.category_id is None or output.category_id in range(1, 6) else None
        except (ValidationError, KeyError):
            outputs[row['id']] = None
    category = priority = abstentions = 0; high_as_low = []; high_false_negatives = []
    medium_as_low = []; low_as_medium = []
    category_matrix = {str(i): {str(j): 0 for j in (1, 2, 3, 4, 5, 'ABSTENCION', 'FALLO')} for i in range(1, 6)}
    priority_matrix = {str(i): {str(j): 0 for j in (1, 2, 3, 'ABSTENCION', 'FALLO')} for i in (1, 2, 3)}
    mismatches = []
    for row in regular:
        output = outputs[row['id']]
        outcome = 'FALLO' if output is None else 'ABSTENCION' if output.result == 'SIN_CLASIFICACION' else None
        category_matrix[str(row['category_id'])][outcome or str(output.category_id)] += 1
        priority_matrix[str(row['priority'])][outcome or str(output.priority)] += 1
        if outcome or output.category_id != row['category_id'] or output.priority != row['priority']:
            mismatches.append({'id': row['id'], 'expected_category': row['category_id'],
                               'expected_priority': row['priority'], 'outcome': outcome or 'CLASIFICADA',
                               'predicted_category': output.category_id if output else None,
                               'predicted_priority': output.priority if output else None})
        if row['priority'] == 1 and (not output or output.result != 'CLASIFICADA' or output.priority != 1):
            high_false_negatives.append(row['id'])
        if output and output.result == 'CLASIFICADA':
            category += output.category_id == row['category_id']
            priority += output.priority == row['priority']
            if row['priority'] == 1 and output.priority == 3:
                high_as_low.append(row['id'])
            if row['priority'] == 2 and output.priority == 3:
                medium_as_low.append(row['id'])
            if row['priority'] == 3 and output.priority == 2:
                low_as_medium.append(row['id'])
    for row in abstention:
        output = outputs[row['id']]
        abstentions += bool(output and output.result == 'SIN_CLASIFICACION')
    class_metrics = {}
    for label, matrix in priority_matrix.items():
        total = sum(matrix.values())
        class_metrics[label] = {'reference_cases': total, 'correct': matrix[label],
                                'recall': matrix[label] / total if total else None}
    # Indicador complementario: no cambia retrospectivamente las metas globales del PRD.
    media_baja_targets = None
    if all(class_metrics[str(p)]['reference_cases'] >= 10 for p in (2, 3)):
        media_baja_targets = all(class_metrics[str(p)]['recall'] >= 0.8 for p in (2, 3))
    all_high_identified = not high_false_negatives if class_metrics['1']['reference_cases'] >= 10 else None
    global_targets = category >= 45 and priority >= 40 and not high_as_low and abstentions == 5
    priority_checks = (global_targets and media_baja_targets and all_high_identified
                       if media_baja_targets is not None and all_high_identified is not None else None)
    pair_metrics = None
    if pairs:
        failed_pairs = [ident for ident, rows in pairs.items() if not all(
            outputs[r['id']] and outputs[r['id']].result == 'CLASIFICADA'
            and outputs[r['id']].priority == r['priority'] for r in rows)]
        pair_metrics = {'pairs': len(pairs), 'both_priorities_correct': len(pairs) - len(failed_pairs),
                        'accuracy': (len(pairs) - len(failed_pairs)) / len(pairs), 'failed_pair_ids': failed_pairs}
    return {'reference_cases': 50, 'category_correct': category, 'priority_correct': priority,
            'category_accuracy': category / 50, 'priority_accuracy': priority / 50,
            'abstention_cases': 5, 'abstention_correct': abstentions, 'high_as_low_ids': high_as_low,
            'high_false_negative_ids': high_false_negatives,
            'category_confusion_matrix': category_matrix, 'priority_confusion_matrix': priority_matrix,
            'mismatches': mismatches,
            'priority_class_metrics': class_metrics, 'medium_as_low_ids': medium_as_low,
            'low_as_medium_ids': low_as_medium, 'media_baja_targets_met': media_baja_targets,
            'priority_contrast_pairs': pair_metrics,
            'automated_targets_met': global_targets,
            'all_high_priority_identified': all_high_identified,
            'priority_checks_met': priority_checks,
            'independent_labels_and_all_high_priority_false_negatives_require_review': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('references'); parser.add_argument('predictions'); args = parser.parse_args()
    with open(args.references, encoding='utf-8') as source: references = json.load(source)
    with open(args.predictions, encoding='utf-8') as source: predictions = json.load(source)
    print(json.dumps(evaluate(references, predictions), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
