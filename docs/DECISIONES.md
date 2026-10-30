# Decisiones iniciales



- Base funcional: PRD 1.6 recibido el 15 de octubre de 2026. La autora autoriza iniciar el desarrollo sin aprobación de terceros.

- Monorepositorio con backend FastAPI y frontend React separados.

- Incidencias confidenciales visibles solo para Admin RH, conforme al PRD vigente.

- Primera entrega de Git: documentación y estructura. No se presenta como MVP funcional.

- Credenciales exclusivamente locales; `.env` se excluye de Git.

- Las versiones anteriores del PRD no se convierten en commits retrospectivos.



## 15 de octubre de 2026 — Proveedor de IA



La autora elige la API directa de OpenAI, conforme a la plataforma mostrada en su captura. La integración prevista será desde el backend con LangChain; no se utilizará Azure OpenAI Service en este MVP. Se conserva el descriptivo académico original como referencia, documentando esta diferencia.



La elección no acredita conectividad: aún no se ha realizado una llamada de prueba ni seleccionado el modelo. Las credenciales se configuran localmente mediante OPENAI_API_KEY; nunca se incluyen en el frontend ni en Git. La implementación y evaluación se registrarán en avances posteriores.



## 15 de octubre de 2026 — API inicial



- FastAPI con Uvicorn, aplicación creada mediante fábrica para facilitar pruebas aisladas.

- `/health` es disponibilidad del proceso (liveness), sin acceso a datos ni llamadas externas. Las comprobaciones de dependencias se incorporarán al integrar PostgreSQL y Redis.

- Entorno virtual del backend y dependencias fijadas. No se modifica el Python global ni el .env.

- CI de backend incluida; su ejecución remota deberá verificarse tras publicar el commit.

- Referencias: https://fastapi.tiangolo.com/deployment/manually/ y https://fastapi.tiangolo.com/reference/testclient/ .



## 15 de octubre de 2026 — Entorno Compose local



- API con Python 3.11 slim y usuario sin privilegios; solo código y dependencias de ejecución dentro de la imagen.

- PostgreSQL 17 y Redis 7.4 con volúmenes nombrados; sin publicación de puertos de datos al host. API publicada solo en 127.0.0.1.

- Compose espera healthchecks antes de arrancar API; no implica integración de persistencia todavía.

- Contraseña PostgreSQL obligatoria mediante variable local; no se copia .env a la imagen ni se inyectan claves OpenAI innecesarias.

- Imágenes fijadas por línea de versión; no se afirma reproducibilidad binaria por digest. Configuración local, no de producción.



## 15 de octubre de 2026 — Persistencia inicial



- SQLAlchemy síncrono con Psycopg 3 y Alembic. Ruta de DB síncrona en FastAPI para no bloquear directamente el bucle asíncrono.

- Conexión diferida; /health no necesita configuración. /health/db comprueba conexión y revisión 0001, con respuesta genérica sin detalles de error.

- Migraciones explícitas, DDL congelado y catálogos en revisión inicial. No se crean tablas al iniciar API. No se cargan usuarios reales ni seeds de personas en esta entrega.

- Historial admite affected_user_id y actor nullable para eventos del sistema. Reglas de permisos, auditoría atómica y privilegios de producción quedan en próximos avances.



## 15 de octubre de 2026 — Fixtures de usuarios



Carga explícita, sin endpoint web y sin contraseñas. Dos departamentos DEMO y seis usuarios con identidades ficticias, en transacción. UUID estables, sin actualizar registros existentes. No es un comando de administración real ni evita Entra ID. Los eventos de auditoría de cuentas reales se implementarán con su servicio administrativo; estos fixtures solo preparan datos de QA.



## 15 de octubre de 2026 — Autenticación propia autorizada



La autora decide no utilizar Entra ID en el MVP por falta de acceso y consentimiento. Esta decisión sustituye la planificación anterior de SSO sin modificar los registros Azure ya creados. PRD vigente 1.7 en Markdown; Word 1.6 queda histórico.



Implementación: Argon2id mediante pwdlib, sesiones opacas aleatorias de 256 bits y digest SHA-256 en base, expiración fija de una hora, revocación por logout/cambio de contraseña, validación de cuenta/departamento activo. Se elige sesión revocable en lugar de JWT para simplificar revocación inmediata sin claves de firma.



No hay registro público. Bootstrap por operador con getpass; altas por Admin RH y recuperación inicial por operador. Se mantienen IDs internos, campos externos opcionales y posibilidad futura de vinculación verificada. No hay vinculación automática por correo. Migración 0002 sin eliminación de datos. Detalles y límites en AUTENTICACION.md.



## 15 de octubre de 2026 — Consolidación PRD 1.8



Se reorganiza el PRD por reglas, RF-1 a RF-8, modelo objetivo, seguridad, QA y plan. Se conserva autenticación local y Word 1.6 como histórico. El estado vigente del backlog y trazabilidad sustituye sus listas acumuladas; la cronología permanece en bitácora y Git.



Decisiones funcionales para implementar: ámbitos PERSONA/ENTORNO; afectados condicionales; participantes y exclusión de gestores involucrados; confidencialidad automática ante Supervisor/Admin implicado; bandera classification_valid sin borrar actor/fecha; revalidación antes de resolver; retroceso protector excepcional a PENDIENTE si no hay responsable independiente. Requieren migración futura; no se modifica 0001/0002.



IA: solo texto simulado mínimo revisado, sin confidenciales; OMITIDA como estado de trabajo, con atención manual. Conjunto final 50 casos con categoría y prioridad, metas iniciales explícitas; 20 casos previos solo smoke test. No se garantiza anonimización ni cumplimiento legal para datos reales. Retención de demo hasta cierre de evaluación +30 días por operador; plazos reales pendientes antes de uso productivo.



Correo: solo eventos del MVP; SLA/vencimientos fuera. RF-7 administración y RF-8 panel separados. Cronograma por diez hitos sin inventar fecha límite o capacidad semanal. Nombres técnicos existentes conservados con glosario.


## 15 de octubre de 2026 — PRD 1.9

Se conserva restricción preventiva al declarar a un gestor: validación previa por el señalado expondría el reporte. La declaración debe ser dentro del ámbito, justificada y revisada por un administrador independiente; no desactiva cuentas. Si falta revisor puede retrasarse el caso. El procedimiento para provisionar un administrador adicional es requisito pendiente, no funcionalidad del bootstrap actual.

Power BI excluye confidenciales y relaciones pendientes; celdas requieren cinco casos distintos (y cinco afectados si son personales), con supresión complementaria y sin datos ocultos importados. El reportante recibe solo acuse; no seguimiento de confidenciales. Reportes exclusivamente como testigo fuera del MVP, sin canal alternativo implementado. API y pantalla son necesarias para RF-7.

Se elimina promesa de estimaciones no hechas y se prioriza flujo núcleo antes de integraciones, manteniendo IA/correo/Power BI en entrega final. Se corrige «smoke test histórico»: 20 casos fueron solo planificados. La IA puede abstenerse y requiere validación humana. La revisión jurídica de uso real queda como condición explícita, sin afirmar ley aplicable o cumplimiento no verificados.

## 16 de octubre de 2026 — Migración 0003

Cambios aditivos sin editar migraciones previas. Casos existentes quedan PERSONA; departamento reportado toma el histórico, no el actual. Bandera preserva solo validaciones con metadatos previos completos. Categoría Riesgos conserva ID 4 del catálogo inicial. Revisión de participantes restringida por integridad de campos y sin autorrevisión; autorización global y auditoría requieren servicios futuros. Valores booleanos se declaran como expresiones SQL true/false para comportamiento consistente en SQLite/PostgreSQL. No hay downgrade automático.

## 16 de octubre de 2026 — Registro y autorización SQL

