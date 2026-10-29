# Administración de departamentos

API y React permiten administrar departamentos con baja lógica e historial. La migración de auditoría departamental está probada en PostgreSQL aislado y existe un recorrido básico de interfaz; falta completar la matriz de aceptación. Aplica siempre el head del proyecto, conservando datos y cuentas.

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

## Actualización y verificación

Sigue el arranque y las migraciones del README. No repitas seed ni bootstrap. Después, verifica `/health/db` y abre Departamentos con una cuenta Admin RH autorizada.

La evidencia 68 registra alta, renombrado, baja y reactivación con historial de un departamento simulado. Las migraciones y pruebas PostgreSQL se ejecutaron posteriormente en un clúster aislado. Esos resultados no acreditan un check actual del entorno de uso ni todos los escenarios concurrentes. Consulta QA y completa la matriz de aceptación antes de cerrar RF-7/RF-8.
