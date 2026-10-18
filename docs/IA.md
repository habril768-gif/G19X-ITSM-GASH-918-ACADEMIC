# Asistencia IA — API 0.10.0 / React 0.7.0

Preparado el 17 de octubre de 2026. RF-3 parcialmente implementado: revisión explícita, trabajo durable, worker Redis/PostgreSQL, LangChain/OpenAI y sugerencia separada de decisión humana. No se hicieron llamadas reales al proveedor. Configuración desactivada por defecto.

## Revisión y decisión

Solo un Supervisor/Admin RH autorizado solicita asistencia en caso abierto, no confidencial, sin conflicto ni validación humana vigente. Escribe hechos mínimos simulados y confirma simulación y ausencia de identificadores. El formulario empieza vacío: nunca copia la descripción. Servidor exige confirmaciones, texto no vacío de hasta 4000 caracteres y retira/rechaza correos, URLs y UUID evidentes. El filtro no es anonimizador ni detecta toda información personal; no se permiten datos reales.

Cada solicitud conserva texto revisado, revisión de contenido, catálogo, gestor, modelo y prompt. Editar descripción incrementa content_revision y retira revisión previa. Volver a un texto anterior no rehabilita una confirmación vieja. Migración no genera trabajos ni envía descripciones existentes.

CLASIFICADA devuelve categoría del catálogo, prioridad 1/2/3, sugerencia y motivo. SIN_CLASIFICACION devuelve categoría/prioridad nulas y motivo: trabajo COMPLETADA sin categoría forzada, requiere aclaración o clasificación manual. ENTORNO solo ofrece Riesgos. Salida inválida o error permanente conduce a FALLIDA; atención manual permanece disponible.

UI no rellena/valida automáticamente categoría/prioridad ni cambia asignaciones, estado, resolución, classification_valid o validated_by. La primera respuesta aceptada se conserva; propietario anterior o respuesta duplicada no la reemplazan. Cambios de acceso/confidencialidad/contenido o decisión humana durante petición causan descarte operativo.

## Cola durable y reintentos

POST /incidents/{id}/ai: ai_input_text, confirmed_simulated=true y confirmed_no_identifiers=true; HTTP 202 con job_id, received, already_requested y queue_available. GET de esa ruta: seguimiento exclusivo a gestores autorizados; empleado no administra trabajos/revisión.

PostgreSQL ai_jobs guarda revisión y auditoría en una transacción. Redis recibe solo UUID, nunca texto. Fallo de notificación no pierde solicitud confirmada: worker también consulta periódicamente PostgreSQL. No usa el ID de Redis como autoridad ni como datos de petición.

Worker: bloqueo administrativo compartido, luego caso y trabajo; revalida revisor, cuenta/departamento activos, acceso, revisión, estado y confidencialidad. Registra inicio autorizado y libera transacción antes de HTTP. Una protección posterior no garantiza detener envío ya autorizado/iniciado; se descarta respuesta operativa al volver a comprobar condiciones.

Lease/token 120s, timeout proveedor 30s, tres intentos por solicitud y SDK sin reintentos ocultos. Solo conexión/rate limit/servidor transitorios reprograman (5/10s). Recuperación de intento vencido consume intentos restantes. Una interrupción después de enviar y antes de persistir puede repetir llamada/coste: no hay promesa de exactamente una vez. Token y auditoría transaccional evitan aceptar un dueño antiguo o sugerencia parcial.

Auditoría: VALIDACION_IA con source=IA y operaciones IA_ENCOLADA/IA_ENVIO/IA_REINTENTO/IA_RESPUESTA/IA_OMITIDA/IA_FALLIDA. No confundir con decisión oficial: conserva source=HUMANA, bandera/actor/fecha. Errores guardados genéricamente, sin claves, cuerpos ni excepciones crudas.

## Proveedor y configuración

ChatOpenAI, Responses API y JSON Schema estricto, store=false, sin herramientas de ejecución y con trazas LangSmith deshabilitadas en contexto. Solo instrucciones/catálogo y texto revisado: sin descripción original, título, usuario, caso o metadatos identificadores. Modelo explícito fijado al solicitar; límite de salida 1500 tokens.

