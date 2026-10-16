# Entorno local con Docker Compose

## Requisitos

Docker Desktop con motor Linux y Docker Compose v2. Debe estar iniciado. No se instala automáticamente como parte del repositorio.

## Configuración

Desde la raíz del proyecto, si todavía no existe `.env`, copiar `.env.example` a `.env`. Si ya existe, conservarlo y agregar solo las variables faltantes. Completar localmente `POSTGRES_PASSWORD` con una contraseña propia y no compartirla. No es necesaria una clave de OpenAI para esta entrega.

Variables usadas ahora: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD y API_PORT (opcional, por defecto 8000). DATABASE_URL sigue reservada para la capa de persistencia; no se utiliza aún. Compose proporciona a la API las variables de conexión individuales; la API todavía no conecta a esos servicios.

## Comprobar y arrancar

Desde la raíz:

```powershell
docker version
docker compose version
docker compose config --quiet
docker compose up -d --build --wait
docker compose ps
```

Usar `config --quiet` evita imprimir las variables resueltas con contraseñas. Si un Uvicorn local ocupa el puerto 8000, detenerlo con Ctrl+C o agregar `API_PORT=8001` al .env.

Abrir http://127.0.0.1:8000/docs y ejecutar GET /health. Ajustar el puerto si se cambió API_PORT.

## Validar los servicios

```powershell
docker compose exec postgres sh -c 'pg_isready -h 127.0.0.1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'
docker compose exec postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1;"'
docker compose exec redis redis-cli ping
```

Se espera PostgreSQL aceptando conexiones, una fila con valor 1 y Redis PONG. La API solo acredita disponibilidad HTTP: todavía no hay modelos, migraciones ni integración de persistencia. La comprobación de PostgreSQL comprueba servicio; la prueba SELECT comprueba ejecución SQL local en el contenedor.

## Detener y volver a arrancar

```powershell
docker compose down
docker compose up -d --wait
```

`down` conserva los volúmenes nombrados. No agregar `--volumes` al detener: eliminaría los datos persistidos. La contraseña inicializa PostgreSQL únicamente con un volumen vacío; cambiarla en .env no modifica una base ya inicializada. No eliminar volúmenes para resolver errores sin preservar datos.

## Evidencia

Guardar capturas de `docker compose ps`, SELECT 1, PONG y respuesta HTTP 200 en docs/evidencias, sin contraseñas ni datos personales. Registrar fecha, comando, resultado y limitaciones en REPORTE_QA.md. No presentar como verificadas hasta ejecutar realmente las pruebas.

## Diseño y límites

PostgreSQL y Redis solo son accesibles dentro de la red Compose; no publican puertos al equipo. Solo la API se publica en 127.0.0.1. La imagen API usa usuario sin privilegios y el contexto de construcción excluye .env y el entorno virtual. Redis conserva datos con AOF; no hay worker todavía. No es una configuración de producción ni implementa HTTPS o respaldo. Las imágenes se fijan por línea de versión, no por digest: futuras reconstrucciones pueden incorporar parches.

Fuentes: [orden de arranque](https://docs.docker.com/compose/how-tos/startup-order/) y [imagen PostgreSQL](https://hub.docker.com/_/postgres).
