# Backend PluriOne

API inicial FastAPI. Requiere Python 3.11 o posterior; versión de referencia: Python 3.11.

## Instalación en Windows PowerShell

Desde la raíz del repositorio:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
```

No es necesario activar el entorno ni cambiar la política de ejecución de PowerShell. Para ejecutar sin herramientas de prueba se puede instalar solo `backend/requirements.txt`.

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

Detener con Ctrl+C. Si el puerto está ocupado, usar `--port 8001` y ajustar la URL. `/` no tiene ruta: su 404 es esperado.

## Ejecutar pruebas

Desde `backend/`:

```powershell
.venv/Scripts/python.exe -m pytest -q
```

Desde la raíz del repositorio:

```powershell
backend/.venv/Scripts/python.exe -m pytest -q backend/tests
```

## Alcance actual

`/health` es una comprobación pública del proceso HTTP y no prueba disponibilidad de base de datos, Redis o IA. No requiere ni lee `.env`; no realiza llamadas externas. Las rutas de negocio y Entra ID aún no están implementadas. `/health/db` sí requiere PostgreSQL y revisión 0001; ver docs/DATOS.md. El servidor local usa HTTP; HTTPS deberá configurarse antes de un despliegue externo. No se exponen datos de empleados.

La página `/docs` usa recursos Swagger UI alojados en una CDN; para visualizarla completamente se requiere conexión del navegador. `/openapi.json` se sirve localmente.

## Organización

- `app/main.py`: creación de aplicación y registro de rutas.
- `app/api/health.py`: endpoint y contrato de respuesta.
- `app/core`, `app/models`, `app/services`: capas previstas para siguientes entregas.
- `tests/test_api.py`: contrato HTTP y documentación.

Dependencias de ejecución en `requirements.txt`; pruebas en `requirements-dev.txt`. Las versiones transitivas se fijan para reproducir la instalación. Consultar el reporte QA y la bitácora antes de dar por cumplido un requisito del MVP.

## Migraciones

Consultar [diseño de datos](../docs/DATOS.md). La API no crea tablas automáticamente. En Docker: `docker compose exec api python -m alembic upgrade head`, desde la raíz del repositorio.
