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