Predicado único para listar/contar/consultar, con exclusión de gestores involucrados y protección dinámica por roles de participantes/afectado. No exponer existencia vía ID: 404 para ausentes/no autorizados. Creación devuelve acuse, no expediente. Auditoría y participantes se guardan con el caso o se revierten juntos. Historial para empleado solo cronología sin actor/copias; motivos de participantes solo gestores autorizados. Máximo técnico 20 participantes por petición. No cambia el esquema ni implementa todavía todo el ciclo.

## 16 de octubre de 2026 — Gestión transaccional de casos

Se implementa API 0.6.0 sin nueva migración: clasificación humana, asignación, edición e inicio/resolución/cierre/reapertura. Se bloquea expediente con SELECT FOR UPDATE antes de reevaluar acceso y estado; auditoría y cambios se confirman juntos. El evento existente VALIDACION_IA se reutiliza para confirmación manual, con source=HUMANA. Reapertura conserva ciclo anterior en before/after del historial; no se crea tabla adicional. Cambiar descripción invalida bandera sin borrar último validador. Participantes, confidencialidad, retroceso protector y administración completa siguen pendientes; no hay integración IA/correo.

## 16 de octubre de 2026 — Protección del expediente 0.7.0

Participantes y confidencialidad se modifican solo por Admin RH independiente, bajo bloqueo del caso y con auditoría atómica. La declaración de un gestor activa protección antes de revisar; descartarla no desmarca confidencialidad. La respuesta es un acuse mínimo porque el actor puede perder acceso al declarar su propia relación. Se reutiliza CAMBIO_CONFIDENCIALIDAD con operation explícita para alta/revisión/protección; el original y revisiones anteriores se conservan. Reasignación automática a RH independiente por ID estable si el anterior pierde acceso, o retroceso protector a PENDIENTE sin responsable si no existe ninguno. Retirar protección no reinicia IA. Se mantiene esquema 0003. Provisión adicional por operador, cambios administrativos de rol/departamento, worker y concurrencia real PostgreSQL siguen pendientes.

## 16 de octubre de 2026 — Cuenta independiente por operador

Se amplía el CLI existente, sin endpoint ni migración. Exige nueva cuenta y motivo, no modifica restricciones ni asigna casos. Auditoría por servidor con actor nulo y affected_user_id; no inventa un actor humano autenticado. La independencia entre personas depende de designación administrativa; no puede demostrarse con un UUID. Detalles en ADMIN_INDEPENDIENTE.md. Paquete preparado, pendiente de aplicar.

## 16 de octubre de 2026 — Ajustes administrativos atómicos

Se conserva historial finalizado: un ajuste que requiere protección/asignación sobre RESUELTA/CERRADA se rechaza hasta reapertura. Si un caso está oculto al administrador, rechaza la modificación indirecta sin revelar IDs. Reasignación a RH elegible por ID estable; retroceso sin responsable solo para confidencialidad sin gestor independiente. Advisory lock global coordina escritura de usuarios e incidencias; recorrido completo de casos aceptado para MVP, rendimiento por medir. No se promete RF-7 completo; paquete aún por aplicar.

## 16 de octubre de 2026 — Resultado posterior a aplicación 0.8.0

Se conserva distinción entre acuse de modificación y estado persistido, y entre logout y revocación administrativa. Evidencias 38–46 consolidadas; suite completa aprobada por ejecución de la autora. No se elimina historial de intentos interrumpidos ni se presentan tres pruebas PostgreSQL omitidas como aprobadas. Ver REVISION_ADMIN_USUARIOS.md.

## 17 de octubre de 2026 — Cliente React con sesión efímera

React/Vite, cliente /api con proxy local al backend para desarrollo, sin CORS nuevo ni variables con secretos. Token solo en memoria; recarga pide login y logout retira datos aun si falla red, informando resultado no confirmado. Totales/filtros y eventos autorizados vienen de API. Primera entrega de lectura, sin botones de escritura que aún no existen. No se activa integración IA ni persistencia del navegador. Guía FRONTEND.md; CI remoto y pruebas visuales pendientes.

## 17 de octubre de 2026 — Acuse de alta y respuesta incierta

Formulario React 0.2.0 usa directorio permitido y aviso general de confidencialidad, con confirmación cuando se prevé restricción. La API decide acceso final. can_view=false muestra solo acuse; no se enlaza expediente ni se consulta su estado. Una respuesta ambigua de red/servidor bloquea reenvío en esa instancia y recomienda comprobar el registro antes de repetir. Esto reduce duplicados locales; no implementa idempotencia de backend. Sin borradores persistidos ni llamadas IA. Verificación manual agrupada con una evidencia de acuse, sin captura por campo.

## 17 de octubre de 2026 — Gestión UI con estado confirmado por API

Formularios por rol/estado, candidatos de directorio permitido y exclusión preventiva de involucrados. El backend conserva autoridad final. Cada éxito dispara lectura de detalle/historial; no se simula transición definitiva en cliente. Reapertura requiere motivo/responsable, cierre confirmación RH; edición advierte revalidación. Error 404 retira datos; respuesta incierta requiere actualización antes de repetir. Prueba manual agrupada con una evidencia final; sin repetir capturas de cada operación. UI de protección/administración queda pendiente.

## 17 de octubre de 2026 — Usuarios y protección desde UI

Se reutilizan rutas backend existentes, sin duplicar políticas de acceso. RH administra cuentas con motivo; cambios propios que revocan sesiones retiran token y vistas sin relectura. Protección usa acuse can_view y retira expediente cuando corresponde; conserva declaraciones y exige reapertura de casos finalizados. Se utiliza reasignación automática protectora del servidor sin nuevo selector. Recuperación de contraseña y CRUD departamentos no se incorporan. Verificación agrupada con una evidencia de directorio, manteniendo pruebas simuladas separadas de resultados reales.

## 17 de octubre de 2026 — Cambio de contraseña en UI

Se ofrece cambio personal a los tres roles usando el contrato existente. Confirmación solo local, sin persistencia de campos ni token. Éxito vuelve al login tras revocación por API. Red/5xx se trata como resultado incierto: retirar sesión local y no repetir automáticamente una escritura potencialmente completada. Contraseña perdida conserva recuperación por operador; no se añade restablecimiento público ni nuevas políticas de credencial. Una sola evidencia de login vacío, nunca formulario con credenciales.

## 17 de octubre de 2026 — Baja lógica y auditoría de departamentos

Se incorpora catálogo administrable por RH con tabla de auditoría propia (0004), sin distorsionar eventos de usuario/incidencia. No hay eliminación física ni traslados masivos. Baja bloqueada con usuarios activos o casos abiertos de entorno/de afectados actuales; los casos finalizados y referencias históricas se conservan. Motivo obligatorio también para alta y reactivación. Se preservan catálogos antiguos sin fabricar historia y se reutiliza bloqueo administrativo con revalidación de actor. No se declara concurrencia validada por SQLite ni migración aplicada sin evidencia. Guía DEPARTAMENTOS.md y una sola captura de historial prevista.

## 17 de octubre de 2026 — Verificación PostgreSQL sin reutilizar desarrollo

Se usa clúster nativo temporal (PostgreSQL 18.6 ya instalado) con puerto/base/credencial propios y entorno limitado al hijo; Compose conserva PostgreSQL 17. Guardas de nombre/host y current_database previenen errores de destino. Ejecutor exige cero omisiones, detiene recursos y valida su ruta antes de limpiar; si no confirma parada conserva carpeta. Un fallo/interrupción no acredita pruebas. Evidencia de CI 17 del commit anterior se distingue de ejecución local 18.6 y de futuras carreras de negocio. Rechazo automático del borrado manual de restos se respeta sin recurrir a otro mecanismo.

## 17 de octubre de 2026 — IA durable sin autoridad operativa

