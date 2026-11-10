# Alcance y aceptación del MVP

## Objetivo

Gestionar incidencias laborales simuladas desde su registro hasta su cierre,
con acceso por rol, revisión humana, auditoría y protección de la información.
Las reglas de negocio se detallan en el [PRD](PRD.md).

## Funciones implementadas

| Requisito | Función de la entrega | Validación y límite |
| --- | --- | --- |
| RF-1 Identidad | Acceso local, sesiones revocables, cambio de contraseña y bloqueo de intentos | Pruebas automáticas y recorridos registrados en la matriz |
| RF-2 Expedientes | Registro PERSONA/ENTORNO, filtros, detalle e historial autorizado | Evidencia por rol; conservar los casos de prueba existentes |
| RF-3 Asistencia IA | Texto simulado revisado, cola durable, sugerencia y clasificación humana | Evaluación conservada; la sugerencia requiere validación de una persona |
| RF-4 Gestión y protección | Clasificación, responsable, estados, reapertura, participantes y confidencialidad | A10 documenta el acceso de Empleado y Supervisor antes y después de restringir el caso, con Admin RH como control |
| RF-5 Correo | Avisos de creación, asignación, resolución, cierre y reapertura mediante outbox | A09 documenta en Mailpit un destinatario inactivo excluido del aviso de creación, con entrega de control a Admin RH |
| RF-6 Analítica | Vistas agregadas, supresión por privacidad, cuenta de lectura y Power BI Desktop | Se conservan exclusiones, corte y límites de la población exportable |
| RF-7 Administración | Alta y actualización de cuentas y departamentos, baja lógica y auditoría | Recorridos de administración y denegaciones documentados |
| RF-8 Panel | Bandeja, búsqueda, filtros, paginación y consulta según permisos | Filtro «Sin responsable» y limpieza comprobados en 259 |
| RNF-2 Rendimiento | Protocolo HTTP QA cumplido en el entorno Linux CI documentado | [Evidencia 270](evidencias/270-rnf2-linux-ci-aprobado.json); A01 cerrado en ese alcance |

## Condiciones para dar la entrega por terminada

**Fecha de entrega: 5 de noviembre de 2026.** Fijada por la autora el 2 de noviembre.

La [matriz de aceptación](ACEPTACION_ENTREGA.md) registra estos recorridos:

- **A09.** La [evidencia 275](evidencias/275-corte4-a09-destinatario-inactivo.json)
  documenta el aviso de creación en Mailpit. La cuenta RH inactiva quedó fuera
  de los destinatarios y Admin RH recibió el aviso de control. Los fallos SMTP
  y los reintentos reales quedan pendientes.
- **A10.** La [evidencia 279](evidencias/279-corte4-a10-confidencialidad-por-roles.json)
  documenta que Empleado y Supervisor podían consultar el caso antes de restringirlo.
  Después, ambos perdieron acceso y Admin RH lo conservó. Queda pendiente la
  revisión integral de participantes y conflictos de interés.
- **A14.** La [evidencia 285](evidencias/285-corte4-a14-recorrido-manual-confirmado.json)
  registra el recorrido del manual, que cubrió consulta de expedientes,
  administración en lectura, correo y BI. El equipo evaluador verificó ese
  recorrido el 6 de noviembre, según el [corte 5](RETROALIMENTACION_CORTE5.md).
  La capacitación y la aceptación formal quedan pendientes.

Para el cierre de la entrega:

1. Consultar la matriz para identificar los escenarios parciales y pendientes.
2. Registrar los resultados de las verificaciones adicionales con su evidencia
   y alcance.
3. Mantener disponibles los manuales y la evidencia de instalación, respaldo y recuperación.
   Los ensayos 255 y 256 y la comprobación local 272 conservan sus alcances documentados.
4. Preparar código, documentos y guion de demostración con una versión identificada.
5. Adaptar el informe académico cuando se reciba la plantilla y registrar la aceptación
   o capacitación a terceros cuando ocurran.

El [plan de cierre](BACKLOG.md) organiza el trabajo del 2 al 5 de noviembre.

## Fuera del alcance actual

Entra ID, nómina, SLA y alertas por tiempo, aplicación móvil nativa, registro público,
recuperación automática por correo y despliegue productivo con datos laborales reales.
El envío a buzones externos fue diferido por la autora; Mailpit captura los avisos locales.
Los agregados de Power BI representan la población exportable, no el total de la empresa.

## Dónde están las evidencias

- [Aceptación por roles](ACEPTACION_ENTREGA.md): recorridos y pendientes de entrega.
- [Trazabilidad](TRAZABILIDAD.md): requisitos, implementación y pruebas.
- [Reporte de QA](REPORTE_QA.md): procedencia y alcance de las validaciones.
- [Bitácora](BITACORA.md): antecedentes, fechas y detalle de las corridas.
- [Observaciones del corte 4](RETROALIMENTACION_CORTE4.md): atención y comprobación de cada punto.
