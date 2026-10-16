# Reporte QA inicial

## 15 de octubre de 2026 — API 0.1.0

Entorno: Windows, Python 3.11, entorno virtual local `backend/.venv`. Sin conexión a datos reales ni servicios de IA.

| Comprobación | Resultado | Evidencia |
| --- | --- | --- |
| GET /health con cliente ASGI | Aprobada | HTTP 200, contenido JSON y contrato esperado |
| Contrato OpenAPI | Aprobada | Ruta /health y referencia HealthResponse presentes |
| Página /docs | Aprobada | HTML disponible con referencia al contrato local |
| Dependencias | Aprobada | pip check: No broken requirements found |
| Arranque Uvicorn | Aprobada | Application startup complete; escucha en 127.0.0.1:8000 |
| Consulta HTTP entre procesos del entorno | No verificada | PowerShell agotó el tiempo de conexión a loopback; no se presenta como prueba HTTP aprobada |
| Secretos y entorno virtual excluidos | Aprobada | git check-ignore sobre .env y backend/.venv/pyvenv.cfg |
| CI de GitHub | Pendiente | Workflow creado; no se ha observado una ejecución remota |

Comando de pruebas desde la raíz: `backend/.venv/Scripts/python.exe -m pytest -q backend/tests`. Resultado: **3 passed, 1 warning**. La advertencia indica deprecación de httpx en TestClient de Starlette; no hay fallos. Se conserva constancia y se revisará la migración al ampliar las pruebas.

La descarga directa mediante pip fue bloqueada por el entorno. Se descargaron ruedas oficiales de PyPI mediante PowerShell y se instalaron localmente con pip --no-index; posteriormente se verificaron los archivos requirements contra el entorno instalado. Los archivos descargados quedan fuera del repositorio. En un equipo con conectividad normal se utiliza el comando documentado de pip.

## Límites de esta validación

No se probaron autenticación, incidencias, PostgreSQL, Redis, Docker, IA, correo, rendimiento ni frontend. Docker no está disponible como comando en este entorno. La prueba de /docs verifica HTML, no un renderizado visual de Swagger UI en navegador. Este reporte no acredita el MVP completo.

## 15 de octubre de 2026 — Configuración Compose

Revisión estática: API con contexto backend, instalación por requirements, PostgreSQL/Redis sin ports, contraseña requerida, healthchecks y volúmenes nombrados. .env y entorno virtual excluidos de Git y del contexto de construcción.

**Pendiente:** validación real de `docker compose config --quiet`, construcción de imagen Linux, arranque de servicios, GET /health, SELECT 1 y PONG. Docker no está disponible como comando. No hay un resultado de contenedores aprobado. La validación automática YAML tampoco se ejecutó por ausencia de los parsers consultados.

Ejecutar los pasos de infra/README.md y guardar las evidencias indicadas en docs/evidencias/README.md. No reutilizar el resultado de pruebas ASGI como evidencia de Docker.

## Evidencias recibidas el 15 de octubre de 2026 — Verificación manual

La autora ejecutó los comandos en su equipo y proporcionó las capturas siguientes. Se inspeccionaron visualmente; no son ejecuciones nuevas del asistente. Esta evidencia complementa las limitaciones históricas descritas arriba.

| Comprobación | Resultado observado | Evidencia |
| --- | --- | --- |
| GET /health desde navegador | HTTP 200 y JSON status ok, service plurione-api | [Captura](evidencias/01-api-health-200.png) |
| Construcción y arranque Compose | Imagen API construida; API, PostgreSQL y Redis healthy | [Captura](evidencias/02-compose-servicios.png) |
| PostgreSQL SELECT 1 | Una fila con valor 1 | [Captura](evidencias/03-postgres-select.png) |
| Redis PING | PONG | [Captura](evidencias/04-redis-ping.png) |

La captura HTTP no permite distinguir por sí sola entre el arranque nativo y Docker. La captura Compose sí acredita la comprobación de salud del contenedor API. No se acredita aún conexión de la aplicación con PostgreSQL o Redis, persistencia tras reinicio, migraciones, autenticación o flujos del MVP.

## 15 de octubre de 2026 — Capa de datos inicial

Resultado local: **8 passed, 2 skipped, 1 warning**. Comando: backend/.venv/Scripts/python.exe -m pytest -q backend/tests.

Pruebas nuevas aprobadas: manejo de caracteres reservados en contraseña sin URL concatenada; respuesta genérica 503 con liveness operativo; respuesta 200 con dependencia simulada; compilación de esquema PostgreSQL con JSONB/fechas y restricciones; generación offline de migración y catálogos. Las tres pruebas HTTP anteriores siguen aprobadas. pip check: sin conflictos.

Las dos pruebas PostgreSQL (esquema/catálogos e identidad Entra única) se omiten sin RUN_DB_TESTS=1. No se presentan como aprobadas. La CI ahora prepara PostgreSQL aislado, aplica migración dos veces, comprueba alineación de modelos y ejecuta integración; no se ha observado su resultado remoto.

Docker instalado localizado, pero conexión al pipe dockerDesktopLinuxEngine denegada para el asistente. Migración real, alembic check y /health/db contra PostgreSQL quedan pendientes. Prueba HTTP 200 nueva usa dependencia simulada y no acredita conexión real. Instrucciones en DATOS.md.
