# Resultado de evaluación IA — ejecución v3

## Resultado verificado

55 intentos y 55 respuestas externas coherentes. Métricas recomputadas offline, hashes de referencias/entradas/catálogo/proveedor/prompt y diario verificados; se conservan todos los originales. Sin llamadas adicionales durante la revisión.

| Medida | Resultado | Lectura |
| --- | --- | --- |
| Categoría | 49/50 (98 %) | Supera meta global |
| Prioridad global | 46/50 (92 %) | Supera meta global |
| Media | 20/20 (100 %) | Cumple objetivo específico |
| Baja | 20/20 (100 %) | Cumple objetivo específico |
| Pares Media/Baja completos | 20/20 | Ambos niveles correctos en cada par |
| Abstención separada | 5/5 | Cumple |
| Alta | 6/10 (60 %) | Cuatro falsos negativos Alta→Media |
| Alta→Baja | 0 | No elimina los otros errores de Alta |

Conclusión técnica: Media/Baja se distingue correctamente en este conjunto, pero no se recomienda aplicar v3 como mejora integral ni aceptar su prioridad mientras queden sin resolver los cuatro Alta→Media.

automated_targets_met=true y media_baja_targets_met=true son los indicadores originales. La regla global histórica bloquea Alta→Baja, pero requiere revisar otros falsos negativos; no garantiza acierto de todos los Alta. No se cambia el reporte para falsear sus indicadores ni se interpreta true como aceptación humana. human_acceptance=false se conserva.

## Evidencia y consumo reportado

Modelo solicitado gpt-4.1-mini; efectivo gpt-4.1-mini-2025-04-14 en las 55 respuestas. Prompt plurione-classify-v3 y archivos aceptacion-v3, fijados tras revisión declarada antes de predicciones. Sin revisión independiente de terceros atribuida.

55 START/END y 55 IDs de respuesta distintos, sin fallos de transporte/esquema ni envíos inciertos registrados. 50 referencias clasificadas y cinco abstenciones separadas correctas. Tokens reportados: 63069 entrada, 4050 salida, 67119 totales. No se verificaron saldo, factura ni coste. Tiempos UTC: inicio 2026-10-18T22:26:23, reporte 2026-10-18T22:27:51.

Originales en ejecucion-v3, referencias en aceptacion-v3 y evidencia estructurada ../evidencias/82-evaluacion-ia-resultado-v3.json. No se alteraron etiquetas, respuestas, modelo, configuración o prompt en este registro.

## Revisión técnica de los cuatro falsos negativos Alta

| ID | Hecho relevante de referencia | Respuesta | Revisión |
| --- | --- | --- | --- |
| MB3-C1-A2 | Entrega obligatoria vence en quince minutos; omitirla cancela definitivamente permiso necesario para operar | Ausencias/Media | El propio motivo reconoce plazo inminente y consecuencias graves; corresponde a Alta por la regla del PRD. No exige peligro físico. |
| MB3-C3-A1 | Única copia de archivos se transfiere a medio que se borrará en minutos; pérdida impediría reanudar servicio | Incumplimientos/Media | Amenaza inmediata a continuidad operativa con pérdida grave descrita; la referencia Alta se conserva. No se trata solo de una tarea retrasada. |
| MB3-C5-A1 | Recepción documental cierra en diez minutos; falta implica pérdida definitiva de prestación esencial | Solicitudes Administrativas/Media | Plazo explícito y consecuencia grave sustentan Alta. Que sea trámite administrativo no limita a Media. |
| MB3-C5-A2 | Corrección documental vence en media hora para impedir anulación irreversible de autorización indispensable | Solicitudes Administrativas/Media | Plazo y consecuencia irreversible sustentan Alta; respuesta la trata solo como atención pronta. |

Los cuatro casos tienen consecuencias graves sin necesidad de lesión física. Varias razones reconocen datos que activarían Alta pero devuelven Media. La revisión técnica detecta ese incumplimiento; no se atribuye nueva aprobación humana de resultados ni se convierten estos errores en aciertos.

## Desacuerdo de categoría

MB3-C1-A1: referencia Ausencias/Alta, predicción Riesgos/Alta. El hecho base es falta de supervisión por ausencia y consecuencia de peligro vehicular inmediato. La prioridad es correcta; el modelo eligió la consecuencia de riesgo como categoría. Se conserva referencia previa y su no acierto. Las demás categorías tienen 10/10; Ausencias 9/10.

## Alcance de la conclusión

V2 y v3 usan conjuntos distintos; sus porcentajes no prueban por sí solos un efecto causal aislado del prompt. No se afirma una regresión causal midiendo muestras diferentes. Sí se detectan cuatro falsos negativos urgentes en la ejecución actual, suficientes para no recomendar aceptación integral de prioridad por un porcentaje global alto.

Los veinte pares fueron creados para distinguir la necesidad operativa de atención; comparten rúbrica y autoría sintética. Su acierto no garantiza desempeño en casos reales o todos los casos de frontera. Mantener validación humana obligatoria y no afirmar que la clasificación Alta se ha preservado.

## Siguiente trabajo

1. Conservar esta línea base y no repetir llamadas para buscar una ejecución favorable.
2. Reforzar y verificar el criterio Alta por plazo explícito con consecuencia grave y por pérdida operativa inminente, diferenciándolo de simple atención pronta. Examinar por qué el motivo reconoce datos urgentes y la prioridad no los refleja; no corregir automáticamente por palabras clave.
3. Antes de aceptar, comprobar tanto Alta como Media/Baja, abstención y categoría en una evaluación con referencias fijadas. Como este conjunto se usa para diagnóstico, no presentarlo luego como independiente si guía ajustes.
4. No modificar referencias históricas para mejorar puntuación ni crear bucles ilimitados de llamadas. Un nuevo envío requiere versión/propósito/carpeta claros y conservar límite/diario.
5. No recomendar despliegue automático de v3 basándose solo en los indicadores globales. El contenedor de evaluación no actualizó API/worker operativos y no se inspeccionó su versión actual. No se cambió .env ni procesos operativos en esta revisión.

La gestión manual sigue siendo necesaria. Precisión integral de prioridad y aceptación siguen pendientes; este registro no cambia código ni realiza llamadas externas.
