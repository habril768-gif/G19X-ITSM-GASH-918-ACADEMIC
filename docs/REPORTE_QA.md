# Reporte de calidad y evidencias

## RNF-2: cumplido en QA local — 30 de octubre de 2026

[Primera formal aprobada220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json):10 clientes,100 casos iniciales,30+300s,API de 3 procesos,35.216 solicitudes sin errores. P95 listado123,81/detalle113,27/creación194,04/actualización167,77ms, todos<200 ms; auditoría/colas/logout/parada correctos. Acredita este alcance HTTP Docker local y hardware declarado, no rendimiento universal ni proveedores externos. Diez fallos históricos se conservan. [Perfil opcional 221](evidencias/221-perfil-compose-rnf2-reproducible.json) y [protocolo](PRUEBA_RENDIMIENTO.md) permiten reproducir configuración/medición. Los demás pendientes de entrega siguen vigentes.


## Cómo consultar este reporte

Este archivo conserva resultados cronológicos: cada entrada acredita únicamente lo que se ejecutó o inspeccionó en ese momento. Para el estado vigente consulta [MVP](MVP.md), [trazabilidad](TRAZABILIDAD.md) y [backlog](BACKLOG.md). Los pendientes de una entrada antigua pueden tener evidencia posterior; no se deben leer como la lista actual de funciones ausentes.



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

## 17 de octubre de 2026 — React 0.5.0: contraseña personal

Validación final: npm.cmd test -- --maxWorkers=2, 48/48 aprobadas en 7 archivos, 67.31s. npm.cmd run build correcto: 22 módulos, 749ms. Cinco pruebas nuevas del formulario: confirmación distinta sin envío, contrato exacto/limpieza, rechazo 400 sin éxito, resultado incierto sin reintento, doble envío/cancelación bloqueados. Tres integraciones App comprueban acceso por ADMIN_RH/SUPERVISOR/EMPLEADO y regreso al login con campos vacíos y sin casos tras éxito.

Primer intento con paralelismo predeterminado: 46 aprobadas/2 timeout de 5000ms en pruebas existentes de registro y login, 97.98s; las ocho nuevas pasaron. Repetición completa con dos workers aprobada sin ampliar timeout. Se fija maxWorkers=2 en vite.config.js para limitar carga en ejecuciones posteriores. No se atribuye el fallo a un defecto de producto sin evidencia.

Todas las pruebas UI usan API simulada: no certifican cambio real de hash, revocación de otras sesiones ni acceso con nueva contraseña. Backend no modificado ni repetido. Evidencia 67 y recorrido real pendientes, con instrucciones en FRONTEND.md. No se solicita captura del formulario con credenciales.

## 17 de octubre de 2026 — Evidencia 67: contraseña desde React

Se inspeccionó directamente docs/evidencias/67-react-password-actualizada.png, guardada por la autora. Muestra login con correo/contraseña vacíos y aviso «Contraseña actualizada. Se revocaron tus sesiones. Inicia sesión con la nueva contraseña». Sin credenciales ni token visibles; conservada sin edición. Acredita resultado visible y retiro de la vista autenticada tras el flujo guiado, no revocación de todas las sesiones por sí sola.

La autora informó que volvió a iniciar sesión después del cambio; se registra como comprobación manual reportada de acceso con la nueva contraseña, sin inspeccionar ni guardar la credencial. No se comprobó rechazo de contraseña anterior ni de otras sesiones abiertas. RF-1/RF-8 siguen parciales. No se repitieron pruebas de código para este registro; la suite previa de 48 pruebas UI simuladas se mantiene separada.

## 17 de octubre de 2026 — API 0.9.0 / React 0.6.0: departamentos

Backend final: python -m pytest tests -q -o faulthandler_timeout=30, 90 aprobadas, 3 integraciones PostgreSQL omitidas y 1 advertencia previa Starlette/httpx, 23.96s. Trece pruebas HTTP/servicio nuevas con SQLite/FK verifican alta/renombrado/baja/reactivación/auditoría, permisos RH/empleado/supervisor/anónimo, duplicados/validación/paginación, rechazo con usuarios activos y casos abiertos PERSONA/ENTORNO, rollback por fallo de auditoría, preservación de casos finalizados/referencias, exclusión de inactivos en opciones y revalidación del actor después del bloqueo. Se ampliaron pruebas existentes de SQL offline y migración PostgreSQL aislada: esta última sigue omitida.

Frontend: npm.cmd test, 55/55 aprobadas en 8 archivos, 77.33s. Seis pruebas de Departments y una integración App nuevas: alta/edición y payload, conflicto sin éxito simulado, respuesta incierta sin reenvío, catálogo/historial paginados, prohibición a empleado y navegación sin mezclar vistas. Build: 23 módulos, 571ms. UI con API simulada; no prueba de navegador/API real por este avance.

Incidencias del entorno: primer pytest nuevo no terminó y se interrumpió; diagnóstico con faulthandler mostró bloqueo al crear socketpair del event loop de Windows durante apertura de TestClient. Se interrumpió también ese intento y se habilitó red de pruebas para la conexión interna, sin cambiar código del producto para ocultar el bloqueo. Suite completa posterior: 88 aprobadas/3 omitidas/1 advertencia en 22.43s; se añadieron dos pruebas adicionales y la repetición final dio 90 aprobadas. No se cuentan intentos interrumpidos como aprobados.

Docker compose ps devolvió permission denied al pipe dockerDesktopLinuxEngine. No se ejecutaron rebuild, migración real ni alembic check contra la base del proyecto. No se declara validada 0004 en PostgreSQL ni concurrencia por las pruebas SQLite. Preparados instrucciones de aplicación y recorrido real agrupado/evidencia 68 en DEPARTAMENTOS.md. RF-7/RF-8 parciales.

## 17 de octubre de 2026 — Evidencia 68: historial de departamentos desde React

Se inspeccionó directamente 68-react-departamentos-historial.png, guardada por la autora y conservada sin edición. Historial de «DEMO - PRUEBA 1» con cuatro eventos visibles: CREADO (nombre DEMO, activo), ACTUALIZADO por renombrado DEMO → DEMO - PRUEBA 1, ACTUALIZADO por desactivación (Inactivo), y ACTUALIZADO por reactivación (Activo). Cada entrada muestra fecha/hora y motivo académico; página 1 sin navegación adicional disponible. Sin contraseñas, tokens ni datos personales visibles.

Se acredita visualmente el recorrido básico de alta/renombrado/baja/reactivación y consulta de historial desde React para el departamento simulado. Sustituye el pendiente total de prueba manual de esta función. El recorte no muestra actor/UUID, terminal, versión Alembic ni alembic check: no acredita por sí solo revisión 0004 sin diferencias, autorización entre roles, bloqueo por usuarios/casos activos, atomicidad bajo fallos ni concurrencia PostgreSQL. La ejecución funcional observada es compatible con aplicación del backend y nueva auditoría; no se registra como verificación directa de migración.

Actualización documental, sin repetir pruebas de código. Se conservan separados resultados previos: 90 backend aprobadas/3 PostgreSQL omitidas/1 advertencia y 55 UI simuladas/build correcto. RF-7/RF-8 parciales; no se requieren nuevas capturas de los mismos campos.

## 17 de octubre de 2026 — Integraciones PostgreSQL ejecutadas sin omisiones

Ejecutor backend/scripts/test_postgres_isolated.py sobre PostgreSQL 18.6 local temporal: upgrade head, repetición, alembic check sin diferencias y suite completa 103 aprobadas/0 fallos/0 errores/0 omitidas/1 advertencia previa, 21.70s. Resumen leído desde JUnit; servidor y carpeta de la ejecución final retirados. No se utilizó la base de desarrollo.

Se ejecutaron las tres integraciones antes omitidas y dos nuevas: exclusión de bloqueo administrativo con conexiones independientes/lock_timeout y rollback real de departamento/auditoría bajo savepoint. Ocho pruebas nuevas del ejecutor/guardas verifican destinos dedicados y limpieza/conservación al fallar. La prueba de identidad reservada usa ahora correos distintos y comprueba uq_users_entra, evitando confundir rechazo por correo con identidad. No reactiva Entra ID.

Ejecución anterior del nuevo ejecutor completó etapas con salida 0, pero no se consignó conteo no observado; se añadió salida explícita/JUnit y se repitió para obtener el resultado anterior. Primer intento con captura de pipes se interrumpió; restos propios ignorados conservados tras rechazo automático de borrado. Servidor inicial detenido/puerto cerrado comprobados; detalle en PRUEBAS_POSTGRESQL.md.

Además se consultó la API pública de GitHub: run 39090144556, commit c8ad75c, job postgres-integration exitoso en PostgreSQL 17 con upgrades/check/pytest exitosos. Acredita CI de ese commit, no de estas pruebas nuevas. Docker sigue inaccesible desde el entorno; binarios locales proporcionaron aislamiento alternativo sin cambiar el stack. Evidencia 69 JSON y guía PRUEBAS_POSTGRESQL.md.

La suite completa aún contiene fixtures SQLite: cinco pruebas son específicamente PostgreSQL. No se certifican todas las carreras de negocio ni la matriz completa de roles/UI. Frontend sin cambios, no repetido. Sin nuevas capturas manuales requeridas.

## 17 de octubre de 2026 — API 0.10.0 / React 0.7.0: IA revisada

Backend final: ejecutor PostgreSQL 18.6 aislado, 129 aprobadas/0 fallos/0 errores/0 omitidas, 23.97s. Upgrade 0005 repetido y check sin diferencias; servidor/carpeta final retirados. Seis integraciones PostgreSQL, una nueva del trabajo IA/descarte de respuesta por privacidad con proveedor simulado; resto conserva fixtures originales. No son 129 llamadas ni integraciones reales del modelo.

Pruebas nuevas cubren confirmaciones/identificadores/permisos, entrada revisada sin copiar original, durabilidad sin Redis, idempotencia, sugerencia sin decisión oficial, abstención, cancelación antes de envío/cambios durante petición, tres intentos, esquema/catálogo inválidos, lease vencido y propietario antiguo, nueva revisión tras editar y rollback ante fallo de auditoría de solicitud/resultado. Proveedor: configuración Responses/store=false/reintentos 0/salida acotada con constructor/invocación simulados; Redis solo ID. Evaluador prueba denominadores, fallos y Alta→Baja, sin medir calidad real.

Primer pase específico: 18 aprobadas/1 fallo por orden de trabajos creados en un mismo segundo en SQLite. Corregidos timestamp explícito y orden por revisión; siguiente pase 23 aprobadas/9.08s. Con auditoría e integración nueva, suite 129/45.12s; tras acotar salida y completar reporte de falsos negativos, repetición final 129/23.97s.

Frontend completo: 64 aprobadas/9 archivos/66.43s, incluida integración donde la sugerencia no rellena clasificación oficial. Tras ajuste de mensajes, ocho específicas/9.96s y build 24 módulos/658ms correctos. Primera suite de 62 también pasó, sin presentarse como conteo final.

Dependencias y transitivas fijadas; pip check correcto. Compose parseado con PyYAML: clave solo worker/perfil ai. Pip inicial encontró PermissionError de conexión; instalación con wheels oficiales PyPI descargados HTTPS y hashes SHA256 verificados, sin desactivar TLS. Importación detectó escritura de SSLKEYLOGFILE heredado fuera del workspace; validación sin ese log de depuración en proceso hijo solamente, sin modificar configuración persistente/certificados. No se leyó .env real ni clave API.

