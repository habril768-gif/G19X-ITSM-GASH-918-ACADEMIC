# Resultado de evaluación IA — ejecución v2

## Resultado verificado

Se completaron 55 intentos externos y 55 respuestas. La recomputación offline coincide con el reporte original; diario, entradas, referencias, catálogo, proveedor y prompt corresponden a la versión fijada antes de ejecutar. Sin llamadas adicionales durante esta revisión.

| Medida | Resultado | Meta del PRD | Resultado numérico |
| --- | --- | --- | --- |
| Categoría | 49/50 (98 %) | ≥45/50 (90 %) | Cumple |
| Prioridad | 40/50 (80 %) | ≥40/50 (80 %) | Cumple en el umbral |
| Abstenciones separadas | 5/5 | 5/5 | Cumple |
| Alta identificada | 15/15 | Revisar cualquier falso negativo | Sin falsos negativos |
| Alta → Baja | 0 | 0 | Cumple |

automated_targets_met=true. human_acceptance=false se conserva tal como lo genera el ejecutor; no se convierte en aprobación final de la autora ni del sistema completo. El cumplimiento se limita a este conjunto sintético y no garantiza calidad general, privacidad completa ni operación productiva. La validación humana sigue siendo obligatoria.

## Integridad, modelo y uso

- Modelo solicitado: gpt-4.1-mini.
- Modelo efectivo en 55 respuestas: gpt-4.1-mini-2025-04-14.
- Prompt: plurione-classify-v2, con hashes de proveedor e instrucciones iguales al manifiesto fijado.
- Datos: aceptacion-v2, 50 referencias y cinco abstenciones, etiquetas revisadas y aprobadas según declaración previa de la autora; no se atribuye revisión de terceros.
- Diario: 55 START/END, correspondencia exacta con predicciones y 55 IDs de respuesta únicos.
- Cero fallos de transporte/esquema o envíos inciertos registrados; ninguna abstención en las 50 referencias regulares.
- Uso reportado: 49321 tokens de entrada, 4191 de salida y 53512 totales. No se consultaron saldo, factura ni coste.
- Marcas UTC de los archivos: inicio 2026-10-18T21:45:24 y reporte 2026-10-18T21:46:47.
- Evidencia estructurada: ../evidencias/78-evaluacion-ia-resultado-v2.json. Originales preservados en ejecucion-v2.

## Desglose

| Categoría esperada | Aciertos |
| --- | --- |
| Ausencias | 9/10 |
| Conflictos | 10/10 |
| Incumplimientos | 10/10 |
| Riesgos | 10/10 |
| Solicitudes Administrativas | 10/10 |

| Prioridad esperada | Aciertos |
| --- | --- |
| Alta | 15/15 |
| Media | 10/20 |
| Baja | 15/15 |

La mitad de las referencias Media se clasificó como Baja. Aunque el porcentaje global cumple el umbral, este patrón tiene relevancia operativa y debe constar como limitación; no se automatiza la prioridad oficial. No hubo Media→Alta ni Baja→Alta en esta ejecución.

## Revisión técnica de las 11 discrepancias

| ID | Referencia fijada | Respuesta | Observación |
| --- | --- | --- | --- |
| NUEVO-C1-02 | Ausencias/Media | Ausencias/Baja | Hay redistribución de trabajo requerida hoy; el motivo del modelo enfatiza ausencia de daño grave. |
| NUEVO-C1-04 | Ausencias/Media | Ausencias/Baja | Atención pendiente que requiere apoyo hoy; el modelo enfatiza falta de peligro/urgencia. |
| NUEVO-C1-05 | Ausencias/Baja | Solicitudes Administrativas/Baja | Frontera semántica: aclaración documental de una falta histórica; la referencia previa conserva Ausencias. |
| NUEVO-C1-07 | Ausencias/Media | Ausencias/Baja | Trabajo incompleto antes del siguiente turno; ausencia de amenaza no elimina por sí sola impacto operativo. |
| NUEVO-C2-04 | Conflictos/Media | Conflictos/Baja | Entrega de esta tarde afectada; el motivo se centra en falta de violencia. |
| NUEVO-C2-07 | Conflictos/Media | Conflictos/Baja | Retraso del plan de mañana; no tener amenaza no equivale necesariamente a falta de atención pronta. |
| NUEVO-C3-02 | Incumplimientos/Media | Incumplimientos/Baja | Revisión necesaria para continuar mañana; se enfatiza que no hay consecuencias graves. |
| NUEVO-C3-04 | Incumplimientos/Media | Incumplimientos/Baja | Materiales pendientes para esta tarde; impacto próximo subvalorado respecto a la referencia. |
| NUEVO-C4-02 | Riesgos/Media | Riesgos/Baja | Riesgo contenido con reparación antes de reabrir la próxima semana; frontera de urgencia que requiere criterio humano. |
| NUEVO-C5-04 | Solicitudes Administrativas/Media | Solicitudes Administrativas/Baja | Revisión de mañana se retrasa sin documentación; el motivo descarta prioridad al no existir urgencia elevada. |
| NUEVO-C5-07 | Solicitudes Administrativas/Media | Solicitudes Administrativas/Baja | Gestión detenida esta semana; el modelo enfatiza ausencia de amenaza o vencimiento grave. |

Se conservaron etiquetas y respuestas sin cambios, también en los casos semánticamente discutibles. No se eleva la puntuación corrigiendo referencias retrospectivamente. Esta es revisión técnica del asistente, no nueva aprobación humana de los resultados. No hay falsos negativos de Alta que requieran análisis adicional en esta ejecución.

## Interpretación y límites

El conjunto v2 se redactó después de fijar el prompt v2 y sus etiquetas se revisaron antes de observar predicciones. Comparte autoría sintética y rúbrica con v1; no se certifica independencia estadística ni revisión de terceros.

V1 y v2 usan textos distintos. Sus porcentajes no prueban por sí solos el efecto causal aislado del cambio de prompt. El resultado v2 sí verifica que el modelo/prompt evaluados cumplen los umbrales de ingeniería del PRD en estas referencias.

No se ajustará de nuevo el prompt usando este conjunto y se seguirá llamando prueba independiente al mismo tiempo. Cualquier ajuste guiado por estas respuestas exige otro conjunto para una futura aceptación. El módulo conserva sugerencias separadas de decisiones oficiales y su revisión humana.

## Continuación del proyecto

No repetir ejecucion-v2 ni generar más llamadas para intentar mejorar la puntuación. Registrar el cumplimiento numérico y mantener pendiente la aceptación integral y las comprobaciones restantes de operación.

Aplicar API 0.10.1 y worker v2 juntos al producto antes de nuevas solicitudes operativas, siguiendo IA.md; el contenedor de evaluación no actualizó esos procesos. No hay nueva migración sobre 0005. Después continuar H8: correo por eventos con capturador SMTP y verificación de permisos antes de envío. H9 analítica y QA integral permanecen pendientes.

No se modificaron prompt, datos, configuración local ni código durante esta revisión, y no se repitieron suites o llamadas externas.
