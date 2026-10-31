# Aceptación de entrega por roles

Fecha de preparación: 30 de octubre de 2026. Esta matriz reúne evidencia existente y recorridos pendientes. La ejecución real de departamentos D01–D08 está registrada en223; no acredita aceptación institucional. El cumplimiento de un requisito no cierra automáticamente toda la plataforma.

## Estado y orden de trabajo

RNF-2 está cumplido en su [alcance QA local de tres procesos](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json). No repetirlo para aumentar evidencias. **Departamentos con Admin RH (D01–D08) ya fue observado conforme en223.** Siguen restricciones de Supervisor y Empleado y controles pendientes del MVP. No repetir la clasificación de IA ya confirmada ni modificar expedientes conservados de pruebas anteriores.

Las pruebas automáticas de backend y PostgreSQL del [CI 41165580804](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/41165580804) corresponden al código actual de la aplicación. No sustituyen interacción real en el panel ni aprobación de una persona. Los escenarios API usan sus fixtures/aislamiento; no atribuirles una sesión real de los usuarios de la instalación.

| ID | Escenario | Evidencia disponible | Pendiente de aceptación |
| --- | --- | --- | --- |
| A01 | Rendimiento de lectura, detalle, creación y actualización | Formal local aprobada [220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json) | Cerrado en el alcance declarado; revalidar solo ante cambios relevantes |
| A02 | Crear, renombrar, desactivar y reactivar departamento; auditoría | [Pruebas de departamentos](../backend/tests/test_departments.py), ejecutadas por CI; fuente del [panel](../frontend/src/pages/Departments.jsx) | D01–D08 observado conforme en [223](evidencias/223-departamentos-admin-rh-recorrido-ui.json); baja final conservada |
| A03 | Nombre duplicado, motivo obligatorio y rechazo de baja con usuarios/casos | Pruebas de departamentos: validación, duplicados y bloqueos | Duplicado observado rechazado en223; motivo vacío y bloqueos con dependencias siguen pendientes de recorrido real aislado |
| A04 | Supervisor y Empleado no administran departamentos | Prueba API `test_non_admin_cannot_list_write_or_read_history` | Sesiones reales: verificar acceso y rechazo sin inferir seguridad solo por botón oculto |
| A05 | Administrar usuarios y revocar acceso sin perder historial | [Pruebas de usuarios](../backend/tests/test_user_administration.py) | Recorrido real pendiente; usar cuentas ficticias nuevas, nunca el último Admin RH ni cuentas requeridas para otros recorridos |
| A06 | Empleado registra y consulta su expediente | [111](evidencias/111-supervisor-empleado-ui.json): capturas/confirmación de la autora | Evidencia parcial existente; completar solo diferencias de la matriz, no repetir el mismo caso |
| A07 | Empleado no ve expediente ajeno | [114](evidencias/114-empleado-caso-ajeno-ui.json): aviso sin contenido en sesión distinta | Parcial: negativa visual no reemplaza matriz API de confidencialidad/conflictos |
| A08 | RH revisa, resuelve, cierra y reabre | [112](evidencias/112-rh-ciclo-reapertura-ui.json), [204](evidencias/204-correo-cierre-recorrido-local-verificado.json) | Mantener alcance parcial y procedencia de cada observación; no cambiar los expedientes protegidos para completar filas |
| A09 | Correo por creación, asignación, resolución y cierre | [204](evidencias/204-correo-cierre-recorrido-local-verificado.json), [captura 206](evidencias/206-correo-cierre-mailpit.jpg) | Positivo local verificado; exclusiones, fallos y reintentos negativos reales pendientes; no acredita buzón externo |
| A10 | Confidencialidad, participantes y conflictos de interés | [Pruebas de incidencias](../backend/tests/test_incidents.py) | Matriz integral real y concurrencia adicional pendientes; conservar denegaciones y no mostrar contenido sensible |
| A11 | Uso del panel en ancho reducido | [113](evidencias/113-vista-estrecha-empleado.json) | Emulación parcial existente; no es teléfono físico ni auditoría de accesibilidad |
| A12 | Recuperación y continuidad | [103](evidencias/103-recuperacion-aislada.json) | Ensayo lógico nativo aprobado; instalación completa/secuencia Docker siguen pendientes según [mantenimiento](PLAN_MANTENIMIENTO.md) |
| A13 | Custodia, retención y retirada de copias/analítica | Procedimiento en mantenimiento; evidencias BI conservadas | Requiere responsables/destino/plazo reales y operación autorizada; no inventar datos o constancias |
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
