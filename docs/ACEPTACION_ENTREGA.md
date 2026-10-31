# Aceptación de entrega por roles

Fecha de preparación: 30 de octubre de 2026. Esta matriz reúne evidencia existente y recorridos pendientes. La ejecución real de departamentos D01–D08 está registrada en223; no acredita aceptación institucional. El cumplimiento de un requisito no cierra automáticamente toda la plataforma.

## Estado y orden de trabajo

RNF-2 está cumplido en su [alcance QA local de tres procesos](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json). No repetirlo para aumentar evidencias. **Departamentos con Admin RH (D01–D08) ya fue observado conforme en223.** Siguen restricciones de Supervisor y Empleado y controles pendientes del MVP. No repetir la clasificación de IA ya confirmada ni modificar expedientes conservados de pruebas anteriores.

Las pruebas automáticas de backend y PostgreSQL del [CI 41165580804](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/41165580804) corresponden al código actual de la aplicación. No sustituyen interacción real en el panel ni aprobación de una persona. Los escenarios API usan sus fixtures/aislamiento; no atribuirles una sesión real de los usuarios de la instalación.

| ID | Escenario | Evidencia disponible | Pendiente de aceptación |
| --- | --- | --- | --- |
| A01 | Rendimiento de lectura, detalle, creación y actualización | Formal local aprobada [220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json) | Cerrado en el alcance declarado; revalidar solo ante cambios relevantes |
| A02 | Crear, renombrar, desactivar y reactivar departamento; auditoría | [Pruebas de departamentos](../backend/tests/test_departments.py), ejecutadas por CI; fuente del [panel](../frontend/src/pages/Departments.jsx) | D01–D08 observado conforme en [223](evidencias/223-departamentos-admin-rh-recorrido-ui.json); baja final conservada |
| A03 | Nombre duplicado, motivo obligatorio y rechazo de baja con usuarios/casos | Pruebas de departamentos: validación, duplicados y bloqueos | Duplicado observado en223; motivo obligatorio [231](evidencias/231-departamento-motivo-obligatorio-confirmado.json) y rechazo con usuario activo vinculado [232](evidencias/232-departamento-bloqueo-usuario-activo-confirmado.json), confirmados por usuaria. [233](evidencias/233-departamento-incidencia-pendiente-confirmado.json): rechazo con incidencia Pendiente y cuenta de prueba inactiva reportados. Recorrido manual cubierto con límites: aviso genérico, otras dependencias y causa exclusiva sin inspección independiente; sin HTTP/SQL |
| A04 | Supervisor y Empleado no administran departamentos | Prueba API `test_non_admin_cannot_list_write_or_read_history` | [226](evidencias/226-visibilidad-administracion-supervisor-empleado-confirmada.json): autora confirma ausencia de controles en Supervisor y Empleado; parte visual verificada por reporte textual. [240](evidencias/240-rechazos-api-supervisor-empleado-confirmados.json): roles verificados por /auth/me, GET /users, /users/options y /departments403 en ambas sesiones; logout204. [241](evidencias/241-rechazos-administrativos-ampliados.json): ocho403 por rol incluyen historial y POST/PUT con cuerpos vacíos, con logout204. Recorrido acotado comprobado por salidas de usuaria; escrituras con payload válido/recursos existentes no probadas |
| A05 | Administrar usuarios y revocar acceso sin perder historial | [Pruebas de usuarios](../backend/tests/test_user_administration.py) | [227](evidencias/227-usuario-ficticio-alta-edicion-baja-confirmadas.json): autora confirma alta, renombrado, baja y rechazo genérico al login. [228](evidencias/228-revocacion-sesion-usuario-confirmada.json): en recorrido posterior, usuaria confirma login exitoso y revocación de la sesión abierta tras desactivación. [229](evidencias/229-usuarios-duplicado-motivo-confirmados.json): conflicto por correo y motivo obligatorio confirmados. [238](evidencias/238-expediente-conservado-tras-baja-usuario.json): autora confirma globalmente consulta del expediente ficticio y evento CREADO tras la baja. [239](evidencias/239-auditoria-usuario-ficticio-consulta-lectura.json): consulta READ ONLY aportada muestra11 eventos administrativos, activación/motivos y banderas de revocación. Recorrido acotado de A05 cubierto con límites: conservación reportada para un caso, operación del evento más antiguo/actor y otras combinaciones no comprobados; no aceptación integral |
| A06 | Empleado registra y consulta su expediente | [111](evidencias/111-supervisor-empleado-ui.json): capturas/confirmación de la autora | Evidencia parcial existente; completar solo diferencias de la matriz, no repetir el mismo caso |
| A07 | Empleado no ve expediente ajeno | [114](evidencias/114-empleado-caso-ajeno-ui.json): aviso sin contenido en sesión distinta | [242](evidencias/242-empleado-expediente-ajeno-404.json): detalle/historial/participantes404 con rol Empleado verificado y logout204; caso consultable previamente como RH en238. [243](evidencias/243-control-admin-expediente-200.json): posterior control Admin RH obtiene200 en las mismas tres rutas y logout204. Contraste por sesiones sucesivas, no simultáneas; recorrido acotado, sin matriz completa de confidencialidad/conflictos |
| A08 | RH revisa, resuelve, cierra y reabre | [112](evidencias/112-rh-ciclo-reapertura-ui.json), [204](evidencias/204-correo-cierre-recorrido-local-verificado.json) | Mantener alcance parcial y procedencia de cada observación; no cambiar los expedientes protegidos para completar filas |
| A09 | Correo por creación, asignación, resolución y cierre | [204](evidencias/204-correo-cierre-recorrido-local-verificado.json), [captura 206](evidencias/206-correo-cierre-mailpit.jpg) | Positivo local verificado; exclusiones, fallos y reintentos negativos reales pendientes; no acredita buzón externo |
| A10 | Confidencialidad, participantes y conflictos de interés | [Pruebas de incidencias](../backend/tests/test_incidents.py) | Matriz integral real y concurrencia adicional pendientes; conservar denegaciones y no mostrar contenido sensible |
| A11 | Uso del panel en ancho reducido | [113](evidencias/113-vista-estrecha-empleado.json) | Emulación parcial existente; no es teléfono físico ni auditoría de accesibilidad |
| A12 | Recuperación y continuidad | [103](evidencias/103-recuperacion-aislada.json) | Ensayo nativo103 y restauración lógica Docker [230](evidencias/230-restauracion-docker-confirmada.json) con filas/huellas coincidentes y reanudación confirmada por usuaria. Salud posterior confirmada en [234](evidencias/234-salud-posterior-reanudacion-docker.json): API healthy y health/db ok. Pendiente: recuperación integral de instalación y secuencias/roles/ACL; ver [mantenimiento](PLAN_MANTENIMIENTO.md) |
| A13 | Custodia, retención y retirada de copias/analítica | Procedimiento en mantenimiento; evidencias BI conservadas | [235](evidencias/235-custodia-respaldo-confirmada.json): autora asume responsabilidad del respaldo en RespaldosPluriOne de su computadora. [236](evidencias/236-conservacion-respaldo-acordada.json): conservación hasta concluir evaluación y atender observaciones finales. Parcial: disposición posterior pendiente; sin comprobación de acceso restringido, copia adicional o entrega. Analítica mantiene pendientes propios |
| A14 | Manuales, capacitación y aceptación final | [Manual de usuario](MANUAL_USUARIO.md), [manual técnico](MANUAL_TECNICO.md), [MVP](MVP.md) | Validar recorridos pendientes y registrar capacitación/aprobación únicamente cuando ocurran |

