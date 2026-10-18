# Reporte QA inicial



## 15 de octubre de 2026 — API 0.1.0



Entorno: Windows, Python 3.11, entorno virtual local `backend/.venv`. Sin conexión a datos reales ni servicios de IA.



| Comprobación | Resultado | Evidencia |

| --- | --- | --- |

| GET /health con cliente ASGI | Aprobada | HTTP 200, contenido JSON y contrato esperado |

| Contrato OpenAPI | Aprobada | Ruta /health y referencia HealthResponse presentes |

| Página /docs | Aprobada | HTML disponible con referencia al contrato local |

| Dependencias | Aprobada | pip check: No broken requirements found |

| Arranque Uvicorn | Aprobada | Application startup complete; escucha en 127.0.0.1:8000 |

| Consulta HTTP entre procesos del entorno | No verificada | PowerShell agotó el tiempo de conexión a loopback; no se presenta como prueba HTTP aprobada |

| Secretos y entorno virtual excluidos | Aprobada | git check-ignore sobre .env y backend/.venv/pyvenv.cfg |

| CI de GitHub | Pendiente | Workflow creado; no se ha observado una ejecución remota |



Comando de pruebas desde la raíz: `backend/.venv/Scripts/python.exe -m pytest -q backend/tests`. Resultado: **3 passed, 1 warning**. La advertencia indica deprecación de httpx en TestClient de Starlette; no hay fallos. Se conserva constancia y se revisará la migración al ampliar las pruebas.



La descarga directa mediante pip fue bloqueada por el entorno. Se descargaron ruedas oficiales de PyPI mediante PowerShell y se instalaron localmente con pip --no-index; posteriormente se verificaron los archivos requirements contra el entorno instalado. Los archivos descargados quedan fuera del repositorio. En un equipo con conectividad normal se utiliza el comando documentado de pip.



## Límites de esta validación



No se probaron autenticación, incidencias, PostgreSQL, Redis, Docker, IA, correo, rendimiento ni frontend. Docker no está disponible como comando en este entorno. La prueba de /docs verifica HTML, no un renderizado visual de Swagger UI en navegador. Este reporte no acredita el MVP completo.



## 15 de octubre de 2026 — Configuración Compose



Revisión estática: API con contexto backend, instalación por requirements, PostgreSQL/Redis sin ports, contraseña requerida, healthchecks y volúmenes nombrados. .env y entorno virtual excluidos de Git y del contexto de construcción.



**Pendiente:** validación real de `docker compose config --quiet`, construcción de imagen Linux, arranque de servicios, GET /health, SELECT 1 y PONG. Docker no está disponible como comando. No hay un resultado de contenedores aprobado. La validación automática YAML tampoco se ejecutó por ausencia de los parsers consultados.



Ejecutar los pasos de infra/README.md y guardar las evidencias indicadas en docs/evidencias/README.md. No reutilizar el resultado de pruebas ASGI como evidencia de Docker.



## Evidencias recibidas el 15 de octubre de 2026 — Verificación manual



La autora ejecutó los comandos en su equipo y proporcionó las capturas siguientes. Se inspeccionaron visualmente; no son ejecuciones nuevas del asistente. Esta evidencia complementa las limitaciones históricas descritas arriba.



| Comprobación | Resultado observado | Evidencia |

| --- | --- | --- |

| GET /health desde navegador | HTTP 200 y JSON status ok, service plurione-api | [Captura](evidencias/01-api-health-200.png) |

| Construcción y arranque Compose | Imagen API construida; API, PostgreSQL y Redis healthy | [Captura](evidencias/02-compose-servicios.png) |

| PostgreSQL SELECT 1 | Una fila con valor 1 | [Captura](evidencias/03-postgres-select.png) |

| Redis PING | PONG | [Captura](evidencias/04-redis-ping.png) |



La captura HTTP no permite distinguir por sí sola entre el arranque nativo y Docker. La captura Compose sí acredita la comprobación de salud del contenedor API. No se acredita aún conexión de la aplicación con PostgreSQL o Redis, persistencia tras reinicio, migraciones, autenticación o flujos del MVP.



## 15 de octubre de 2026 — Capa de datos inicial



Resultado local: **8 passed, 2 skipped, 1 warning**. Comando: backend/.venv/Scripts/python.exe -m pytest -q backend/tests.



Pruebas nuevas aprobadas: manejo de caracteres reservados en contraseña sin URL concatenada; respuesta genérica 503 con liveness operativo; respuesta 200 con dependencia simulada; compilación de esquema PostgreSQL con JSONB/fechas y restricciones; generación offline de migración y catálogos. Las tres pruebas HTTP anteriores siguen aprobadas. pip check: sin conflictos.



Las dos pruebas PostgreSQL (esquema/catálogos e identidad Entra única) se omiten sin RUN_DB_TESTS=1. No se presentan como aprobadas. La CI ahora prepara PostgreSQL aislado, aplica migración dos veces, comprueba alineación de modelos y ejecuta integración; no se ha observado su resultado remoto.



Docker instalado localizado, pero conexión al pipe dockerDesktopLinuxEngine denegada para el asistente. Migración real, alembic check y /health/db contra PostgreSQL quedan pendientes. Prueba HTTP 200 nueva usa dependencia simulada y no acredita conexión real. Instrucciones en DATOS.md.



## Evidencias de migración y conexión recibidas el 15 de octubre de 2026



Inspección visual de [05-migracion-inicial.png](evidencias/05-migracion-inicial.png): tres contenedores healthy, revisión 0001 (head) y «No new upgrade operations detected». La autora aplicó y verificó la migración en su equipo.



Inspección de [06-api-db-health-200.png](evidencias/06-api-db-health-200.png): API 0.2.0, GET /health/db, HTTP 200, status ok y database postgresql. Acredita conexión real desde la API y revisión esperada; no son resultados simulados. Los archivos recibidos eran PNG sin extensión y se renombraron sin alterar contenido.



Esto completa la validación manual pendiente de la migración; las dos pruebas automáticas PostgreSQL de la suite no se consideran ejecutadas por estas capturas.



## Fixtures DEMO