Texto simulado confirmado por gestor, sin copiar descripción ni admitir confidenciales/conflictos. PostgreSQL conserva solicitud y revisión; Redis solo avisa con UUID y su caída no pierde lo confirmado. Worker revalida antes/después; no se promete retirar petición ya autorizada/iniciada. Tres intentos/lease/token: puede duplicarse llamada/coste tras interrupción, no respuesta aceptada ni decisión oficial.

Abstención es trabajo completado sin categoría forzada. store=false/tracing desactivado no equivalen a retención cero. Clave solo worker y perfil ai desactivado por defecto, modelo local explícito, sin solicitudes externas en desarrollo.

Evaluación separada de fixtures: 50 referencias independientes más 5 abstenciones, todos los falsos negativos de Alta revisables y bloqueo Alta→Baja. No aceptar RF-3 ni declarar calidad sin respuestas reales/referencias independientes. Fuentes/límites en IA.md.
## 17 de octubre de 2026 — Separar propuesta de etiquetas y aceptación de IA

El asistente prepara candidatos sintéticos con justificación sin consultar al modelo evaluado; no se atribuye revisión ni independencia humana. Antes de llamadas, revisar y registrar etiquetas realmente acordadas y congelar una nueva versión con hashes. Entradas separadas excluyen etiquetas y justificaciones; el proveedor solo recibe texto/catálogo. IDs no se envían. No corregir referencias conociendo predicciones para mejorar puntuación. Esta preparación no cambia el prompt ni consume API; conjunto usado para ajuste requiere reemplazo independiente para aceptación final.

## 18 de octubre de 2026 — Conformidad sobre casos de evaluación

A petición de la autora se retira la fecha de la nota introductoria de REVISION.md y de la presentación del conjunto. La autora confirmó que los casos están bien: conformidad general reportada, sin atribuir revisión individual de etiquetas ni aprobación independiente. Manifiesto y hashes normalizados actualizados y comprobados; sin cambios en textos/etiquetas, sin predicciones ni llamadas. Congelación y evaluación pendientes.
## 18 de octubre de 2026 — Congelación y ejecución separada del sistema operativo

La conformidad general reportada habilita fijar una versión de trabajo; no se inventa revisión independiente de terceros ni examen individual observado. Se conservan borrador y referencia fijada, con hashes UTF-8/LF del catálogo, textos y proveedor; el cambio local de formato de la autora no modifica las etiquetas. Prompt productivo sin ajustar con referencias.

Evaluación mediante CLI sin base/Redis, explícitamente optativa y sin llamadas por defecto. Máximo 55 intentos acumulados, sin reintentos del SDK; diario persistido antes de envío. Una interrupción puede haber generado cargo sin respuesta registrada: marcar incierta y no reenviar, manteniéndola en denominador. No se garantiza techo monetario ni exactamente una vez ante borrado del diario/nueva carpeta. Metadatos del proveedor se limitan a modelo/ID/contadores de tokens, nunca excepciones crudas o claves. Todo fallo detiene el bloque; la misma carpeta reanuda pendientes sin repetir casos. RF-3 requiere resultados y revisión, no solo metas automáticas.
## 18 de octubre de 2026 — Conservar evaluación fallida y separar ajuste de aceptación

La ejecución v1 no alcanza categoría/prioridad; se conserva íntegra sin cambiar referencia, respuestas o denominadores. Un Alta inconcluso exige revisión aunque no haya Alta→Baja. El diagnóstico usa estas respuestas, por lo que futuras mejoras del prompt deben evaluarse para aceptación con otro conjunto independiente. Se proponen reglas generales del PRD y contexto de simulación confirmada, no respuestas memorizadas. No se implementó corrección ni se ejecutaron más llamadas en este registro. Conformidad general de autora no se convierte en validación independiente ni aceptación automática de calidad.
## 18 de octubre de 2026 — Rúbrica del PRD y separación de conjuntos v2

Cambiar prompt a plurione-classify-v2, mantener selección de modelo local, no respuestas memorizadas ni ejemplos del conjunto. Categoría por hecho principal: asistencia es específica frente a incumplimiento genérico; infracción explícita frente a condición insegura se distingue por el hecho principal, sin convertir gravedad en categoría. Ante hechos principales indistinguibles se conserva abstención. Definiciones y prioridad provienen del PRD; aclaración reflejada en 3.1, sin ampliar alcance.

Contexto de simulación confirmado por gestor pertenece a instrucciones confiables; no se exige palabra clave de simulación en cada texto. Sigue sin autorizar datos reales/confidenciales ni órdenes incrustadas. La modificación no certifica calidad. Nuevo candidato redactado después de fijar prompt y antes de observar predicciones; autoría asistente y revisión pendiente explícitas. Cero coincidencias textuales con v1 no implica independencia garantizada.

Manifest canónico permite nombres de archivos declarados y validados, hash del proveedor e instrucciones. Vista previa acepta borrador sin envío; ejecución exige conformidad/congelación. No modificar la referencia congelada v1 para superar el bloqueo de versiones. Trabajos pendientes de otra versión se omiten sin llamada; resultados ya completados conservan su procedencia. Aplicar API y worker en la misma versión para nuevas solicitudes.
## 18 de octubre de 2026 — Registrar conformidad real y separar comprobación de gasto

La respuesta explícita de la autora sobre revisión y conformidad permite fijar aceptacion-v2 sin editar textos ni etiquetas. Se atribuye solo revisión declarada, no aprobación de terceros ni independencia certificada. Snapshot del candidato preservado. Hashes normalizados para que CRLF/LF no se confunda con un cambio de etiquetas.

Comando PowerShell sin llamadas por defecto; -Ejecutar explícito construye imagen y llama al evaluador con configuración local y carpeta fija. No reconstruye producto operativo ni crea casos. Pruebas usan stub de Docker y no se declaran resultados externos. Mantener diario/carpeta para evitar reenvíos al reanudar; límite de intentos no equivale a límite monetario.
## 18 de octubre de 2026 — Cumplimiento numérico v2 con revisión humana vigente

Registrar 98 % categoría/80 % prioridad/5 de 5 abstenciones y cero falsos negativos Alta como cumplimiento del umbral en este conjunto. No convertir automated_targets_met en aprobación humana, independencia certificada ni plataforma completa. Diez Media→Baja y una categoría discrepante se mantienen en puntuación y como limitación operativa, sin modificar referencias después de predecir ni ocultar matriz.

No cambiar nuevamente prompt usando estos resultados y presentar el mismo conjunto como aceptación independiente. V1 y v2 usan textos diferentes; comparación no demuestra efecto causal aislado. Conservar ambas ejecuciones y avanzar a correo/analítica con validación humana obligatoria y QA integral pendientes. Sin nuevas llamadas o ajuste de modelo en este registro.
## 18 de octubre de 2026 — No compensar Media con otras prioridades

Implementar v3 para que la falta de Alta no derive directamente en Baja: evaluar atención operativa pronta como Media, sin exigir daño, amenaza o pérdida grave. Una fecha aislada o un asunto sin afectación no fuerza Media. Conservar Alta por peligro/conflicto activo/vencimiento grave y decisión humana; no usar regex o elevación masiva de prioridades.

Conservar metas globales y resultados v2; añadir diagnóstico complementario Media/Baja ≥80% por cada clase con al menos diez referencias, null sin muestra. No se acepta una aparente mejora clasificando todas como Media. Pares contrastivos miden ambos niveles; categoría se puntúa por separado. Nuevo conjunto propuesto tras fijar instrucciones, sin consultar predicciones ni afirmar independencia de terceros. Sin medir v3 no se declara mejora real. Scripts/evaluaciones v1/v2 no se fuerzan con nuevos hashes; cada versión conserva procedencia.
## 18 de octubre de 2026 — Fijación v3 con conformidad explícita

