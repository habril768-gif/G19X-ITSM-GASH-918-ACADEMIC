# Resultado de evaluación IA — ejecución v1

## Resultado verificado

Ejecución externa de 55 casos registrada por la autora y comprobada con archivos locales. Se recalcularon las métricas offline y coincidieron con reporte.json; diario, IDs de respuesta y predicciones son coherentes, sin filas omitidas. No se repitieron llamadas.

| Medida | Resultado | Meta del PRD | Estado |
| --- | --- | --- | --- |
| Categoría | 32/50 (64 %) | ≥45/50 (90 %) | No cumple |
| Prioridad | 30/50 (60 %) | ≥40/50 (80 %) | No cumple |
| Abstención separada | 5/5 | 5/5 | Cumple |
| Alta → Baja | 0 casos | 0 casos | Sin degradación directa |
| Otros falsos negativos de Alta | 1 abstención | Revisión obligatoria | Revisado técnicamente; decisión humana pendiente |

RF-3 permanece parcial y no aceptado. Finalizar 55 llamadas demuestra ejecución, no precisión suficiente ni aceptación humana.

## Trazabilidad y consumo reportado

- Modelo solicitado: gpt-4.1-mini.
- Modelo efectivo en las 55 respuestas: gpt-4.1-mini-2025-04-14.
- Prompt: plurione-classify-v1; hash de proveedor coincide con manifest fijado.
- Entradas, referencias y catálogo coinciden con los hashes de run.json y manifest-congelado-v1.json.
- 55 inicios y 55 resultados, sin fallos de transporte/esquema ni envíos inciertos registrados.
- Tokens reportados por las respuestas: 17624 de entrada, 3788 de salida, 21412 en total. No se consultaron factura, saldo ni coste real.
- Secuencia según marcas UTC guardadas: 2026-10-18T20:40:09 a 2026-10-18T20:41:38. No se reconstruyen otras actividades.
- Evidencia estructurada: ../evidencias/75-evaluacion-ia-resultado-v1.json; archivos originales en ejecucion-v1.

Los 50 casos regulares contienen 38 clasificaciones y 12 abstenciones. Las abstenciones permanecen como no aciertos; no se redujo el denominador. Los cinco casos separados de abstención se resolvieron como SIN_CLASIFICACION.

## Desglose de aciertos

| Categoría esperada | Aciertos |
| --- | --- |
| Ausencias | 6/10 |
| Conflictos | 9/10 |
| Incumplimientos | 6/10 |
| Riesgos | 4/10 |
| Solicitudes Administrativas | 7/10 |

| Prioridad esperada | Aciertos |
| --- | --- |
| Alta | 14/15 |
| Media | 10/20 |
| Baja | 6/15 |

Hay 24 casos con discrepancia en categoría, prioridad o abstención, listados en reporte.json. Las matrices tienen filas esperadas y columnas predichas; cada una conserva los 50 casos regulares, incluidos abstención y fallo.

## Revisión técnica del falso negativo de Alta

EVAL-C4-02 describe una estantería inclinada y objetos pesados a punto de caer junto a un paso utilizado, con necesidad explícita de aislar el área de inmediato. Referencia fijada: Riesgos/Alta. El proveedor respondió SIN_CLASIFICACION porque no consideró explícito el vínculo con un hecho laboral simulado.

El texto sí describe una amenaza inmediata conforme al PRD 3.1. Es una abstención incorrecta respecto a la referencia vigente y un falso negativo de Alta; no se transforma en acierto por sugerir revisión humana. La respuesta queda conservada sin corrección retrospectiva. Se recomienda mantener esa referencia en esta ejecución; no se atribuye aprobación de esta revisión técnica a la autora. La clasificación y atención operativa siguen siendo humanas y el sistema no reemplaza canales de emergencia.

## Hallazgos y límites

Las respuestas de seis casos Riesgos se abstuvieron; varias razones exigen vínculo explícito con simulación o riesgo laboral, pese a la confirmación del conjunto. También hay abstenciones en trámites concretos y desviaciones de políticas. La ausencia de urgencia no excluye por sí sola un caso del catálogo: puede corresponder a Baja.

En tres referencias Ausencias se predijo Incumplimientos y en otra Riesgos. Dos Incumplimientos se clasificaron Riesgos. Algunos hechos pertenecen a fronteras semánticas reales (ausencia que produce peligro, incumplimiento de seguridad); las etiquetas fueron propuestas por asistente con conformidad general, sin revisión independiente de terceros. Esa limitación no habilita cambiar las referencias después de ver respuestas para elevar métricas.

El proveedor v1 envía nombres del catálogo y equivalencias 1/2/3 de prioridad. No incluye definiciones completas de categorías ni la rúbrica Alta/Media/Baja del PRD; tampoco dice explícitamente que un gestor ya confirmó que todos los textos enviados son simulados. Esto es una hipótesis fundamentada sobre la causa de varios errores, no una demostración de que añadir reglas resolverá todos los casos ni de incapacidad general del modelo.

## Siguiente corrección y reevaluación

1. Conservar esta ejecución v1 como línea base fallida, sin editar etiquetas ni respuestas, cambiar denominadores o repetir en la misma carpeta.
2. Preparar una versión nueva del prompt con definiciones/rúbrica del PRD, contexto de simulación confirmada, distinción entre urgencia y pertenencia al catálogo, y criterios generales para categorías que se superponen. No introducir textos, IDs ni respuestas específicas del conjunto.
3. Probar que se conserva la omisión de confidenciales, la resistencia a instrucciones incrustadas, la salida estructurada y la validación humana. La corrección requiere desarrollo/pruebas; no está implementada por este documento.
4. Como los resultados v1 se usan para diagnóstico/ajuste, este conjunto pasa a ser de desarrollo. Su eventual repetición no acredita aceptación final: preparar y revisar otro conjunto independiente antes de ejecutarlo.
5. Registrar nueva versión/procedencia y predicciones, revisar todos los falsos negativos de Alta y exigir nuevamente los umbrales. La aceptación humana permanece pendiente.

No se desactivó ni modificó la configuración local de la autora. La gestión manual permanece disponible. No se ejecutaron llamadas adicionales, no se alteró el prompt y no se declara RF-3 aceptado.
