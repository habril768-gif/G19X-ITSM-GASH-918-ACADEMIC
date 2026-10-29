# Evaluación IA — versión fijada v1

Estado: etiquetas fijadas con conformidad general de la autora. La evaluación externa v1 ya se ejecutó: no alcanzó metas de categoría/prioridad. Se conserva como línea base de desarrollo; consultar RESULTADOS_V1.md. La conformidad no se presenta como revisión independiente de terceros ni como revisión individual observada de todas las etiquetas.

## Archivos de referencia

- referencias-congeladas-v1.json: 50 referencias justificadas y cinco abstenciones.
- entradas-congeladas-v1.json: mismos textos y ámbitos, sin etiquetas ni justificaciones, en orden entrelazado.
- catalogo-v1.json: cinco categorías del catálogo; ENTORNO se limita a Riesgos.
- manifest-congelado-v1.json: hashes SHA256 normalizados a UTF-8/LF, versión de prompt, hash del proveedor y procedencia de la conformidad.
- REVISION.md: documento de lectura humana. Se conserva la edición de formato de la autora. Sus textos y etiquetas no se modificaron al fijar la versión.
- Los archivos borrador-v1 permanecen como historial; sus hashes describen el momento del borrador, no las modificaciones posteriores del documento de lectura.

Textos sintéticos propuestos por asistente a partir del PRD, sin consultar predicciones del modelo evaluado. No son casos reales ni muestra representativa. Diez referencias por categoría; prioridades 15 Alta, 20 Media y 15 Baja; cinco abstenciones. El ejemplo manual piso mojado queda fuera. El conjunto no se usó para ajustar el prompt. Si se utiliza para ajuste, se requiere otro conjunto independiente para aceptación final.

## Vista previa sin consumir saldo

Desde raíz del proyecto:

~~~powershell
docker compose --profile ai build ai-worker
docker compose --profile ai run --rm --no-deps --volume "${PWD}/docs/evaluacion_ia:/evaluation" ai-worker python -m app.ai.run_evaluation --dataset /evaluation
~~~

Esperado: «Vista previa: 50 referencias + 5 abstenciones; hashes correctos. Sin llamadas.» La primera orden construye la imagen; la segunda valida archivos sin consultar modelo/base de datos/Redis. La clave procede de la configuración local del worker y nunca se imprime.

Alternativa nativa desde backend (no necesita clave para vista previa):

~~~powershell
./.venv/Scripts/python.exe -m app.ai.run_evaluation --dataset ../docs/evaluacion_ia
~~~

## Ejecución externa optativa

El siguiente comando sí usa la API y puede generar cargos. Conserva el mismo directorio de salida al reanudar:

~~~powershell
docker compose --profile ai run --rm --no-deps --volume "${PWD}/docs/evaluacion_ia:/evaluation" ai-worker python -m app.ai.run_evaluation --dataset /evaluation --output /evaluation/ejecucion-v1 --max-calls 55 --execute --confirm-reviewed-simulated
~~~

Requiere AI_ENABLED=true, OPENAI_MODEL y OPENAI_API_KEY configurados localmente. No pegar claves en comandos ni compartir .env. No crea incidencias ni modifica la base. El proveedor recibe solo texto y catálogo: no ID, etiqueta esperada, justificación ni ámbito como metadato.

Límite acumulado: 55 intentos en esa carpeta y 1500 tokens de salida por llamada; SDK sin reintentos automáticos. Es un límite de llamadas/salida, no un tope monetario garantizado. Los tokens de entrada también se facturan según el modelo; revisar consumo en la cuenta. No se fijó una tarifa ni coste estimado en este avance.

Tras un error, se detiene el bloque y registra el caso como fallo. Al repetir exactamente la orden, omite todos los casos ya intentados y continúa con los restantes. Un envío iniciado sin respuesta guardada queda INCIERTO y no se reenvía automáticamente. No borrar el diario ni abrir otra carpeta para repetir: eso perdería la protección contra cargos duplicados y constituye otra ejecución.

