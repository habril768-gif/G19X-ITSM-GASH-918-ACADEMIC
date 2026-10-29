# Evaluación de aceptación v2

Versión fijada después de que la autora declarara que revisó los 55 casos y está de acuerdo con sus categorías, prioridades y justificaciones. No se atribuye revisión independiente de terceros ni garantía estadística. Textos y etiquetas propuestos por asistente a partir del PRD, sin predicciones del modelo evaluado.

## Integridad

referencias.json, entradas.json y catalogo.json son equivalentes al candidato-v2 revisado; no se alteraron textos ni etiquetas al fijar la versión. Manifest registra conformidad declarada, labels_frozen=true y hashes normalizados UTF-8/LF de datos, proveedor y prompt plurione-classify-v2. El candidato queda como historial.

El primer chequeo de igualdad de bytes detectó diferencias CRLF/LF al copiar a versión normalizada. La verificación por hashes normalizados y equivalencia JSON confirmó que no cambiaron textos/etiquetas. No se presentan diferencias de saltos de línea como cambios de contenido.

## Un solo comando

Desde la raíz, comprobación local sin llamadas ni Docker:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V2.ps1
~~~

Para ejecutar la evaluación externa:

~~~powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\EVALUAR_IA_V2.ps1 -Ejecutar
~~~

La opción -Ejecutar puede generar cargos. El script primero comprueba archivos y versión fijada con el Python del proyecto, construye la imagen ai-worker y ejecuta el bloque en Docker. Clave/modelo/configuración se obtienen del .env local mediante Compose, nunca se imprimen ni se incluyen en argumentos. Mantiene el modelo ya configurado.

Directorio de salida exclusivo: ../ejecucion-v2. No lo borrar ni cambiar para repetir la evaluación. Máximo acumulado de 55 intentos, sin reenvíos de casos ya intentados al reanudar la misma carpeta, según diario del ejecutor. Un envío incierto no se reenvía automáticamente. Límite de llamadas/salida no garantiza un techo monetario; revisar uso real.

El script construye y usa un contenedor de evaluación independiente, sin consultar PostgreSQL/Redis ni crear incidencias. No actualiza los contenedores operativos API/worker. Para aplicar API 0.10.1/prompt v2 al producto se mantienen las instrucciones de candidato-v2/README.md; no solicitar asistencia durante la actualización.

## Resultado pendiente

No se han generado predicciones de esta versión en el momento de fijarla. Los ensayos del comando usaron Docker simulado; no acreditan construcción o evaluación externa. La suite backend previa 147/147 permanece separada de esta comprobación de script.

Tras ejecución real, revisar ../ejecucion-v2/reporte.json, predicciones.json, journal.jsonl y run.json. Metas: ≥45/50 categoría, ≥40/50 prioridad, 5/5 abstenciones, cero Alta→Baja y revisión de todos los falsos negativos de Alta. execution_complete no certifica metas ni aceptación humana. No cambiar las referencias después de conocer resultados para mejorar puntuación.

Sin necesidad de 55 capturas; basta mensaje final y revisión directa de los archivos guardados. No compartir .env, clave o pantalla de credenciales. El archivo de revisión humana está en [REVISION.md](REVISION.md).
## Resultado real de esta versión

La autora ya ejecutó la evaluación; las notas anteriores de resultado pendiente describen la preparación. Ver [RESULTADOS_V2.md](../RESULTADOS_V2.md): categoría 98 %, prioridad 80 %, abstenciones 5/5, Alta 15/15. Cumple metas numéricas con diez Media→Baja y un desacuerdo de categoría; mantener validación humana. Originales ../ejecucion-v2 y evidencia 78. No repetir el comando para mejorar porcentaje, editar referencias o borrar diario. Aceptación integral/operativa y revisión de procedencia siguen diferenciadas del umbral automático.