La respuesta de la autora sobre revisión y acuerdo permite fijar aceptacion-v3 con los mismos datos/etiquetas y hashes normalizados del candidato. Se registra revisión declarada, no independencia de terceros ni aceptación del modelo. No modificar referencias al observar resultados. Ejecución en carpeta v3 exclusiva, conservar diario/límite 55; controles con Docker simulado no son medición externa ni gasto real.
## 18 de octubre de 2026 — No aceptar una mejora parcial por promedios altos

Conservar automated_targets_met=true/media_baja_targets_met=true de v3 como cálculos históricos; cuatro Alta→Media requieren revisión y no se presentan como prioridad lista. No cambiar etiquetas o umbrales para elevar aceptación, ni inferir desempeño general por veinte pares correctos. No recomendar aplicar v3 mientras no se resuelva y verifique Alta por consecuencias graves no físicas. V2/v3 son muestras distintas, no prueba causal aislada del efecto del prompt. Mantener decisiones oficiales humanas; no introducir corrección por palabras clave ni llamadas repetidas sin propósito/versionado.

## 18 de octubre de 2026 — Alta v4 preparada y referencias revisadas

API 0.10.3/prompt plurione-classify-v4 aclara que los criterios de Alta son alternativas suficientes. Un plazo/evento inminente con consecuencia grave descrita puede exigir Alta sin peligro físico; no basta una fecha aislada. Se conservan Media/Baja, catálogo, revisión humana y prioridades oficiales sin cambios automáticos. No se añade corrección por palabras clave ni se cambia el modelo local.

El evaluador agrega all_high_priority_identified (mínimo diez referencias Alta, cero falsos negativos) y priority_checks_met (metas globales + Media/Baja + Alta; false en ejecución parcial). Diagnóstico offline separado DIAGNOSTICO_ALTAS_V3.json: global y Media/Baja históricos true, pero Alta/indicador combinado false por cuatro Alta→Media. Originales v1/v2/v3 intactos; no se reescribe el reporte histórico.

Conformidad explícita recibida sobre los nuevos contrastes y etiquetas: aceptacion-v4 fijada antes de predicciones, con hashes equivalentes al candidato. Contiene 20 Alta (doce plazos graves no físicos), 15 Media, 15 Baja, quince pares y cinco abstenciones; cero coincidencias textuales exactas anteriores no garantiza independencia estadística. Autoría sintética del asistente y revisión declarada, sin atribuir terceros. Meta complementaria Alta 20/20, Media y Baja ≥12/15 cada una; categoría ≥45/50, prioridad ≥40/50 y abstenciones 5/5.

Validación: 56 pruebas específicas aprobadas en 13.65s; suite completa con PostgreSQL 18.6 aislado: 160 aprobadas, cero fallos/errores/omisiones, 95.81s. Migración 0005 dos veces y check sin operaciones nuevas; servidor temporal detenido y archivos propios retirados. La suite incluye SQLite/SDK simulado, no son 160 integraciones del modelo. Frontend sin cambios ni repetición. Cero llamadas externas nuevas, sin inspeccionar .env ni medir precisión v4. Evidencia 83. Calidad real y aceptación integral RF-3 pendientes.

Comando preparado: scripts/EVALUAR_IA_V4.ps1 valida sin gasto por defecto; -Ejecutar construye ai-worker y evalúa con salida exclusiva ejecucion-v4, máximo 55 intentos acumulados y cargos posibles. Conservar diario ante fallos. No actualiza contenedores operativos; aplicar API/worker juntos solo cuando corresponda, sin migración nueva. Jobs pendientes v1/v2/v3 se omiten antes de envío y resultados completados se conservan. No repetir para buscar una puntuación favorable ni editar etiquetas tras ver respuestas.

## 18 de octubre de 2026 — V4 cumple metas de prioridad

Evaluación externa v4 verificada: 55 respuestas, diario 55 START/END, IDs únicos y hashes coherentes; todas las métricas recalculadas coinciden. Categoría 47/50 (94%), prioridad 50/50, Alta 20/20, Media 15/15, Baja 15/15, pares 15/15 y abstención 5/5; ningún Alta omitido. Cumple metas numéricas globales y complementarias. Tres diferencias Ausencias→Solicitudes Administrativas del mismo grupo se conservan como errores; prioridades correctas. Revisión técnica en RESULTADOS_V4.md, evidencia 84 y originales intactos.

Modelo efectivo {'gpt-4.1-mini-2025-04-14': 55}; tokens reportados 76487 entrada/4164 salida, sin cotejar factura o saldo. Conformidad previa de etiquetas no equivale a aceptación integral: human_acceptance=false preservado. Conjuntos v3/v4 diferentes, sin prueba causal aislada ni garantía general. Mantener validación humana y no repetir para buscar puntuación favorable. Evaluación no actualiza procesos operativos. Sin código/referencias/configuración modificados, llamadas nuevas ni suites repetidas; 160 pruebas backend previas. Cambio local previo de REVISION.md conservado fuera del commit. Continuar H8 correo/H9 analítica y QA final; aceptación integral RF-3 pendiente.

## 18 de octubre de 2026 — Correo por eventos preparado y probado

API 0.11.0/React 0.8.0 y migración 0006: outbox de correo en la transacción de creación, asignación/reasignación (incluidas protección y administración), resolución y reapertura. Deduplicación por evento/destinatario y omisión registrada sin destinatarios elegibles. Worker separado con consulta durable, reclamo/token y comprobación de acceso al reclamar e inmediatamente antes de SMTP. Correo mínimo ID/enlace, sin contenido del expediente ni nombres. RH autorizado consulta fallos/omisiones paginados desde React/API. El enlace requiere login y autorización vigente.

Perfil mail con Mailpit v1.27.4, SMTP solo interno y panel en loopback; no envíos a buzones reales ni claves IA en el worker. MAIL_ENABLED desactivado fuera del perfil. Un intento inicial más tres reintentos transitorios, fallo permanente sin reintento, mensajes de error genéricos. Bloqueos de caso/administración se mantienen durante despacho con timeout por socket; pueden demorar brevemente otras mutaciones. SMTP/PostgreSQL sin transacción común: Message-ID estable no garantiza exactamente una entrega; caída tras aceptación puede duplicar aviso. No confundir SMTP aceptado con recepción o lectura.

Validación: 19 específicas iniciales aprobadas (13.63s), luego ampliadas con TLS y cierre de socket; suite final 183 aprobadas/0 fallos/errores/omisiones en 41.71s con PostgreSQL 18.6 aislado. Upgrade 0006 dos veces y check sin diferencias; clúster propio detenido/retirado. Incluye siete pruebas PostgreSQL y también fixtures SQLite/transportes simulados, además de un SMTP TCP local real sin reenvío. React: 67 aprobadas en suite (157.95s) más 1 prueba de enlace autenticado; build correcto. Script ACTUALIZAR_CORREO: seis controles con Docker simulado, parser/secuencia y parada por cada fallo. YAML revisado sin expandir secretos. Evidencia 85.

Incidencias de verificación: primera prueba de recuperación esperaba un trabajo concreto sin respetar orden de cola; corregida para drenar y comprobar mismo ID/intentos. Dos ejecuciones React con forks agotaron tiempos (5 y 8 fallos, esta última con worker sin arrancar); se repitió con threads/un worker y mayor timeout, sin eliminar aserciones. Primer PostgreSQL no pudo abrir puerto (Permission denied); log y pg_ctl confirmaron servidor apagado, carpeta ignorada preservada; segundo arranque y ejecución final correctos. Ensayo YAML inicial falló por expansión PowerShell en la aserción, corregido a archivo Python literal. No se utilizaron bases de desarrollo, .env ni proveedores externos.