El archivo execution.lock excluye procesos simultáneos. Si se mata el proceso sin limpieza, puede quedar el bloqueo: verificar que el proceso terminó antes de retirar únicamente ese archivo. Diario truncado/corrupto, cambio de conjunto, modelo, prompt, proveedor o límite detienen reanudación; conservar archivos para revisar. No intentar reparar borrando intentos.

## Resultados

En ejecucion-v1 se generan:

- run.json: configuración de ejecución, hashes y fecha UTC real.
- journal.jsonl: inicio persistido antes de cada llamada y resultado/fallo después.
- predicciones.json: exactamente 55 filas, incluidas NO_EJECUTADA/FALLO/INCIERTA.
- reporte.json: aciertos, matrices de confusión categoría/prioridad, desacuerdos y falsos negativos de Alta; ejecución parcial nunca cumple las metas.

Cada respuesta válida registra modelo efectivo, ID de respuesta y tokens reportados cuando están disponibles; ausencias son desconocidas, no cero. No se guardan claves, cuerpos de excepción ni cabeceras del proveedor. Una interrupción puede dejar coste sin uso conocido; cotejar consumo de la cuenta. Un modelo alias puede resolver a versiones diferentes: revisar metadatos antes de comparar resultados.

Metas: categoría ≥45/50, prioridad ≥40/50, abstención 5/5; todos los falsos negativos de Alta requieren revisión y cualquier Alta→Baja bloquea aceptación. Los fallos y abstenciones de las 50 referencias permanecen en el denominador. Matrices: filas son etiquetas esperadas, columnas las predicciones, ABSTENCION o FALLO; incluyen solo las 50 referencias regulares.

El indicador automated_targets_met no acredita independencia ni aprobación humana. human_acceptance permanece false. Revisar etiquetas, discrepancias y limitaciones antes de aceptar RF-3, incluso si se cumplen porcentajes.

Cálculo posterior sin llamadas, desde backend:

~~~powershell
./.venv/Scripts/python.exe -m app.ai.evaluate ../docs/evaluacion_ia/referencias-congeladas-v1.json ../docs/evaluacion_ia/ejecucion-v1/predicciones.json
~~~

## Alcance de la comprobación

El ejecutor se prueba con proveedor simulado; esos resultados temporales no son predicciones ni medición de precisión. La prueba manual 71–73 es evidencia funcional separada. Aceptación RF-3 pendiente: la ejecución externa v1 falló las metas de calidad. No hacen falta 55 capturas de pantalla.

