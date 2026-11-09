# Demostración final de PluriOne

Duración orientativa de 7 minutos. La demostración usa el entorno académico local y expedientes ficticios ya preparados.

## Antes de presentar

- Abre el panel en http://127.0.0.1:5173/ y comprueba que http://127.0.0.1:5173/api/health/db devuelve `ok` y `postgresql`. Si la instalación está detenida, sigue el [README](../README.md).
- Prepara una sesión Admin RH y una sesión Empleado en perfiles de navegador separados. Introduce las credenciales antes de compartir pantalla.
- Deja abiertas la [matriz de aceptación](ACEPTACION_ENTREGA.md), la [evidencia del corte 5](evidencias/292-corte5-arranque-y-responsable-ui.json) y el [resultado RNF-2](evidencias/270-rnf2-linux-ci-aprobado.json).

## Recorrido

| Tiempo | Qué mostrar | Qué explicar |
| --- | --- | --- |
| 0:00–0:45 | Panel de incidencias como Admin RH | PluriOne reúne el registro, seguimiento y revisión de incidencias laborales con permisos por rol y trazabilidad. |
| 0:45–2:00 | Expediente cerrado «Prueba IA — piso mojado» | En Seguimiento aparece «RH Independiente Demo». La ficha permite revisar responsable, resolución y fechas del ciclo. |
| 2:00–3:15 | Caso «QA Corte4 A10 — acceso por confidencialidad», ID `aaa54e3c-a35b-4419-8c3d-7e8926773095` | Admin RH consulta el expediente protegido y su historial. Abre el mismo enlace como Empleado para mostrar la denegación. Las capturas 280 a 284 conservan el contraste previo y posterior con los roles probados. |
| 3:15–4:15 | Departamentos y captura 294 | El intento de alta con «DEMO - PRUEBA 1» devuelve el motivo concreto del conflicto. La captura conserva el mensaje. |
| 4:15–5:15 | «QA Corte 5 — IA desactivada, segundo intento» | El expediente recién registrado muestra «Asistencia IA no configurada. Clasificación manual.». La clasificación sigue a cargo de la persona autorizada. |
| 5:15–6:15 | Correo y Power BI | Usa la evidencia 275 para mostrar el caso negativo y su control en Mailpit. Muestra la fecha de corte y las cifras suprimidas en la copia local autorizada del informe, o consulta la evidencia 253 si Power BI Desktop no está disponible. |
| 6:15–7:00 | Informe en borrador y evidencias técnicas | Presenta el resultado RNF-2 en el runner Linux del commit medido, las pruebas del corte 5 y el enlace al repositorio. Indica el alcance académico y los puntos que corresponden a la evaluación final. |

El [registro 292](evidencias/292-corte5-arranque-y-responsable-ui.json) enlaza
las capturas del responsable, Departamentos y asistencia IA. Si un servicio
falla durante la presentación, usa esas evidencias y explica qué parte
presentas mediante capturas. Conserva el resultado real de la evaluación
en la bitácora cuando se realice.
