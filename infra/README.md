# Entorno local con Docker Compose

## Preparación

Requiere Docker Desktop iniciado con motor Linux. Sigue el [arranque principal](../README.md#arranque-local-en-cinco-pasos); conserva `.env`, cuentas y volúmenes existentes. La API usa las variables PostgreSQL suministradas por Compose, y Redis notifica al worker IA sobre trabajos guardados en PostgreSQL.

## Servicios y perfiles

| Servicio | Activación | Acceso |
| --- | --- | --- |
| API, PostgreSQL y Redis | Compose base | API en `127.0.0.1:8000`; bases internas |
| Worker IA | Perfil `ai` | Sin puerto público; [configuración IA](../docs/IA.md) |
| Worker de correo y Mailpit | Perfil `mail` | Buzón de pruebas en `127.0.0.1:8025`; SMTP interno |
| Conexión Power BI | Override `compose.bi.yaml` | Solo PostgreSQL en `127.0.0.1:5433`; [analítica](../docs/ANALITICA.md) |

No se instala ni activa un perfil por copiar `.env`. Si modificas puertos, usa los valores locales correspondientes en el navegador y en las conexiones.

## Diagnóstico

Desde la raíz:

```powershell
docker compose config --quiet
docker compose ps
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
docker compose exec redis redis-cli ping
```

`config --quiet` valida sin imprimir valores resueltos. Redis debe responder `PONG`. `/health` verifica HTTP; `/health/db`, PostgreSQL y esquema. La salud del contenedor no sustituye un recorrido de negocio.

## Detener y conservar datos

```powershell
docker compose stop
docker compose start
```

Si necesitas recrear servicios, utiliza la misma combinación de archivos Compose y perfiles con la que los activaste. `docker compose down` conserva los volúmenes nombrados; añadir `--volumes` elimina datos. Cambiar `POSTGRES_PASSWORD` en `.env` no cambia la contraseña de una base ya inicializada. No elimines volúmenes para resolver errores de acceso.

## Actualizaciones y límites

Reconstruye API y workers cuando cambie su código y aplica las migraciones pendientes. Los scripts de correo y analítica documentan su secuencia específica. No repitas bootstrap ni seed para actualizar.

El entorno usa loopback, almacenamiento persistente y una imagen API sin privilegios. No constituye un despliegue productivo: HTTPS externo, estrategia de respaldo/restauración, monitoreo y mantenimiento requieren preparación y validación propias. Nunca captures contraseñas, `.env`, tokens o datos personales en evidencias.
