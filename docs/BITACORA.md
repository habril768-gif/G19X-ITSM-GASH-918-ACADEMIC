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