Comando: backend/.venv/Scripts/python.exe -m pytest -q backend/tests/test_seed_demo.py. Resultado: **3 passed in 1.35s**. SQLite solo para las tablas auxiliares: roles, departamentos y users. Se verificó repetición sin duplicados, conservación de is_active=False y reversión de transacción.



El intento de suite completa no terminó: se bloqueó en la prueba ASGI preexistente test_api.py::test_health_contract, confirmado con ejecución detallada; ambos intentos se interrumpieron. No se afirma una regresión completa aprobada. La carga DEMO en PostgreSQL y ejecución de CI siguen pendientes. Las ocho pruebas aprobadas del avance anterior permanecen como resultado histórico, no una ejecución nueva.



## Evidencias de carga DEMO recibidas el 15 de octubre de 2026



Se inspeccionaron las capturas proporcionadas por la autora, sin ejecutar nuevamente la carga desde el asistente.



- [07-usuarios-demo.png](evidencias/07-usuarios-demo.png): contenedores healthy y carga completada con departamentos_creados=2, usuarios_creados=6.

- [08-usuarios-demo-sin-duplicados.png](evidencias/08-usuarios-demo-sin-duplicados.png): segunda ejecución completada con ambos contadores en 0.



Resultado: carga inicial en PostgreSQL y repetición sin inserciones adicionales verificadas manualmente. No acredita autenticación SSO, permisos de negocio, conservación de cambios en PostgreSQL ni pruebas automáticas de integración pendientes. No hay credenciales visibles en estas capturas.



## Autenticación local — 15 de octubre de 2026



Suite actual: **20 passed, 2 skipped, 1 warning in 12.72s**. Comando desde raíz: backend/.venv/Scripts/python.exe -m pytest -q backend/tests. Las dos omitidas requieren PostgreSQL de pruebas. La advertencia de TestClient/httpx sigue pendiente de migración de herramienta; no hay fallos. La suite completa sí terminó en esta ejecución.



Pruebas de autenticación en tests/test_auth.py: hash Argon2id; token almacenado solo como digest; errores indistinguibles de cuenta/contraseña; cinco intentos bloquean 15 minutos; logout, expiración y desactivación; empleado sin permiso administrativo; cambio de contraseña revoca todas las sesiones; política de longitud; flujo HTTP login/me/logout y no devolución de secretos en validaciones; alta administrativa auditada sin exponer hash y rechazo de duplicado. SQLite se usa con variantes JSON de los modelos; no sustituye validación PostgreSQL de concurrencia/migración.



Migration offline 0001→0002 compilada sin credenciales; conserva esquema y añade tablas e índice de correo. pip check sin conflictos. Pendientes: aplicación real en PostgreSQL, alembic check y pruebas manuales de autenticación Docker, bootstrap interactivo y ejecución CI. Los resultados manuales de 0001 permanecen como evidencia histórica. No se presentan como verificación de 0002.



## Revisión documental PRD 1.8 — 15 de octubre de 2026



Comprobaciones: ocho requisitos RF únicos, RF-1 a RF-8 presentes en trazabilidad, enlaces locales existentes en documentos modificados, campos de revalidación/participantes/IA omitida declarados y ausencia de marcadores de codificación incorrecta en PRD, backlog, trazabilidad y README. git diff --check sin incidencias.



No se ejecutaron pruebas de aplicación porque esta entrega cambia requisitos/documentación, no código. Los requisitos de entorno, conflicto de interés y classification_valid requieren una migración futura y pruebas: no se consideran satisfechos por la revisión. La última suite de autenticación conserva su resultado histórico de 20 aprobadas y 2 omitidas, sin repetición en este avance.


## Revisión documental 1.9 — 15 de octubre de 2026

Se comprueba PRD con ocho RF y AC-11 a AC-16 en trazabilidad, exclusión de confidenciales en Power BI, supresión complementaria, criterio SIN_CLASIFICACION y ausencia de la afirmación de smoke test ejecutado. No se ejecutó suite funcional; las pruebas nuevas son previstas. Documentos preparados fuera del repositorio por restricción de escritura; pendientes de incorporar.

## 16 de octubre de 2026 — Esquema 0003

Suite completa: **34 passed, 3 skipped, 1 warning in 8.75s**. Comando desde raíz: backend/.venv/Scripts/python.exe -m pytest -q backend/tests. La advertencia de TestClient/httpx continúa; sin fallos en la ejecución final. Las tres omitidas requieren PostgreSQL de pruebas y no se consideran aprobadas.

Cobertura nueva: combinaciones ámbito/afectado, categoría de entorno, vigencia de clasificación y resolución, motivo de omisión IA, datos de revisión del texto, revisión de participantes sin autorrevisión, conservación de declaración y compilación de migración offline. Se corrigieron valores booleanos SQL para no depender de literales de texto en SQLite y la prueba de revisión actualiza sus campos antes de autoflush. pip check sin conflictos. SQL offline de todas las revisiones generado correctamente.

Nueva prueba PostgreSQL preparada: esquema QA transaccional aislado, dos casos previos y aplicación 0003 para verificar preservación y creación ENTORNO. No fue ejecutada aquí. Aplicación real 0003, alembic check y readiness continúan pendientes de terminal Docker autorizada; no se afirman por pasar SQLite.

Evidencias 09–11 inspeccionadas: revisión 0002/alineación, respuesta autenticada 200 con ADMIN_RH y 401 posterior con sesión inválida/expirada. La captura 10 guardada era la vista previa alterada; se reemplazó por la redacción determinística preparada desde el original (bloque opaco, sin alterar otros píxeles). No se reproduce ningún token. El 401 es consistente con logout reportado por la autora; su captura aislada también podría corresponder a expiración, por lo que no demuestra por sí sola causalidad exclusiva de logout.

## 16 de octubre de 2026 — Validación manual de 0003

Capturas aportadas por la autora e inspeccionadas visualmente: [12-migracion-incidencias.png](evidencias/12-migracion-incidencias.png) muestra servicios healthy, revisión 0003 (head) y «No new upgrade operations detected»; [13-db-health-0003.png](evidencias/13-db-health-0003.png) muestra GET /health/db, HTTP 200 y status ok/database postgresql. No se observan tokens en las capturas.

