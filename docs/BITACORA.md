# Bitácora de desarrollo



## 15 de octubre de 2026 — Base inicial y documentación académica



**Propósito:** iniciar el proyecto y organizar evidencia conforme a las diez actividades del anteproyecto.



**Avances realizados:**



- Se creó el repositorio local con PRD 1.6, README, backlog, .gitignore y .env.example: commit f5fe074.

- Se creó la estructura de backend, frontend e infraestructura: commit 5d0b8b1.

- La autora ejecutó git push; la captura compartida confirma publicación de main y vinculación a origin/main. La autenticación desde el entorno del asistente había fallado; no se atribuye al asistente esa subida.

- Se revisó la sección 7 del descriptivo y se añadió matriz de entregables, trazabilidad inicial y reglas de documentación continua.



**Validación:** lectura de los archivos y del PDF fuente; revisión del estado e historial local de Git. En la preparación inicial se comprobó que .env queda ignorado. No se leyó ni publicó su contenido.



**Resultado:** documentación y estructura inicial disponibles. No existe todavía un sistema funcional ni pruebas de aplicación ejecutadas.



**Pendientes:** API inicial, dependencias reproducibles, arquitectura, modelos de datos y autenticación. Definir Azure OpenAI Service frente a API de OpenAI antes de la integración.



## Formato para siguientes entradas



- Fecha real y nombre del avance.

- Propósito y requisito/actividad relacionada.

- Cambios y evidencia identificable.

- Validación ejecutada, resultado y limitaciones.

- Estado de entregables, pendientes y referencia del commit cuando esté disponible.



## 15 de octubre de 2026 — Selección del proveedor de IA



**Propósito:** resolver la diferencia entre el descriptivo y el PRD.



**Cambio:** la autora seleccionó la API directa de OpenAI mediante la captura compartida. Se actualizaron DECISIONES.md, ENTREGABLES.md, BACKLOG.md y TRAZABILIDAD.md. El PRD ya identifica ese proveedor y no requiere cambiar por esta decisión.



**Validación:** comprobación de coherencia documental y de la variable OPENAI_API_KEY en .env.example. No se leyó .env ni se probaron credenciales o servicios externos.



**Resultado:** proveedor definido; no hay integración ejecutada.



**Pendientes:** implementar backend, seleccionar modelo, configurar credenciales localmente y probar con datos simulados.



## 15 de octubre de 2026 — Primera API ejecutable



**Propósito:** iniciar la fase de desarrollo con una base verificable de FastAPI, sin exponer datos de negocio.



**Cambios:** fábrica de aplicación, endpoint /health tipado, documentación OpenAPI y /docs, entorno virtual local, dependencias fijadas, tres pruebas y workflow CI. Se actualizaron README, instrucciones de backend, manual técnico, backlog, matriz de entregables, trazabilidad y decisiones.



**Validación:** tres pruebas ASGI aprobadas; pip check sin conflictos; Uvicorn inició correctamente. La consulta de loopback entre procesos agotó el tiempo de conexión. Se registra como no verificada. Advertencia de deprecación de TestClient documentada. .env y .venv continúan ignorados. Ver REPORTE_QA.md.



**Resultado:** API inicial disponible como código ejecutable con instrucciones. Servidor de comprobación detenido al terminar. La CI está preparada, pero su ejecución remota no está confirmada.



**Pendientes:** cliente React, Docker Compose, PostgreSQL/Redis, modelos y migraciones, autenticación, flujos de incidencias e integraciones. No se realizaron llamadas a OpenAI ni se modificó .env.



## 15 de octubre de 2026 — Entorno de contenedores



**Propósito:** preparar ejecución local conjunta de API, PostgreSQL y Redis, como base para persistencia.



**Cambios:** compose.yaml en la raíz, Dockerfile y .dockerignore del backend, instrucciones en infra/README.md, variable opcional API_PORT, guía de evidencias y actualización de manual, backlog y trazabilidad. .env no se leyó ni modificó.



**Validación:** revisión estática de rutas de construcción, comandos, variables, healthchecks, volúmenes y publicación exclusiva en loopback para API. git diff --check. Docker no está disponible; no se ejecutaron build, compose config ni contenedores. Los parsers YAML consultados tampoco están instalados; no se afirma validación sintáctica automática.



**Resultado:** configuración preparada y documentada, ejecución pendiente. No se considera probada la integración de servicios.



**Pendientes:** instalar/iniciar Docker Desktop, completar contraseña local, ejecutar comprobaciones documentadas y conservar evidencia. Después implementar modelos, migraciones y acceso real a datos.



## 15 de octubre de 2026 — Inventario de herramientas



**Propósito:** identificar instalaciones necesarias antes de ejecutar Compose.

**Validación:** comandos de ubicación y versión: Git, VS Code, Python 3.11.0, Node 24.13.1 y npm 11.8.0 disponibles. Docker ausente. WSL y listado de aplicaciones Store no pudieron verificarse por acceso denegado. Power BI no localizado en rutas habituales.

**Resultado:** inventario en HERRAMIENTAS.md; sin instalaciones ni cambios al sistema. Pendiente Docker Desktop y comprobación manual de WSL 2. Power BI puede prepararse posteriormente.



## 15 de octubre de 2026 — Evidencia de servicios locales



**Propósito:** documentar las comprobaciones manuales de infraestructura realizadas por la autora.

**Cambios:** cuatro capturas incorporadas a docs/evidencias, índice actualizado y resultados vinculados en REPORTE_QA.md. Se actualiza el estado de infraestructura en backlog y entregables.

**Validación:** inspección visual de HTTP 200, servicios healthy, SELECT 1 y PONG. No se observaron credenciales en las capturas. No se ejecutaron nuevas pruebas de servicios desde el asistente.

**Resultado:** arranque básico de contenedores y respuestas de servicios acreditados por evidencia manual.

**Pendientes:** esquema de datos, migraciones y conexión real desde FastAPI; pruebas de persistencia y permisos.



## 15 de octubre de 2026 — Modelos y primera migración



**Propósito:** iniciar persistencia conforme al PRD, separando disponibilidad HTTP y disponibilidad de base de datos.

**Cambios:** SQLAlchemy, Psycopg y Alembic; siete modelos; migración 0001 con tres roles y cinco categorías; conexión diferida; /health/db; inclusión de migraciones en imagen; documentación DATOS.md y CI PostgreSQL. No se cargaron credenciales reales ni se modificó .env.

**Validación:** ocho pruebas aprobadas, dos de integración omitidas; una advertencia de TestClient ya conocida. pip check sin conflictos. Alembic upgrade head --sql generado sin credenciales. Se corrigió path_separator para soportar rutas Windows con espacios. Docker localizado en instalación por usuario; acceso al pipe del motor denegado en este entorno.

**Resultado:** modelos, migración y endpoint implementados. Migración real aún no aplicada por el asistente; CI remota pendiente.

**Pendientes:** aplicar upgrade head desde terminal autorizada, comprobar alembic check y GET /health/db; después usuarios simulados, autenticación y flujos de incidencias.



## 15 de octubre de 2026 — Evidencias de migración y usuarios simulados



**Propósito:** cerrar la evidencia de conexión y preparar datos para pruebas de roles.

**Cambios:** capturas 05/06 verificadas y extensión PNG corregida; comando app.seed_demo con confirmación explícita; dos departamentos y seis usuarios ficticios; guía DATOS_DEMO.md y seguimiento actualizado.

**Validación:** tres pruebas nuevas de fixtures aprobadas en SQLite (repetición y conservación de bajas, roles ausentes y reversión). La suite completa se intentó ejecutar, pero se bloqueó en la prueba ASGI existente test_health_contract; se interrumpió sin atribuirle éxito. La ejecución detallada confirmó ese punto de bloqueo. No se cambió código HTTP en este avance.

**Resultado:** evidencias manuales de migración y conexión documentadas; carga DEMO implementada. No se ejecutó la carga PostgreSQL desde el asistente.

**Pendientes:** ejecutar carga en terminal de la autora, obtener evidencia 07, revisar bloqueo local de TestClient y validar suite en CI. Autenticación Entra y diez incidencias simuladas pendientes.



## 15 de octubre de 2026 — Validación manual de fixtures DEMO



**Propósito:** registrar carga inicial y repetición de datos simulados.

**Cambios:** evidencias 07 y 08 incorporadas; reporte QA, índice, backlog, entregables y trazabilidad actualizados.

**Validación:** inspección visual de 2 departamentos y 6 usuarios creados; segunda ejecución con contadores 0/0. Comandos ejecutados por la autora en Docker; no por el asistente.

**Resultado:** carga PostgreSQL y repetición sin duplicados acreditadas mediante evidencia manual.

**Pendientes:** autenticación Entra ID, diez incidencias ficticias y revisión del bloqueo de la suite HTTP. No se considera terminado el MVP ni la autenticación por tener usuarios DEMO.



## 15 de octubre de 2026 — Autenticación local



**Propósito:** sustituir la dependencia de Entra ID, por decisión explícita de la autora, conservando roles y datos.

**Cambios:** PRD 1.7; credenciales Argon2id; sesiones revocables con digest; migración 0002; login, me, logout, cambio de contraseña y alta restringida; bootstrap/restablecimiento interactivos. Variables Entra retiradas de la plantilla sin modificar .env. Guía AUTENTICACION.md y trazabilidad actualizadas.

**Validación:** suite completa: 20 passed, 2 skipped, 1 warning en 12.72 segundos. Incluye hash Argon2id, normalización, rechazo genérico, bloqueo de intentos, expiración, logout, cuenta inactiva, revocación al cambiar contraseña, permisos de alta y redacción de secretos en errores HTTP. Se corrigió uso inicial incompatible de la API de pwdlib mediante verify_and_update. pip check sin conflictos y migración offline generada.

**Resultado:** API 0.3.0 implementada; suite local completada, superando el bloqueo observado en el avance anterior. No se ejecutó migración 0002 ni login real en PostgreSQL desde el asistente.

**Pendientes:** aplicar 0002 en Docker, provisionar primer administrador y verificar manualmente login/me/logout. CI remota no confirmada. Interfaz React, gestión completa de usuarios, incidencias y recuperación por correo pendientes.



## 15 de octubre de 2026 — Revisión integral del PRD



**Propósito:** resolver inconsistencias de la revisión externa y consolidar una fuente única de requisitos.

**Cambios:** PRD 1.8 reestructurado, RF-7/RF-8, reglas de ámbito, revalidación, conflicto de interés, privacidad IA y evaluación; modelo objetivo integrado; backlog y trazabilidad reescritos como estado vigente; README identifica Word histórico.

**Validación:** revisión documental de IDs, enlaces relativos, reglas y referencias cruzadas; diferencias con esquema actual declaradas. No se modifica código ni base y no se vuelven a ejecutar pruebas funcionales por este cambio documental.

**Resultado:** requisitos consistentes como objetivo de desarrollo; funciones nuevas siguen pendientes.

**Pendientes:** fecha límite y horas disponibles para calendarizar; validación real de autenticación 0002; diseño e implementación de migración/servicios del nuevo alcance de incidencias.


## 15 de octubre de 2026 — Revisión documental 1.9 preparada

**Propósito:** resolver observaciones finales de la revisión externa sin añadir módulos nuevos.
**Cambios:** PRD 1.9, backlog, trazabilidad AC-11 a AC-16, decisiones y README; restricciones preventivas revisables, privacidad de agregados, límites de confidencialidad, exclusión de testigos, prioridades y corrección de evidencia IA no ejecutada.
**Validación:** comprobaciones documentales de identificadores y consistencia; sin ejecutar pruebas de aplicación ni modificar esquema.
**Resultado:** paquete preparado en la carpeta de outputs del chat. El repositorio original no se modificó desde esta sesión porque está fuera de sus raíces de escritura. Los documentos quedan aplicados al repositorio solo cuando la autora los incorpore. No se creó commit desde esta sesión.
**Pendientes:** incorporar documentos y hacer commit; procedimientos de participantes/administrador independiente, vistas de privacidad y demás reglas nuevas siguen pendientes de código.

## 16 de octubre de 2026 — Migración de incidencias

**Propósito:** preparar esquema PRD 1.9 conservando datos existentes.
**Cambios:** 0003, modelos de ámbito/participantes/revalidación/control IA; API 0.4.0 y readiness 0003; pruebas y documentación actualizados. Se conserva el historial de migraciones y se integra evidencia de autenticación previa. Captura 10 corregida usando copia determinística redactada, descartando la vista previa alterada.
**Validación:** 34 pruebas aprobadas, 3 PostgreSQL omitidas, 1 advertencia; pip check sin conflictos; SQL offline compilado. Revisión documental y diff sin espacios accidentales. Sin cambios a .env ni datos del motor Docker.
**Resultado:** estructura implementada; aplicación real 0003 pendiente. Endpoints, autorización por expediente, auditoría transaccional de casos, recusa e IA siguen pendientes de servicios.
**Pendientes:** aplicar 0003, verificar revision/alineación y health/db; conservar evidencias 12/13. Después implementar servicios protegidos y registro auditado.

## 16 de octubre de 2026 — Evidencias 12 y 13

**Propósito:** registrar la verificación manual de la migración 0003.
**Cambio:** evidencias enlazadas al QA y estado de backlog/trazabilidad actualizado.
**Validación:** inspección de revisión 0003, esquema sin cambios pendientes y GET /health/db HTTP 200. Ejecución realizada por la autora.
**Resultado:** migración y conexión real acreditadas. Sin nuevas pruebas funcionales ejecutadas en este avance.
**Pendientes:** servicios de autorización por expediente, creación/consulta auditadas y pruebas entre roles y departamentos. Las tres pruebas automáticas PostgreSQL siguen sin resultado observado.

## 16 de octubre de 2026 — Registro y lectura protegidos

**Propósito:** comenzar gestión funcional de casos conforme al PRD 1.9.
**Cambios:** API 0.5.0; POST/GET /incidents, opciones, detalle, participantes e historial; autorización SQL común por rol/ámbito/conflicto, acuse seguro y auditoría transaccional. Guía INCIDENCIAS.md y seguimiento actualizados. Sin cambios a .env, esquema o cuentas.
**Validación:** 45 pruebas aprobadas, 3 PostgreSQL omitidas, 1 advertencia; pip check sin conflictos. Once casos nuevos comprueban acceso y rollback. Pruebas SQLite/HTTP con identidades simuladas; no se ejecutaron comandos Docker desde el asistente.
**Resultado:** registro/listados/detalle backend parcial implementado. Validación manual PostgreSQL de endpoints pendiente.
**Pendientes:** reconstruir imagen y obtener evidencias 14/15. Luego validación/edición, asignación y transiciones auditadas; API completa de administración y frontend pendientes.

## 16 de octubre de 2026 — Evidencias de registro y listado

Propósito: verificar el primer registro de caso con PostgreSQL. Cambios: incorporación de evidencias 14/15 y actualización del seguimiento documental. Validación: inspección visual de POST con HTTP 201, received=true y can_view=true; GET con HTTP 200 y el mismo ID, título Ausencia simulada, estado PENDIENTE y total=1. Ejecución manual realizada por la autora. No se observan credenciales en estas capturas. Resultado: registro y listado básicos acreditados; sin ejecutar nuevamente pruebas automáticas. Pendientes: detalle/historial manuales, validación, asignación y transiciones, revisión de participantes, frontend e integraciones.

## 16 de octubre de 2026 — Historial manual verificado

Se inspeccionó docs/evidencias/16-historial-incidencia-200.png, ejecutada y guardada por la autora. HTTP 200, evento CREADO, total=1 y detalle de Ausencia simulada con datos ficticios. No se observan token ni Curl. Se documenta lectura básica del historial para el gestor autenticado; no acredita permisos de otros roles, detalle individual ni el ciclo completo. Sin cambios de código ni nueva ejecución automática. Pendientes: clasificación humana, asignación, transiciones auditadas y revisión de participantes.

## 16 de octubre de 2026 — Gestión API 0.6.0

Propósito: implementar clasificación humana, asignación y ciclo auditado. Cambios: services/lifecycle.py, esquemas/rutas en api/incidents.py y versión 0.6.0; edición invalida clasificación y reapertura conserva ciclo previo. Manuales, decisiones y seguimiento actualizados. Validación final: 51 passed, 3 skipped, 1 warning in 11.14s; pip check sin conflictos. Seis pruebas nuevas HTTP/SQLite con identidad simulada, sin ejecutar Docker ni modificar .env. Resultado: gestión backend parcial implementada; no acredita concurrencia real PostgreSQL ni prueba manual nueva. Pendientes: reconstrucción y evidencias 17/18; revisión de participantes/confidencialidad, retroceso protector, frontend y demás integraciones.

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

## 16 de octubre de 2026 — Protección de expedientes API 0.7.0

Propósito: implementar revisión independiente y recusa. Cambios: services/protection.py, tres rutas/esquemas protegidos, API 0.7.0 y ocho pruebas nuevas; manuales, PRD, decisiones y seguimiento. Alta de participantes, revisión con motivo y original conservado; confidencialidad automática/expresa, omisión IA, reasignación atómica o retroceso protector si no hay RH elegible. Respuesta mínima si actor pierde acceso. Validación final: 59 passed, 3 skipped, 1 warning in 13.60s; pip check sin conflictos. Primera ejecución de seis pruebas nuevas: 57 aprobadas; se añadieron reasignación expresa/afectado gestor y límite/inactivos, repitiendo suite. SQLite/HTTP con identidad de prueba; sin comandos Docker ejecutados desde asistente. Resultado: backend parcial implementado, sin nueva migración ni cambios a .env. Pendientes: prueba manual 0.7.0/evidencia 24, concurrencia PostgreSQL, provisión adicional por operador y gestión de cambios administrativos, frontend/IA/correo/analítica.

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

## 16 de octubre de 2026 — Procedimiento de RH independiente preparado

Propósito: atender casos sin RH independiente disponible. Se preparó actualización del CLI con provision-independent-admin, motivo obligatorio, contraseña privada, cuenta nueva y auditoría atómica. Validación en copia aislada: 24 passed in 4.39s (siete nuevas de CLI y regresiones de esquema/seed); pip check sin conflictos. Se probaron rechazo de correo existente, primer bootstrap exclusivo, motivo, departamento inactivo, rollback de alta/credencial/departamento, contraseña no mostrada y conservación de exclusión/asignación del caso. La suite completa y una selección que incluía pruebas HTTP fueron interrumpidas al bloquearse sin resultado final; no se dan por aprobadas. No se ejecutó CLI contra Docker ni PostgreSQL; bloqueo concurrente y validación manual pendientes. La carpeta del proyecto es de solo lectura en esta sesión: paquete preparado, no aplicado al repositorio y sin commit. El script de aplicación verifica hashes previos y conserva respaldos. No se modifica .env ni datos reales. La cuenta nueva no garantiza por sí sola independencia humana; el operador debe designar a otra persona autorizada, limitación documentada.
Pendientes: aplicar paquete, reconstruir, prueba manual y suite completa en entorno habilitado.

## 16 de octubre de 2026 — Aplicación reportada y prueba de RH independiente

Propósito: consolidar procedimiento y evidencias de acceso. Cambios: incorporar registro detallado de revisión, actualizar seguimiento y enlaces. La autora reportó aplicación del paquete, reconstrucción Docker y creación de RH Independiente Demo. Evidencias 34–37 inspeccionadas: 34 acredita sesión HTTP 200 ADMIN_RH de la cuenta nueva; 35 acuse HTTP 201; 36 detalle HTTP 200 del nuevo caso confidencial con el administrador original como afectado, PENDIENTE, IA OMITIDA y sin responsable; 37 muestra 404 Incidencia no encontrada, tras cambio de sesión reportado por la autora. El recorte 37 no muestra ID consultado ni identidad del solicitante: por sí solo no distingue exclusión de un ID inexistente; se documenta en conjunto con el recorrido reportado y las pruebas automáticas previas, sin exagerar la evidencia. No se observaron contraseñas ni tokens. El caso original y la asignación no se alteraron por provisionar la cuenta. Las cuentas distintas no garantizan independencia humana: el operador debe designar otra persona autorizada. No se ejecutaron pruebas automáticas nuevas en esta revisión; siguen vigentes las 24 pruebas seleccionadas de CLI/esquema/seed aprobadas en copia y la suite HTTP completa sin resultado final de esta sesión. Concurrencia real PostgreSQL, auditoría del alta en motor real y matriz completa de permisos siguen pendientes.
Esta entrada complementa los registros de preparación anteriores: aplicación reportada y prueba manual realizadas después. Actualización documental y commit preparados fuera del repositorio; se materializan al ejecutar REGISTRAR_Y_COMMIT.ps1.

## 16 de octubre de 2026 — Administración de usuarios preparada

Propósito: mantener autorización al cambiar cuentas. Cambios: servicios/rutas/gate y once pruebas nuevas; manuales, decisiones y seguimiento. API 0.8.0 preparada en copia aislada, esquema 0003 sin migración. GET /users/options y /users; PUT /users/{id} auditado, con rol/departamento/activación, revocación y protección de asignaciones. Bloqueo advisory compartido/exclusivo coordina mutaciones administrativas e incidencias. 35 pruebas seleccionadas aprobadas en 6.50s; primera ejecución 1 fallida/32 aprobadas por caché del fixture, corregida comprobando datos persistidos y refrescando la entidad. No se ejecutó suite HTTP completa ni concurrencia PostgreSQL. El paquete no está aplicado; no hay commit/push. No se modificó .env ni datos reales. Validación manual, frontend y administración de departamentos pendientes. Guía y límites en ADMIN_USUARIOS.md.

## 16 de octubre de 2026 — Administración aplicada y evidencia consolidada

Propósito: conservar implementación y validación del avance. Cambios: actualización de seguimiento, guía y registro REVISION_ADMIN_USUARIOS.md con evidencias 38–46. API 0.8.0 aplicada y reconstruida según reporte de la autora; evidencia 38 inspeccionada confirma suite completa ejecutada por ella: 77 passed, 3 skipped, 1 warning in 16.49s. Las tres omitidas son las integraciones PostgreSQL optativas y no se declaran aprobadas; advertencia conocida de TestClient/httpx. La ejecución completa posterior sustituye el pendiente histórico de suite HTTP de este avance. No prueba concurrencia PostgreSQL. Evidencias 39–46 inspeccionadas: listado 200, desactivación y estado inactivo, reactivación y estado activo, rechazo de sesión anterior y nueva sesión RH permitida. La autora reporta prueba en dos pestañas con modificación administrativa desde la cuenta original; los recortes 401 no muestran identidad/token/solicitud previa, por lo que se documentan como respuestas consistentes con la secuencia reportada, sin afirmar causalidad exclusiva frente a expiración. No se observaron contraseñas ni tokens en las capturas revisadas. No se cambiaron .env ni datos por el asistente durante esta consolidación. No hay prueba manual nueva de cambio de rol, traslado con reasignación ni concurrencia; esas comprobaciones no se infieren de las capturas. RF-7 permanece parcial por frontend y administración de departamentos pendientes.
Los registros de preparación anteriores se conservan como historial; esta entrada los actualiza. El paquete de consolidación y commit se prepara fuera del repositorio; la incorporación se materializa al ejecutar REGISTRAR_Y_COMMIT.ps1.

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

## 17 de octubre de 2026 — Administración y protección en React 0.4.0

Propósito: completar en bloque pantallas de cuentas y protección, reduciendo pasos manuales. Añadidos pages/Users.jsx y components/CaseProtection.jsx, integrados en App/CaseManagement; estilos, versión/lock y pruebas actualizados. Usuarios: listado/alta/edición auditada, estado/rol/departamento; protección: confidencialidad, participantes y revisión. Retiro inmediato de sesión propia revocada y de expediente sin acceso. Documentación sincronizada con los límites reales.

Verificación: primer pase 37 aprobadas/1 fallo por selector ambiguo de prueba, corregido; suite final 40 aprobadas en 6 archivos/23.66s. Build 21 módulos/358ms. API simulada; backend no modificado ni repetido. Pendiente comprobación agrupada real con evidencia 64, CRUD departamentos, móvil/matriz de roles e integraciones. No se registran como ejecutadas acciones de la autora que aún no ocurrieron.

## 17 de octubre de 2026 — Evidencia manual 64: administración React

Capturas aportadas por la autora: 64-admin-react-usuarios.png y continuación 64b-admin-react-usuarios-continuacion.png. Revisión visual: sección Usuarios con listado administrativo, nombres/correos de demostración, rol, departamento, activación y botones de edición. Aviso visible: «Cambios guardados. Sin cambio de permisos. Casos ajustados: 0». Continuación muestra Supervisor RH Demo Juan y paginación «Página 1 de 1». Sin contraseñas/tokens visibles. Capturas conservadas sin edición.

Se acredita listado renderizado y confirmación de guardado desde React para el recorrido reportado. No hay comparación antes/después del nombre ni cuerpo de petición, y las imágenes no prueban por sí solas auditoría persistida, revocación, alta, otros roles, protección ni concurrencia PostgreSQL. No se repitieron pruebas de código para esta actualización documental. RF-7/RF-8 siguen parciales; siguiente comprobación agrupada: confidencialidad/participantes sobre caso ficticio abierto con RH independiente.

## 17 de octubre de 2026 — Evidencias 65–66: protección desde React

Capturas aportadas por la autora, conservadas sin edición. 65-react-confidencialidad.png muestra Ausencia simulada EN_REVISION, aviso «Protección actualizada. Se recargaron expediente, relaciones e historial», acceso restringido a RH independiente, clasificación vigente e IA omitida. Se acredita estado confidencial renderizado tras el recorrido reportado; la imagen no muestra motivo enviado ni historial completo, y no prueba que el caso antes fuera público.

66-react-participante-confirmado.png muestra Empleado Operaciones Uno Demo con estado CONFIRMADO, declaración «testigo» y última revisión «Testigo Visual». La declaración se conserva separada del motivo de revisión y los campos del siguiente envío están vacíos. El recorte no incluye título/ID, revisor ni fecha: no permite vincular por sí solo la relación con el expediente de la evidencia 65 ni probar autoría independiente.

Sin contraseñas ni tokens visibles. Primera comprobación manual de confidencialidad y relación confirmada en React acreditada dentro de esos límites; no demuestra toda la matriz de permisos, exclusión del propio gestor, descarte, auditoría persistida ni concurrencia. No se repitieron tests para este registro documental; se mantienen separados los 40 tests UI simulados previos. RF-4/RF-8 parciales. No se requieren capturas adicionales de los mismos campos.

## 17 de octubre de 2026 — Cambio personal de contraseña en React 0.5.0

Propósito: ofrecer el endpoint existente de cambio de credencial en la interfaz de los tres roles. Añadidos PasswordChange.jsx y sus pruebas; App incorpora navegación personal, bloqueo durante envío y retiro de vistas/token al guardar o resultado incierto. Paquete/lock actualizados a 0.5.0; Vitest limitado a dos workers. Sin dependencias, backend ni migración nuevos.

Verificación: primer pase 46 aprobadas/2 timeout de pruebas anteriores; repetición completa con dos procesos, 48 aprobadas/7 archivos/67.31s. Build 22 módulos/749ms; diff revisado. Detalle y límites en REPORTE_QA.md. Manual/README, decisiones, backlog, entregables, trazabilidad y PRD actualizados. Pendientes: comprobación real con cuenta DEMO/evidencia 67, administración de departamentos y demás integraciones/matriz de roles. No se declara ejecución manual realizada.

## 17 de octubre de 2026 — Evidencia 67: contraseña desde React

Se inspeccionó directamente docs/evidencias/67-react-password-actualizada.png, guardada por la autora. Muestra login con correo/contraseña vacíos y aviso «Contraseña actualizada. Se revocaron tus sesiones. Inicia sesión con la nueva contraseña». Sin credenciales ni token visibles; conservada sin edición. Acredita resultado visible y retiro de la vista autenticada tras el flujo guiado, no revocación de todas las sesiones por sí sola.

La autora informó que volvió a iniciar sesión después del cambio; se registra como comprobación manual reportada de acceso con la nueva contraseña, sin inspeccionar ni guardar la credencial. No se comprobó rechazo de contraseña anterior ni de otras sesiones abiertas. RF-1/RF-8 siguen parciales. No se repitieron pruebas de código para este registro; la suite previa de 48 pruebas UI simuladas se mantiene separada.

## 17 de octubre de 2026 — Administración de departamentos

Propósito: cubrir catálogo administrativo pendiente con API y React. Añadidos api/departments.py, services/departments.py, DepartmentAudit, migración 0004 y Departments.jsx con navegación RH. Alta/renombrado/baja lógica/reactivación/historial con motivo y restricciones. Escritura/auditoría transaccionales; exclusión de usuarios activos/casos abiertos para baja. API 0.9.0, React 0.6.0; readiness ahora exige 0004. No se modificaron migraciones anteriores ni dependencias.

Validación final: 90 pruebas backend aprobadas/3 PostgreSQL omitidas/1 advertencia previa, 23.96s; 55 frontend aprobadas, 77.33s; build 23 módulos/571ms. Diagnóstico de conexión interna de TestClient y pasos interrumpidos documentados en REPORTE_QA.md; tests completos se ejecutaron después de habilitar red para pruebas.

Guía DEPARTAMENTOS.md creada; modelo de datos, manuales/README, decisiones, PRD, entregables, trazabilidad y backlog actualizados. Tabla y orden inmediato del backlog sincronizados para evitar presentar estados históricos como vigentes. Docker rechazó acceso desde el entorno del asistente: aplicación 0004, check real, evidencia 68 y concurrencia pendientes. No se declara RF-7 completo ni desplegado.

## 17 de octubre de 2026 — Evidencia 68: historial de departamentos desde React

Se inspeccionó directamente 68-react-departamentos-historial.png, guardada por la autora y conservada sin edición. Historial de «DEMO - PRUEBA 1» con cuatro eventos visibles: CREADO (nombre DEMO, activo), ACTUALIZADO por renombrado DEMO → DEMO - PRUEBA 1, ACTUALIZADO por desactivación (Inactivo), y ACTUALIZADO por reactivación (Activo). Cada entrada muestra fecha/hora y motivo académico; página 1 sin navegación adicional disponible. Sin contraseñas, tokens ni datos personales visibles.

Se acredita visualmente el recorrido básico de alta/renombrado/baja/reactivación y consulta de historial desde React para el departamento simulado. Sustituye el pendiente total de prueba manual de esta función. El recorte no muestra actor/UUID, terminal, versión Alembic ni alembic check: no acredita por sí solo revisión 0004 sin diferencias, autorización entre roles, bloqueo por usuarios/casos activos, atomicidad bajo fallos ni concurrencia PostgreSQL. La ejecución funcional observada es compatible con aplicación del backend y nueva auditoría; no se registra como verificación directa de migración.

