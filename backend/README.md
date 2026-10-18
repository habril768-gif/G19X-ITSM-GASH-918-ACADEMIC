# Backend PluriOne

API inicial FastAPI. Requiere Python 3.11 o posterior; versiÃ³n de referencia: Python 3.11.

## InstalaciÃ³n en Windows PowerShell

Desde la raÃ­z del repositorio:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
```

No es necesario activar el entorno ni cambiar la polÃ­tica de ejecuciÃ³n de PowerShell. Para ejecutar sin herramientas de prueba se puede instalar solo `backend/requirements.txt`.

## Ejecutar

```powershell
cd backend
.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- Disponibilidad: http://127.0.0.1:8000/health
- Interfaz de API: http://127.0.0.1:8000/docs
- Contrato: http://127.0.0.1:8000/openapi.json

Respuesta esperada de `/health`:

```json
{"status":"ok","service":"plurione-api"}
```

Detener con Ctrl+C. Si el puerto estÃ¡ ocupado, usar `--port 8001` y ajustar la URL. `/` no tiene ruta: su 404 es esperado.

## Ejecutar pruebas

Desde `backend/`:

```powershell
.venv/Scripts/python.exe -m pytest -q
```

Desde la raÃ­z del repositorio:

```powershell
backend/.venv/Scripts/python.exe -m pytest -q backend/tests
```

## Alcance actual

`/health` es una comprobaciÃ³n pÃºblica del proceso HTTP y no prueba disponibilidad de base de datos, Redis o IA. No requiere ni lee `.env`; no realiza llamadas externas. Las rutas de negocio y autenticaciÃ³n externa no se implementarÃ¡n en el MVP. `/health/db` sÃ­ requiere PostgreSQL y revisiÃ³n 0002; ver docs/DATOS.md. El servidor local usa HTTP; HTTPS deberÃ¡ configurarse antes de un despliegue externo. No se exponen datos de empleados.

La pÃ¡gina `/docs` usa recursos Swagger UI alojados en una CDN; para visualizarla completamente se requiere conexiÃ³n del navegador. `/openapi.json` se sirve localmente.

## OrganizaciÃ³n

- `app/main.py`: creaciÃ³n de aplicaciÃ³n y registro de rutas.
- `app/api/health.py`: endpoint y contrato de respuesta.
- `app/core`, `app/models`, `app/services`: capas previstas para siguientes entregas.
- `tests/test_api.py`: contrato HTTP y documentaciÃ³n.

Dependencias de ejecuciÃ³n en `requirements.txt`; pruebas en `requirements-dev.txt`. Las versiones transitivas se fijan para reproducir la instalaciÃ³n. Consultar el reporte QA y la bitÃ¡cora antes de dar por cumplido un requisito del MVP.

## Migraciones

Consultar [diseÃ±o de datos](../docs/DATOS.md). La API no crea tablas automÃ¡ticamente. En Docker: `docker compose exec api python -m alembic upgrade head`, desde la raÃ­z del repositorio.

## Sesiones locales

Ver [AUTENTICACION.md](../docs/AUTENTICACION.md): migraciÃ³n 0002, bootstrap interactivo, login, /auth/me, logout y cambio de contraseÃ±a. La API no necesita variables Entra ni claves de firma JWT.

## Esquema de incidencias

API 0.4.0 requiere 0003 para readiness. Ver docs/DATOS.md para actualización y conservación. No existen todavía rutas de gestión de incidencias; los modelos no sustituyen sus servicios de permisos.

Actualización 17 de octubre de 2026: API 0.9.0 / React 0.6.0 añaden administración de departamentos con historial propio, baja lógica protegida y reactivación. Requiere aplicar 0004; sustituye el pendiente de código de departamentos, sin acreditar despliegue ni recorrido real. Guía vigente DEPARTAMENTOS.md. RF-7/RF-8 parciales; instalación, PostgreSQL real/concurrencia y evidencia 68 pendientes.

17 de octubre de 2026: integraciones antes omitidas ejecutadas en clúster temporal PostgreSQL 18.6; suite 103 aprobadas/0 omitidas/1 advertencia. Incluye cinco integraciones PostgreSQL y las pruebas originales SQLite. Migración hasta 0004 y check verificados en aislamiento; base de desarrollo sin modificar. CI PostgreSQL 17 del commit c8ad75c observado exitoso. Guía PRUEBAS_POSTGRESQL.md, evidencia 69 JSON y límites en REPORTE_QA.md. Nuevas pruebas remotas y carreras adicionales pendientes; sin nuevas capturas.

17 de octubre de 2026: API 0.10.0 / React 0.7.0 preparan IA revisada, trabajo durable PostgreSQL/avisos Redis y sugerencia independiente de validación humana. Requiere 0005; desactivada por defecto, clave solo worker. 130 backend sin omisiones en aislamiento y 64 UI/build correctos; no acreditan calidad del modelo. Proveedor/Redis reales, despliegue y evaluación independiente 50+5 pendientes. Guía IA.md y evidencia 70; RF-3/RF-8 parciales.
