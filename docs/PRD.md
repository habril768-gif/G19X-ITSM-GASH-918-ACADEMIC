# PRD PluriOne 1.9

Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V.

| Dato | Valor |
| --- | --- |
| Clave | G19X-ITSM-GASH-918-ACADEMIC |
| Autora | Gilian Abril Sánchez Hernández |
| Fecha de consolidación | 15 de octubre de 2026 |
| Versión | 1.9 — base de desarrollo |
| Autenticación | Local en FastAPI |
| Fuente vigente | Este archivo PRD.md |

Este documento consolida las reglas del MVP. Describe comportamiento requerido, no certifica funcionalidad implementada. El estado real y sus evidencias se consultan en [TRAZABILIDAD.md](TRAZABILIDAD.md), [BACKLOG.md](BACKLOG.md) y [REPORTE_QA.md](REPORTE_QA.md). La copia Word 1.6 es histórica; las versiones previas de este texto se conservan en Git. No se exige aprobación de terceros para desarrollar.

## Índice

- [1. Objetivo y alcance](#1-objetivo-y-alcance)

- [2. Actores y permisos](#2-actores-y-permisos)

- [3. Reglas de negocio](#3-reglas-de-negocio)

- [4. Requisitos funcionales](#4-requisitos-funcionales)

- [5. Arquitectura y tecnologías](#5-arquitectura-y-tecnologías)

- [6. Modelo de datos objetivo](#6-modelo-de-datos-objetivo)

- [7. Seguridad y datos](#7-seguridad-y-datos)

- [8. Requisitos no funcionales](#8-requisitos-no-funcionales)

- [9. Evaluación y aceptación](#9-evaluación-y-aceptación)

- [10. Plan de entrega](#10-plan-de-entrega)

- [11. Supuestos dependencias y riesgos](#11-supuestos-dependencias-y-riesgos)

- [12. Glosario y cambios](#12-glosario-y-cambios)

## 1. Objetivo y alcance

Registrar, clasificar y dar seguimiento a incidencias, con decisiones humanas auditables y acceso restringido. El MVP académico se demuestra exclusivamente con datos simulados. No se ha medido todavía una mejora operativa real; se evaluarán funcionamiento y métricas técnicas.

| Dentro del MVP | Fuera del MVP |
| --- | --- |
| Autenticación local; cuentas administradas por Admin RH | Entra ID, MFA y registro público |
| Incidencias personales y riesgos generales | Nómina, pagos y procedimientos legales automatizados |
| Registro de hechos que afectan al propio empleado | Denuncias como testigo exclusivamente sobre terceros; sin canal alternativo implementado |
| Clasificación asistida y validación humana | Decisiones disciplinarias automáticas y chatbots |
| Panel React, filtros y detalle | Aplicaciones móviles nativas |
| Correo por eventos | SLA, vencimientos, escalamiento por tiempo y alertas periódicas |
| Analítica agregada Power BI Desktop | Dashboard de Power BI con expedientes individuales |
| Historial, manuales, QA y plan de soporte | Uso de datos laborales reales y despliegue productivo |

No se permite eliminar incidencias mediante la aplicación. Los errores de registro se resuelven administrativamente con motivo, siguiendo el ciclo normal.

## 2. Actores y permisos

- **Empleado:** registra hechos personales o riesgos de su departamento y consulta sus casos personales no confidenciales.

- **Supervisor:** registra y gestiona casos de su departamento cuando no sean confidenciales y no esté involucrado.

- **Admin RH:** administra cuentas y gestiona casos, incluidos confidenciales, excepto aquellos en los que esté involucrado.

- **Gerencia:** recibe reportes agregados; no es un rol de acceso a expedientes en el MVP.

- **Operador del servidor:** provisiona el primer administrador, restablece contraseñas y realiza mantenimiento. No se presume que pueda atender expedientes mediante la aplicación.

Los permisos requieren cuenta y departamento activos y se aplican en la API, no solo ocultando botones. Estar asignado nunca otorga acceso que contradiga estas reglas.

| Operación | Empleado | Supervisor | Admin RH no involucrado |
| --- | --- | --- | --- |
| Crear personal | Afectado = él mismo | Afectado de su departamento | Cualquier afectado |
| Crear riesgo general | Su departamento | Su departamento | Cualquier departamento |
| Consultar personal no confidencial | Si es el afectado | Departamento actual del afectado | Sí |
| Consultar riesgo general no confidencial | Solo si lo creó y sigue en ese departamento | Departamento reportado | Sí |
| Consultar confidencial | No, incluso si reportó | No | Sí |
| Validar, asignar, resolver | No | Caso visible sin conflicto | Sí |
| Cerrar, reabrir o retirar confidencialidad | No | No | Sí |
| Administrar cuentas y departamentos | No | No | Sí, con restricciones de RF-7 |

## 3. Reglas de negocio

### 3.1 Categorías y prioridad

| Categoría | Definición | Ejemplo simulado |
| --- | --- | --- |
| Ausencias | Faltas, retardos y permisos no autorizados | Ausencia sin aviso |
| Conflictos | Problemas interpersonales | Discusión por recursos compartidos |
| Incumplimientos | Violaciones de políticas internas | Uso indebido de equipo |
| Riesgos | Condiciones inseguras o accidentes menores | Piso mojado sin señalización |
| Solicitudes Administrativas | Trámites que requieren seguimiento | Solicitud de constancia |

Prioridad Alta: amenaza inmediata de seguridad, conflicto activo con riesgo de daño o plazo explícito con consecuencia grave. Media: impacto operativo que requiere atención pronta sin amenaza inmediata. Baja: situación sin urgencia identificada. Ante ambigüedad, el responsable humano determina prioridad y registra justificación. Una categoría no determina automáticamente su prioridad. Estas prioridades no constituyen SLA ni reemplazan canales de emergencia.

### 3.2 Persona, entorno y participantes

`scope` distingue PERSONA y ENTORNO. PERSONA requiere `affected_employee_id`; ENTORNO exige que sea nulo y solo admite categoría Riesgos. En ENTORNO es obligatorio `reported_department_id`.

Un empleado reporta un conflicto que le afecta seleccionándose como afectado y declarando a otros participantes; no registra una incidencia personal exclusivamente sobre un tercero. Los reportes como testigo exclusivamente sobre terceros quedan fuera del MVP. Este sistema no ofrece todavía un canal alternativo para recibirlos ni promete derivación automática; esa limitación se indica antes del registro. Un riesgo físico sin víctima se registra como ENTORNO; no se inventa un empleado afectado.

El departamento reportado de PERSONA se obtiene del afectado al registrar. `department_id_at_creation` es la copia inmutable de ese departamento; en ENTORNO es copia del departamento reportado. Sirve para analítica histórica. La visibilidad personal utiliza el departamento actual del afectado; la de ENTORNO, el departamento reportado. Los cambios de departamento requieren revisar asignaciones que pierdan autorización.

Los participantes se guardan por ID; el afectado siempre cuenta como involucrado. El reportante no cuenta como involucrado por el solo hecho de registrar. El Empleado declara participantes solo al crear su caso personal; selecciona usuarios de su departamento y contactos de gestión Supervisor/Admin RH habilitados en un directorio mínimo de nombres y roles, sin correos ni información del resto del personal. No puede cambiar el afectado ni editar participantes después del envío. El Supervisor declara dentro de su departamento y esos contactos; Admin RH independiente puede completar la declaración con auditoría. No hay incorporación masiva ni selección arbitraria de IDs fuera del conjunto permitido por la API.

Cada participante adicional exige explicar su relación con el hecho; no se exige adjuntar pruebas para admitir un reporte. La relación tiene estado DECLARADO, CONFIRMADO o DESCARTADO, motivo original y actor/fecha de revisión. Una declaración sobre un gestor aplica protección preventiva inmediatamente; no se expone el caso a esa persona mientras se valida. No desactiva su cuenta ni restringe otros expedientes. Solo Admin RH independiente revisa la relación y confirma o descarta con motivo, conservando el original. Descartar una relación no equivale por sí solo a retirar confidencialidad solicitada.

Si se declara al único Admin RH, el caso sigue restringido hasta disponer de un revisor independiente. El operador puede provisionar otro administrador mediante el procedimiento auditado pendiente de RF-7; no juzga el contenido ni desbloquea al señalado. No hay desbloqueo automático por tiempo ni validación por el propio involucrado. La protección reduce el riesgo de exposición, pero admite que declaraciones erróneas o abusivas puedan retrasar ese caso. La interfaz lo informa y la revisión queda auditada. Las restricciones se recalculan al cambiar participantes o roles.

### 3.3 Confidencialidad y conflicto de interés

Cualquier rol puede solicitar confidencialidad al crear. Mientras sea confidencial, el reportante pierde acceso; el formulario lo explica antes de guardar. Solo se entrega acuse de recepción con ID de referencia, sin enlace accesible, participantes, estado posterior o resultado. Un Supervisor/Admin RH afectado tampoco puede consultar su propio expediente. No existe seguimiento de estado ni notificación de resultado para quien carece de acceso; esta es una limitación deliberada del MVP, no una entrega ya satisfecha al reportante.

Un caso que involucre a un Supervisor o Admin RH pasa automáticamente a confidencial y exige atención por un Admin RH no involucrado. Una persona involucrada con privilegios de gestión no puede consultar, asignar, clasificar, resolver, cerrar, reabrir ni modificar restricciones de su caso. No basta ocultar el botón. No se excluye a un empleado de sus casos personales no confidenciales por ser el afectado.

Si no hay Admin RH activo e independiente, el caso queda PENDIENTE y restringido, sin responsable, hasta disponer de uno. El operador podrá provisionar una cuenta independiente mediante el procedimiento administrativo, sin otorgar acceso al involucrado ni autoasignar el caso. No se garantiza resolución mientras falte ese responsable.

Solo Admin RH no involucrado puede cambiar confidencialidad de un caso existente. En EN_REVISION, pasar a confidencial exige reasignar atómicamente a un Admin RH activo e independiente; si no existe, se devuelve a PENDIENTE, conserva historial y queda sin responsable. Este retroceso solo se admite para protección de acceso, con motivo obligatorio. En RESUELTA/CERRADA se exige reapertura antes del cambio.

Retirar confidencialidad exige motivo y no puede hacerse mientras siga involucrado un Supervisor/Admin RH. La corrección/revisión de participantes sigue los estados y permisos de 3.2, exige motivo y auditoría y nunca puede realizarla el involucrado; una relación DECLARADA o CONFIRMADA mantiene la exclusión del gestor. El acceso no se restaura por haber empezado RH a atender el caso, sino por cambiar válidamente la restricción.

### 3.4 Estados y validez de clasificación

Se usan exclusivamente PENDIENTE, EN_REVISION, RESUELTA y CERRADA.

| Transición | Actor autorizado | Condiciones |
| --- | --- | --- |
| PENDIENTE → EN_REVISION | Supervisor autorizado o Admin RH independiente | Responsable activo y autorizado; categoría/prioridad; validación vigente; registrar inicio del ciclo |
| EN_REVISION → RESUELTA | Supervisor autorizado o Admin RH independiente | Validación vigente; resolución no vacía; registrar resolved_at |
| RESUELTA → CERRADA | Admin RH independiente | Registrar closed_at |
| RESUELTA/CERRADA → EN_REVISION | Admin RH independiente | Motivo; responsable activo autorizado; archivar ciclo; limpiar resolución y fechas finales; actualizar inicio |
| EN_REVISION → PENDIENTE | Admin RH independiente | Solo protección por confidencialidad sin responsable elegible; motivo e historial; desasignación atómica |

`classification_valid` inicia en FALSE y es la fuente explícita de vigencia. `validated_by` y `validated_at` identifican la última validación y no se borran al invalidarla. Editar descripción o cambiar la categoría/prioridad oficial pone la bandera en falso; confirmar validación la vuelve verdadera y actualiza actor/fecha. La validación confirma categoría y prioridad juntas. La corrección y su confirmación pueden ser una sola operación auditada.

Un caso EN_REVISION puede permanecer allí con bandera falsa tras una edición, pero no puede resolverse hasta revalidar. Solo se exige validación vigente al entrar inicialmente en revisión y al resolver. La sugerencia IA original no se sustituye ni relanza automáticamente al editar; se avisa que corresponde al texto anterior.

La reapertura archiva resolución y fechas anteriores, conserva clasificación si sigue vigente y registra cada ciclo. Cualquier cambio posterior de descripción requiere revalidación. Todos los cambios de estado, responsable, validación y acceso se guardan en una transacción con el evento de auditoría.

## 4. Requisitos funcionales

### RF-1 Autenticación local

Correo único sin distinguir mayúsculas, contraseña de 12–128 caracteres con Argon2id, cuenta/departamento activos, sin registro público. Primer Admin RH mediante comando interactivo del operador. Sesión opaca de 256 bits, digest SHA-256 en base, una hora de vigencia. Roles se consultan en base. Logout revoca sesión actual; cambio/restablecimiento de contraseña revoca todas. Cinco fallos por correo bloquean 15 minutos con respuesta genérica. Recuperación inicial por operador, no por correo.

**Aceptación:** login válido permite /auth/me; contraseña incorrecta, expiración y logout rechazan acceso; cuenta desactivada pierde acceso; ningún hash aparece en respuestas. No se requieren credenciales Microsoft ni JWT.

### RF-2 Registro y edición

Formulario: título, descripción, fecha del evento, ámbito, afectado cuando aplique, departamento cuando aplique, participantes y solicitud de confidencialidad. El servidor obtiene autor, departamento histórico y estado PENDIENTE. Aplica reglas de actores y conflicto antes de devolver datos. La respuesta de creación confidencial no expone el expediente a quien perdió acceso; solo confirma recepción.

Solo gestores autorizados editan título/descripción en PENDIENTE o EN_REVISION, conservando valores anteriores. RESUELTA/CERRADA requieren reapertura. No hay eliminación ni estado ANULADA.

**Aceptación:** rechazar ámbito/afectado incompatibles, registros fuera de departamento y cambios no autorizados; permitir riesgo sin víctima; la edición invalida clasificación; los errores se resuelven con motivo «Registro creado por error; sin acción correctiva» siguiendo el flujo normal.

### RF-3 Clasificación IA y validación humana

OpenAI mediante LangChain y worker Redis. El MVP procesa solo textos simulados, no confidenciales y revisados para no incluir identificadores personales. No se envía automáticamente la descripción original: un gestor autorizado confirma un `ai_input_text` simulado y mínimo antes de encolar. Los casos confidenciales, conflictos de interés y textos no elegibles se clasifican manualmente, con `ai_status=OMITIDA` y motivo.

Antes de enviar, el worker vuelve a comprobar elegibilidad y permisos. Si el caso se volvió confidencial, cancela el envío. Si la petición externa ya salió, no se puede retirar; se registra el hecho y se descarta la respuesta para uso operativo. No se puede afirmar confidencialidad retroactiva sobre información ya enviada.

La IA puede devolver resultado CLASIFICADA o SIN_CLASIFICACION. En CLASIFICADA devuelve categoría, prioridad y sugerencia; en SIN_CLASIFICACION devuelve categoría/prioridad nulas y motivo (texto insuficiente, ambiguo o fuera de catálogo). No se fuerza una categoría ni se inventa una sexta categoría «Otro». SIN_CLASIFICACION es un resultado de la respuesta, no un nuevo estado de caso ni de cola: ai_status=COMPLETADA con resultado inconcluso y validación humana pendiente. El gestor solicita aclaración o clasifica manualmente dentro del catálogo; no avanza a revisión sin clasificación oficial válida. Validar contra catálogo y esquema; rechazar instrucciones incrustadas como órdenes de sistema. No ejecuta acciones, correos ni decisiones disciplinarias. Guardar la primera respuesta válida y la versión del texto enviado, modelo y versión de prompt, sin claves.

Hasta tres intentos ante fallos transitorios; si falla, marcar FALLIDA y permitir clasificación manual. Respuesta tardía nunca cambia decisión humana. PENDIENTE, COMPLETADA, FALLIDA y OMITIDA describen el trabajo IA, no el estado del caso.

**Aceptación:** salida SIN_CLASIFICACION válida no fuerza categoría y conduce a revisión manual; UI muestra sugerencia y decisión por separado; validación explícita actualiza bandera/actor/fecha; caso confidencial no inicia una llamada; una falla no impide atención manual; auditoría conserva correcciones.

### RF-4 Asignación y ciclo

Gestores solo asignan a usuarios activos autorizados y no involucrados. Cumplir matriz de transiciones; no basta ser responsable para acceder. Registrar cada ciclo y evitar actualizaciones concurrentes que omitan validación o acceso.

**Aceptación:** rechazar saltos, responsable sin acceso y resolución sin revalidación; reapertura conserva historia; protección por confidencialidad nunca deja un supervisor como responsable de un caso restringido.

### RF-5 Correo por eventos

Eventos: creación hacia RH elegible sin asignado; asignación/reasignación al nuevo responsable; resolución al reportante y afectado si pueden consultar; reapertura al responsable. Verificar acceso e independencia justo antes de enviar; deduplicar destinatarios/eventos. Sin destinatario autorizado, registrar omisión. Un caso confidencial nunca notifica al reportante o afectado sin permiso.

Asunto con ID de caso y cuerpo con enlace; sin nombres, descripción o resolución. En desarrollo usar SMTP de pruebas con buzón capturador, sin correo real. Configuración por variables; servicio concreto configurable. Correos asíncronos, hasta tres reintentos transitorios; fallo final visible a RH autorizado. No bloquea creación.

**Aceptación:** comprobar eventos, exclusiones por acceso, deduplicación, reintentos y fallo sin revertir el caso. No se prometen alertas por vencimiento ni SLA.

### RF-6 Analítica agregada

Power BI Desktop de uso Admin RH y Gerencia. Solo importar vistas previamente agregadas y filtradas con cuenta de lectura; nunca expedientes individuales ni filas luego ocultas solo en el visual. Excluir completamente del conjunto exportable los casos confidenciales y con conflicto de interés activo o revisión de participantes pendiente. No exportar nombres, emails, textos o resoluciones. Las métricas siguientes corresponden solo a la población exportable y deben etiquetarse así; no representan el total de la empresa.

Publicación por combinación fija de mes de creación, categoría y departamento histórico. Una celda solo se publica con al menos cinco incidencias distintas; si contiene casos personales, también exige cinco afectados distintos. Un caso de ENTORNO sin víctima no cuenta como afectado personal. Si no cumple, mostrar «Suprimido por privacidad», nunca 0 ni el valor real. Promedios, porcentajes y numeradores/denominadores tienen la misma regla sobre sus respectivos casos contribuyentes, no solo sobre la celda de volumen.

La supresión debe ocurrir en la vista de exportación, no mediante formato visual. Aplicar supresión complementaria: no publicar totales/subtotales que permitan reconstruir una celda suprimida por resta. Ante duda se omite el total/subtotal completo. No habilitar drill-through, filas de detalle, dimensiones o filtros que formen grupos más pequeños que los exportados, ni varias granularidades superpuestas que permitan restar resultados. Los cálculos se obtienen de los mismos conjuntos autorizados, sin completar valores suprimidos con información operacional.

Actualización manual y fecha de corte visible. Antes de compartir una nueva versión, volver a verificar confidencialidad y retirar de la nueva extracción los casos que perdieron elegibilidad; regenerar el archivo sin caché de versiones anteriores. Una copia previamente entregada no se puede revocar automáticamente: su distribución queda limitada a destinatarios autorizados y se documenta como riesgo residual. Estas reglas reducen reidentificación; no garantizan anonimato de datos reales y el MVP sigue usando datos simulados.

- **Volumen:** contar IDs únicos por fecha de creación y dimensiones.

- **Resolución del último ciclo:** promedio en horas de resolved_at − cycle_start_at para casos cuyo último ciclo esté resuelto/cerrado; excluir ciclos abiertos. Consultas históricas usan ciclos archivados.

- **Reapertura:** población = casos con al menos una resolución en el periodo; numerador = IDs de esa población reabiertos después de la primera resolución del periodo hasta fecha de corte; cada ID una vez. Denominador cero: «Sin datos».

- **Concordancia operativa:** coincidencia de categoría sugerida y humana en casos con ambas; excluir IA omitida/fallida y contarlas aparte. No equivale a precisión contra referencia.

**Aceptación:** fórmulas con conjuntos conocidos, ciclos múltiples y población vacía; excluir confidenciales; suprimir celdas de 1–4 casos y promedios con pocos contribuyentes; suprimir también cinco casos del mismo afectado; comprobar que totales/filtros no reconstruyen valores; el .pbix no importa filas ni valores suprimidos. Modelo sin datos prohibidos. No sustituye al panel de expedientes React.

### RF-7 Administración de usuarios y departamentos

Admin RH crea cuentas y asigna roles/departamentos mediante API protegida y pantalla de administración React; se requieren ambas para aceptar RF-7. Los comandos de bootstrap/restablecimiento siguen reservados al operador y no sustituyen esa pantalla. No hay registro público ni contraseña común de seed. Registrar altas, cambios, bajas y restablecimientos sin guardar contraseñas en auditoría. Cambiar rol/departamento o desactivar exige revisar casos asignados y reasignar si se pierde acceso. Revocar sesiones al cambiar privilegios o credencial. Impedir dejar el sistema sin Admin RH activo con acceso local.

Bootstrap y recuperación por operador quedan separados de las operaciones de RH. Debe existir además un procedimiento auditado para provisionar un administrador independiente adicional cuando no haya gestor elegible; es una operación del operador que no concede acceso al caso al involucrado. Esta operación todavía no existe en el CLI actual y debe implementarse antes de aceptar la regla de escalamiento. Las cuentas DEMO no pueden iniciar sesión hasta asignarles contraseña explícitamente. Usuarios externos futuros solo por vinculación verificada, sin unificación automática por email.

**Aceptación:** empleado/supervisor reciben 403 en administración; duplicado de correo recibe conflicto; baja impide acceso; cambio no deja casos sin responsable indebidamente y queda auditado. La gestión completa aún debe implementarse.

### RF-8 Panel operativo React

Pantallas: login, listado de casos, registro, detalle con historial y validación, administración RH. Listado paginado (20 por defecto, máximo 100), orden por creación descendente y filtros por estado, prioridad, categoría, responsable y rango de creación. Búsqueda por ID y título dentro del conjunto autorizado; no búsqueda libre de textos confidenciales fuera del expediente.

Detalle: información, participantes según acceso, responsable, sugerencia IA cuando exista, decisión oficial, vigencia, resolución e historial. Botones según estado/rol, sin sustituir controles API. Estados de carga, vacío, error, IA omitida/fallida y sesión expirada. Bandeja RH sin responsable y contadores operativos respetan las mismas restricciones.

**Aceptación:** datos ajenos no aparecen en filas, conteos, búsquedas o filtros; paginación consistente; deep link sin autorización rechazado; logout elimina token de memoria y vuelve a login. El token no se guarda en URL ni almacenamiento persistente del navegador.

## 5. Arquitectura y tecnologías

| Componente | Tecnología y responsabilidad |
| --- | --- |
| Cliente | React; panel y consumo de API |
| API | Python/FastAPI; autorización y transacciones |
| Persistencia | PostgreSQL, SQLAlchemy, Psycopg; Alembic para migraciones |
| Identidad | Argon2id y sesiones en PostgreSQL |
| Trabajo asíncrono | Redis y worker para IA/correo; librería de tareas por decidir antes de implementar |
| Clasificación | API directa OpenAI con LangChain; modelo por evaluar |
| Correo | SMTP configurable; capturador de pruebas en desarrollo |
| Analítica | Power BI Desktop y vistas agregadas |
| Ejecución | Docker Compose local y GitHub Actions para verificaciones |

Redis no almacena las sesiones de autenticación actuales. No se presenta la configuración de CI como despliegue continuo ya implementado. APIs de negocio, worker y frontend se implementan por hitos del backlog.

## 6. Modelo de datos objetivo

Los nombres técnicos existentes se conservan para no renombrar columnas sin necesidad. Nombres de interfaz en español. UUID para entidades operativas; catálogos con ID entero; fechas operativas UTC con zona horaria.

| Entidad | Campos y reglas |
| --- | --- |
| roles | id, nombre: ADMIN_RH, SUPERVISOR, EMPLEADO |
| departamentos | id, nombre único, is_active |
| users | id estable, email único sin mayúsculas, nombre_completo, departamento_id, rol_id, is_active; tenant_id/external_id opcionales y emparejados, reservados para identidad futura |
| local_credentials | user_id, password_hash Argon2id, updated_at |
| auth_sessions | token_hash, user_id, created_at, expires_at, revoked_at |
| login_throttle | email normalizado, failures, locked_until |
| categorias_incidencia | id, nombre, descripcion; cinco categorías |
| incidencias | id, titulo, descripcion, incident_date, scope, reported_department_id, department_id_at_creation, created_by, affected_employee_id nullable según scope, assigned_to nullable en PENDIENTE, status, priority nullable inicialmente, category_id nullable inicialmente, classification_valid, validated_by, validated_at, is_confidential, ai_status, ai_input_text, ai_input_reviewed_by/at, ai_suggestion, ai_error, ai_skip_reason, ai_model, ai_prompt_version, resolution_text, cycle_start_at, resolved_at, closed_at, reopening_reason, created_at, updated_at |
| incident_involved_users | incidencia_id, user_id; pareja única; review_status (DECLARADO, CONFIRMADO, DESCARTADO), declaration_reason, reviewed_by/at, review_reason; conservar declaración y revisiones en auditoría |
| historial_incidencias | id, incidencia_id nullable, affected_user_id nullable, usuario_id nullable para sistema, accion, detalle JSONB con valores anteriores/nuevos, fecha; exigir al menos un destino |

Acciones de auditoría: CREADO, ESTADO_CAMBIADO, ASIGNADO, REAPERTURA, VALIDACION_IA, CAMBIO_CONFIDENCIALIDAD, CONTENIDO_EDITADO, USUARIO_ACTUALIZADO. Los detalles distinguen operaciones específicas y ciclos; no contienen contraseñas, tokens o claves. USUARIO_ACTUALIZADO usa affected_user_id sin forzar incidencia_id. El nombre usuario_id significa actor, no siempre el usuario modificado.

La historia de ciclos se conserva completa en eventos de transición con inicio y fechas finales. Historial inmutable mediante servicios y privilegios de aplicación separados de migración antes de entrega externa.

**Estado de implementación del modelo:** las revisiones 0001 y 0002 no se reescriben. La 0003 implementa estructura de ámbito, afectado condicional, departamento reportado, participantes/revisión, classification_valid y control IA. Su aplicación real en PostgreSQL y los servicios de autorización, recusa, validación e IA siguen pendientes. La estructura no certifica RF-2/RF-3/RF-4 completos. Detalle de conservación y validación en DATOS.md.

## 7. Seguridad y datos

### 7.1 Uso permitido y minimización

Solo datos simulados en el MVP académico y pruebas. No introducir expedientes reales, información médica ni identificadores reales en la IA. Casos confidenciales o con conflicto de interés: clasificación manual, sin envío externo. Credenciales solo en .env local excluido de Git; variables de ejemplo sin secretos. No registrar tokens, contraseñas ni cuerpos de login en logs/capturas.

La revisión del texto antes de IA no garantiza anonimización de datos reales. La revisión previa a producción debe identificar expresamente el marco jurídico aplicable al responsable y al tratamiento concretos; no se presume cumplimiento ni se fija una ley por simple inferencia de ubicación. El uso real queda bloqueado hasta definir base de tratamiento, información a las personas, responsables, proveedores, conservación y medidas aplicables con los responsables de la organización. Este PRD no acredita cumplimiento legal ni fija una retención obligatoria para expedientes reales.

### 7.2 Conservación y acceso operativo

Datos de demostración: conservar hasta cierre de la evaluación académica y hasta 30 días después; luego el operador elimina la base de demostración o la sustituye por un conjunto limpio mediante procedimiento documentado. No es eliminación desde la aplicación. Si la institución exige otro plazo para evidencia académica, registrar el ajuste antes de esa limpieza. Capturas del repositorio solo con datos simulados; no incluir bases ni respaldos en Git.

Sesiones expiradas/revocadas e intentos antiguos: planificar limpieza técnica tras 30 días, preservando únicamente eventos necesarios sin secretos. Hasta implementar limpieza no afirmar que se ejecuta automáticamente. Respaldos de pruebas con el mismo plazo y acceso restringido al operador. Retención productiva y ejercicio de derechos quedan como condición previa al uso real, no como funcionalidad terminada.

## 8. Requisitos no funcionales

- **RNF-1 Seguridad:** HTTPS para acceso externo; HTTP solo en loopback local. Validar sesión y autorización por objeto en cada solicitud protegida. Sin secretos en logs, respuestas o repositorio. Limitación global de tráfico y revisión de privilegios antes de exposición pública; bloqueo por cuenta ya definido en RF-1.

- **RNF-2 Rendimiento:** p95 de operaciones simples de lectura/creación/actualización inferior a 200 ms, con 10 usuarios simultáneos en Docker local, 100 incidencias simuladas y prueba sostenida de 5 minutos tras calentamiento. Excluir duración de servicios externos; incluir encolado en creación. Registrar hardware, errores y resultados. No se acredita hasta medir.

- **RNF-3 Reproducibilidad:** arranque documentado, migraciones desde base vacía y actualización sin pérdida de datos, dependencias fijadas, .env.example, Docker y CI. Declarar resultados locales y remotos por separado.

- **RNF-4 Trazabilidad:** cambios de negocio y evento de auditoría en misma transacción. Rechazo sin efectos parciales. Copias previas de descripción, clasificación y ciclos recuperables por usuarios autorizados.

- **RNF-5 Operación:** manuales de instalación/uso, plan de soporte y recuperación probado con datos simulados antes de entrega. No se presupone alta disponibilidad ni escalabilidad por usar Docker.

## 9. Evaluación y aceptación

### 9.1 IA

Conjunto inicial de evaluación: 50 casos simulados, 10 por categoría; al menos 10 de prioridad Alta, 10 Media y 10 Baja. Etiquetas de referencia y justificación fijadas antes de ejecutar; casos distintos de ejemplos de prompt. Registrar modelo, prompt, fecha, respuestas válidas/fallidas y matriz de confusión por categoría y prioridad.

Metas de ingeniería iniciales, no garantías estadísticas: al menos 45/50 categorías correctas y 40/50 prioridades correctas. Revisión obligatoria de todos los falsos negativos de prioridad Alta; cualquier Alta etiquetada que salga Baja debe corregirse y reevaluarse antes de aceptar la sugerencia de prioridad. SIN_CLASIFICACION o respuesta fallida en un caso etiquetado dentro del catálogo cuenta como no acierto; no se excluye del denominador para mejorar métricas. Agregar además cinco casos ambiguos/fuera de catálogo como prueba separada de abstención: deben conducir a atención manual sin categoría forzada. No se ajusta la referencia para mejorar la puntuación. Si se usa el conjunto para ajustar el prompt, se prepara otro conjunto independiente antes de la aceptación final.

El conjunto de 20 casos se propuso en versiones anteriores, pero no se ejecutó ni se presenta como evidencia histórica. Se sustituye por la evaluación prevista de 50 casos. Si no se cumplen metas, la gestión manual sigue operativa, pero RF-3 no se marca aceptado. Evaluar también omisión de confidenciales, JSON inválido, cola fallida, duplicación y respuesta tardía.

### 9.2 Flujos y pruebas

Validar autenticación, roles, IDOR, departamentos, riesgos sin víctima, conflictos sobre Supervisor y Admin RH, falta de gestor independiente, cambio de participantes, confidencialidad y notificaciones. Probar edición con clasificación inválida, revalidación, transiciones, reaperturas múltiples, concurrencia y rollback. Diez incidencias simuladas de demostración se crean mediante el servicio auditado; los fixtures no eluden reglas.

Cada RF requiere evidencia en REPORTE_QA.md y trazabilidad al código/prueba. No marcar aprobado por existencia de pantalla o captura de ejemplo. Aceptación global: RF-1 a RF-8 implementados y verificados, sin fallos pendientes de acceso o pérdida de datos, instalación reproducible y documentos académicos completos.

## 10. Plan de entrega

El cronograma de seis semanas anterior se reemplaza por una secuencia priorizada de hitos. No hay todavía estimaciones de esfuerzo ni calendario comprometido. No se ha comunicado una fecha límite definitiva ni disponibilidad semanal; no se inventan fechas de término. Fecha de arranque documentada: 15 de octubre de 2026. Antes de comprometer calendario, registrar fecha límite y horas disponibles en BACKLOG.md.

| Orden | Hito del backlog | Entregables académicos relacionados |
| --- | --- | --- |
| 1 | Requisitos y propuesta | Detección de necesidades, propuesta técnica |
| 2 | Arquitectura, estructura y entorno | Documento de arquitectura, plan del proyecto |
| 3 | Esquema, migraciones y datos simulados | Desarrollo y evidencia técnica |
| 4 | Autenticación, usuarios y permisos | Desarrollo y QA de acceso |
| 5 | Registro, consultas y panel React | Desarrollo funcional |
| 6 | Ciclo, confidencialidad y auditoría | Desarrollo y QA funcional |
| 7 | IA asíncrona y evaluación | Desarrollo y reporte IA |
| 8 | Correo por eventos | Integración y reporte QA |
| 9 | Analítica y reportes | Reporte Power BI y validación |
| 10 | QA integral y entrega | Manuales, mantenimiento, capacitación real e informe final |

Prioridad núcleo: hitos 1–6 y pruebas/documentación del hito 10 necesarias para demostrar el flujo manual completo. Prioridad de integración posterior: hitos 7–9 (IA, correo y Power BI). Los tres siguen siendo entregables del proyecto y no pueden omitirse de la aceptación final sin un cambio explícito de alcance; la prioridad solo ordena el desarrollo. La versión manual puede demostrarse como avance parcial, no como MVP completo aceptado.

Los hitos de código no equivalen uno a uno a las diez actividades académicas: documentación se mantiene en todos; mantenimiento, capacitación y cierre se concretan al entregar. Estado real en BACKLOG.md. No se inventan entrevistas, capacitaciones, firmas ni evaluaciones.

## 11. Supuestos dependencias y riesgos

| Tipo | Condición | Tratamiento |
| --- | --- | --- |
| Dependencia | Docker y terminal autorizada para el motor | Algunos comandos los ejecuta la autora; conservar evidencia |
| Dependencia | API OpenAI, modelo y crédito disponible | Seleccionar modelo antes de RF-3; modo manual ante falla |
| Dependencia | SMTP de pruebas y Power BI Desktop | Preparar antes de RF-5/RF-6 |
| Supuesto | Datos simulados y responsables independientes disponibles | Si falta gestor elegible, caso restringido pendiente |
| Riesgo | Alcance excesivo para una desarrolladora | Priorizar flujo completo manual, luego IA/correo/analítica; no ocultar funciones pendientes |
| Riesgo | Texto sensible enviado fuera | Solo texto simulado revisado; confidenciales omitidos; sin uso real hasta revisar tratamiento |
| Riesgo | Deriva entre PRD, código y Word | PRD.md fuente única; trazabilidad distingue objetivo/implementado |
| Riesgo | Conflicto o abuso de privilegios | Exclusión por involucrados, auditoría y revisión de roles |
| Riesgo | Declaración errónea o abusiva sobre el único gestor | Protección preventiva por caso y revisión independiente; puede retrasar atención, no desactiva cuentas |
| Riesgo | Reportante o gestor afectado sin seguimiento confidencial | Acuse de recepción; comunicar limitación, sin resultados a quien no tiene acceso |
| Riesgo | Reidentificación por agregados pequeños o exportaciones previas | Excluir confidenciales; supresión primaria/complementaria; limitar distribución, sin prometer revocación de copias |
| Riesgo | Reportes de testigos fuera del alcance | Indicar exclusión antes de registro; no inventar canal alternativo |
| Riesgo | Presupuesto/calendario aún no fijados | No prometer fecha o costo; registrar antes de comprometer entrega |

Entra ID no es dependencia ni bloqueo activo. Una integración futura implica un cambio de alcance y vinculación verificada.

## 12. Glosario y cambios

- **Reportante:** created_by; quien registra.

- **Afectado:** affected_employee_id; persona sobre quien versa el caso personal.

- **Involucrado:** afectado o participante con relación DECLARADA/CONFIRMADA; determina exclusión preventiva del gestor. DESCARTADO conserva auditoría sin activar por sí solo esa exclusión.

- **Responsable:** assigned_to; usuario que atiende con autorización vigente.

- **Clasificación vigente:** bandera verdadera tras confirmación humana sobre el contenido actual.

- **Confidencial:** acceso solo a Admin RH independiente.

- **Ciclo:** periodo de revisión hasta resolución; una reapertura inicia otro.

- **Sesión opaca:** token aleatorio revocable; no JWT ni identidad Microsoft.

La versión 1.9 precisa revisión independiente de participantes, supresión de agregados, consecuencias de confidencialidad, exclusión de reportes de testigos, prioridades de entrega, administración por API/pantalla y abstención IA. Corrige la referencia errónea a pruebas históricas no ejecutadas. No cambia código ni aplica migraciones. Las diferencias funcionales necesitan implementación y pruebas posteriores, registradas en BACKLOG.md.

### Estado técnico de la entrega 0.5.0

Registro y consultas backend de RF-2/RF-8 implementados parcialmente, con auditoría y acceso; sin edición ni ciclo completo. Campo participants limita a 20 entradas por petición como control técnico contra incorporación masiva. El empleado consulta cronología, sin detalles históricos que incluyan terceros; participantes detallados solo para gestores autorizados. No equivale a aceptación final; ver INCIDENCIAS.md y TRAZABILIDAD.md.

Actualización de implementación, 16 de octubre de 2026 (API 0.7.0): los servicios ya incorporan alta/revisión de participantes, cambios de confidencialidad y reasignación/retroceso protector auditados. Sustituye menciones anteriores a estos servicios como pendientes. Continúan pendientes provisión adicional de administrador independiente por operador, revisión de asignaciones al cambiar usuarios/roles/departamentos, concurrencia PostgreSQL y UI. La estructura y servicios parciales no certifican RF completos; ejecución manual de 0.7.0 aún pendiente.

Actualización técnica preparada el 16 de octubre de 2026: procedimiento de operador para RH adicional implementado y probado en copia aislada; aún no aplicado al repositorio. Conserva exclusión del involucrado y no cambia casos automáticamente. La designación de otra persona es responsabilidad del operador; el sistema no detecta que una misma persona controle dos cuentas. RF-7 sigue parcial, no hay administración React completa. Guía ADMIN_INDEPENDIENTE.md.

Estado posterior al paquete: procedimiento de RH adicional aplicado/ejecutado según la autora y sesión independiente verificada con evidencia 34. Recorrido de acceso 35–37 documentado con sus límites en REVISION_RH_INDEPENDIENTE.md. No implica RF-7 completo ni demostración técnica de independencia humana entre cuentas.

Estado preparado para 0.8.0: backend de modificaciones de usuario con revocación y revisión de asignaciones implementado en copia; no aplicado todavía. RF-7 parcial, frontend y CRUD de departamentos pendientes. Política de casos finalizados y restricciones detallada en ADMIN_USUARIOS.md.

Estado posterior de administración 0.8.0, 16 de octubre de 2026: implementación aplicada según la autora, suite completa de 77 pruebas aprobadas y tres integraciones PostgreSQL omitidas. Evidencias manuales y limitaciones en REVISION_ADMIN_USUARIOS.md. Actualiza el estado previo de paquete preparado, sin declarar RF-7 completo ni UI entregada.

Estado frontend al 17 de octubre de 2026: primera UI React de login, listado/filtros y detalle/historial de lectura implementada y compilada; sustituye referencias históricas a frontend inexistente. RF-8 parcial: registro/gestión/administración UI y enlaces profundos pendientes. Pruebas/validación manual distinguidas en FRONTEND.md y REPORTE_QA.md.

Estado de UI al 17 de octubre de 2026: React 0.2.0 incorpora alta persona/entorno, participantes y acuse mínimo con acceso confirmado por API. Sustituye el pendiente histórico de formulario de registro; edición/validación/asignación/transiciones y administración UI siguen pendientes. 15 pruebas simuladas aprobadas; alta real desde UI todavía pendiente. RF-2/RF-8 parciales, límites en FRONTEND.md.
