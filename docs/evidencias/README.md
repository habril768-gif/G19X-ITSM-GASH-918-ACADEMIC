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

Evidencias 14/15 recibidas e inspeccionadas el 16 de octubre de 2026:

- [14-registro-incidencia-201.png](14-registro-incidencia-201.png): acuse HTTP 201, received=true y can_view=true.
- [15-listado-incidencias-200.png](15-listado-incidencias-200.png): listado HTTP 200 con el mismo caso PENDIENTE y total=1.

Sin token ni Curl visibles; resultados y límites en REPORTE_QA.md.

- [16-historial-incidencia-200.png](16-historial-incidencia-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, evento CREADO y total=1 con datos simulados, sin token/Curl visibles. No sustituye pruebas entre roles.

Próximas evidencias previstas para API 0.6.0: 17-clasificacion-validada-200.png y 18-asignacion-200.png. Aún no recibidas ni verificadas. Guardar solo Server response con datos ficticios; omitir Curl/token.

- [17-clasificacion-validada-200.png](17-clasificacion-validada-200.png): revisada el 16 de octubre de 2026; HTTP 200 y classification_valid=true. Clasificación humana, sin IA ejecutada ni credenciales visibles.

- [18-asignacion-200.png](18-asignacion-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, assigned_to presente y estado PENDIENTE, sin token/Curl visibles.

- [19-en-revision-200.png](19-en-revision-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200 y estado EN_REVISION, sin token/Curl visibles.

- [20-resuelta-200.png](20-resuelta-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, RESUELTA con resolución y fecha, sin token/Curl visibles.

- [21-cerrada-200.png](21-cerrada-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, CERRADA y closed_at presente, sin token/Curl visibles.

- [22-reapertura-200.png](22-reapertura-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, EN_REVISION y campos finales nulos. Conservación del ciclo previo aún pendiente de inspección del historial. Sin token/Curl visibles.

- [23-historial-reapertura-200.png](23-historial-reapertura-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, REAPERTURA y before con estado/fechas anteriores. Recorte no permite verificar texto de resolución anterior ni motivo. Sin token/Curl visibles.

- [23b-historial-reapertura-detalle.png](23b-historial-reapertura-detalle.png): inspeccionada el 16 de octubre de 2026; completa evidencia 23 mostrando resolución/fechas anteriores y reason. Sin token/Curl visibles.

Evidencia 24-confidencialidad-200.png prevista para API 0.7.0, todavía no recibida ni verificada. Capturar Server response del detalle, sin token/Curl y con datos simulados. Guía en INCIDENCIAS.md.

- [24-confidencialidad-200.png](24-confidencialidad-200.png): inspeccionada el 16 de octubre de 2026; acuse HTTP 200 con received/can_view verdaderos. No contiene detalle de confidencialidad/IA; pendiente captura complementaria del GET. Sin credenciales visibles.

- [24b-confidencialidad-detalle-200.png](24b-confidencialidad-detalle-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, is_confidential=true y ai_status=OMITIDA con motivo. Completa acuse 24, sin token/Curl visibles.

- [25-confidencialidad-retirada-200.png](25-confidencialidad-retirada-200.png): inspeccionada el 16 de octubre de 2026; HTTP 200, is_confidential=false y ai_status=OMITIDA. Sin token/Curl visibles.

- [26-participante-declarado-201.png](26-participante-declarado-201.png): acuse HTTP 201 revisado el 16 de octubre de 2026, received/can_view verdaderos. No contiene detalle de relación ni confidencialidad. Sin credenciales visibles.

- [27-participante-declarado-detalle-200.png](27-participante-declarado-detalle-200.png): revisada el 16 de octubre de 2026; HTTP 200, DECLARADO, motivo original y revisión todavía nula. Sin credenciales visibles.

- [28-participante-confirmado-200.png](28-participante-confirmado-200.png): revisada el 16 de octubre de 2026; HTTP 200, CONFIRMADO, revisión completa y motivo original conservado. Sin credenciales visibles.

- [29-bloqueo-confidencialidad-409.png](29-bloqueo-confidencialidad-409.png): revisada el 16 de octubre de 2026; HTTP 409 esperado, impide retirar confidencialidad con gestor involucrado. Sin credenciales visibles.

- [30-participante-descartado-200.png](30-participante-descartado-200.png): revisada el 16 de octubre de 2026; HTTP 200, DESCARTADO, declaración original y revisión con motivo. Sin credenciales visibles.

- [31-confidencialidad-tras-descarte-200.png](31-confidencialidad-tras-descarte-200.png): revisada el 16 de octubre de 2026; HTTP 200, confidencialidad activa e IA omitida después de evidencia 30. Sin credenciales visibles.

- [32-retiro-tras-descarte-200.png](32-retiro-tras-descarte-200.png): revisada el 16 de octubre de 2026; HTTP 200, is_confidential=false y ai_status=OMITIDA tras descarte y retiro explícito reportados. Sin credenciales visibles.

- [33-historial-proteccion.json](33-historial-proteccion.json): revisado el 16 de octubre de 2026, JSON válido con 15/15 eventos; conserva declaración/revisiones, protección y retiro explícito, además del ciclo previo. Solo datos simulados, sin contraseñas ni tokens observados.

## RH independiente — evidencias revisadas el 16 de octubre de 2026

- [34-rh-independiente-auth-me-200.png](34-rh-independiente-auth-me-200.png): cuenta nueva autenticada ADMIN_RH.
- [35-caso-rh-involucrado-201.png](35-caso-rh-involucrado-201.png): acuse 201.
- [36-rh-independiente-acceso-200.png](36-rh-independiente-acceso-200.png): detalle confidencial 200 con administrador original afectado.
- [37-rh-involucrado-acceso-404.png](37-rh-involucrado-acceso-404.png): rechazo 404 según recorrido reportado; recorte sin ID/identidad.

Sin contraseñas ni tokens observados. Ver ../REVISION_RH_INDEPENDIENTE.md y ../REPORTE_QA.md.

Evidencia 38-admin-usuarios-listado-200.png prevista para 0.8.0, todavía no recibida ni verificada. Solo Server response de GET /users con datos simulados, sin Curl/token.

## Evidencias de administración consolidadas — 16 de octubre de 2026

- [38-suite-completa-77-passed.png](38-suite-completa-77-passed.png)
- [39-admin-usuarios-listado-200.png](39-admin-usuarios-listado-200.png)
- [40-usuario-demo-desactivado-200.png](40-usuario-demo-desactivado-200.png)
- [41-usuario-demo-inactivo-listado-200.png](41-usuario-demo-inactivo-listado-200.png)
- [42-usuario-demo-reactivado-200.png](42-usuario-demo-reactivado-200.png)
- [43-sesion-revocada-401.png](43-sesion-revocada-401.png)
- [44-revocacion-administrativa-401.png](44-revocacion-administrativa-401.png)
- [45-token-anterior-tras-reactivacion-401.png](45-token-anterior-tras-reactivacion-401.png)
- [46-rh-reactivado-nueva-sesion-200.png](46-rh-reactivado-nueva-sesion-200.png)

Todas inspeccionadas; evidencia 42 actual muestra GET con cuenta activa. Recorrido, resultados y límites en ../REVISION_ADMIN_USUARIOS.md. Sin tokens ni contraseñas observados.

## Traslado y rol — revisadas el 17 de octubre de 2026

Evidencias 47–57 (incluye 52b): detalle, resultados, enlaces y límites en [REVISION_TRASLADO_ROL.md](../REVISION_TRASLADO_ROL.md). JSON 51 contiene 4/4 eventos; JSON 57, 5/5. Datos ficticios, sin tokens/contraseñas observados. No equivale a concurrencia PostgreSQL verificada.

Evidencia prevista 58-panel-react-incidencias.png para prueba manual del frontend de lectura. Todavía no recibida ni verificada. Solo datos simulados y listado; omitir contraseña/token, red y cualquier identidad real. Guía ../FRONTEND.md.

- [58-panel-react-incidencias.png](58-panel-react-incidencias.png): revisada el 17 de octubre de 2026; listado React con dos casos simulados, sin credenciales visibles. Primera prueba manual del listado, límites en REPORTE_QA.md.

- [59-panel-react-detalle.png](59-panel-react-detalle.png): revisada el 17 de octubre de 2026; detalle e historial parcial del caso simulado, sin credenciales visibles.

- [60-panel-react-filtro.png](60-panel-react-filtro.png): revisada el 17 de octubre de 2026; búsqueda por título, una fila y total 1, sin credenciales visibles.

- [61-panel-react-sesion-cerrada.png](61-panel-react-sesion-cerrada.png): revisada el 17 de octubre de 2026; login vacío y aviso de cierre, sin datos de casos ni credenciales visibles.

Evidencia prevista 62-registro-react-acuse.png, todavía no recibida ni verificada: una sola captura del acuse de alta desde React con datos simulados. No capturar cada campo ni credenciales. Plan agrupado en ../FRONTEND.md.

- [62-registro-react-acuse.png](62-registro-react-acuse.png): revisada el 17 de octubre de 2026; acuse React con referencia y acceso permitido. Sin credenciales visibles; límites en REPORTE_QA.md.

Evidencia prevista 63-gestion-react-caso-cerrado.png: una captura final del recorrido de gestión React 0.3.0, todavía no recibida ni verificada. Solo datos ficticios, sin credenciales. No se requiere captura de cada paso. Plan en ../FRONTEND.md.

- [63-gestion-react-caso-cerrado.png](63-gestion-react-caso-cerrado.png): captura aportada y guardada sin edición el 17 de octubre de 2026; caso Retardo cerrado con resolución y fechas, sin credenciales visibles. Límites en REPORTE_QA.md.

Evidencia prevista 64-admin-react-usuarios.png: una captura final de listado/confirmación de modificación de nombre DEMO en React 0.4.0. Todavía no recibida ni verificada. Datos ficticios, sin contraseñas/tokens; no se exige captura de cada campo. Guía agrupada en ../FRONTEND.md.

- [64-admin-react-usuarios.png](64-admin-react-usuarios.png): revisada el 17 de octubre de 2026; listado administrativo React y aviso de guardado sin cambio de permisos/0 casos ajustados. Sustituye el estado anterior de captura pendiente.
- [64b-admin-react-usuarios-continuacion.png](64b-admin-react-usuarios-continuacion.png): continuación aportada en el mismo mensaje, conservada sin edición; filas finales (incluido Supervisor RH Demo Juan) y página 1 de 1. Sin credenciales visibles. Límites en REPORTE_QA.md.

- [65-react-confidencialidad.png](65-react-confidencialidad.png): revisada el 17 de octubre de 2026; Ausencia simulada EN_REVISION, protección actualizada, acceso restringido a RH independiente e IA omitida.
- [66-react-participante-confirmado.png](66-react-participante-confirmado.png): revisada el 17 de octubre de 2026; Empleado Operaciones Uno Demo CONFIRMADO, declaración «testigo» y última revisión «Testigo Visual». Recorte sin ID de expediente. Ambas sin credenciales visibles; límites en REPORTE_QA.md.

Evidencia prevista 67-react-password-actualizada.png: login vacío con aviso de contraseña actualizada tras cambio desde React. Todavía no recibida ni verificada. No capturar formulario ni credenciales; plan en ../FRONTEND.md.

- [67-react-password-actualizada.png](67-react-password-actualizada.png): inspeccionada el 17 de octubre de 2026; login vacío con aviso de contraseña actualizada, sin credenciales visibles. Sustituye el estado previo de evidencia pendiente. Nuevo inicio de sesión reportado por la autora; límites en REPORTE_QA.md.