Resultado: actualización y alineación del esquema y conexión desde API verificadas manualmente. No acredita por sí sola preservación con casos previos poblados, pruebas automáticas PostgreSQL omitidas, ni endpoints y permisos de incidencias todavía pendientes. No se ejecutaron comandos Docker desde el asistente en este registro.

## 16 de octubre de 2026 — Registro y consultas API 0.5.0

Suite completa: **45 passed, 3 skipped, 1 warning in 8.67s**. Comando: backend/.venv/Scripts/python.exe -m pytest -q backend/tests. La advertencia TestClient/httpx es conocida; las tres pruebas PostgreSQL siguen omitidas sin RUN_DB_TESTS. pip check sin conflictos.

Once pruebas nuevas en tests/test_incidents.py: registro y cronología reducida; registro de tercero/autor falsificado rechazado; riesgo sin víctima y límites; IDOR y conteos; acuse confidencial sin expediente; Admin RH declarado sin acceso y gestor independiente con acceso; supervisor afectado y promoción dinámica; participantes fuera de ámbito/duplicados; creación por supervisor/admin; rollback ante auditoría fallida; opciones, comodines literales, filtros/paginación y textos vacíos.

Las pruebas HTTP usan SQLite con FK y sustituyen solo current_user por actores ficticios. No acreditan una sesión real PostgreSQL de estos endpoints ni todo el ciclo. La suite de autenticación existente sí se ejecutó junto con ellas. El primer intento HTTP fue interrumpido por bloqueo del entorno; se concedieron sockets locales y la ejecución final terminó.

Pendientes: reconstruir Docker, prueba manual de opciones/registro/listado/detalle con Admin RH, evidencias 14/15. No hay nueva migración: se mantiene 0003. Asignación, transición, revisión de participantes, frontend, IA y correo no se presentan como implementados.

## 16 de octubre de 2026 — Evidencias 14 y 15 revisadas

[Registro 201](evidencias/14-registro-incidencia-201.png): received=true y can_view=true. [Listado 200](evidencias/15-listado-incidencias-200.png): mismo ID, Ausencia simulada, PERSONA, PENDIENTE, total=1, sin responsable ni clasificación validada. Capturas de la autora inspeccionadas visualmente, sin token ni Curl. Acreditan registro y listado básicos en el entorno Docker/PostgreSQL reportado; no prueban por sí solas detalle, historial, permisos entre roles, persistencia tras reinicio ni ciclo completo. No se ejecutó suite nueva para esta revisión.

## 16 de octubre de 2026 — Historial manual verificado

Se inspeccionó docs/evidencias/16-historial-incidencia-200.png, ejecutada y guardada por la autora. HTTP 200, evento CREADO, total=1 y detalle de Ausencia simulada con datos ficticios. No se observan token ni Curl. Se documenta lectura básica del historial para el gestor autenticado; no acredita permisos de otros roles, detalle individual ni el ciclo completo. Sin cambios de código ni nueva ejecución automática. Pendientes: clasificación humana, asignación, transiciones auditadas y revisión de participantes.

## 16 de octubre de 2026 — Gestión API 0.6.0

Ejecución final: backend/.venv/Scripts/python.exe -m pytest -q backend/tests → 51 passed, 3 skipped, 1 warning in 11.14s. pip check sin conflictos. Primera ejecución con cinco pruebas nuevas: 50 passed; se añadió caso de pérdida de acceso del responsable, rollback de transición y reaperturas múltiples, y se repitió suite completa.

Seis pruebas nuevas en test_incidents.py: recorrido de estados y archivo de resolución/fechas; edición y revalidación; roles/IDOR y responsable elegible; categoría de ENTORNO y transiciones inválidas; rollback de validación ante fallo de auditoría; pérdida de acceso del asignado, rollback de resolución y ciclos múltiples. SQLite no demuestra bloqueo concurrente PostgreSQL. Se mantienen tres pruebas de integración omitidas y advertencia conocida TestClient/httpx. No se ejecutó nueva validación Docker desde el asistente. Evidencias manuales 17/18 y ciclo completo siguen pendientes. No se presenta RF-3/RF-4 como terminado.

## 16 de octubre de 2026 — Clasificación manual verificada

Propósito: comprobar confirmación humana del caso simulado. Evidencia 17-clasificacion-validada-200.png aportada por la autora e inspeccionada: HTTP 200, Ausencia simulada, category_id=1, priority=2, classification_valid=true, validated_by y validated_at presentes. Sigue PENDIENTE y sin responsable. Sin token ni Curl visibles. Se actualiza seguimiento, sin cambios de código ni nueva ejecución automática. Pendientes: asignación y prueba manual del ciclo, concurrencia PostgreSQL e integraciones. Esta captura no acredita ejecución de IA.

## 16 de octubre de 2026 — Asignación manual verificada

Propósito: comprobar asignación del caso simulado. Evidencia 18-asignacion-200.png ejecutada por la autora e inspeccionada: HTTP 200, Ausencia simulada, assigned_to con ID de gestor, clasificación vigente y estado PENDIENTE. Sin Curl ni token visibles. Cambio: seguimiento documental y referencia a evidencia. Sin cambios de código ni nueva ejecución automática. Resultado: asignación básica acreditada; asignar no inicia revisión automáticamente. Pendientes: prueba manual de transiciones y archivo de ciclos; controles de acceso entre roles y concurrencia real no se acreditan con esta captura.

## 16 de octubre de 2026 — Inicio de revisión verificado

Propósito: comprobar entrada en revisión del caso simulado. Evidencia 19-en-revision-200.png ejecutada por la autora e inspeccionada: HTTP 200, Ausencia simulada en EN_REVISION, responsable asignado y classification_valid=true. Sin Curl ni token visibles. Cambio: actualización documental. Resultado: transición básica acreditada; no se comprueba cycle_start_at en esta captura porque no se expone en la respuesta. Sin cambios de código ni pruebas automáticas nuevas. Pendientes: resolución, cierre, reapertura e historial de ciclos manuales; concurrencia PostgreSQL.

## 16 de octubre de 2026 — Resolución manual verificada