Actualización documental, sin repetir pruebas de código. Se conservan separados resultados previos: 90 backend aprobadas/3 PostgreSQL omitidas/1 advertencia y 55 UI simuladas/build correcto. RF-7/RF-8 parciales; no se requieren nuevas capturas de los mismos campos.

## 17 de octubre de 2026 — PostgreSQL aislado reproducible

Propósito: ejecutar las integraciones omitidas sin tocar la base del proyecto. Añadidos test_support.py, guardas pytest, ejecutor nativo temporal y ocho pruebas unitarias; ampliado test_postgres.py con dos integraciones reales y precisión de unicidad. Se detectaron binarios PostgreSQL 18.6 instalados; no se descargó servidor ni se alteró Compose/PostgreSQL 17.

Verificación final: 103 aprobadas, cero omitidas, una advertencia previa, 21.70s; upgrade 0001–0004 repetido y check sin diferencias. Resultado JUnit validado antes de retirada del servidor/carpeta final. Se observaron también pasos exitosos de CI PostgreSQL 17 del commit c8ad75c. Fallo inicial de captura de pipes y rechazo automático de limpieza de restos documentados con sus límites en REPORTE_QA.md/PRUEBAS_POSTGRESQL.md.

Actualizados seguimiento, trazabilidad, modelo/guías y evidencia estructurada 69. Las tres pruebas antes omitidas ya tienen ejecución acreditada en base aislada; el modo sin RUN_DB_TESTS las conserva omitidas por diseño. Pendientes: CI del nuevo commit, carreras adicionales de negocio, matriz UI e integraciones IA/correo/analítica. No se exigen más capturas por esta ejecución.

## 17 de octubre de 2026 — Flujo IA con revisión y cola durable

Implementados contratos/proveedor/avisos Redis/worker y evaluador offline en app/ai, servicio/rutas, AIJob/0005 e invalidación de entrada al editar descripción. API 0.10.0, React 0.7.0 con solicitud/seguimiento/sugerencia separada de clasificación oficial. Compose agrega worker ai optativo y deja clave fuera de API/frontend. Dependencias fijadas; migraciones anteriores y credenciales intactas.

Validación final: 130 backend/0 omitidas/23.65s, upgrade/check 0005 correctos en PostgreSQL aislado; 64 UI/66.43s y ocho específicas tras ajuste de mensaje/9.96s; build 24 módulos/658ms. Fallo de orden temporal e instalación/importación detallados en REPORTE_QA.md. Sin envíos a OpenAI ni medición de calidad; proveedor/Redis simulados. Documentación/modelo/seguimiento y evidencia 70 actualizados. Pendiente aplicar 0005 al proyecto, configurar proveedor, probar Redis/worker reales y reunir 50+5 referencias independientes. RF-3 parcial.
## 17 de octubre de 2026 — Registro del recorrido IA real

Propósito: registrar la primera prueba guiada de asistencia y cierre con datos simulados. Inspeccionadas 71–73: respuesta completada en un intento, sugerencia Riesgos/Alta separada de la clasificación oficial y mismo expediente cerrado con prioridad Alta/validación vigente. Actualizados QA, IA, backlog, entregables, trazabilidad, README e índice de evidencias. Configuración/ejecución local reportadas por la autora; sin leer clave/.env ni repetir llamadas o tests. Alcance y límites en REPORTE_QA.md. Pendientes calidad independiente 50+5, modelo/consumo efectivos, check directo de desarrollo y matriz completa; RF-3/RF-8 parciales.
## 17 de octubre de 2026 — Borrador del conjunto de evaluación IA

Preparados docs/evaluacion_ia con 50 casos ficticios (10 por categoría), cinco abstenciones, etiquetas y justificaciones propuestas, entradas separadas sin etiquetas, revisión legible y manifiesto SHA256. Autoría del asistente explícita: revisión humana, independencia aceptada y congelación pendientes. Validación offline observada: 55 IDs/textos únicos, distribución 15 Alta/20 Media/15 Baja, contratos AIInput 55/55 y proyección exacta; evaluador existente admite estructura, con fallos marcados como no ejecutados solo en memoria. Sin predicciones guardadas, llamadas ni cargos. Actualizados QA, backlog, entregables, trazabilidad, decisiones, IA y README. No cambia código productivo ni prompt; no se repitieron suites. Pendiente revisión humana, congelación, ejecución real y matrices de confusión.

## 18 de octubre de 2026 — Conformidad sobre casos de evaluación

A petición de la autora se retira la fecha de la nota introductoria de REVISION.md y de la presentación del conjunto. La autora confirmó que los casos están bien: conformidad general reportada, sin atribuir revisión individual de etiquetas ni aprobación independiente. Manifiesto y hashes normalizados actualizados y comprobados; sin cambios en textos/etiquetas, sin predicciones ni llamadas. Congelación y evaluación pendientes.
## 18 de octubre de 2026 — Versión fijada y ejecutor de evaluación IA

Fijados referencias/entradas/catalogo/manifest v1 sin modificar textos ni etiquetas; conformidad general de autora preservada con sus límites. Se conserva su cambio local de formato en REVISION.md fuera del commit de este avance. Añadido app/ai/run_evaluation.py: vista previa por defecto, confirmación/configuración local para enviar, hashes de conjunto/proveedor, exclusión de procesos, diario fsync, máximo acumulado 55 intentos y reanudación sin reenviar fallos ni envíos inciertos. Proveedor ofrece metadatos optativos sin cambiar prompt/contrato operativo. Evaluador genera matrices y discrepancias.

Validación: 17 específicas aprobadas/7.03s; suite completa PostgreSQL 18.6 aislado, upgrade dos veces/check, 141 aprobadas/0 omitidas/27.85s; servidor/carpeta propios retirados. Primer pase específico: 11 aprobadas/6 fallidas por PermissionError de reemplazo en temporal sandbox; repetición en .pgdata pasó. CLI invocada inicialmente desde raíz no resolvió app; corregido directorio de ejecución a backend, vista previa correcta sin llamadas. Sin cambios frontend ni nuevas llamadas externas. Documentación/seguimiento y evidencia 74 actualizados. Pendientes ejecución real local y revisión de calidad/independencia; RF-3 parcial.
## 18 de octubre de 2026 — Evaluación IA externa v1 no supera metas

La autora ejecutó en Docker los 55 casos. Inspeccionados run/predicciones/reporte/diario; recomputación offline coincide, 55 START/END coherentes, IDs únicos y hashes de conjunto/proveedor correctos. Modelo efectivo gpt-4.1-mini-2025-04-14 en 55 respuestas; 17624 tokens de entrada y 3788 de salida reportados, sin verificar coste/saldo. Resultado: categoría 32/50, prioridad 30/50, abstención 5/5; 12 abstenciones en referencias regulares, cero fallos de transporte/esquema. Un falso negativo Alta: EVAL-C4-02, abstención; cero Alta→Baja. RF-3 no aceptado.

Conservados originales, análisis RESULTADOS_V1.md y evidencia 75. Actualizados seguimiento/guía/trazabilidad. Revisión técnica del caso Alta y posible insuficiencia de definiciones/contexto en prompt documentadas, sin atribuir revisión humana no realizada. Sin modificar código, referencias, respuestas ni prompt; sin llamadas adicionales ni suites repetidas. Pendientes corrección versionada, pruebas y otro conjunto independiente de aceptación tras uso diagnóstico del v1. Cambio local de formato en REVISION.md conservado fuera de este commit.
## 18 de octubre de 2026 — Prompt v2 y nuevo conjunto candidato

API 0.10.1, PROMPT_VERSION plurione-classify-v2. Extraídas instrucciones a app/ai/prompts.py: definiciones del PRD, prioridad por amenaza/impacto/plazo, hecho principal y asistencia como categoría específica, contexto confirmado de simulación, separación urgencia/categoría, abstención sin inventar hechos. Mantiene proveedor/endpoint/modelo local/salida estructurada/store=false/trazas/reintentos y decisión humana. Runner acepta manifest canónico, verifica hash separado del prompt, permite vista previa de borradores y bloquea envío sin congelación/conformidad; v1 no se ejecuta con v2.

Preparado candidato-v2 con 50 referencias y cinco abstenciones, 55 textos únicos y cero coincidencias textuales exactas con v1; autoría asistente explícita, sin revisión humana ni garantía de independencia, sin predicciones. Instrucciones fijadas antes de redactar candidatos y no ajustadas con resultados v2. Originales y referencias v1 intactos; edición local de la autora en REVISION.md conservada fuera del commit.

Validación: CLI vista previa correcta sin llamadas; 43 específicas aprobadas en 13.11s; suite completa PostgreSQL 18.6 aislado, upgrade 0005 dos veces/check sin diferencias, 147 aprobadas/0 omitidas en 35.30s; clúster propio detenido/retirado. Tests de borrador, mezcla de versiones/hash/rutas, metadatos/rechazo, separación de instrucciones y omisión de trabajo v1 antes de envío. Son simulaciones: no certifican precisión ni resistencia semántica real del modelo. Sin frontend modificado, suites UI no repetidas, sin llamadas/cargos ni lectura de .env. QA/guías/PRD/seguimiento/evidencia 76 actualizados. Pendientes revisión de candidatos, congelación, aplicación Docker y evaluación externa; RF-3 no aceptado.
## 18 de octubre de 2026 — Conformidad declarada y aceptación v2 fijada

La autora respondió explícitamente que revisó los 55 casos nuevos y está de acuerdo con categorías, prioridades y justificaciones. Copiada versión de trabajo a aceptacion-v2, fijadas etiquetas/hashes y registrada conformidad declarada antes de predicciones. Sin atribuir revisión independiente de terceros. Candidato y baseline v1 preservados; modificación local previa en REVISION.md permanece fuera del commit.

Añadido scripts/EVALUAR_IA_V2.ps1: vista previa nativa por defecto, opción -Ejecutar para construir imagen y evaluación aislada con configuración Compose local, límite 55 y salida fija ejecucion-v2. Sin imprimir/leer .env ni claves. Verificación observada: sintaxis PowerShell, vista previa sin Docker, argumentos correctos con Docker simulado y fallo de construcción bloquea siguiente etapa. Cero llamadas reales. Primera comparación de bytes del copiado falló por normalización CRLF/LF; verificación posterior de tres hashes normalizados y equivalencia JSON confirmó contenidos idénticos, CLI aprobó. Sin repetir suite backend (147 previa) ni frontend para esta preparación; guías/seguimiento/evidencia 77 actualizados. Pendientes ejecución real, revisión de métricas/independencia y aceptación RF-3.
## 18 de octubre de 2026 — V2 cumple metas numéricas de evaluación

Autora ejecutó scripts/EVALUAR_IA_V2.ps1 -Ejecutar y aportó captura final 55/55. Inspeccionados originales en ejecucion-v2; métricas recalculadas idénticas, diario 55 START/END y respuestas únicas, hashes de datos/proveedor/prompt concordantes. Modelo efectivo gpt-4.1-mini-2025-04-14; 49321 tokens entrada/4191 salida reportados, sin verificar factura/saldo.

Resultado: categoría 49/50 (98 %), prioridad 40/50 (80 %), abstenciones 5/5; Alta 15/15, cero falsos negativos Alta y Alta→Baja. Cumple metas numéricas, prioridad justo en umbral. Revisión técnica de 11 discrepancias: diez Media→Baja y una categoría Ausencias→Solicitudes Administrativas. Se conservan etiquetas/respuestas incluso en fronteras; aceptación humana/integral no inventada. Informe RESULTADOS_V2.md, evidencia 78 y documentación de seguimiento actualizados. Conjuntos v1/v2 distintos no prueban causalidad aislada ni independencia estadística. Sin código modificado, nuevos envíos ni suites repetidas. Próximo: aplicar versión operativa y H8 correo, conservando QA integral pendiente. Modificación local previa de REVISION.md permanece fuera del commit.
## 18 de octubre de 2026 — Mejora dirigida Media/Baja, prompt v3

Petición de la autora: mejorar la distinción tras diez Media→Baja en v2. API 0.10.2, plurione-classify-v3: prioridad en orden Alta→Media→Baja, Media por impacto operativo que requiere atención pronta sin exigir peligro/consecuencia grave, Baja solo cuando tampoco existe esa necesidad; una fecha por sí sola no fuerza Media. Se preservan clasificación humana, catálogo, abstención, contexto simulado, seguridad y criterios Alta; no se implementa corrección por palabras clave ni se cambian prioridades oficiales.

Evaluador agrega métricas por clase con denominadores completos, listas Media→Baja/Baja→Media, indicador complementario ≥80% en ambas clases (mínimo 10 por clase; null sin muestra) y acierto de ambos niveles por par contrastivo. Metas globales originales no reescritas. Diagnóstico offline de respuestas v2 confirma Media 10/20 y Baja 15/15, global previo cumple pero indicador complementario falla; se guarda separado, sin editar reporte original.

Nuevo candidato-v3: 20 pares Media/Baja, diez Alta y cinco abstenciones; textos nuevos fijados después del prompt y antes de predicciones, revisión humana/congelación pendientes. Datos con distribución 10 por categoría y prioridades 10/20/20, cero coincidencias textuales exactas con v1/v2, sin garantía de independencia. IDs de par solo en referencias. Guías/PRD/seguimiento/evidencia 79 actualizados; originales v1/v2 y edición local previa de REVISION.md conservados.

Validación: vista previa nativa correcta sin llamadas; 50 específicas aprobadas/15.31s; suite PostgreSQL 18.6 aislado, upgrade 0005 dos veces/check sin diferencias, 154 aprobadas/0 fallos/errores/omisiones en 34.52s. Clúster propio detenido/retirado. Tests mantienen bloqueos de borradores/versiones y jobs v1/v2 omitidos antes de envío. Frontend sin cambios/no repetido, sin nuevas llamadas, coste ni .env inspeccionados. Precisión v3, revisión de candidatos y Docker pendientes; no se declara mejora real por mocks.
## 18 de octubre de 2026 — Comando de vista previa v3 con envío bloqueado

Preparado scripts/EVALUAR_IA_V3.ps1 a partir del flujo v2, con carpeta fija ejecucion-v3 y prompt v3. Sin -Ejecutar valida aceptacion-v3 si existe, o candidato-v3 como borrador; no invoca Docker/proveedor. -Ejecutar requiere versión aceptacion-v3 fijada con conformidad y detiene antes de construir si falta. La pregunta sobre revisión de etiquetas está pendiente; no se inventa aprobación ni se crea una versión fijada.

Comprobación final observada: parser PowerShell correcto, vista previa nativa valida borrador sin Docker y ejecución bloqueada antes de Docker; tres controles aprobados, cero llamadas. La rama externa todavía no se ejecuta ni se presenta como calidad v3. Backend sin cambios: se mantienen 154 pruebas previas, no repetidas. Guías/seguimiento/evidencia 80 actualizados. Pendientes respuesta de revisión, fijación y evaluación real; originales y cambio local previo de REVISION.md preservados.
## 18 de octubre de 2026 — Conformidad v3 recibida y referencias fijadas

La autora respondió explícitamente que revisó pares Media/Baja, casos Alta y abstenciones y está de acuerdo con etiquetas y justificaciones. Copiado candidato a aceptacion-v3, conformidad declarada/fijación registradas antes de predicciones, tres hashes normalizados y equivalencia JSON verificados; datos/etiquetas/pares intactos. No se atribuye revisión de terceros. Candidato y evaluaciones anteriores preservados.

Comando EVALUAR_IA_V3.ps1 comprobado después de fijar: parser, vista previa nativa sin Docker, argumentos aceptacion-v3/ejecucion-v3 y límite 55 con Docker simulado, detención tras fallo de construcción. Cuatro controles correctos, cero llamadas reales; mensajes de ejecución del ensayo corresponden al stub, no resultados externos. No se creó ejecucion-v3 ni se consumió saldo. Backend/script sin cambios, 154 pruebas previas no repetidas; guías/seguimiento/evidencia 81 actualizados. Pendiente evaluación externa, métricas Media/Baja/Alta/pares y aceptación integral. Modificación local previa de REVISION.md conservada fuera del commit.
## 18 de octubre de 2026 — V3 distingue Media/Baja pero falla cuatro Alta

Autora ejecutó evaluación v3 y aportó captura 55/55. Archivos inspeccionados/recalculados: categoría 49/50, prioridad 46/50, Media 20/20, Baja 20/20, pares 20/20, abstención 5/5. Alta 6/10: cuatro Alta→Media, cero Alta→Baja. Diario 55 START/END, IDs únicos y hashes de datos/proveedor/prompt concordantes. Modelo efectivo gpt-4.1-mini-2025-04-14, uso reportado 63069 entrada/4050 salida sin verificar coste/saldo.

Revisión técnica de cuatro urgentes y un desacuerdo de categoría en RESULTADOS_V3.md; todos conservados sin alterar referencias. Los urgentes incluyen plazo/pérdida grave no física; varios motivos reconocen esos hechos aunque asignan Media. No se recomienda aplicar v3 ni aceptar prioridad integral por cumplir promedios. Indicadores originales true y human_acceptance=false preservados. Conjuntos v2/v3 distintos no prueban regresión causal aislada. Originales/evidencia 82 y documentación actualizados. Sin código/prompt/configuración modificados, sin llamadas adicionales ni tests repetidos; cambio local previo REVISION.md conservado. Pendiente resolver/verificar Alta sin perder Media/Baja, no repetir por buscar una puntuación favorable.

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

## 19 de octubre de 2026 — Guías consolidadas tras revisión de avance

Propósito: analizar la evaluación recibida y sustituir la documentación acumulada por entregas por una estructura coherente de uso, operación, alcance y cierre. Se confirmó el problema documental y de UTF-8; se corrigió la lectura desactualizada sobre correo/analítica sin declararlos aceptados integralmente.

Cambios: README de raíz/backend/frontend/infra; índice docs/README.md; nuevo MVP.md y análisis REVISION_EVALUACION.md; consolidación de PRD, manual técnico, backlog, entregables, trazabilidad, datos, frontend, autenticación y aperturas/estado de guías administrativas, IA, correo y analítica. Declaración de apoyo de Codex y uso de IA en el producto. Decisión de conservar en historial y artefactos técnicos las referencias necesarias para reproducibilidad. Tres fuentes Python solo cambian textos descriptivos; sin modificación funcional.

Validación: 26 documentos y 152 enlaces/anclas comprobados, UTF-8 y bloques Markdown correctos, comparación AST de tres fuentes con HEAD sin cambios funcionales; git diff --check correcto. El lanzador venv falló al iniciar Python; no se reparó ni se reejecutó la suite/API. Los resultados previos siguen siendo históricos, no resultados de este cambio. Sin llamadas pagadas, datos operativos, secretos ni cambios a referencias congeladas. Edición local previa de docs/evaluacion_ia/REVISION.md preservada fuera del cambio; capturas personales excluidas de Git conservadas.

Resultado: guías principales sin capítulos por versiones ni contradicciones conocidas sobre funciones ausentes; estado y condiciones de cierre explícitos. Pendientes: revisión semántica/valores/refresco de Power BI, propuesta/arquitectura formal, aceptación por roles, legibilidad acotada de funciones extensas, manual de usuario y recuperación/soporte/capacitación/informe. Fecha límite y capacidad todavía sin confirmar.

Registro Git pendiente: el intento de preparar el commit devolvió permiso denegado al crear .git/index.lock, aun con acceso solicitado. Los archivos quedaron guardados en el proyecto; no se creó commit ni se publicó el cambio.

## 19 de octubre de 2026 — Propuesta y arquitectura documentadas

Propósito: completar los documentos técnicos faltantes identificados en la evaluación, manteniendo la estructura por tarea y sin capítulos por versiones. Archivos nuevos PROPUESTA_TECNICA.md y ARQUITECTURA.md; actualizados README documental, ENTREGABLES, BACKLOG, MVP, MANUAL_TECNICO, REVISION_EVALUACION, TRAZABILIDAD, DECISIONES y REPORTE_QA.

Contenido: objetivos y cobertura de requisitos, alternativas, recursos, riesgos, aceptación y tres diagramas Mermaid de componentes/flujo/datos. Se documentaron límites del código observado y de operación; sin inventar aprobación, entrevistas, mejora medida, presupuesto, capacidad ni fecha de entrega. Se contrastaron fuentes de Compose, modelos, servicios, workers, cuenta de reporting y workflows.

Validación: comprobación estática final de 28 documentos y 202 enlaces/anclas del cambio acumulado, sin errores de UTF-8 o bloques Markdown; referencias de entidades y componentes contrastadas y git diff --check correcto. No se ejecutaron nuevas pruebas funcionales ni renderizado de diagramas. No se modificaron código, configuración, datos o referencias congeladas en esta actividad. Los cambios previos del proyecto se conservaron; el commit sigue pendiente por el bloqueo de escritura Git registrado antes.

Resultado: propuesta y arquitectura disponibles y enlazadas; las matrices ya no las marcan como archivos pendientes. Continúan Power BI semántico/valores/refresco, aceptación por roles, instalación limpia, carga, manual de usuario, respaldo/restauración, soporte, capacitación e informe. Estos documentos no certifican operación productiva ni cierre académico.

## 19 de octubre de 2026 — Manual de usuario y plan de soporte/recuperación

Propósito: completar las guías de uso y operación restantes sin presentar procedimientos preparados como pruebas ejecutadas. Nuevos MANUAL_USUARIO.md y PLAN_MANTENIMIENTO.md, con instrucciones por rol, resolución de dificultades, soporte por niveles y copia/restauración aislada. Matrices e índice actualizados junto con MVP, manual técnico, trazabilidad, decisiones y revisión de la evaluación.

Validación: revisión contra componentes React, modelos/Compose y documentación oficial pg_dump/pg_restore. Parser PowerShell sobre cuatro bloques, cero errores de sintaxis y sin ejecutar comandos. Comprobación estática del cambio acumulado de 30 documentos, 218 enlaces/anclas y tres fuentes Python sin errores; git diff --check correcto. No se efectuaron respaldo, restauración, carga, llamadas IA, consulta de datos operativos ni pruebas funcionales. No cambió código o configuración en esta actividad; se preservaron cambios previos del proyecto, revisión IA local y capturas excluidas.

Resultado: manual de usuario integrado y mantenimiento/soporte documentados. El ensayo debe usar un contenedor sin red/puertos, no sustituye la base de uso, no activa workers y separa recuperación de datos de reconstrucción/verificación de privilegios. La copia lógica no incluye por sí sola roles globales ni configuración privada. No se asignaron SLA/RPO/RTO, retención o métricas ficticias.

Pendientes: ejecutar el ensayo con casos simulados y registrar conteos/relaciones/tiempos, comprobar recuperación completa de permisos, definir custodia/retención, completar Power BI y matriz por roles, capacitación real e informe final. Los documentos ya no figuran como inexistentes; su validación operativa sigue pendiente. Cambios guardados localmente, sin commit nuevo por el bloqueo Git previamente registrado.

## 19 de octubre de 2026 — Ejecutor de recuperación e intento nativo

Propósito: pasar del procedimiento de copia/restauración a un ensayo reproducible sin tocar la base de trabajo. Nuevo backend/scripts/test_recovery_isolated.py; actualizados plan, backlog, entregables, trazabilidad, decisiones y QA. Evidencia 99 registra el intento fallido y la comprobación posterior de ausencia de servidor.

Validación real: importación de SQLAlchemy/Alembic/psycopg existentes con runtime disponible; initdb correcto; arranque pg_ctl bloqueado al crear token restringido (87/3), sin copia ni restauración. pg_ctl status posterior confirmó que no había servidor activo. CLI --help correcta. Fixture comprobado en SQLite con FK: seis casos, uno confidencial/cerrado, participante, trabajo IA y outbox. No se repitió suite funcional, no se inició API/worker y no hubo llamadas de pago ni acceso a .env o base operativa. Carpeta propia conservada en .pgdata; sin borrados recursivos ni cambio del entorno virtual.

Resultado y pendientes: ejecutor y orden de terminal propia preparados; recuperación completa, reconstrucción BI en destino, comparación de objetos/datos y tiempos sin acreditar hasta ejecución exitosa. El bloqueo se documentó sin eludir restricciones de procesos. Secuencia Docker e instalación limpia siguen pendientes, además de Power BI y matriz por roles. Cambios previos y revisión IA local preservados; registro Git pendiente por bloqueo previamente documentado.

## 20 de octubre de 2026 — Ensayo de copia y restauración completado

Propósito: verificar la recuperación aislada después de que la autora reportó Docker operativo. Cambios en ejecutor test_recovery_isolated.py y nuevas pruebas test_recovery_runner.py; reportes 100–103; actualizados plan, backlog, entregables, MVP, manual técnico, arquitectura, revisión de evaluación, trazabilidad, decisiones y QA.

Resultados: 100–102 fallaron en comparación textual de definiciones aunque datos/copia/restauración coincidían. Se diagnosticaron casts de arrays de literales varchar a text distribuidos por el parser y se acotó esa normalización con cinco pruebas aprobadas (0.09 s), sin modificar datos ni relajar opciones de seguridad. 103 PASSED: catorce tablas, dos vistas, 144 restricciones y 35 índices comprobados; esquema/check correctos. Cuenta BI reconstruida lee agregados y rechaza tres operaciones operativas. Archivo inválido rechazado, origen sin cambios y ambos servidores detenidos. Evidencia conserva conteos, hashes y tiempos, sin secretos.

Límites: prueba nativa PostgreSQL 18.6 con seis casos y entidades ficticias, sin secuencia Docker (API de Docker denegada a herramientas), aplicación o workers. No es carga, recuperación completa de instalación/roles ni RPO/RTO. Sin .env, base de uso, emails, llamadas IA, reinstalaciones o borrados recursivos. Se preservaron reportes fallidos y cambios previos, incluida revisión IA y capturas excluidas. El primer intento de crear el archivo de pruebas quedó sin ejecutar por permiso de carpeta; se resolvió y se verificó.

Pendientes: instalación completa/secuencia Docker, custodia/retención, Power BI semántico/formatos/refresco, matriz por rol y cierre académico. La suite funcional previa no se vuelve a declarar ejecutada por este avance; registro Git sigue pendiente por las restricciones de acceso conocidas.


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


## 20 de octubre de 2026 — Custodia y retirada de informes preparadas

Propósito: completar un pendiente documental de entrega reutilizando evidencia existente. PLAN_MANTENIMIENTO.md incorpora un procedimiento breve de preparación, identificación por corte/hash, autorización, custodia, sustitución y retirada confirmada. Define campos para un registro privado sin introducir datos personales en Git. BACKLOG.md distingue procedimiento preparado de responsables, destino, conservación y operación aún pendientes.

Validación: lectura de los tres documentos modificados, UTF-8, bloques Markdown y referencias locales del apartado revisados; sin pruebas funcionales ni repetición de Power BI. No hubo distribución, borrados, nuevos archivos de datos, cambios de permisos o ejecución del comando de hash; este se ofrece como instrucción para una entrega futura. No se inventaron custodios, destinatarios, plazos, autorizaciones o retiradas. Resultado: procedimiento revisable; aplicación real y aceptación por roles pendientes. Sin commit.


## 20 de octubre de 2026 — Consulta administrativa confirmada por la autora

Evidencia 110: la autora indicó iniciar sesión como admin@plurione.local y confirmó que cargan los listados de Usuarios y Departamentos. Es una comprobación manual reportada por ella, sin captura ni observación directa del agente; no acredita altas, ediciones, bajas, auditoría ni restricciones de otros roles. El control de ventanas había fallado y se detuvieron los reintentos para acotar consumo.

Se registró la evidencia y se actualizó RF-7 en TRAZABILIDAD.md. QA y bitácora conservan la procedencia del resultado; aceptación integral pendiente. Una primera solicitud de escritura apuntó por error a una ruta incorrecta, sin modificar archivos; se corrigió el permiso antes de guardar en docs. Validación limitada a lectura JSON y presencia del registro en los tres documentos. Sin pruebas nuevas, cambios funcionales, operación de Power BI, datos modificados o commit.


## 20 de octubre de 2026 — Comprobación manual parcial de Supervisor y Empleado

Propósito: consolidar las capturas y confirmaciones del recorrido por roles sin repetir pruebas costosas. Nueva evidencia 111; actualizados TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Supervisor: listado visible, detalle confirmado y reapertura no permitida según la autora. Empleado 1: lista inicialmente vacía, alta de un caso simulado, detalle con evento CREADO y listado posterior; ausencia de más acciones confirmada por la autora. El caso permanece registrado; no hubo modificación de código ni eliminación de datos.

Durante el recorrido hubo error Docker 500 y rechazo de conexión del frontend. Tras reiniciar, una captura mostró Client/Server sin error y la autora confirmó reapertura de la página. No se atribuye causa raíz ni se declara resuelta su recurrencia. El aviso anterior de caso no disponible/sin permiso no acredita una denegación válida sin expectativa definida.

Validación documental: JSON releído y referencias nuevas comprobadas en los cuatro documentos. Originales de capturas fuera de Git; procedencia y límites explícitos. Pendientes: comprobación API, casos ajenos/confidenciales, gestión RH, móvil y accesibilidad; sin aceptación integral, pruebas automáticas nuevas ni commit.


## 21 de octubre de 2026 — RH: cierre, reapertura y consulta coherente por Empleado

Propósito: consolidar el recorrido manual de RH sobre el caso simulado iniciado en evidencia 111. Nueva evidencia 112 y actualización de TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. La autora confirmó resolución, cierre y registro de reapertura. Las capturas finales muestran el mismo ID En revisión desde RH y Empleado, prioridad Baja y validación vigente en RH. El aviso de reapertura declara conservación del ciclo anterior; no se inspeccionó su contenido completo. El seguimiento actual no muestra resolución ni fechas de resuelta/cerrada. Caso dejado en revisión, sin nuevo cierre.

Validación: JSON releído y enlaces a evidencia comprobados en los tres documentos actualizados. Capturas originales fuera de Git. Sin cambios funcionales, suite automática, comprobación API, validación SMTP/IA ni commit. No se inventa la fecha de las operaciones intermedias, el texto exacto guardado ni aprobación institucional. Persisten pruebas negativas de acceso, móvil/accesibilidad y demás aceptación integral.


## 21 de octubre de 2026 — Revisión parcial a 390 px y diagnóstico del enlace previo

Propósito: consolidar capturas y confirmaciones de la autora. Nueva evidencia 113; actualizados TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Detalle legible sin desplazamiento horizontal reportado en emulación 390 × 844; filtros en columna observados. Captura de consola identifica solicitudes 404 de detalle/historial de un expediente anterior, con sesión activa; retorno al panel confirmado sin problemas. No se comprobó existencia/permisos de ese expediente ni se declara autorización negativa probada.