Sin OpenAI/Redis reales, evaluación independiente 50+5, despliegue/check de desarrollo ni nueva UI manual acreditados. Docker continúa restringido. RF-3 no aceptado por tests de infraestructura; manual operativa. Guía IA.md y evidencia 70.

Verificación adicional final del adaptador: clase real ChatOpenAI/OpenAI SDK con MockTransport HTTP, serializa Responses JSON Schema/store=false/max_output_tokens=1500 y parsea resultado válido; sin red ni credencial real. Pase específico proveedor: 3/3, 5.73s; ampliado chequeo de límite y repetida suite completa nativa final: 130/130 aprobadas, 0 omitidas, 23.65s, migración/check correctos y recursos de esa ejecución retirados. Este es el resultado backend vigente, posterior a los pases de 129 anteriores.

CLI del worker comprobado con AI_ENABLED=false y --once: salida 0, mensaje de IA desactivada y ninguna consulta de cola/proveedor; confirma arranque seguro sin credencial.
## 17 de octubre de 2026 — Primera prueba manual de IA integrada

Inspeccionadas directamente las evidencias 71–73, conservadas sin edición y sin claves, contraseñas ni tokens visibles. La autora informó configuración local de la clave, saldo y ejecución de Compose; la captura de terminal aportada mostró ai-worker en ejecución y API/PostgreSQL/Redis saludables. No se leyó el .env ni se consultó la cuenta del proveedor.

71 muestra trabajo COMPLETADA, intento 1/3, categoría sugerida Riesgos y prioridad Alta, pendiente de validación humana. 72 muestra «Prueba IA — piso mojado» en PENDIENTE, ámbito Entorno, prioridad oficial por definir y clasificación que requiere validación humana. 73 muestra el mismo título e ID, CERRADA, prioridad Alta, validación vigente, responsable, resolución simulada y fechas de resolución/cierre. El recorrido guiado y reportado acredita una primera respuesta de la integración externa y cierre posterior por decisión humana; las capturas no muestran modelo efectivo, consumo, identificador del proveedor, historial completo ni recorrido intermedio EN_REVISION. La captura 71 recorta el ID: su asociación al caso procede del recorrido compartido por la autora.

Configuración indicada para esta prueba: gpt-4.1-mini; acceso y valor efectivo no inspeccionados directamente. Redis saludable y resultado completado no demuestran el transporte exacto de aviso: el worker también consulta PostgreSQL. No se certifican con este caso todas las condiciones de privacidad, concurrencia, reintentos ni calidad estadística. La actualización fue reportada por la autora; versión Alembic/check de la base de desarrollo no inspeccionados en esta revisión.

RF-3/RF-8 permanecen parciales. Sustituye el pendiente total de primera prueba manual con proveedor y UI reales. Siguen pendientes referencias independientes de 50 casos y 5 de abstención, ejecución y revisión de métricas. Cambio documental: no se repitieron suites ni llamadas externas; se mantienen separados los 130 tests backend y 64 UI previos.
## 17 de octubre de 2026 — Validación offline del borrador 50+5

Conjunto candidato en evaluacion_ia: 50 referencias, 10 por categoría, prioridades 15/20/15 y cinco abstenciones. Comprobados 55 IDs y textos únicos, igualdad de entradas/referencias, entradas sin etiquetas/justificación, ámbito y catálogo coherentes, justificaciones no vacías, exclusión del ejemplo manual piso mojado y AIInput 55/55. Evaluador offline ejecutado únicamente con 55 marcadores NOT_EXECUTED_STRUCTURE_CHECK en memoria para verificar compatibilidad: cero aciertos y metas falsas, sin guardar aquello como predicciones ni medir calidad. Manifiesto SHA256 generado. Sin consulta al proveedor ni tests productivos adicionales. Etiquetas redactadas por el asistente; no revisadas por humanos ni congeladas. No certifica independencia, calidad o aceptación RF-3. El evaluador aún no genera matrices de confusión exigidas para el reporte final; pendiente junto con revisión y ejecución.
## 18 de octubre de 2026 — Ejecutor IA y matrices de confusión

17 pruebas específicas aprobadas en 7.03s, incluido adaptador real LangChain/SDK contra MockTransport con captura de modelo efectivo/ID/tokens. Nuevos casos: vista previa sin construir proveedor ni salida; hashes alterados bloquean envío; 55 llamadas simuladas sin enviar etiquetas/IDs; reanudación sin repetición; cambio de modelo rechazado; límite acumulado; fallo sin excepción sensible; interrupción tras START conservada como incierta; concurrencia/diario corrupto bloqueados; categoría fuera de catálogo rechazada; matrices conservan fallos, abstenciones y Alta→Baja. No son 55 llamadas externas ni medición de calidad.

Primer pase específico: 11 aprobadas/6 fallidas por PermissionError de os.replace en temporal del sandbox. No se retiró escritura atómica para ocultarlo: repetición con --basetemp dentro de .pgdata autorizada dio 17/17. La llamada de CLI desde raíz falló por ModuleNotFoundError app; desde backend la vista previa verificó los hashes sin llamadas. Para estas validaciones se retiró SSLKEYLOGFILE solo del proceso hijo, como en avances previos.

Suite final completa con ejecutor PostgreSQL 18.6 aislado y temporal de pytest dedicado: upgrade 0005 dos veces, alembic check sin operaciones nuevas, 141 aprobadas/0 fallos/0 errores/0 omitidas en 27.85s; servidor y carpeta de clúster final retirados. .pgdata de fixtures de pytest permanece ignorada. No se tocó base de desarrollo ni leyó .env. Frontend sin cambios/no repetido. Imagen Docker/CLI en Docker no ejecutados en este entorno; guía para terminal de autora.

Conjunto fijado v1 conserva textos/etiquetas aprobados de forma general por la autora. No implica revisión independiente de terceros ni revisión individual observada; el manifest conserva esa distinción. Sin llamadas/predicciones de evaluación reales ni aceptación RF-3. 74-evaluacion-ia-ejecutor.json registra resultados de infraestructura.
## 18 de octubre de 2026 — Resultado externo IA v1

Archivos de ejecucion-v1 inspeccionados y evaluador recalculado offline: resultados idénticos a reporte original. Diario con 55 START/END y 55 respuestas únicas; hashes conjunto/proveedor coinciden con manifest. No hay fallos de transporte/esquema ni inciertos. Modelo efectivo gpt-4.1-mini-2025-04-14, prompt plurione-classify-v1; 17624 tokens entrada/3788 salida según metadatos, sin cotejo de factura o saldo.

Categoría 32/50 (64 %, meta 90 %); prioridad 30/50 (60 %, meta 80 %); abstenciones separadas 5/5. Doce referencias regulares quedaron inconclusas y se mantienen en denominador. Alta 14/15; EVAL-C4-02 abstuvo ante una estantería inestable con caída inminente. Revisión técnica confirma contradicción con referencia Riesgos/Alta, sin cambiarla; aprobación humana de análisis pendiente. Cero Alta→Baja no compensa los umbrales incumplidos. Veinticuatro discrepancias totales en reporte; análisis y recomendaciones en evaluacion_ia/RESULTADOS_V1.md. RF-3 parcial/no aceptado.

No se modificó prompt ni se repitieron llamadas. No se atribuye revisión independiente de etiquetas ni calidad general a este conjunto sintético. Usarlo para diagnóstico implica reservar otro conjunto independiente para aceptación final tras corrección. Revisión de archivos sin claves/tokens de acceso observados; metadatos incluyen solo IDs de respuesta, modelo y uso. Evidencia 75 y originales conservados. Actualización documental, sin repetir suites de código.
## 18 de octubre de 2026 — Validación del prompt v2 sin proveedor externo

43 específicas aprobadas/13.11s. Suite completa con PostgreSQL 18.6 aislado: 147 aprobadas/0 fallos/0 errores/0 omitidas, 35.30s; upgrade 0005 repetido y check sin diferencias. Servidor/carpeta propios retirados. Se mantienen fixtures SQLite y MockTransport en la suite; no son 147 integraciones del modelo.

Cobertura nueva: trabajo pendiente v1 omitido antes de invocar proveedor v2; entrada con órdenes incrustadas permanece en mensaje humano y no altera instrucciones/catálogo autorizado; contenido de definiciones/prioridades/contexto simulado transportado al adaptador; rechazo de salida mantiene fallo y metadatos sin excepción cruda; vista previa de candidato sin congelar permitida pero envío bloqueado; evaluación congelada v1 rechazada con proveedor/prompt actuales; ruta de archivo insegura y hash de instrucciones cambiado rechazados. Las aprobaciones de etiquetas para probar envío se simulan solo en copias temporales, nunca en manifest candidato real.

Candidato-v2: contratos/correspondencia/hashes/distribución verificados offline, 50 referencias (10 por categoría, 15 Alta/20 Media/15 Baja) más cinco abstenciones, 55 textos únicos; sin coincidencias textuales exactas con v1. Esa diferencia textual no prueba independencia estadística ni humana. Etiquetas propuestas por asistente después de fijar prompt v2; revisión real pendiente y envío bloqueado. CLI vista previa correcta, sin clave ni llamadas.

No se alteraron resultados/referencias v1, no se cambió modelo local ni se realizaron llamadas adicionales. No se afirma mejora de 64/60 % por pruebas de código ni que un modelo ignore siempre instrucciones incrustadas. Frontend sin cambios/no repetido; aplicación Docker y medición externa v2 pendientes. Evidencia 76. RF-3 parcial/no aceptado; control manual permanece.
## 18 de octubre de 2026 — Comando de evaluación v2 preparado

Conformidad de la autora sobre los 55 casos nuevos recibida por respuesta explícita; se registra como revisión declarada, no observación independiente ni validación estadística. aceptacion-v2 conserva equivalencia JSON y tres hashes UTF-8/LF del candidato. Primera verificación de bytes produjo AssertionError por CRLF/LF después de escribir versión normalizada; nueva verificación de contenido y hashes correcta, sin cambiar textos/etiquetas. No se repitió la creación ni sobrescribió el candidato.

Script EVALUAR_IA_V2.ps1 comprobado con cuatro controles: parser PowerShell sin errores, vista previa nativa correcta sin invocar Docker, construcción/ejecución con Docker simulado usando aceptacion-v2/ejecucion-v2 y límite 55, y error de construcción detiene antes del envío. Varias vistas previas sin llamadas; no se creó ejecucion-v2. Mensajes de ejecución en test corresponden a stub, no a resultados externos. Cero llamadas/cargos adicionales y ninguna clave/.env inspeccionados. Backend/worker no modificados: se conserva suite previa 147/147 y no se repite. Docker y calidad v2 reales todavía pendientes; evidencia 77.
## 18 de octubre de 2026 — Evaluación externa v2: umbrales cumplidos

55 respuestas externas; recomputación de evaluate idéntica a reporte original, hashes de aceptacion-v2/proveedor/prompts y run.json correctos, diario 55 START/END e IDs únicos. Modelo efectivo gpt-4.1-mini-2025-04-14; uso reportado 49321 entrada/4191 salida/53512 total, sin cotejo de factura o saldo. Cero fallos de transporte/esquema, cero abstenciones en referencias regulares. Evidencia 78 y originales preservados.

