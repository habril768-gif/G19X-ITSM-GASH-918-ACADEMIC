> Actualización vigente: esquema 0002 y autenticación local; consultar AUTENTICACION.md. La descripción de 0001 que sigue documenta el esquema inicial.

# Diseño de datos e instalación del esquema inicial

## Alcance

SQLAlchemy 2 con Psycopg 3; migraciones Alembic. Revisión inicial `0001`. Datos UUID para usuarios, departamentos, casos y auditoría; catálogos con ID entero. El esquema utiliza JSONB y fechas con zona horaria de PostgreSQL. La aplicación debe enviar fechas UTC.

## Entidades

| Tabla | Propósito y restricciones |
| --- | --- |
| roles | ADMIN_RH=1, SUPERVISOR=2, EMPLEADO=3 |
| departamentos | Nombre único, estado activo |
| users | Identidad única por tenant_id y external_id; rol y departamento obligatorios |
| categorias_incidencia | Cinco categorías del PRD, IDs 1 a 5 |
| incidencias | Autor, afectado, departamento histórico, responsable, clasificación humana/IA y ciclo |
| historial_incidencias | Actor nullable para sistema, destino incidencia o usuario, acción y detalle JSONB |

No se crean usuarios ni credenciales reales. La migración inserta únicamente roles y categorías. La generación de departamentos y usuarios simulados se implementará después. Los IDs UUID se generan por SQLAlchemy; inserciones SQL manuales deben proporcionarlos.

`affected_user_id` permite auditar gestión de usuarios sin asociar artificialmente una incidencia. Los CHECK controlan valores y campos esenciales; permisos, confidencialidad, transiciones, usuario activo y escritura atómica del historial se implementarán en los servicios. El esquema por sí solo no aplica esas reglas. La eliminación no se publica como operación de aplicación. La inmutabilidad del historial deberá reforzarse con el usuario de aplicación al separar privilegios de migración; actualmente Compose usa el usuario de desarrollo.

## Aplicar en Docker desde la raíz

```powershell
docker compose up -d --build --wait
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
```

Se espera revisión `0001` y ningún cambio de esquema pendiente. Aplicar `upgrade head` nuevamente no debe duplicar catálogos. Las migraciones son explícitas: la API no crea tablas al arrancar. No ejecutar downgrade sobre datos que deban conservarse; el downgrade inicial elimina las tablas.

Después abrir http://127.0.0.1:8000/docs y ejecutar GET /health/db. Devuelve HTTP 200 solo si conecta a PostgreSQL y la revisión es 0001. Si no hay configuración, no hay conexión o faltan migraciones, devuelve 503 genérico, sin credenciales. `/health` sigue respondiendo si el proceso está disponible.

```powershell
docker compose exec postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT version_num FROM alembic_version;"'
docker compose exec postgres sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT nombre FROM categorias_incidencia ORDER BY id;"'
```

Capturas previstas: docs/evidencias/05-migracion-inicial.png y 06-api-db-health-200.png. No se consideran existentes hasta recibirlas.

## Configuración de conexión

La aplicación lee POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER y POSTGRES_PASSWORD del entorno del proceso. Compose ya los proporciona. No se concatena la contraseña en una URL: URL.create preserva caracteres especiales. DATABASE_URL permanece reservada y no se utiliza. La API no lee automáticamente .env; en ejecución nativa se deben definir variables en PowerShell y tener acceso a PostgreSQL. Los servicios de Compose no exponen puerto PostgreSQL al host.

## Verificación

Desde la raíz: backend/.venv/Scripts/python.exe -m pytest -q backend/tests. Sin base de prueba, se omiten las pruebas marcadas por RUN_DB_TESTS. La CI incluye PostgreSQL aislado, aplica migración dos veces, ejecuta alembic check y habilita pruebas de integración. Su resultado remoto queda pendiente de observar. No activar RUN_DB_TESTS en una base de trabajo con datos reales.

Las migraciones contienen DDL congelado y no importan modelos actuales. La generación offline no sustituye una ejecución real en PostgreSQL. Futuras modificaciones de modelos exigen otra revisión Alembic.

Referencias: https://docs.sqlalchemy.org/en/20/dialects/postgresql.html y https://alembic.sqlalchemy.org/en/latest/tutorial.html .
