# Distinción Media/Baja — candidato v3

Estado: propuesta sin revisión humana ni predicciones. El asistente fijó el prompt v3 antes de redactar estos casos; no se enviaron al modelo. Son datos sintéticos, sin revisión independiente de terceros ni independencia estadística certificada.

## Corrección

API 0.10.2, plurione-classify-v3: comprobar primero Alta; cuando no corresponde, evaluar Media por trabajo/actividad que requiere atención pronta; asignar Baja cuando tampoco existe esa necesidad operativa. La falta de daño grave no equivale a Baja. Una fecha, trámite o riesgo controlado tampoco basta por sí solo para Media: importa el impacto pendiente. Se conservan catálogo, abstención, texto no confiable y validación humana. No se introduce un clasificador por palabras clave ni se cambia automáticamente la prioridad oficial.

El motivo debe explicar el impacto y la necesidad de atención cuando corresponde Media, y la falta de urgencia operativa si corresponde Baja. No se exige ni muestra razonamiento interno extenso.

## Referencias para revisar

[REVISION.md](REVISION.md) contiene 20 pares Media/Baja (40 casos), diez Alta y cinco abstenciones. Cada categoría tiene diez casos: 2 Alta, 4 Media, 4 Baja. En cada par, categoría y hecho base se mantienen, pero cambian las consecuencias pendientes que requieren o no atención pronta.

El conjunto es nuevo respecto a v1/v2 por texto exacto; compartir rúbrica y escenarios generales no garantiza independencia. pair_id solo está en referencias; el proveedor recibe texto/catálogo, nunca etiqueta, justificación, ID de caso o de par. entradas.json mezcla el orden para que los pares no lleguen consecutivamente por diseño.

La autora debe revisar que los contrastes y justificaciones sean razonables antes de fijar versión. El manifest continúa labels_frozen=false y author_conformity.reported=false; el envío está bloqueado, aunque se pase confirmación en CLI. No alterar etiquetas después de observar predicciones para elevar resultados.

## Medición que evita ocultar el problema

El PRD mantiene sus metas globales; no se reescribieron las evaluaciones anteriores. El evaluador añade:

- priority_class_metrics: referencias, correctos y recall por prioridad (correctos dividido entre todas las referencias esperadas de esa clase; fallos/abstenciones permanecen en denominador). Sin referencias, recall es null.
- medium_as_low_ids y low_as_medium_ids: listas de confusiones en ambas direcciones.
- media_baja_targets_met: indicador complementario para exigir ≥80% en ambas clases cuando hay al menos diez referencias por clase; null si no hay muestra suficiente. No equivale a aceptación humana ni altera automated_targets_met.
- priority_contrast_pairs: número de pares, ambos niveles de prioridad acertados y pares fallidos. Mide solo prioridad; categoría se evalúa por separado.

Objetivo de esta mejora: al menos 16/20 Media y 16/20 Baja, manteniendo metas globales, abstenciones y revisión de cualquier falso negativo Alta. Informar los veinte pares completos, sin seleccionar solo los favorables. No cambiar a todas las salidas Media para mejorar una sola clase.

DIAGNOSTICO_MEDIA_BAJA_V2.json es un recálculo offline de respuestas históricas: Media 10/20 (50%), Baja 15/15 (100%), indicador complementario false. No es una llamada nueva ni una medición del prompt v3.

## Vista previa sin gasto

Desde backend:

~~~powershell
./.venv/Scripts/python.exe -m app.ai.run_evaluation --dataset ../docs/evaluacion_ia/candidato-v3
~~~

Comprueba integridad, referencias y pares sin clave, base de datos, Redis o llamadas. Debe mostrar borrador. Todavía no existe una versión aceptacion-v3 ni predicciones v3. No modificar manifiestos históricos para utilizar v3 con v1/v2.

Tras revisión real se fijará una nueva versión con hashes, antes de ejecutar llamadas limitadas y evaluar métricas reales. La preparación no consume saldo. No se promete alcanzar las metas por pasar tests simulados.

## Operación

API/worker deben usar la misma versión para nuevas solicitudes. Sin migración adicional (0005). Jobs pendientes de v1/v2 se omiten antes del despacho al detectar versión distinta; las sugerencias completadas y decisiones humanas se conservan. Evitar solicitudes durante una actualización. No se aplicó Docker ni cambió .env en este avance.

V1 y v2 permanecen como evidencia histórica; ambas ya observadas y utilizadas en diagnóstico. No volver a llamarlas evaluación independiente de aceptación si se ajusta con esos resultados.

Fuente de diseño: [guía oficial de instrucciones y evaluación](https://developers.openai.com/api/docs/guides/prompt-engineering). Las reglas de prioridad proceden del PRD local.
## Comando de vista previa simplificado

Desde raíz: powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V3.ps1. Valida este borrador sin invocar Docker ni modelo. La opción -Ejecutar sigue bloqueada hasta registrar revisión y fijar una versión aceptacion-v3; no se debe ejecutar el borrador ni modificar sus banderas manualmente para saltar el proceso. Tres controles de comando correctos, sin llamadas reales. La revisión de etiquetas se ha solicitado y está pendiente de respuesta.
## Revisión recibida y versión fijada

La autora ya declaró revisión y acuerdo con pares Media/Baja, Alta y abstenciones y sus etiquetas/justificaciones. Este candidato se conserva como historial; usar [aceptacion-v3](../aceptacion-v3/README.md) para la medición, sin repetir la revisión ni cambiar etiquetas. Las notas anteriores de revisión pendiente corresponden a la preparación. Sin predicciones ni mejora real todavía; cuatro controles finales del comando sin proveedor/Docker reales.