Categoría 49/50 (98 %, meta 90 %), prioridad 40/50 (80 %, meta 80 %), abstenciones 5/5. Alta 15/15; sin falsos negativos de Alta ni Alta→Baja. Cumple metas numéricas de este conjunto. Revisión técnica individual de 11 discrepancias en RESULTADOS_V2.md: diez Media→Baja y una categoría discutible de aclaración de falta histórica, conservada según referencia. La prioridad Media tiene 10/20 aciertos y la métrica global carece de margen sobre el umbral; debe mantenerse como sugerencia con revisión humana.

La autora revisó etiquetas antes de llamadas; no se atribuye revisión de terceros ni aceptación nueva de resultados. human_acceptance=false original se conserva. El conjunto v2 no se usó para ajustar su prompt antes de ejecutar; v1/v2 diferentes no prueban causalidad aislada de mejora, ni independencia estadística. No se modifican referencias para incrementar puntuación. Sin nuevos envíos, ajustes de prompt o repetición de tests en esta revisión documental. Aceptación integral/operación y otros controles pendientes; no se declara toda la plataforma terminada.
## 18 de octubre de 2026 — API 0.10.2 / distinción Media-Baja v3

50 pruebas específicas aprobadas en 15.31s. Suite completa PostgreSQL 18.6 aislado: 154 aprobadas/0 fallos/0 errores/0 omitidas, 34.52s; upgrade 0005 repetido, check sin operaciones nuevas, servidor/carpeta de clúster propios retirados. Backend contiene también fixtures SQLite/SDK simulado; no son 154 integraciones del modelo. Frontend sin cambios/no repetido.

Cobertura nueva: global 80% puede pasar con Media 50% y debe fallar indicador complementario; forzar todas las salidas no Alta a Media falla Baja; fallos y abstenciones se conservan en denominador de clase; clase sin referencias es null, no acierto perfecto; par requiere ambos niveles correctos y referencia Media/Baja de misma categoría/ámbito; versiones v1/v2 congeladas rechazadas con v3 y jobs pendientes omitidos antes de llamar; mensajes transportan prioridad ordenada sin reducir Alta por mera ausencia de peligro si existe vencimiento grave. Son comprobaciones de contrato/medición, no garantía de comportamiento semántico del modelo.

DIAGNOSTICO_MEDIA_BAJA_V2.json recalcula las mismas predicciones externas: Media 10/20 (50%), Baja 15/15 (100%), indicador complementario false; metas globales históricas no alteradas. Ninguna llamada nueva ni reporte v2 editado. Candidato-v3 válido offline: 20 pares (40 casos), 10 Alta, 5 abstenciones; 10 por categoría, 55 textos únicos y cero coincidencias textuales exactas con v1/v2. Autoría asistente, revisión humana/congelación pendientes y sin predicciones. No se atribuye independencia por esos conteos. Evidencia 79. Medición real v3/Docker pendiente, sin afirmar precisión mejorada por tests.
## 18 de octubre de 2026 — Vista previa del comando v3

scripts/EVALUAR_IA_V3.ps1: tres controles finales correctos, parser sin errores, vista previa nativa del candidato con hashes correctos y cero invocaciones Docker, y -Ejecutar detenido por ausencia de aceptacion-v3 antes de construir/invocar Docker. Se utilizó una función Docker que fallaría si fuera llamada y su contador quedó en cero. No hay llamadas reales ni resultados v3; no se creó aceptación sin respuesta de la autora.

El comando usa solo datos/versiones locales y no imprime .env o claves. Rama externa preparada con aceptacion-v3/ejecucion-v3, 55 intentos y diario; todavía no comprobada con proveedor/Docker reales. Backend sin cambios y suite 154 previa no repetida para este script. Evidencia 80. Revisar y fijar etiquetas antes de ejecución; no atribuir independencia o calidad por vista previa.
## 18 de octubre de 2026 — V3 fijada tras revisión declarada

La autora confirmó revisión y conformidad de todos los tipos de casos v3. aceptacion-v3 preserva equivalencia JSON/hashes UTF-8-LF de referencias, entradas y catálogo; sin cambio de etiquetas o pares. Manifest registra conformidad declarada, no revisión independiente certificada.

Cuatro controles finales del comando: parser correcto, vista previa nativa sin invocaciones Docker, construcción/evaluación simuladas con dataset/salida exclusivos v3 y límite 55, y fallo de construcción detiene antes de ejecutar. No hubo Docker/proveedor reales ni se creó ejecucion-v3; mensajes de evaluación en prueba son del stub. Backend/script no modificados, suite 154 previa no repetida. Evidencia 81. Medición real sigue pendiente: Media ≥16/20 y Baja ≥16/20 complementarias a metas globales/Alta/abstención; no se afirma mejora por estos controles.
## 18 de octubre de 2026 — Resultado externo v3 y revisión de Alta

Recomputación offline idéntica a reporte, hashes y run.json correctos, 55 START/END y respuestas únicas; sin fallos de transporte/esquema o envíos inciertos. Modelo efectivo gpt-4.1-mini-2025-04-14, prompt v3, uso reportado 67119 tokens (63069/4050), sin coste/factura cotejados. Datos revisados/fijados antes de ejecutar, originales preservados, evidencia 82.

Categoría 49/50 (98%), prioridad 46/50 (92%), Media y Baja 20/20 cada una, pares contrastivos 20/20, abstención 5/5. Alta solo 6/10: MB3-C1-A2, MB3-C3-A1, MB3-C5-A1 y MB3-C5-A2 clasificadas Media. Cero Alta→Baja no elimina esos cuatro falsos negativos; revisión individual en RESULTADOS_V3.md confirma plazo explícito/consecuencia grave o pérdida operativa inminente descritos. Motivos a veces reconocen esas condiciones sin asignar Alta. Una diferencia de categoría en MB3-C1-A1, prioridad Alta correcta. No se alteran etiquetas o puntuaciones.

Los indicadores global/complementario son true según reglas históricas, pero human_acceptance=false se conserva y no se recomienda aplicar v3 ni aceptar prioridad integral. No se cambia el umbral para ocultar resultado; falta verificar que la mejora específica no comprometa urgentes. V2/v3 son conjuntos distintos y no prueban causalidad aislada. Sin cambios de código, llamadas adicionales o suites repetidas. Versión de procesos operativos no inspeccionada; el contenedor de evaluación no los actualizó.

## 18 de octubre de 2026 — Alta v4 preparada y referencias revisadas

API 0.10.3/prompt plurione-classify-v4 aclara que los criterios de Alta son alternativas suficientes. Un plazo/evento inminente con consecuencia grave descrita puede exigir Alta sin peligro físico; no basta una fecha aislada. Se conservan Media/Baja, catálogo, revisión humana y prioridades oficiales sin cambios automáticos. No se añade corrección por palabras clave ni se cambia el modelo local.

El evaluador agrega all_high_priority_identified (mínimo diez referencias Alta, cero falsos negativos) y priority_checks_met (metas globales + Media/Baja + Alta; false en ejecución parcial). Diagnóstico offline separado DIAGNOSTICO_ALTAS_V3.json: global y Media/Baja históricos true, pero Alta/indicador combinado false por cuatro Alta→Media. Originales v1/v2/v3 intactos; no se reescribe el reporte histórico.

Conformidad explícita recibida sobre los nuevos contrastes y etiquetas: aceptacion-v4 fijada antes de predicciones, con hashes equivalentes al candidato. Contiene 20 Alta (doce plazos graves no físicos), 15 Media, 15 Baja, quince pares y cinco abstenciones; cero coincidencias textuales exactas anteriores no garantiza independencia estadística. Autoría sintética del asistente y revisión declarada, sin atribuir terceros. Meta complementaria Alta 20/20, Media y Baja ≥12/15 cada una; categoría ≥45/50, prioridad ≥40/50 y abstenciones 5/5.

Validación: 56 pruebas específicas aprobadas en 13.65s; suite completa con PostgreSQL 18.6 aislado: 160 aprobadas, cero fallos/errores/omisiones, 95.81s. Migración 0005 dos veces y check sin operaciones nuevas; servidor temporal detenido y archivos propios retirados. La suite incluye SQLite/SDK simulado, no son 160 integraciones del modelo. Frontend sin cambios ni repetición. Cero llamadas externas nuevas, sin inspeccionar .env ni medir precisión v4. Evidencia 83. Calidad real y aceptación integral RF-3 pendientes.

Comando preparado: scripts/EVALUAR_IA_V4.ps1 valida sin gasto por defecto; -Ejecutar construye ai-worker y evalúa con salida exclusiva ejecucion-v4, máximo 55 intentos acumulados y cargos posibles. Conservar diario ante fallos. No actualiza contenedores operativos; aplicar API/worker juntos solo cuando corresponda, sin migración nueva. Jobs pendientes v1/v2/v3 se omiten antes de envío y resultados completados se conservan. No repetir para buscar una puntuación favorable ni editar etiquetas tras ver respuestas.

Comando v4 después de fijar: cuatro controles correctos (parser, vista previa sin Docker, argumentos con Docker simulado y detención tras fallo de construcción). El primer ensayo del stub falló por alcance de variables en el propio ensayo; corregido a variables globales exclusivas y repetido con éxito. No fue un fallo de aplicación ni una llamada real. No existe ejecucion-v4 todavía.

## 18 de octubre de 2026 — V4 cumple metas de prioridad

Evaluación externa v4 verificada: 55 respuestas, diario 55 START/END, IDs únicos y hashes coherentes; todas las métricas recalculadas coinciden. Categoría 47/50 (94%), prioridad 50/50, Alta 20/20, Media 15/15, Baja 15/15, pares 15/15 y abstención 5/5; ningún Alta omitido. Cumple metas numéricas globales y complementarias. Tres diferencias Ausencias→Solicitudes Administrativas del mismo grupo se conservan como errores; prioridades correctas. Revisión técnica en RESULTADOS_V4.md, evidencia 84 y originales intactos.

Modelo efectivo {'gpt-4.1-mini-2025-04-14': 55}; tokens reportados 76487 entrada/4164 salida, sin cotejar factura o saldo. Conformidad previa de etiquetas no equivale a aceptación integral: human_acceptance=false preservado. Conjuntos v3/v4 diferentes, sin prueba causal aislada ni garantía general. Mantener validación humana y no repetir para buscar puntuación favorable. Evaluación no actualiza procesos operativos. Sin código/referencias/configuración modificados, llamadas nuevas ni suites repetidas; 160 pruebas backend previas. Cambio local previo de REVISION.md conservado fuera del commit. Continuar H8 correo/H9 analítica y QA final; aceptación integral RF-3 pendiente.

## 18 de octubre de 2026 — Correo por eventos preparado y probado

API 0.11.0/React 0.8.0 y migración 0006: outbox de correo en la transacción de creación, asignación/reasignación (incluidas protección y administración), resolución y reapertura. Deduplicación por evento/destinatario y omisión registrada sin destinatarios elegibles. Worker separado con consulta durable, reclamo/token y comprobación de acceso al reclamar e inmediatamente antes de SMTP. Correo mínimo ID/enlace, sin contenido del expediente ni nombres. RH autorizado consulta fallos/omisiones paginados desde React/API. El enlace requiere login y autorización vigente.