Propósito: comprobar resolución del caso simulado. Evidencia 20-resuelta-200.png ejecutada por la autora e inspeccionada: HTTP 200, Ausencia simulada en RESUELTA, resolution_text con acción simulada, resolved_at presente, clasificación vigente y closed_at nulo. Sin Curl ni token visibles. Cambios: seguimiento documental. Resultado: resolución básica acreditada, todavía sin cierre. Sin cambios de código ni ejecución automática nueva. Pendientes: cierre, reapertura y revisión del historial de ciclos; concurrencia real PostgreSQL.

## 16 de octubre de 2026 — Cierre manual verificado

Propósito: comprobar cierre del caso simulado. Evidencia 21-cerrada-200.png ejecutada por la autora e inspeccionada: HTTP 200, Ausencia simulada en CERRADA, closed_at presente y resolución/fecha de resolución conservadas. Sin Curl ni token visibles. Cambio: seguimiento documental. Resultado: cierre básico acreditado; la captura no demuestra por sí sola bloqueo de ediciones ni permisos entre roles. Sin cambios de código ni nuevas pruebas automáticas. Pendientes: reapertura e historial de ciclos manuales y concurrencia PostgreSQL.

## 16 de octubre de 2026 — Reapertura manual verificada

Propósito: comprobar retorno del caso cerrado a revisión. Evidencia 22-reapertura-200.png ejecutada por la autora e inspeccionada: HTTP 200, Ausencia simulada en EN_REVISION, responsable y clasificación vigente conservados; resolution_text, resolved_at y closed_at nulos. Sin Curl ni token visibles. Cambio: seguimiento documental. Resultado: reapertura básica acreditada. La captura no muestra el motivo ni la conservación del ciclo anterior; verificar ambos mediante historial. Sin cambios de código ni ejecución automática nueva. Pendientes: historial de reapertura y concurrencia PostgreSQL; RF-4 continúa parcial.

## 16 de octubre de 2026 — Historial de reapertura, revisión parcial

Propósito: comprobar auditoría de reapertura. Evidencia 23-historial-reapertura-200.png ejecutada por la autora e inspeccionada: HTTP 200, evento REAPERTURA; after muestra EN_REVISION con campos finales nulos y before muestra CERRADA con fechas de resolución/cierre anteriores. El bloque está recortado: no son visibles resolution_text anterior ni reason, por lo que no se declaran verificados manualmente todavía. Sin token ni Curl visibles. Cambios: registro documental, sin código ni pruebas automáticas nuevas. Resultado: evento y conservación de estado/fechas anteriores acreditados parcialmente; completar evidencia del texto y motivo. RF-4 continúa parcial y concurrencia PostgreSQL pendiente.

## 16 de octubre de 2026 — Detalle de reapertura confirmado

Evidencia complementaria 23b-historial-reapertura-detalle.png aportada por la autora e inspeccionada. HTTP 200: before conserva estado CERRADA, resolución simulada y fechas previas; reason conserva el motivo de información adicional simulada; source=HUMANA y operation=transition. Complementa la captura 23, donde se veía el evento REAPERTURA y after. Resultado: conservación del ciclo anterior y motivo verificados visualmente para este caso. Cambios: seguimiento documental, sin código ni nuevas pruebas automáticas. Sin Curl ni token visibles. Esto no acredita concurrencia real, permisos de todos los roles ni revisión de participantes/confidencialidad; RF-4 sigue parcial.

## 16 de octubre de 2026 — Pruebas de protección 0.7.0

Suite final: 59 passed, 3 skipped, 1 warning in 13.60s; backend/.venv/Scripts/python.exe -m pytest -q backend/tests. pip check sin conflictos. Ocho pruebas nuevas en test_incidents.py verifican revisión independiente, conservación de declaración, descarte sin desmarcar protección, reincorporación confirmada, reasignación al involucrar supervisor, bloqueo de actor involucrado, retorno a PENDIENTE sin RH independiente, motivos/estados terminales, rollback completo ante fallo de auditoría, responsable explícito, afectado gestor, límite 20 y participantes inactivos. Se usan SQLite y actores simulados: no acredita concurrencia PostgreSQL ni sesión real de estas rutas. Tres integraciones PostgreSQL omitidas y advertencia TestClient/httpx conocida. Evidencia 24 y prueba manual del módulo pendientes; no se declara RF-4 completo.

## 16 de octubre de 2026 — Evidencia 24, acuse de protección

La autora guardó 24-confidencialidad-200.png y se inspeccionó visualmente. Muestra HTTP 200 con received=true y can_view=true para el mismo expediente. Es el acuse de la operación, no el detalle GET solicitado: no muestra is_confidential ni ai_status. Resultado: acuse verificado; confidencialidad persistida y omisión IA pendientes de evidencia del detalle. Sin token/Curl visibles, sin código ni pruebas automáticas nuevas. Se solicita conservar acuse y añadir captura complementaria del GET.

## 16 de octubre de 2026 — Detalle de confidencialidad confirmado

Propósito: verificar el resultado persistido de protección. Evidencia 24b-confidencialidad-detalle-200.png aportada por la autora e inspeccionada: HTTP 200, Ausencia simulada en EN_REVISION, is_confidential=true, ai_status=OMITIDA y motivo de clasificación manual; conserva responsable RH y clasificación vigente. Complementa el acuse 24. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni pruebas automáticas nuevas. Resultado: protección y omisión IA verificadas para este caso; no acredita rechazo de otros roles ni llamadas externas, revisión de participantes o concurrencia PostgreSQL.

## 16 de octubre de 2026 — Retiro de confidencialidad verificado

Propósito: verificar retiro explícito de protección para el caso simulado. Evidencia 25-confidencialidad-retirada-200.png ejecutada por la autora e inspeccionada: HTTP 200, Ausencia simulada en EN_REVISION, is_confidential=false y ai_status=OMITIDA, con responsable y clasificación vigente conservados. Sin token/Curl visibles. Cambio: seguimiento documental. Resultado: retiro de confidencialidad y ausencia de reactivación automática de cola IA acreditados en el detalle. La captura no acredita motivo auditado, permisos de todos los roles, revisión de participantes ni concurrencia real. Sin cambios de código ni pruebas automáticas nuevas. Pendiente: prueba manual de declaración/revisión de participante gestor.

