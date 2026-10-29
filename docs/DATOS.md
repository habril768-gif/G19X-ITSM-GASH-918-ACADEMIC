# Datos y migraciones

## Persistencia

PostgreSQL almacena usuarios, credenciales y sesiones, departamentos, catálogos, incidencias, participantes, ciclos e historial. También conserva trabajos IA, sugerencias y entregas de correo. SQLAlchemy define los modelos; Alembic mantiene la evolución sin crear tablas automáticamente al iniciar la API.

Los archivos de migración y sus identificadores se conservan para reproducir y auditar el esquema. No deben renombrarse ni reemplazarse por una copia de tablas vacías.

## Preparar o actualizar la base

Desde la raíz, con los servicios iniciados:

```powershell
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
```

La revisión requerida por el código está en `app/core/database.py`; `/health/db` devuelve 503 si no coincide o la conexión falla. `alembic check` detecta diferencias con los modelos. Consulta [el entorno Docker](../infra/README.md) para configuración; nunca publiques credenciales o salidas de variables resueltas.

Las migraciones conservan las cuentas y datos existentes. No ejecutes bootstrap, seed ni downgrade para actualizar. Las reversiones que comprometen credenciales o auditoría están deshabilitadas; una recuperación necesita un procedimiento y respaldo validados.

## Reglas del modelo

| Área | Restricción principal |
| --- | --- |
| Identidad | Correo único sin distinguir mayúsculas, credenciales separadas y sesiones revocables |
| Ámbito | PERSONA requiere afectado; ENTORNO no lo admite y exige departamento reportado |
| Historia departamental | Se conserva el departamento del caso al crearse; un traslado no reescribe ese origen |
| Clasificación | Categoría/prioridad oficiales requieren confirmación humana vigente; editar contenido la invalida |
| Participantes | Declaración y revisión independientes, con motivos y trazabilidad |
| Ciclos | Resolución y cierre exigen validación; reapertura conserva el ciclo anterior en auditoría |
| IA | Texto revisado y revisión de contenido, intentos y propietario de trabajo; no envía descripciones históricas al migrar |
| Correo | Outbox ligada al evento de negocio y revalidación de permisos antes de SMTP |

Las restricciones SQL se complementan con autorización y servicios transaccionales. Tener una FK o una tabla no demuestra que una operación esté permitida.

## Analítica

`analytics.incident_metrics` y `analytics.export_info` son vistas de lectura agregada con barrera de seguridad y supresión por privacidad. La cuenta BI solo debe acceder a ellas, sin permisos sobre tablas operativas. Su actualización se deriva de cada consulta; una importación Power BI conserva una instantánea hasta refrescar.

Consulta [ANALITICA.md](ANALITICA.md) para población, granularidad, denominadores, mínimos y límites. No sumar celdas para reconstruir datos suprimidos ni reemplazar NULL por cero.

## Datos de prueba y validación

La [carga DEMO](DATOS_DEMO.md) es explícita, transaccional y sin contraseñas predeterminadas. No se ejecuta como parte de una actualización. Para pruebas completas utiliza [PostgreSQL aislado](PRUEBAS_POSTGRESQL.md); no apuntes pruebas o seeds a una base real.

La última ejecución registrada aprobó 201 pruebas backend en un clúster temporal, con migración repetida y check sin diferencias. No acredita por sí sola el estado actual de la base de uso ni una restauración de respaldo. Los resultados y límites están en [QA](REPORTE_QA.md).