Perfil mail con Mailpit v1.27.4, SMTP solo interno y panel en loopback; no envíos a buzones reales ni claves IA en el worker. MAIL_ENABLED desactivado fuera del perfil. Un intento inicial más tres reintentos transitorios, fallo permanente sin reintento, mensajes de error genéricos. Bloqueos de caso/administración se mantienen durante despacho con timeout por socket; pueden demorar brevemente otras mutaciones. SMTP/PostgreSQL sin transacción común: Message-ID estable no garantiza exactamente una entrega; caída tras aceptación puede duplicar aviso. No confundir SMTP aceptado con recepción o lectura.

Validación: 19 específicas iniciales aprobadas (13.63s), luego ampliadas con TLS y cierre de socket; suite final 183 aprobadas/0 fallos/errores/omisiones en 41.71s con PostgreSQL 18.6 aislado. Upgrade 0006 dos veces y check sin diferencias; clúster propio detenido/retirado. Incluye siete pruebas PostgreSQL y también fixtures SQLite/transportes simulados, además de un SMTP TCP local real sin reenvío. React: 67 aprobadas en suite (157.95s) más 1 prueba de enlace autenticado; build correcto. Script ACTUALIZAR_CORREO: seis controles con Docker simulado, parser/secuencia y parada por cada fallo. YAML revisado sin expandir secretos. Evidencia 85.

Incidencias de verificación: primera prueba de recuperación esperaba un trabajo concreto sin respetar orden de cola; corregida para drenar y comprobar mismo ID/intentos. Dos ejecuciones React con forks agotaron tiempos (5 y 8 fallos, esta última con worker sin arrancar); se repitió con threads/un worker y mayor timeout, sin eliminar aserciones. Primer PostgreSQL no pudo abrir puerto (Permission denied); log y pg_ctl confirmaron servidor apagado, carpeta ignorada preservada; segundo arranque y ejecución final correctos. Ensayo YAML inicial falló por expansión PowerShell en la aserción, corregido a archivo Python literal. No se utilizaron bases de desarrollo, .env ni proveedores externos.

Pendiente recorrido Docker/Mailpit y navegador real en el equipo, CI remoto y QA integral. Script de actualización prepara ese recorrido sin seed/bootstrap ni borrados; no se ejecutó Docker desde las herramientas. No se declara RF-5 aceptado integralmente por mocks. Guía CORREO.md. IA v4/resultados permanecen intactos, sin nuevas llamadas o gasto; cambio local previo REVISION.md conservado fuera del commit.

Revisión final: una asignación pendiente conserva el aviso cuando comienza revisión con el mismo responsable; solo la reapertura exige el mismo ciclo para su aviso. Se corrigió esa omisión y se añadió una prueba del recorrido real antes de repetir la suite final. React final: 67 en suite más enlace autenticado aislado (1 aprobado, 13 no seleccionados por filtro), sin otras omisiones de cobertura.

## 18 de octubre de 2026 — Recorrido de correo 86–91

Recorrido aportado por responsable: capturas 86–91 verifican tres avisos de creación a RH distintos, un aviso de asignación al supervisor, resolución al reportante del caso ENTORNO y reapertura al supervisor. Enlace abre el expediente correcto bajo cuenta RH; panel React muestra seis aceptaciones SMTP al primer intento. Mensaje mínimo con ID/enlace, sin descripción/resolución. Evidencia estructurada 92 con hashes; capturas conservadas sin edición ni credenciales visibles. SMTP de captura Mailpit, no entrega a buzones reales. No se consultó la base operativa ni se repitieron pruebas o llamadas IA. RF-5 tiene recorrido básico real; exclusiones/fallos reales y aceptación integral pendientes (cobertura automatizada previa: 85).

## 18 de octubre de 2026 — Agregación y conexión Power BI preparadas

API 0.12.0/esquema 0007: analytics.incident_metrics y export_info con agregación previa, única granularidad mes de creación/categoría/departamento histórico. Excluye confidenciales, cualquier relación activa o pendiente y afectado gestor aun con marca incorrecta. Sin IDs personales, textos ni filas de expedientes. Cada subconjunto/complemento no vacío exige ≥5 casos y, si hay PERSONA, ≥5 afectados distintos; se suprime toda la celda si alguno incumple. No publica totales/subtotales ni valores parciales que permitan completar una celda oculta.

Fórmulas verificadas: promedio del último ciclo resuelto, población de reapertura recuperada también de snapshots auditados (primer evento del periodo, ID una vez), concordancia operativa solo con validación humana vigente y conteos IA omitida/fallida. Periodo de reapertura fijo: inicio del año local a corte; filas siguen agrupadas por mes de creación, incluso cohortes anteriores. Corte, periodo y metadata en un mismo SELECT para Power BI, con fila metadata sin números cuando no hay población. Sin ventana arbitraria ni exportación de promedios históricos alternativos.

Cuenta nueva de lectura por operador con contraseña interactiva, sin secretos en fuente/chat: SELECT solo en dos vistas, sin privilegios operativos o creación. Rechaza roles existentes y falla/revierte ante permisos inseguros de PUBLIC. ACL comprobadas con SET ROLE en PostgreSQL, no se confía solo en default_transaction_read_only. Script ACTUALIZAR_ANALITICA.ps1 construye/migra API y aplica puerto PostgreSQL opcional solo loopback mediante compose.bi.yaml, sin seed ni borrar datos. Plantillas M/SQL/DAX en powerbi y guía ANALITICA.md; usuario confirmó tener Desktop instalado. Importación, medidas, filtros, formato y .pbix todavía no ejecutados/validados en Desktop.

Validación final: 201 pruebas backend aprobadas/0 fallos/errores/omisiones en 45.99s con PostgreSQL 18.6 aislado; upgrade 0007 repetido/check sin diferencias, clúster propio detenido/retirado. Pruebas de celdas 1–4, cinco casos de una misma persona, mezcla ENTORNO/PERSONA, falta de denominador, privacidad que cambia, resolución con pocos contribuyentes, múltiples ciclos, traslados, futura auditoría, permisos negativos y rollback de provisión insegura. Primera ejecución 199 aprobadas/44.05s; luego extracción única y guarda de auditoría posterior al corte añadidas y verificadas en suite final. SQL de extracción se ejecutó en PostgreSQL; plantillas M/DAX son fuentes pendientes de compilación en Desktop. Seis controles del script con Docker simulado, sin despliegue real. React sin cambios/sin repetir sus pruebas. Evidencia 93.

Sin leer .env, consultar base operativa, crear cuentas reales, generar incidencias o hacer llamadas IA. No se produjo .pbix ni se compartió/publicó reporte. Puerto opcional puede reiniciar brevemente PostgreSQL; cuentas BI/copia distribuida requieren custodia/revocación manual. Supresión conservadora puede dejar todas las celdas vacías; no es un fallo ni se baja el mínimo para obtener gráficos. Instantáneas/metadata reducen pero no eliminan reidentificación temporal o externa: solo datos simulados y aprobación integral pendientes. Cambio local previo evaluacion_ia/REVISION.md permanece fuera del commit.

## 19 de octubre de 2026 — Informe Power BI guardado y revisado

Informe powerbi/plurione_bi.pbix localizado y registrado junto con capturas 94–95; 96–97 inspeccionadas y conservadas solo locales por nombre real de cuenta visible en cabecera, excluidas mediante .gitignore sin modificar ni eliminar originales. Evidencia 98 contiene hashes y límites. Las capturas muestran conexión PostgreSQL, consulta Indicadores de 24 columnas y tres celdas agregadas con números NULL/«Suprimido por privacidad»; no son tres incidencias. La conexión de prueba local se configuró sin TLS por la responsable; no se automatizaron credenciales ni ajustes de seguridad.

Detectada discrepancia entre captura 97 y archivo: PBIX de 78236 bytes solo tenía Volumen visible en la tabla. Con computer-use se seleccionó únicamente Power BI/plurione_bi y guardó con Ctrl+S el trabajo ya abierto, sin modificar medidas o datos. Archivo final de 78823 bytes, CRC ZIP correcto y definición PBIR revisada: tabla con mes_creacion directo, categoría, departamento, privacidad y cuatro medidas; totals=false y showAll=true. También tarjeta Fecha de corte y leyenda de población parcial/datos simulados. No se confundió guardar un visual con reextraer datos: el corte visible sigue 18/10/2026 09:02:54 p.m.

La revisión del contenedor no decodifica DataModel binario ni certifica ausencia de todas las tablas ocultas/fuentes individuales. Formatos porcentuales y resultados positivos no son verificables con todas las celdas suprimidas. RF-6 tiene conexión/informe básico real, pero falta revisión semántica, valores publicables de QA, actualización manual y aceptación integral. No reducir k=5 ni reemplazar NULL por cero para generar gráficos. Sin publicación, consultas operativas desde herramientas ni llamadas IA; backend/SQL sin cambios y 201 pruebas previas no repetidas. El lanzador venv no pudo iniciar su Python en este entorno; para inspección ZIP/JSON se usó Python 3.12.14 del runtime de artefactos, sin reinstalar ni modificar el entorno del proyecto. Cambio local previo evaluacion_ia/REVISION.md preservado fuera del commit.


## 19 de octubre de 2026 — Reorganización documental y codificación

Se contrastó la evaluación aportada por la autora con código y evidencia posterior: correo e informe Power BI ya existen, aunque no están aceptados integralmente. Se consolidaron guía de inicio, manual técnico, guías de módulos, alcance del MVP, backlog, entregables y trazabilidad. El análisis queda en REVISION_EVALUACION.md; índice en docs/README.md. Se retiraron capítulos cronológicos por versión de las guías principales; referencias congeladas, dependencias, migraciones e historial se conservan para auditoría.

Se corrigieron acentos dañados en Swagger y docstrings de main.py, core/database.py y models/__init__.py. Una comparación de árboles AST con el contenido de HEAD confirmó que las únicas diferencias de esas tres fuentes son docstrings y la descripción OpenAPI; no se alteraron rutas, modelos, permisos, versiones técnicas ni lógica de negocio. Verificación estática de UTF-8, enlaces locales y anclas, bloques Markdown y AST sin errores; recuento final en la bitácora. git diff --check sin errores.

El lanzador Python del entorno virtual del proyecto no pudo iniciar su intérprete. Se usó el Python del runtime para comprobaciones estáticas, sin instalar ni reparar dependencias. No se ejecutó la API/Swagger en navegador ni la suite funcional; las 201 pruebas backend previas conservan su fecha y alcance originales. No hubo llamadas IA, consultas a la base operativa, reconstrucción Docker ni modificaciones de .env. No se presenta esta revisión como aceptación final o una nueva calificación.

Registro Git pendiente: el intento de preparar el commit devolvió permiso denegado al crear .git/index.lock, aun con acceso solicitado. Los archivos quedaron guardados en el proyecto; no se creó commit ni se publicó el cambio.

## 19 de octubre de 2026 — Propuesta técnica y arquitectura

Se elaboraron PROPUESTA_TECNICA.md y ARQUITECTURA.md a partir del PRD, modelos, servicios, workers, Compose, vistas de analítica y workflows presentes. La propuesta incluye cobertura RF-1 a RF-8, alternativas/compromisos, recursos sin cotización inventada, riesgos y criterios de aceptación. La arquitectura contiene diagramas Mermaid de componentes, secuencia y relaciones, límites de confianza, transacciones, acceso, trabajo asíncrono y despliegue local.

