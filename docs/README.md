# Documentación de PluriOne

## Lectura principal

1. [Guía de inicio](../README.md): propósito, configuración y arranque.
2. [Alcance del MVP](MVP.md): qué está implementado y qué falta aceptar.
3. [Requisitos](PRD.md): reglas funcionales y límites del producto.
4. [Propuesta técnica](PROPUESTA_TECNICA.md) y [arquitectura](ARQUITECTURA.md): solución, componentes, flujos y decisiones.
5. [Backlog](BACKLOG.md): prioridades y criterios de cierre.
6. [Entregables](ENTREGABLES.md): estado académico y documental.
7. [Trazabilidad](TRAZABILIDAD.md): relación entre requisitos, código, pruebas y pendientes.

## Operación y desarrollo

| Necesidad | Guía |
| --- | --- |
| Operar el entorno y diagnosticar fallos | [Manual técnico](MANUAL_TECNICO.md), [Docker](../infra/README.md), [backend](../backend/README.md) |
| Configurar cuentas y sesiones | [Autenticación](AUTENTICACION.md), [usuarios](ADMIN_USUARIOS.md), [RH independiente](ADMIN_INDEPENDIENTE.md) |
| Usar el panel según rol | [Manual de usuario](MANUAL_USUARIO.md), [guía frontend](FRONTEND.md) |
| Registrar y gestionar expedientes | [Incidencias](INCIDENCIAS.md), [departamentos](DEPARTAMENTOS.md) |
| Mantener, respaldar y solicitar soporte | [Plan de mantenimiento](PLAN_MANTENIMIENTO.md) |
| Actualizar esquema y preparar QA | [Datos](DATOS.md), [datos DEMO](DATOS_DEMO.md), [pruebas PostgreSQL](PRUEBAS_POSTGRESQL.md) |
| Usar integraciones | [IA](IA.md), [correo](CORREO.md), [analítica](ANALITICA.md), [Power BI](../powerbi/README.md) |

## Evaluación del avance

[Informe académico en borrador](INFORME_ENTREGA_BORRADOR.md): objetivo, desarrollo, resultados, limitaciones y conclusiones para revisión.

[Resumen de entrega](RESUMEN_ENTREGA.md): resultados comprobados, límites, pendientes y preparación de la demostración.

[Respuesta al corte del 23 de octubre](AUDITORIA_2026-10-23.md): guía, UTF-8, publicación y aviso de cierre RF-5.

[Análisis de la evaluación recibida](REVISION_EVALUACION.md): hallazgos confirmados, observaciones desactualizadas y prioridades.

## Evidencia e historial

- [Reporte QA](REPORTE_QA.md): resultados reales, alcance y limitaciones.
- [Bitácora](BITACORA.md): secuencia de avances con fechas y validación.
- [Decisiones](DECISIONES.md): motivos técnicos y cambios de alcance.
- [Evaluación IA](evaluacion_ia/README.md): referencias, ejecuciones y resultados conservados para auditoría.
- `evidencias/`: capturas y registros sanitizados; un archivo no acredita por sí solo aceptación integral.

Las guías principales describen el estado actual. Los números de dependencias, migraciones y evaluaciones identifican artefactos técnicos reproducibles; no son capítulos del manual. La copia Word del PRD y los registros cronológicos se conservan como referencias históricas, sin sustituir el PRD Markdown ni las matrices vigentes.

El [control opcional de estadísticas SQL QA](PRUEBA_RENDIMIENTO.md#consultas-reales-estadísticas-de-ejecución-del-servidor-qa) mide ejecución de consultas reales sin modificar el sitio. Su estado y límites se registran en las evidencias207/208; RNF-2 cuenta con aprobación formal posterior en la [evidencia220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json).

La [comparación de uno y dos procesos API](PRUEBA_RENDIMIENTO.md#comparación-breve-de-uno-y-dos-procesos-api) usa dos QA nuevos y no cambia el despliegue operativo. Preparación y límites en211; la aprobación formal posterior con tres procesos está documentada en220. Los ensayos breves no acreditan por sí solos RNF-2.

El estado actual y los pendientes están en el [resumen de entrega](RESUMEN_ENTREGA.md) y la [matriz de aceptación](ACEPTACION_ENTREGA.md). Las notas cronológicas de preparación y fallos de rendimiento se conservan en la [bitácora](BITACORA.md).
