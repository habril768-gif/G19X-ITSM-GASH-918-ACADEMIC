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
    predicted_ids = [row['id'] for row in predictions]
    if len(predicted_ids) != len(set(predicted_ids)) or set(predicted_ids) != set(ids):
        raise ValueError('Registrar una predicción o fallo para cada referencia; sin omitir resultados')
    outputs = {}
    for row in predictions:
        try:
            outputs[row['id']] = AIResult.model_validate(row['output']) if not row.get('error') else None
        except (ValidationError, KeyError):
            outputs[row['id']] = None
    category = priority = abstentions = 0; high_as_low = []; high_false_negatives = []
    for row in regular:
        output = outputs[row['id']]
        if row['priority'] == 1 and (not output or output.result != 'CLASIFICADA' or output.priority != 1):
            high_false_negatives.append(row['id'])
        if output and output.result == 'CLASIFICADA':
            category += output.category_id == row['category_id']
            priority += output.priority == row['priority']
            if row['priority'] == 1 and output.priority == 3:
                high_as_low.append(row['id'])
    for row in abstention:
        output = outputs[row['id']]
        abstentions += bool(output and output.result == 'SIN_CLASIFICACION')
    return {'reference_cases': 50, 'category_correct': category, 'priority_correct': priority,
            'category_accuracy': category / 50, 'priority_accuracy': priority / 50,
            'abstention_cases': 5, 'abstention_correct': abstentions, 'high_as_low_ids': high_as_low,
            'high_false_negative_ids': high_false_negatives,
            'automated_targets_met': category >= 45 and priority >= 40 and not high_as_low and abstentions == 5,
            'independent_labels_and_all_high_priority_false_negatives_require_review': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('references'); parser.add_argument('predictions'); args = parser.parse_args()
    with open(args.references, encoding='utf-8') as source: references = json.load(source)
    with open(args.predictions, encoding='utf-8') as source: predictions = json.load(source)
    print(json.dumps(evaluate(references, predictions), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
