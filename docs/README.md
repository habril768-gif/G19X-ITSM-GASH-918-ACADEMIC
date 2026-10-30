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

[Respuesta al corte del 23 de octubre](AUDITORIA_2026-10-23.md): guía, UTF-8, publicación y aviso de cierre RF-5.

[Análisis de la evaluación recibida](REVISION_EVALUACION.md): hallazgos confirmados, observaciones desactualizadas y prioridades.

## Evidencia e historial

- [Reporte QA](REPORTE_QA.md): resultados reales, alcance y limitaciones.
- [Bitácora](BITACORA.md): secuencia de avances con fechas y validación.
- [Decisiones](DECISIONES.md): motivos técnicos y cambios de alcance.
- [Evaluación IA](evaluacion_ia/README.md): referencias, ejecuciones y resultados conservados para auditoría.
- `evidencias/`: capturas y registros sanitizados; un archivo no acredita por sí solo aceptación integral.

Las guías principales describen el estado actual. Los números de dependencias, migraciones y evaluaciones identifican artefactos técnicos reproducibles; no son capítulos del manual. La copia Word del PRD y los registros cronológicos se conservan como referencias históricas, sin sustituir el PRD Markdown ni las matrices vigentes.

El [control opcional de estadísticas SQL QA](PRUEBA_RENDIMIENTO.md#consultas-reales-estadísticas-de-ejecución-del-servidor-qa) mide ejecución de consultas reales sin modificar el sitio. Su estado y límites se registran en las evidencias207/208; RNF-2 sigue pendiente.

La [comparación de uno y dos procesos API](PRUEBA_RENDIMIENTO.md#comparación-breve-de-uno-y-dos-procesos-api) usa dos QA nuevos y no cambia el despliegue operativo. Preparación y límites en211; resultados reales todavía pendientes.


### 2026-10-30 — RNF-2: formal QA de dos procesos preparada

[Evidencia213](evidencias/213-formal-qa-dos-procesos-preparada.json): opcion explicita `--api-workers 2` en run_performance_full_guarded.py; conserva protocolo10clientes/30+300s/p95<200ms, guardas CPU/redes e integridad.126 unitarias aprobadas; ejecución formal real pendiente. Ver comando y límites en [prueba de rendimiento](PRUEBA_RENDIMIENTO.md). La restricción histórica de dos procesos solo smoke se amplía a full sin diagnóstico; sitio sin cambios.
