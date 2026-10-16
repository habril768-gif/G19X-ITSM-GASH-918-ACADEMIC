# Evidencias verificadas

Capturas proporcionadas por la autora e inspeccionadas el 15 de octubre de 2026:

- [01-api-health-200.png](01-api-health-200.png): respuesta HTTP real 200 y JSON de disponibilidad.
- [02-compose-servicios.png](02-compose-servicios.png): construcción y servicios API, PostgreSQL y Redis healthy.
- [03-postgres-select.png](03-postgres-select.png): SELECT 1, una fila.
- [04-redis-ping.png](04-redis-ping.png): respuesta PONG.

Alcance y limitaciones en [REPORTE_QA.md](../REPORTE_QA.md). No contienen contraseñas visibles. Las capturas no acreditan funcionalidades del MVP aún pendientes.

Evidencias adicionales verificadas: [05-migracion-inicial.png](05-migracion-inicial.png), revisión 0001 y esquema alineado; [06-api-db-health-200.png](06-api-db-health-200.png), conexión real HTTP 200. Próxima evidencia pendiente: 07-usuarios-demo.png.

- [07-usuarios-demo.png](07-usuarios-demo.png): carga inicial, 2 departamentos y 6 usuarios.
- [08-usuarios-demo-sin-duplicados.png](08-usuarios-demo-sin-duplicados.png): repetición, 0 departamentos y 0 usuarios nuevos.

Ambas capturas fueron inspeccionadas y documentadas en REPORTE_QA.md.

Autenticación local: siguientes evidencias pendientes 09-migracion-auth-local.png, 10-auth-me.png y 11-logout-sesion-revocada.png. No guardar contraseñas, tokens, cuadros Authorize ni encabezados Authorization en capturas. Instrucciones en AUTENTICACION.md.

09–11: migración 0002, usuario autenticado y rechazo de sesión posterior verificados visualmente. La captura 10 conserva únicamente la versión redactada a partir del original, con bloque sensible opaco. Próximas evidencias pendientes: 12-migracion-incidencias.png y 13-db-health-0003.png.

- [12-migracion-incidencias.png](12-migracion-incidencias.png): revisión 0003 y esquema alineado.
- [13-db-health-0003.png](13-db-health-0003.png): conexión real PostgreSQL con HTTP 200.

Ambas inspeccionadas el 16 de octubre de 2026; limitaciones en REPORTE_QA.md.

Próximas evidencias previstas: 14-registro-incidencia-201.png y 15-listado-incidencias-200.png, solo Server response con datos simulados y sin token/Curl.
