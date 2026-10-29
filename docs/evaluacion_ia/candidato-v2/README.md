# Candidato de evaluación para prompt v2

Estado: borrador, sin predicciones y pendiente de revisión de la autora. Textos y etiquetas propuestos por el asistente a partir del PRD, después de fijar las instrucciones v2. No se han enviado al modelo evaluado. No se atribuye revisión independiente de terceros ni independencia estadística por tratarse de textos nuevos.

## Qué revisar

Abrir [REVISION.md](REVISION.md). Contiene 50 casos regulares con etiqueta/justificación y cinco de abstención, todos ficticios: 10 por categoría y prioridades 15 Alta, 20 Media y 15 Baja. La categoría se propone por hecho principal y la prioridad por amenaza, impacto operativo y plazo, conforme al PRD. Si un caso admite más de una referencia razonable, aclararlo antes de fijar; no ajustarlo después de conocer predicciones.

Los 55 textos e IDs son distintos del conjunto v1; se verificó cero coincidencias textuales exactas. Comparten categorías, rúbrica y autoría del asistente, por lo que eso no certifica independencia. El conjunto v1 ya observado queda reservado para desarrollo, nunca se modifica para convertir errores en aciertos.

## Archivos

- referencias.json: etiquetas y justificaciones propuestas.
- entradas.json: proyección sin etiquetas ni justificaciones, en orden entrelazado.
- catalogo.json: catálogo autorizado; ENTORNO se restringe a Riesgos.
- manifest.json: labels_frozen=false y conformidad aún no registrada; hashes normalizados UTF-8/LF del contenido, proveedor e instrucciones v2.

El prompt contiene reglas generales del PRD, no IDs, textos, etiquetas concretas ni ejemplos de este conjunto. Las instrucciones se fijaron antes de preparar estos casos y no se ajustaron con sus predicciones.

## Validación sin llamadas

Desde backend:

~~~powershell
./.venv/Scripts/python.exe -m app.ai.run_evaluation --dataset ../docs/evaluacion_ia/candidato-v2
~~~

La vista previa verifica hashes, distribución, ámbitos, texto minimizado y correspondencia de entradas/referencias. Debe indicar borrador y «Sin llamadas». La orden no necesita clave ni base de datos/Redis. Enviar con --execute permanece bloqueado mientras no exista versión fijada y conformidad registrada; las casillas de CLI por sí solas no convierten este borrador en aprobado.

No se han generado predicciones v2 ni medido calidad. Las salidas simuladas de tests no se guardan como resultados externos.

## Después de revisar

Registrar la conformidad o correcciones reales, fijar una versión de aceptación y sus hashes antes de llamadas. Preparar la ejecución con el modelo local ya seleccionado y una carpeta nueva de salida exclusiva de v2. No cambiar modelo de forma silenciosa ni reutilizar ejecucion-v1.

Aplicar API 0.10.1/worker v2 antes de solicitar nuevas asistencias, sin migración adicional (esquema 0005). Evitar solicitudes durante reconstrucción y mantener ambos procesos en la misma versión. Los trabajos pendientes de v1 se omiten por discrepancia de versión, sin reenviar automáticamente; las sugerencias ya completadas se conservan con su procedencia. Clasificación oficial/manual e historial no se reescriben.

La nueva llamada externa puede generar cargos y deberá mantener el límite de intentos, diario y reanudación existentes. No se incluye una orden para lanzar este borrador sin revisión.

## Alcance de la corrección

plurione-classify-v2 agrega definiciones del catálogo y prioridades del PRD, contexto de simulación confirmada, separación categoría/urgencia y criterios generales para asistencia e incumplimientos. Conserva entrada no confiable, abstención, ausencia de herramientas/sanciones, salida estructurada, store=false y validación humana.

La suite comprueba contratos, separación de mensajes y controles de ejecución. No demuestra que un modelo real siempre ignore una inyección o alcance las metas. El cambio no permite aceptar RF-3 sin evaluación real y revisión de calidad/procedencia.

Fuente de diseño: [guía oficial de instrucciones y contexto](https://developers.openai.com/api/docs/guides/prompt-engineering). Las reglas de negocio proceden del PRD local.
## Versión revisada fijada

La autora declaró que revisó los 55 casos y está de acuerdo con categorías/prioridades/justificaciones. Se conserva este borrador como historial de preparación; la versión fijada está en [aceptacion-v2](../aceptacion-v2/README.md), sin cambios de texto/etiquetas. Las notas de revisión pendiente de este documento describen su preparación original; no debe volver a solicitarse esa misma revisión. Predicciones y calidad externa siguen pendientes.
