# Administración de usuarios — API 0.8.0

Paquete preparado el 16 de octubre de 2026, todavía pendiente de aplicar al proyecto. Mantiene esquema 0003, sin nueva migración. Reconstruir Docker tras aplicarlo.

## API protegida de RH

GET /users: listado paginado (20 por defecto, máximo 100), total, ID, correo, nombre, departamento, rol e is_active. Nunca devuelve credenciales ni sesiones. Orden nombre/ID estable. GET /users/options: roles y departamentos activos. PUT /users/{user_id}: reemplaza los cuatro campos administrativos, con motivo obligatorio. POST /users existente sigue creando cuentas con contraseña privada, ahora coordinado con las actualizaciones. No se permite cambiar correo o contraseña mediante PUT, ni eliminar registros. Las rutas exigen sesión Admin RH y devuelven Cache-Control: no-store. GET /auth/me sirve para comprobar la cuenta de la sesión.

```json
{
  "nombre_completo": "Empleado de prueba",
  "departamento_id": "UUID_DE_DEPARTAMENTO_ACTIVO",
  "rol_id": 3,
  "is_active": false,
  "reason": "Desactivación de cuenta ficticia para prueba académica"
}
```

El ID de usuario se obtiene de GET /users, no de la incidencia. El ID de departamento y catálogo de roles se obtienen de GET /users/options. Roles: ADMIN_RH=1, SUPERVISOR=2, EMPLEADO=3. Para reactivar, enviar is_active=true conservando el rol y departamento deseados. No probar primero con el propio administrador: puede revocar su sesión. Usar una cuenta DEMO y conservar al menos un RH local activo.

Respuesta mínima: id, updated=true, sessions_revoked y cases_adjusted. No expone expedientes en la administración. No usar los contadores para inferir casos ocultos: si una corrección afecta un caso restringido al actor, se rechaza todo con 409 genérico y sin IDs. Un cambio de nombre aislado no revoca sesiones; cambios de rol, departamento o activación sí revocan todas las sesiones del usuario. Reactivar no recupera tokens viejos.

## Protección de casos

Se impide retirar el último Admin RH activo con credencial local y departamento activo. Otro administrador sin credencial local no basta. Se rechazan rol/departamento inválidos, departamento inactivo, texto en blanco y campos extra. No se registra contraseña, hash ni token en eventos.

Al cambiar permisos se revisan todos los casos del MVP bajo bloqueo administrativo. Al promover al afectado o participante DECLARADO/CONFIRMADO a gestor, activa confidencialidad y omite IA. Al degradarlo no retira confidencialidad automáticamente. No se cambia el departamento histórico del caso. Cambio de departamento del afectado puede retirar acceso al supervisor anterior; se revisa la asignación.

Si el responsable pierde acceso: en PENDIENTE queda sin asignar; en EN_REVISION se reasigna a un Admin RH activo independiente por orden estable de ID. Si no existe y el caso es confidencial, vuelve a PENDIENTE sin responsable ni inicio de ciclo actual, guardando el anterior en auditoría. En un caso no confidencial sin reemplazo se rechaza el cambio: asignar primero responsable válido. RESUELTA/CERRADA afectadas por reasignación o nueva confidencialidad exigen reapertura antes del cambio administrativo: no se reescriben registros finalizados silenciosamente. No se permite al administrador modificar indirectamente restricciones de un caso que no podía consultar; debe hacerlo un RH independiente.

Usuario, revocaciones, ajustes y eventos se confirman juntos; 409/422/fallo SQL revierten todo. Auditoría de usuario USUARIO_ACTUALIZADO guarda before/after, motivo y contadores; auditoría por caso guarda estado/asignación/protección anteriores/nuevos y afectado administrativo. 503 es error de datos genérico; no muestra SQL ni secretos.

## Coordinación y límites

