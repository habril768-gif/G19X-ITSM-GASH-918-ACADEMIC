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
