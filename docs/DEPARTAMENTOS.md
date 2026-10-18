# Administración de departamentos — API 0.9.0 / React 0.6.0

Preparado el 17 de octubre de 2026. Migración 0004 añade exclusivamente department_audit_events. No cambia cuentas, incidencias, identidades ni las migraciones 0001–0003. La aplicación real de 0004 permanece pendiente: el acceso a Docker desde el entorno del asistente devolvió permission denied para dockerDesktopLinuxEngine.

## Reglas y uso

Admin RH dispone de menú Departamentos: listado paginado de activos/inactivos, alta, renombrado, baja lógica, reactivación e historial paginado. Nombre de 1–120 caracteres y motivo de 1–2000, sin textos vacíos. API rechaza nombres duplicados sin distinguir mayúsculas en las escrituras administradas y conserva los existentes. Los límites y autorizaciones se validan también en servidor.

Alta siempre activa. Baja mediante edición de is_active; no existe borrado físico. La baja se rechaza con 409 si hay cualquier usuario activo del departamento o casos PENDIENTE/EN_REVISION vinculados: ENTORNO usa departamento reportado; PERSONA, departamento actual del afectado, aunque su cuenta esté inactiva. Primero se trasladan/desactivan cuentas con su procedimiento auditado y se atienden los casos. No se cambia automáticamente personal, asignaciones, sesiones ni expedientes. La cuenta del propio RH sigue activa y, por ello, bloquea desactivar su departamento.

RESUELTA/CERRADA no bloquean por sí solas la baja: conservan ID de departamento histórico/reportado y resolución. Renombrar conserva ID y asociaciones; no crea una copia histórica del nombre. Un departamento inactivo no aparece entre las opciones activas para asignar cuentas. Los listados ya abiertos se actualizan al volver a entrar o pulsar actualización; la API rechaza opciones que se hayan desactivado entre carga y envío.

Cada escritura guarda actor, fecha, motivo, valores anteriores y posteriores en department_audit_events en la misma transacción. Fallo de auditoría revierte también la mutación. Catálogos anteriores empiezan sin eventos; no se fabrica historial retrospectivo. Lectura de auditoría exclusiva de RH; no incluye expedientes ni usuarios del departamento.

Mutaciones usan bloqueo administrativo exclusivo compartido con altas/cambios de cuentas y operaciones de incidencias existentes. Se revalida actor después del bloqueo. Las pruebas SQLite no verifican el comportamiento de estos bloqueos en PostgreSQL real. Una operación directa fuera de estos servicios no recibe esas garantías.

UI bloquea doble envío y no presenta modificaciones optimistas como confirmadas. Red/5xx exige actualizar listado antes de repetir y no reintenta escritura automáticamente. 401/403 retiran sesión conforme al cliente existente; 409 no guarda cambios parciales.

## Contratos

- GET /departments?page=1&page_size=20: items (id, nombre, is_active), total y paginación.
- POST /departments: nombre, reason; HTTP 201.
- PUT /departments/{id}: nombre, is_active, reason; HTTP 200.
- GET /departments/{id}/history?page=1&page_size=20: eventos, total y paginación.
- Todas requieren Admin RH; respuestas correctas llevan Cache-Control: no-store.

## Aplicación local pendiente

En PowerShell, desde la raíz del proyecto y con Docker Desktop iniciado:

~~~powershell
docker compose up -d --build --wait api
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
Invoke-RestMethod http://127.0.0.1:8000/health/db
~~~

Esperado: 0004 (head), ausencia de nuevas operaciones de actualización y health/db con status ok. /health sigue comprobando solo disponibilidad del proceso; /health/db exige ahora 0004. No repetir bootstrap/seed ni restablecer contraseñas. La reversión automática está deshabilitada para preservar auditoría; requiere plan y respaldo, como 0002/0003.

Con Vite activo, recargar navegador y entrar como RH. Crear «DEMO - Departamento temporal» con motivo académico, renombrarlo, desactivar y reactivar (sin asignarle usuarios/casos). Consultar Historial y comprobar eventos/motivos. Una captura final del historial: 68-react-departamentos-historial.png, solo datos ficticios y sin credenciales. No crear un departamento si ya existe el nombre de la prueba; reutilizarlo. Este recorrido aún no está acreditado.

## Validación y límites

Pruebas HTTP locales con SQLite/FK; UI con API simulada; compilación y SQL de Alembic offline. Resultados exactos en REPORTE_QA.md. PostgreSQL real, concurrencia, instalación 0004 y recorrido de interfaz permanecen pendientes. La prueba optativa existente de migraciones en esquema transaccional aislado se amplió para aplicar 0004 y comprobar conservación; no se presenta como ejecutada si RUN_DB_TESTS no está habilitado. RF-7/RF-8 parciales.