## 16 de octubre de 2026 — Acuse de participante verificado

Evidencia 26-participante-declarado-201.png ejecutada por la autora e inspeccionada: HTTP 201, received=true y can_view=true para el caso simulado. Solo acredita acuse, no identidad/estado de relación ni confidencialidad automática: pendientes de GET participantes y detalle. Sin token/Curl visibles. Propósito: verificar alta; cambio: seguimiento documental. Sin código ni pruebas automáticas nuevas. Resultado parcial, revisión independiente pendiente.

## 16 de octubre de 2026 — Relación declarada verificada

Propósito: verificar relación creada. Evidencia 27-participante-declarado-detalle-200.png aportada por la autora e inspeccionada: HTTP 200, una relación con user_id, review_status=DECLARADO y motivo original; reviewed_by, reviewed_at y review_reason nulos. La respuesta no incluye nombre/rol, por lo que no se acredita visualmente que el ID pertenezca al supervisor elegido. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni pruebas automáticas nuevas. Resultado: declaración persistida verificada; revisión y protección automática tras alta pendientes de evidencia específica.

## 16 de octubre de 2026 — Participante confirmado verificado

Propósito: comprobar revisión de relación. Evidencia 28-participante-confirmado-200.png aportada por la autora e inspeccionada: HTTP 200, misma relación en CONFIRMADO, motivo original conservado y reviewed_by/reviewed_at/review_reason presentes; revisor distinto del participante. reviewed_at usa UTC y muestra 17 de octubre, consistente con ejecución nocturna local del 16 de octubre. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni pruebas automáticas nuevas. Resultado: confirmación registrada verificada; no acredita por sí sola rol del participante ni rechazo al retirar confidencialidad. Pendientes: comprobar bloqueo protector y descarte auditado; concurrencia PostgreSQL.

## 16 de octubre de 2026 — Bloqueo protector verificado

Propósito: comprobar rechazo al retirar confidencialidad con gestor involucrado. Evidencia 29-bloqueo-confidencialidad-409.png aportada por la autora e inspeccionada: HTTP 409 y mensaje No se puede retirar confidencialidad con gestor involucrado. Resultado esperado de prueba negativa; no es fallo de la prueba. La captura no muestra el estado persistido posterior ni todos los permisos entre roles. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni pruebas automáticas nuevas. Fecha registrada en hora local; cabecera HTTP usa UTC del 17 de octubre. Pendientes: descarte y conservación de declaración/revisión en historial; concurrencia PostgreSQL.

## 16 de octubre de 2026 — Descarte de participante verificado

Propósito: comprobar corrección de relación con motivo. Evidencia 30-participante-descartado-200.png aportada por la autora e inspeccionada: HTTP 200, relación DESCARTADO, declaración original conservada, revisor/fecha y nuevo motivo presentes. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni nuevas pruebas automáticas. Resultado: descarte persistido acreditado. La respuesta de participantes no muestra confidencialidad ni eventos anteriores; ambos deben consultarse para acreditarlos manualmente. Cabeceras/fecha de revisión UTC del 17 de octubre, registro local del 16 de octubre. Pendientes: comprobar confidencialidad después del descarte e historial de revisiones; concurrencia real PostgreSQL.

## 16 de octubre de 2026 — Protección conservada tras descarte

Propósito: verificar que descartar una relación no retira protección automáticamente. Evidencia 31-confidencialidad-tras-descarte-200.png aportada por la autora e inspeccionada: HTTP 200, mismo caso Ausencia simulada en EN_REVISION, is_confidential=true y ai_status=OMITIDA. Complementa evidencia 30 con relación DESCARTADO. Resultado: confidencialidad conservada acreditada para este caso, no se infieren permisos de otros roles ni auditoría histórica completa. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni nuevas pruebas automáticas. Registro en fecha local; cabecera HTTP UTC del 17 de octubre. Pendientes: retiro explícito después del descarte e historial de revisiones; concurrencia PostgreSQL.

## 16 de octubre de 2026 — Retiro posterior al descarte verificado

Propósito: comprobar retiro explícito tras revisión de relación. Evidencia 32-retiro-tras-descarte-200.png aportada por la autora e inspeccionada: HTTP 200, mismo caso Ausencia simulada, EN_REVISION, is_confidential=false y ai_status=OMITIDA. Complementa evidencias 30/31: descarte no retira protección por sí mismo; el retiro posterior reportado por la autora queda reflejado en detalle. La captura no incluye el motivo auditado ni historial de revisiones. Sin token/Curl visibles. Cambio: seguimiento documental, sin código ni pruebas automáticas nuevas. Resultado: comprobación básica de protección/revisión/retiro completada para este caso; no acredita todos los permisos entre roles ni concurrencia PostgreSQL. Pendiente auditoría histórica de las revisiones.

## 16 de octubre de 2026 — Historial de protección completo revisado

Propósito: verificar auditoría de revisión y protección. Archivo 33-historial-proteccion.json descargado por la autora e inspeccionado, JSON válido con 15 eventos, total=15, page=1 y page_size=20; no faltan páginas para este total. Comprobación estructurada: una alta participant_add y dos participant_review; secuencia DECLARADO → CONFIRMADO → DESCARTADO, con declaración original, revisores, fechas y motivos conservados. El alta activa confidencialidad (before=false/after=true); el descarte mantiene true y la última operación explícita la retira (true→false) con motivo. También conserva reapertura con resolución y fechas del ciclo anterior. Una solicitud repetida de retiro sin cambio produjo evento adicional y se conserva sin alterarlo. No hay contraseñas ni tokens en el archivo revisado; contiene textos ficticios e IDs de prueba. Cambio: documentación, sin código ni nueva ejecución de la suite. Resultado: auditoría del recorrido manual de este caso verificada; no acredita concurrencia real, matriz completa de roles, provisión de RH adicional ni integraciones pendientes. Fechas UTC del 17 de octubre corresponden a la noche local del 16.

## 16 de octubre de 2026 — Pruebas del CLI independiente

