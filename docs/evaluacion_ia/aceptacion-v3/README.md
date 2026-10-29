# Evaluación de aceptación v3 — Media/Baja

Versión fijada después de que la autora declarara revisar los pares Media/Baja, casos Alta y abstenciones y estar de acuerdo con etiquetas y justificaciones. Conformidad declarada antes de predicciones; sin revisión independiente de terceros ni garantía estadística.

## Integridad y diseño

referencias.json, entradas.json y catalogo.json conservan los mismos contenidos JSON y hashes normalizados UTF-8/LF del candidato revisado. Manifest fija prompt v3, proveedor e instrucciones, sin cambiar etiquetas ni justificaciones. El candidato-v3 permanece como historial.

50 referencias: 10 Alta, 20 Media y 20 Baja, diez casos por categoría. Las 40 referencias Media/Baja forman veinte pares contrastivos con hecho base/categoría comunes y distinta necesidad de atención operativa. Cinco casos adicionales requieren abstención. IDs/etiquetas/justificaciones y pair_id no se envían al proveedor.

## Comando desde raíz

Comprobar sin gasto:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V3.ps1
~~~

Ejecutar evaluación externa:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V3.ps1 -Ejecutar
~~~

-Ejecutar puede generar cargos. El script valida archivos con Python local, construye la imagen ai-worker y ejecuta el evaluador en Docker con el modelo/clave ya configurados por Compose. No imprime credenciales ni lee el .env para mostrarlas. No usa base de datos/Redis ni crea incidencias; tampoco actualiza contenedores operativos API/worker.

Límite acumulado de 55 intentos y salida fija ../ejecucion-v3; conservar diario/carpeta al reanudar. No borrar ni cambiar directorio para repetir envíos. Un envío incierto se conserva y no se reenvía automáticamente. Este límite no garantiza techo monetario; revisar uso real de la cuenta.

## Resultados pendientes

La preparación solo comprobó cuatro controles con Docker simulado: parser, vista previa sin Docker, argumentos de dataset/salida/límite y detención ante fallo de construcción. Sus mensajes de ejecución no acreditan llamadas ni resultados externos. No existen predicciones v3 todavía.

Tras ejecución real, revisar reporte.json, predicciones.json, journal.jsonl y run.json en ejecucion-v3.

- Metas globales: categoría ≥45/50, prioridad ≥40/50, abstención 5/5, cero Alta→Baja y revisión de todo falso negativo Alta.
- Objetivo específico: Media ≥16/20 y Baja ≥16/20; no mejorar Media a costa de clasificar todas como Media.
- Informar los veinte pares y cuántos aciertan ambos niveles de prioridad; categoría se puntúa por separado.
- Sin referencias de clase suficientes, el indicador complementario es null, no un acierto perfecto.
- automated_targets_met/media_baja_targets_met no equivalen a aceptación humana ni garantía general.

No modificar etiquetas después de ver respuestas para mejorar métricas. Si el conjunto se usa para ajustar el prompt, reservar otro para aceptación posterior. Referencias y resultados v1/v2 se conservan; no usar sus scripts con hashes alterados para ejecutar v3.

La validación humana oficial del expediente sigue siendo obligatoria. Aún no se demuestra mejora real Media/Baja por haber preparado y probado el comando. No se requiere una captura por caso: basta resultado final y revisión directa de archivos.
## Ejecución real y limitación detectada

La evaluación ya fue ejecutada; las notas previas de resultado pendiente describen la preparación. [RESULTADOS_V3.md](../RESULTADOS_V3.md) verifica Media/Baja y pares 100%, pero cuatro Alta→Media (6/10 Alta). Global 98% categoría/92% prioridad y abstención 5/5 no justifican aceptación integral. No volver a ejecutar para obtener una puntuación favorable, alterar referencias o borrar diario. Conservar resultados y resolver/verificar los urgentes. No se recomienda aplicar v3 al producto por este resultado.
