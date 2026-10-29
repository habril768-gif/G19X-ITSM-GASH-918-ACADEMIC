# Prioridad Alta sin perder Media/Baja — referencias fijadas v4

Estado: etiquetas fijadas tras revisión y conformidad explícitas de la persona responsable, sin predicciones ni envío. Casos sintéticos preparados por asistente después de fijar las instrucciones v4; no se atribuye revisión independiente de terceros ni independencia estadística.

## Qué cambia

API 0.10.3/prompt plurione-classify-v4 conserva la regla Media/Baja y refuerza tres criterios suficientes alternativos de Alta: amenaza inmediata de seguridad, conflicto activo con riesgo de daño o plazo/evento inminente con consecuencia grave descrita. No se exige peligro físico para el tercero, ni cumplir simultáneamente todos los criterios. Una vez identificado un criterio suficiente, la categoría administrativa o el impacto operativo no rebajan la prioridad. El motivo y la prioridad deben ser coherentes; no inventar gravedad a partir de una fecha aislada.

No se agrega un clasificador por palabras clave, reglas de elevación masiva ni modificación automática de prioridad oficial. Las salidas siguen como sugerencias y la revisión humana es obligatoria. No cambió la selección local de modelo ni el contrato HTTP.

## Diseño para revisar

[REVISION.md](REVISION.md) contiene 50 referencias: 20 Alta, 15 Media y 15 Baja (diez por categoría), más cinco abstenciones.

- Alta: doce plazos/pérdidas graves no físicas, cuatro conflictos activos y cuatro amenazas inmediatas de seguridad.
- Quince contrastes con un hecho base y tres consecuencias Alta/Media/Baja; las versiones Media/Baja forman quince pares medidos.
- Cinco casos Alta adicionales, uno por categoría.
- high_trigger/pair_id, etiquetas y justificaciones quedan solo en referencias; entradas.json no los incluye. Solo texto y catálogo llegan al proveedor.
- Cero coincidencias textuales exactas con v1/v2/v3; eso no certifica independencia ni representatividad.

La persona responsable declaró su conformidad con etiquetas y justificaciones; esto no acepta resultados del modelo. Revisar durante el análisis si cada consecuencia grave está sustentada, si Media requiere atención pronta y si Baja carece de necesidad operativa urgente. No convertir todo plazo en Alta ni todo trámite en Media. Corregir o sustituir referencias antes de fijar, nunca después de observar predicciones para elevar porcentajes.

## Indicadores sin ocultar Alta

El evaluador conserva automated_targets_met y media_baja_targets_met, pero añade:

- all_high_priority_identified: true solo con al menos diez referencias Alta y ningún falso negativo (incluye Alta→Media, Alta→Baja, abstenciones o fallos); null con muestra insuficiente.
- priority_checks_met: combina metas globales, Media/Baja y todos los Alta identificados; null si falta muestra por clase. Una ejecución parcial lo fuerza a false. No equivale a aceptación humana ni habilita despliegue.
- Se mantienen matrices, discrepancias, listas de falsos negativos y pares.

[DIAGNOSTICO_ALTAS_V3.json](../DIAGNOSTICO_ALTAS_V3.json) recalcula respuestas históricas: global y Media/Baja true, pero Alta y el indicador combinado false por cuatro Alta→Media. No modifica reporte original ni es una medición del prompt v4.

Objetivos para esta mejora: al menos 45/50 categorías, 40/50 prioridades, 5/5 abstenciones, 12/15 tanto Media como Baja y 20/20 Alta; revisar los quince pares completos. Aunque se cumplan, hace falta revisión de resultados/procedencia y aceptación integral.

## Comando sin gasto

Desde raíz:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V4.ps1
~~~

Verifica hashes y estructura de aceptacion-v4 sin Docker/modelo. La opción -Ejecutar construye la imagen y habilita una evaluación externa con cargos posibles. No modificar manualmente banderas ni los hashes de versiones anteriores para saltar la revisión.

La revisión fue declarada y las referencias se fijaron antes de llamadas, con salida exclusiva ejecucion-v4 y límite de 55 intentos acumulados. Mantener diario para reanudar sin reenviar casos intentados. No repetir indefinidamente por buscar una puntuación favorable ni presentar un conjunto utilizado para ajuste como aceptación independiente.

El código preparado no se ha aplicado a Docker ni se ha medido v4. Actualizar API/worker juntos cuando corresponda, sin migración adicional a 0005; jobs pendientes v1/v2/v3 se omiten antes de envío por discrepancia de versión, y sugerencias completadas se conservan. No crea incidencias durante evaluación.

Fuente de diseño: [guía oficial de instrucciones y evaluaciones](https://developers.openai.com/api/docs/guides/prompt-engineering); reglas del PRD local.

Desde la raíz, para medir con el proveedor real (puede consumir saldo):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V4.ps1 -Ejecutar
```

Esta orden evalúa; no actualiza los contenedores operativos. Conservar ejecucion-v4 ante una interrupción y compartir el mensaje final. No mezclar scripts de versiones anteriores con el prompt v4.
