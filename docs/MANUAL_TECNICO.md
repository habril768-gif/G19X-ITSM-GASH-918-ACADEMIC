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