Pendiente recorrido Docker/Mailpit y navegador real en el equipo, CI remoto y QA integral. Script de actualización prepara ese recorrido sin seed/bootstrap ni borrados; no se ejecutó Docker desde las herramientas. No se declara RF-5 aceptado integralmente por mocks. Guía CORREO.md. IA v4/resultados permanecen intactos, sin nuevas llamadas o gasto; cambio local previo REVISION.md conservado fuera del commit.

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

## 19 de octubre de 2026 — Documentación organizada por tarea

Las guías de inicio, módulos y estado se consolidan para describir el sistema actual sin capítulos por versión. El historial permanece en BITACORA.md, QA y Git. Se conservan identificadores de migraciones, dependencias fijadas, referencias de evaluación, hashes y resultados: eliminarlos impediría reproducir o auditar el trabajo. La evaluación externa se contrasta con evidencias posteriores de correo y analítica; su puntuación orientativa no se usa como porcentaje de terminación.

## 19 de octubre de 2026 — Documentos de solución y arquitectura basados en código

Se separan propuesta (problema documentado, objetivos, compromisos, riesgos y aceptación), arquitectura (componentes, datos, flujos y límites de confianza) y manual técnico (instalación y operación). Los documentos describen el sistema implementado sin atribuir entrevistas, aprobación o despliegue productivo. Se explicitan las credenciales PostgreSQL compartidas por los procesos operativos, la cuenta BI limitada y los límites de exactamente una vez/recuperación, evitando convertir una separación de procesos en una garantía de seguridad u operación no verificada.

## 19 de octubre de 2026 — Manual de usuario y recuperación sin sustituir la base

Se separa el manual por tareas/roles de los procedimientos técnicos del operador. La recuperación se prepara como ensayo en un contenedor PostgreSQL sin red, puertos ni consumidores, con archivo copiado como binario, sin clean ni reemplazo de la base activa. Restaurar sin propietarios/ACL permite validar los datos en un destino independiente, pero no acredita restauración de privilegios; cuenta BI y permisos necesitan reconstrucción y prueba aparte. Copias fuera de Git, roles globales/configuración privada bajo custodia separada y tiempos/retención sin inventar. El documento no se marca como ensayo ejecutado ni capacitación impartida.

## 19 de octubre de 2026 — Ensayo de recuperación nativo con guardas de aislamiento

Se agrega un ejecutor que usa dos clústeres propios y nombres QA, sin leer configuración operativa. Filtra las variables libpq heredadas, compara datos y objetos de esquema, separa la restauración sin ACL de la provisión/verificación posterior BI y conserva únicamente recursos de su propia carpeta para diagnóstico. No sobrescribe reportes ni utiliza consumidores externos. El bloqueo de creación de token restringido de Windows no se elude ejecutando directamente el servidor; se registra y deja la ejecución completa para la terminal de la responsable.

## 20 de octubre de 2026 — Comparación de esquema tras copia lógica

La restauración nativa conservó todas las filas, pero PostgreSQL descompuso casts de arrays de literales varchar sin límite a text en casts por elemento al volver a analizar las definiciones. La comparación textual inicial produjo falsos rechazos (100–102). Se normaliza exclusivamente esa equivalencia en definiciones, sin retirar casts de columnas, varchar(n), números, valores o seguridad de vistas. Datos y opciones de seguridad se comparan exactamente; cinco pruebas cubren casos equivalentes, valores con comillas/espacios, idempotencia y cambios que deben rechazarse. El ensayo 103 pasó sin modificar datos para hacerlo aprobar. La cuenta BI se reconstruye y valida por separado porque la copia de una base no traslada roles globales.


## 20 de octubre de 2026 — Modelo de una tabla y formatos explícitos

Se desactiva fecha/hora automática únicamente en el PBIX actual para conservar Indicadores como única tabla; las fechas se muestran mediante columnas directas. Porcentajes existentes: división entre 100 y formato Porcentaje/un decimal. Horas: Número decimal/dos decimales. No se alteran medidas por celda, supresión o totales. Evidencia 104 distingue propiedades configuradas de verificación visual con valores publicables, todavía pendiente. El refresco fallido no actualiza el corte ni permite entregar el informe como actual; habilitar puerto local mediante compose.bi.yaml y repetir sin cambiar seguridad o credenciales.


## 20 de octubre de 2026 — QA separada del informe conectado

Se conserva el principal con PostgreSQL y se prueban formatos/medidas y retirada Desktop en copias identificadas QA con agregados ficticios manuales. Una copia mantiene caché publicable y otra el estado suprimido; la entrada activa termina suprimida. No se rebaja privacidad para obtener cifras ni se modifica la base de uso. La prueba de sustitución JSON→Desktop no se presenta como recorrido de cambio de elegibilidad SQL integrado; ambos alcances permanecen explícitos en 105/106 y matrices. Retirada de copias distribuidas y aceptación siguen siendo tareas operativas separadas.


## 20 de octubre de 2026 — Puente agregado explícito para QA de elegibilidad

El ensayo nuevo genera ambos estados desde las vistas con cuenta BI real, sin sintetizar métricas, y usa JSON agregado para llevarlos a la copia Desktop. Se mantiene explícito ese transporte y se compara el corte esperado por fase para rechazar caché antigua. No se introducen credenciales en archivos ni se cambia la fuente del principal. Este ensayo no reemplaza la prueba del conector directo contra servidor aislado si la aceptación la exige, ni la matriz API/UI o la retirada operativa de copias.


## 21 de octubre de 2026 — Generador HTTP de rendimiento separado

Se implementa un generador con biblioteca estándar de Python, sin plugins pytest ni cambios en dependencias del producto. Usa un cliente/sesión por usuario y barrera común; no reintenta escrituras y mantiene fallos separados de latencias de éxito. Exige puerto alternativo, cuentas y prefijos QA, fixture de cien casos e identificación del entorno. La declaración de recursos aislados es del operador, no una inspección Docker automática. El modo corto no acredita RNF-2 y modifica el fixture: requiere una corrida formal con fixture nuevo. Pruebas locales en 121; carga real pendiente.


## 21 de octubre de 2026 — Provisionar una corrida de rendimiento por proceso

El provisionador genera su Compose JSON y recursos exclusivos, sin reutilizar compose.yaml/.env/volúmenes de uso. Mantiene contraseñas aleatorias en memoria y configuración privada de contenedores, sin archivos de contraseñas. Usa servicios del producto para cien casos iniciales; credenciales y cuentas QA se preparan dentro de una base nueva. Smoke y full generan entornos distintos, conservan reporte y recursos detenidos para diagnóstico. No borrar volúmenes automáticamente. Muestreo Docker y comprobación SQL complementan el generador; resultados reales todavía pendientes. Evidencia 122 acredita pruebas simuladas, no arranque real.


## 22 de octubre de 2026 — Entrada HTTP separada en QA de rendimiento

El primer smoke creó y verificó fixture, pero el cliente del host recibió ConnectionRefusedError antes de carga. Se añade una segunda red QA no interna solo a API, conservando PostgreSQL/Redis en la red interna y sin puertos. Se valida salud HTTP antes de crear fixture y se registran redes/puertos inspeccionados. Se permite salida desde API QA; no se configura proveedor externo ni worker. No se cambia red de uso ni se atribuye causa raíz a Docker/firewall sin prueba. Corrección local cubierta por doce tests simulados, pendiente verificación real. Reporte incompleto conservado en 123.


## 22 de octubre de 2026 — Separar conexiones de preparación y fases de carga

El segundo smoke superó salud y autenticación, pero cuatro listados fallaron con excepción no tipificada. Se corrige el generador para renovar sockets al entrar en cada fase, conservando sesión y persistencia dentro de fase; conexión inicial queda medida. Se tipifican excepciones sin mensajes sensibles y sin reintentos de carga. No alargar timeouts del servidor ni excluir errores para mejorar cifras. Quince pruebas locales aprobadas; causa real y smoke satisfactorio pendientes. Evidencia 124 conserva el reporte anterior.


