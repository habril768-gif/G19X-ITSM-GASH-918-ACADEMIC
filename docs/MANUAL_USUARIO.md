# Manual de usuario de PluriOne

## Propósito y preparación

Esta guía explica el uso del panel local con datos ficticios. Antes de comenzar, el operador debe iniciar los servicios y provisionar tu cuenta según la [guía de inicio](../README.md). La entrega integral sigue pendiente; no se deben registrar datos laborales reales en este entorno.

Abre http://127.0.0.1:5173/ o la dirección local indicada por el operador. Necesitas tu correo y contraseña propios. No hay registro público ni contraseña compartida. No incluyas credenciales, datos personales reales o información sensible en capturas de soporte.

## Qué puede hacer cada perfil

| Perfil | Tareas habituales | Límite principal |
| --- | --- | --- |
| Empleado | Registrar sus incidencias personales o riesgos de su departamento; consultar lo permitido | No clasifica, asigna ni resuelve; un caso confidencial puede dejar de ser visible incluso para quien lo registró |
| Supervisor | Consultar y gestionar casos permitidos de su departamento | No accede a confidenciales ni casos en que esté involucrado; no cierra ni reabre |
| Admin RH independiente | Gestionar casos permitidos, revisar participantes/protección, cerrar/reabrir y administrar cuentas/departamentos | Su rol no le permite gestionar un caso en el que esté involucrado |
| Destinatario de reportes | Consultar el informe agregado autorizado | Gerencia no es un rol de acceso al panel de expedientes |

La asignación o un enlace de correo no conceden permisos adicionales. Una declaración de participación sobre un gestor puede restringirle el expediente inmediatamente. El operador puede provisionar otro RH cuando se requiera una persona independiente; no se debe usar una segunda cuenta de la misma persona para eludir la restricción.

## Entrar, salir y cambiar contraseña

1. Introduce correo y contraseña e inicia sesión.
2. Comprueba las opciones visibles y el perfil de la cabecera. Si no corresponde al autorizado, informa al administrador.
3. Al terminar pulsa **Cerrar sesión**. Recargar la página también exige un nuevo acceso porque la sesión del panel no se conserva de forma persistente.

Si se informa un bloqueo por intentos, evita seguir probando contraseñas. El bloqueo temporal es de 15 minutos tras cinco fallos. Solicita al operador el restablecimiento si no recuerdas tu contraseña; no existe recuperación automática por correo.

En **Cambiar contraseña**, introduce la actual, una nueva de 12 a 128 caracteres y su confirmación. Guarda y vuelve a iniciar sesión con la nueva. El cambio revoca las sesiones existentes. Si la respuesta es incierta, no reenvíes el formulario a ciegas: comprueba el acceso o solicita ayuda al operador sin compartir la contraseña.

## Consultar y buscar incidencias

Abre **Incidencias**. Usa los filtros disponibles por identificador/título, estado, prioridad, categoría, responsable y fecha. El total corresponde solo a los resultados autorizados que cumplen los filtros. Revisa la paginación si esperas más resultados.

Abre el título para consultar el expediente. En **Descripción del caso** verás los datos disponibles; **Seguimiento** muestra responsable, resolución y fechas cuando existen. La ausencia de responsable puede mostrarse como Sin asignar. No deduzcas que un caso está resuelto por tener una sugerencia IA.

El historial muestra acciones permitidas y sus motivos cuando corresponda. Su contenido depende del perfil. Si no encuentras un caso, revisa filtros y sesión; también puede haber cambiado tu permiso. No pruebes identificadores de otros expedientes para superar una restricción.

## Registrar una incidencia

1. Pulsa **Nueva incidencia** y elige el ámbito que corresponda.
2. Escribe un título breve y los hechos ficticios concretos, sin contraseñas ni datos personales reales. Completa la fecha del hecho conforme a la prueba.
3. En PERSONA selecciona el afectado permitido; un empleado registra sobre sí mismo. En ENTORNO selecciona el departamento permitido y no inventes una persona afectada.
4. Declara participantes únicamente cuando corresponda, con el motivo de su relación y dentro de las opciones permitidas. No repitas al afectado ni dupliques participantes.
5. Revisa el formulario y envía una sola vez. Conserva el identificador y el acuse.