Validación documental: JSON releído y enlaces nuevos comprobados. Capturas fuera del repositorio. Sin código modificado, suite nueva, teléfono físico, auditoría de accesibilidad ni commit. Pendientes: prueba negativa con caso conocido, móvil real y accesibilidad. Se revisaron estáticamente visibility() y cuentas demo para preparar una prueba entre empleados; esto no acredita su ejecución.


## 21 de octubre de 2026 — Consulta de caso ajeno entre empleados

Propósito: verificar un resultado negativo con un caso cuya existencia está documentada, evitando atribuir permisos al antiguo expediente ambiguo. Nueva evidencia 114 y actualización de TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Capturas aportadas muestran Empleado Operaciones Dos Demo, listado vacío y aviso de acceso no disponible al enlace del caso de Empleado 1 según la autora. Resultado esperado para este escenario manual; identidad visible, URL completa y tráfico HTTP no inspeccionados. Filtros adicionales del listado colapsados.

Validación documental: JSON releído y referencias nuevas comprobadas. Sin cambios de código, mutaciones de datos, nuevas suites, llamadas API directas ni commit. Originales de capturas fuera del repositorio. Pendientes: confidencialidad, restricciones de escritura y demás aceptación integral; no se extrapola este resultado a todos los objetos o roles.


## 21 de octubre de 2026 — Confidencialidad y consulta del creador

Propósito: consolidar la prueba manual de protección del mismo caso simulado de 111–112. Nueva evidencia 115; actualizados TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. La autora confirmó cambio a confidencial desde RH independiente y conservación de consulta RH. Capturas de Empleado 1 muestran denegación del detalle por el enlace indicado y lista vacía con contador cero. Cambio de confidencialidad y acceso RH sustentados por texto, no por captura independiente; filtros adicionales del listado colapsados. Caso conservado confidencial, sin reversión solicitada.

Validación documental: JSON releído y referencias nuevas comprobadas. Sin cambios de código, nuevas suites, llamadas API directas ni commit. No se verificaron auditoría del cambio, retirada de datos de sesiones abiertas, cachés, correo o BI. Originales de capturas fuera del repositorio. Pendientes: restricciones de escritura y demás escenarios de aceptación integral.


## 21 de octubre de 2026 — Intento acotado de pruebas de escritura

Propósito: verificar restricciones sin modificar el caso confidencial de uso. Leídos tests existentes y seleccionados cuatro de backend/tests/test_incidents.py. Primer intento con .venv sin salida, interrumpido; segundo con runtime auxiliar y site-packages del proyecto falló antes de resultados al importar ArgsKwargs desde pydantic_core. Evidencia 116 preserva ambos fallos y límites; no se declara ningún test aprobado ni causa raíz del primer bloqueo.

Actualizados TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Sin modificaciones de código, dependencias instaladas, PostgreSQL operativo solicitado ni commit. Una búsqueda inicial de archivos incluyó test_lifecycle.py y pyproject.toml inexistentes; se continuó con test_incidents.py y pytest.ini reales. Validación documental: JSON releído y referencias nuevas comprobadas. Pendiente ejecutar la selección en un runtime compatible.


## 21 de octubre de 2026 — Seguimiento de interrupción pytest

Evidencia 117: captura de la autora muestra KeyboardInterrupt en importlib y cero tests en 8,67 s. Es interrupción antes de resultados, no un test de permisos fallido. pyvenv.cfg identifica Python 3.11 y extensión cp311; el intérprete base imprime versión correctamente. Intento adicional del agente con ese Python, dependencias del proyecto y autoload de plugins deshabilitado tampoco produjo salida; se interrumpió sin traza. No se conoce la causa raíz.

Sin código ni dependencias modificados, pruebas aprobadas nuevas o commit. Actualizado el pendiente en BACKLOG.md. Validación documental: JSON releído y enlace comprobado. Próximo diagnóstico acotado: una prueba con --full-trace para obtener el punto real de importación al interrumpir; no repetir suites completas. Captura original fuera del repositorio.


## 21 de octubre de 2026 — Cuatro tests de escritura aprobados en terminal de la autora

Propósito: cerrar la ejecución pendiente de la selección de permisos de 116–117. Nueva evidencia 118 y actualización de TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Capturas aportadas muestran 1 passed in 5.85s y 3 passed, 22 deselected in 5.13s. Los nombres seleccionados corresponden a gestión/asignación, protección por RH independiente, revalidación/límites del supervisor y registro no autorizado por empleado. La primera captura muestra PYTEST_DISABLE_PLUGIN_AUTOLOAD=1; segunda ejecución indicada en la misma terminal, sin reimpresión de variable. No se aisló un plugin causante ni se afirma causalidad exclusiva.

Validación: resultados de consola revisados en capturas, cobertura contrastada con código leído en el avance previo, JSON releído y referencias nuevas comprobadas. Fixtures SQLite y usuario/sesión sustituidos; sin autenticación real, PostgreSQL operativo o suite completa. Sin cambios de código/dependencias ni commit. Antecedentes interrumpidos conservados como tales; capturas fuera de Git. Pendientes: demás escenarios operativos y aceptación integral.


## 21 de octubre de 2026 — Salud de la instalación actual confirmada

Propósito: comprobar disponibilidad actual sin repetir restauración ni modificar servicios. Evidencia 119 con capturas aportadas: /health devuelve status ok/service plurione-api; /health/db devuelve status ok/database postgresql; compose ps muestra API, PostgreSQL y Redis Up 37 minutes (healthy). No hubo reinicio o instalación limpia en esta comprobación. Se mantiene separado del ensayo aislado 103.

Actualizados TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Validación: lectura de capturas, JSON releído y referencias nuevas comprobadas. Sin código modificado, llamadas Docker del agente, nuevas suites o commit. No se declaran workers activos, recuperación completa, carga, RTO/RPO ni disponibilidad futura. Pendientes operativos conservados.


## 21 de octubre de 2026 — Consulta RH y salud tras reinicio reportado de API

Propósito: consolidar comprobación manual posterior a docker compose restart api solicitado. Evidencia 120: la autora confirmó finalización y aportó listado/detalle RH con el caso conocido, estado En revisión, prioridad Baja, validación vigente y acceso restringido a RH independiente; posteriormente confirmó /health/db ok mediante captura. No hay captura del comando ni tiempos de reinicio. El detalle también muestra IA omitida; no se atribuye una nueva ejecución ni causa al reinicio.

Actualizados TRAZABILIDAD.md, BACKLOG.md, ENTREGABLES.md y PLAN_MANTENIMIENTO.md. Validación: capturas revisadas, JSON releído y enlaces nuevos comprobados. Sin nuevas suites, código modificado, datos alterados por el agente o commit. Prueba de reinicio API reportado, no instalación limpia, reinicio de base/Redis ni recuperación completa. Sin RTO/RPO medido; aceptación integral y comprobaciones operativas restantes pendientes. Originales de capturas fuera de Git.


## 21 de octubre de 2026 — Protocolo de rendimiento RNF-2

Propósito: convertir el criterio de rendimiento pendiente en un ensayo revisable sin cargar la plataforma de uso. Nuevo PRUEBA_RENDIMIENTO.md; actualizados TRAZABILIDAD.md, BACKLOG.md y ENTREGABLES.md. Criterio de p95, diez usuarios, cien casos y cinco minutos tomado del PRD; calentamiento, distribución de operaciones, tratamiento de errores y aislamiento definidos como decisiones del protocolo. Endpoints contrastados con rutas del repositorio. No se cambia el requisito ni se inventan resultados.

Validación documental: fuente del criterio y rutas leídas, UTF-8 y enlaces locales nuevos comprobados. Una búsqueda incluyó QA.md inexistente; no se creó ni se usó como fuente. Sin ejecutor implementado, Docker operado, carga ejecutada, dependencias cambiadas o commit. Pendiente implementar/validar generador y desplegar QA separado para medir con hardware/configuración registrados.


## 21 de octubre de 2026 — Ejecutor de rendimiento y pruebas locales

Propósito: implementar el generador del protocolo sin cargar la plataforma actual. Nuevos backend/scripts/performance_runner.py, manifiesto de ejemplo deshabilitado y backend/tests/test_performance_runner.py. Actualizados PRUEBA_RENDIMIENTO.md, TRAZABILIDAD.md, BACKLOG.md, ENTREGABLES.md y DECISIONES.md; evidencia 121 con hashes. Implementa destino loopback separado, preflight de cuentas y cien casos, diez clientes sincronizados, cuatro operaciones, modo corto/formal, métricas por operación y errores, conteos, muestras y revocación de sesiones. No provisiona ni inspecciona Docker ni registra recursos automáticamente.

Validación: AST válido; trece pruebas locales instaladas aprobadas en 0,084 s con unittest estándar y mocks. Una prueba ampliada falló inicialmente por contraseña ficticia ausente en su fixture; corregida con entorno simulado y sin relajar el ejecutor. Repetición tras instalar comprueba importación por ruta final. CLI rechazó manifiesto de ejemplo por AISLAMIENTO_NO_CONFIRMADO con salida 1 antes de HTTP. JSON, hashes y enlaces nuevos comprobados. Sin suite backend completa, carga real, Docker operado, base de uso modificada, dependencias instaladas o commit. RNF-2 permanece pendiente de provisionar QA, smoke y medición formal con metadatos/verificaciones externas.


## 21 de octubre de 2026 — Provisionador Docker QA de rendimiento preparado

Propósito: permitir una corrida aislada reproducible mediante un comando. Nuevos provision_performance_qa.py, performance_seed.py y test_performance_provisioner.py; performance_runner.py añade marcas UTC por fase. Protocolo, trazabilidad, backlog, entregables y decisiones actualizados. Evidencia 122 con hashes, alcance y límites; hash anterior del generador en 121 conservado como histórico.

Validación instalada: nueve tests simulados de provisionador aprobados en 1,236 s y trece de generador en 0,079 s. CLI --plan salida 0 sin Docker/archivos/contraseñas. Una corrida inicial falló por temporales no escribibles en el sandbox; tests redirigidos a cwd permitido, sin cambiar la política del provisionador. Una búsqueda inicial con glob en argumento no fue válida en PowerShell; se corrigió buscando sobre el directorio real. AST y enlaces/JSON/hashes comprobados.

No se ejecutó Docker real, build, fixture PostgreSQL real, HTTP smoke ni carga formal; no se instalaron dependencias ni se modificó base operativa. Sin commit. Provisionador verifica configuración/propiedad de recursos y prevé parada exclusiva sin borrar; su compatibilidad real con Compose/red debe comprobarse mediante smoke desde la terminal de la autora, dado el acceso Docker denegado a herramientas previamente documentado. RNF-2 permanece pendiente.


## 22 de octubre de 2026 — Diagnóstico del primer smoke y conectividad QA

Propósito: resolver el bloqueo real sin repetir carga inexistente ni tocar la plataforma de uso. Leído el reporte de performance-897c25b02d4340d6: INCOMPLETA por ConnectionRefusedError HTTP, sin calentamiento/medición. SQL verifica cien casos/eventos CREADO, mil entregas, cero intentos SMTP y trabajos IA; contenedores detenidos. Original preservado con hash en evidencia 123.

Modificados provision_performance_qa.py y test_performance_provisioner.py: red de entrada propia adicional para API, datos solo en red interna, salud desde host previa a fixture y diagnóstico de redes/puertos. Actualizados protocolo, trazabilidad, backlog, entregables y decisiones. Doce pruebas simuladas instaladas aprobadas en 0,993 s; AST y referencias/JSON/hashes comprobados. Ejecutor de carga sin cambios. Consulta de documentación oficial de Docker usada como referencia, no como demostración de causa raíz.

Sin Docker operado por el agente, repetición de carga, cambios en configuración de uso, borrado de recursos o commit. Corrección pendiente de smoke real; red de entrada deja salida disponible para API QA, con proveedores sin claves/desactivados y sin workers. No se declara RNF-2 aprobado ni rechazo de conexión resuelto todavía.


## 22 de octubre de 2026 — Segundo smoke y sockets del generador

Leído reporte real d1c2d490b7df42b4 de la autora. Salud host OK en un intento y preflight completo; calentamiento interrumpido a unos 0,13 s con diez listados, seis 200 válidos y cuatro EXCEPTION. Sin fase medida ni operaciones posteriores de carga. Diez logout 204, QA detenido y cien casos/eventos/mil entregas, cero intentos SMTP/trabajos IA. Primera búsqueda devolvió metadatos extensos del reporte; se conservaron en evidencia únicamente resultados pertinentes sin secretos.

Modificados performance_runner.py y test_performance_runner.py: cerrar sockets de preparación al entrar en fases, preservar tokens, conexiones nuevas para postcomprobaciones/logout y excepciones tipificadas sin mensajes ni reintentos. Hipótesis de sockets keep-alive caducados; no se demuestra causa raíz con el registro EXCEPTION anterior. Documentación oficial de Uvicorn consultada, sin modificar producto/servidor. Quince tests locales instalados aprobados en 0,135 s; AST, JSON, enlaces y hashes comprobados.

Evidencia 124; protocolo, trazabilidad, backlog, entregables y decisiones actualizados. Reporte real conservado con hash. Sin Docker operado por el agente, nueva carga real, suite completa o commit. Pendiente smoke con la corrección; RNF-2 no aprobado.


## 22 de octubre de 2026 — Smoke real de rendimiento satisfactorio en su alcance

Leído reporte de la autora performance-42486b8ff1264162 y revisada captura. Salud host OK, diez clientes completan calentamiento 2 s y medición 5 s: 70 y 150 solicitudes sin errores. Conteos 100/120/160, SQL con 160 eventos CREADO, 40 CONTENIDO_EDITADO, 1600 entregas, cero intentos SMTP y trabajos IA. Diez logout 204, contenedores detenidos y tres muestras de recursos. Original conservado con hash en evidencia 125.

Actualizados protocolo, trazabilidad, backlog y entregables. Validación documental: JSON releído, métricas/conteos cotejados y referencias comprobadas. No se cambia código ni repiten suites. p95 corto de creación 931,9 ms y edición 434,0 ms superan 200 ms; no se acredita RNF-2 ni causa raíz del rendimiento. Pendiente corrida formal de 30 + 300 s en entorno nuevo. Sin Docker operado por el agente, borrado de recursos o commit.


## 22 de octubre de 2026 — Medición formal de rendimiento: umbral incumplido

Leído reporte real d1c50f8001464425 y captura aportada por la autora. Calentamiento 30 s y medición 300 s completos, diez clientes, 7813 solicitudes medidas y cero errores. p95 de listado 283,1 ms, detalle 253,9 ms, creación 1245,9 ms y actualización 476,0 ms: cuatro incumplimientos de <200 ms. RNF-2 medido y no cumplido, sin ocultar resultado. Casos 100/295/2249; SQL con 2249 creaciones, 2139 ediciones, 22490 entregas, cero intentos SMTP/trabajos IA. Diez logout 204 y contenedores detenidos. Cuarenta y nueve muestras Docker conservadas.

Evidencia 126 con hash del original, métricas y límites. Actualizados protocolo, trazabilidad, backlog (también fila de estado principal) y entregables. Validación documental: JSON releído, suma/errores/duración cotejados y referencias comprobadas. Original preservado. Sin nueva corrida, cambios funcionales o commit. No se identifica causa raíz con estos datos: siguiente avance debe perfilar y justificar una optimización antes de repetir; preservar auditoría, permisos y encolado. Generador y Docker comparten equipo; ese límite queda explícito.


## 22 de octubre de 2026 — Agrupación de consultas para destinatarios de creación

Propósito: atacar el coste medido de creación sin reducir controles. Modificados services/incidents.py y services/mail.py; añadido tests/test_mail_batching.py. Perfil con TestClient inicial bloqueado al importar y detenido, sin resultados. Perfil alternativo usa AST de funciones reales/modelos reales/SQLite propio, sin FastAPI o SDK, con utcnow sustituido. Antes: 10/42/122 sentencias para 2/10/30 RH. Después: 4/4/4, mismas entregas e idempotencia; nueve escenarios de confidencialidad/relaciones/afectación/actividad/roles coinciden con funciones antiguas, con rollback de evento y entregas. No es latencia PostgreSQL ni API.

Nueva selección SQL de RH activos independientes, predicado compartido, consulta conjunta de IDs UUID5 existentes y adiciones en lote en la transacción original. AST de allowed(), omission() y process_one() sin cambios. Trece regresiones pytest preparadas con AST válido; todavía no ejecutadas. Evidencia 127 registra hashes, método, resultados y límites; protocolo, trazabilidad, backlog, entregables y decisiones actualizados. JSON/referencias/AST comprobados. Sin nuevo p95, carga, migración, Docker operado, cambios de configuración de uso o commit. Pendiente regresión API desde la terminal de la autora antes de repetir smoke/full.


## 22 de octubre de 2026 — Regresión de correo/incidencias/encolado aprobada por ejecución de la autora

Captura aportada muestra comando de tres archivos y resultado 60 passed in 15.07s. Integraciones DB desactivadas, SSLKEYLOGFILE vacío y plugins automáticos/caché pytest deshabilitados. Evidencia 128 registra procedencia y hashes coincidentes con 127; no se atribuye la ejecución satisfactoria al agente ni se declara CI remoto.

Actualizados protocolo, trazabilidad, backlog y entregables. Validación documental: captura revisada, JSON releído, hashes y referencias comprobados. No se modifica código ni repiten pruebas. Esta selección valida regresión SQLite/TestClient/correo con transportes de prueba; no PostgreSQL concurrente, suite completa o nuevo p95. Siguiente paso: una medición formal en QA nuevo con el protocolo existente para comparar con 126. Sin cambios en servicios de uso o commit.


## 22 de octubre de 2026 — Segunda medición formal tras optimizar encolado

Leídos reportes reales 791d2288a84d4872 y línea base d1c50f8001464425. Nueva corrida completa, diez clientes/300 s, 11226 solicitudes y cero errores; p95 listado 301,8, detalle 267,7, creación 609,0 y edición 485,9 ms. Frente a 126, creación baja aproximadamente 51,1% y solicitudes suben 43,7%; lecturas/edición no mejoran y cuatro umbrales siguen incumplidos. Casos 100/398/3205; SQL con 3205 creaciones, 3096 ediciones, 32050 entregas, cero intentos SMTP/trabajos IA. Diez logout 204 y QA detenido.

Evidencia 129 con hashes originales, métricas/comparación completa y diferencias de código declarado. Actualizados protocolo, trazabilidad, backlog y entregables. JSON, referencias y preservación de originales comprobados. Sin cambios de código, suite nueva, carga repetida o commit. Comparación no causal: el conjunto final crece más al aumentar throughput y no se midió capacidad del generador. Pendiente perfilar edición/lecturas antes de otro cambio y no repetir medición sin justificación. RNF-2 permanece no cumplido.


## 22 de octubre de 2026 — Consulta de sesión/usuario/departamento agrupada

Propósito: reducir un coste común antes de otra carga. Modificado únicamente current_user en core/security.py y añadido tests/test_auth_queries.py con trece casos. Perfil del cuerpo real mediante AST, modelos reales y SQLite propio: sesión válida pasa de tres SELECT a uno; doce escenarios conservan estados/mensajes/challenge. Tres cambios externos con entidades precargadas son detectados. Depends/HTTPException sustituidos para evitar importar SDK/FastAPI en el perfil; no es prueba HTTP. Otras funciones de security.py mantienen AST. Hashes de lifecycle.py, administration_lock.py y database.py coinciden con la corrida 129.

Evidencia 130 con resultados/método/hashes. Actualizados protocolo, trazabilidad, backlog, entregables y decisiones. AST, JSON y referencias comprobados. Una búsqueda incluyó test_security.py inexistente; se continuó con test_auth.py real. Sin pytest API ejecutado, latencia nueva, Docker, migraciones, cambios de contraseñas, configuración de uso o commit. Pendiente ejecutar autenticación existente y nueva en terminal de la autora; no repetir los sesenta tests sin cambios de correo/incidencias. RNF-2 continúa incumplido según 129 hasta nueva medición justificada.


## 22 de octubre de 2026 — Regresión de autenticación aprobada

La autora aportó captura de 22 passed in 13.84s para test_auth.py y test_auth_queries.py con plugins automáticos deshabilitados e integraciones DB apagadas. Evidencia 131: procedencia y hashes coincidentes con 130. Actualizados protocolo, trazabilidad, backlog y entregables; JSON/referencias/hashes comprobados. Sin repetir suites, modificar código/servicios o commit. No es carga, PostgreSQL o CI remoto. Pendiente medición full en QA nuevo para comparar con 129; no se acredita RNF-2 todavía.


## 22 de octubre de 2026 — Medición formal después de agrupar autenticación

Leído reporte real c7ad7be7ff304f58 y comparación con 791d2288a84d4872. Calentamiento 30 s y medición 300 s completos, diez clientes, 13072 solicitudes sin errores. p95 listado 236,6, detalle 206,2, creación 521,6 y edición 398,7 ms; mejoran las cuatro y aumentan solicitudes 16,4%, pero todas siguen fuera de <200 ms. SQL/conteos coinciden: 3629 casos/CREADO, 3516 ediciones y 36290 entregas, cero intentos SMTP/trabajos IA. Diez logout 204 y QA detenido.

Evidencia 132 y actualización de protocolo, trazabilidad, backlog y entregables. JSON, referencias y hashes de originales comprobados. Sin cambio de código, suite o carga adicional, ni commit. No son poblaciones finales idénticas y no se controló host/capacidad del generador: comparación observacional. Siguiente paso perfilar creación/edición antes de nueva optimización, conservando controles. RNF-2 incumplido.


## 22 de octubre de 2026 — Respuestas de escritura antes del commit

[Evidencia 133](evidencias/133-respuestas-escritura-sin-recarga.json): creación prepara el recibo bajo la transacción y las cuatro rutas de gestión capturan CaseDetail antes de confirmar. Solo se devuelve éxito tras commit; el servicio mantiene retorno ORM por defecto y Session conserva expire_on_commit. El cuerpo previo a queue_event de manage_case mantiene bloqueos, relectura de visibilidad, permisos y auditoría sin cambios por comparación AST.

Perfil aislado SQLite con cuerpos reales por AST: creación 14 → 11 consultas (después del commit: 4 → 0); edición 10 → 9 (1 → 0). Tres fallos simulados —commit de creación, commit de edición y presentador— conservaron caso, auditoría y cola sin cambios parciales. No ejecuta HTTP/Pydantic ni demuestra concurrencia PostgreSQL. Se prepararon 11 casos en backend/tests/test_write_responses.py, todavía pendientes de ejecutar con la regresión existente. Sin nueva medición Docker: RNF-2 continúa pendiente y la evidencia 132 conserva FALLA_UMBRAL.

Propósito: reducir recargas ORM posteriores al guardado sin relajar permisos ni serialización. Cambiados backend/app/services/incidents.py, backend/app/services/lifecycle.py y backend/app/api/incidents.py; nuevo test_write_responses.py. Validación: perfil antes/después, tres escenarios de rollback y AST; los 11 tests de API solo están preparados. Actualizados BACKLOG, ENTREGABLES, TRAZABILIDAD, PRUEBA_RENDIMIENTO y DECISIONES. Sin instalación de dependencias, carga Docker ni commit. Pendiente: ejecutar regresión API y, si pasa, una medición formal nueva.


## 22 de octubre de 2026 — Regresión de respuestas: preparación de tres casos corregida

[Evidencia 134](evidencias/134-regresion-escritura-correccion-fixtures.json): la autora ejecutó cinco archivos y obtuvo **79 aprobadas y 3 fallidas en 18,27 s**. Los tres fallos pertenecen al nuevo test_write_responses.py: dos peticiones de RH omitían el empleado afectado y devolvían 422; el fixture de transición marcaba clasificación vigente sin los campos exigidos por ck_incident_classification_valid. Se corrigió la preparación: afectado explícito y clasificación/asignación mediante las rutas reales antes de observar SQL. Las aserciones de respuesta, cero consultas posteriores al commit y rollback se conservan.

Solo cambió la preparación de backend/tests/test_write_responses.py; sin cambio de aplicación ni relajación de restricciones. AST comprobado, reejecución de los 11 casos pendiente. Los otros cuatro archivos pasaron en la ejecución aportada. RNF-2 continúa pendiente; no repetir carga hasta confirmar estos casos.

Propósito: resolver los tres errores de preparación introducidos en las pruebas de 133. Validación realizada: texto completo de pytest revisado, causas contrastadas con el test y la restricción de modelos, AST del archivo corregido válido. Resultado: corrección guardada, sin nuevo resultado pytest. Nueva evidencia 134 y actualización de cuatro documentos de seguimiento. Pendiente: ejecutar solo el archivo corregido; sin Docker, nuevas dependencias o commit.


## 22 de octubre de 2026 — Respuestas de escritura: 11 pruebas aprobadas

[Evidencia 135](evidencias/135-respuestas-escritura-11-aprobadas.json): captura de terminal de la autora confirma **11 passed in 5.52s** para backend/tests/test_write_responses.py después de corregir la preparación documentada en 134. Cubre recibos, cuatro respuestas de gestión sin consultas posteriores al commit, rollback por fallos de commit/presentador y retorno ORM compatible. SQLite y dependencias sustituidas; no acredita concurrencia PostgreSQL, autenticación real ni suite completa. El resultado inicial de 134 se conserva.

La regresión del archivo corregido queda aprobada; los otros cuatro archivos ya pasaron en la ejecución de 134. No se atribuyen a una ejecución conjunta nueva. Siguiente paso: una medición formal full aislada con el ajuste de 133. RNF-2 sigue pendiente hasta ese reporte; 132 conserva FALLA_UMBRAL.

Propósito: registrar el resultado real de la reejecución tras 134. Validación: comando, 100 % y resumen 11 passed in 5.52s leídos en captura aportada. Nueva evidencia 135 y cuatro documentos de seguimiento actualizados. Sin cambios de código, ejecución pytest por el agente, Docker ni commit. Pendiente: medir rendimiento formal y contrastar p95 por operación, errores y auditoría/colas del entorno QA aislado.


## 22 de octubre de 2026 — Medición posterior al ajuste de respuestas

[Evidencia 136](evidencias/136-rendimiento-respuestas-comparacion.json): corrida 3dabef717c5549c6 ejecutada por la autora; reporte original conserva FALLIDA_UMBRAL. Diez clientes, 30 s de calentamiento y 300 s completos de medición; 14346 solicitudes, cero errores, frente a 13072 anteriores.

| Operación | p95 anterior (ms) | p95 actual (ms) | Cambio |
| --- | ---: | ---: | ---: |
| listado | 236.55 | 249.83 | +5.6 % |
| detalle | 206.16 | 217.49 | +5.5 % |
| creacion | 521.57 | 449.40 | -13.8 % |
| actualizacion | 398.67 | 358.22 | -10.1 % |

Creación y edición mejoraron; listado y detalle aumentaron. Las cuatro siguen sobre el umbral de 200 ms. Conteos 100 → 439 → 4026; SQL confirma 4026 creaciones auditadas, 3919 ediciones, 40260 entregas en cola, cero intentos SMTP y cero trabajos IA. Diez sesiones revocadas con 204 y contenedores QA detenidos. Los hashes reportados de los tres archivos del ajuste coinciden con el código local.

Comparación observacional: población creciente y distinta, host compartido con generador, sin control exclusivo del entorno ni CPU del generador medida. No atribuir causalidad exclusiva ni identificar un cuello de botella a partir de estos agregados. RNF-2 sigue pendiente. No repetir full sin cambio; siguiente diagnóstico: medir coste por fase/consulta antes de optimizar de nuevo.

Propósito: contrastar la medición formal posterior a 133/135 con 132. Validación: lectura de ambos JSON, comparación de métricas, hashes de fuente y código, conteos SQL, logout y parada; evidencia releída. Sin ejecutar carga ni Docker desde herramientas, sin cambios de código o commit. Nueva evidencia 136 y cuatro documentos de seguimiento actualizados. Pendiente: diagnóstico temporal del coste restante y cumplimiento real de RNF-2.


## 22 de octubre de 2026 — Diagnóstico por etapas preparado

[Evidencia 137](evidencias/137-diagnostico-etapas-qa-preparado.json): entrada ASGI de diagnóstico exclusiva de QA y opción --diagnostic del provisionador, permitida solo con smoke. Mide por fase/operación total ASGI, autenticación real, endpoint, SQL, commit y cantidad de consultas. Guard de base/usuario/run_id, proveedores deshabilitados y sin datos privados en agregados. Las respuestas, permisos y bloqueos de producto se mantienen. Los agregados se recogen al detener QA y sus conteos se cruzan con las peticiones HTTP.

Validación local final: **40 unitarias aprobadas en 1,681 s**, con dobles ASGI sin sockets, propagación de contexto a hilos y Docker simulado. Incluye 13 casos nuevos y 27 anteriores. No hubo ejecución real de API/Docker; no se afirma integración aprobada. Dos intentos previos se interrumpieron durante creación de loop asyncio Windows; traza en socketpair/accept. Las dobles se adaptaron para no requerir sockets; esos intentos no se cuentan como aprobados.

RNF-2 sigue pendiente y 136 conserva FALLIDA_UMBRAL. El diagnóstico añade coste y dura 2+5 s de carga; no acredita rendimiento. SQL/commit se solapan con auth/endpoint: no sumar sus p95. SQL excluye pool/pre_ping interno y parte ORM; total ASGI excluye red/cliente. Primera corrida diagnóstica real pendiente.

Propósito: localizar coste restante sin repetir medición formal ciega. Archivos cambiados: backend/app/core/performance_timing.py, backend/app/core/performance_diagnostics.py, backend/scripts/performance_runner.py, backend/scripts/provision_performance_qa.py, backend/tests/test_performance_diagnostics.py, backend/tests/test_performance_provisioner.py. Actualizados BACKLOG, ENTREGABLES, TRAZABILIDAD, PRUEBA_RENDIMIENTO y DECISIONES; nueva evidencia 137. Validación: AST, suite unittest final y revisión del código instalado de FastAPI para rutas diferidas. Resultado local satisfactorio con alcance limitado; sin Docker desde herramientas, cambios de servicios de negocio, dependencias nuevas o commit. Pendiente: primera corrida smoke diagnóstica real y análisis de sus agregados.


## 22 de octubre de 2026 — Diagnóstico QA real revisado

[Evidencia 138](evidencias/138-diagnostico-etapas-qa-resultados.json): corrida e22ded0274034faf, estado DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2. Captura y reporte aportados por la autora: 231 peticiones en los 5 s medidos, cero errores; conteos de ocho grupos coinciden con las dos fases HTTP según validación del provisionador.

