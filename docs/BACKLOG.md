# Plan de cierre de la entrega

**Fecha de entrega: 5 de noviembre de 2026.** Fijada por la autora el 2 de noviembre.
El trabajo se concentra en aceptación, legibilidad y documentación del MVP existente.

## Pendientes y calendario

| Prioridad | Trabajo | Fecha prevista | Estado al 2 de noviembre |
| --- | --- | --- | --- |
| 1 | Reordenar MVP y corregir redacción del README | 2 de noviembre | Publicado en 96fe0d3 |
| 2 | Dividir líneas largas de los tres archivos Python señalados | 2 de noviembre | Formato274 y CI278 aprobados |
| 3 | A09: comprobar un destinatario inactivo y un aviso de control en Mailpit | 3 de noviembre | Comprobado el 2 de noviembre en275 |
| 4 | A10: consultar un caso confidencial como Empleado y Supervisor, con control RH | 3 de noviembre | Comprobado el 2 de noviembre en279 |
| 5 | A14: seguir el manual y corregir diferencias con el panel | 4 de noviembre | Recorrido manual pendiente |
| 6 | Consolidar matriz, informe en borrador y paquete identificado | 4 de noviembre | Depende de los recorridos |
| 7 | Revisar el paquete y realizar la demostración de entrega | 5 de noviembre | Previsto; no declarar aceptación antes de realizarla |

Las fechas de las actividades son un plan de trabajo. El estado cambia con evidencia;
el calendario por sí solo no acredita una actividad realizada.

## Criterio para cerrar cada trabajo

Un cambio termina cuando es revisable, tiene la validación pertinente y registra el
resultado y sus límites. Las observaciones están en [atención del corte 4](RETROALIMENTACION_CORTE4.md).
Los recorridos de usuario se registran en [aceptación por roles](ACEPTACION_ENTREGA.md).

## Resultados que se conservan

- RF-1 a RF-8 cuentan con implementación y pruebas; los recorridos pendientes siguen visibles.
- A01 está cerrado en el alcance HTTP QA Linux de la [evidencia 270](evidencias/270-rnf2-linux-ci-aprobado.json).
- Instalación nueva y recuperación de copia: evidencias 255 y 256, con sus límites.
- Actualización local y acceso posterior: [evidencia 272](evidencias/272-actualizacion-local-salud-y-acceso-confirmados.json).
- IA, Mailpit y Power BI conservan sus resultados previos; no se amplían funciones para este cierre.

## Publicación del avance

Crear un commit por trabajo terminado, añadir solo sus archivos y subirlo el mismo día.
Comprobar que cada commit nuevo quede por debajo de 3 000 líneas cambiadas.
El criterio de dos días distintos se acredita con actividad real en dos fechas;
permanece en seguimiento hasta que eso ocurra.

## Antecedentes

El [backlog histórico hasta el 31 de octubre](BACKLOG_HISTORICO_20261031.md)
conserva el documento anterior. La [bitácora](BITACORA.md) registra cambios y resultados;
el [MVP](MVP.md) define el alcance vigente.