Se preparó actualización del CLI con provision-independent-admin, motivo obligatorio, contraseña privada, cuenta nueva y auditoría atómica. Validación en copia aislada: 24 passed in 4.39s (siete nuevas de CLI y regresiones de esquema/seed); pip check sin conflictos. Se probaron rechazo de correo existente, primer bootstrap exclusivo, motivo, departamento inactivo, rollback de alta/credencial/departamento, contraseña no mostrada y conservación de exclusión/asignación del caso. La suite completa y una selección que incluía pruebas HTTP fueron interrumpidas al bloquearse sin resultado final; no se dan por aprobadas. No se ejecutó CLI contra Docker ni PostgreSQL; bloqueo concurrente y validación manual pendientes. La carpeta del proyecto es de solo lectura en esta sesión: paquete preparado, no aplicado al repositorio y sin commit. El script de aplicación verifica hashes previos y conserva respaldos. No se modifica .env ni datos reales. La cuenta nueva no garantiza por sí sola independencia humana; el operador debe designar a otra persona autorizada, limitación documentada.
Comando aprobado desde copia backend: python -m pytest -q tests/test_manage_users.py tests/test_incident_schema.py tests/test_seed_demo.py.

## 16 de octubre de 2026 — Recorrido manual de RH independiente

La autora reportó aplicación del paquete, reconstrucción Docker y creación de RH Independiente Demo. Evidencias 34–37 inspeccionadas: 34 acredita sesión HTTP 200 ADMIN_RH de la cuenta nueva; 35 acuse HTTP 201; 36 detalle HTTP 200 del nuevo caso confidencial con el administrador original como afectado, PENDIENTE, IA OMITIDA y sin responsable; 37 muestra 404 Incidencia no encontrada, tras cambio de sesión reportado por la autora. El recorte 37 no muestra ID consultado ni identidad del solicitante: por sí solo no distingue exclusión de un ID inexistente; se documenta en conjunto con el recorrido reportado y las pruebas automáticas previas, sin exagerar la evidencia. No se observaron contraseñas ni tokens. El caso original y la asignación no se alteraron por provisionar la cuenta. Las cuentas distintas no garantizan independencia humana: el operador debe designar otra persona autorizada. No se ejecutaron pruebas automáticas nuevas en esta revisión; siguen vigentes las 24 pruebas seleccionadas de CLI/esquema/seed aprobadas en copia y la suite HTTP completa sin resultado final de esta sesión. Concurrencia real PostgreSQL, auditoría del alta en motor real y matriz completa de permisos siguen pendientes.
Registro detallado: REVISION_RH_INDEPENDIENTE.md. No equivale a RF-7 completo ni certificación de todos los permisos.

## 16 de octubre de 2026 — Pruebas de administración

API 0.8.0 preparada en copia aislada, esquema 0003 sin migración. GET /users/options y /users; PUT /users/{id} auditado, con rol/departamento/activación, revocación y protección de asignaciones. Bloqueo advisory compartido/exclusivo coordina mutaciones administrativas e incidencias. 35 pruebas seleccionadas aprobadas en 6.50s; primera ejecución 1 fallida/32 aprobadas por caché del fixture, corregida comprobando datos persistidos y refrescando la entidad. No se ejecutó suite HTTP completa ni concurrencia PostgreSQL. El paquete no está aplicado; no hay commit/push. No se modificó .env ni datos reales. Validación manual, frontend y administración de departamentos pendientes. Guía y límites en ADMIN_USUARIOS.md.
Comando desde copia backend: python -m pytest -q tests/test_user_administration.py tests/test_manage_users.py tests/test_incident_schema.py tests/test_seed_demo.py. Cobertura: desactivación y revocación persistida, último RH local, promoción protectora, traslado y departamento histórico, caso finalizado, restricción al actor involucrado, rollback completo, validación/listados y edición de nombre sin revocar, recorrido de servicios de caso y refresco de privilegios antiguos. Las lecturas de ruta se invocan directamente en estas pruebas; no acreditan todo el middleware HTTP.

## 16 de octubre de 2026 — Suite completa y recorrido administrativo

API 0.8.0 aplicada y reconstruida según reporte de la autora; evidencia 38 inspeccionada confirma suite completa ejecutada por ella: 77 passed, 3 skipped, 1 warning in 16.49s. Las tres omitidas son las integraciones PostgreSQL optativas y no se declaran aprobadas; advertencia conocida de TestClient/httpx. La ejecución completa posterior sustituye el pendiente histórico de suite HTTP de este avance. No prueba concurrencia PostgreSQL. Evidencias 39–46 inspeccionadas: listado 200, desactivación y estado inactivo, reactivación y estado activo, rechazo de sesión anterior y nueva sesión RH permitida. La autora reporta prueba en dos pestañas con modificación administrativa desde la cuenta original; los recortes 401 no muestran identidad/token/solicitud previa, por lo que se documentan como respuestas consistentes con la secuencia reportada, sin afirmar causalidad exclusiva frente a expiración. No se observaron contraseñas ni tokens en las capturas revisadas. No se cambiaron .env ni datos por el asistente durante esta consolidación. No hay prueba manual nueva de cambio de rol, traslado con reasignación ni concurrencia; esas comprobaciones no se infieren de las capturas. RF-7 permanece parcial por frontend y administración de departamentos pendientes.
Comando mostrado en evidencia 38: backend/.venv/Scripts/python.exe -m pytest backend/tests -vv -o faulthandler_timeout=30. Prueba aislada anterior: test_health_contract, 1 passed, 1 warning in 3.88s. Un primer intento completo fue interrumpido con KeyboardInterrupt y no se contó como aprobado. La ejecución completa posterior sí terminó. Detalles y límites en REVISION_ADMIN_USUARIOS.md.

## 17 de octubre de 2026 — Traslado y cambio de rol verificados

