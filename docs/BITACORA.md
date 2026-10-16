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