El acuse acredita que el registro fue recibido; no garantiza acceso posterior al expediente. Si la confidencialidad o un conflicto lo impiden, no se muestra su detalle. En caso de error de red o resultado no confirmado, comprueba primero si el caso existe antes de volver a registrarlo.

Ejemplo ficticio para practicar: título «Prueba — constancia solicitada pendiente de revisión»; descripción «Una persona ficticia solicitó una constancia para un trámite interno. La solicitud está registrada y requiere revisión administrativa; no se indica un vencimiento ni una consecuencia grave». Usa una cuenta DEMO y la fecha elegida para la prueba. La categoría y prioridad oficiales deben confirmarse por un gestor según los hechos, sin adoptar una etiqueta automática por copiar el ejemplo.

## Clasificar, asignar y editar

Las opciones de **Gestionar incidencia** dependen de rol, acceso y estado:

- Revisa los hechos y confirma la categoría y prioridad oficiales. Alta, Media y Baja se determinan por las reglas del PRD y el impacto descrito, no por la sola presencia de una fecha o palabra.
- Asigna un responsable activo y elegible. La lista no autoriza a elegir una persona con conflicto ni a concederle acceso a un confidencial.
- Corrige título o descripción cuando la operación esté permitida. Cambiar la descripción invalida la clasificación anterior; debe validarse de nuevo antes de continuar el ciclo.

Una operación confirmada debe reflejarse en el expediente y su historial. Ante un resultado incierto, actualiza y verifica el estado antes de repetir la escritura. Que un botón no aparezca o una operación sea rechazada puede corresponder a una restricción legítima.

## Avanzar el ciclo de atención

| Estado y acción | Condición y resultado |
| --- | --- |
| Pendiente → En revisión | Gestor autorizado, clasificación humana vigente y responsable elegible |
| En revisión → Resuelta | Resolución escrita y condiciones de clasificación/responsable vigentes |
| Resuelta → Cerrada | Admin RH independiente confirma el cierre |
| Resuelta o Cerrada → En revisión | Admin RH independiente reabre con motivo y responsable elegible; conserva el ciclo anterior |

No hay salto libre entre estados ni edición de un caso finalizado sin reapertura. Si falta clasificación o responsable, completa primero ese requisito. Una reapertura no borra la resolución anterior; consulta el historial autorizado.

## Confidencialidad y participantes

En **Confidencialidad y participantes**, solo un Admin RH independiente puede revisar relaciones y protección. Escribe el motivo de cada cambio. Confirmar o descartar una relación conserva su declaración original. Descartarla no retira automáticamente la confidencialidad.

No declares participantes para probar restricciones sobre el único RH disponible sin disponer de una persona independiente autorizada. Si te declaras a ti mismo, puedes perder acceso al caso. En expedientes resueltos o cerrados se requiere reapertura antes de modificar esta protección.

Los cambios pueden retirar un responsable que perdió elegibilidad o devolver un caso a Pendiente cuando no existe reemplazo permitido. Comprueba el resultado informado; no intentes desactivar las protecciones para conservar acceso.

## Solicitar y revisar asistencia IA

La asistencia es opcional y solo está disponible para gestores elegibles. Si no está activada, está omitida o falla, continúa con la gestión manual.

1. Abre un caso ficticio permitido y revisa los hechos que necesitan clasificación.
2. Escribe en el formulario IA un resumen mínimo simulado. Empieza vacío: no copies información real ni identificadores. Confirma las casillas exigidas.
3. Solicita asistencia una sola vez. Usa **Actualizar asistencia IA** para consultar el trabajo registrado.
4. Lee la sugerencia y su motivo. Una respuesta completada sigue pendiente de validación humana.
5. Confirma la categoría/prioridad oficiales en la sección de clasificación, si estás de acuerdo y los hechos lo justifican. Si la salida es inconclusa, aclara los hechos o clasifica manualmente.

La IA no resuelve el caso, no sustituye revisión humana y no debe usarse como asesoría laboral ni protocolo de emergencia. Los resultados simulados de evaluación no garantizan acierto en un caso nuevo. Las solicitudes al proveedor pueden consumir saldo de la cuenta configurada.

