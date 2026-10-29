# Backend de PluriOne

API FastAPI con autenticación local, expedientes, administración, auditoría y seguimiento de trabajos. PostgreSQL conserva los datos y las colas durables; los workers de IA y correo se ejecutan por separado.

## Arranque recomendado

Sigue los [cinco pasos de la guía principal](../README.md#arranque-local-en-cinco-pasos). Compose instala las dependencias de la imagen. La API no crea tablas automáticamente: aplica `alembic upgrade head` y verifica `alembic check` antes de usarla.

## Desarrollo sin contenedores

Usa Python 3.11, que coincide con el Dockerfile. Desde la raíz:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
```

Configura en el entorno del proceso las variables PostgreSQL de `.env.example`. La aplicación no lee `.env` automáticamente; Compose sí le proporciona las variables. Una API ejecutada en el equipo necesita una conexión PostgreSQL accesible desde él: el servicio base no publica su puerto.

Desde `backend/`, con la base configurada:

```powershell
.venv/Scripts/python.exe -m alembic upgrade head
.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

No es necesario activar el entorno ni cambiar la política de PowerShell. Detén Uvicorn con Ctrl+C. No ejecutes a la vez otra API en el mismo puerto.

## Contrato y diagnóstico

| Recurso local | Función |
| --- | --- |
| [Health](http://127.0.0.1:8000/health) | Disponibilidad HTTP, independiente de servicios externos |
| [Health DB](http://127.0.0.1:8000/health/db) | Conexión PostgreSQL y revisión de esquema requerida por el código |
| [Swagger](http://127.0.0.1:8000/docs) | Contrato interactivo; sus recursos visuales requieren acceso a la CDN |
| [OpenAPI](http://127.0.0.1:8000/openapi.json) | Contrato servido localmente |

Las rutas de negocio exigen sesión y permisos sobre cada objeto. Consulta [autenticación](../docs/AUTENTICACION.md), [incidencias](../docs/INCIDENCIAS.md) y el [manual técnico](../docs/MANUAL_TECNICO.md). La raíz `/` sin ruta definida puede responder 404.

## Estructura

- `app/api/`: rutas, dependencias y contratos HTTP.
- `app/services/`: autorización y operaciones de negocio transaccionales.
- `app/models/`: modelos SQLAlchemy y restricciones.
- `app/core/`: configuración, seguridad y conexión diferida.
- `app/ai/`, `app/mail/`, `app/reporting/`: proveedores, workers y acceso analítico.
- `migrations/`: evolución controlada de esquema y vistas.
- `tests/`: pruebas HTTP, servicios, persistencia y permisos.

## Pruebas

Desde `backend/`:

```powershell
.venv/Scripts/python.exe -m pytest -q
```

La suite requiere dependencias de desarrollo. Para ejecutar también las integraciones PostgreSQL sin usar la base operativa, sigue [PRUEBAS_POSTGRESQL.md](../docs/PRUEBAS_POSTGRESQL.md). Revisa fallos y omisiones: una prueba omitida no es una integración aprobada.

Los resultados ejecutados se registran en [REPORTE_QA.md](../docs/REPORTE_QA.md); no se deducen del número de archivos. No ejecutar seeds, evaluaciones con cargos ni pruebas destructivas contra la base de uso.

## Integraciones

IA está desactivada por defecto y requiere revisión de texto simulado, perfil `ai` y credenciales del worker. Correo usa perfil `mail` y Mailpit para capturar avisos. Analítica se consulta con una cuenta limitada a las vistas agregadas. Guías: [IA](../docs/IA.md), [correo](../docs/CORREO.md) y [analítica](../docs/ANALITICA.md).
