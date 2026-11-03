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
| RF-4 Gestión y protección | Clasificación, responsable, estados, reapertura, participantes y confidencialidad | A10 requiere completar el recorrido de dos roles |
| RF-5 Correo | Avisos de creación, asignación, resolución, cierre y reapertura mediante outbox | Mailpit local; A09 requiere un caso negativo documentado |
| RF-6 Analítica | Vistas agregadas, supresión por privacidad, cuenta de lectura y Power BI Desktop | Se conservan exclusiones, corte y límites de la población exportable |
| RF-7 Administración | Alta y actualización de cuentas y departamentos, baja lógica y auditoría | Recorridos de administración y denegaciones documentados |
| RF-8 Panel | Bandeja, búsqueda, filtros, paginación y consulta según permisos | Filtro «Sin responsable» y limpieza comprobados en 259 |
| RNF-2 Rendimiento | Protocolo HTTP QA cumplido en el entorno Linux CI documentado | [Evidencia 270](evidencias/270-rnf2-linux-ci-aprobado.json); A01 cerrado en ese alcance |

## Condiciones para dar la entrega por terminada

**Fecha de entrega: 5 de noviembre de 2026.** Fijada por la autora el 2 de noviembre.

1. Completar los recorridos pendientes de la [matriz de aceptación](ACEPTACION_ENTREGA.md),
   empezando por A09 (correo negativo), A10 (confidencialidad con dos roles) y A14 (manual).
2. Registrar para cada recorrido el resultado real, su evidencia y las limitaciones.
   Una prueba automática o una pantalla implementada no sustituyen el recorrido manual.
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
