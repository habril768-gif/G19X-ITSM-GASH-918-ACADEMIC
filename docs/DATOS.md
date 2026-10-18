# Modelo de datos y migración 0003

API 0.4.0. Base funcional: PRD 1.9. Las revisiones 0001 y 0002 permanecen intactas; la 0003 añade estructura para incidencias. No implementa aún sus endpoints ni las reglas completas de autorización.

## Cambios de esquema

| Cambio | Regla |
| --- | --- |
| scope | PERSONA o ENTORNO; PERSONA por defecto |
| affected_employee_id | Obligatorio en PERSONA y nulo en ENTORNO |
| reported_department_id | Departamento reportado obligatorio, con FK |
| department_id_at_creation | Departamento histórico existente, conservado |
| classification_valid | FALSE inicialmente; TRUE exige categoría, prioridad y última validación |
| Resolución | RESUELTA/CERRADA exigen bandera de validación vigente además de campos anteriores |
| ai_status | Añade OMITIDA, que exige motivo no vacío |
| Control IA | Texto revisado, revisor/fecha, motivo de omisión, modelo y versión de prompt |
| incident_involved_users | Pareja caso/usuario única; declaración, revisión y estado DECLARADO/CONFIRMADO/DESCARTADO |

ENTORNO acepta solo categoría Riesgos (ID estable 4 del catálogo inicial), o categoría nula mientras esté pendiente. No permite resolver sin categoría ni prioridad. La revisión de participante requiere motivo, actor/fecha y prohíbe que el actor sea el propio participante. La independencia respecto a otros involucrados y las exclusiones de acceso deben implementarse en los servicios; una restricción por fila no cubre todas las relaciones.

Los CHECK de la base validan combinaciones y referencias, pero no ejecutan transiciones ni escriben auditoría automáticamente. La edición de descripción deberá invalidar la bandera en la misma transacción en el servicio futuro. No se crean casos ni participantes por arrancar la API.

## Conservación de casos previos

0003 asigna PERSONA a cada caso existente y copia reported_department_id desde department_id_at_creation, sin recalcular historia con el departamento actual del afectado. Preserva IDs, textos, fechas y auditoría. Conserva clasificación vigente solo si ya hay categoría, prioridad y actor/fecha de validación; no crea una validación humana nueva. Se añaden restricciones después del relleno. Los casos resueltos válidos de 0002 cumplen esos campos.

El código de migración contiene DDL congelado y no importa los modelos actuales. La operación PostgreSQL es transaccional. No se permite downgrade automático por el riesgo de perder datos de entorno/participantes. No borrar volúmenes para resolver errores.

## Aplicar desde la raíz

Con Docker Desktop abierto, sin cambiar .env:

```powershell
docker compose up -d --build --wait
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
```

Se espera 0003 (head) y sin operaciones nuevas pendientes. Antes de aplicar sobre datos importantes, realizar el respaldo indicado por el procedimiento del proyecto; no hay respaldo automático en este avance.

GET /health/db devuelve 200 solo con conexión y revisión 0003. El liveness /health no depende de la migración. Hasta aplicar la actualización puede verse 503 en /health/db. Las cuentas y sesiones existentes no se eliminan.

Capturas previstas: docs/evidencias/12-migracion-incidencias.png y 13-db-health-0003.png. La respuesta de /health/db no incluye credenciales. No es necesario repetir bootstrap ni proporcionar contraseñas por esta migración.

## Validación

Pruebas SQLite con FK habilitadas: ámbito/afectado, categoría de entorno, bandera, omisión IA, revisión de participantes y resolución sin revalidar. Prueba offline Alembic: compila 0002→0003 y confirma relleno/creación sin DROP TABLE.

Prueba PostgreSQL optativa: crea un esquema QA aislado en una transacción, aplica 0001/0002, inserta dos casos simulados, aplica 0003 y comprueba conservación, relleno y alta ENTORNO. Revierte la transacción al terminar. Solo se ejecuta con RUN_DB_TESTS=1 contra base de pruebas; la CI preparada usa PostgreSQL aislado y alembic check. No ejecutar contra datos reales.

Resultados actuales y límites en REPORTE_QA.md. Generar SQL o pasar pruebas SQLite no equivale a haber aplicado 0003 en PostgreSQL.

## 17 de octubre de 2026 — Migración 0004 preparada

Añade department_audit_events (id UUID, department_id FK, actor_id FK, detalle JSONB, fecha timestamptz) e índice por departamento. Generación UUID a cargo del modelo, como tablas anteriores. Catálogo departamentos y sus referencias permanecen intactos; no se rellenan eventos de altas históricas. Servicio transaccional escribe valores antes/después y motivo; no se añade FK ficticia a un expediente ni se reutiliza USUARIO_ACTUALIZADO para departamentos.

Readiness exige 0004. La compilación offline y pruebas SQLite no acreditan aplicación PostgreSQL. Ampliada prueba optativa de esquema aislado para comprobar preservación de tres casos y catálogo al aplicar 0004. Actualización real pendiente por falta de acceso al pipe de Docker del entorno del asistente; comandos y restricciones en DEPARTAMENTOS.md. Reversión automática deshabilitada para conservar auditoría.