Revisión estática de referencias, nombres de entidades, perfiles, puertos por defecto, cuenta BI limitada y separación de responsabilidades contra sus fuentes. Se distinguen las credenciales operativas compartidas de los permisos BI, persistencia de respaldo y unicidad de la outbox de entrega exactamente una vez. Se actualizaron índice, entregables, backlog, MVP, manual técnico y trazabilidad para no mantener esos dos documentos como ausentes.

No se ejecutaron servicios ni nuevas pruebas funcionales, cargas, restauraciones o llamadas al proveedor. Los diagramas se comprobaron como bloques de documentación; no se acredita renderizado gráfico ni ejecución de sus flujos en esta actividad. La validación final de enlaces/UTF-8 y coherencia se registra en bitácora. No se consultó .env, la base operativa ni datos personales; revisión previa y capturas excluidas de Git preservadas. El registro Git sigue pendiente por el bloqueo de escritura indicado en la entrada anterior.

## 19 de octubre de 2026 — Manual de usuario y mantenimiento preparados

Se elaboraron MANUAL_USUARIO.md (recorridos por perfil, registro, ciclo, protección, asistencia, correo, administración, lectura BI y soporte) y PLAN_MANTENIMIENTO.md (soporte por niveles, rutinas, copia lógica y ensayo de restauración en contenedor sin red ni consumidores). Actualizados índice, entregables, backlog, MVP, manual técnico, análisis de evaluación, trazabilidad y decisiones para distinguir documentos disponibles de ejecución pendiente.

Comprobaciones realizadas: nombres y reglas contrastados con guías y componentes React; modelos de outbox, Compose y estado previo revisados. Semántica de pg_dump/pg_restore consultada en documentación oficial PostgreSQL. Cuatro bloques PowerShell analizados con el parser del lenguaje, cero errores de sintaxis y ningún comando del procedimiento ejecutado. Validación estática del cambio acumulado: 30 documentos, 218 enlaces/anclas locales y tres fuentes Python, sin errores de codificación, bloques o diferencias funcionales inesperadas frente a la revisión base. git diff --check correcto.

No se inició Docker ni PostgreSQL de ensayo, no se detuvieron servicios, no se creó copia de base, no se restauraron datos ni se ejecutó la suite funcional en esta actividad. Por tanto no se acredita respaldo válido, restauración exitosa, tiempos de recuperación ni preservación de ACL. La lectura del catálogo y el hash previstos son controles parciales; el plan exige restauración real, comprobaciones de datos y verificación de permisos separada antes de aceptar recuperación. Tampoco se acredita capacitación impartida o matriz completa de roles.

No se leyeron .env, claves, sesiones o datos operativos. Copias futuras deberán quedar fuera del repositorio y bajo custodia. Se conservaron los cambios previos y referencias congeladas; el registro Git sigue pendiente por el bloqueo de escritura indicado anteriormente.

## 19 de octubre de 2026 — Intento real de recuperación aislada bloqueado

Se agregó backend/scripts/test_recovery_isolated.py para crear origen/destino nativos nuevos, migrar, insertar un conjunto ficticio, copiar/restaurar y comparar datos, restricciones, índices y vistas; reconstruye BI y prevé permisos negativos y rechazo de archivo inválido. Es un ejecutor de QA, sin cambios al código de negocio. Requiere dependencias existentes y binarios PostgreSQL; no instala ni repara entornos.

Intento real: initdb de origen completó. pg_ctl no pudo crear el token restringido (error Windows 87), y no inició servidor (error 3). La parada intentada tampoco pudo confirmarse desde el ejecutor inicial; una consulta posterior pg_ctl status confirmó «no server running». Evidencia 99 conserva fallo y comprobación posterior; no se creó copia, no se migró ese origen ni se restauró. No se inició destino. La carpeta propia quedó en .pgdata ignorada por Git; no se borraron recursos ajenos.

Docker no fue localizado y el Python del proyecto devolvió acceso denegado en herramientas. Sin reinstalar, las dependencias de datos existentes se importaron con Python del runtime y psycopg en implementación Python; sirvió para comprobaciones y el intento documentado, no para cambiar versiones del proyecto. Fixture probado en SQLite/FK con seis casos, uno confidencial/cerrado, participante, AIJob y outbox. CLI --help correcta. Sintaxis y enlaces verificados por separado; no se ejecutó suite completa ni llamadas externas. Estas comprobaciones no sustituyen la recuperación PostgreSQL y ACL pendientes.

El plan incluye ahora una orden reproducible para terminal propia y reporte nuevo, sin reusar evidencia fallida como éxito. No se eludió el mecanismo de token restringido ni se apuntó a la base de uso. Mantener RNF-3/RNF-5 parciales y completar Power BI/aceptación integral por separado.

## 20 de octubre de 2026 — Recuperación nativa y permisos BI aprobados

La autora informó que Docker volvió a funcionar. Desde herramientas su API continúa devolviendo permiso denegado; el Python del proyecto sí inicia y se ejecutó el ensayo PostgreSQL nativo con .env y base de trabajo fuera del recorrido.

Evidencias 100/101/102: copia y restauración correctas, ambas instancias detenidas, datos de todas las tablas iguales; comparación de definiciones rechazada por casts equivalentes expresados de forma diferente tras pg_dump/restore. Se mantuvieron los fallos como tales. Se añadieron diagnósticos de secciones/tablas/vistas y normalización estricta de arrays de literales varchar a text, incluidas las formas pretty con/sin paréntesis. Nunca se normalizan valores internos, tipos acotados, números, casts de columnas u opciones de seguridad. Cinco pruebas pasaron en 0.09 s, con pytest cache desactivada; primer intento de prueba no se ejecutó porque faltaba permiso para crear el archivo nuevo, resuelto al conceder acceso a su carpeta.

Evidencia 103 PASSED: migración/check de origen y check del destino correctos; catorce tablas restauradas idénticas por conteo y hash de filas completas, seis casos (cinco ENTORNO exportables y uno PERSONA confidencial/cerrado), historial, participante, credencial ficticia no utilizable, sesión expirada/revocada, AIJob y outbox. Comparación de dos vistas/opciones, 144 restricciones y 35 índices. Archivo inválido rechazado. Cuenta BI del origen ausente en el destino como rol global; nueva cuenta BI provisionada por el procedimiento del proyecto, lee ambas vistas y volumen cinco, y se rechazan lectura, borrado y DDL sobre tablas operativas. Origen y destino sin cambios de datos durante validación. Ambos clústeres detenidos; archivos propios conservados en .pgdata ignorado, sin borrados recursivos.

Copia 0.546 s, restauración 0.667 s y check destino 2.210 s: son etapas de un conjunto pequeño, no un RTO ni rendimiento bajo carga. Binarios PostgreSQL 18.6 y Python 3.11 del proyecto; no se reinstaló ni cambió el entorno. No hubo API, workers, correo, llamadas IA o acceso a la base operativa. No se repitió la suite funcional completa: este avance valida el ejecutor, comparador y ensayo. Secuencia Docker, recuperación de una instalación con configuración/roles completos, retención/custodia, Power BI y aceptación por roles siguen pendientes.


## 20 de octubre de 2026 — Modelo Power BI revisado y refresco diagnosticado

Propósito: verificar el PBIX real antes de continuar aceptación RF-6. Desktop confirmó cinco medidas válidas. Reapertura y Concordancia ya tenían formato Porcentaje/un decimal y dividían entre 100; no se modificaron. El FormatString vacío de INFO.VIEW.MEASURES no bastaba para concluir que faltaba formato; se corrigió esa interpretación contrastando la cinta. Resolución horas pasó de General a Número decimal/dos decimales. No cambió su expresión por celda.

Desactivadas fechas automáticas solo para el archivo actual. Inventario DAX antes: Indicadores y cuatro tablas generadas ocultas; después de ejecutar de nuevo: únicamente Indicadores, visible, Import. Una partición; QueryDefinition coincide con Indicadores.pq al ignorar espacios, CR/LF/tabuladores y el comentario inicial conocido. No es una comparación semántica SQL. Se guardó el archivo antes del refresco. ZIP/CRC y tres visuales comprobados, sin cambiar los ocho campos de tabla, showAll=true o totals=false. Evidencia 104 contiene hashes y observaciones sin capturas con nombre real.

Actualización manual intentada: FALLÓ por conexión rechazada. La tarjeta conserva 18/10/2026 09:02:54 p.m. Docker Desktop muestra motor activo y postgres-1 en ejecución sin puerto publicado; falta aplicar compose.bi.yaml. La CLI de herramientas recibió permiso denegado en la tubería de Docker y no se alteraron ACL. El aviso de error quedó abierto: la automatización rechazó el cierre al identificar el punto como msedgewebview2 en vez de PBIDesktop, también tras activar/refrescar; se detuvieron los reintentos. No se confundió guardar con refrescar ni se declararon valores nuevos.

Archivos: powerbi/plurione_bi.pbix, powerbi/README.md, ANALITICA, BACKLOG, ENTREGABLES, TRAZABILIDAD, DECISIONES, QA y esta bitácora; nueva evidencia 104. Primer intento de escribir la evidencia rechazado por permisos de carpeta; se solicitó acceso acotado a docs/powerbi antes de repetir. Sin cambios de backend, SQL, credenciales, seguridad, umbral, NULL, datos simulados, publicación, correo o llamadas IA. Suite backend no repetida. Pendientes: aplicar puerto desde terminal propia, refrescar sin error, valores publicables y retirada tras cambio de elegibilidad, custodia y aceptación integral. Cambios previos y revisión IA local preservados; sin commit nuevo.

Validación documental del avance: 30 documentos y 221 enlaces/anclas, UTF-8 y bloques sin errores; tres fuentes Python descriptivas conservan AST funcional. Evidencia JSON coherente y ZIP/CRC del PBIX correctos. git diff --check no pudo ejecutarse: Git devolvió «this operation must be run in a work tree»; no se declara aprobado. Actualizados también MVP y revisión de evaluación. Sin captura nueva ni commit.


## 20 de octubre de 2026 — Refresco confirmado y QA de presentación/retirada en Desktop

La autora confirmó aplicar la capa BI y actualizar. Se observó el principal sin aviso y con corte 20/10/2026 10:06:02 a.m.; Ctrl+S guardó el resultado. Tres celdas suprimidas, números vacíos. Evidencia 105 conserva hash/CRC y distingue confirmación del usuario de observación en Desktop; fallo 104 conservado.

Se creó por Guardar como plurione_bi_QA_agregados_ficticios.pbix y se cambió solo su consulta a JSON manual de dos celdas/24 campos. No cambió ninguna expresión de medida. QA visual: 20, 6.00, 55.0%, 50.0% en A; B con volumen 20, indicadores sin denominador BLANK. Cinco controles DAX True, 564 ms. Copia publicable conservada; después entrada suprimida y Actualizar: A conserva etiqueta Suprimido por privacidad y retira sus cuatro números, B conserva volumen 20. Cinco controles ejecutados de nuevo True, 220.7 ms; corte ficticio avanza un minuto y QA se guarda. No son diez escenarios de negocio. Evidencia 106, fixtures, consulta M, DAX y guía reproducible en powerbi/QA.