Medias por petición, en ms salvo cantidad de consultas. SQL y commit son subconjuntos solapados: no sumar columnas.

| Operación | ASGI | Auth | Endpoint | SQL | Commit | Consultas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| listado | 196.86 | 49.33 | 41.63 | 62.59 | 0.00 | 4.00 |
| detalle | 159.85 | 43.17 | 25.96 | 46.38 | 0.00 | 3.00 |
| creacion | 355.41 | 34.46 | 246.59 | 239.82 | 12.18 | 13.00 |
| actualizacion | 239.97 | 36.42 | 127.13 | 127.43 | 10.89 | 11.00 |

Creación concentra el mayor coste observado; SQL acumulado supera ampliamente al commit. Esto orienta la revisión a las 13 consultas y sus viajes, sin identificar una sentencia o causa única. Residual fuera de auth/endpoint entre 74,37 y 105,90 ms de media; no atribuirlo directamente a red o base: incluye planificación, dependencias, serialización y potencial limpieza posterior al envío. Total ASGI no equivale al tiempo HTTP cliente; sus p95 no son intercambiables.

Conteos 100 → 120 → 175; SQL confirma 175 creaciones auditadas, 73 ediciones, 1750 entregas, cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido. Smoke instrumentado corto, 54–61 muestras por operación; no acredita RNF-2 ni mejora frente a 136. Sin nueva modificación de código o carga completa. Pendiente: revisar coste y necesidad de consultas de creación preservando permisos/bloqueos; medir por familias si falta detalle.

Propósito: interpretar el diagnóstico de 137 antes de escoger otra optimización. Validación: JSON original, hash, conteos HTTP/instrumentación, verificación SQL, sesiones y parada contrastados. Nueva evidencia 138 y cuatro documentos de seguimiento actualizados. Sin ejecución Docker ni tests desde herramientas, sin cambio de servicios o commit. Resultado: diagnóstico disponible con límites explícitos; RNF-2 y causa detallada pendientes.


## 22 de octubre de 2026 — Relectura administrativa agrupada

[Evidencia 139](evidencias/139-relectura-administrativa-agrupada.json): administration_lock conserva el advisory compartido/exclusivo con clave 71419322 y, después de adquirirlo, relee usuario y departamento en una consulta con populate_existing. Sustituye tres lecturas del helper; no cachea permisos ni cambia transacciones. La identidad se obtiene sin cargar atributos expirados y el actor debe pertenecer a la Session actual. Filas ausentes o inactivas reciben 403 explícito. Llamadas sin actor conservan su comportamiento.

Perfil aislado SQLite de cuerpos reales por AST: creación **11 → 9** consultas; edición **9 → 7**, sin lecturas posteriores al commit. Catorce comprobaciones locales aprobaron actividad, cambios de rol/departamento, expiración, ausencias, identidad de Session y orden del SQL advisory simulado. No prueban concurrencia PostgreSQL ni HTTP/Pydantic. Se prepararon 14 casos pytest en test_administration_lock_queries.py, cuya ejecución con los servicios afectados sigue pendiente.

Sin medición formal nueva: el ahorro de consultas no garantiza p95. RNF-2 continúa pendiente y 136 conserva FALLIDA_UMBRAL. Próximo paso: regresión API/servicios; no repetir full hasta aprobarla.

Propósito: reducir viajes SQL administrativos observados tras 138. Cambiados backend/app/services/administration_lock.py y nuevo backend/tests/test_administration_lock_queries.py. Validación: AST del bloque PostgreSQL preservado, perfil antes/después y 14 comprobaciones locales con alcance descrito; pytest preparado pero no ejecutado. Primer helper de edición se detuvo por CRLF antes de modificar el servicio; normalización corregida y respaldo conservado. Evidencia 139 y cinco documentos de seguimiento/decisiones actualizados. Sin Docker, dependencias nuevas o commit. Pendiente: regresión de permisos y servicios consumidores en runtime compatible.


## 22 de octubre de 2026 — Regresión administrativa aprobada: 128 pruebas

[Evidencia 140](evidencias/140-regresion-administrativa-128-aprobadas.json): captura de la autora confirma **128 passed in 27.84s** en los ocho archivos seleccionados: relectura administrativa, incidencias, administración de usuarios, departamentos, IA, correo, respuestas de escritura y autenticación. Incluye los 14 casos nuevos preparados en 139. RUN_DB_TESTS=0 y autoload de plugins deshabilitado según terminal.

La regresión seleccionada del ajuste queda aprobada. No es suite completa ni demuestra concurrencia PostgreSQL. Próximo paso: una corrida full QA sin instrumentación diagnóstica para comparar con 136. RNF-2 sigue pendiente hasta el nuevo reporte; no se declara mejora de p95 a partir de estos tests.

Propósito: confirmar regresión del cambio de 139 antes de carga formal. Validación: comando, variables, progreso 100 % y resumen revisados en captura. Nueva evidencia 140 y cuatro documentos de seguimiento actualizados. Sin cambios de código, ejecución pytest por el agente, Docker o commit. Pendiente: medir p95 del ajuste en la corrida formal aislada.


## 22 de octubre de 2026 — Relectura administrativa: sin mejora de p95 en carga formal

[Evidencia 141](evidencias/141-rendimiento-relectura-administrativa.json): corrida e0b63b390b764550 sin instrumentación diagnóstica, diez clientes, 30 s de calentamiento y 300 s medidos completos. Resultado FALLIDA_UMBRAL: **13873 solicitudes sin errores**, frente a 14346 en 136.

| Operación | p95 anterior (ms) | p95 actual (ms) | Cambio |
| --- | ---: | ---: | ---: |
| listado | 249.83 | 286.91 | +14.8 % |
| detalle | 217.49 | 258.43 | +18.8 % |
| creacion | 449.40 | 505.98 | +12.6 % |
| actualizacion | 358.22 | 393.49 | +9.8 % |

Las cuatro aumentaron en p95; creación y edición bajaron ligeramente en mediana, lo cual no cumple ni sustituye el criterio. El ahorro local de consultas de 139 y la regresión aprobada de 140 no demostraron mejora de p95 aquí. El hash del helper coincide con el declarado por el reporte. Conteos 100 → 368 → 3837; SQL confirma 3837 creaciones auditadas, 3730 ediciones, 38370 entregas, cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido.

Comparación observacional con host compartido y población creciente distinta; las muestras CPU de contenedores no miden el generador ni explican por sí solas el resultado. No afirmar causa única ni relajar controles. RNF-2 continúa pendiente. No repetir full sin cambio justificado: investigar variabilidad, coste residual, consultas por familias y carga del generador/host.

Propósito: evaluar el efecto real de 139 después de 140. Validación: JSON originales, hashes, conteos HTTP/SQL, p95/medianas, logout y parada contrastados; CPU agregada por ventanas temporales con datetime.fromisoformat. Un intento previo en PowerShell no calculó CPU por conversión automática de fechas/cultura; sus muestras vacías se descartaron y no son resultados válidos. Nueva evidencia 141 y cuatro documentos actualizados. Sin cambios de código, carga Docker por el agente, nuevos tests o commit. Pendiente: diagnóstico del coste y variabilidad antes de otra prueba completa.


## 22 de octubre de 2026 — Diagnóstico v2: familias SQL, respuesta y CPU

[Evidencia 142](evidencias/142-diagnostico-familias-cpu-preparado.json): diagnóstico smoke ampliado para separar familias SQL y el tiempo de envío/cierre ASGI, más CPU del generador y del equipo Windows por fase. Sin cambios en servicios de negocio ni umbral RNF-2. Etiquetas SQL proceden de verbos/tablas conocidos; no se guardan consultas, parámetros o datos de casos. Las sumas por familia deben coincidir con cantidad y tiempo SQL global.

Validación local: **46 unitarias aprobadas en 2,536 s** (seis nuevas y 40 anteriores), con ASGI/Docker simulados y CPU sintética. Callbacks reales cargados por AST con SQLite agruparon las 9 consultas de creación y 7 de edición sin pérdidas. Sondeo GetSystemTimes disponible, pero intervalo inmediato sin delta válido se reportó NO_DISPONIBLE; no hubo medida real bajo carga. AST de siete archivos comprobado. Integración v2 real pendiente.

CPU del generador usa todos sus hilos y se presenta por núcleo/equipo; CPU host incluye otras aplicaciones/VM. Son medias de fase, sin atribución causal. hasta_envio marca entrega a ASGI, no recepción cliente; cierre cubre el resto. Familias pueden combinar consultas distintas y no equivalen a EXPLAIN. SQL/commit se solapan con auth/endpoint; no sumar p95. Instrumentación añade coste. RNF-2 continúa pendiente y 141 conserva FALLIDA_UMBRAL.

Propósito: orientar el próximo cambio con costes por familias y carga compartida tras 141. Archivos: backend/app/core/performance_timing.py, backend/app/core/performance_diagnostics.py, backend/scripts/performance_runner.py, backend/scripts/provision_performance_qa.py, backend/scripts/performance_host.py, backend/tests/test_performance_diagnostics.py, backend/tests/test_performance_provisioner.py. Nueva evidencia 142; actualizados BACKLOG, ENTREGABLES, TRAZABILIDAD, PRUEBA_RENDIMIENTO y DECISIONES. Validación y límites descritos arriba; no Docker desde herramientas, dependencias nuevas o commit. Pendiente: una corrida smoke v2 y revisión de sus datos antes de otra carga formal.


## 22 de octubre de 2026 — Diagnóstico v2 real: inserción de correo como mayor familia de creación

[Evidencia 143](evidencias/143-diagnostico-familias-cpu-resultados.json): corrida f7457a68919e4fb2 terminó DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2. Diez clientes, 2+5 s, **249 solicitudes medidas sin errores**. Los ocho grupos concuerdan con HTTP y sus familias suman consultas y tiempo SQL. Creación mantiene 11 consultas/petición y edición nueve, coherentes con el ahorro local de 139 más autenticación y advisory PostgreSQL.

En creación INSERT/mail_deliveries es la mayor familia: **66,05 ms de media por petición**, frente a 11–13,4 ms en la mayoría de otras familias y 22,25 ms de autenticación SQL. SQL acumulado medio 198,93 ms. Conteos confirman diez entregas por creación; una ejecución instrumentada no prueba cuántos viajes hace internamente el driver. Próxima revisión: forma de insertar varias MailDelivery juntas, conservando destinatarios, IDs, idempotencia y transacción.

Generador: 5,15 % de un núcleo / **1,29 % del equipo** de cuatro CPU; host global medio **73,64 %**. No demuestra saturación continua ni causa única. Creación: media hasta entregar último cuerpo a ASGI 303,97 ms y cierre 19,14 ms; total 323,11 ms. El cierre no explica todo el residual; no equivale a tiempo de recepción HTTP cliente. No sumar p95 de componentes solapados.

Conteos 100 → 124 → 185; SQL: 185 creaciones auditadas, 80 ediciones, 1850 entregas, cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido. Smoke con 60–66 muestras por operación y coste instrumental: no acredita RNF-2. 141 conserva FALLIDA_UMBRAL. No repetir full sin un cambio justificado y regresión previa.

Propósito: interpretar el diagnóstico ampliado de 142 para orientar el próximo ajuste. Validación: JSON original y hash, ocho grupos, sumas por familia, tiempos CPU/respuesta, auditoría/colas, sesiones y parada contrastados. Nueva evidencia 143 y cuatro documentos de seguimiento actualizados. Sin cambios de código de negocio, pruebas ejecutadas por el agente, Docker o commit. Pendiente: inspección de inserción de correo y validación de una alternativa antes de otra carga formal.


## 22 de octubre de 2026 — Entregas de correo en INSERT multirregistro

[Evidencia 144](evidencias/144-correo-insert-multirregistro.json): queue_event prepara las mismas filas y usa INSERT VALUES múltiples de hasta 50 entregas por sentencia. Diez destinatarios caben en una sentencia; se conservan UUID5, consulta de IDs existentes, destinatarios, contexto/estados y la misma transacción del caso/auditoría. Sin commit propio, SMTP o Redis. El worker y sus comprobaciones permanecen idénticos por AST.

Perfil local con SQLAlchemy/SQLite y cuerpos reales por AST: antes executemany con 2/10/30/123 juegos; ahora execute único para 2/10/30 y tres sentencias para 123. Compilación PostgreSQL válida, máximo 600 parámetros por bloque. No prueba viajes ni rendimiento PostgreSQL. Nueve escenarios de destinatarios coinciden con el control previo y revierten correctamente. Reintento parcial conserva fila ENVIADA y rellena la ausente; fallo del segundo bloque revierte filas previas y auditoría al hacer rollback.

Se prepararon seis casos en test_mail_multivalues.py. El test existente de fallo de outbox ahora intercepta INSERT real en lugar de objetos ORM pendientes; mantiene 503 y conteos cero de caso/auditoría/entregas. Pytest de API pendiente; no se declaran estas pruebas aprobadas. Sin p95 nuevo: RNF-2 sigue pendiente y 141 conserva FALLIDA_UMBRAL. Próximo paso: regresión de correo/incidencias/respuestas; después diagnóstico breve, sin repetir full automáticamente.

Propósito: probar forma alternativa de inserción de la familia más costosa de 143. Archivos cambiados: backend/app/services/mail.py, backend/tests/test_mail.py, backend/tests/test_mail_multivalues.py. Validación: perfiles antes/después con 2/10/30/123 filas, compilación PostgreSQL, matriz de nueve escenarios, dos escenarios adicionales de reintento/fallo y AST. Nueva evidencia 144 y cinco documentos de seguimiento/decisiones actualizados. Sin pytest API ejecutado por el agente, Docker, dependencias nuevas o commit. Pendiente: regresión compatible y diagnóstico real del INSERT antes de medir full.


## 22 de octubre de 2026 — Correo multirregistro: 77 pruebas aprobadas

[Evidencia 145](evidencias/145-correo-multirregistro-77-aprobadas.json): captura de la autora confirma **77 passed in 23.15s** en test_mail_multivalues.py, test_mail.py, test_mail_batching.py, test_incidents.py y test_write_responses.py. Incluye los seis casos nuevos preparados en 144 y el test de fallo de outbox adaptado al INSERT real. Variables visibles: SSLKEYLOGFILE vacío, RUN_DB_TESTS=0 y PYTEST_DISABLE_PLUGIN_AUTOLOAD=1.

Regresión seleccionada aprobada; no es suite completa ni medición PostgreSQL/rendimiento. Siguiente paso: una corrida smoke diagnóstica v2 para contrastar la familia INSERT/mail_deliveries con 143, preservando límites de comparación y verificación de conteos. No repetir full automáticamente. RNF-2 sigue pendiente y 141 conserva FALLIDA_UMBRAL.

Propósito: confirmar regresión del ajuste de 144 antes de medir su efecto real. Validación: comando, variables, progreso 100 % y resumen revisados en captura. Nueva evidencia 145 y cuatro documentos de seguimiento actualizados. Sin cambios de código, pytest ejecutado por el agente, Docker o commit. Pendiente: corrida diagnóstica breve del INSERT multirregistro.


## 22 de octubre de 2026 — Menor coste de INSERT correo, CPU host alta

[Evidencia 146](evidencias/146-diagnostico-correo-mejora-host-alto.json): diagnóstico 4fc3ea94293a4348 completó **150 solicitudes medidas sin errores**. La familia INSERT/mail_deliveries bajó de **66,05 a 16,94 ms medios por petición** (aprox. −74,4 %); hash del servicio coincide con el ajuste de 144. No es mejora global: creación ASGI media subió de 323,11 a 423,33 ms. CPU global media subió de **73,64 % a 95,27 %**, mientras generador bajó de 1,29 % a 0,68 % del equipo. Comparación observacional de smoke con cargas distintas; no causa única ni cumplimiento RNF-2.

Ocho grupos y sumas SQL/HTTP coherentes. SQL confirma 155 casos/creaciones auditadas, 41 ediciones, 1550 entregas y cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido. La muestra actual de procesos desde herramientas solo expuso pwsh; no sirve de inventario del host ni para identificar responsables.

Se preparó backend/scripts/check_performance_host.ps1, solo lectura y muestra breve de CPU por proceso en terminal de la autora. No cierra procesos ni cambia configuración; datos posteriores no explican retrospectivamente la corrida. Antes de repetir carga, revisar consumidores actuales. No repetir full automáticamente. RNF-2 continúa pendiente; 141 conserva FALLIDA_UMBRAL.

Propósito: contrastar la inserción multirregistro tras 145 y orientar la siguiente medición sin repetir carga bajo CPU alta. Validación: reportes JSON, hashes, ocho grupos, sumas de familias, auditoría/colas, CPU, logout y parada. Nueva evidencia 146 y cuatro documentos actualizados; script de CPU preparado, pendiente de análisis sintáctico. Sin cambio de producto, Docker desde herramientas, cierre de procesos o commit. Pendiente: sondeo en terminal del equipo y condiciones de medición antes de otra carga.


Comprobación posterior de 146: sintaxis de check_performance_host.ps1 validada con Parser de PowerShell sin errores; ejecución en terminal de la autora pendiente. Un primer análisis se inició mientras el helper de escritura seguía activo y no encontró el archivo; tras finalizar ese proceso se repitió solo la validación dependiente y pasó. Evidencia 146 actualizada con el resultado real.


## 22 de octubre de 2026 — Sondeo parcial de procesos y CPU global pendiente

[Evidencia 147](evidencias/147-sondeo-procesos-baseline-global.json): la autora aportó salida de 5,7 s, cuatro CPU, 252 procesos comparados y 214 lecturas no disponibles. Mayor consumidor visible 4,8 % del equipo; suma parcial del top 10, 19,47 %. Esa suma no es CPU global ni permite atribuir los 95,27 % de 146 a una aplicación: es una muestra posterior con cobertura parcial. No se indicó ni ejecutó cierre de procesos.

Se agregó `performance_host.py --baseline`, solo lectura: tres intervalos globales Windows de dos segundos, sin generar carga ni consultar procesos. Media ponderada con medidas válidas; ausencia se conserva como null. **48 pruebas locales aprobadas en 1,880 s**, dos nuevas, con CPU sintética y Docker/ASGI simulados. Baseline en terminal de la autora pendiente. RNF-2 sigue pendiente; no repetir full automáticamente.

Propósito: evitar atribución errónea de CPU a partir de inventario parcial y preparar línea base global. Cambiados backend/scripts/performance_host.py y backend/tests/test_performance_diagnostics.py. Validación: salida aportada revisada, suma parcial distinguida de CPU global, AST válido y suite local 48/48. Nueva evidencia 147 y cuatro documentos actualizados. Sin Docker, cierre de procesos, dependencias nuevas o commit. Pendiente: obtener muestra global actual desde terminal de la autora antes de decidir otra carga.


## 22 de octubre de 2026 — CPU global 97,42 % sin carga generada

[Evidencia 148](evidencias/148-cpu-global-baseline-97-4.json): salida aportada por la autora de performance_host.py --baseline. Tres intervalos válidos: 92,12 %, 99,82 % y 100,00 %; media ponderada **97,42 %** durante aproximadamente 6,4 s. El script no genera carga de prueba, pero otras aplicaciones/servicios/VM pueden estar activos. La medida es actual y no atribuye retrospectivamente los resultados anteriores a una causa exclusiva.

No repetir benchmark bajo estas condiciones. Próximo paso: contrastar CPU global y procesos ordenados por consumo en Administrador de tareas; no cerrar procesos automáticamente. La lista parcial de 147 no identifica al responsable. RNF-2 sigue pendiente y 141 conserva FALLIDA_UMBRAL; no cambiar el umbral ni declarar correcto el rendimiento del producto.

Propósito: registrar la línea base global posterior a 147 antes de otra carga. Validación: salida completa revisada y media ponderada recalculada a partir de tres intervalos; JSON releído. Nueva evidencia 148 y cuatro documentos actualizados. Sin cambios de código, pruebas adicionales, Docker, cierre de procesos o commit. Pendiente: contraste visual de consumo y disponibilidad del equipo antes de medir rendimiento.


## 22 de octubre de 2026 — Rendimiento: informe consolidado y mediciones diferidas

[Evidencia 149](evidencias/149-rendimiento-informe-consolidado.json): PRUEBA_RENDIMIENTO.md consolidado en el mismo archivo; corrige el encabezado obsoleto «medición real no ejecutada», reúne cinco formales cotejadas con sus JSON, protocolo y uso actual, diagnóstico v2 y pendientes. Todos los enlaces JSON previos se conservan; no se reescriben reportes originales ni se crean versiones paralelas del informe.

Revisión estática acotada de correo: mismo hash que diagnóstico 146, sin commit propio, UUID5 y lotes de 50 conservados; consumidores consultan filas persistidas. Sin cambio de servicios ni repetición de tests/carga. La autora usa Brave para videollamada; última captura CPU 32 %/memoria 84 % es observación instantánea. Mantener actividad y diferir mediciones de carga hasta después de la llamada. RNF-2 permanece pendiente; última formal 141 no incluye INSERT multirregistro y no se declara mejora global.

Propósito: eliminar contradicción del estado inicial y facilitar revisión del requisito mientras no se mide durante la videollamada. Cambiados PRUEBA_RENDIMIENTO.md, BACKLOG.md, ENTREGABLES.md y TRAZABILIDAD.md; nueva evidencia 149. Validación: JSON de cinco corridas, p95/solicitudes, enlaces locales y conservación de referencias, AST/ausencia de commit y hash de correo. Sin pruebas ejecutadas adicionales, Docker, cambios de código funcional, nuevos archivos de versión del informe o commit. Pendiente: retomar medición después de la llamada con condiciones registradas y mismo criterio RNF-2.


## 22 de octubre de 2026 — Sexta formal: mejora observada, umbral pendiente

[Evidencia 150](evidencias/150-rendimiento-formal-correo-multirregistro.json): corrida c0baad3867644ad2 sin diagnóstico, diez clientes y 30+300 s completos; **15349 solicitudes sin errores** frente a 13873 de 141. p95 listado 286,91 → 259,28 ms; detalle 258,43 → 221,32; creación 505,98 → 385,49; edición 393,49 → 347,43. Las cuatro mejoran y siguen >=200 ms. No acreditar RNF-2 ni atribuir causalidad exclusiva: el host y la población difieren.

Conteos 100 → 502 → 4341; auditoría confirma 4341 creaciones, 4231 ediciones y 43410 entregas; cero SMTP/IA. Diez logout 204 y QA detenido. Hash de correo coincide con INSERT multirregistro; captura previa CPU 19 %/memoria 86 % es instantánea, sin medir toda la ventana. Informe consolidado actualizado en el mismo archivo con sexta fila y estado vigente. No repetir full sin otro cambio/diagnóstico justificado.

Propósito: evaluar efecto formal del INSERT multirregistro tras 145–149. Validación: reportes originales y hashes, cuatro p95/solicitudes, duración/concurrencia, auditoría/colas, logout y parada; enlaces locales del informe comprobados. Nueva evidencia 150 y actualización de PRUEBA_RENDIMIENTO.md, BACKLOG, ENTREGABLES y TRAZABILIDAD. Sin cambios funcionales, tests/carga ejecutados por el agente, Docker o commit. Pendiente: coste restante y RNF-2; no declarar cierre por mejora parcial.


## 22 de octubre de 2026 — Rol validado reutilizado dentro de la gestión

[Evidencia 151](evidencias/151-gestion-rol-leido-una-vez.json): helper privado puro para construir el mismo predicado de visibilidad con rol ya validado. La entrada pública sigue leyendo rol; manage_case lo valida tras bloqueo administrativo y eligible_manager al validar responsable. Reuso local a esa operación, sin cachear entre peticiones ni cambiar bloqueo de caso antes de reevaluar visibilidad.

Perfil aislado SQLite de funciones reales por AST: edición **7 → 6** consultas, creación **9 → 9**. Seis comprobaciones locales aprobaron gestores permitidos, empleado denegado, responsables y bajada de rol entre peticiones con actor obsoleto. Nueve escenarios de destinatarios conservaron resultados/rollback. Predicado y SELECT de bloqueo del caso idénticos por AST. No prueba FastAPI/Pydantic ni concurrencia PostgreSQL. Seis casos pytest preparados en test_lifecycle_role_queries.py; ejecución pendiente. Sin p95 nuevo: 150 sigue fuera de umbral y es anterior a este cambio.

Propósito: reducir consulta repetida observada en SELECT/roles de gestión sin retirar controles. Archivos: backend/app/services/incidents.py, backend/app/services/lifecycle.py, backend/tests/test_lifecycle_role_queries.py. Validación: perfil antes/después, seis comprobaciones y nueve escenarios por AST/SQLite; predicado, SELECT de bloqueo y funciones no afectadas comparados por AST. Nueva evidencia 151; informe consolidado y BACKLOG/ENTREGABLES/TRAZABILIDAD/DECISIONES actualizados. Sin pytest API ejecutado por el agente, Docker, dependencias nuevas o commit. Pendiente: regresión de servicios afectados antes de otra medición.


## 22 de octubre de 2026 — Reutilización del rol: 75 pruebas aprobadas

[Evidencia 152](evidencias/152-gestion-rol-regresion-75-aprobadas.json): captura de la autora confirma **75 passed in 12.91s** en cinco archivos: consultas de rol en gestión, incidencias, administración de usuarios, correo y respuestas de escritura. Incluye los seis casos nuevos de 151. Variables y comando visibles; RUN_DB_TESTS=0. Regresión seleccionada aprobada, sin suite completa o prueba de concurrencia PostgreSQL.

Informe consolidado actualizado: 151 ya tiene regresión API seleccionada, pero no diagnóstico/formal posterior. Las 77 pruebas anteriores son otra selección y no se suman como únicas. Próximo paso: una corrida smoke diagnóstica para revisar SELECT/roles, conteos y condiciones; no repetir full automáticamente. RNF-2 continúa pendiente y 150 conserva FALLIDA_UMBRAL.

Propósito: registrar regresión real del ajuste de 151. Validación: variables, comando de cinco archivos, 100 % y resumen revisados en captura; JSON releído e informe actualizado. Nueva evidencia 152; PRUEBA_RENDIMIENTO.md, BACKLOG, ENTREGABLES y TRAZABILIDAD actualizados. Sin cambios funcionales, pytest ejecutado por el agente, Docker o commit. Pendiente: diagnóstico breve del coste restante antes de otra formal.


## 22 de octubre de 2026 — Una lectura de rol confirmada en diagnóstico real

[Evidencia 153](evidencias/153-gestion-rol-diagnostico-real.json): corrida 33d131e588f1435a terminó DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2. **229 solicitudes medidas sin errores**; edición pasó de 9 a 8 consultas y SELECT/roles de dos a una por petición. Hashes de los dos servicios coinciden con el código del ajuste. Ocho grupos y sumas por familia concordantes.

CPU global media 81,06 %; generador 0,38 % del equipo. Edición ASGI media 247,80 ms: auth 49,56 ms, endpoint 110,98 ms y residual 87,25 ms. No sumar p95 ni atribuir a una causa única; smoke corto y condiciones distintas. SQL confirma 178 casos/creaciones auditadas, 70 ediciones, 1780 entregas, cero SMTP/IA. Diez logout 204 y QA detenido.

Reducción SQL prevista confirmada, sin acreditar latencia formal. Informe consolidado actualizado; 150 sigue siendo la última de seis formales fallidas. RNF-2 pendiente. Revisar costes comunes antes de otra formal y no repetir full automáticamente.

Propósito: contrastar diagnóstico del ajuste 151 tras regresión 152. Validación: JSON original, hash, conteos por fase/familia, CPU, auditoría/colas, logout y parada; hashes de servicios verificados. Nueva evidencia 153 y PRUEBA_RENDIMIENTO.md/BACKLOG/ENTREGABLES/TRAZABILIDAD actualizados. Sin cambios funcionales, tests adicionales, Docker desde herramientas o commit. Pendiente: costes compartidos y RNF-2, sin declarar aprobación por ahorro de una consulta.


## 22 de octubre de 2026 — Diagnóstico v3 de espera/retorno de hilos preparado

[Evidencia 154](evidencias/154-diagnostico-esperas-hilos-preparado.json): instrumentación opcional solo en la entrada QA de anyio.to_thread.run_sync. Categorías fijas distinguen autenticación, endpoint, validación de respuesta, apertura/cierre de dependencia y otras. Mide espera/ejecución/retorno, sin guardar argumentos/resultados o cambiar limiter/cancelación, sin reintentos. Llamadas incompletas y sumas discordantes invalidan el agregado. No cambia aplicación normal ni servicios de negocio.

**56 unitarias locales aprobadas en 1,251 s**, ocho nuevas; dobles ASGI/ejecutor y contexto en hilo real, sin servidor FastAPI/AnyIO o Docker real. Primera corrida v3 pendiente. Instrumentación añade coste y sus componentes se solapan: no sumar p95 ni atribuir causa única. RNF-2 pendiente y 150 conserva FALLIDA_UMBRAL. Solo un smoke diagnóstico nuevo se justifica; no repetir full automáticamente.

Propósito: desglosar residual de 153 antes de elegir el siguiente cambio. Archivos: backend/app/core/performance_timing.py, backend/app/core/performance_diagnostics.py, backend/scripts/provision_performance_qa.py, backend/tests/test_performance_diagnostics.py, backend/tests/test_performance_provisioner.py. Validación: revisión de código instalado FastAPI/Starlette/AnyIO, AST de cinco archivos y suite local 56/56. Evidencia 154; informe consolidado, BACKLOG, ENTREGABLES, TRAZABILIDAD y DECISIONES actualizados. Sin carga Docker desde herramientas, cambios de producto, dependencias nuevas o commit. Pendiente: primera integración v3 real y análisis de etapas antes de otra formal.


## 22 de octubre de 2026 — Esperas y retornos de hilos medidos

[Evidencia 155](evidencias/155-diagnostico-hilos-resultados.json): diagnóstico 19f2fbae76134abb completó **224 solicitudes medidas sin errores**, ocho grupos, sumas SQL/hilos concordantes y cero llamadas incompletas. En edición, cinco pasos por hilo: espera media 42,09 ms, retorno 36,24 ms y ejecución 130,01 ms; ASGI total medio 215,31 ms. Apertura y validación de respuesta ejecutan menos de 0,1 ms cada una, pero espera/retorno suman unos 15,00 y 13,85 ms respectivamente.