Fuentes de contrato: [salidas estructuradas oficiales](https://developers.openai.com/api/docs/guides/structured-outputs) y proveedor productivo app/ai/provider.py. El prompt permanece plurione-classify-v1; no se incorporaron etiquetas ni justificaciones de referencia.
## Resultado de ejecución v1

55/55 respuestas externas verificadas. Categoría 32/50 y prioridad 30/50: no cumplen metas; abstención 5/5. Un falso negativo Alta (abstención), cero Alta→Baja. Modelo efectivo gpt-4.1-mini-2025-04-14. Ver [RESULTADOS_V1.md](RESULTADOS_V1.md) y archivos originales en ejecucion-v1. Sustituye el estado anterior de ejecución pendiente. No volver a ejecutar este conjunto para mejorar puntuación: ahora sirve como línea base de desarrollo/diagnóstico; nueva versión del prompt y otro conjunto independiente para aceptación están pendientes. No se cambiaron referencias ni respuestas.
## Siguiente versión del prompt

API 0.10.1 usa plurione-classify-v2 y hash separado de instrucciones. Este directorio raíz y ejecucion-v1 se conservan como referencia histórica de desarrollo. Las órdenes anteriores de envío v1 no deben repetirse con v2: el ejecutor detecta la diferencia y bloquea mezcla. La recomputación offline de evaluate permanece disponible sin proveedor. Revisar el [candidato nuevo](candidato-v2/REVISION.md) y [su guía](candidato-v2/README.md) antes de congelar y ejecutar otra evaluación. Borrador con vista previa permitida, envío bloqueado, sin predicciones ni aceptación humana. No se certifica independencia por compartir rúbrica o tener textos distintos.
## Aceptación v2 fijada tras revisión

La autora confirmó revisión y conformidad con los 55 casos nuevos. [aceptacion-v2/README.md](aceptacion-v2/README.md) contiene versión fijada y comando simplificado. El candidato se conserva como historial. Envío/medición externa y revisión de resultados pendientes; conformidad de etiquetas no equivale a aceptación de calidad ni revisión independiente de terceros.
## Resultado externo v2 registrado

[RESULTADOS_V2.md](RESULTADOS_V2.md): 49/50 categoría, 40/50 prioridad, 5/5 abstención; sin falsos negativos Alta. Metas numéricas cumplidas, prioridad en el umbral y diez Media→Baja conservadas. Originales en ejecucion-v2 y evidencia 78. No repetir para optimizar puntuación ni modificar referencias. human_acceptance=false sigue diferenciando metas automáticas de aceptación humana/integral. Sin nuevas llamadas en revisión.
## Mejora dirigida Media/Baja v3

La autora pidió mejorar la debilidad residual v2. [Candidato-v3](candidato-v3/README.md) y [revisión de pares](candidato-v3/REVISION.md): 20 pares Media/Baja, 10 Alta y 5 abstenciones, todavía sin revisar/fijar ni enviar. API 0.10.2/prompt v3 y nuevas métricas por clase probados con 154 tests, no con predicciones v3. [Diagnóstico histórico separado](DIAGNOSTICO_MEDIA_BAJA_V2.json) conserva Media 50%/Baja 100% sin modificar reporte original. V1/v2 quedan históricos; no mezclar scripts o manifiestos con v3.
## Aceptación v3 fijada tras revisión

La autora confirmó revisión y etiquetas/justificaciones de pares, Alta y abstenciones. [Versión fijada v3](aceptacion-v3/README.md), sin cambios de datos o pares; candidato preservado. Cuatro controles del comando con Docker simulado correctos, sin predicciones ni llamadas reales. Falta ejecutar y revisar métricas específicas Media/Baja y globales; conformidad de etiquetas no certifica mejora o calidad del modelo.
## Resultado externo v3

[RESULTADOS_V3.md](RESULTADOS_V3.md): Media/Baja 20/20 y pares 20/20, pero cuatro Alta→Media (6/10 Alta). Global categoría 98%/prioridad 92% y abstención 5/5. Referencias y originales ejecucion-v3 preservados, evidencia 82. Indicadores automáticos true no justifican aplicar v3 o aceptar prioridad integral. No repetir por mejorar puntuación ni cambiar referencias; resolver/verificar urgentes sin perder distinción, con nueva evaluación adecuada después de ajuste.

## Alta v4: lista para evaluación externa

API 0.10.3/prompt v4 refuerza Alta por plazos/pérdidas graves sin exigir peligro físico, conservando Media/Baja. Referencias v4 fijadas tras conformidad declarada; 160 pruebas backend aprobadas con PostgreSQL aislado, sin llamadas nuevas ni precisión v4 medida. Nuevos indicadores señalan cualquier Alta omitida aunque cumplan los promedios. Guía: docs/evaluacion_ia/aceptacion-v4/README.md; evidencia 83.

Desde raíz: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V4.ps1` valida sin gasto. Añadir `-Ejecutar` para evaluación externa con cargos posibles y máximo 55 intentos acumulados; conservar ejecucion-v4/diario ante fallo. No usar scripts anteriores con prompt v4. La evaluación no actualiza procesos operativos ni acepta calidad; revisar Alta 20/20, Media/Baja ≥12/15 cada una y quince pares además de metas globales.

## Resultado externo v4

Prioridad 50/50: Alta 20/20, Media 15/15, Baja 15/15, pares 15/15 y abstenciones 5/5; categoría 47/50 (94%). Cero Alta omitidas, metas numéricas cumplidas en este conjunto. Tres diferencias Ausencias/Administrativas conservadas; validación humana obligatoria y aceptación integral pendiente. Informe RESULTADOS_V4.md en docs/evaluacion_ia y evidencia 84. Sin llamadas adicionales ni despliegue operativo acreditado. No repetir evaluación para mejorar puntuación; continuar correo y analítica.