El hash del principal permanece 2eba3a958b14efc29e3ebf38991c55e9dbc92c82263d09efa5e151eb46b6b636 durante QA. ZIP/CRC correctos. Una captura de aplicación PQ agotó tiempo, recuperada reseleccionando ventana. Lectura inicial del DAX del PBIX como UTF-8 falló; prefijo comprobado y decodificación UTF-16LE correcta, sin modificar el archivo por ese error. Sin credenciales/seguridad, SQL/backend, datos operativos, nuevas incidencias, llamadas IA, correo, publicación o capturas personales versionadas. Suite backend no repetida.

Actualizados README Power BI, guía QA, analítica, MVP, backlog, entregables, trazabilidad, revisión de evaluación y decisiones. Fechas QA fijas/simuladas: no son el corte real del informe principal. La supresión del fixture es manual; falta recorrido integrado de elegibilidad SQL→Desktop, custodia/retirada de copias y aceptación completa. Cambios previos/revisión IA local preservados; sin commit.

Validación final del avance: 30 documentos/224 enlaces locales sin errores de UTF-8, bloques o anclas; revisión adicional de dos README Power BI/siete enlaces y ocho hashes de artefactos correcta. Fixture activo coincide con suprimido.json, dos celdas/24 campos, todos los números de A NULL y volumen de B conservado. Principal reabierto en una segunda ventana, mismo corte guardado y sin aviso; QA permanece guardada por separado. No se repitió Git por el fallo de work tree ya documentado ni se declara commit.


## 20 de octubre de 2026 — Elegibilidad SQL y refresco de agregados en Desktop

Propósito: pasar de agregados manuales a la salida real de las vistas tras un cambio de confidencialidad. Nuevo backend/scripts/test_powerbi_sql_isolated.py; nuevas extracciones/M/DAX/guía en powerbi/QA_SQL, copia QA SQL y evidencias 107–109. Matrices, analítica y README actualizados. Sin cambios en SQL, modelos ni servicios del producto.

107 FAILED: migración/check y lectura BI correctas, fallo del fixture al insertar QA_CONFIDENCIALIDAD, fuera de ck_audit_action; servidor detenido. Se corrigió únicamente a CAMBIO_CONFIDENCIALIDAD, sin relajar la restricción. 108 PASSED: PostgreSQL 18.6 nuevo en loopback, 40 casos ficticios, cuenta BI sin acceso operativo, misma consulta.sql y dos celdas/24 campos. A inicial 20/6h/55%/50%; B volumen 20 sin denominadores. Un caso A marcado confidencial por ORM y auditado; nueva consulta excluye el caso y suprime los once números de A, conservando B. Corte posterior comprobado. Servidor detenido y carpeta propia retenida en .pgdata ignorada; sin .env o base de uso.

109 Desktop: copia independiente de QA con extracciones reales mediante puente JSON. Valores iniciales visibles 20/6.00/55.0%/50.0%; seis controles True (354.5 ms). Expectativas de suprimido antes de Actualizar rechazaron estado/números/corte viejos (control negativo esperado, 477.2 ms). Tras refrescar desaparecen las cifras de A, B conserva volumen 20 y seis controles True (208.8 ms), incluido corte a precisión de segundos. Se guardaron copia publicable y final suprimida; hash/CRC y DAX persistido comprobados. No son doce escenarios de negocio independientes ni una suite backend nueva.

Limitaciones: SQL→JSON→Desktop, no conexión directa Desktop→PostgreSQL temporal; fixture/cambio ORM, sin API/UI ni workers. Principal y QA manual anteriores preservados; el principal mantiene hash 2eba3a958b14efc29e3ebf38991c55e9dbc92c82263d09efa5e151eb46b6b636. Sin datos personales exportados, llamadas IA, correos, publicación ni capturas con nombre real versionadas. Copia intermedia bloqueada por permiso temporal expirado, renovado antes de repetir; una lectura de textos incompleta se releyó sin cambiar archivos. Pendientes: custodia/retirada de copias, matriz por roles y aceptación integral; conector directo aislado si se exige. Sin commit; restricciones Git previamente registradas.

Validación final del avance: 30 documentos/227 enlaces y tres fuentes descriptivas sin errores de UTF-8, bloques, anclas o AST; revisión adicional de tres README Power BI/doce enlaces y diecisiete hashes de artefactos correcta, incluida preservación de QA manual 106. AST del ejecutor nuevo válido. Entrada SQL activa idéntica a suprimido.json; reportes 107 y 108 confirman parada de sus servidores. No se repitió la suite backend ni Git tras el bloqueo de work tree previamente registrado.


## 20 de octubre de 2026 — Consulta administrativa confirmada por la autora

Evidencia 110: la autora indicó iniciar sesión como admin@plurione.local y confirmó que cargan los listados de Usuarios y Departamentos. Es una comprobación manual reportada por ella, sin captura ni observación directa del agente; no acredita altas, ediciones, bajas, auditoría ni restricciones de otros roles. El control de ventanas había fallado y se detuvieron los reintentos para acotar consumo.

Se registró la evidencia y se actualizó RF-7 en TRAZABILIDAD.md. QA y bitácora conservan la procedencia del resultado; aceptación integral pendiente. Una primera solicitud de escritura apuntó por error a una ruta incorrecta, sin modificar archivos; se corrigió el permiso antes de guardar en docs. Validación limitada a lectura JSON y presencia del registro en los tres documentos. Sin pruebas nuevas, cambios funcionales, operación de Power BI, datos modificados o commit.

## 2026-10-29 — Revisión de auditoría 23-oct

[Respuesta verificable](AUDITORIA_2026-10-23.md) y [evidencia201](evidencias/201-respuesta-auditoria-cierre-correo.json): README de arranque en cinco pasos y cuentas DEMO locales; UTF-8 comprobado; RF-5 amplía creación/asignación/resolución/reapertura con aviso de **cierre**, migración0008 y permisos/deduplicación/ciclo vigente. Ocho nuevas pruebas de servicios/SQLite+DDL offline,27casos de regresión de outbox,102herramientas y4React aprobados; buildVite correcto. No atribuir esos resultados a PostgreSQL/Mailpit nuevo. Historial local conservado y copia de publicación preparada; confirmar push/Actions y recorrido nuevo de cierre antes de declararlo aceptado. RNF-2 sigue pendiente con siete formales fuera de umbral. No se requiere resolver RNF-2 para entregar estas correcciones.

## 2026-10-29 — Publicación y CI confirmados

La rama pública main recibió el commit [1794299](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/commit/179429934fb632e1874bd0dcd67ae00747e0f4ff), confirmado por GitHub y git ls-remote. Su árbol a0bf144c395d8795621e8db87ef2eead29c6c587 coincide con la instantánea revisada de495archivos. Se publicó mediante la conexión GitHub autorizada porque el gestor Git local no proporcionó autenticación. Se conserva el historial local original en bundle; no se sobrescribió historial remoto ni se publicó el cambio ajeno de REVISION.md o .env/.pgdata.

**GitHub Actions aprobado:** [Backend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40946040298), trabajos tests y postgres-integration SUCCESS; [Frontend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40946040141) SUCCESS. PostgreSQL ejecutó upgrade head dos veces, alembic check y pytest con RUN_DB_TESTS=1. Son resultados remotos sobre1794299, no se atribuyen a Docker local. Generación local del contrato OpenAPI3.1.0:25rutas y descripción «Gestión» correcta, sin base de datos o servidor HTTP; no captura visual de Swagger.

[Registro202](evidencias/202-publicacion-auditoria-ci-aprobada.json). Se corrigen además dos instrucciones obsoletas de DEMO: exigir migraciones vigentes y crear casos desde el panel, pues seed no crea incidencias. Pendiente instalar esta versión en Docker local mediante ACTUALIZAR_CORREO.ps1 y capturar cierre en Mailpit. RNF-2 continúa pendiente; CI y correo no lo acreditan.

## 2026-10-29 — Verificación local posterior a actualización

[Evidencia203](evidencias/203-actualizacion-local-servicios-y-mailpit.json): API /health y /health/db HTTP200; Mailpit /livez HTTP200. OpenAPI0.12.0 describe «Gestión» correctamente y expone seguimiento mail. Docker API npipe sigue denegada al agente; no se afirma lectura directa de alembic current o contenedores. Panel5173 inicialmente rechazaba conexión: se inició npm run dev -- --host127.0.0.1 y se observó login en navegador integrado. Vite usa su caché local, sin cambio de código.

Mailpit muestra un mensaje mínimo de caso ficticio; el asunto genérico no demuestra tipo CIERRE. Sin sesión RH no se accedió al seguimiento autenticado ni se modificaron expedientes. Se pidió iniciar sesión en el panel, sin compartir contraseña en chat. Verificación funcional de cierre continúa pendiente; no confundir disponibilidad con aceptación. RNF-2 pendiente y sin otra carga. Registro local hasta completar el recorrido autenticado; publicación previa y CI202 conservados.

## 2026-10-29 — Correo de cierre verificado en el entorno local

[Evidencia204](evidencias/204-correo-cierre-recorrido-local-verificado.json) y [captura206](evidencias/206-correo-cierre-mailpit.jpg). La usuaria inició sesión RH en el navegador integrado; el agente creó únicamente el nuevo caso ficticio «Auditoría RF-5 — cierre ficticio 29-oct-2026», ámbito ENTORNO, sin afectado/participantes/confidencialidad. Clasificación manual de QA Riesgos/Media, revisión con responsable Administrador RH, resolución explícitamente ficticia y cierre. No se solicitó IA. El historial mostró creación, clasificación y tres cambios de estado; no se tocaron casos previos.

El panel mostró estado Cerrada y seis avisos Aceptada por SMTP, cada uno al primer intento: tres creaciones a RH, una asignación, una resolución al reportante y un cierre al mismo reportante (sin afectado en ENTORNO). Mailpit conserva seis mensajes del ID de prueba: tres a las17:09 y tres sucesivos a las17:10. El último muestra solo ID/enlace autorizado, sin título, descripción o resolución. Captura íntegra JPEG guardada e inspeccionada visualmente, hash en204. La atribución de tipo CIERRE proviene del panel; el asunto genérico de Mailpit por sí solo no distingue evento.

La primera captura del panel no pudo guardarse por EPERM y luego hubo interrupciones/pérdida de pestaña. No se inventó ni recreó esa imagen; se conserva observación directa del árbol accesible de la sesión y captura posterior auténtica de Mailpit. No hubo inspección SQL operativa ni prueba nueva negativa de permisos/reapertura/reintentos; esas coberturas automatizadas y límites siguen vigentes. SMTP capturado no demuestra buzón externo/lectura. RF-5 tiene ahora recorrido local básico de creación, asignación, resolución y cierre. RNF-2 continúa pendiente, sin nueva carga. No se cambió código en esta verificación.

## 2026-10-29 — Control SELECT1 real; estadísticas de consultas de negocio preparadas

[Evidencia207](evidencias/207-control-select1-postgresql-real-rnf2-pendiente.json), runee6fcc5a7e8c411e (UTC30-oct/local29-oct): arranque18,51s; diagnóstico5 válido y control DB completo. **286 solicitudes medidas, cero errores HTTP**, conteos100->130->201; SQL201casos/creaciones,96ediciones y2.010entregas, cero SMTP/IA. Diez logout204, postHTTP OK y QA detenido. Reporte original intacto por hash;54hashes de producto coinciden. SQL3/2/9/7, workers3/3/2/2 y cero incompletas conservados.