PostgreSQL usa advisory lock transaccional 71419322: exclusivo para actualización/alta de usuarios y bootstrap/provisión; compartido para creación/edición/gestión/protección de incidencias. Se toma antes de los bloqueos por fila y se refresca la cuenta del actor después. Así se evita aplicar una mutación con rol cargado antes de una modificación administrativa. Todas esas rutas deben actualizarse juntas. La actualización recorre todos los casos, decisión de MVP; hay que medir rendimiento y estudiar consultas dirigidas al crecer. SQLite no comprueba bloqueo ni comportamiento concurrente real. Los listados son lecturas con autorización por petición; no se promete revocar datos ya entregados.

No incluye pantalla React, administración CRUD de departamentos, reset de contraseña por RH, informes de auditoría de usuario ni eliminación. El operador mantiene el CLI de recuperación/provisión. RF-7 sigue parcial. El trabajador IA y su verificación de permisos siguen pendientes.

## Verificación

En copia aislada: 35 passed in 6.50s (once nuevas de administración, siete de CLI y regresiones de esquema/seed). Pruebas directas de servicios/contratos sobre SQLite, sin solicitudes HTTP nuevas. Primera ejecución: 1 fallo/32 aprobadas por lectura de entidad de sesión sin refrescar en el fixture. Se confirmó revocación mediante consulta persistida y refresh antes de verificar current_user; la ejecución final pasa sin cambiar la función existente de revocación. No se declara pasada suite HTTP completa ni concurrencia/PostgreSQL.

Tras aplicar, desde la raíz:

```powershell
backend/.venv/Scripts/python.exe -m pytest -q backend/tests
docker compose up -d --build --wait
```

Guardar el resultado real de la suite completa. Abrir /docs y comprobar 0.8.0. Iniciar sesión como RH, ejecutar GET /users/options y GET /users; primera evidencia prevista 38-admin-usuarios-listado-200.png, solo Server response y usuarios ficticios, sin Curl ni tokens. Luego probar desactivación de cuenta DEMO, sesión revocada y reasignación con casos simulados. Estas verificaciones todavía no se ejecutaron en el motor del proyecto. No fabricar un resultado aprobado por aplicar este paquete.

## Validación posterior a la preparación

API 0.8.0 aplicada y reconstruida según reporte de la autora; evidencia 38 inspeccionada confirma suite completa ejecutada por ella: 77 passed, 3 skipped, 1 warning in 16.49s. Las tres omitidas son las integraciones PostgreSQL optativas y no se declaran aprobadas; advertencia conocida de TestClient/httpx. La ejecución completa posterior sustituye el pendiente histórico de suite HTTP de este avance. No prueba concurrencia PostgreSQL. Evidencias 39–46 inspeccionadas: listado 200, desactivación y estado inactivo, reactivación y estado activo, rechazo de sesión anterior y nueva sesión RH permitida. La autora reporta prueba en dos pestañas con modificación administrativa desde la cuenta original; los recortes 401 no muestran identidad/token/solicitud previa, por lo que se documentan como respuestas consistentes con la secuencia reportada, sin afirmar causalidad exclusiva frente a expiración. No se observaron contraseñas ni tokens en las capturas revisadas. No se cambiaron .env ni datos por el asistente durante esta consolidación. No hay prueba manual nueva de cambio de rol, traslado con reasignación ni concurrencia; esas comprobaciones no se infieren de las capturas. RF-7 permanece parcial por frontend y administración de departamentos pendientes.
La primera evidencia de listado es 39-admin-usuarios-listado-200.png, porque el número 38 se usó para 38-suite-completa-77-passed.png. Esto actualiza la numeración prevista en la sección anterior. El detalle del recorrido y los pendientes están en REVISION_ADMIN_USUARIOS.md.

## Validación manual de traslado y rol — 17 de octubre de 2026

Recorrido verificado y límites en REVISION_TRASLADO_ROL.md: traslado con reasignación a RH, departamento histórico inmutable, promoción con protección automática y restauración de rol sin desmarcar confidencialidad. Complementa pruebas previas de activación/revocación. Sin nueva migración ni suite ejecutada por esta revisión.