## Notificaciones por correo

Admin RH autorizado puede consultar **Notificaciones por correo** y pulsar **Actualizar correos**. El panel distingue pendientes, procesamiento, omisiones, fallos e intentos. **Aceptada por SMTP** indica aceptación del transporte, no lectura ni recepción confirmada en un buzón externo.

En las pruebas, el operador facilita el buzón Mailpit local en http://127.0.0.1:8025/. Los mensajes contienen aviso mínimo y enlace al expediente. Al abrirlo, inicia sesión si se solicita; el servidor comprueba tu acceso actual. No reenvíes capturas del buzón con información personal.

No se envía correo por todas las operaciones: creación, asignación, resolución y reapertura tienen reglas específicas. Una omisión por falta de destinatario autorizado puede ser correcta. Consulta al soporte si esperabas un aviso; no repitas la operación de negocio solo para generar otro mensaje.

## Administrar usuarios y departamentos

Admin RH dispone de **Usuarios** para alta y actualización de cuentas permitidas. Revisa nombre, correo, rol, departamento y activación según el formulario. Los cambios administrativos requieren motivo cuando se solicite y pueden revocar sesiones o ajustar casos. No se elimina una cuenta ni se cambia su contraseña mediante la edición administrativa general; la recuperación corresponde al operador.

En **Departamentos**, registra o edita el nombre, activación y motivo. La baja es lógica y puede rechazarse si existen usuarios activos o casos abiertos vinculados. Atiende esas dependencias mediante sus procedimientos; no borres datos para forzar la baja. Consulta el historial para revisar cambios confirmados.

El botón **Historial** de Departamentos consulta sus cambios. Usuarios registra auditoría internamente, pero no ofrece una vista de historial administrativo en el panel; solicita su comprobación al operador autorizado. El historial de un expediente es una consulta distinta.

Guías administrativas: [usuarios](ADMIN_USUARIOS.md), [departamentos](DEPARTAMENTOS.md) y [provisión independiente](ADMIN_INDEPENDIENTE.md).

## Leer el informe Power BI

Abre la copia autorizada del informe. Comprueba **Fecha de corte** y la leyenda de población exportable: sus cifras no representan toda la empresa. El mes mostrado corresponde a creación, y las dimensiones son categoría oficial y departamento histórico.

Si una fila indica **Suprimido por privacidad**, sus números deben permanecer vacíos. Vacío no significa cero. No combines otras fuentes ni reduzcas filtros de seguridad para reconstruir esa cifra. Las medidas por celda no deben interpretarse como totales empresariales.

Reapertura y concordancia son indicadores distintos; concordancia compara sugerencia con clasificación humana vigente y no equivale a precisión contra una referencia independiente. La actualización manual requiere conexión autorizada; guardar el archivo no refresca los datos. La revisión de modelo, valores publicables y refresco sigue pendiente según [ANALITICA.md](ANALITICA.md).

## Resolver dificultades y pedir soporte

| Situación | Acción |
| --- | --- |
| No inicia sesión | Comprueba correo, credencial y bloqueo; solicita al operador recuperación si corresponde |
| Vuelve al login | La sesión pudo expirar, revocarse o perderse al recargar; inicia sesión nuevamente |
| No aparece un caso | Revisa filtros y rol; un cambio de protección puede retirar acceso |
| No permite resolver/cerrar | Revisa estado, clasificación vigente, responsable y rol exigido |
| Respuesta de guardado incierta | Actualiza y comprueba antes de reenviar; informa al soporte si sigue incierta |
| IA omitida/fallida | Revisa la elegibilidad sin relajar protección y continúa manualmente |
| No aparece correo | Revisa el seguimiento con RH autorizado; SMTP aceptado no acredita recepción externa |
| Power BI vacío | Comprueba corte, población y privacidad; no conviertas valores suprimidos en cero |

Informa pantalla, acción, resultado esperado/observado y hora aproximada. Incluye identificador ficticio solo si el receptor está autorizado. Adjunta un recorte sanitizado, sin contraseñas, tokens, claves o datos reales. El [plan de soporte](PLAN_MANTENIMIENTO.md) establece cómo escalar; este manual no declara una capacitación impartida ni una aceptación completa.