P95 HTTP ms: listado231,82; detalle207,12; creación363,92; edición289,96: ninguno bajo200. CPUhost74,54%, generador0,84%. Workers creación23,51msCPU frente184,33mstranscurridos; edición14,95CPU/137,03ms. Control después de HTTP: con1conexión5muestras, driver4,370ms/ejecución servidor0,507ms medios; con10conexiones50muestras, driver4,952ms/CPUworker0,665ms, planificación0,02052ms/ejecución0,01944ms medios. P95 driver concurrente8,686ms. No mide consultas reales bajo carga, no restar p95 ni atribuir diferencia a red/IO/GIL/SO/VM únicos. Tampoco permite afirmar que PostgreSQL explique o no explique el coste de negocio. No octava formal; RNF-2 pendiente.

[Evidencia208](evidencias/208-estadisticas-sql-servidor-qa-preparadas.json): opción --server-stats solo smoke diagnóstico, protegida antes de crear recursos. Añade pg_stat_statements/compute_query_id únicamente al PostgreSQL QA nuevo, crea extensión con guard de identidad y toma snapshots sin reset. Deltas por consulta se agregan a familias: llamadas, ejecución/filas y media ponderada; no SQL, parámetros o IDs de consulta en reporte. Detecta reset global/individual por stats_since, desalojo y disminución de contadores. Ventana incluye login/logout, calentamiento, carga y verificación SQL, excluye seed y sondeo SELECT1 posterior. La extensión mantiene textos en su QA privado y añade coste; planning tracking off, sin p95 servidor. No cambia el sitio, Compose operativo, pool, durabilidad ni criterio formal.

**113 unitarias stdlib aprobadas en2,441s**, once nuevas:9helper y2provisionador. Incluyen guard, privacidad, deltas/ponderación, reset/evicción/contadores, configuración solo opt-in, orden alrededor de HTTP/control y parada conservando HTTP/SQL ante fallo posterior. AST4archivos correcto; --plan confirmado sin Docker. Lectores actuales revalidan el reporte real207. No ejecución PG real de208 ni optimización de producto nueva; pendiente un único smoke opcional de estadísticas. No repetir formal sin evidencia/hipótesis nueva.

## 2026-10-29 — CI de herramientas SQL aprobado, perfil real pendiente

[Evidencia209](evidencias/209-ci-control-sql-servidor-aprobado.json): [GitHub Actions Backend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40990308380) sobre3f07628 terminó con tests y postgres-integration SUCCESS. Complementa las113unitarias locales de208. La integración PostgreSQL usa configuración normal del workflow; no ejecuta --server-stats ni demuestra todavía el preload/CREATE EXTENSION/snapshots reales del modo nuevo. Pendiente un único diagnóstico QA con esa opción; no otro full ni carga generada por el agente. RNF-2 sigue pendiente.

## 2026-10-30 — SQL real breve; comparación de capacidad API preparada

[Evidencia210](evidencias/210-sql-servidor-real-breve-latencia-http-pendiente.json), run 3ea817bdffc847fc ejecutado el 29-oct a las 20:23 local (30-oct UTC): arranque de 18,08 s; **269 solicitudes medidas sin errores**, conteos100->130->198. SQL198casos/creaciones,88ediciones y1.980entregas, cero SMTP/IA; post HTTP correcto, diez logout 204 y QA detenido. Diagnóstico 5/sumas de servidor y 54 hashes de producto coincidentes validados; reporte original intacto por hash. P95 listado286,24/detalle233,77/creación340,60/edición303,63ms, todos sobre 200. CPUhost76,06 %, generador 0,84 %. SQL 3/2/9/7 y workers 3/3/2/2.

El nuevo control funcionó realmente:28 familias, 4.160 llamadas y 521,964 ms de ejecución acumulada en su ventana amplia, no solo 5 s HTTP. Cada media por familia menor de 1 ms: autenticación 0,066 ms, advisory 0,0098 ms, INSERT incidencias 0,903 ms e INSERT mail 0,963 ms. La API observa aproximadamente12-29ms por familia SQL durante medición. No restar métricas/ventanas distintas: pg_stat_statements no mide planificación ni todo coste de confirmación, transporte o planificación de CPU. No afirmar causa única GIL/red/VM ni eliminar protección/locks/durabilidad. El resultado orienta a probar capacidad de procesos API; no acredita RNF-2 ni añade formal.

[Evidencia211](evidencias/211-comparacion-uno-dos-procesos-api-preparada.json): --api-workers 2 únicamente en smoke sin diagnóstico. validate_workers rechaza tipo/cuenta/mode inseguros antes de recursos. specification/validate_resolved habilitan comando exacto Uvicorn app.main:app --workers 2 con marcador propio; run comprueba Config.Cmd real del contenedor API y pertenencia de ID antes de migrar, y registra api_workers_declarados/comando_api_workers_verificado. Uno por defecto, Dockerfile/Compose del sitio, código productivo y modo formal permanecen sin cambios. No se mezclan logs de diagnóstico multiproceso ni se afirma reparto por PID.

compare_performance_workers.ps1 exige confirmación QA, ejecuta secuencia 1/2 sin reintentos, cada vez libera dos redes QA elegibles vacías (máximo 4 en total) y crea QA independiente con 10 clientes/100 casos iniciales, smoke de 2 + 5 s sin instrumentos. Si limpieza falla/omite o una prueba queda incompleta, detiene la secuencia. No detiene el sitio ni borra volúmenes/reportes. El pool sigue en 15 por proceso: dos duplican techo teórico API a 30, con más memoria; pendiente medir. Carga de ciclo cerrado puede producir distintos totales/dataset final; una pareja y diferente CPU no prueban causalidad.

**120 unitarias locales aprobadas en 3,309 s**, siete nuevas:5 de configuración/CLI/guardas y 2 del provisionador simulado, incluyendo comando real y parada ante fallo. AST de 3 archivos Python correcto y parser PowerShell sin errores; controlador no ejecutado. Estas pruebas se observaron durante la preparación; no son dos corridas Docker. Pendiente ejecución real y comparación de ambos reportes; no promoción a formal o cambio operativo anticipado.


## 2026-10-30 — Comparación real de uno y dos procesos API

[Evidencia212](evidencias/212-comparacion-real-uno-dos-procesos-api.json): el usuario ejecutó el controlador preparado. Dos QA independientes con diez clientes, cien casos iniciales, calentamiento2s y medición5s, sin diagnóstico. Los54 hashes de producto coinciden entre corridas y con los archivos actuales. Ambos completos, cero errores HTTP en calentamiento/medición, conteos SQL coherentes, diez logout204, post HTTP correcto y QA detenido. El comando de dos procesos está verificado; no acredita reparto por PID.

P95 en ms (uno → dos): listado252,57→90,79; detalle202,21→114,17; creación290,63→163,91; actualización249,18→153,28. Solicitudes medidas339→583. Conteos100→121→204 y100→145→290; SQL204/290 creaciones,100/182 ediciones y2.040/2.900 entregas, sin SMTP/IA. Los cuatro p95 de dos procesos están por debajo de200ms únicamente en este smoke. Resultado favorable para investigar capacidad multiproceso; RNF-2 continúa pendiente y no hay nueva prueba formal.

No hay CPU global registrada en este modo. Muestras Docker escasas y en ventanas diferentes, incluida una posterior a medición con dos procesos: no atribuir la mejora a una causa única ni comparar sus porcentajes como medias. La memoria API muestreada aumenta aproximadamente de78–85MiB a170–192MiB; no son máximos continuos. Pareja secuencial y conjunto final distinto no eliminan variación del host/sesgo de orden. Mantener configuración del sitio y formal actual; preparar validación sostenida reproducible antes de adoptar dos procesos, conservando diez clientes, p95<200ms y controles de integridad.

Archivos cambiados: evidencia212 y documentación de seguimiento. Validación: lectura de ambos originales, SHA256,54 hashes, fases completas, errores, sumas HTTP/SQL, logout y parada. No se ejecutó carga adicional ni se modificó código productivo.


## 2026-10-30 — Validación formal QA con dos procesos preparada

[Evidencia213](evidencias/213-formal-qa-dos-procesos-preparada.json). A partir de la comparación real212 favorable y a petición de cerrar RNF-2 para entrega, se habilita `--api-workers 2` en QA formal sin diagnóstico. Sustituye la restricción histórica de211 que permitía dos solo en smoke. El guard conserva un proceso por defecto, valida el número antes de CPU/Docker y registra la selección en precondiciones. Verifica CPU previa, libera hasta dos redes QA elegibles, y provisiona un proyecto nuevo; el provisionador mantiene validación de ID propio y comando Uvicorn real. Dos procesos con diagnóstico siguen rechazados. Sitio/Dockerfile/Compose operativo, pool15 por proceso, locks, transacciones y runner/verdict intactos.

**Protocolo sin rebajar:** diez clientes, cien casos iniciales,30s calentamiento y300s medición; cada p95 de listado/detalle/creación/actualización estrictamente menor de200ms, sin errores y con verificaciones HTTP/SQL/logout/parada. CPU previa: media≤30% y cada intervalo≤50%; si no cumple, no inicia carga. No detener automáticamente servicios ajenos ni desactivar protecciones.

Comando desde raíz, con Docker abierto:

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/run_performance_full_guarded.py --api-workers 2 --confirm-isolated-qa
```

Validación realizada:126 pruebas de herramientas aprobadas en4,827s, AST de cinco archivos correcto; se comprobó que runner y configuración productiva no cambiaron frente a la versión publicada. Nuevas pruebas cubren selección full2 en CLI, rechazo de diagnóstico, guardas CPU/redes no eludibles, validación anticipada y despacho full sin convertirlo en smoke; resultado FALLIDA_UMBRAL simulado conserva fallo y parada. No se ejecutó carga Docker desde el agente. Pendiente corrida real del usuario, lectura íntegra del original y acreditación únicamente si cumple. Siete fallos formales anteriores siguen documentados; aún no hay octava formal. Dos procesos aumentan memoria y techo API a30 conexiones. Un éxito futuro solo acredita el alcance y hardware declarados, no rendimiento universal ni proveedores externos.

Archivos: provision_performance_qa.py, run_performance_full_guarded.py y tres pruebas relacionadas; evidencia213 y documentación de seguimiento. No se afirma RNF-2 listo antes de observar la ejecución real.


## 2026-10-30 — Octava formal: lecturas cumplen, escrituras pendientes; candidato QA3

[Evidencia214](evidencias/214-formal-dos-procesos-fallo-escrituras.json), run342970ed6e004063: formal30+300s/diez clientes y comando real de dos procesos verificado.54 hashes de producto actuales coinciden.27.722 solicitudes medidas, cero errores en ambas fases. P95 listado160,12/detalle156,67ms cumplen; creación264,38/actualización227,96ms incumplen200ms. Conteos100→548→7.479; SQL7.479CREADO,7.368EDITADO,74.790entregas, ceroSMTP/IA. Post HTTP correcto, diez logout204 y QA detenido. **FALLIDA_UMBRAL: RNF-2 sigue pendiente.** La CPU previa20,37% permitió iniciar;50 muestras Docker no son CPU global ni diagnóstico por operación. No atribuir el fallo exclusivamente al host ni ignorarlo. Original preservado por hash.

[Evidencia215](evidencias/215-formal-tres-procesos-candidato.json): se amplía la selección explícita a1/2/3 procesos solo QA sin diagnóstico multiproceso, conservando default1 y comportamiento2. Comando y marcador3 deben coincidir en configuración y en contenedor propio. CLI del guard y provisionador admiten3; permanece protocolo30+300s/diez clientes/p95<200ms, umbrales CPU, limpieza2redes, identidad de recursos y controles de integridad. Runner/producto/Dockerfile/pool/locks/durabilidad intactos. Tercero es candidato a medir, no mejora demostrada; equipo4CPU lógicas también necesita capacidad para PostgreSQL/Windows y pool máximo API aumenta a45. No modificar configuración del sitio ni declarar cumplimiento antes de la evidencia real.

**Validación:**130 pruebas de herramientas aprobadas en4,471s y AST5 archivos correcto. Primera ejecución encontró5fallos/5errores por variable fuera de alcance en validación del comando; se corrigió para usar marcador validado y la suite completa pasó. Pruebas nuevas cubren CLI3, marcador/comando incoherentes, diagnóstico rechazado, guardCPU no eludible, despacho full real simulado, veredictos aprobado/fallido conservados y parada antes de migración si comando inválido. Sin Docker real ejecutado por agente. Archivos: dos scripts y tres pruebas, evidencias214/215 y documentación. Pendiente una única formal QA3 del usuario y revisión del original; no reintentos automáticos ni más procesos.

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/run_performance_full_guarded.py --api-workers 3 --confirm-isolated-qa
```


