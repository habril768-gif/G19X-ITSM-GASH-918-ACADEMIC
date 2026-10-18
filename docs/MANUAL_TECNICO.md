# Manual técnico inicial

## Estado

Versión de API 0.1.0. Solo disponibilidad y documentación HTTP. PostgreSQL, Redis, Entra ID, React, OpenAI y correo aún no están conectados.

## Instalación y operación local

Seguir [las instrucciones del backend](../backend/README.md), desde un clon del repositorio. El entorno virtual se reconstruye a partir de requirements; no se versiona.

## Contrato

GET `/health`: HTTP 200 y JSON con status `ok` y service `plurione-api`. GET `/openapi.json`: contrato OpenAPI. GET `/docs`: interfaz Swagger UI. No hay rutas de negocio.

## Estructura y seguridad

La fábrica create_app registra el router de sistema. La ruta de salud no devuelve secretos ni datos personales. El arranque predeterminado escucha solo 127.0.0.1. La API inicial no carga .env. No se debe exponer como servicio empresarial hasta incorporar autenticación en rutas de negocio y HTTPS.

## Verificación y soporte inicial

Ejecutar las pruebas según backend/README.md. Registrar salidas y fallos sanitizados en REPORTE_QA.md. Si el puerto 8000 está ocupado, elegir otro puerto. Si faltan módulos, instalar las dependencias con el Python del entorno virtual. Docker, migraciones, respaldo y procedimientos de producción quedan pendientes de sus respectivas implementaciones.

## Entorno de contenedores

El archivo compose.yaml define API, PostgreSQL y Redis. Consultar [arranque y verificación](../infra/README.md). Está preparado, pendiente de ejecución en Docker Desktop. La API recibe variables de conexión, pero todavía no las utiliza. PostgreSQL y Redis no publican puertos; para SQL y ping se usa docker compose exec. No se ha implementado esquema de datos ni worker.

## Conexión y migraciones

API 0.2.0 incorpora SQLAlchemy, Psycopg, Alembic y /health/db. Consultar DATOS.md para esquema, configuración, instalación y validación. El entorno Docker debe reconstruir la imagen antes de ejecutar la migración. La revisión requerida por readiness es 0001 y debe actualizarse con nuevas revisiones futuras. El endpoint no devuelve detalles de conexión. La API todavía no ofrece operaciones de incidencias.

## Fixtures de QA

Seguir DATOS_DEMO.md para carga explícita, repetible y transaccional de cuentas ficticias. No permite iniciar sesión. Migración y conexión PostgreSQL están verificadas por evidencia manual en REPORTE_QA.md.

## API 0.3.0: autenticación propia

Esta actualización sustituye las referencias anteriores a Entra ID. Ver AUTENTICACION.md para migración 0002, primer administrador, inicio/cierre de sesión, alta de usuarios y restablecimiento. El token es opaco y solo su digest se almacena en PostgreSQL; no requiere secreto JWT. La contraseña se introduce por getpass para comandos de operación.

## API 0.4.0 y esquema 0003

Actualizar según DATOS.md, sin repetir alta del administrador. Readiness exige 0003, liveness no depende de DB. La migración no publica nuevos endpoints de casos ni ejecuta IA.

## API 0.5.0 — Incidencias iniciales

Consultar INCIDENCIAS.md para rutas, contrato y validación manual. Requiere esquema 0003 y sesión válida; basta reconstruir imagen, no repetir bootstrap. No hay estados de negocio mutables todavía. La auditoría inicial se realiza dentro de la transacción. Un fallo SQL devuelve 503 genérico sin consulta ni credenciales.

## API 0.6.0 — Operación de incidencias

Mantiene esquema 0003. Reconstruir con docker compose up -d --build --wait y verificar 0.6.0 en /docs. No necesita credenciales nuevas ni cambios a .env. Rutas, reglas y prueba manual en INCIDENCIAS.md. Para confirmación humana usar PUT classification antes de iniciar revisión; asignar solo gestor con acceso. No hay frontend de gestión todavía. Las rutas devuelven 409 ante estado incompatible, 422 ante datos/responsable inválidos, 403 para operación de rol no permitido y 404 ante expediente no visible. Un error SQL revierte cambios y devuelve 503 genérico.

## API 0.7.0 — Protección del expediente