Propósito: consolidar pruebas manuales de revisión de acceso/asignación. Cambios: REVISION_TRASLADO_ROL.md, enlaces 47–57 y seguimiento documental. Validación: inspección visual y JSON, 51 con 4/4 eventos y 57 con 5/5, motivos y estados anteriores/nuevos conservados. Traslado reasigna a RH y mantiene departamento histórico; promoción activa confidencialidad e IA omitida; restauración a EMPLEADO conserva protección. Usuario queda activo en departamento destino y caso EN_REVISION protegido. Sin código ni nueva ejecución automática: resultado previo 77 aprobadas/3 omitidas/1 advertencia sigue siendo evidencia distinta. No se modificaron .env ni datos del motor por el asistente. Pendientes: concurrencia real y tres integraciones PostgreSQL, matriz de permisos completa, frontend y departamentos. Registro completo y límites en REVISION_TRASLADO_ROL.md.

## 17 de octubre de 2026 — Primera interfaz React

Propósito: usar la API desde un panel de lectura. Cambios: frontend React/Vite con login, listado/filtros/paginación, detalle/historial, cliente con sesión en memoria, estilos adaptables y workflow frontend. Dependencias fijadas/lockfile y manual FRONTEND.md. Validación final: 9 pruebas frontend aprobadas en 17.97s, build correcto (17 módulos/442ms), HTTP frontend 200 y proxy /api/health ok. Pruebas usan jsdom/fetch simulado; no equivalen a login real ni auditoría visual. Instalación con certificados del sistema tras error TLS, sin desactivar validación; npm reporta cero vulnerabilidades en la instalación. No se modificó API, esquema, .env ni datos del motor. Backend no repetido por este cambio. Resultado: UI parcial de lectura ejecutable. Pendientes: verificación manual/visual y evidencia 58, formularios de registro/gestión/administración, deep links, concurrencia PostgreSQL e integraciones. Límites en FRONTEND.md.

## 17 de octubre de 2026 — Panel React, listado real verificado

Propósito: verificar primera lectura con API real. Evidencia 58-panel-react-incidencias.png aportada por la autora e inspeccionada visualmente: panel con Administrador RH, 2 casos en consulta (Prueba de traslado de departamento y Ausencia simulada), ambos En revisión, prioridad Media, acceso Restringido/Según rol respectivamente y página 1 de 1. Formularios de filtro y sesión visibles; sin contraseñas/tokens. Esto acredita listado renderizado con datos simulados y acceso reportado, no prueba por sí solo filtrado, detalle, logout, permisos de otros roles ni accesibilidad móvil. Cambio: seguimiento documental; sin código ni nuevas pruebas automáticas. Pendiente detalle/historial real y formularios de gestión. Resultados previos de 9 pruebas UI simuladas y build se conservan como evidencia distinta.

## 17 de octubre de 2026 — Detalle React verificado

Propósito: comprobar lectura de expediente e historial en interfaz. Evidencia 59-panel-react-detalle.png aportada por la autora e inspeccionada: caso Prueba de traslado de departamento, EN_REVISION, descripción ficticia, prioridad Media, acceso restringido a RH independiente y validación vigente. Se muestra IA omitida, responsable en formato UUID y ausencia de resolución/fechas finales. Fragmento de historial muestra CAMBIO CONFIDENCIALIDAD y ASIGNADO con motivos de promoción/traslado. No muestra todo el historial ni su paginación; no se declaran verificados en su totalidad. Sin token/contraseña visibles. Cambio: seguimiento documental, sin código ni nuevas pruebas automáticas. Resultado: detalle e inicio de historial renderizados verificados; pendientes filtro/logout/móvil manuales y formularios de gestión. No se acredita matriz de acceso completa.

## 17 de octubre de 2026 — Filtro React verificado

Propósito: comprobar búsqueda y total autorizado en UI. Evidencia 60-panel-react-filtro.png aportada por la autora e inspeccionada: búsqueda Ausencia simulada, una fila con ese título y contador 1, página 1 de 1. Estado En revisión, prioridad Media y acceso Según rol. Sin token/contraseña visibles. Resultado: búsqueda por título y total coincidente verificados para este caso; no acredita todos los filtros ni controles entre roles. Cambio: seguimiento documental, sin código ni nuevas pruebas automáticas. Pendientes logout manual, vista móvil y formularios de gestión.

## 17 de octubre de 2026 — Cierre de sesión React verificado

Propósito: comprobar retirada de información al salir. Evidencia 61-panel-react-sesion-cerrada.png aportada por la autora e inspeccionada: formulario Inicia sesión, aviso Cerraste tu sesión, campos correo/contraseña vacíos y ausencia de listado/detalle/identidad de cuenta. La autora reporta pulsar Cerrar sesión. Esto acredita pantalla posterior y retirada visible de datos; la imagen no demuestra por sí sola revocación persistida en servidor ni ausencia de tokens en almacenamiento (cubierta por implementación y pruebas simuladas previas). Sin credenciales visibles. Cambio: documentación y consolidación de evidencias 58–61; sin código ni nueva ejecución automática. Resultado: recorrido manual inicial de listado, detalle, búsqueda y logout acreditado con estos límites. Pendientes: móvil, todos los roles/filtros y formularios de gestión; RF-8 parcial.

## 17 de octubre de 2026 — Registro de incidencias React 0.2.0

Propósito: registrar casos desde la interfaz con controles de ámbito y acuse seguro. Cambios: pages/NewIncident.jsx, integración de menú, estilos, texto genérico de validación, versión frontend/lock 0.2.0 y seis pruebas de formulario. Validación final: 15 pruebas aprobadas en 3 archivos, 17.63s; build correcto con 18 módulos/379ms. API simulada, sin crear casos ni modificar usuarios del motor real desde el asistente. Se conserva backend 0.8.0 y esquema 0003, sin .env nuevo ni dependencias nuevas. Resultado: alta UI implementada, comprobación manual agrupada pendiente. Acuse no ofrece expediente sin permiso; previene reintento automático ambiguo, sin prometer idempotencia de servidor. Pendientes: prueba real/evidencia 62, formularios de gestión y administración, móvil/otros roles y restantes integraciones. No se repitió suite backend por este avance de frontend.

## 17 de octubre de 2026 — Acuse de registro React verificado

