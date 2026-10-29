# Asistencia IA

RF-3 dispone de revisión explícita, trabajo durable, workers Redis/PostgreSQL y sugerencias separadas de la decisión humana. Se realizaron pruebas integradas y evaluaciones sobre casos simulados; los resultados y límites están en el reporte QA y la documentación de evaluación. La configuración distribuida mantiene IA desactivada por defecto.

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
- OPENAI_MODEL: modelo explícito de la cuenta compatible con Responses y salida estructurada; comprobar disponibilidad y coste antes de nuevas llamadas.
- OPENAI_API_KEY: solo ai-worker, nunca API/frontend.
- REDIS_URL interno; sin variables VITE con secretos.


## Instalar y activar

Aplica las migraciones con `alembic upgrade head` según el README. No repitas bootstrap ni seed. Con `AI_ENABLED=false`, la gestión manual permanece disponible y no se habilitan llamadas por iniciar el núcleo.

Para activar asistencia, configura localmente `AI_ENABLED=true`, `OPENAI_MODEL` y la clave del worker. Desde la raíz:

```powershell
docker compose --profile ai up -d --build api ai-worker
```

Actualizar API y worker juntos evita procesar solicitudes con instrucciones incompatibles. Los trabajos y resultados conservan su procedencia; no reescribir sugerencias completadas para aparentar una evaluación nueva.

En un caso ficticio elegible, escribe texto mínimo, confirma las casillas y solicita asistencia. Actualizar asistencia consulta el resultado sin crear otra solicitud. Después confirma la clasificación oficial en el formulario humano. Cada envío elegible al proveedor puede consumir saldo.

## Evaluación y resultados

Se registraron ejecuciones externas con referencias simuladas revisadas por la autora. El último conjunto obtuvo prioridad 50/50, categoría 47/50 y abstenciones 5/5; no omitió prioridades Alta en ese conjunto. Se conservan tres diferencias de categoría y la revisión humana obligatoria. Estos resultados no garantizan desempeño en datos nuevos ni certifican revisión independiente de terceros.

Consulta el [resultado detallado](evaluacion_ia/RESULTADOS_V4.md) y el [conjunto fijado](evaluacion_ia/aceptacion-v4/README.md). Las evaluaciones anteriores son historial de desarrollo; sus archivos, hashes y diarios se conservan sin mezclarlos. No volver a ejecutar para buscar una puntuación mejor ni modificar etiquetas después de observar predicciones.

La ejecución de evaluación es separada del arranque y exige su procedimiento específico; no debe automatizarse por un cambio documental. Correo e informe Power BI tienen guías propias.

## Aceptación pendiente

Las evidencias 71–73 muestran el primer recorrido integrado; la 84 documenta la medición más reciente. Falta aceptación integral y completar controles operativos según QA. No se considera terminada la plataforma por cumplir las metas numéricas de un conjunto. La IA sigue limitada a texto simulado revisado y no sustituye atención humana.
