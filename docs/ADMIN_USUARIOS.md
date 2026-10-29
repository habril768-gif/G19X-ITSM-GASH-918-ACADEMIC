# Administración de usuarios

La API y el panel permiten crear y actualizar cuentas según permisos. Aplica las migraciones pendientes y reconstruye los componentes afectados al actualizar. La aceptación integral sigue pendiente; resultados y límites en QA.

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

La pantalla React y la administración de departamentos están disponibles en sus guías. El restablecimiento por operador mantiene el CLI; no se incluye reset por RH en pantalla, informes completos de auditoría ni eliminación física. El worker IA revalida permisos. La aceptación completa permanece pendiente.


## Verificación y pendientes

Las pruebas y recorridos de usuarios, revocación y traslados están registrados en [QA](REPORTE_QA.md), [revisión de usuarios](REVISION_ADMIN_USUARIOS.md) y [revisión de traslado](REVISION_TRASLADO_ROL.md). Son registros históricos con alcance acotado, no una lista de instrucciones pendientes. Completar la matriz por rol y concurrencia antes de aceptar RF-7 integralmente.