## 22 de octubre de 2026 — Encolado por lote conservando política de destinatarios

La línea base 126 motiva perfilar primero el coste de creación. El perfil aislado demuestra consultas crecientes por destinatario. Se extrae el predicado Admin RH independiente a una función compartida con visibility(), y la creación selecciona IDs elegibles en SQL con actividad del usuario/departamento, afectación y relaciones activas. Se busca idempotencia por todos los UUID5 en una consulta y se insertan entregas sin autoflush por búsquedas intermedias. No cambiar worker, comprobación de permisos al despachar, auditoría ni commit del servicio. Nueve escenarios SQL comparados con funciones anteriores; regresión API pendiente. No extrapolar reducción de sentencias a p95 sin nueva medición.


## 22 de octubre de 2026 — Agrupar autenticación sin caché ni cambios de bloqueo

Se reduce el coste común de peticiones protegidas leyendo AuthSession/User/Department con outer joins en una consulta. Se mantienen 401 y challenge de sesión inválida, precedencia de revocación/expiración y 403 por cuenta/departamento inactivos. populate_existing obliga a refrescar objetos ya cargados para no ocultar cambios externos; no guardar permisos en caché. No modificar expire_on_commit, get_session o la secuencia lock→visibilidad de edición para ahorrar consultas. Perfil aislado en 130; regresión API y efecto en latencia pendientes.


## 22 de octubre de 2026 — Capturar respuesta de gestión dentro de la transacción

Las rutas de clasificación, asignación, contenido y transición pasan CaseDetail.model_validate como presentador a manage_case. Se hace flush y captura antes del commit; solo se retorna después de confirmar. Un error de preparación revierte caso, auditoría y cola. No se cambia expire_on_commit global ni la secuencia de bloqueo y reevaluación de visibilidad; otros llamadores conservan ORM. Creación prepara el recibo dentro de su transacción con visibilidad actual y reutiliza el rol RH ya comprobado bajo bloqueo administrativo. Motivo: evitar SELECT de recarga después del commit y evitar un fallo de lectura después de una escritura ya confirmada. Evidencia 133 registra reducción local y límites; regresión HTTP y RNF-2 aún pendientes.


## 22 de octubre de 2026 — Instrumentación optativa solo en QA

Tras 136 se prioriza diagnóstico por etapas antes de otra optimización. Entrada ASGI separada y guard estricto de identidad QA; provisionador la selecciona solo con --diagnostic y smoke. No se cambia app.main ni el umbral RNF-2. Agregados sin datos privados emitidos al shutdown y cotejados con conteos HTTP; un reporte incompleto no se considera diagnóstico satisfactorio. SQL y commit se documentan como subconjuntos solapados; no sumar p95. Evidencia 137: 40 unitarias locales aprobadas; integración real pendiente.


## 22 de octubre de 2026 — Releer identidad y departamento en una consulta después del lock

Se mantiene la adquisición advisory existente y se usa SELECT con LEFT JOIN y populate_existing para refrescar identidad y departamento dentro de la misma transacción. Leer antes del lock podría conservar un estado anterior a una operación administrativa competidora; por eso el orden no cambia. Se exige actor persistente en la misma Session para no continuar con un objeto ajeno/obsoleto en los llamadores. Ausencias e inactividad deniegan con 403. Sin caché ni supresión de controles. Evidencia 139: reducción local de dos consultas por creación/edición; regresión API y rendimiento real pendientes.


## 22 de octubre de 2026 — Diagnosticar variabilidad antes de otra optimización

Tras 141 no se atribuye una mejora de p95 al ahorro local de SQL. Se amplía únicamente el modo QA smoke con familias de tablas de lista fija, separación de entrega/cierre ASGI y CPU por fase mediante biblioteca estándar. El reporte requiere coherencia de conteos/tiempos por familias. El generador y el host se distinguen, sin medir procesos ajenos individualmente. No se relajan controles ni objetivo RNF-2. Evidencia 142 registra validación local y primera integración v2 pendiente.


## 22 de octubre de 2026 — INSERT VALUES acotado para outbox

Tras 143 se prueba INSERT multirregistro explícito en queue_event para evitar executemany por destinatario. Bloques de 50 acotan SQL y parámetros sin cambiar transacción, destinatarios, idempotencia o despacho. No se usa upsert: los errores de escritura siguen propagándose para rollback del caso/auditoría. La creación ORM pendiente se sustituye por Core INSERT inmediato; la prueba de fallo se mueve al límite real de SQL. Evidencia 144 registra comprobaciones locales y deja API/rendimiento pendientes.


## 22 de octubre de 2026 — Reusar rol solo dentro de la operación validada

Se extrae un constructor privado puro del predicado de visibilidad, manteniendo visibility como entrada que consulta rol. Gestión y elegibilidad reutilizan el rol ya validado localmente. El bloqueo administrativo mantiene estables los cambios autorizados mediante los servicios durante esa transacción; la siguiente petición vuelve a leer. No se guardan roles en Session.info/usuario/caché, ni se combina adquisición del bloqueo de caso con el SELECT de visibilidad. Evidencia 151 registra ahorro local y deja API/rendimiento pendientes.


## 22 de octubre de 2026 — Medir saltos de hilo antes de cambiar ejecución normal

Tras 153 se añade instrumentación a AnyIO exclusivamente en la entrada QA protegida, sin parchear la instalación normal ni cambiar límites/cancelación. Etiquetas fijas y medidas agregadas preservan datos privados; reporte v3 exige integridad y llamadas completas. Medir planificación/retorno evita atribuir automáticamente el residual ASGI a SQL. Evidencia 154 documenta 56 unitarias locales e integración real pendiente.


## 22 de octubre de 2026 — Construcción local y cierre de Session en worker

Tras 155, convertir solo get_session a dependencia asíncrona elimina la planificación de la construcción no bloqueante. Se conserva Session por petición y el cierre en worker; CapacityLimiter(1) propio evita esperar el limiter general mientras se necesita devolver una conexión al pool. CancelScope protegido garantiza la limpieza ante cancelación de ámbito AnyIO, sujeta a integración real pendiente. No mover rollback/cierre SQL al event loop ni cambiar expiración, commit o servicios. [Evidencia 156](evidencias/156-sesion-apertura-sin-salto-hilo.json): siete locales aprobadas con dobles, tres integraciones preparadas; sin resultado de rendimiento nuevo.


## 22 de octubre de 2026 — Liberar únicamente redes QA vacías y registradas

Ante el agotamiento confirmado, se incorpora mantenimiento explícito de redes por nombre, etiquetas Compose y configuración/reporte locales, con revalidación por ID y límite predeterminado de dos. Se preservan contenedores/volúmenes y reportes; no se usa prune global ni subred fija que pueda solaparse. El provisionador conserva su política previa de stop. [Evidencia 162](evidencias/162-redes-direcciones-agotadas-limpieza-preparada.json): 63 unitarias con Docker simulado; limpieza real pendiente.


## 22 de octubre de 2026 — Validar el DTO junto al trabajo síncrono de cuatro endpoints

Tras 165, mantener confirmación y durabilidad y reducir un paso por hilos identificado en 164. worker_response captura el modelo dentro del mismo worker que ejecuta el endpoint; FastAPI mantiene response_model y serializa DTOs preparados. Se preserva la firma y la clase/ubicación de errores de salida. Solo las cuatro operaciones medidas cambian. La adaptación QA envuelve el worker y no la corutina; endpoint incluye validación/preparación ahora, con diferencia declarada al comparar. [Evidencia 166](evidencias/166-respuesta-validada-en-worker-preparada.json): siete locales y 64 de herramientas aprobadas; regresión API real pendiente, sin latencia nueva.