Propósito: comprobar alta desde interfaz real. Evidencia 62-registro-react-acuse.png aportada por la autora e inspeccionada: pantalla Recibimos tu reporte, ID de referencia, aviso de acceso permitido y botones Consultar expediente/Volver al listado. No muestra contraseña/token ni contenido sensible. La autora reporta envío del formulario; imagen acredita acuse renderizado, no título/afectado, código HTTP ni apertura del detalle, que no se infieren solo por el recorte. Resultado: primera comprobación manual de registro/acuse completada; no exige repetir capturas por campo. Cambio: documentación y evidencia, sin código ni nueva ejecución automática. Quedan pendientes prueba manual de acuse restringido/entorno/otros roles y formularios de gestión. Las 15 pruebas frontend previas son evidencia separada. El servidor React se reinició después de conexión rechazada y se comprobó HTTP 200 y proxy health ok, sin cambios de código.

## 17 de octubre de 2026 — Gestión de casos React 0.3.0

Propósito: gestionar clasificación, responsable y ciclo desde panel. Cambios: components/CaseManagement.jsx y pruebas, integración con detalle/recarga de historial, edición de contenido, estilos, mensaje 409 y versión/lock 0.3.0. Validación final: 26 pruebas aprobadas en 4 archivos, 15.80s, incluyendo once nuevas y un ciclo UI completo con API simulada; build correcto 19 módulos/262ms. Primer intento falló por sintaxis JSX; corregido y suite final completa aprobada. Sin cambios al backend 0.8.0, esquema 0003, .env ni datos del motor; no se repitió suite backend ni se ejecutó ciclo real contra PostgreSQL. Resultado: gestión UI parcial implementada con roles, requisitos, respuesta incierta y refresco posterior. Pendiente una comprobación manual agrupada/evidencia 63, interfaces de participantes/confidencialidad/admin, móvil/otros roles e integraciones. Detalles en FRONTEND.md.

## 17 de octubre de 2026 — Cierre de caso desde React verificado

Propósito: acreditar resultado del recorrido de gestión UI. Captura aportada por la autora, inspeccionada y copiada sin edición como 63-gestion-react-caso-cerrado.png. Caso Retardo, mismo ID del acuse 62, muestra aviso Caso cerrado y estado Cerrada, descripción ficticia, prioridad Media, validación vigente, responsable RH y resolución simulada con fechas de resolución/cierre presentes. Sesión visible Administrador RH. Resultado final compatible con el recorrido guiado por la autora; no se infiere de una sola captura la revisión exhaustiva de cada transición ni todos los roles. Asistencia IA pendiente refleja estado existente, no ejecución de IA ni bloqueo del cierre humano; integración/worker siguen pendientes. Sin token/contraseña visibles. Cambio: evidencia/documentación, sin código, nuevas pruebas automáticas ni alteración de datos del motor desde el asistente. Pendientes: prueba real de reapertura/edición en esta UI, móvil/otros roles y pantallas de protección/admin; RF-3/RF-4/RF-8 parciales.

## 17 de octubre de 2026 — React 0.4.0: usuarios y protección

npm test: 40/40 aprobadas, 6 archivos, 23.66s. npm run build: correcto, 21 módulos, 358ms. Nuevas pruebas: acceso administrativo, alta/limpieza de contraseña, modificación auditada, revocación propia sin relectura, conflicto sin actualización optimista, paginación; confidencialidad con motivo, acuse sin acceso, revisión/descarte, prohibición de autorrevisión, estados finalizados y respuesta incierta. Integraciones App comprueban navegación a Usuarios y retiro de sesión/directorio, y desaparición de expediente/historial al perder acceso por participante.

Primer pase observado: 37 aprobadas y 1 fallida por selector de texto ambiguo (párrafo y textarea); corregido selector y fixture de participantes, añadidas dos integraciones y repetida suite completa con éxito. Las pruebas usan API simulada. No se ejecutaron cambios reales de cuentas/protección ni PostgreSQL/concurrencia para esta entrega. Backend sin cambios, no repetido. Evidencia 64 y recorrido real agrupado pendientes; instrucciones en FRONTEND.md.

## 17 de octubre de 2026 — Evidencia manual 64: administración React

Capturas aportadas por la autora: 64-admin-react-usuarios.png y continuación 64b-admin-react-usuarios-continuacion.png. Revisión visual: sección Usuarios con listado administrativo, nombres/correos de demostración, rol, departamento, activación y botones de edición. Aviso visible: «Cambios guardados. Sin cambio de permisos. Casos ajustados: 0». Continuación muestra Supervisor RH Demo Juan y paginación «Página 1 de 1». Sin contraseñas/tokens visibles. Capturas conservadas sin edición.

Se acredita listado renderizado y confirmación de guardado desde React para el recorrido reportado. No hay comparación antes/después del nombre ni cuerpo de petición, y las imágenes no prueban por sí solas auditoría persistida, revocación, alta, otros roles, protección ni concurrencia PostgreSQL. No se repitieron pruebas de código para esta actualización documental. RF-7/RF-8 siguen parciales; siguiente comprobación agrupada: confidencialidad/participantes sobre caso ficticio abierto con RH independiente.

## 17 de octubre de 2026 — Evidencias 65–66: protección desde React

Capturas aportadas por la autora, conservadas sin edición. 65-react-confidencialidad.png muestra Ausencia simulada EN_REVISION, aviso «Protección actualizada. Se recargaron expediente, relaciones e historial», acceso restringido a RH independiente, clasificación vigente e IA omitida. Se acredita estado confidencial renderizado tras el recorrido reportado; la imagen no muestra motivo enviado ni historial completo, y no prueba que el caso antes fuera público.

66-react-participante-confirmado.png muestra Empleado Operaciones Uno Demo con estado CONFIRMADO, declaración «testigo» y última revisión «Testigo Visual». La declaración se conserva separada del motivo de revisión y los campos del siguiente envío están vacíos. El recorte no incluye título/ID, revisor ni fecha: no permite vincular por sí solo la relación con el expediente de la evidencia 65 ni probar autoría independiente.

Sin contraseñas ni tokens visibles. Primera comprobación manual de confidencialidad y relación confirmada en React acreditada dentro de esos límites; no demuestra toda la matriz de permisos, exclusión del propio gestor, descarte, auditoría persistida ni concurrencia. No se repitieron tests para este registro documental; se mantienen separados los 40 tests UI simulados previos. RF-4/RF-8 parciales. No se requieren capturas adicionales de los mismos campos.