## Preparar el entorno de uso

La comprobación de preparación obtuvo HTTP 200 del panel en 5173; la API 8000/health/db no fue accesible en ese momento. No se deduce la causa exacta ni se da por arrancada la instalación. El agente no pudo operar el daemon Docker desde su sesión; el operador ejecuta el arranque en su PowerShell.

Desde la raíz del proyecto, manteniendo `.env`, cuentas y volúmenes existentes:

```powershell
docker compose -f compose.yaml -f compose.rnf2.yaml --profile mail up -d --build --wait
docker compose -f compose.yaml -f compose.rnf2.yaml --profile mail exec api python -m alembic upgrade head
docker compose -f compose.yaml -f compose.rnf2.yaml --profile mail exec api python -m alembic check
```

La actualización de esquema conserva datos; revisar cualquier error antes de continuar. No volver a cargar DEMO ni hacer bootstrap sobre una instalación existente. Si el esquema está desactualizado, la salud HTTP no sustituye la migración/check. El perfil `mail` arranca captura Mailpit y el worker SMTP local; no activa IA ni demuestra envío a personas reales. El override de RNF-2 fija tres procesos API y no transforma este entorno en el fixture de la prueba formal.

Abrir [panel](http://127.0.0.1:5173/) y [Mailpit](http://127.0.0.1:8025/). La sesión Admin RH debe iniciarla la usuaria en el navegador que se vaya a observar; introducir la contraseña únicamente en el panel. Si el frontend deja de responder, iniciar `npm.cmd run dev` desde `frontend` en su propia terminal. [Cuentas DEMO existentes](DATOS_DEMO.md): no publicar contraseñas ni extraer tokens del navegador.

## Primer recorrido: departamentos de Admin RH (A02/A03)

Usar un departamento nuevo, vacío y exclusivamente ficticio. Nombre propuesto: `QA entrega - departamentos - 20261030-01`. Si ya existe, detener la creación y revisar el historial; no reusar ni modificar otro departamento por conveniencia. No asignarle usuarios o incidencias.

| Paso | Acción prevista | Resultado esperado; todavía no observado en este recorrido |
| --- | --- | --- |
| D01 | Admin RH abre **Departamentos** | Catálogo visible sin errores; registrar fecha y rol sin credenciales |
| D02 | **Crear departamento**, nombre propuesto, motivo `Prueba ficticia de aceptación de entrega` | Se guarda como activo y aparece en catálogo; conservar UUID si se puede obtener sin credenciales |
| D03 | Intentar crear nuevamente el mismo nombre y un motivo ficticio | Rechazo por duplicado; no aparece segundo registro ni evento de creación exitoso |
| D04 | Editar solo ese registro, agregar ` - revisado`, motivo `Renombrado ficticio de aceptación` | Nuevo nombre guardado; historial conserva nombre anterior y motivo |
| D05 | Editar, desmarcar **Departamento activo**, motivo `Baja ficticia sin dependencias` | Registro inactivo; no se elimina historial ni cambia otros usuarios/casos |
| D06 | Reactivar el mismo registro, motivo `Reactivación ficticia de aceptación` | Estado activo y nuevo evento auditable |
| D07 | Desactivarlo como cierre, motivo `Fin de prueba ficticia de aceptación` | Queda inactivo y conservado, sin eliminación física |
| D08 | Abrir **Historial** y actualizar catálogo | Cinco cambios exitosos: creación, renombrado, baja, reactivación y baja final; duplicado no se cuenta como cambio exitoso. Registrar los motivos/estados observados y cualquier discrepancia |

Antes de cada escritura, comprobar el nombre/identificador del objeto; detenerse ante resultado incierto para evitar duplicación. No tocar Recursos Humanos, Operaciones u otros departamentos existentes. Los rechazos por usuarios activos o casos abiertos ya tienen pruebas automáticas; no provocarlos desactivando departamentos usados en este recorrido.

## Cómo registrar la ejecución

En una evidencia nueva, indicar fecha real, origen (agente/UI, autora o CI), rol, entorno, datos ficticios, pasos ejecutados y resultado por ID. Estados posibles: observado conforme, observado con fallo, no ejecutado o resultado incierto. Guardar capturas sanitizadas solo de los objetos ficticios y nunca credenciales, cookies o tokens. Un plan o resultado esperado no cuenta como aprobado.

Para A02/A03, registrar UUID/nombre ficticio, estado final inactivo, cinco eventos exitosos esperados y resultado del duplicado; si el panel no permite comprobar un dato, conservarlo como no verificado. La aprobación institucional y la capacitación siguen siendo actividades humanas separadas. La preparación222 no creó datos; la ejecución223 creó y modificó únicamente el departamento ficticio descrito, con estado final inactivo. No se modificó la aplicación.


## Ejecución real de D01–D08 — 30 de octubre de2026

[Evidencia223](evidencias/223-departamentos-admin-rh-recorrido-ui.json): sesión Admin RH introducida por la usuaria en la pestaña integrada y verificada visualmente. El agente ejecutó los ocho pasos y observó resultados conformes. Catálogo pasó de cuatro a cinco filas; intento de nombre repetido rechazado sin segunda fila. Nombre final `QA entrega - departamentos - 20261030-01 - revisado`, estado **Inactivo**. No se expone UUID enUI ni se consultó SQL; no presentarlos como comprobados.

Se observaron cinco cambios en Historial, con motivos y estados, entre23:51:53 y23:52:50 local: creación, renombrado, baja, reactivación y baja final. El duplicado no añadió cambio exitoso. Al pulsar Actualizar departamentos y reabrir Historial persistieron registro inactivo y cinco entradas. [Captura final224](evidencias/224-departamentos-admin-rh-historial-final.jpg) y [rechazo225](evidencias/225-departamento-duplicado-rechazado.jpg). A02 queda verificado enUI; A03 sigue parcial yA04 pendiente, con sus pruebas API independientes. Esta ejecución no cierra usuarios, concurrencia, custodia o aceptación humana.


## Confirmación visual por roles — 31 de octubre de 2026

[226](evidencias/226-visibilidad-administracion-supervisor-empleado-confirmada.json): controles administrativos presentes para RH Independiente Demo y ausentes para Supervisor RH y Empleado, según confirmaciones textuales de la autora. No se observó directamente el panel ni se capturó rechazo HTTP. A04 queda parcial, con su evidencia automatizada independiente; no aceptación integral.


### 2026-10-31 — Usuarios: confirmación de recorrido ficticio

[227](evidencias/227-usuario-ficticio-alta-edicion-baja-confirmadas.json): autora confirma alta/listado, nombre revisado, estado Inactiva y acceso rechazado con aviso genérico. A05 parcial: sin comprobación independiente, auditoría o revocación de sesión previa; no atribuir el rechazo solo a la baja sin verificar credenciales previamente. Registro local, sin repetir pruebas ni publicación remota.


### 2026-10-31 — Revocación de sesión al desactivar usuario ficticio

[Evidencia 228](evidencias/228-revocacion-sesion-usuario-confirmada.json): la usuaria confirma inicio de sesión exitoso con `qa-entrega-20261031-01@example.invalid` y, tras el procedimiento guiado de desactivación desde Admin RH y nueva solicitud desde la sesión abierta, pérdida de acceso con el mensaje «Tu sesión terminó o cambió el acceso de tu cuenta. Inicia sesión nuevamente.» Resultado esperado confirmado por la usuaria; sin observación directa del agente ni inspección HTTP/SQL. Esta comprobación amplía la evidencia 227, cuyos límites originales se conservan.

Propósito: verificar invalidación de sesión existente al desactivar una cuenta. Archivos: evidencia 228 y seguimiento documental de aceptación, QA, bitácora, backlog, entregables y trazabilidad. Validación: registro JSON leído de nuevo y referencia de matriz comprobada. A05 continúa parcial para auditoría y conservación del historial; no se declaran esos puntos probados. Sin cambios de código, repetición de RNF-2 ni publicación remota; registro local agrupado.


### 2026-10-31 — Usuarios: conflicto por correo y motivo obligatorio

[Evidencia 229](evidencias/229-usuarios-duplicado-motivo-confirmados.json): la usuaria confirma rechazo al intentar repetir el correo ficticio existente y bloqueo del formulario al omitir el motivo administrativo. Propósito: ampliar aceptación A05. Validación manual guiada y reportada por la usuaria; JSON y enlaces locales comprobados. Sin inspección HTTP/SQL: el aviso genérico no acredita por sí solo atomicidad y la validación del formulario no sustituye pruebas directas de API. A05 sigue parcial para auditoría y conservación de historial. Evidencia 228 conserva la revocación confirmada. Sin cambios de código ni publicación remota; RNF-2 aprobado se mantiene.


### 2026-10-31 — Consolidación de recuperación Docker y controles de departamentos

Propósito: integrar los resultados manuales aportados por la usuaria, sin repetir pruebas ni modificar código. [230](evidencias/230-restauracion-docker-confirmada.json): respaldo `plurione-20261031-092101.dump`, 75624 bytes, SHA256 `A21826DB6F16EBEA761D83B0DB1BD27D89A801E54CAAB5568AC1A0BB0F0F13B0`; pg_restore sin errores reportados, revisión 0008, cantidades y huellas de contenido de todas las tablas public coincidentes. Destino `plurione-restore-c368a6c78bd8` sin red/puertos según comando, luego detenido; origen reanudado y acceso Admin RH confirmado. La salida ps aún mostraba API health: starting; no declarar healthy posterior del API/worker. No se compararon independientemente secuencias, restricciones, índices, vistas, ACL ni roles globales; no es recuperación completa de instalación ni medición de RTO/RPO.

[231](evidencias/231-departamento-motivo-obligatorio-confirmado.json): la usuaria confirma bloqueo del formulario al omitir motivo. [232](evidencias/232-departamento-bloqueo-usuario-activo-confirmado.json): tras reactivar el departamento ficticio y vincular la cuenta ficticia activa, la baja se rechaza con aviso genérico; después confirma que se guardan las bajas de cuenta y departamento. Ambos quedan inactivos según reporte. Bloqueo por incidencias abiertas sigue pendiente por separado. No inferir respuesta HTTP, auditoría, atomicidad SQL ni validación API a partir del formulario o aviso genérico.

Archivos: evidencias 230–232, matriz de aceptación, mantenimiento, QA, bitácora, backlog, entregables, trazabilidad y MVP. Validación documental: JSON reabiertos, enlaces locales comprobados y matriz contrastada con las confirmaciones. Registros 228/229 conservan revocación, correo duplicado y motivo de usuarios; A05 sigue parcial por auditoría/historial. Sin nuevas pruebas de código, publicación remota ni cambios al cumplimiento de RNF-2. Pendientes: A03 incidencias abiertas, negativos por roles, auditoría de usuarios, recuperación integral, custodia y aceptación humana conforme a la matriz.


### 2026-10-31 — Baja de departamento con incidencia pendiente

[Evidencia 233](evidencias/233-departamento-incidencia-pendiente-confirmado.json): tras la preparación guiada, la usuaria reporta incidencia ficticia `710482ca-a652-4679-9abf-13c3b3553e10` Pendiente y rechazo de baja del departamento con aviso genérico; confirma expresamente que la cuenta ficticia está inactiva. Resultado esperado del recorrido confirmado por reporte, coherente con bloqueo por incidencia abierta. No se inspeccionaron otras cuentas vinculadas, departamento histórico, HTTP/SQL ni causa exclusiva. Conservar incidencia Pendiente y departamento operativo; no borrar ni cerrar para completar evidencias.

Propósito: completar el supuesto manual pendiente de A03. Archivos: evidencia 233, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: lectura JSON y referencia en matriz comprobadas. A03 reúne ahora duplicado observado en223 y motivo/bloqueos reportados en231–233, con sus límites; no equivale a comprobación independiente de todas las precondiciones o aceptación institucional. No hay cambios de código, pruebas automáticas nuevas ni publicación remota. Persisten pendientes de otros escenarios de la matriz.


### 2026-10-31 — Salud confirmada tras reanudar Docker

[Evidencia 234](evidencias/234-salud-posterior-reanudacion-docker.json): salida aportada por la usuaria confirma API, PostgreSQL, Redis y Mailpit healthy; worker de correo Up sin estado de salud reportado. GET /health/db devuelve status ok y database postgresql. Completa la comprobación de salud posterior que seguía pendiente en230; acceso Admin RH ya confirmado. No prueba entrega de correo ni recuperación integral de instalación, roles/ACL o secuencias. Archivos: evidencia234 y seguimiento de aceptación, mantenimiento, QA, bitácora, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces locales comprobados. Sin cambios de código, pruebas automáticas nuevas o publicación remota.


### 2026-10-31 — Responsabilidad y ubicación del respaldo declaradas

[Evidencia 235](evidencias/235-custodia-respaldo-confirmada.json): la autora declara que será responsable del respaldo y que lo conservará en RespaldosPluriOne de su computadora. Se referencia el archivo y hash registrados en230, sin publicar ruta privada ni identidad personal. Propósito: registrar una decisión real de custodia, no una asignación inferida. Archivos: evidencia235, mantenimiento, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlace comprobados. Pendientes: plazo o condición de conservación, acceso restringido no inspeccionado y disposición posterior; no se declara copia adicional o entrega a terceros. A13 continúa parcial y no se extiende esta declaración a exportaciones analíticas. Sin cambios de código, pruebas nuevas ni publicación remota.


### 2026-10-31 — Condición de conservación del respaldo acordada

[Evidencia 236](evidencias/236-conservacion-respaldo-acordada.json): la usuaria acepta conservar el respaldo hasta concluir la evaluación y atender las observaciones finales. Se mantienen responsable y ubicación declarados en235. Propósito: completar condición real de retención del respaldo académico. Archivos: evidencia236, mantenimiento, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación: JSON y referencia comprobados. Sin fecha de vencimiento inventada, eliminación automática, publicación remota o nuevas pruebas. Pendientes: disposición posterior y controles de custodia no inspeccionados; analítica conserva sus decisiones independientes.


### 2026-10-31 — Conservación de expediente tras baja de cuenta

[Evidencia 238](evidencias/238-expediente-conservado-tras-baja-usuario.json): ante la solicitud de comprobar título, descripción, estado Pendiente y evento CREADO del caso ficticio 710482ca-a652-4679-9abf-13c3b3553e10 como Admin RH, manteniendo la cuenta ficticia inactiva, la usuaria confirma globalmente «todo sigue bien». Se registra como confirmación textual guiada, sin observación directa ni verificación independiente por campo/HTTP/SQL. Propósito: comprobar conservación de ese expediente después de la baja; no acredita auditoría administrativa de usuarios ni todos los supuestos de permisos. Archivos: evidencia238, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y referencia comprobados. Sin cambios de código, nuevas pruebas automáticas, modificación indicada del caso ni publicación remota. A05 conserva pendiente auditoría administrativa; alcance de conservación acotado a este caso.


### 2026-10-31 — Auditoría administrativa del usuario ficticio consultada

[Evidencia 239](evidencias/239-auditoria-usuario-ficticio-consulta-lectura.json): salida aportada por la usuaria de consulta READ ONLY muestra11 eventos USUARIO_ACTUALIZADO de la cuenta ficticia, nueve cambios de activación con bandera sessions_revoked=true y motivos; renombrado con true→true y bandera false; evento más antiguo sin los campos proyectados. El código ALTA_LOCAL no guarda esos campos, lo cual es compatible, pero operacion no fue seleccionada y no se confirma esa identidad. La bandera no cuenta sesiones ni reemplaza la comprobación funcional228. Propósito: verificar registro administrativo del recorrido A05. Archivos: evidencia239, matriz, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y referencia comprobados; contraste con api/auth.py y services/users.py. A05 reúne alta/edición/baja reportadas, revocación228, negativos229, expediente238 y consulta239 en su alcance acotado; no aceptación integral de cambios de rol/departamento, concurrencia o todos los expedientes. Sin cambios de código, nueva pantalla, nuevas pruebas automáticas o publicación remota.


### 2026-10-31 — Rechazos administrativos de lectura con dos sesiones reales

[Evidencia240](evidencias/240-rechazos-api-supervisor-empleado-confirmados.json): la usuaria aporta ejecución del auxiliar local para Supervisor RH y Empleado Operaciones2. Rol comprobado mediante /auth/me; GET /users, /users/options y /departments devuelve403 en ambas sesiones; logout204 en ambas. Propósito: complementar controles ocultos226 con denegaciones HTTP reales. Alcance: seis rechazos de lectura y dos cierres de sesión reportados; no se ejecutan escrituras ni historial de departamentos. Tres comprobaciones simuladas previas del auxiliar validaron manejo de403, rol incorrecto y200 inesperado, sin llamadas reales del agente. Archivos: evidencia240, aceptación, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. No se recopilan contraseñas ni tokens. A04 tiene lecturas verificadas por salida de la usuaria; escritura/historial en sesión real permanecen fuera del recorrido, con sus pruebas automatizadas separadas. Registro local, sin publicación en este avance ni cambios de producto.


### 2026-10-31 — Restricciones administrativas ampliadas en sesiones reales

[Evidencia241](evidencias/241-rechazos-administrativos-ampliados.json): Supervisor RH y Empleado Operaciones2, roles comprobados por /auth/me, aportan ocho403 cada uno: lecturas users/opciones/departamentos/historial y POST/PUT de usuarios/departamentos. Dos cierres204. Escrituras con cuerpo vacío y PUT a UUID nulo: se confirma rechazo de esos intentos, no la matriz completa con cuerpos válidos y registros existentes. Auxiliar local con sintaxis y cuatro escenarios simulados comprobados; sin código de producto nuevo ni credenciales registradas. Propósito: ampliar A04 sin generar altas/ediciones válidas. Archivos: evidencia241, aceptación, resumen, QA, bitácora, backlog, entregables y trazabilidad. Validación documental: JSON y referencias comprobados. Se mantienen límites de confidencialidad, concurrencia y aceptación institucional. Registro local, sin publicación remota en este avance.


### 2026-10-31 — Expediente ficticio no disponible para otro Empleado

[Evidencia242](evidencias/242-empleado-expediente-ajeno-404.json): salida aportada por la usuaria con rol EMPLEADO verificado para Empleado Operaciones2: GET detalle, historial y participantes de710482ca-a652-4679-9abf-13c3b3553e10 devuelve404; logout204. Existencia/conservación accesible previamente como Admin RH reportada en238, sin comprobación simultánea nueva. Propósito: ampliar A07 con tres respuestas HTTP reales de no disponibilidad, sin mostrar contenido. Un404 aislado no distingue inexistencia/denegación; no se infieren todos los casos de confidencialidad, relaciones, listados o escrituras. Auxiliar local con sintaxis y tres escenarios simulados verificados; sin nuevas llamadas reales del agente. Archivos: evidencia242, matriz, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. Sin cambios de código de producto o publicación remota en este avance.


### 2026-10-31 — Control positivo Admin RH del expediente ficticio

[Evidencia243](evidencias/243-control-admin-expediente-200.json): rol ADMIN_RH comprobado, detalle/historial/participantes del caso710482ca-a652-4679-9abf-13c3b3553e10 responden200; cierre204, según salida aportada por usuaria. Contrasta con los tres404 de Empleado en242 mediante sesiones sucesivas, sin mostrar contenido. Propósito: confirmar disponibilidad autorizada posterior y reforzar el recorrido A07. No prueba simultaneidad, ausencia de cambios entre sesiones o matriz integral de conflictos/participantes. Correo operativo omitido en nueva evidencia; credenciales/tokens no recogidos. Auxiliar con sintaxis y tres escenarios simulados comprobados. Archivos: evidencia243, aceptación, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. Sin código de producto nuevo, mutaciones de negocio solicitadas ni publicación remota en este avance.