## 22 de octubre de 2026 — Leer rol junto a identidad tras el advisory lock

Tras 168, combinar el SELECT de Role.nombre con la relectura ya existente de usuario/departamento. Se hace únicamente cuando el llamador pide include_role y siempre después del mismo bloqueo administrativo; el modo previo conserva None y comportamiento. Se selecciona el nombre escalar de BD para evitar un objeto Role obsoleto precargado. El rol retornado se usa dentro de creación/gestión y su predicado, sin almacenamiento entre llamadas ni alteración de otros gestores/locks. [Evidencia 169](evidencias/169-rol-agrupado-tras-bloqueo-preparado.json): ahorro local de una consulta por escritura y nueve unitarias; integración API/PostgreSQL pendiente.


## 22 de octubre de 2026 — Agrupar página/count y rol/detalle sin caché de permisos

Tras 171, reducir viajes de lectura en SQL en vez de añadir datos de autorización persistentes al usuario o cambiar autenticación. El listado usa LEFT JOIN del agregado con la página para conservar total en offset vacío; ambas ramas comparten condiciones y snapshot de sentencia. visible_case usa Role como fila base y LEFT JOIN del caso autorizado, con distinción explícita 403/404. Se reutilizan predicados por rol y retorno ORM, sin cambios de escritura. [Evidencia 172](evidencias/172-lecturas-listado-detalle-agrupadas-preparadas.json): once locales y compilación PostgreSQL; plan/latencia y regresión API pendientes. Mayor complejidad SQL no se presenta como mejora de tiempo demostrada.


## 23 de octubre de 2026 — Reutilizar estructura SQL sin cachear autorización

Tras 174, separar una estructura Select estable de los cuatro parámetros de identidad/caso. La fábrica sin argumentos retiene solo cláusulas con bindparam, valores dinámicos None y tipos; visible_case consulta rol y expediente de nuevo con diccionario independiente por ejecución. Esto evita reconstruir aliases/predicados, sin almacenar permisos, objetos User/Session o resultados ni alterar políticas. [Evidencia 175](evidencias/175-detalle-plantilla-sql-parametrizada-preparada.json): perfil local acotado y 17 unitarias, incluidas dos sesiones concurrentes; regresión API y rendimiento QA pendientes. No extrapolar microperfil SQLite a p95 HTTP.


## 27 de octubre de 2026 — Condicionar arranque formal a línea base y capacidad QA

Ante aplicación sin cambios y CPU previa media 70,29 %, preparar validación formal conjunta en lugar de otra optimización sin perfil. El comando explícito comprueba tres muestras válidas (media <=30 %, pico de intervalo <=50 %) antes de tocar Docker, y exige liberación acotada de dos redes vacías antes de full. Son condiciones operativas, no nuevos criterios RNF-2; no garantizan estabilidad posterior. Se conservan protocolo, permisos/durabilidad y veredictos; los metadatos de arranque quedan en el reporte, sin repetir cargas automáticamente. [Evidencia 178](evidencias/178-formal-condicionada-preparada-cpu-previa-alta.json): 74 locales con Docker simulado; integración real pendiente.


## 27 de octubre de 2026 — Delegar lotes del outbox a insertmanyvalues

Tras perfil que detecta recompilacion por creacion, usar Core INSERT..RETURNING(id) con parametros separados y lotes de 50 para reutilizar compilacion. Mantener consulta vigente de destinatarios/entregas, UUID deterministas, campos y transaccion. No usar upsert, cache de destinatarios o commits por lote. Las filas devueltas no requieren orden ni objetos ORM; cerrar resultado. [Evidencia 183](evidencias/183-outbox-insertmanyvalues-compilacion-reutilizada.json): mecanismo observado y atomicidad SQLite verificada; API y PostgreSQL reales pendientes, no acredita RNF-2.


## 27 de octubre de 2026 — Reutilizacion local de departamento validado; conservar relecturas tras locks