## 2026-10-30 — Novena formal: solo creación incumple; una consulta menos en outbox nuevo

[Evidencia216](evidencias/216-formal-tres-procesos-fallo-creacion.json),run85395e3b50fc4f8d: QA3 verificado, diez clientes/30+300s,54 hashes coincidentes con versión publicada previa.34.027 solicitudes medidas sin errores en ambas fases. P95 listado125,63/detalle119,11/actualización173,60ms cumplen; **creación202,6812ms incumple p95<200ms**. No redondear ni elevar umbral. Conteos100→944→9.449; SQL9.449CREADO,9.342EDITADO,94.490entregas, ceroSMTP/IA. Post HTTP correcto,diez logout204 y QA detenido. Noveno fallo formal conservado; RNF-2 sigue pendiente. Comparación con2procesos es favorable en los cuatro p95 y throughput, pero host/orden/dataset difieren; no prueba causalidad única. La preparación previa de3procesos pasó CIBackend41133946635; no es esta optimización.

[Evidencia217](evidencias/217-outbox-evento-nuevo-sin-lectura-redundante.json): queue_event inspecciona estado ORM antes de flush. Solo un evento pendiente en la misma Session y con ID todavía None evita SELECT mail_deliveries: no puede tener entregas previas antes de existir; el flush debe generar su ID e insertarlo correctamente. Eventos ya persistentes, reencolados o con ID explícito conservan consulta y deduplicación. No se añade indicador público ni cache de datos/permisos. Mantiene destinatarios autorizados, contexto, IDs deterministas, constraint, INSERT multivalores cacheable, flush/transacción/commit/rollback, locks y durabilidad. El código consumidor no cambia su contrato ni ejecuta SMTP durante petición. Fuente de estados ORM: [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/session_state_management.html).

**Validación local real:**30 pruebas sin HTTP aprobadas en2,522s y AST3 archivos correcto. Tres nuevas cubren evento pendiente sin ID sin búsqueda, replay con búsqueda/IDs únicos y rollback; evento con ID explícito en ruta conservadora; omisión por cero destinatarios y repetición sin duplicados. Las anteriores cubren123destinatarios en3lotes, caché sin mezclar eventos y rollback completo al fallar segundo lote durante create_case. Consultas directas SQLite con mismo departamento7→6 y otro8→7; mantienen permisos y ceroSQL postcommit. No es medición PostgreSQL ni latencia HTTP; ahorro equivalente de una consulta en QA pendiente de observar, no afirmar p95 alcanzado. Runner, guard, protocolo, número3 del candidato, Dockerfile, pool y sitio intactos; no cuarto proceso ni relajación de200ms. Pendiente CIbackend/PostgreSQL y una única formal con código nuevo. Archivos: mail.py y dos pruebas; evidencias216/217 y documentación.

Comando después de las validaciones, con Docker abierto y entorno normal detenido:

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/run_performance_full_guarded.py --api-workers 3 --confirm-isolated-qa
```


## 2026-10-30 — Décima formal falla en las cuatro operaciones; CPU pasiva por fase

[Evidencia218](evidencias/218-decima-formal-fallida-cuatro-operaciones.json),runf756ceeff8384365: QA3 verificado, diez clientes/30+300s,54 hashes de producto coincidentes con fuente actual/publicada, incluyendo outbox217.24.450 solicitudes medidas sin errores. P95 listado209,73/detalle200,83/creación328,30/actualización289,47ms: **las cuatro incumplen p95<200ms; décima formal FALLIDA_UMBRAL y RNF-2 pendiente**. Conteos100→527→6.639; SQL6.639CREADO,6.528EDITADO,66.390entregas, ceroSMTP/IA. Post HTTP correcto,diez logout204 y QA detenido. El ahorro de consulta no bastó para aprobar; sin A/B controlado no demuestra que cause el empeoramiento ni que solo sea culpa del equipo. CPU previa25,48% no describe los cinco minutos; este reporte aún no tiene CPU Windows/generador por fase. Original intacto por hash. CI del cambio217 pasó backend/PostgreSQL41153543326, no acredita RNF-2.

[Evidencia219](evidencias/219-cpu-pasiva-por-fase-formal.json): detener ajustes de negocio sin más evidencia; phase_run captura dos host_stamp por fase, en la barrera inicial y al terminar workers, y host_summary añade cpu_generador_host también sin diagnóstico. Cuatro lecturas en calentamiento+medición; ninguna por petición. Antes solo se emitía con diagnóstico. Conserva null/NO_DISPONIBLE si falta lectura; no habilita cabeceras/perfil API ni diagnóstico multiproceso. No cambia API, outbox217, locks/pools/durabilidad, guardas CPU previa/redes, configuración normal, tres procesos del candidato ni veredicto. CPU de carga se observa sin ser nuevo criterio de aprobación ni excusa automática para descartar un fallo. Host incluye propia carga y otras apps/VM; no atribuir causa única ni restar porcentajes de intervalos distintos. Incluye drenaje final, no preflight/login/logout; son medias, no serie de picos. Pequeño coste adicional de cuatro lecturas del generador no medido, declarado.

**Validación:**132 pruebas de herramientas aprobadas en4,612s, dos nuevas para emisión sin diagnóstico/API y host ausente como null; AST2archivos correcto. Suite anterior conserva veredictos, protocolo, guardas y configuraciones1/2/3. Código producto idéntico a217; no se incrementa a4procesos ni se promete mejora por añadir medición. Pendiente CI y nueva medición real con CPU durante fases antes de decidir otra optimización. Archivos: performance_runner.py/test_performance_runner.py,evidencias218/219 y seguimiento. La nueva observación no está incluida retrospectivamente en218.


## 2026-10-30 — RNF-2 cumplido en alcance HTTP QA local de tres procesos

[Evidencia 220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json),run52326520485242bf: **APROBADA_ALCANCE_HTTP_QA**, undécima formal completa y primera aprobada. Diez clientes distintos/cien casos iniciales,30 s de calentamiento y300 s medidos; comando realAPI de 3 procesos verificado,sin diagnóstico API y con CPU pasiva219.54 hashes de producto coinciden con fuente actual/publicada; incluye217. **35.216 solicitudes medidas sin errores**, tampoco hubo errores en calentamiento. P95 listado123,81/detalle113,27/creación194,04/actualización167,77ms: las cuatro estrictamente por debajo de200 ms, criterioPRD sin modificación. P99 y algunos máximos mayores de200 ms no se presentan como latencia de todas las peticiones.

Conteos100→1.021→9.825; SQL 9.825 casos/CREADO,9.719 EDITADO y98.250 entregas encoladas, cero SMTP/IA. Post HTTP correcto,diez logout 204 y QA detenido. Verificados sumas y original porSHA256, no modificado. Windows4 CPU lógicas,Docker4 CPU/3,512GiB; generador mismo equipo. CPU medida de faseWindows 89,74 %,generador 1,78 %normalizado por equipo; no es causa única ni nuevo criterio de fallo. CPU previa 13,61 %. Creación tiene margen de 5,962 ms: una aprobación real, no repetibilidad universal ni aprobación institucional. Los diez fallos previos permanecen intactos. RNF-2 queda acreditado en este protocolo/configuración/hardware local y excluye tiempos de proveedores externos; no certificar instalaciónbase1 proceso u otros equipos/cargas.

[Evidencia 221](evidencias/221-perfil-compose-rnf2-reproducible.json): compose.rnf2.yaml opcional fija comando API3 idéntico al validado. Compose config del base y base+override comparados en memoria: diferencia única comando API; commandnull del base normalizado en comparación. Sin daemon/arranque operativo ni secretos impresos. No cambia base,puertos,credenciales,volúmenes,workers/perfiles IA/correo. TechoAPI de 45 conexiones por tres pools de 15 conexiones y mayor memoria; el perfil replica cantidad de procesos, no fixture/configuración exactaQA. No arrancado por el agente. Documentación actualizada en guía principal,manual técnico,MVP,backlog,entregables,trazabilidad,QA y protocolo. No ejecutar otro full para aumentar evidencias. Revalidar ante cambios de producto/configuración/hardware relevantes.

Validación de esta entrega: lectura completa de reporte real,54 hashes,comando3,fases completas/10 clientes/30+300s,cuatro p95,errores/sumas HTTP/SQL,logout/parada yconfigCompose local. CI previo de 219: Backend/PostgreSQL 41165580804 SUCCESS,132 unitarias previas; no sustituyen aprobación real220. Sin cambio de código productivo/harness en esta entrega. Otros pendientes de aceptación integral,capacitación,recuperación o privacidad no se cierran por este resultado.


## 2026-10-30 — Aceptación de entrega agrupada: siguiente recorrido de departamentos

[Evidencia222](evidencias/222-matriz-aceptacion-entrega-preparada.json) y [matriz](ACEPTACION_ENTREGA.md):14 escenarios separan pruebas automáticas, recorridos previos parciales y aceptación pendiente. RNF-2 aprobado220 no se repite. Se prepara recorrido D01–D08 con Admin RH: departamento nuevo ficticio y vacío, duplicado rechazado, renombrado, baja/reactivación y baja final; cinco eventos exitosos esperados, sin borrar ni afectar departamentos usados. El plan no acredita la ejecución ni aceptación institucional.

Validación: enlaces locales de la matriz comprobados y cinco nombres de pruebas de departamentos contra fuente; lectura de UI confirma campos, controles e historial. Panel5173 respondió200; API8000/health/db no accesible en esa muestra. No arrancado Docker por agente ni nuevas escrituras; siguiente paso requiere arranque del operador con compose.rnf2.yaml/perfilmail, migración/check existentes y sesión Admin RH introducida solo en panel. Documento incluye comandos y registro sanitizado de resultados. No ejecutados tests repetidos ni creados usuarios/departamentos. Sin cambios de aplicación. Pendientes de custodia, recuperaciónDocker, matriz completa, manual/capacitación y aceptación humana se conservan.

Archivos: ACEPTACION_ENTREGA.md, evidencia222 y enlaces/seguimiento en backlog,entregables,trazabilidad,MVP,QA e índice documental.