Cierre posterior al envío: ejecución 0,049 ms y espera/retorno 17,71 ms en estas escrituras; no representa todo el cierre posible de lecturas ni toda la latencia cliente. CPU host media 80,26 %. No sumar p95 ni atribuir a limiter/OS/GIL una causa única. SQL confirma 184 casos/creaciones, 73 ediciones, 1840 entregas, cero SMTP/IA. Diez logout 204 y QA detenido.

Orientación: evaluar reducción acotada de pasos de tareas pequeñas, manteniendo SQL y rollback/cierre bloqueante en worker, validación y limpieza ante errores/cancelación. Sin modificación funcional nueva o p95 formal; 150 conserva FALLIDA_UMBRAL y RNF-2 pendiente. No repetir carga automáticamente.

Propósito: analizar primera integración v3 de 154. Validación: JSON original y hash, ocho grupos, sumas, llamadas completas, auditoría/colas, CPU, logout y parada cotejados. Nueva evidencia 155; informe consolidado y BACKLOG/ENTREGABLES/TRAZABILIDAD actualizados. Sin cambio de producto, tests ejecutados adicionales, Docker desde herramientas o commit. Pendiente: cambio acotado basado en el desglose y regresión antes de otra medición.


## 22 de octubre de 2026 — Apertura de sesión sin paso por worker

[Evidencia 156](evidencias/156-sesion-apertura-sin-salto-hilo.json): get_session es generador asíncrono. Construye Session sin consultas/checkout; mantiene autenticación, endpoints y SQL en sus workers. El cierre potencialmente bloqueante usa worker, CapacityLimiter(1) independiente y protección CancelScope(shield=True). Sin commit implícito ni supresión/reintentos de errores. Busca retirar únicamente el paso de apertura señalado por 155; no cambia permisos, auditoría o cola.

**7 pruebas locales aprobadas en 0,143 s**, con SQLAlchemy/SQLite y worker reales, dobles de AnyIO sin event loop. Comprueban entrada sin SQL/salto, rollback en worker, commit conservado, cierre único, errores/CancelledError inyectada, fallo de cierre y factory. **Tres integraciones AnyIO/FastAPI preparadas, todavía no ejecutadas**, y regresión API pendiente; las locales no acreditan cancelación real. No repetir carga antes de esa regresión. RNF-2 pendiente, sin nuevo p95; 150 conserva FALLIDA_UMBRAL.

Propósito: retirar una planificación de tarea no bloqueante con base en 155. Archivos: backend/app/core/database.py y backend/tests/test_database_session.py. Validación: siete unitarias locales, AST, revisión de integración de Depends y del limiter independiente de FastAPI; alcance y pendientes arriba. Evidencia 156, PRUEBA_RENDIMIENTO, BACKLOG, ENTREGABLES, TRAZABILIDAD y DECISIONES actualizados. Sin Docker, nueva medición, dependencias, cambios en servicios o commit. Pendiente: tres integraciones reales y regresión API antes de valorar diagnóstico.


## 22 de octubre de 2026 — Regresión de sesión asíncrona: 93 aprobadas

[Evidencia 157](evidencias/157-sesion-asincrona-regresion-93-aprobadas.json): la autora ejecutó los siete archivos solicitados con RUN_DB_TESTS=0 y plugins automáticos desactivados; captura muestra **93 passed in 17.43s**, 100 %, sin errores. Incluye los diez casos de test_database_session.py y sus tres integraciones AnyIO/FastAPI reales: cierre con limiter general ocupado, limpieza ante cancelación de ámbito y rollback de la dependencia original tras HTTP 200/409. Hashes actuales coinciden con 156; no son prueba retrospectiva del proceso capturado.

La regresión seleccionada del ajuste 156 queda aprobada, sin equivaler a suite completa ni PostgreSQL/Docker real. No sumar siete locales como pruebas adicionales. RNF-2 continúa pendiente, sin nuevo p95; 150 conserva FALLIDA_UMBRAL. Próximo paso: un smoke diagnóstico para contrastar retirada del salto de apertura, integridad de auditoría/colas y cierre; no repetir full automáticamente.

Propósito: registrar validación real seleccionada del cambio 156. Validación: comando, tres variables, progreso y resultado revisados en captura; hashes actuales cotejados con 156 y JSON releído. Nueva evidencia 157 e informe consolidado actualizado. Sin cambios funcionales, tests ejecutados de nuevo por el agente, Docker o commit. Pendiente: diagnóstico breve del efecto antes de valorar otra formal.


## 22 de octubre de 2026 — Diagnóstico de sesión interrumpido en arranque QA

[Evidencia 158](evidencias/158-sesion-smoke-arranque-incompleto.json): corrida cc10cf1d32dd4a8d terminó **INCOMPLETA**, código ARRANQUE_QA_SALIDA_1 después de validar configuración. Compose falló construyendo/iniciando; no llegó a migraciones, fixture, carga ni tiempos por hilos. Parada no confirmada (contenedores_detenidos=false, parada_requiere_revision=true); comprobar estados sin asumir que siguen en ejecución. Recursos retenidos sin borrar volúmenes.

Causa raíz no disponible en el reporte resumido; no atribuir a código, RAM, disco o permisos. Antes de repetir: comprobar servidor Docker y estados del proyecto exacto. La regresión seleccionada 157 de 93 aprobadas se conserva; efecto de 156 y RNF-2 pendientes. No hay p95 nuevo ni cambio de producto en este avance.

Propósito: conservar fallo real y detener repeticiones sin diagnóstico. Validación: captura, JSON original/hash, ruta de error y parada en provision_performance_qa.py y listado de archivos revisados. Evidencia 158, informe consolidado y documentos de estado actualizados. Sin ejecución Docker/test, modificación funcional, borrados o commit. Pendiente: disponibilidad Docker/estado del proyecto y causa de arranque antes de otra carga.


## 22 de octubre de 2026 — Docker disponible y proyecto QA sin contenedores

[Evidencia 159](evidencias/159-docker-disponible-qa-sin-contenedores.json): captura de la autora confirma servidor Docker 29.6.1 y listado sin filas para el filtro exacto del proyecto cc10cf1d32dd4a8d. En esta consulta no hay contenedores de esa corrida por detener. No demuestra ausencia de volúmenes/redes/imágenes ni reconstruye el estado durante el fallo; reporte 158 intacto.

Causa de arranque todavía pendiente. Dockerfile/specification revisados: siguiente diagnóstico acotado es construir solo la imagen QA con salida plain, sin servicios ni carga. Sin nueva medición, borrados, cambios funcionales o pruebas adicionales; 157 conserva 93 aprobadas y RNF-2 sigue pendiente.

Propósito: verificar disponibilidad/parada tras 158. Validación: dos comandos/resultados leídos en captura, construcción definida en Dockerfile y specification inspeccionada; JSON releído. Sin Docker desde herramientas ni commit. Pendiente: salida de construcción para identificar si el fallo se reproduce.


## 22 de octubre de 2026 — Construcción explícita de imagen QA completada

[Evidencia 160](evidencias/160-imagen-qa-construida-diagnostico-pendiente.json): salida aportada por la autora muestra construcción/exportación/naming/unpacking completos de plurione-qa-perf-cc10cf1d32dd4a8d-api:latest, sin ERROR. Pasos de aplicación/dependencias en caché; no es instalación limpia ni arranque de servicios. El fallo 158 no se reprodujo en esta construcción, pero su causa histórica sigue desconocida.

Tras disponibilidad y ausencia de contenedores comprobadas en 159, corresponde un único reintento de smoke diagnóstico con proyecto nuevo para verificar arranque completo y efecto de 156. Sin full, sobrescritura o borrado de la corrida fallida. 157 mantiene 93 aprobadas; no hay p95 nuevo y RNF-2 pendiente.

Propósito: registrar diagnóstico acotado de construcción antes de reintentar carga. Validación: salida textual #0–#12 revisada, caché y digest/exportación identificados; JSON releído. Informe consolidado actualizado. Sin Docker/test desde herramientas, modificación funcional o commit. Pendiente: arranque completo y smoke diagnóstico.


## 22 de octubre de 2026 — Segundo fallo QA antes de generar carga

[Evidencia 161](evidencias/161-segundo-fallo-arranque-qa-sin-medicion.json): corrida 6bcb02bfdbe040ad vuelve a INCOMPLETA/ARRANQUE_QA_SALIDA_1 tras validar configuración, antes de migraciones/fixture/carga; parada no confirmada. Reporte original y hash conservados. La construcción correcta 160 no explica este fallo; command() solo conserva el código por privacidad.

Se observaron 16 carpetas de corridas; cada configuración reserva dos redes y stop las conserva. Posible agotamiento de direcciones por comprobar, sin inferir inventario real a partir de carpetas. Siguiente paso acotado: crear red interna temporal vacía con nombre aleatorio y retirar solo esa red si se creó correctamente; observar error original. No repetir smoke/full, iniciar servicios o borrar redes existentes. Sin resultados nuevos de rendimiento; 157 mantiene 93 aprobadas y RNF-2 pendiente.

Propósito: conservar fallo repetido y acotar diagnóstico. Validación: captura/JSON/hash cotejados, command/specification/parada y pruebas del provisionador leídos; 16 carpetas contadas. Nueva evidencia 161 e informe consolidado actualizado. Sin Docker/tests desde herramientas, cambio funcional, borrados o commit. Pendiente: resultado de asignación de red y revisión del estado de la nueva corrida.


## 22 de octubre de 2026 — Pools de direcciones agotados: limpieza QA acotada preparada

[Evidencia 162](evidencias/162-redes-direcciones-agotadas-limpieza-preparada.json): la prueba de red devolvió «all predefined address pools have been fully subnetted», confirmando el agotamiento actual. Es consistente con los fallos de arranque 158/161, sin recuperar su stderr histórico. La red de prueba no se creó.

Nueva release_performance_networks.py: revisión por defecto; --apply --limit 2 retira hasta dos redes QA vacías con nombre/etiquetas, reporte y compose originales concordantes. Exige contexto Docker local, revalida ID/uso/propiedad antes de rm, no toca contenedores, imágenes, volúmenes o reportes. No hace prune global ni cambia la retención automática del provisionador.

**63 pruebas locales aprobadas en 1,401 s**, siete nuevas de limpieza, con Docker simulado. AST de dos archivos correcto. Liberación real pendiente de ejecutar por la autora; no repetir carga antes de comprobarla. La selección API 157 mantiene 93 aprobadas y RNF-2 pendiente, sin nuevo p95.

Propósito: resolver de forma acotada el agotamiento que impide arrancar QA. Archivos: backend/scripts/release_performance_networks.py y backend/tests/test_performance_network_release.py; evidencia 162, README, informe consolidado y DECISIONES actualizados. Validación: captura, código de propiedad/revalidación, 63 unitarias y AST. Sin Docker real desde herramientas, borrados ejecutados, cambios en producto o commit. Pendiente: resultado de limpieza real y nuevo diagnóstico solo con recursos disponibles.


## 22 de octubre de 2026 — Dos redes QA liberadas sin errores

[Evidencia 163](evidencias/163-liberacion-real-dos-redes-qa.json): la autora ejecutó release_performance_networks.py --apply --limit 2. La salida enumera 28 redes elegibles antes de aplicar y confirma únicamente dos eliminadas: 897c25b02d4340d6_net y d1c2d490b7df42b4_net, con prefijo plurione-qa-perf-. Sin omitidas al revalidar ni fallidas. No equivale a eliminar las 28 listadas ni a inventario global; herramienta limitada a redes QA vacías registradas, sin contenedores/volúmenes/imágenes/reportes o prune.

La limpieza real de 162 queda observada. Procede un smoke diagnóstico nuevo para comprobar reserva efectiva de dos redes, arranque completo y efecto del ajuste de sesión 156; no liberar más automáticamente ni lanzar full. No hay medición nueva, RNF-2 pendiente y 157 mantiene 93 aprobadas. Reportes 158/161 intactos.

Propósito: registrar liberación acotada real tras agotamiento confirmado. Validación: salida textual revisada, nombres/cantidad/límite y listas vacías cotejados; JSON releído. Evidencia 163 e informe consolidado actualizados. Sin Docker/tests desde herramientas, cambios funcionales o commit. Pendiente: nuevo smoke diagnóstico y revisión de sus resultados.


## 22 de octubre de 2026 — Diagnóstico real: cuatro pasos por hilo confirmados

[Evidencia 164](evidencias/164-sesion-diagnostico-cuatro-hilos-resultados.json): corrida 077bbcf2cb8d4142 completó **249 peticiones medidas sin errores** tras liberar dos redes en 163. Ocho grupos v3 y sumas concordantes, cuatro pasos por hilo en todos los grupos (antes cinco), sin dependency_enter ni llamadas incompletas. Hash de database.py coincide con 156. Cierre registrado como other, SQL en worker conservado.

SQL por petición listado/detalle/creación/edición: 4/3/11/8. Conteo HTTP 100 → 120 → 181; PostgreSQL confirma 181 casos/creaciones auditadas, 73 ediciones, 1810 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido.

El objetivo estructural se confirma; no hay mejora global de latencia demostrada. Edición ASGI media 269,85 ms frente a 215,31 en 155; commit medio 66,42 frente a 11,14 ms, p95 de commit actual 356,23 ms. Espera/retorno medios de hilos 32,71/32,02 ms frente a 42,09/36,24. CPU global media 68,02 %, generador 1,16 % del equipo. Smoke corto instrumentado y condiciones variables: no sumar p95 ni atribuir causa única.

HTTP p95 de este smoke: listado 190,86; detalle 203,76; creación 465,74; edición 488,66 ms. No acredita RNF-2 ni sustituye la formal 150 FALLIDA_UMBRAL. Siguiente revisión: coste de commit/endpoint y alcance de la temporización antes de otro ajuste; no repetir full automáticamente.

Propósito: contrastar integración y efecto de 156 tras recuperación de infraestructura. Validación: captura, reporte original/hash, código declarado, read_diagnostics v3, ocho grupos, sumas SQL/hilos, CPU, auditoría/colas, logout y parada revisados. Nueva evidencia 164 e informe consolidado actualizados. Sin cambios funcionales, tests nuevos, Docker desde herramientas o commit. Pendiente: investigar variación de commit/endpoint y RNF-2, sin afirmar mejora por retirar un paso.


## 22 de octubre de 2026 — Alcance del commit revisado sin cambios de durabilidad

[Evidencia 165](evidencias/165-revision-alcance-commit-sin-sql-pendiente.json): revisión de servicios y SQLAlchemy instalado, más dos comprobaciones locales con funciones extraídas por AST y modelos/SQLite reales. Creación y edición con presenter confirman una vez en Session y driver, con cero objetos nuevos/sucios/borrados al entrar en before_commit y cero SQL/flush hasta after_commit. No hay trabajo redundante identificado dentro de ese intervalo en los escenarios comprobados.

El cronómetro QA acaba antes de expiración (_remove_snapshot) y cierre; el servicio ya ejecutó flush y captura del esquema antes de commit. Los 66,42 ms medios de edición en 164 no representan esas tareas posteriores. Incluyen confirmación del driver y esperas no separadas; no atribuir a WAL/disco/red/GIL una causa única con estos agregados. No se cambian commit, durabilidad, atomicidad, auditoría o permisos.

Otra oportunidad acotada de 164: validación de respuesta ejecuta 0,029 ms dentro del hilo y espera/retorna 15,45 ms. Siguiente revisión de implementación: consolidar preparación/validación de DTO en el worker del endpoint, preservando validación y sin SQL en el event loop. Sin nueva instrumentación, carga o latencia en este avance. RNF-2 pendiente; regresión 157 y formal 150 conservan su alcance.

Propósito: separar alcance del cronómetro y trabajo de confirmación antes de optimizar. Validación: callbacks QA y orden en SQLAlchemy/servicios inspeccionados; dos escenarios locales completados, JSON/hash registrados. Evidencia 165 e informe consolidado actualizados. Sin modificaciones funcionales, Docker, nueva carga o commit Git. Pendiente: diseño acotado para el paso de validación de respuesta; causa de la variación PostgreSQL no determinada y RNF-2 sin acreditar.


## 22 de octubre de 2026 — DTO validado en el worker del endpoint preparado

[Evidencia 166](evidencias/166-respuesta-validada-en-worker-preparada.json): worker_response agrupa ejecución original y captura/validación de Receipt/CasePage/CaseDetail en un trabajo de hilo para listado, detalle, registro y edición. La ruta es async con firma preservada; response_model y serialización de FastAPI se conservan sobre DTO ya preparado. No pasa ORM/SQL al event loop, ni cambia seguridad, SQL, locks, commit, auditoría, cola o cierre. Errores de salida mantienen ResponseValidationError y loc=response; excepciones del servicio se propagan.

Diagnóstico QA adaptado para medir el worker y conservar async. Endpoint incluye ahora la preparación/validación de DTO, sin espera/retorno: declarar esa diferencia de alcance al comparar. Se esperan tres pasos por hilo frente a cuatro, todavía sin ejecución QA real. Misma versión v3 y categorías, con clasificación del worker conocido como endpoint.

**7 pruebas locales del ajuste aprobadas en 0,054 s** con hilo/Pydantic reales y offload simulado; **64 unitarias de herramientas aprobadas en 1,661 s**, una nueva. AST de seis archivos y cuatro rutas correcto. Dos integraciones FastAPI nuevas preparadas, sin ejecutar; regresión API pendiente. Sin nueva carga/latencia ni aprobación RNF-2. Las 93 de 157 corresponden al ajuste anterior y no validan este cambio.

Propósito: retirar planificación separada de validación pequeña observada en 164, tras revisión 165. Archivos: core/worker_response.py, api/incidents.py, core/performance_diagnostics.py, core/performance_timing.py, tests/test_worker_response.py y tests/test_performance_diagnostics.py bajo backend/app o backend/tests. Validación: siete locales, 64 de herramientas, AST/firma/errores y QA worker revisados. Evidencia 166, informe consolidado, BACKLOG/ENTREGABLES/TRAZABILIDAD y DECISIONES actualizados. Sin Docker, nuevas dependencias, modificación transaccional o commit Git. Pendiente: dos integraciones y regresión API antes de medir.


## 22 de octubre de 2026 — Regresión DTO en worker: 102 aprobadas

[Evidencia 167](evidencias/167-respuesta-worker-regresion-102-aprobadas.json): captura de la autora muestra **102 passed in 16.77s**, 100 %, ocho archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye nueve casos del nuevo helper y sus dos integraciones FastAPI reales: un offload de endpoint sin otro de validación de salida, y HTTP 500 ante DTO inválido. También incluye sesión/AnyIO, autenticación, incidencias, administración, correo y respuestas de escritura.

Hashes actuales de los seis archivos coinciden con preparación 166; no prueba retrospectiva de identidad del proceso. Selección aprobada, sin sumar siete locales anteriores ni extrapolar a suite completa/PostgreSQL. Antes de otro smoke diagnóstico, liberar como máximo dos redes QA vacías con herramienta validada y comprobar que se retiraron dos sin fallos; la corrida 164 volvió a reservar dos. No iniciar carga si esa comprobación falla. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL; sin nueva latencia o limpieza ejecutada por el agente.

Propósito: registrar regresión real del ajuste 166 antes de medirlo. Validación: comando/variables/progreso/resultado de captura revisados; seis hashes cotejados y JSON releído. Evidencia 167 e informe consolidado actualizados. Sin modificaciones funcionales, nuevos tests desde herramientas, Docker, limpieza o commit. Pendiente: limpieza acotada verificada y smoke diagnóstico de tres pasos por hilo.


## 22 de octubre de 2026 — DTO en worker: tres pasos por hilo confirmados

[Evidencia 168](evidencias/168-respuesta-worker-diagnostico-tres-hilos.json): limpieza previa de d1c2d490b7df42b4_entry y 42486b8ff1264162_net (prefijo plurione-qa-perf-) retiró dos redes sin fallos; el bloque condicionó la carga a ese resultado. Corrida 485d89bb828f4582 completó **236 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Tres pasos por hilo en todos los grupos (auth/endpoint/other), frente a cuatro en 164; sin validación en otro hilo, apertura o llamadas incompletas. Hashes de cuatro archivos de aplicación/instrumentación coinciden con 166.

Consultas por listado/detalle/creación/edición conservadas en 4/3/11/8. HTTP 100 → 130 → 190 casos; PostgreSQL confirma 190 casos/creaciones auditadas, 78 ediciones, 1900 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido.

HTTP p95 del smoke: listado 302,70; detalle 243,36; creación 427,86; edición 312,76 ms. Frente a 164, escritura mejora y lectura empeora; no hay mejora general o atribución causal demostrada. CPU global media 84,20 % frente a 68,02 %, generador 1,00 %. Commit de edición vuelve a 11,89 ms medios/p95 34,69, sin cambiar durabilidad: el pico previo no se repitió. ASGI edición media 220,86 ms; cierre 30,64 ms. Endpoint incluye ahora preparación/validación de DTO, alcance distinto declarado en 166.

Objetivo estructural confirmado y regresión 167 de 102 aprobadas conservada. RNF-2 pendiente; no sustituir formal 150 FALLIDA_UMBRAL ni repetir full automáticamente. Próxima revisión: viajes SQL y condiciones del entorno con base en evidencia, sin rebajar controles o durabilidad.

Propósito: contrastar efecto e integración de 166 tras regresión 167. Validación: salida de limpieza/smoke, reporte original/hash, cuatro hashes de código, read_diagnostics, grupos/sumas/CPU, auditoría/colas, logout y parada cotejados. Evidencia 168 e informe consolidado actualizados. Sin cambio funcional, tests nuevos, Docker desde herramientas o commit. Pendiente: RNF-2 y siguiente mejora justificada, sin atribuir causa única al cambio.


## 22 de octubre de 2026 — Rol agrupado en relectura posterior al bloqueo preparado

[Evidencia 169](evidencias/169-rol-agrupado-tras-bloqueo-preparado.json): administration_lock mantiene su modo anterior (None y lectura de usuario/departamento) y añade include_role=True para devolver el rol válido leído con LEFT JOIN en esa misma relectura posterior al advisory lock. Creación y gestión usan ese rol; el recibo usa el mismo predicado con rol validado. Sin caché entre solicitudes ni cambios de lock de expediente, escritura/commit, auditoría, colas o cierre. Ausencias/inactividad/rol desconocido conservan denegaciones y mensajes.

**9 unitarias locales aprobadas en 0,188 s** con servicios/modelos/SQLite reales. Cubren frescura de usuario/rol, no caché entre llamadas, rol ausente/desconocido, cuenta inactiva, compatibilidad previa, actor persistente y orden del lock compartido/exclusivo simulado. Perfil con funciones extraídas por AST antes/después: creación 9 → 8 y edición 6 → 5 consultas, sin SQL después de commit; no incluye autenticación ni advisory PostgreSQL. En QA se espera 11 → 10 y 8 → 7, sin acreditarlo todavía. AST de cinco archivos correcto.

Regresión API pendiente: las 102 de 167 validan el cambio anterior. No se ejecutó nueva carga o limpieza de redes ni se demostró latencia; RNF-2 pendiente y formal 150 FALLIDA_UMBRAL. Las escrituras usan advisory compartido; el perfil SQLite no lo ejecuta. No repetir diagnóstico antes de regresión.

Propósito: ahorrar un viaje SQL de rol preservando revalidación después de bloqueo. Archivos: services/administration_lock.py, services/incidents.py, services/lifecycle.py bajo backend/app; tests/test_administration_role_join.py y tests/test_lifecycle_role_queries.py bajo backend. Validación: nueve unitarias, perfiles SQL antes/después y AST; evidencia 169, informe consolidado y DECISIONES actualizados. Sin Docker, HTTP real, nuevas dependencias o commit. Pendiente: regresión seleccionada y, si pasa, diagnóstico real acotado con capacidad de redes verificada.


## 22 de octubre de 2026 — Rol agrupado: 98 pruebas y cuatro subpruebas aprobadas

[Evidencia 170](evidencias/170-rol-agrupado-regresion-98-aprobadas.json): captura de la autora muestra **98 passed, 4 subtests passed in 11.72s**, 100 %, siete archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye nueve nuevas pruebas de rol agrupado y regresión de lock/rol de gestión, incidencias, administración, correo y respuestas transaccionales. Cuatro subpruebas registradas por separado; no convertir en 102 pruebas únicas ni sumar selecciones anteriores.

Hashes actuales de cinco archivos coinciden con preparación 169, sin prueba retrospectiva de identidad del proceso. Regresión seleccionada aprobada, sin acreditar PostgreSQL/concurrencia o latencia. Próximo paso justificado: un smoke diagnóstico tras liberar y verificar dos redes QA vacías, condicionado a dos eliminaciones sin fallos. Creación 11 → 10 y edición 8 → 7 consultas siguen siendo expectativa en QA, no observación real. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL.

Propósito: registrar regresión real seleccionada del ajuste 169 antes de medir. Validación: captura/comando/variables/progreso/resultados cotejados, cinco hashes comparados y JSON releído. Evidencia 170 e informe consolidado actualizados. Sin cambios funcionales, tests adicionales, Docker, limpieza o commit desde herramientas. Pendiente: integración QA real y análisis de SQL/latencia dentro del alcance diagnóstico.


## 22 de octubre de 2026 — Rol agrupado confirmado en PostgreSQL QA

[Evidencia 171](evidencias/171-rol-agrupado-diagnostico-sql-confirmado.json): limpieza previa retiró 42486b8ff1264162_entry y d1c50f8001464425_entry (prefijo plurione-qa-perf-), sin omitidas/fallidas, antes del smoke condicionado. Corrida b2bda80fd89d433c completó **202 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Hashes de los tres servicios coinciden con 169. Creación pasó de 11 a 10 consultas y edición de 8 a 7; listado/detalle mantienen 4/3. SELECT de usuario/área/rol sustituye al SELECT/roles individual en las dos escrituras y ambas fases. Tres pasos por hilo, sin incompletas.

HTTP 100 → 128 → 178 casos; PostgreSQL confirma 178 casos/creaciones auditadas, 68 ediciones, 1780 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido. Regresión 170 de 98 pruebas/cuatro subpruebas conservada.

HTTP p95: listado 366,18; detalle 273,95; creación 760,44; edición 423,13 ms, todos peores que 168 y fuera del umbral. CPU global media 88,72 % frente a 84,20 %, generador 0,76 % del equipo. Ahorro SQL confirmado, sin mejora de latencia demostrada. No atribuir a CPU/código una causa exclusiva: smoke corto, instrumentado, conjunto final y condiciones distintos. RNF-2 pendiente; formal 150 FALLIDA_UMBRAL sigue vigente. No repetir full/smoke sin otra hipótesis o cambio justificado.

Propósito: contrastar integración y efecto de 169 tras regresión 170. Validación: salida de limpieza/smoke, JSON original/hash, tres hashes de código, ocho grupos/sumas/consultas/familias/hilos, CPU, auditoría/colas, logout y parada cotejados. Evidencia 171 e informe consolidado actualizados. Sin cambio funcional, tests adicionales, Docker desde herramientas o commit. Pendiente: RNF-2 y siguiente acción justificada, sin ocultar latencia adversa ni encadenar repeticiones.


## 22 de octubre de 2026 — Listado y detalle con un viaje SQL menos preparados

[Evidencia 172](evidencias/172-lecturas-listado-detalle-agrupadas-preparadas.json): listado agrupa count y página autorizada en una sentencia con LEFT JOIN desde el agregado; conserva total con página vacía/fuera de rango, filtros y orden created_at/id descendente. Detalle/visible_case lee Role.nombre y expediente autorizado en un SELECT; conserva 403 para rol no habilitado y 404 para caso ausente/oculto, sin caché. Los tres roles usan los mismos predicados previos. Autenticación/escrituras/transacciones y DTO/worker no cambian; visible_case compartido mantiene contrato para historial/participantes/correo.

**11 pruebas locales aprobadas en 1,323 s**, con funciones/modelos/Pydantic/SQLite reales. Matriz de 56 actor/caso y listado para siete actores coinciden con predicado anterior. Cubren páginas vacías/fuera de rango, filtros, orden empatado/sin duplicados, 403/404, no SQL al capturar DTO y compilación PostgreSQL. Listado local 3 → 2 consultas y detalle 2 → 1, sin autenticación; se espera QA 4 → 3 y 3 → 2. AST de tres archivos correcto.

Regresión HTTP/API pendiente. SQL más complejo puede tener otro coste de planificación/ejecución; no se acredita latencia por reducir viajes. Sin nueva carga/limpieza o cambios de permisos/commit. Las 98 pruebas/cuatro subpruebas de 170 validan código anterior; RNF-2 pendiente y formal 150 FALLIDA_UMBRAL. No repetir diagnóstico hasta regresión.

Propósito: reducir viajes de lecturas tras 171, sin cambiar autenticación o cachear rol. Archivos: backend/app/services/incidents.py, backend/app/api/incidents.py y backend/tests/test_read_query_grouping.py. Validación: once unitarias, matriz de permisos, conteos SQL y dialecto PostgreSQL; AST, evidencia 172 e informe/DECISIONES actualizados. Sin HTTP real, Docker, nuevas dependencias, nuevas cargas o commit. Pendiente: regresión de API/seguridad y después diagnóstico acotado con capacidad de redes verificada.


## 22 de octubre de 2026 — Lecturas agrupadas: 111 pruebas y 63 subpruebas aprobadas

[Evidencia 173](evidencias/173-lecturas-agrupadas-regresion-111-aprobadas.json): captura de la autora muestra **111 passed, 63 subtests passed in 22.41s**, 100 %, ocho archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye once nuevos casos de agrupación y subpruebas de matriz de permisos/listado, además de regresión seleccionada de incidencias, correo, respuestas/DTO, autenticación y administración. Subpruebas reportadas por separado; no son 174 pruebas únicas ni se suman selecciones anteriores.

Hashes actuales de tres archivos coinciden con 172, sin prueba retrospectiva de identidad del proceso. Regresión seleccionada aprobada; plan/ejecución y latencia PostgreSQL siguen pendientes. Próximo paso: smoke diagnóstico de listado 4 → 3 y detalle 3 → 2, condicionado a liberar/verificar dos redes QA vacías. No full automático ni resultado anticipado de mejora. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL.

Propósito: registrar regresión real seleccionada de 172 antes de medir. Validación: captura/comando/variables/progreso/resultados cotejados, tres hashes comparados y JSON releído. Evidencia 173 e informe consolidado actualizados. Sin modificación funcional, tests adicionales, Docker, limpieza o commit desde herramientas. Pendiente: integración/diagnóstico QA y revisión de latencias en su alcance corto.


## 23 de octubre de 2026 — Lecturas agrupadas confirmadas en PostgreSQL QA