store=false no garantiza retención cero ni anonimato; siguen aplicando controles del proveedor según cuenta. Fuentes: [salida estructurada OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs), [controles de datos](https://developers.openai.com/api/docs/guides/your-data), [ChatOpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai), [colas Redis](https://redis.io/docs/latest/develop/use-cases/job-queue/). Aquí PostgreSQL conserva el trabajo durable.

Variables en .env local, sin compartir/versionar:
- AI_ENABLED=false por defecto.
- OPENAI_MODEL: modelo de la cuenta compatible con Responses y salida estructurada; no se seleccionó ni comprobó acceso/coste de un modelo real.
- OPENAI_API_KEY: solo ai-worker, nunca API/frontend.
- REDIS_URL interno; sin variables VITE con secretos.

## Instalar sin activar llamadas

Desde raíz, con Docker Desktop en terminal de la autora:

~~~powershell
docker compose up -d --build --wait api
docker compose exec api python -m alembic upgrade head
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
~~~

Esperado 0005 (head), sin diferencias. Readiness /health/db exige 0005. No repetir seed/bootstrap. 0005 añade tabla/revisión sin reescribir 0001–0004 ni enviar datos; downgrade automático deshabilitado para preservar historial.

Actualizar React con Vite activo y abrir un caso autorizado. AI_ENABLED=false muestra asistencia sin activar y mantiene clasificación manual. Nueva UI en navegador real aún pendiente.

## Activación externa pendiente

Configurar modelo/clave y AI_ENABLED=true solo localmente; después:

~~~powershell
docker compose --profile ai up -d --build api ai-worker
~~~

Abrir caso ficticio sin confidencialidad ni clasificación vigente, escribir hechos simulados, confirmar casillas y solicitar. Actualizar asistencia IA consulta resultado. Confirmar categoría/prioridad después en Clasificación humana. Sin worker listo, solicitud permanece pendiente: HTTP 202 no acredita resultado.

No capturar clave, .env, formulario con datos reales o red. Proveedor/Redis reales y una única evidencia final de sugerencia se revisarán cuando exista configuración autorizada; no se declaran verificados por mocks.

## Evaluación independiente pendiente

Cálculo offline sin llamadas:

~~~powershell
cd backend
.\.venv\Scripts\python.exe -m app.ai.evaluate referencias.json predicciones.json
~~~

Referencias JSON: 50 filas kind=reference, id único, category_id 1–5, priority 1–3; cinco filas más kind=abstention. Congelar previamente etiquetas independientes y conservar procedencia/revisión/versiones. Predicciones: una fila por ID con output (cinco campos del esquema) o error. No omitir fallos/abstenciones para mejorar el denominador 50.

Metas: 45/50 categorías y 40/50 prioridades; listar todos los falsos negativos de Alta para revisión, y bloquear cualquier Alta→Baja. Cinco casos de abstención deben ir a atención manual sin categoría forzada. automated_targets_met no certifica independencia, revisión humana ni aceptación RF-3. Si se ajusta prompt con referencias, preparar otras antes de aceptación.

Fixtures sintéticos de tests comprueban el cálculo; no son conjunto independiente ni medición de calidad. No se prepararon ni ejecutaron 50+5 referencias independientes durante este avance.

## Validación

130 backend aprobadas/0 omitidas, seis integraciones PostgreSQL 18.6 aisladas, migraciones/check hasta 0005 correctos. 64 UI aprobadas; tras ajustar mensajes, ocho específicas y build 24 módulos/658ms correctos. Proveedor y Redis simulados, sin llamadas OpenAI, calidad independiente ni despliegue Docker acreditados. Resultados/límites en REPORTE_QA.md y evidencia 70 JSON. RF-3/RF-8 parciales.

Resultado final backend: 130/130, 23.65s. Incluye adaptador real LangChain/SDK contra transporte HTTP simulado; se verifican formato/store=false/límite de salida sin red ni clave real. Los pases de 129 anteriores son históricos.

Para suspender procesamiento: detener ai-worker desde Compose, poner AI_ENABLED=false localmente y recrear API para retirar nuevas solicitudes. Cambiar solo el archivo .env no cambia procesos ya iniciados. Una petición ya despachada no se puede retirar; el trabajo durable y sus controles permanecen. Nunca eliminar historial para ocultar un envío.