Esquema 0003. Reconstruir con docker compose up -d --build --wait y verificar 0.7.0. No repetir bootstrap ni seed. Rutas de participantes/revisión y confidencialidad documentadas en INCIDENCIAS.md. Solo Admin RH independiente; respuesta mínima con can_view porque puede perder acceso. RESUELTA/CERRADA exigen reapertura. Confidencialidad fuerza omisión IA y revisión preserva original. Reasignación y retroceso protector se ejecutan junto con auditoría. Pruebas SQLite no demuestran bloqueo concurrente PostgreSQL. El CLI para provisionar administrador independiente adicional sigue pendiente.

Procedimiento provision-independent-admin preparado para operador; tras aplicar paquete, reconstruir imagen sin migración nueva (0003, API 0.7.0). Comando interactivo y límites en ADMIN_INDEPENDIENTE.md. Mantiene bootstrap y restablecimiento de contraseña; no usar contraseña en argumentos.

Actualización posterior: paquete de RH adicional aplicado y reconstruido según reporte de la autora. API 0.7.0/esquema 0003 conservados. Sesión nueva y recorrido manual en REVISION_RH_INDEPENDIENTE.md; no hay suite HTTP completa nueva acreditada.

Actualización preparada 0.8.0: aplicar paquete completo y ejecutar suite, luego reconstruir con docker compose up -d --build --wait. No requiere nueva migración ni bootstrap. Mutaciones de usuarios/incidencias coordinadas, deben desplegarse juntas. Guía ADMIN_USUARIOS.md.

Estado posterior de 0.8.0: paquete aplicado y Docker reconstruido según la autora. Suite completa 77/3/1 observada, recorrido administrativo documentado en REVISION_ADMIN_USUARIOS.md. Sin nueva migración (0003); no repetir bootstrap. Los pendientes de pruebas PostgreSQL y concurrencia siguen vigentes.

Frontend React 0.1.0: Node 24 verificado, npm.cmd ci y npm.cmd run dev desde frontend; http://127.0.0.1:5173/. Backend existente debe seguir activo. Proxy /api local sin secretos. Pruebas/build: npm test, npm run build. No migración adicional. Configuración, limitaciones y comprobación manual en FRONTEND.md.

Frontend 0.2.0 añade Nueva incidencia. No requiere npm install adicional ni nueva migración; conservar npm ci para instalación limpia y npm run dev desde frontend. Validación: npm test y npm run build. Prueba manual agrupada en FRONTEND.md; operaciones de gestión restantes siguen en Swagger.

React 0.3.0 incorpora gestión al detalle del expediente para Supervisor/Admin RH. Mantener npm run dev en frontend, actualizar e iniciar sesión; sin nuevas dependencias, Docker build ni migración requeridos por el frontend. Pruebas/build: npm test y npm run build. Recorrido agrupado y límites en FRONTEND.md; no cambiar .env.

## React 0.4.0 — 17 de octubre de 2026

Mismos comandos de frontend: npm.cmd run dev, npm.cmd test y npm.cmd run build, desde frontend. No requiere npm install, reconstrucción Docker, migración ni variables nuevas. Backend 0.8.0 y esquema 0003.

Users.jsx consume GET /users/options, GET /users paginado, POST /users y PUT /users/{id}. CaseProtection.jsx consume POST /incidents/{id}/participants, PUT /participants/{user_id}/review y PUT /confidentiality bajo la incidencia. Roles/estados solo orientan UI: autorización definitiva en API. onSelfRevoked limpia sesión y onAccessLost retira expediente/historial. La recuperación administrativa de contraseña conserva su procedimiento existente. Uso y comprobación manual agrupada en FRONTEND.md; evidencia 64 todavía pendiente.

React 0.5.0, 17 de octubre de 2026: pantalla de cambio de contraseña para todos los roles, reutilizando /auth/change-password. Confirma nueva credencial, limpia campos y vuelve al login al guardar; resultado incierto retira sesión local sin reenvío. Sin migración ni backend nuevo. RF-1/RF-8 parciales; comprobación real/evidencia 67 y departamentos pendientes. Uso y límites en FRONTEND.md.

Actualización 17 de octubre de 2026: API 0.9.0 / React 0.6.0 añaden administración de departamentos con historial propio, baja lógica protegida y reactivación. Requiere aplicar 0004; sustituye el pendiente de código de departamentos, sin acreditar despliegue ni recorrido real. Guía vigente DEPARTAMENTOS.md. RF-7/RF-8 parciales; instalación, PostgreSQL real/concurrencia y evidencia 68 pendientes.