[Evidencia 174](evidencias/174-lecturas-agrupadas-diagnostico-sql-confirmado.json): limpieza previa retiró d1c50f8001464425_net y 791d2288a84d4872_net (prefijo plurione-qa-perf-), sin fallos/omitidas; el bloque verificó el resultado antes de cargar. Corrida 1c455546c34c4d0f completó **203 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Hashes de los dos archivos coinciden con 172. Listado pasó de 4 a 3 consultas y detalle de 3 a 2 en ambas fases; escrituras 10/7 sin cambios. Tres pasos por hilo y cero incompletas.

HTTP 100 → 123 → 173 casos. PostgreSQL confirma 173 casos/creaciones auditadas, 69 ediciones, 1730 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido. Regresión 173 de 111 pruebas/63 subpruebas conservada.

HTTP p95: listado 285,30; detalle 347,96; creación 474,43; edición 371,37 ms. Tres operaciones mejoran frente a 171 y detalle empeora (273,95 → 347,96), sin causa exclusiva demostrada. CPU global media 83,16 %, generador 1,14 %. En detalle, SQL medio baja 61,37 → 52,85 ms, pero endpoint sube 40,52 → 54,40 y ASGI 198,27 → 230,48. La diferencia incluye construcción/compilación, fetch/ORM, validación y planificación; no identifica por sí sola el origen. SQL combinado de rol/caso medio 21,26 ms frente a 36,45 de los dos SELECT anteriores; no sumar p95.

Ahorro de viajes confirmado, sin mejora general o cumplimiento RNF-2. Mantener formal 150 FALLIDA_UMBRAL y todos los reportes. Siguiente revisión: tramo de detalle fuera del cursor antes de más cambios/cargas. No repetir full/smoke automáticamente.

Propósito: registrar integración y resultado mixto del ajuste 172 tras regresión 173. Validación: salida de limpieza/smoke, reporte original/hash, dos hashes de código, ocho grupos/sumas/SQL/hilos/CPU, auditoría/colas, logout y parada cotejados. Evidencia 174 e informe consolidado actualizados con fecha de registro real del cliente (23/10). Sin cambios funcionales, tests adicionales, Docker desde herramientas o commit. Pendiente: RNF-2 y análisis acotado del coste fuera de cursor de detalle.


## 23 de octubre de 2026 — Plantilla SQL de detalle sin datos por petición preparada

[Evidencia 175](evidencias/175-detalle-plantilla-sql-parametrizada-preparada.json): perfil local de 174 identificó reconstrucción de predicados/aliases. _visible_case_statement conserva solo una estructura SQL con cuatro bindparams tipados, sin recibir actor/Session/UUID real/rol vigente/resultados. visible_case pasa diccionario nuevo con parámetros actuales y vuelve a consultar Role.nombre y caso autorizado en cada ejecución. Misma SQL/política/403/404 y cantidad de viajes; ninguna caché de permisos o datos. Primera construcción concurrente duplicada es inocua y no comparte parámetros.

Perfil propio SQLite, una muestra fría y treinta calientes por proceso: construcción media caliente 7,53 → 0,005 ms, total 9,01 → 0,52 ms; frío 18,17 → 20,14 ms (una muestra, sin mejora demostrada). No equivale a latencia HTTP/PostgreSQL o RNF-2. **17 pruebas locales aprobadas en 1,371 s**, seis nuevas de ausencia de datos en plantilla, parámetros frescos, confidencialidad/rol cambiantes y dos sesiones/hilos concurrentes sin mezcla de permisos. Once anteriores conservan matriz/orden/total/filtros, conteo SQL y compilación PostgreSQL. AST de dos archivos válido.

Regresión API pendiente; las 111 pruebas/63 subpruebas de 173 validan código anterior. Sin nueva carga/Docker/limpieza, cambios de autenticación, writes/commit, locks, auditoría/colas o DTO. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL conservada. No medir antes de regresión.

Propósito: retirar trabajo Python repetido de detalle identificado con perfil local, sin caché de autorización. Archivos: backend/app/services/incidents.py y backend/tests/test_detail_sql_template.py. Validación: perfil local antes/después, 17 unitarias, concurrencia SQLite y AST; evidencia 175 e informe/DECISIONES actualizados. Sin HTTP real, PostgreSQL, nuevas dependencias, carga o commit. Pendiente: regresión API y diagnóstico real solo si pasa, manteniendo capacidad de redes verificada.


## 23 de octubre de 2026 — Plantilla de detalle: 117 pruebas y 63 subpruebas aprobadas

[Evidencia 176](evidencias/176-plantilla-detalle-regresion-117-aprobadas.json): captura de la autora muestra **117 passed, 63 subtests passed in 22.73s**, 100 %, nueve archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye seis casos nuevos de estructura sin datos, parámetros independientes, permisos/rol cambiantes y sesiones concurrentes SQLite, además de la matriz y regresión API seleccionada anterior. Conteos separados; no son 180 pruebas únicas ni se acumulan con selecciones anteriores.

Hashes actuales de dos archivos coinciden con 175, sin prueba retrospectiva de identidad del proceso. Regresión seleccionada aprobada; el microperfil local no demuestra p95 HTTP/PostgreSQL. Corresponde un smoke diagnóstico para contrastar el tramo de endpoint y latencia de detalle, conservando conteos SQL e integridad. Antes, liberar/verificar dos redes QA vacías. No full automático. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL.

Propósito: registrar regresión real seleccionada de 175 antes de medir. Validación: captura/comando/variables/progreso/resultados cotejados, dos hashes comparados y JSON releído. Evidencia 176 e informe consolidado actualizados. Sin cambios funcionales, tests adicionales, Docker, limpieza o commit desde herramientas. Pendiente: integración QA real y comparación de detalle dentro del alcance corto instrumentado.


## 23 de octubre de 2026 — Plantilla de detalle: mejora localizada, p95 pendiente

[Evidencia 177](evidencias/177-plantilla-detalle-diagnostico-endpoint-reducido.json): limpieza previa retiró 791d2288a84d4872_entry y c7ad7be7ff304f58_net (prefijo plurione-qa-perf-), sin fallos/omitidas, antes de cargar. Corrida fd78431c613f4e14 completó **218 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Hash de incidents.py coincide con 175; diferencias de código declarado registradas. SQL listado/detalle/creación/edición 3/2/10/7 y tres pasos por hilo sin incompletas, como antes.

HTTP 100 → 110 → 164 casos. PostgreSQL confirma 164 casos/creaciones auditadas, 60 ediciones, 1640 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido. Regresión 176 de 117 pruebas/63 subpruebas conservada.

Detalle: endpoint medio 54,40 → 25,98 ms, ASGI medio 230,48 → 209,92 y mediana HTTP 186,72 → 148,69. Mejora localizada compatible con retirar construcción repetida; p95 HTTP empeora 347,96 → 360,31 ms. HTTP p95 listado/detalle/creación/edición actual 588,84/360,31/479,34/313,43 ms: solo edición mejora frente a 174. CPU global media 80,43 %, generador 0,99 %. Espera media de hilos de detalle 61,42 ms y residual ASGI 126,52; cierre medio 50,72 ms incluye trabajo posterior al envío y no equivale a latencia cliente. No sumar p95 ni atribuir causa única.

El ahorro de trabajo local aparece en endpoint, sin mejora general o cumplimiento RNF-2. Formal 150 FALLIDA_UMBRAL y todos los reportes se conservan. No repetir full/smoke sin otra hipótesis o cambio justificado.

Propósito: contrastar integración y mejora localizada de 175 tras regresión 176. Validación: salida de limpieza/smoke, reporte original/hash, código declarado/diferencias, ocho grupos/sumas/SQL/hilos/CPU, auditoría/colas, logout y parada cotejados. Evidencia 177 e informe consolidado actualizados. Sin cambios funcionales, tests adicionales, Docker desde herramientas o commit. Pendiente: RNF-2, variabilidad/esperas compartidas y siguiente acción justificada, sin convertir microperfil o endpoint medio en aprobación de p95.


## 27 de octubre de 2026 — Formal condicionada preparada; CPU previa alta

[Evidencia 178](evidencias/178-formal-condicionada-preparada-cpu-previa-alta.json): quince archivos cubiertos por regresiones y 53 de la identidad QA 177 coinciden sin diferencias. Aplicación sin cambios desde 175; no se implementó otra refactorización de autenticación tras la interrupción. Sondeo real de solo lectura del agente, sin carga generada: tres intervalos válidos 67,63/91,62/51,56 %, media ponderada **70,29 %**. No identifica responsable ni condiciones de corridas anteriores.

Nuevo run_performance_full_guarded.py: requiere confirmación QA, mide CPU antes de comandos Docker; solo sigue con tres muestras válidas, media <=30 % e intervalos <=50 %. Son umbrales operativos de arranque, no RNF-2 ni garantía de carga constante. Si no cumple, NO_INICIADA_CPU_PREVIA sin Docker/redes. Si cumple, verifica Docker local y libera hasta dos redes QA vacías; exige dos eliminadas sin fallos/omitidas. Después llama full una vez, sin diagnóstico API, manteniendo protocolo 30+300 s, diez clientes y p95<200 ms. precondiciones_arranque conserva línea base/umbrales/redes en el reporte original, sin reescribir anteriores.

**74 unitarias locales aprobadas en 1,839 s**, diez nuevas; CPU/Docker simulados. AST de cuatro archivos correcto. El nuevo comando completo no se ejecutó en Docker real; con la línea base observada no corresponde iniciar carga ahora. No se ejecutó séptima formal o smoke, no hay p95 nuevo; RNF-2 pendiente y formal 150 FALLIDA_UMBRAL conservada. Las 117 pruebas/63 subpruebas de 176 siguen siendo la última regresión de aplicación.

Propósito: pasar de diagnósticos sucesivos a validación formal del conjunto actual con condición previa verificable. Archivos: scripts/run_performance_full_guarded.py y scripts/provision_performance_qa.py bajo backend; tests/test_performance_full_guard.py y tests/test_performance_provisioner.py. Validación: hashes, línea base real, 74 unitarias y AST; evidencia 178, README, informe/DECISIONES actualizados. Primer guardado impedido por permisos fuera de raíces; acceso renovado y guardado/pruebas completados. Sin modificación de producto, Docker real, carga, limpieza o commit. Pendiente: integración real del comando cuando la CPU previa cumpla; no reintentar en bucle o aprobar por condiciones iniciales.


## 27 de octubre de 2026 — Formal no iniciada por CPU previa del usuario

[Evidencia 179](evidencias/179-formal-no-iniciada-cpu-previa-usuario.json): ejecución real del comando condicionado compartida por el usuario, estado **NO_INICIADA_CPU_PREVIA**. Tres intervalos válidos: 77,82/94,93/78,52 %, media ponderada **83,74 %**. Supera los límites operativos de media <=30 % e intervalo <=50 %. El flujo se detuvo antes de Docker, limpieza o carga; no produjo séptima formal ni p95 nuevo. Se comprobó el rechazo real por CPU alta; el camino con CPU baja y la formal completa siguen pendientes.

Sin cambios de aplicación o herramientas ni nuevas pruebas de API. Se conservan las seis formales FALLIDA_UMBRAL, las 117 pruebas/63 subpruebas de 176 y el criterio RNF-2 p95<200 ms por operación con diez clientes. El requisito continúa pendiente. La medición no identifica procesos responsables ni explica retrospectivamente las formales. Siguiente paso: observación actual de solo lectura o esperar a menor actividad; preservar Brave si continúa la videollamada y evitar reintentos en bucle.

Propósito: registrar fielmente la integración de la guardia y evitar nuevas cargas con CPU previa alta. Archivos: evidencia 179 y cinco documentos de seguimiento/informe. Validación: salida aportada por el usuario y lectura del flujo de guardia documentado en 178; JSON y referencias locales comprobados. Pendiente: condiciones de arranque y medición formal del conjunto actual.


## 27 de octubre de 2026 — Sondeo parcial de procesos tras rechazo de arranque

[Evidencia 180](evidencias/180-sondeo-procesos-lecturas-incompletas.json): salida aportada por el usuario, 5,34 s, cuatro CPU lógicas, 156 procesos comparados y 201 lecturas no disponibles (no necesariamente procesos distintos). Diez consumos visibles suman aproximadamente 8,12 %; máximo Docker Desktop 4,31 %. No es CPU global ni muestra simultánea con el 83,74 % de 179, por lo que no identifica responsable ni demuestra una contradicción. La frase genérica del script «posterior a la carga» no acredita carga nueva: el intento 179 no inició.

Sin cambios de código, carga o pruebas adicionales. RNF-2 pendiente, seis formales conservadas. Pendiente: observar CPU global y procesos simultáneamente en Administrador de tareas, orden descendente por CPU, sin cerrar servicios por conjetura ni afectar la videollamada. No repetir benchmarks mientras se identifica la actividad del equipo.

Propósito: interpretar las limitaciones del sondeo sin atribuir causalidad. Archivos: evidencia 180 y cinco documentos de seguimiento/informe. Validación: transcripción de diez filas, suma y JSON comprobados; no nuevas pruebas de aplicación. Resultado: diagnóstico de procesos inconcluso; observación simultánea pendiente.


## 27 de octubre de 2026 — Arranque QA incompleto; excepciones y tiempos distinguibles

[Evidencia 181](evidencias/181-arranque-incompleto-diagnostico-excepciones.json): tras detener desarrollo, CPU previa 28,35 % y dos redes QA retiradas sin errores permitieron iniciar 66f8604531244a51. Resultado INCOMPLETA / ARRANQUE_QA_NO_COMPLETADO, antes de migraciones, fixture y carga; parada confirmada. API creada 20:38:31 UTC, iniciada 20:38:38 y detenida 20:38:46 con salida 0, sin OOM y check /health correcto. Redis tuvo dos PONG y salida 0; PostgreSQL listo y luego detenido ordenadamente. No demuestra un fallo de salud durante arranque. La fecha inicial del reporte no marca el comienzo exacto de compose up; el codigo anterior agrupaba TimeoutExpired/OSError y no permite confirmar retrospectivamente cual ocurrio.

Se distingue ahora *_TIEMPO_AGOTADO de *_ERROR_INVOCACION y se guarda arranque_qa con inicio/fin UTC, duracion, limite y resultado. Limite de 900 s y carga formal sin cambios; no se publican stdout/stderr/argumentos privados. **76 unitarias locales aprobadas en 2,722 s**, dos nuevas; Docker simulado y AST valido. Sin nueva ejecucion Docker/carga ni cambios de producto. Reporte original preservado con hash. RNF-2 pendiente; no septima medicion formal completada. Pendiente: un intento explicito condicionado con diagnostico preciso, sin bucle ni aumento especulativo de plazo.

Proposito: evitar atribuir timeout sin evidencia y registrar excepcion/tiempo precisos. Archivos: backend/scripts/provision_performance_qa.py, backend/tests/test_performance_provisioner.py, evidencia 181 y cinco documentos. Primer guardado bloqueado sin cambios; permiso de escritura concedido para este turno y cambio/pruebas completados. Validacion y limites detallados arriba.


## 27 de octubre de 2026 — Septima formal completa: FALLIDA_UMBRAL

[Evidencia 182](evidencias/182-septima-formal-completa-fallida-umbral.json), run 0769b0ce07b943e5: CPU previa 21,53 %, dos redes vacias liberadas sin errores; arranque QA OK en 30,54 s. Se completo 30 s de calentamiento y 300 s de medicion con diez clientes, sin instrumentacion diagnostica de API. **9.603 solicitudes de medicion, cero errores HTTP**. p95: listado **438,45 ms**, detalle **361,19 ms**, creacion **687,49 ms**, actualizacion **554,30 ms**. Las cuatro operaciones incumplen p95<200 ms; RNF-2 sigue pendiente. Es la septima formal completada, diferente de los intentos no iniciados o incompletos.

Conteos 100 iniciales ->326 tras calentamiento ->2.725 finales. SQL: 2.725 incidencias y eventos de creacion, 2.620 eventos de edicion, 27.250 entregas encoladas, cero intentos SMTP y trabajos IA. Comprobaciones HTTP posteriores OK, diez logout 204 y contenedores detenidos. Hashes declarados coinciden con archivos actuales. Reporte original preservado mediante hash; sin nueva carga ni cambios de producto.

Los cuatro p95 son mayores que en formal 150 (259,28/221,32/385,49/347,43 ms). No atribuir causalidad: codigo, entorno y crecimiento de datos difieren. La CPU previa baja no garantiza CPU baja durante la carga; la formal no registra CPU global Windows durante medicion ni desglose interno. No permite culpar a Avast o una optimizacion concreta. Conservar las siete formales fallidas. Pendiente: revisar perfiles existentes del camino de creacion y costes compartidos antes de otra carga; no repetir sin hipotesis nueva ni relajar permisos/auditoria/durabilidad/umbral.

Proposito: registrar el resultado formal real del conjunto actual. Archivos: evidencia 182 y cinco documentos de seguimiento/informe. Validacion: lectura del reporte original, completitud/ventanas/clientes, suma de solicitudes y errores, consistencia SQL/HTTP, parada y hashes. No pruebas nuevas de codigo ni Docker ejecutado por el agente. Resultado adverso preservado; siguiente trabajo requiere hipotesis tecnica.


## 27 de octubre de 2026 — Outbox: compilacion reutilizada por lote

[Evidencia 183](evidencias/183-outbox-insertmanyvalues-compilacion-reutilizada.json): perfil local acotado de 31 creaciones ENTORNO reales (una fria +30 calientes con cProfile, diez RH ficticios, SQLite/Session nueva) detecto recompilacion de INSERT multirregistro: queue_event 575,20/860,44 ms acumulados de create_case; compilacion 250,02 ms en 30 llamadas. No es perfil HTTP/PostgreSQL. Se cambia solo insercion final del outbox a Core INSERT..RETURNING(id) con lista de parametros en execute, insertmanyvalues_page_size=50 y segmentos de 50, cerrando resultado. Mismos destinatarios, UUID, campos, idempotencia y transaccion; sin cache de autorizacion, commits adicionales o proveedores externos.