Devolver opcionalmente rol/departamento ya revalidados por administration_lock para creacion, sin cache entre operaciones; otros departamentos siguen consulta independiente. No fusionar advisory/relectura ni lock de expediente/visibilidad: el snapshot de cada sentencia y posibles esperas requieren conservar orden para no introducir decisiones obsoletas. Esta es una precaucion de diseño basada en semantica de [SELECT PostgreSQL17](https://www.postgresql.org/docs/17/sql-select.html), no una carrera PostgreSQL ejecutada. [Evidencia186](evidencias/186-creacion-reutiliza-departamento-validado.json): 25 locales aprobadas, una consulta menos localmente; API/QA pendientes.


## 27 de octubre de 2026 — Excepcion acotada al cierre siempre en worker

Cerrar localmente solo Session de clase exacta estandar original sin transaccion: version2.1.4 instalada y pruebas muestran expunge sin IO ni pool. Todas las sesiones custom/activas conservan cierre protegido en worker independiente; no usar is_active como indicador de ausencia de transaccion. Mantener shield y propagacion sin reintentos. Esta decision acota156; no lleva SQL/rollback al loop. [Evidencia189](evidencias/189-cierre-session-limpia-sin-worker.json):14 locales aprobadas, API/AnyIO/QA pendientes. El cierre es postenvio: no declarar ahorro directo p95. Revisar fastpath si cambian version o callbacks de detach.


## 27 de octubre de 2026 — Medir pre_ping sin desactivarlo

No eliminar pool_pre_ping para ganar latencia: cumple recuperacion de conexiones obsoletas. Antes de optimizar autenticacion, medir do_ping separado porque evento de motor no lo observa. Wrapper solo en entrada QA tras guard, preserva clasificacion original de desconexion y no guarda datos privados. v4 explicito y lector compatible v3; consultas no incluye todos los viajes. [Evidencia192](evidencias/192-diagnostico-pool-pre-ping-separado.json):88 pruebas locales aprobadas, PostgreSQL QA pendiente; no ganancia p95 demostrada.


## 27 de octubre de 2026 — Retener diez conexiones sin aumentar maximo

Ante escenario10clientes, default5retenidas+10overflow recrea conexiones entreoleadas locales. Retener10yoverflow5 conserva tope15/tiempos/pre_ping/reset y evita recreacion localmente. Mas memoria ociosa posible (cinco conexiones adicionales), sin preapertura ni promesa dep95. [Evidencia193](evidencias/193-ping-postgresql-coste-medido-sin-fallos.json) mide ping, no demuestra overflow comocausaunica; [194](evidencias/194-pool-retiene-diez-maximo-quince.json) valida mecanismo con20pruebaslocales. API/PGpendientes. No reducir chequeo pre_ping ni cambiar protocolo RNF-2.


## 27 de octubre de 2026 — Retirar retencion experimental10 de194

Diagnostico196 muestra mas pings/reuso compatible, pero ninguna ganancia p95 y cincoociosas adicionales posibles. Restaurar poolbase5+10,max15,conpre_ping/tiempos intactos; database.py vuelve al hash190. No inferir causalidad adversa exclusiva por una ventana. Mantener resultados194/195/196 y demas mejoras. [Evidencias196](evidencias/196-pool-diez-diagnostico-sin-ganancia-p95.json)/[197](evidencias/197-pool-base-restaurado-experimento-retirado.json):20locales aprobadas, sin nuevaformal.


## 27 de octubre de 2026 — Medir CPU de worker antes de cambiar mas consultas

Tras retirar pool194 por falta de beneficio demostrado, separar CPU real de wall por worker con time.thread_time, sin atribuir diferencia a servidor/GIL/SO automaticamente. Solo diagnostico5 protegido y agregados; versiones3/4legibles. Mantener poolbase,SQL,locks y umbral. [Evidencia198](evidencias/198-diagnostico-cpu-worker-separada-de-tiempo.json):94locales aprobadas; medidaPGpendiente,no gananciap95.


## 27 de octubre de 2026 — ControlSQLfijo sin extensiones para separar tiempos

CPUworkers199 es baja respectoawall, sincausaunica demostrada. Prepararcontrol200 opcional SELECT1 conEXPLAIN, solodespuesdecarga enQA nuevo, sinperfilardatos reales/cambiarPG. No usarlo como p95delproducto ni restarcomponentesheterogeneos.55lecturas/limites/guard identidades, sinSQLarbitrario. [199](evidencias/199-cpu-worker-baja-frente-a-tiempo-transcurrido.json)/[200](evidencias/200-control-driver-servidor-select1-preparado.json):102localesaprobadas,PGpendiente.

## 2026-10-29 — Aviso de cierre RF-5 y publicación de avances

El corte docente pide avisos al cerrar además de registrar/asignar. Se agrega tipo CIERRE en la outbox existente, no un envío SMTP dentro del endpoint. Destinatarios: reportante y afectado con permiso vigente, deduplicados; sin acceso se registra OMITIDA. El instante closed_at del cierre se captura solo para ese tipo y se coteja antes del despacho, junto con estado CERRADA y controles previos de usuario/departamento/visibilidad. Reapertura o nuevo cierre invalida el pendiente anterior. Mantiene bloqueo administrativo/expediente, transacción de evento/outbox y reintentos existentes. Migración0008 amplía CHECK sin backfill ni reenvío; no se edita la0006 aplicada. Health/db y prueba de PostgreSQL exigen0008. Cierre sigue reservado a RH independiente. Mensaje mínimo ID/enlace y aceptación SMTP sin promesa de entrega. Ver auditoría201 y límites de pruebas.

Se preservan los commits locales posteriores al17-oct y se prepara publicación descendiente del remoto, sin force push. La carpeta .git original rechaza escritura; una copia de publicación dentro del workspace permite registrar sin modificar el índice original ni el cambio ajeno de REVISION.md. La recepción remota se registra únicamente después de comprobarla.

El gestor local de credenciales Git no permitió autenticar el push. Se usa la conexión GitHub autorizada para publicar objetos de contenido y commits descendientes del remoto. La instantánea conserva el estado del código; el bundle local conserva adicionalmente los commits originales no enviados. No se presenta una fecha de autoría reconstruida como actividad pasada en GitHub.

## 2026-10-29 — Contadores servidor para consultas reales, solo QA opcional

El control207 confirma que SELECT1 posterior no explica por sí solo el tiempo de consultas reales bajo carga. Se prepara208 con pg_stat_statements del PostgreSQL17 QA nuevo, no EXPLAIN ANALYZE sobre escrituras ni una extensión en la base operativa. Preload al crear nuevo servidor y CREATE EXTENSION protegido; sin reinicio o ALTER SYSTEM del sitio. Se comparan snapshots después del seed y después de SQL final, sin reset. Solo DB/usuario actuales; reportar familias fijas con deltas/medias de ejecución, nunca SQL o parámetros. Los IDs y stats_since se usan solo en memoria para detectar cambios de identidad/reset; dealloc/globalreset también invalidan. La ventana declarada incluye operaciones de preparación/finales y no es una estadística exclusiva de los5s HTTP.

Planning tracking permanece apagado para limitar coste adicional; esa métrica no se presenta como planificación cero. La extensión conserva texto representativo dentro del QA privado; los reportes excluyen texto e IDs. Instrumentación opcional no acredita p95 ni mejora de producto. Guardas preservan modo formal/normal sin extensión y evitan comandos PG arbitrarios. Fuente primaria: [PostgreSQL17 pg_stat_statements](https://www.postgresql.org/docs/17/pgstatstatements.html).

## 2026-10-30 — Comparar procesos antes de modificar más SQL

Las medias de ejecución de 210 son breves, con ventanas/agrupación distintas del cursor API y sin planificación/durabilidad completas. Se elige probar 1/2 procesos sobre entrada normal de app, sin nuevos cambios de permisos/SQL/índices/pool. Dos procesos solo en smoke QA nuevo y sin instrumentación; el agregador diagnóstico actual exige un emisor y se conserva. Full con 2 se rechaza: falta elegir/configurar despliegue reproducible y adaptar prueba formal tras evidencia, no se elude su control previo.

El controlador produce dos reportes originales en QA independientes con 100 casos iniciales, mismo modo sin instrumentos y 10 clientes. No reutilizar dataset crecido ni comparar como causal con ventanas instrumentadas. Secuencia fija sin reintentos, hasta 4 redes QA vacías retiradas en dos pasos acotados. Dos workers tienen memoria/pool separados y techo teórico API 30; no promesa de ganancia. Comando real del contenedor verificado, no distribución por PID. Documentación primaria: [Uvicorn](https://www.uvicorn.org/deployment/) y [FastAPI workers](https://fastapi.tiangolo.com/deployment/server-workers/).


### 2026-10-30 — Comparación API real, RNF-2 pendiente

[Evidencia212](evidencias/212-comparacion-real-uno-dos-procesos-api.json): smoke1/2 completado y coherente; p95 de dos procesos90,79/114,17/163,91/153,28ms frente252,57/202,21/290,63/249,18ms. Cero errores,339→583 solicitudes. Resultado breve favorable, sin nueva formal ni cambio operativo. Pendiente validar de forma sostenida y reproducible; conservar diez clientes, p95<200ms, locks y auditoría.


## 2026-10-30 — Validación formal QA con dos procesos preparada

[Evidencia213](evidencias/213-formal-qa-dos-procesos-preparada.json). A partir de la comparación real212 favorable y a petición de cerrar RNF-2 para entrega, se habilita `--api-workers 2` en QA formal sin diagnóstico. Sustituye la restricción histórica de211 que permitía dos solo en smoke. El guard conserva un proceso por defecto, valida el número antes de CPU/Docker y registra la selección en precondiciones. Verifica CPU previa, libera hasta dos redes QA elegibles, y provisiona un proyecto nuevo; el provisionador mantiene validación de ID propio y comando Uvicorn real. Dos procesos con diagnóstico siguen rechazados. Sitio/Dockerfile/Compose operativo, pool15 por proceso, locks, transacciones y runner/verdict intactos.

**Protocolo sin rebajar:** diez clientes, cien casos iniciales,30s calentamiento y300s medición; cada p95 de listado/detalle/creación/actualización estrictamente menor de200ms, sin errores y con verificaciones HTTP/SQL/logout/parada. CPU previa: media≤30% y cada intervalo≤50%; si no cumple, no inicia carga. No detener automáticamente servicios ajenos ni desactivar protecciones.

Comando desde raíz, con Docker abierto:

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/run_performance_full_guarded.py --api-workers 2 --confirm-isolated-qa
```

Validación realizada:126 pruebas de herramientas aprobadas en4,827s, AST de cinco archivos correcto; se comprobó que runner y configuración productiva no cambiaron frente a la versión publicada. Nuevas pruebas cubren selección full2 en CLI, rechazo de diagnóstico, guardas CPU/redes no eludibles, validación anticipada y despacho full sin convertirlo en smoke; resultado FALLIDA_UMBRAL simulado conserva fallo y parada. No se ejecutó carga Docker desde el agente. Pendiente corrida real del usuario, lectura íntegra del original y acreditación únicamente si cumple. Siete fallos formales anteriores siguen documentados; aún no hay octava formal. Dos procesos aumentan memoria y techo API a30 conexiones. Un éxito futuro solo acredita el alcance y hardware declarados, no rendimiento universal ni proveedores externos.

Archivos: provision_performance_qa.py, run_performance_full_guarded.py y tres pruebas relacionadas; evidencia213 y documentación de seguimiento. No se afirma RNF-2 listo antes de observar la ejecución real.
