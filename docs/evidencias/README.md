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