Perfil despues: primera CACHE_MISS y 30 CACHE_HIT, frente a 31 NO_CACHE_KEY; media caliente **28,78->18,35 ms** (36,23 % menor localmente). Fria 53,43->66,30 ms: no se demuestra mejora en frio. No extrapolar al p95 HTTP. Se comprobo ejecucion fisica de tres INSERT para 123 filas, cero cursor.executemany, <=600 parametros por lote. SQLAlchemy 2.1.4/dialecto psycopg anuncian soporte y se compila RETURNING para PostgreSQL; ejecucion real PostgreSQL pendiente. [Documentacion oficial](https://docs.sqlalchemy.org/en/20/core/dml.html).

**8 nuevas unitarias aprobadas en 0,659 s y 19 casos existentes de servicios, total 27 finales en 2,450 s**. Incluyen campos/UUID, mezcla de eventos/casos, destinatarios vigentes/omision, reintentos, fallo en segundo lote y rollback completo de creacion con 503. Casos existentes ejecutados por puente directo SQLite, no HTTP/TestClient. Primer puente habia usado ENTORNO donde el caso affected_rh requiere PERSONA; se corrigio fixture y se aprobaron todos sin relajar restriccion. Conteos SQL locales mantienen creacion 8 (5 SELECT/3 INSERT), edicion 5 (3 SELECT/1 INSERT/1 UPDATE), sin SQL posterior al commit. AST de tres archivos correcto.

Pendiente regresion API por el usuario y comprobacion real PostgreSQL antes de decidir otra formal. Sin nueva carga Docker, formal o smoke; RNF-2 pendiente y siete formales FALLIDA_UMBRAL conservadas, ultima 182. No atribuir el resultado a Avast ni declarar mejora formal por este perfil.

Proposito: reducir recompilacion demostrada en creacion sin cambiar semantica. Archivos: backend/app/services/mail.py, tests/test_outbox_cached_insert.py y test_mail_multivalues.py, evidencia 183 y documentos. Validacion/resultado/limites arriba. Pruebas previas que exigian executemany=False se adaptaron a estilo INSERTMANYVALUES; nuevas pruebas observan cursor fisico para no confundir metadato logico con llamadas por fila. No commit Git ni alteracion de reportes anteriores.


## 27 de octubre de 2026 — Regresion de outbox: 85 pruebas aprobadas

[Evidencia 184](evidencias/184-regresion-api-outbox-85-aprobadas.json): el usuario ejecuto pytest con seis archivos (outbox_cached_insert, mail_multivalues, mail_batching, mail, incidents, write_responses), resultado **85 passed in 17.90s**. Seleccion mixta de unitarias y API; no son 85 HTTP exclusivamente. RUN_DB_TESTS=0, autoload de plugins deshabilitado y sin cacheprovider. Tres hashes de implementacion/pruebas de 183 coinciden; tambien se registran hashes de los seis archivos seleccionados. Sin cambios de codigo en este avance.

Valida la seleccion funcional/atomica de la mejora 183; no valida PostgreSQL real ni p95. Las siete formales fallidas se conservan y RNF-2 continua pendiente. Pendiente un unico smoke diagnostico PostgreSQL QA aislado, con liberacion acotada de dos redes vacias previamente comprobada; revisar conteos/auditoria/outbox, cero proveedores externos, errores HTTP, perfil SQL/hilos y parada. No repetir formal ni acreditar por smoke.

Proposito: registrar regresion real antes de integracion QA. Archivos: evidencia 184 y cinco documentos de seguimiento/informe. Validacion: salida del usuario, hashes de 183 y JSON comprobados. Resultado 85 aprobadas; sin nuevas pruebas ejecutadas por el agente ni modificacion de producto/reportes anteriores. Pendiente PostgreSQL QA y criterio RNF-2.


## 27 de octubre de 2026 — Outbox integrado en PostgreSQL QA; escrituras aun sobre umbral

[Evidencia 185](evidencias/185-outbox-diagnostico-postgresql-integrado.json), run 746faa7071714c1e: usuario libero dos redes QA vacias sin fallos/omitidas e inicio unico smoke diagnostico 2+5 s, diez clientes. Arranque OK en 17,52 s. **318 solicitudes medidas, cero errores HTTP**. p95: listado **191,75 ms**, detalle **142,32 ms**, creacion **305,37 ms**, actualizacion **231,60 ms**. Solo lecturas quedan bajo 200 en esta muestra; el smoke no acredita RNF-2.

Conteos 100->128->208; SQL 208 incidencias/eventos creados, 96 editados, 2.080 entregas, cero SMTP/IA. Verificacion HTTP posterior OK, diez logout 204 y parada confirmada. Un INSERT outbox por creacion con diez entregas en PostgreSQL real; no se inyectan fallos PostgreSQL ni se registra cache_hit QA. Ocho grupos v3 validados por read_diagnostics con conteos/sumas SQL/hilos; tres workers y cero incompletas, consultas por peticion 3/2/10/7. Hashes actuales coincidentes; frente a 177 cambia solo mail.py.

Comparacion descriptiva con 177: endpoint de creacion medio 179,61->145,66 ms, p95 HTTP 479,34->305,37 ms. CPU global medida 80,43->66,56 % y tamaños/carga distintos; no prueba causalidad exclusiva ni ganancia formal. No sumar temporizadores solapados ni p95. Sin nueva formal del agente; se conservan siete FALLIDA_UMBRAL, ultima 182 previa a mejora 183 y regresion API de 85 aprobadas 184. Pendiente revisar viajes SQL/costes compartidos de escritura con hipotesis concreta; no repetir full ahora.

Proposito: validar integracion real y leer perfil antes de nueva optimizacion. Archivos: evidencia 185 y cinco documentos. Validacion: reporte original/read_diagnostics, hashes, conteos HTTP/SQL, parada y JSON; original conservado por hash. No cambios de aplicacion o nuevas pruebas ejecutadas por el agente. Resultado/limites/pendientes arriba.


## 27 de octubre de 2026 — Creacion reutiliza departamento ya revalidado

[Evidencia 186](evidencias/186-creacion-reutiliza-departamento-validado.json): el perfil185 muestra un SELECT/departamentos aislado dentro de diez consultas de creacion. administration_lock ya lo carga y revalida bajo bloqueo pero retornaba solo el rol; crear con Session nueva volvia a consultarlo. Nueva opcion include_department=True junto a include_role=True retorna (rol,departamento); modos previos mantienen None/string. create_case conserva la referencia solo dentro de esa operacion y reutiliza si coincide el departamento, manteniendo consulta/validacion independiente para otro. Sin cache entre peticiones ni Session.info.

Conteo local real con Session nueva/expire_on_commit=True: creacion **8->7 sentencias (5->4 SELECT, tres INSERT)**; edicion conserva cinco. Prueba de otro departamento conserva ocho y sus IDs correctos. No SQL postcommit en respuestas de creacion. Se espera 10->9 consultas QA en ENTORNO del departamento propio incluyendo autenticacion/advisory, todavia no observado en PostgreSQL real; no extrapolar ahorro de milisegundos ni p95.

**25 unitarias locales aprobadas en 0,658 s**, ocho nuevas mas nueve de rol/lock y ocho de outbox. SQLite real; cubren traslado obsoleto refrescado, departamento propio inactivo403/otro inactivo422, fronteras empleado/supervisor, compatibilidad anterior, orden simulado del mismo advisory y rollback completo. AST correcto en tres archivos. Se mantienen bloqueo antes de relectura y, en gestion, bloqueo de expediente antes de reevaluar acceso. No fusionar esas lecturas para ahorrar viajes sin demostrar semantica concurrente. [Bloqueos PostgreSQL17](https://www.postgresql.org/docs/17/explicit-locking.html).

Pendiente regresion API y comprobacion real PostgreSQL de reduccion/seguridad. Sin nueva formal/smoke ni cambios en umbral/durabilidad/auditoria/outbox. RNF-2 pendiente; siete formales fallidas conservadas. Las85 pruebas184 corresponden a revision anterior y no sustituyen regresion de este cambio.

Proposito: eliminar una lectura redundante demostrada sin cambiar snapshots de autorizacion. Archivos: services/administration_lock.py y services/incidents.py bajo backend/app, backend/tests/test_creation_department_reuse.py, evidencia186 y documentos. Validacion/resultado/limites detallados arriba. Sin commit Git, Docker o pruebas API ejecutadas por el agente.


## 27 de octubre de 2026 — Departamento revalidado: 97 pruebas y ocho subpruebas aprobadas

[Evidencia187](evidencias/187-regresion-api-departamento-97-aprobadas.json): salida del usuario **97 passed, 8 subtests passed in 8.56s** para ocho archivos: creation_department_reuse, administration_role_join, administration_lock_queries, lifecycle_role_queries, incidents, departments, user_administration y write_responses. Seleccion mixta de unitarias/API con RUN_DB_TESTS=0 y plugins/caches deshabilitados; no prueba PostgreSQL real. Tres hashes de186 coinciden, sin cambio de producto en este avance.

La reduccion local 8->7 sentencias de creacion propia queda cubierta por regresion seleccionada, junto con permisos/departamentos/roles/rollback. Pendiente unico smoke instrumentado PostgreSQL QA para comprobar 10->9 consultas con autenticacion/advisory y conteos reales. El generador actual usa ENTORNO del propio departamento; ese smoke no sustituye regresion de otros departamentos o carrera PostgreSQL. Sin nueva formal del agente; RNF-2 pendiente, siete formales FALLIDA_UMBRAL conservadas.

Proposito: registrar la regresion del usuario antes de integracion QA. Archivos: evidencia187 y cinco documentos de seguimiento/informe. Validacion: salida, hashes y JSON comprobados; sin pruebas adicionales ejecutadas por el agente ni cambios de producto/reportes. Resultado/limites/pendientes arriba.


## 27 de octubre de 2026 — Nueve consultas por creacion confirmadas; p95 sin mejora

[Evidencia188](evidencias/188-creacion-nueve-consultas-postgresql-p95-pendiente.json), run19a673b3854f44ff: dos redes QA vacias retiradas sin fallos/omitidas, arranque OK17,15s, unico smoke instrumentado2+5s con diez clientes. **312 solicitudes medidas, cero errores HTTP**. Consultas por peticion3/2/**9**/7; en calentamiento y medicion de creacion desaparece SELECT/departamentos aislado. Se confirma reduccion prevista10->9 para ENTORNO propio; no se extrapola a otros departamentos.

p95 HTTP: listado **181,25ms**, detalle **188,44ms**, creacion **371,32ms**, actualizacion **258,60ms**. Escrituras siguen sobre200 y empeoran frente185 (305,37/231,60ms). Endpoint de creacion medio145,66->129,83ms; CPU global66,56->70,77%. Menos consultas y menor media interna no acreditan mejora del p95; condiciones y muestras distintas impiden atribuir causa exclusiva. Mantener el resultado adverso.

Conteos100->130->209; SQL209 incidencias/eventos creados,103 editados,2.090 entregas, cero SMTP/IA. HTTP posterior OK, diez logout204, contenedores detenidos. Ocho grupos v3 y sumas validados, tres workers y cero incompletas. Hashes actuales coincidentes; frente185 cambian solo administration_lock.py e incidents.py de servicios. Reporte original preservado por hash. Regresion187 de97 pruebas/ocho subpruebas corresponde a esta revision.

Sin nueva formal del agente; siete formales FALLIDA_UMBRAL conservadas y RNF-2 pendiente. El smoke no prueba carreras ni rollback PostgreSQL. No sumar temporizadores solapados/p95 ni repetir full por consulta eliminada. Pendiente revisar esperas y costes compartidos de escritura con hipotesis concreta antes de otra carga.

Proposito: contrastar hipotesis de186 con PostgreSQL real y preservar resultado adverso de latencia. Archivos: evidencia188 y cinco documentos de seguimiento/informe. Validacion: reporte/read_diagnostics/hash/consistencia SQL-HTTP/parada/JSON. Sin cambio de producto ni carga ejecutada por el agente. Resultado y pendientes arriba.


## 27 de octubre de 2026 — Cierre limpio de Session sin salto a worker

[Evidencia189](evidencias/189-cierre-session-limpia-sin-worker.json): tercer worker del cierre en188 ejecuta solo0,03379ms (creacion) /0,04781ms (edicion) de media, con espera+retorno23,33/22,26ms. Al ocurrir despues del envio, no se resta ese tiempo al p95 HTTP; hipotesis de reducir planificacion/carga compartida, no ganancia formal demostrada. Se reviso SQLAlchemy2.1.4 instalado: Session._close_impl sin _transaction solo expunge_all; in_transaction refleja existencia de transaccion. [Semantica oficial de Session](https://docs.sqlalchemy.org/en/21/orm/session_api.html).

get_session conserva shield. Solo para tipo exacto de Session estandar original y sin transaccion, close local limpia objetos sin SQL/rollback/pool. Sesiones activas, subclases y dobles conservan worker con limiter1 independiente; SELECT posterior a commit vuelve a requerirworker. Sin cambios de consultas, commit, permisos/auditoria/atomicidad, pool, aislamiento o umbral. Excepcion acotada a decision156 de cerrar siempre enworker: todo cierre con posible IO siguefuera del loop. No custom callbacks de detach con IO en esta revision; futuros cambios de ese tipo requeririan revisar criterio.

**14 unitarias locales aprobadas en0,116s**, siete nuevas: ORM expirado tras commit se separa sin SQL/rollback/checkout/checkin; lecturas/escrituras pendientes, fallo de flush, SELECT postcommit, sesiones custom, cancelacion y errores de cierre. Workers reales/SQLite y dobles async sin eventloop. Nueva prueba FastAPI/TestClient para commit/cierre sinIO lista, mas pruebas AnyIO/TestClient previas: pendientes de ejecucion por el usuario. AST correcto en dos archivos. Se espera2 workers por escritura comprometida y3 por lectura, mismo SQL3/2/9/7; aun no observado enQA.

No nueva carga, formal o p95. RNF-2 pendiente; siete formales FALLIDA_UMBRAL conservadas. Regresion187 precede este cambio y no lo valida. Pendiente regresion de sesion/AnyIO/API antes de considerar otro diagnostico; no repetir full ahora.

Proposito: evitar planificacion de cierre puramente local preservando worker para IO. Archivos: backend/app/core/database.py, backend/tests/test_database_session.py, evidencia189 y documentos. Validacion: source SQLAlchemy instalado, perfil188, 14 locales, AST/JSON; resultados/limites arriba. No Docker o pruebas API ejecutados por agente.


## 27 de octubre de 2026 — Cierre de Session: 99 pruebas aprobadas con AnyIO/API

[Evidencia190](evidencias/190-regresion-session-anyio-api-99-aprobadas.json): el usuario ejecuto siete archivos database_session, database, auth, incidents, mail, write_responses y worker_response; resultado **99 passed in12.03s**. Incluye pruebas AnyIO/TestClient pendientes de189, cierre postcommit sinIO y rutas de cierre activo/custom protegidas. Seleccion mixta de unitarias/API, no99HTTP. RUN_DB_TESTS=0, plugins/caches deshabilitados. Ambos hashes189 coinciden; sin cambio de producto en este avance.

Pendiente unico smoke PostgreSQL QA para contrastar dos workers en escrituras comprometidas/tres en lecturas y consultas3/2/9/7, auditoria/outbox/errores/parada. Cierre postenvio: no estimar ahorro directo p95. Sin nueva carga/formal por el agente. RNF-2 pendiente; siete formales FALLIDA_UMBRAL conservadas.

Proposito: registrar integracion real de pruebas AnyIO/API antes de QA. Archivos: evidencia190 y cinco documentos. Validacion: salida del usuario, hashes y JSON verificados. Resultado99aprobadas; limites/pendientes arriba. Sin ejecucion adicional de pruebas/carga o cambios de producto/reportes por agente.


## 27 de octubre de 2026 — Dos workers por escritura confirmados; SQL intacto

[Evidencia191](evidencias/191-cierre-limpio-dos-workers-escritura-postgresql.json), run0e18dbd01e554b2e: dos redes vacias QA retiradas sin fallos/omitidas, arranque OK16,95s y unico smoke instrumentado2+5s con diez clientes. **330 solicitudes medidas, cero errores HTTP**. En ambos periodos, creacion/actualizacion bajan3->2 llamadas a worker; lecturas conservan3. Consultas3/2/9/7 y cero incompletas; no se altera instrumentacion para lograrlo. Frente188 cambia solo core/database.py; hashes actuales coincidentes.

Cierre medio creacion23,53->0,16ms y edicion22,48->0,15ms. Desaparece etapa other de escritura, permanece en lectura para rollback enworker. p95 listado **190,30ms**, detalle **150,90ms**, creacion **271,85ms**, actualizacion **248,74ms**. Escrituras siguen sobre200; frente188 (371,32/258,60) son menores, pero CPU70,77->67,42% y muestras/carga diferentes impiden atribuir toda mejora al codigo. Cierre postenvio: no restar su reduccion al p95 HTTP ni sumar p95 solapados.

Conteos100->130->212; SQL212 incidencias/eventos creados,104 editados,2.120 entregas, cero SMTP/IA. HTTP posterior OK, diez logout204, contenedores detenidos. Ocho grupos v3 y sumas SQL/hilos verificados. Regresion190 de99aprobadas cubre revision; smoke no inyecta fallos ni demuestra carreras PostgreSQL. Reporte original conservado por hash.

RNF-2 pendiente, siete formales FALLIDA_UMBRAL conservadas; sin nueva formal ni carga del agente. Pendiente explicar costes de nueve/siete viajes SQL y autenticacion compartida antes de nueva modificacion/carga; mantener locks, relecturas, durabilidad y criterio. No repetir full ahora.

Proposito: contrastar hipotesis189 de planificacion con PostgreSQL real. Archivos: evidencia191 y cinco documentos. Validacion: reporte/read_diagnostics/hash/conteos/sumas SQL-hilos/parada/JSON; original intacto. Sin cambios de producto ni pruebas/carga ejecutadas por agente. Resultados/limites/pendientes arriba.


## 27 de octubre de 2026 — Diagnostico v4 separa ping de conexion

[Evidencia192](evidencias/192-diagnostico-pool-pre-ping-separado.json): revision de SQLAlchemy2.1.4 instalado confirma que pool_pre_ping usa PGDialect_psycopg.do_ping con SELECT1 directo DBAPI, fuera de before_cursor_execute. Por tanto, las9consultas de creacion son sentencias observadas por motor, no todos los viajes; tampoco incluyen BEGIN/COMMIT/ROLLBACK o apertura de conexion. No cambia p95/formales anteriores. [Semantica oficial de pre_ping](https://docs.sqlalchemy.org/en/21/core/pooling.html).

Entrada QA protegida envuelve do_ping sin cambiar argumentos/resultado/excepcion/recuperacion. Nuevas metricas pool_ping(ms), pool_ping_calls y pool_ping_errors; formato4 con marca de instrumentacion. Contexto ausente no mide; no guarda SQL/conexion/parametros/errores privados. app.main/pool_pre_ping intactos. Reader acepta3/4 y exige metricas v4 finitas/no negativas y conteos coherentes, permite cero si conexion fresca. Reportes185/188/191 v3 revalidados sin reescritura.

**85 unitarias de herramientas aprobadas en1,569s y tres pruebas SQLAlchemy en0,049s**. Nueve nuevas stdlib: resultado/excepcion sin reintentos, privacidad, contextos concurrentes, v3/v4 y pipeline ASGI->snapshot->reader de ocho grupos. Tres nativas: ping SQLite real no aparece en evento de motor, psycopg conserva cursor/autocommit, clasificacion de desconexion original se mantiene. Sin PostgreSQL real ni HTTP/Docker/carga nueva. AST de seis archivos y orden guard/parche comprobados.

Hipotesis por verificar: ping podria explicar parte de autenticacion fuera del SQL cronometrado. No se conoce aun coste ni frecuencia real; no desactivar ping ni atribuirle cuello de botella sin medir. pool_ping solapa auth y no se suman sus p95. Pendiente unico smoke v4; no nueva formal. Siete formales FALLIDA_UMBRAL conservadas, RNF-2 pendiente.

Proposito: medir coste compartido no observado antes de proponer cambios. Archivos: core/performance_timing.py y performance_diagnostics.py bajo backend/app, backend/scripts/provision_performance_qa.py y tres archivos de pruebas, evidencia192 y documentos. Validacion y resultados arriba. Cambio solo de diagnostico/herramientas; sin modificacion de politica de conexiones o ejecucion de Docker.


## 27 de octubre de 2026 — Ping medido; retencion del pool para diez clientes

[Evidencia193](evidencias/193-ping-postgresql-coste-medido-sin-fallos.json), run7b1abe6c5dc54abc: diagnostico4 valido con **296 solicitudes medidas, cero errores y258pings sin fallos**. Tiempo ping medio por peticion8,85/10,70/10,78/10,93ms; no sumarlo a auth ni a sus p95. p95 listado211,39/detalle196,50/creacion383,47/actualizacion304,76ms; solo detalle bajo200 en esta muestra. CPU global78,42%. Conteos100->130->204, SQL204casos/eventos creados,98editados,2.040entregas, cero SMTP/IA. PostHTTP OK,diez logout204,parada confirmada; SQL3/2/9/7 y workers3/3/2/2. Reporte original conservado porhash y codigo previo a194 validado.

38peticiones sinping son compatibles con conexiones frescas (source instalado lo omite), pero no prueban por si solas que todas sean recreaciones poroverflow. Se mantiene pre_ping. [Evidencia194](evidencias/194-pool-retiene-diez-maximo-quince.json): experimento local de tres oleadas de diez conexiones simultaneas con QueuePool/SQLite: default5+overflow10 crea20conexiones y cierra15antes de dispose; retencion10+overflow5 crea10y reutiliza todas despues de primera oleada. No mide tiemposPG/HTTP.

get_engine ahora retiene hasta10conexiones y permite5extra: **mismo maximo15por proceso**, pre_pingTrue, pool_timeout30 y connect_timeout3 sin cambios. Creacion diferida, cachedeengine, transacciones/aislamiento/reset/permisos/auditoria intactos. Puede mantener cinco ociosas adicionales y su memoria; no garantiza ahorro p95.

**20 locales aprobadas en0,211s**, seis nuevas de pool y14deSession. Puente con opciones reales de get_engine hacia SQLite, sinred. Verifica tresoleadas10/0/0 nuevas, max15/rechazo16a, espera/reuso al devolver, recuperacion deconexion obsoleta ydispose. AST valido en dos archivos. Pendiente regresionAPI y diagnosticoPG de194. No nueva carga del agente ni formal; siete FALLIDA_UMBRAL conservadas,RNF-2 pendiente.

Proposito: registrar coste compartido y evitar recreacion demostrada localmente sin aumentar limite de conexiones. Archivos: backend/app/core/database.py, backend/tests/test_database_pool.py, evidencias193/194, cinco seguimientos,DECISIONES yREADME. Validacion/resultados/limites/pendientes arriba; sin commitGit o Docker del agente.


## 27 de octubre de 2026 — Pool ajustado: 105 pruebas aprobadas

[Evidencia195](evidencias/195-regresion-api-pool-105-aprobadas.json): salida del usuario **105 passed in16.15s** para ocho archivos database_pool, database_session, database, auth, incidents, mail, write_responses y worker_response. Seleccion mixta de unitarias/API con RUN_DB_TESTS=0; no105HTTP ni prueba PostgreSQL real. Dos hashes194 coinciden, sin cambios de producto en este avance.

Pendiente unico smoke PostgreSQL QA instrumentado v4 para pool10retenidas+5extra, max15. Contrastar frecuencia/coste de ping/auth, SQL3/2/9/7, workers3/3/2/2, errores/auditoria/outbox/recursos/parada. Mayor frecuencia de ping puede indicar reuso, no acredita latencia; mantener todos los resultados adversos. RNF-2 pendiente y siete formales FALLIDA_UMBRAL conservadas. Sin carga adicional del agente ni nueva formal.

Proposito: registrar regresion del pool antes de integracion PostgreSQL. Archivos: evidencia195 y cinco documentos de seguimiento/informe. Validacion: salida, hashes y JSON comprobados; sin nuevas pruebas/carga del agente ni cambios de producto/reportes. Resultado/limites/pendientes arriba.


## 27 de octubre de 2026 — Pool10 sin ganancia p95; experimento retirado

[Evidencia196](evidencias/196-pool-diez-diagnostico-sin-ganancia-p95.json), runb61bb77e73b94128 (UTC28oct/local27oct): unico diagnostico instrumentado2+5s,267solicitudes medidas sin errores,262pings sinfallos. Frecuencia87,16->98,13% frente193 compatible con mas reuso, no conteo directo completo de creaciones. Pero **los cuatro p95 son mayores: listado249,52/detalle225,90/creacion456,68/actualizacion365,13ms**. Ninguno bajo200 en esta muestra. CPU78,42->79,03%; no atribuir regresion causal con una sola ventana y dataset/carga distintos.

Datos100->130->196; SQL196incidencias/eventos creados,92editados,1.960entregas,ceroSMTP/IA. PostHTTP OK,diez logout204,parada confirmada; SQL3/2/9/7 y workers3/3/2/2. v4/sumas/hash del codigo experimental194validados; solo database.py cambia respecto193. Reporte original intacto.

[Evidencia197](evidencias/197-pool-base-restaurado-experimento-retirado.json): se retira **solo ajuste194 de retener10** porque no demuestra beneficio p95 que justifique hasta5conexiones ociosas mas. database.py vuelve byteporbyte al hash de190: defaults5retenidas+10extra,max15,pre_pingTrue,tiempos30/3. Conserva cierre limpio189,mail183 y departamento186. Diagnostico192tambien conservado. No se afirma que pool10causara por si solo el empeoramiento ni se ocultan194/195/196.

**20 pruebas locales aprobadas en0,294s**, seis de poolbase y catorce deSession. Pruebas de saturacion/capacidad15,obsoletas/pre_ping,liberacion/lazy y cierre activo/limpio preservadas. El codigo productivo restaurado coincide con revision de99pruebas190; no nueva pruebaAPI/PG ejecutada por agente. AST/JSON/hash verificados,README actualizado. RNF-2 pendiente;siete formales FALLIDA_UMBRAL conservadas. No otra formal por restauracion; pendiente hipotesis basada en costes de driver/servidor/planificacion.

Proposito: evaluar experimento sin mantener mayor retencion no respaldada porlatencia. Archivos: core/database.py bajo backend/app,backend/tests/test_database_pool.py, evidencias196/197,cinco seguimientos,DECISIONES yREADME. Validacion/resultados/limites arriba; sin Docker o nuevas pruebasAPI del agente.


## 27 de octubre de 2026 — Diagnostico5: CPU del worker frente a tiempo transcurrido

[Evidencia198](evidencias/198-diagnostico-cpu-worker-separada-de-tiempo.json): thread_run de versiones anteriores incluye esperas/IO/planificacion dentro del worker. Nueva metrica thread_cpu y cpu_ms por etapa mide diferencia de time.thread_time dentro del mismo hilo. Excluye tiempo no ejecutado por ese hilo, eventloop/otros hilos/PostgreSQL/hipervisor. No es CPU global ni permite atribuir todo wall-CPU a una causa. [Definicion de Python](https://docs.python.org/3.11/library/time.html#time.thread_time).

Solo diagnostico protegido QA: formato5 con marca CPU, campos agregados y opciones/cancelacion/excepciones/limiter intactos. Fuera de contexto no mide. Reader acepta3/4/5; en5 exige marca, CPU finita/no negativa y sumas por etapas concordantes; CPU0permitida por granularidad. No guardar argumentos/SQL/errores privados. No sumar/restar p95. No imponerCPU<=wall por diferencias de resolucion.

**94 unitarias stdlib aprobadas en2,125s**, nueve nuevas. Relojes separados, mismo hilo real, ContextVar, excepcion exacta, no inicio, privacidad, legado y validacion corrupta. Pipeline ASGI simulado genera ocho grupos formato5y pasa lector. Reportes177/191v3 y193/196v4 revalidados; AST seisarchivos correcto. Sin nueva carga/Docker/PostgreSQL/HTTP real. database.py conserva hash190restaurado197: poolbase5+10 y todas las otras mejoras permanecen.

Pendiente unico smoke5para decidir si predomina CPU del worker o tiempo fuera deCPU; no es cambio de rendimiento ni acreditacion. Siete formales FALLIDA_UMBRAL conservadas,RNF-2 pendiente. No otraformal sin hipotesis y evidencia.

Proposito: distinguir costes antes de otra optimizacion especulativa. Archivos: core/performance_timing.py yperformance_diagnostics.py bajo backend/app,backend/scripts/provision_performance_qa.py,tresarchivosdepruebas,evidencia198y documentos. Validacion/resultados/limites arriba. Sin cambios del flujo normal del producto ni cargas del agente.


## 27 de octubre de 2026 — CPU de workers medida; control driver/servidor preparado

[Evidencia199](evidencias/199-cpu-worker-baja-frente-a-tiempo-transcurrido.json), runde6481fae3c04e19: diagnostico5 valido,260solicitudes medidas sinerrores. P95 listado233,84/detalle257,01/creacion509,12/edicion285,46ms, todos sobre200. CPUglobal80,20%. Creacion usa23,07msCPU enworkers frente192,29mstranscurridos; endpoint18,06CPU/135,75ms. Edicion14,99CPU/140,83ms; endpoint11,29CPU/99,98ms. Predomina tiempo no ejecutando esos hilos, pero no se identifica aun servidor/IO/GIL/SO/VM; no incluyeCPUeventloop/otrosprocesos.

Conteos100->130->192; SQL192incidencias/eventoscreados,90editados,1.920entregas,ceroSMTP/IA. PostHTTP OK,diezlogout204,parada confirmada. SQL3/2/9/7 y workers3/3/2/2; sumasCPU/hilos y hashesvalidados. Reporteoriginalconservado. No acreditaRNF-2;sieteformalesfallidas vigentes.

[Evidencia200](evidencias/200-control-driver-servidor-select1-preparado.json): control opcional --db-probe solo smoke diagnostico QA nuevo, despues de HTTP y verificacionSQL antes de parada.55lecturas fijas EXPLAIN ANALYZE SELECT1:5en1conexion y50en10conexiones/hilos coninicioalineado. Reporta driver/CPU/planificacion/ejecucionservidor sin SQL/plan/parametros/credenciales. No admite consultas arbitrarias; identidadDB/user real y envQA comprobados. Sin extensiones, cambioPG o API/pool/producto. SETLOCAL timeout3s solo transaccionescontrol; procesoexterno60s. Error conservaHTTP/SQL y marcaINCOMPLETA/parada.

**102 unitarias de herramientas aprobadas en2,266s**, ochonuevas; guard,55muestras/liberacion,privacidad,rechazoformaly recuperaciondeerror, con motoresdobles e hilosreales. Primer fallo deexpectativaregexcorregido sinrelajar guarda. AST4archivoscorrecto; ejecucionPGreal pendiente. El control no reproduce consultas de negocio ni comparte cargaHTTP simultanea; no atribuir diferencia a red pura ni restarp95. Pendiente unico smoke --db-probe, no otraformal.

Proposito: conservar resultadoCPU y preparar contraste acotado sin optimizacion especulativa. Archivos: backend/scripts/performance_db_probe.py yprovision_performance_qa.py,dosarchivosdepruebas,evidencias199/200,seguimientos/DECISIONES/README. Validacion/resultados/limites arriba; sin Docker del agente ni cambio de flujo normal.

## 2026-10-29 — Respuesta a auditoría del corte 23-oct

Se contrastó la captura con GitHub: `main` remoto en7886d1e del17-oct; historial local hastaa3bd482 no publicado. Se conserva ese historial mediante bundle y copia de publicación porque `.git` original rechaza escritura en este entorno. No se altera el cambio local de docs/evaluacion_ia/REVISION.md, ni se incluye en la copia. Sin `.env`, .pgdata, credenciales, dependencias o reportes operativos en los archivos seleccionados.

README mantiene guía en cinco pasos, se retiran notas históricas del pool y se enlazan guías técnicas; se corrigen límites actuales y cuentas DEMO con autenticación local. App y documentos señalados ya estaban en UTF-8; se corrigen dos comentarios mojibake de tests. 89 archivos de app/tests y guías señaladas leídos en UTF-8, AST Python válido y sin patrones Ã/Â/reemplazo. Se añade aviso CIERRE al reportante/afectado con acceso vigente, deduplicación y outbox transaccional; closed_at identifica ciclo y solo se agrega a contexto del aviso nuevo. Reaperturas y cierres posteriores omiten cierres pendientes antiguos. Nueva migración0008 amplía CHECK sin actualizar/borrar entregas, health/db exige0008; React muestra Cierre. Scripts de actualización ya aplican head y sus mensajes dejan de fijar revisión antigua.

Validación:8 pruebas nuevas servicios/SQLite y DDL offline aprobadas (1,838s); regresión8 outbox+19casos de servicio aprobada(2,342s);102 herramientas rendimiento aprobadas(2,180s);4 React MailStatus aprobadas y buildVite aprobado(683ms). Primer ensayo de prueba de segundo ciclo esperaba dos envíos y obtuvo tres porque reapertura también era válida; se corrigió la prueba para contar solo cierres por ID, sin cambiar reglas. Regresión detectó campo closed_at extra en eventos antiguos: se restringió al nuevo tipo CIERRE y regresión volvió a aprobar. No API HTTP/TestClient ni PostgreSQL/Docker ejecutados localmente por este agente; Docker API deniega acceso. CI remoto pendiente de publicación, no se inventa resultado. RNF-2 pendiente; no nueva carga ni cambio de umbral.

Informe: [respuesta a auditoría](AUDITORIA_2026-10-23.md), [evidencia201](evidencias/201-respuesta-auditoria-cierre-correo.json). Pendiente recepción remota, CI y captura Mailpit del cierre nuevo; los avisos anteriores conservan evidencia92.

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


## 2026-10-30 — Departamentos: recorrido real de Admin RH conforme

[Evidencia223](evidencias/223-departamentos-admin-rh-recorrido-ui.json) y capturas 224/225: usuaria aportó arranque Compose rnf2/perfilmail saludable y migraciones/check correctos. API /health y /health/db respondieron 200 desde agente tras permiso de red; 5173 rechazaba conexión. Se inició Vite como proceso persistente y se abrió nueva pestaña; usuaria autenticó Admin RH sin compartir contraseña. El agente verificó rol y ejecutó D01–D08 de [aceptación](ACEPTACION_ENTREGA.md): creación ficticia, duplicado rechazado, renombrado,baja,reactivación,baja final e historial. Estado final **Inactivo**,nombre QA entrega - departamentos - 20261030-01 - revisado; cinco cambios con motivos observados entre 23:51:53–23:52:50 y conservados tras Actualizar y reabrir Historial. Catálogo de 4 a 5 filas; otros departamentos permanecen activos sin editar. Sin eliminación ni cambios de usuarios/incidencias.

Validación real mediante controles visibles, árbol accesible, captura completa revisada y refresco desdeAPI. Duplicado produjo aviso compartido de conflicto, sin capturar código HTTP; no afirmar HTTP 409 real. UUID no expuesto, SQL no inspeccionado. A02 verificado en UI; A03 solo duplicado, aún motivo vacío/dependencias; A04 Supervisor/Empleado sigue pendiente. RNF-2 aprobado220 conservado, sin repetir carga. No se ejecutaron unitarias repetidas para sustituir el recorrido; no hubo cambios de aplicación ni aceptación institucional. Capturas contienen solo nombres genéricos/ficticios y sin credenciales. Archivos: matriz/evidencia/capturas y seguimiento MVP/backlog/entregables/trazabilidad/QA/bitácora.


## 2026-10-31 — Visibilidad de administración por rol confirmada por la autora

[Evidencia226](evidencias/226-visibilidad-administracion-supervisor-empleado-confirmada.json): la usuaria informa que RH Independiente Demo ve Usuarios y Departamentos, Supervisor RH no muestra esas opciones y Empleado tampoco. Confirmación textual de visibilidad, sin observación directa/capturas nuevas del agente ni comprobación API en este recorrido. A04 avanza solo en su parte visual; rechazo de rutas API con sesiones reales sigue sin verificarse aquí. No repetir pruebas ya aprobadas ni crear cuentas para este registro. RNF-2 y recorrido223 se conservan. Registro local, sin publicación remota en este avance para reducir llamadas y consumo.


## 2026-10-31 — Usuarios: alta, renombrado, baja y rechazo de acceso reportados

[Evidencia227](evidencias/227-usuario-ficticio-alta-edicion-baja-confirmadas.json): la autora confirma creación y presencia en listado de la cuenta ficticia indicada `qa-entrega-20261031-01@example.invalid`; después confirma nombre revisado y estado Inactiva. Informa rechazo al intentar iniciar sesión: «Correo o contraseña incorrectos, o acceso temporalmente bloqueado.» Contraseña introducida solo por la autora, no recogida. Sin observación directa/capturas nuevas del agente ni inspección HTTP/SQL.

A05 avanza en el recorrido reportado de alta/edición/baja. El rechazo es coherente con acceso no permitido, pero el aviso genérico no prueba que su causa sea exclusivamente la inactividad: no se observó acceso exitoso previo con la misma contraseña y tampoco se probó revocación de sesión existente. Auditoría de usuarios, duplicados, cambios de rol/departamento y concurrencia permanecen pendientes. No declarar aceptación completa. Registro agrupado local para ahorrar llamadas; sin nuevas pruebas, cambios de código ni publicación remota. Cuenta ficticia conservada inactiva; RNF-2 aprobado y demás evidencias intactas.


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


### 2026-10-31 — Revisión de frases desactualizadas del README

Propósito: atender la observación de auditoría sobre frontend pendiente y ausencia de configuración de claves. Búsqueda literal en README, backend/README, FRONTEND, MANUAL_TECNICO y ENTREGABLES: ambas frases observadas ya estaban ausentes. Se conserva el historial de bitácora como registro fechado. Se encontró y corrigió una contradicción vigente en el resumen de README: RNF-2 ya está aprobado en alcance QA local (220), y restauración lógica/reanudación Docker cuentan con230/234; recuperación integral, aceptación y capacitación siguen pendientes. Se explicitan POSTGRES_PASSWORD, contraseña privada Admin RH, OPENAI_API_KEY para IA opcional y configuración SMTP externa cuando aplique. Archivos: README y seguimiento en bitácora, backlog, entregables y trazabilidad. Validación: textos actuales contrastados con .env.example y evidencias; enlaces locales y ausencia de las frases originales comprobados. Cambio documental: sin nuevas pruebas funcionales ni credenciales publicadas.


### 2026-10-31 — Conservación de expediente tras baja de cuenta

[Evidencia 238](evidencias/238-expediente-conservado-tras-baja-usuario.json): ante la solicitud de comprobar título, descripción, estado Pendiente y evento CREADO del caso ficticio 710482ca-a652-4679-9abf-13c3b3553e10 como Admin RH, manteniendo la cuenta ficticia inactiva, la usuaria confirma globalmente «todo sigue bien». Se registra como confirmación textual guiada, sin observación directa ni verificación independiente por campo/HTTP/SQL. Propósito: comprobar conservación de ese expediente después de la baja; no acredita auditoría administrativa de usuarios ni todos los supuestos de permisos. Archivos: evidencia238, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y referencia comprobados. Sin cambios de código, nuevas pruebas automáticas, modificación indicada del caso ni publicación remota. A05 conserva pendiente auditoría administrativa; alcance de conservación acotado a este caso.


### 2026-10-31 — Auditoría administrativa del usuario ficticio consultada

[Evidencia 239](evidencias/239-auditoria-usuario-ficticio-consulta-lectura.json): salida aportada por la usuaria de consulta READ ONLY muestra11 eventos USUARIO_ACTUALIZADO de la cuenta ficticia, nueve cambios de activación con bandera sessions_revoked=true y motivos; renombrado con true→true y bandera false; evento más antiguo sin los campos proyectados. El código ALTA_LOCAL no guarda esos campos, lo cual es compatible, pero operacion no fue seleccionada y no se confirma esa identidad. La bandera no cuenta sesiones ni reemplaza la comprobación funcional228. Propósito: verificar registro administrativo del recorrido A05. Archivos: evidencia239, matriz, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y referencia comprobados; contraste con api/auth.py y services/users.py. A05 reúne alta/edición/baja reportadas, revocación228, negativos229, expediente238 y consulta239 en su alcance acotado; no aceptación integral de cambios de rol/departamento, concurrencia o todos los expedientes. Sin cambios de código, nueva pantalla, nuevas pruebas automáticas o publicación remota.


### 2026-10-31 — Resumen verificable de entrega

Propósito: facilitar revisión académica sin repetir pruebas o presentar aceptación no realizada. Creado RESUMEN_ENTREGA.md con resultados, procedencia, pendientes y guion de demostración; enlazado desde índice documental. Corregidas dos notas vigentes del índice sobre RNF-2 pendiente/resultados pendientes frente a la aprobación posterior220. Archivos: resumen, índice, bitácora, backlog, entregables y trazabilidad. Validación: enlaces relativos del resumen comprobados; sin nuevos tests funcionales por cambio documental. Evidencias238/239 y resumen siguen locales; última publicación comprobada9e1d77a. No se inventan capacitación, aprobación institucional, fecha de entrega o porcentaje medido.


### 2026-10-31 — Preparación de versión revisable para entrega

Propósito: agrupar conservación de expediente238, consulta de auditoría239 y RESUMEN_ENTREGA para revisión académica mientras continúan los pendientes. Se conserva el código de aplicación y la aprobación RNF-2 en su alcance; no hay nuevas funciones ni nuevas ejecuciones funcionales. Se revisan JSON, enlaces del resumen y diff documental antes de publicar por avance normal de main; la confirmación de publicación debe obtenerse del historial remoto. No se incluyen respaldo binario, configuración privada o credenciales. No se declara capacitación, aceptación integral ni eliminación de pendientes.


### 2026-10-31 — Rechazos administrativos de lectura con dos sesiones reales

[Evidencia240](evidencias/240-rechazos-api-supervisor-empleado-confirmados.json): la usuaria aporta ejecución del auxiliar local para Supervisor RH y Empleado Operaciones2. Rol comprobado mediante /auth/me; GET /users, /users/options y /departments devuelve403 en ambas sesiones; logout204 en ambas. Propósito: complementar controles ocultos226 con denegaciones HTTP reales. Alcance: seis rechazos de lectura y dos cierres de sesión reportados; no se ejecutan escrituras ni historial de departamentos. Tres comprobaciones simuladas previas del auxiliar validaron manejo de403, rol incorrecto y200 inesperado, sin llamadas reales del agente. Archivos: evidencia240, aceptación, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. No se recopilan contraseñas ni tokens. A04 tiene lecturas verificadas por salida de la usuaria; escritura/historial en sesión real permanecen fuera del recorrido, con sus pruebas automatizadas separadas. Registro local, sin publicación en este avance ni cambios de producto.


### 2026-10-31 — Restricciones administrativas ampliadas en sesiones reales

[Evidencia241](evidencias/241-rechazos-administrativos-ampliados.json): Supervisor RH y Empleado Operaciones2, roles comprobados por /auth/me, aportan ocho403 cada uno: lecturas users/opciones/departamentos/historial y POST/PUT de usuarios/departamentos. Dos cierres204. Escrituras con cuerpo vacío y PUT a UUID nulo: se confirma rechazo de esos intentos, no la matriz completa con cuerpos válidos y registros existentes. Auxiliar local con sintaxis y cuatro escenarios simulados comprobados; sin código de producto nuevo ni credenciales registradas. Propósito: ampliar A04 sin generar altas/ediciones válidas. Archivos: evidencia241, aceptación, resumen, QA, bitácora, backlog, entregables y trazabilidad. Validación documental: JSON y referencias comprobados. Se mantienen límites de confidencialidad, concurrencia y aceptación institucional. Registro local, sin publicación remota en este avance.


### 2026-10-31 — Expediente ficticio no disponible para otro Empleado

[Evidencia242](evidencias/242-empleado-expediente-ajeno-404.json): salida aportada por la usuaria con rol EMPLEADO verificado para Empleado Operaciones2: GET detalle, historial y participantes de710482ca-a652-4679-9abf-13c3b3553e10 devuelve404; logout204. Existencia/conservación accesible previamente como Admin RH reportada en238, sin comprobación simultánea nueva. Propósito: ampliar A07 con tres respuestas HTTP reales de no disponibilidad, sin mostrar contenido. Un404 aislado no distingue inexistencia/denegación; no se infieren todos los casos de confidencialidad, relaciones, listados o escrituras. Auxiliar local con sintaxis y tres escenarios simulados verificados; sin nuevas llamadas reales del agente. Archivos: evidencia242, matriz, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. Sin cambios de código de producto o publicación remota en este avance.


### 2026-10-31 — Control positivo Admin RH del expediente ficticio

[Evidencia243](evidencias/243-control-admin-expediente-200.json): rol ADMIN_RH comprobado, detalle/historial/participantes del caso710482ca-a652-4679-9abf-13c3b3553e10 responden200; cierre204, según salida aportada por usuaria. Contrasta con los tres404 de Empleado en242 mediante sesiones sucesivas, sin mostrar contenido. Propósito: confirmar disponibilidad autorizada posterior y reforzar el recorrido A07. No prueba simultaneidad, ausencia de cambios entre sesiones o matriz integral de conflictos/participantes. Correo operativo omitido en nueva evidencia; credenciales/tokens no recogidos. Auxiliar con sintaxis y tres escenarios simulados comprobados. Archivos: evidencia243, aceptación, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. Sin código de producto nuevo, mutaciones de negocio solicitadas ni publicación remota en este avance.


### 2026-10-31 — Ensayo de demostración con capturas de estados

[Evidencia244](evidencias/244-ensayo-estados-capturas-autora.json) y capturas245–247 aportadas por la usuaria: evento CREADO visible, cuenta ficticia EMPLEADO Inactiva vinculada al departamento ficticio, departamento Activo. Propósito: conservar prueba visual del ensayo de demostración. ID/estado Pendiente del caso y sesión Admin RH corresponden al contexto reportado, no visibles en los recortes. Capturas no demuestran por sí solas causa de bloqueo, integridad completa ni aceptación institucional. Archivos: JSON244, tres PNG245–247 y seguimiento documental. Validación: firmas PNG, hashes SHA256 y referencias comprobados. Sin modificar datos, nuevas pruebas de aplicación o publicación remota en este avance. Ensayo no equivale a capacitación acreditada.


### 2026-10-31 — Ensayo: aviso genérico capturado en Mailpit

[Evidencia248](evidencias/248-ensayo-mailpit-aviso-generico.json), capturas249/250 de la autora: mensaje del caso ficticio710482ca-a652-4679-9abf-13c3b3553e10 para destinatario ficticio, cuerpo genérico con enlace local y UUID, sin título/descripción/nombres en texto visible. Comprobador de enlaces mostrado sin resultado; no se declara verificado. Propósito: documentar sección de correo de la demostración. Alcance Mailpit local, sin comprobar buzón externo, Raw/MIME completo, todos los destinatarios o reintentos. Archivos: JSON248, PNG249/250 y seguimiento. Validación: firmas PNG, hashes y referencias comprobados. Sin modificar aplicación, generar avisos nuevos o publicación remota en este avance.


### 2026-10-31 — Apertura del expediente desde enlace de correo

[Evidencia251](evidencias/251-enlace-mailpit-expediente-confirmado.json) y captura252: tras indicación de abrir enlace Mailpit, la autora aporta destino con parametro incident y expediente del mismo UUID, título ficticio y estado Pendiente, sesión Administrador RH visible. Propósito: completar ensayo de navegación correo→expediente. No se observó el clic/login intermedio; no se declara ejecutado el comprobador automático de Mailpit ni entrega externa. La leyenda IA pendiente no demuestra llamada o fallo del proveedor. Archivos: JSON251, PNG252 y seguimiento documental. Validación: firma PNG, hash SHA256 y referencia comprobados. Sin cambios de aplicación, nuevos avisos o publicación remota en este avance.


## 2026-10-31 — Archivo de notas históricas retiradas del índice

Texto histórico conservado del índice documental. Sus pendientes corresponden a cada etapa anterior y no sustituyen el estado vigente de la matriz de aceptación.

### 2026-10-30 — RNF-2: formal QA de dos procesos preparada

[Evidencia213](evidencias/213-formal-qa-dos-procesos-preparada.json): opcion explicita `--api-workers 2` en run_performance_full_guarded.py; conserva protocolo10clientes/30+300s/p95<200ms, guardas CPU/redes e integridad.126 unitarias aprobadas; ejecución formal real pendiente. Ver comando y límites en [prueba de rendimiento](PRUEBA_RENDIMIENTO.md). La restricción histórica de dos procesos solo smoke se amplía a full sin diagnóstico; sitio sin cambios.


### 2026-10-30 — RNF-2 pendiente tras octava formal

[Evidencia214](evidencias/214-formal-dos-procesos-fallo-escrituras.json):27.722 solicitudes sin errores con2procesos; listado/detalle160,12/156,67ms cumplen, creación/actualización264,38/227,96ms incumplen. Integridad y parada correctas. [Candidato215](evidencias/215-formal-tres-procesos-candidato.json): `--api-workers 3` en QA formal con mismo protocolo,130 pruebas aprobadas, todavía sin medición real. Más memoria/conexiones y posible competencia CPU; no cambia sitio ni umbral. Ver [prueba de rendimiento](PRUEBA_RENDIMIENTO.md).


### 2026-10-30 — RNF-2: solo creación pendiente en novena formal

[Evidencia216](evidencias/216-formal-tres-procesos-fallo-creacion.json):QA3,34.027 solicitudes sin errores; p95lecturas125,63/119,11 yactualización173,60ms cumplen; creación202,6812ms incumple. Integridad y parada correctas; RNF-2 pendiente. [Cambio217](evidencias/217-outbox-evento-nuevo-sin-lectura-redundante.json): evita una búsqueda outbox solo para evento pendiente sin identidad, preserva deduplicación de replay y atomicidad;30unitarias aprobadas. Pendiente CI y formal con mismo protocolo3procesos/10clientes/30+300s/p95<200ms.


### 2026-10-30 — RNF-2 pendiente tras décima formal

[Evidencia218](evidencias/218-decima-formal-fallida-cuatro-operaciones.json):24.450 solicitudes sin errores, QA3; p95 listado209,73/detalle200,83/creación328,30/edición289,47ms incumplen. Integridad y parada correctas, outbox217 presente; sin causalidad aislada. [219](evidencias/219-cpu-pasiva-por-fase-formal.json) añade CPU Windows/generador al inicio/fin de cada fase normal/formal, sin perfil API ni cambiar protocolo/veredicto;132 pruebas aprobadas. Pendiente CI y nueva medición; no más procesos ni cambios de negocio a ciegas.


## RNF-2 acreditado en QA local

[220: formal aprobada](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json), [221: perfilCompose](evidencias/221-perfil-compose-rnf2-reproducible.json) y [protocolo/alcance](PRUEBA_RENDIMIENTO.md).Tres procesosAPI,10 clientes/30+300s; cuatro p95 <200 ms,sin errores e integridad correcta. El historial de fallos no se elimina; otros pendientes de entrega continúan.


## Continuación de la entrega: matriz por roles

La [matriz de aceptación](ACEPTACION_ENTREGA.md) reúne14escenarios con origen/alcance de evidencia y pendientes. [Preparación222](evidencias/222-matriz-aceptacion-entrega-preparada.json): siguiente recorrido de departamentos conAdminRH,8pasos previstos y ninguna escritura ejecutada. RNF-2 aprobado220 se conserva; un plan no es aceptación real. Ver comandos de arranque con3procesos/Mailpit y registro de resultados en la matriz.


## Departamentos: aceptación Admin RH observada

[223](evidencias/223-departamentos-admin-rh-recorrido-ui.json): D01–D08 conforme en panel integrado; alta ficticia, duplicado rechazado, renombrado, baja/reactivación y baja final; cinco eventos con motivos y persistencia tras actualizar. Estado final inactivo, sin borrar datos ni tocar departamentos usados. [224: historial](evidencias/224-departamentos-admin-rh-historial-final.jpg),[225: duplicado](evidencias/225-departamento-duplicado-rechazado.jpg). A02 verificado; A03 parcial y A04 pendiente según [matriz](ACEPTACION_ENTREGA.md). No implica aceptación integral ni institucional.


### 2026-10-31 — Revisión de manuales y preparación de evidencias del ensayo

Propósito: dejar guías de uso actuales y agrupar capturas del ensayo para publicación. Se aclara historial de departamentos frente a auditoría interna de usuarios en ambos manuales. Notas cronológicas de preparación/fallos RNF-2 retiradas del índice y conservadas arriba en bitácora; índice enlaza estado vigente. Evidencias244–252 conservan capturas y límites de estados, correo local y destino de enlace; no capacitación ni aceptación formal. Archivos: manuales, índice, bitácora, evidencia gráfica y seguimiento. Validación: JSON de manifiestos, integridad SHA256 de seis PNG, enlaces de manuales/índice y diff comprobados. No se repiten pruebas funcionales por cambio documental ni se publican secretos o respaldos. Publicación por comprobar en rama remota; no se declara ocurrida por prepararla.


### 2026-10-31 — Power BI principal refrescado y guardado

[Evidencia253](evidencias/253-powerbi-refresco-guardado-20261031.json): tras habilitar PostgreSQL local5433 (healthy según salida), autora confirma nuevo corte31/10/2026 02:47:05p.m.; captura muestra ese corte, guardado Hoy2:49p.m., cuatro filas suprimidas, medidas visibles vacías y leyenda de población parcial/datos simulados. Propósito: actualizar sección analítica del ensayo. Original con nombre personal en cabecera conservado en espacio auxiliar fuera de Git; hash de imagen y PBIX local registrados, binario no publicado automáticamente. No se verificaron credenciales efectivas, DAX/SQL de esta ejecución, números positivos o permisos SQL; las pruebas previas conservan alcance independiente. Archivos: evidencia253, guía Power BI, analítica, resumen, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON, hashes y referencias comprobados; sin pruebas funcionales adicionales del agente ni publicación remota en este avance.


### 2026-10-31 — Salud API posterior al refresco Power BI

La autora aporta GET /health/db con status ok/database postgresql después de habilitar puerto BI, reiniciar PostgreSQL y refrescar el principal. Incorporado a evidencia253; solo confirma esta comprobación de conexión/esquema, no todos los workers u operaciones. Archivos: manifiesto253 y bitácora. Validación: JSON releído con respuesta esperada. No hay cambio de alcance de entrega, pruebas nuevas del agente o publicación remota.


### 2026-10-31 — Borrador de informe académico basado en evidencias

Creado INFORME_ENTREGA_BORRADOR.md con objetivo, alcance, arquitectura, resultados, operación, limitaciones y conclusiones. Actualizada matriz de entregables: RNF-2 ya cuenta con carga aprobada, recuperación lógica Docker y custodia tienen evidencia; recuperación integral y aceptación siguen pendientes. Enlazado desde índice. Propósito: preparar entrega pronta sin inventar trabajo de campo, capacitación, fechas, firmas o impacto. Archivos: informe, índice, entregables, bitácora, backlog y trazabilidad. Validación: enlaces locales comprobados, cifras contrastadas con220/RESULTADOS_V4 y resultados conservados; sin nuevos tests o llamadas externas por redacción. Borrador local, no publicado ni presentado como informe institucional aprobado.


### 2026-10-31 — Paquete del código publicado para revisión

Se genera fuera del repositorio ZIP del commit públicobbaad73eea873739a456b0b21e8438610cb392d8, SHA256 `11e96e4d838293d3ca76d76dd3f9e1b68124698f108937983fe2b35bbbed2e96`, 5323995 bytes. Propósito: facilitar entrega revisable con código, informe en borrador y guías publicadas. Comprobación: CRC ZIP, presencia de README/informe y exclusión de .env, .git, dependencias, .pgdata y dumps; sin instalación limpia nueva. Se adjuntan guía y manifiesto fuera de Git. PBIX del ZIP corresponde únicamente a versiones ya publicadas; el principal refrescado localmente y captura con nombre personal no se incorporan. La usuaria decide no implementar correo externo por ahora; Mailpit mantiene el alcance local, sin alterar requisitos institucionales. No acta de entrega o aceptación ni publicación nueva.


### 2026-10-31 — Instalación nueva del núcleo y persistencia tras reinicio

[254](evidencias/254-instalacion-nueva-bloqueada-redes.json) conserva primer intento incompleto por rangos de redes agotados, con imágenes construidas; se liberan dos redes QA antiguas elegibles según salida de autora. [255](evidencias/255-instalacion-nueva-nucleo-reinicio.json): segundo proyecto nuevo, base inicialmente0usuarios/0casos, migración0008/check, backend y frontend npm ci/build, HTTP/proxy ok; bootstrap realCLI,1Admin y creación UI de caso ficticio. Autora confirma conservación tras relogin y después de stop/start. Reporte conserva mismos cuatro contenedores, hash de fila,1evento CREADO,1usuario/1caso y salud API/proxy antes/después; puertos efímeros cambian. Código fuente contrastado con instalación de trabajo sin diferencias en alcance registrado. Propósito: acreditar instalación nueva acotada, no restauración integral o instalación literal NodeWindows del README. Sin IA/correo/BI, pruebas de carga o aceptación institucional. Archivos: evidencias254/255 y seguimiento documental. Validación: JSON, reporte local, comparación de fuentes y coincidencia antes/después; sin acceso independiente del agente al daemon. Cierre de recursos aún pendiente, sin borrado de volúmenes; publicación pendiente.


### 2026-10-31 — Cierre del ensayo de instalación nueva

La autora aporta ENSAYO_DETENIDO_DATOS_CONSERVADOS para plurione-install-da463a2d815a; reporte local registra cuatro IDs detenidos y volumes_deleted=false, después de validación de pertenencia y Running=false por auxiliar. Evidencia255 completada con cierre y hash final de reporte. El panel aislado32771 queda apagado; no se elimina base de prueba. Propósito: finalizar uso de recursos del ensayo tras persistencia comprobada. Archivos: evidencia255 y seguimiento de bitácora, QA, backlog, entregables, trazabilidad, aceptación, mantenimiento y resumen. Validación: JSON y reporte contrastados. No acredita perfiles externos o recuperación integral de instalación previa; no publicación remota en este avance.


### 2026-10-31 — Consolidación publicable de instalación nueva

Informe en borrador, MVP y resumen incorporan255 como ensayo nuevo de núcleo y persistencia en configuración QA propia, sin afirmar recuperación integral anterior. Se agrupan254 (fallo de redes),255 (recorrido satisfactorio y cierre) y notas de paquete revisable/correo externo diferido. Archivos: informe, MVP, resumen y seguimiento; evidencias sin contraseña ni datos del respaldo. Validación documental: JSON, enlaces y diff; versión fuente permanece bbaad73 y comparación de88 archivos registrada en255. No nuevas pruebas del producto por esta consolidación; publicación se verifica contra main remoto.


### 2026-10-31 — Recuperación de copia con aplicación y permisos BI

[Evidencia256](evidencias/256-recuperacion-copia-app-permisos-bi.json): respaldo identificado de75624bytes restaurado a otra base del proyecto QA; catálogo14tablas/2vistas/2secuencias/15índices no asociados a restricciones/20restricciones PK-UQ/25FK coincide por nombres/tipos,0restricciones sin validar, secuencias last_value/is_called coincidentes,9usuarios/8casos, revisión0008. API/panel contra copia y check Alembic sin diferencias;30sesiones históricas revocadas solo en copia. Autora confirma login Admin RH y consulta de expediente. Tras reinicio inesperado Windows41/6008, contenedores exited255: comprobación posterior conserva recuentos/revisión/secuencias. Causa del reinicio desconocida; no inferir fallo Docker o memoria a partir de esos registros.

Cuenta BI nueva creada por CLI después de un intento rechazado por longitud; siete comprobaciones reales de permisos: dos vistas permitidas, cinco42501 (lectura/UPDATE/DELETE users y CREATE public/analytics), sin atributos privilegiados. default_transaction_read_only desactivado solo en sesión de prueba para verificar ACL; ROLLBACK por prueba. Fuente: salidas/reporte local y confirmaciones de autora, sin daemon independiente del agente. Cuatro contenedores detenidos y volúmenes conservados al cierre.

Propósito: ampliar recuperación lógica230 e instalación nueva255 hacia uso de copia y reconstrucción acotada de permisos BI. No equivalencia literal de todos los propietarios/ACL/globales, definiciones o filas del origen actual; no proveedores externos/BI Desktop, RTO/RPO o aceptación institucional. Archivos: evidencia256, matriz, resumen, informe, mantenimiento, MVP, bitácora, QA, backlog, entregables, trazabilidad y decisiones. Validación: JSON/reporte, hash del respaldo, resultados de siete ACL y cierre contrastados; auxiliares probados offline/simulados según manifiesto. Credenciales, dump y datos individuales no publicados; registro local pendiente de publicación.


### 2026-10-31 — RF-8: bandeja sin responsable

[257](evidencias/257-filtro-sin-responsable-regresion-local.json): faltaba filtro exigido enRF-8. API unassigned=true y selector React de gestores implementados; mismo predicado de visibilidad/filtros en filas y total, conflicto de filtros422, vuelve a página1 y limpiar retira selección. Sin migración o cambio de datos. Ocho nuevos escenarios backend y dos frontend.

Validación local: selección44passed/63subtests/12.74s; suite completa en copia escribible476passed/22skipped/147subtests/47.65s; frontend71tests/10archivos/68.04s; build25módulos correcto. Dos pases generales originales interrumpidos, primero con fallos y sin traza final; no aprobados. No se atribuye causa exclusiva sin traza; repetición completa en copia escribible correcta.22 integraciones PG/analítica omitidas no aprobadas aquí; CI pendiente.

Archivos: API incidents y tests nuevos, App/cliente/pruebas frontend, manual/guía, PRD informativo y seguimiento. Tres notas obsoletas de implementación del PRD actualizadas, sin cambiar reglas. Backend fuente actualizado; frontend operativo anterior hasta coordinar imagen API. Prueba UI real y formal RNF-2 para nuevos hashes pendientes:220 es resultado histórico, no aprobación automática del nuevo código. Sin proveedor externo ni aceptación institucional.


### 2026-10-31 — CI remoto de RF-8 aprobado y actualización preparada

[258](evidencias/258-ci-filtro-sin-responsable-aprobado.json): commit4d8e48e publicado y fetch verificado; Frontend41260063541 y Backend41260063582 completed/success; jobs tests/postgres-integration success. No se asignan recuentos remotos sin logs. Complementa regresión257 y verificaciones PG omitidas localmente. Auxiliar de actualización con hashes fuente congelados, protección de cambios locales, imagen API comprobada por OpenAPI antes de copiar frontend, copia previa y conservación de volúmenes; dos simulaciones sin Docker real correctas. Propósito: coordinar activación sin interfaz consultando API antigua. Archivos:258, bitácora, QA y cierre técnico. Prueba operativa UI y formal de nuevos hashes pendientes;220 sigue histórico. Registro local para agrupar publicación tras recorrido, sin nueva prueba de carga, proveedor externo o aceptación institucional.


### 2026-10-31 — RF-8 actualizado y filtro/limpieza comprobados en panel

[259](evidencias/259-filtro-sin-responsable-ui-verificado.json), capturas260/261: actualización coordinada confirma API/health/db y proxy ok, OpenAPI con unassigned y frontend aplicado después; usuaria muestra filtro Sin responsable con1resultado y, tras limpiar, Responsable Todos/8resultados. Menús RH visibles, identidad no incluida en recortes; contexto según procedimiento de autora. No se infiere total global ni detalle de asignación no capturado. Propósito: completar recorrido real del filtro de RF-8. Archivos: manifiesto259, dosPNG y seguimiento. Validación: firmas/hashes PNG, reporte de actualización y JSON contrastados; sin repetir tests o alterar casos. CI257/258 conserva alcance; formal RNF-2 de nuevos hashes pendiente. Registro local para publicación agrupada.


### 2026-10-31 — Revalidación RNF-2 de RF-8: umbral no cumplido

Propósito: verificar rendimiento formal de la versión actualizada. [Evidencia 262](evidencias/262-rnf2-version-rf8-fallida-umbral.json), corrida c7a2582aa61c4e33: tres procesos API, diez clientes, cien casos iniciales, 30 s de calentamiento y 300 s de medición completos. Resultado FALLIDA_UMBRAL: 27 646 solicitudes y cero errores HTTP; p95 listado 169,961 ms, detalle 157,902 ms, creación 265,012 ms y actualización 230,765 ms. Creación/actualización exceden el umbral estricto de 200 ms. CPU global media durante medición 93,699 %; no demuestra una causa exclusiva ni atribuye regresión al filtro. SQL: 7714 incidencias/CREADO, 7609 EDITADO, 77140 entregas encoladas, cero intentos SMTP y trabajos IA. Comprobación HTTP posterior OK y diez cierres de sesión 204. Recursos QA detenidos y datos conservados según reporte leído. Archivos: manifiesto 262 y seguimiento documental; sin cambios de producto. Validación: JSON, hash del reporte, código incidents.py, protocolo y métricas contrastados. La aprobación histórica 220 sigue limitada a su versión; esta versión permanece pendiente. Siguiente: diagnóstico breve de escrituras y estadísticas SQL antes de otra formal; no reducir umbral o concurrencia. Publicación agrupada pendiente.


### 2026-10-31 — Diagnóstico de escrituras y estructuras SQL reutilizables

Propósito: reducir trabajo repetido en escrituras tras el fallo formal 262. [Evidencia 263](evidencias/263-diagnostico-sql-y-plantillas-escritura.json), diagnóstico 232a6419420e4b6c: estadísticas SQL OK, un proceso instrumentado, smoke 2+5 s; sin acreditación RNF-2. En servidor INSERT incidencias promedió 0,866 ms y notificaciones 1,189 ms; los tiempos de driver son mayores en otra ventana y no prueban una causa exclusiva. Cambio: services/incidents.py parametriza y reutiliza tres estructuras de acceso por rol; lifecycle.py usa la misma lectura vigente; services/mail.py reutiliza la selección de destinatarios. Solo se cachea estructura SQL, nunca permisos/resultados/Session/UUID de usuario; bloqueos, consultas y transacciones conservados. Cuatro regresiones nuevas en test_write_sql_templates.py comprueban cambios de confidencialidad, conflictos, roles, actividad y parámetros sin identidad ligada. Validación dirigida: 65 passed/11,88 s. General: 473 passed, 7 failed, 22 skipped y 147 subtests/45,47 s; los siete fallos fueron PermissionError al reemplazar archivos temporales en test_ai_run_evaluation.py. Repetición de ese archivo con temporal autorizado: 16 passed/5,73 s. Intentos previos interrumpidos por espera de socketpair en TestClient; red local concedida antes de la dirigida aprobada. No se declara una ejecución general única totalmente verde. Código aplicado localmente tras comparar la base y conservar copia anterior; principal detenido, sin operar Docker ni cambiar datos. Pendientes: ganancia de rendimiento, formal con tres workers y CI/publicación de este candidato. La evidencia 220 es histórica; 262 sigue siendo la última formal de esta línea.


### 2026-10-31 — Formal del candidato de plantillas SQL: no acredita RNF-2

Propósito: medir el candidato 263 con el protocolo formal sin cambios de umbral o carga. [Evidencia 264](evidencias/264-rnf2-plantillas-escritura-fallida.json), corrida 0e2e0230b104444d: tres procesos API, diez clientes, 30 s de calentamiento y 300 s de medición; hashes de los tres servicios contrastados con 263. Resultado FALLIDA_UMBRAL: 23 918 solicitudes sin errores; p95 listado 209,787 ms, detalle 192,622 ms, creación 312,022 ms y actualización 285,435 ms. Solo detalle cumple el límite estricto de 200 ms. CPU media 88,608 %. SQL: 6775 incidencias/CREADO, 6669 EDITADO, 67750 entregas encoladas, cero SMTP y trabajos IA; HTTP posterior OK, diez cierres 204 y QA detenida con datos conservados. Frente a 262 aumentaron los cuatro p95; no hay mejora demostrada ni comparación causal controlada. Archivos: manifiesto264 y seguimiento; sin cambios nuevos de producto o despliegue principal. Validación: lectura de reportes, hashes, protocolo, métricas y detención. Pendiente: comparación controlada antes de otra modificación/formal, CI/publicación y despliegue del candidato. Aprobación220 histórica, sin extenderla a esta versión. No se declara cierre integral ni se reduce el requisito.


### 2026-10-31 — Principal reanudado según salida y comparación ABBA preparada

La usuaria reporta API, worker de correo, Mailpit, PostgreSQL y Redis healthy tras up --no-build --wait. Propósito siguiente: comparación descriptiva de RF-8 antes/con plantillas263, sin repetir todavía otra formal. [Evidencia265](evidencias/265-comparacion-abba-preparada.json): ejecutor auxiliar compare_write_templates_local.py congela copias de backend, sin .env ni dependencias privadas; verifica hashes de tres servicios y usa smoke existente con tres procesos, diez clientes y cien casos nuevos en orden A–B–B–A. Pausa los cinco servicios principales y finalmente intenta reanudarlos con imágenes existentes; conserva recursos y datos de QA. Validación: preparación sin Docker y tres simulaciones aprobadas/0,147 s (ABBA/reanudación, rechazo CPU, interrupción por QA incompleta). Archivos: dos auxiliares locales de comparación/verificación, manifiesto265 y seguimiento; sin cambio adicional de producto. Pendientes: ejecución real, interpretación descriptiva con límites, decisión sobre candidato263 y formal. No se acredita RNF-2 ni se garantiza control de carga externa/temperatura.


### 2026-10-31 — ABBA completado y agrupación de lectura de recibo/destinatarios

Propósito: contrastar candidato263 y reducir un viaje SQL de creación. [266](evidencias/266-comparacion-abba-plantillas-sql.json): cuatro smoke A–B–B–A con tres procesos y diez clientes, cero errores; creación A257–279 ms/B207–239 ms, actualización A223–251 ms/B212–227 ms. Principal reanudado con cinco servicios healthy según usuaria y exitcode0 en reporte. Conservar263 por señal descriptiva favorable en creación, sin acreditar RNF-2 ni significancia/control completo del host. CPU previa de ejecución anterior impidió toda carga; ejecutor auxiliar añadió espera15 s y hasta tres controles, conservando todas las muestras y límites30/50 %; cuatro simulaciones aprobadas/0,155 s, sin prueba real por agente.

[267](evidencias/267-creacion-recibo-destinatarios-consulta-conjunta.json): services/mail.py agrupa destinatarios y EXISTS del predicado vigente de recibo; services/incidents.py consume el permiso retornado, eliminando su consulta separada. LEFT JOIN de fila única conserva resultado con cero destinatarios. No se cachean decisiones ni se cambian autorización, bloqueo, auditoría o transacción. Test nuevo cubre tres roles, dos ámbitos, confidencialidad, conflicto de gestor y cero destinatarios; conteos previos ajustados por una consulta menos. Validación dirigida81 passed/4subtests/11,87 s; general494 passed/22skipped/147subtests/52.66 s, temporal autorizado. Primera dirigida78/3fallos: dos conteos históricos y una expectativa corregida para respetar restricción por gestor implicado. Archivos: dos servicios, dos pruebas, manifiestos266/267 y seguimiento; copia previa conservada y fuente aplicada tras verificar B. Pendientes: QA real/latencia del candidato267, CI/publicación y formal; no se declara RNF-2 aprobado para estos hashes ni despliegue del candidato en principal.

Seguimiento267 — 31/10/2026: auxiliar local smoke_receipt_group_local.py preparado contra hashes267. Congela backend C y reutiliza el ejecutor probado para una corrida smoke 2+5 s con tres procesos/diez clientes, pausa/CPU/redes QA/reanudación. Preparación sin Docker aprobada (smoke-receipt-group-769fdfcc30f7); cuatro simulaciones del ejecutor aprobadas en0,120 s tras generalizar cantidad de corridas y etiqueta del resultado. Ejecución real, ganancia y RNF-2 pendientes; no se modificaron imágenes principales.


### 2026-10-31 — Smoke C no acredita RNF-2; validación Linux preparada

Propósito: evaluar candidato267 y obtener evidencia separada del host Windows. [268](evidencias/268-smoke-consulta-conjunta-sin-acreditar-rnf2.json): smoke1eb4c64715574171, tres procesos/diez clientes, cero errores; p95 listado114,376 ms, detalle134,766 ms, creación275,641 ms y actualización241,840 ms. SQL265 incidencias/CREADO,162 EDITADO,2650 notificaciones, cero SMTP/IA. QA detenida y principal reanudado healthy según salida y reporte; una muestra breve no demuestra ganancia ni acredita RNF-2.

[269](evidencias/269-rnf2-linux-ci-preparado.json): workflow .github/workflows/performance.yml preparado con protocolo formal existente30+300 s, diez clientes/cien casos y tres procesos, umbral estricto200 ms. Runner ubuntu-24.04 separado del equipo de autora, commit/hardware identificados; sin proveedores ni datos reales. Solo report.json como artefacto14 días, no manifiestos/configuración/claves. El contador Windows de CPU global no aplica a Linux y conserva null; no se modifica guard ni veredicto. La eventual aprobación se limitará al entorno y hashes Linux, sin extenderse a laptop/producción. Archivos: workflow, evidencias268/269 y seguimiento. Validación local: sintaxis YAML/plan del provisionador; ejecución remota y resultado todavía pendientes al registrar. Mantener pruebas funcionales494/22omitidas/147subpruebas y fallos formales262/264 históricos. No se declara cierre integral ni aprobación Linux antes de leer el reporte.
