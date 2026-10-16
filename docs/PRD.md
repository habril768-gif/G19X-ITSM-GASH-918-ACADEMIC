# PRD PluriOne 1.8

Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V.

| Dato | Valor |
| --- | --- |
| Clave | G19X-ITSM-GASH-918-ACADEMIC |
| Autora | Gilian Abril Sánchez Hernández |
| Fecha de consolidación | 15 de octubre de 2026 |
| Versión | 1.8 — base de desarrollo |
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

Un empleado reporta un conflicto que le afecta seleccionándose como afectado y declarando a otros participantes; no registra una incidencia personal exclusivamente sobre un tercero. Los hechos sobre terceros que no le afectan se canalizan a RH, fuera del formulario personal. Un riesgo físico sin víctima se registra como ENTORNO; no se inventa un empleado afectado.

El departamento reportado de PERSONA se obtiene del afectado al registrar. `department_id_at_creation` es la copia inmutable de ese departamento; en ENTORNO es copia del departamento reportado. Sirve para analítica histórica. La visibilidad personal utiliza el departamento actual del afectado; la de ENTORNO, el departamento reportado. Los cambios de departamento requieren revisar asignaciones que pierdan autorización.

Los participantes declarados se guardan por ID en una relación aparte; el afectado cuenta siempre como involucrado. El reportante no cuenta como involucrado por el solo hecho de registrar. Los participantes se declaran dentro del ámbito autorizado; RH puede completarlos con auditoría. Las restricciones se recalculan cuando cambian participantes o roles.

### 3.3 Confidencialidad y conflicto de interés

Cualquier rol puede solicitar confidencialidad al crear. Mientras sea confidencial, el reportante pierde acceso; el formulario lo explica antes de guardar.

Un caso que involucre a un Supervisor o Admin RH pasa automáticamente a confidencial y exige atención por un Admin RH no involucrado. Una persona involucrada con privilegios de gestión no puede consultar, asignar, clasificar, resolver, cerrar, reabrir ni modificar restricciones de su caso. No basta ocultar el botón. No se excluye a un empleado de sus casos personales no confidenciales por ser el afectado.

Si no hay Admin RH activo e independiente, el caso queda PENDIENTE y restringido, sin responsable, hasta disponer de uno. El operador podrá provisionar una cuenta independiente mediante el procedimiento administrativo, sin otorgar acceso al involucrado ni autoasignar el caso. No se garantiza resolución mientras falte ese responsable.

Solo Admin RH no involucrado puede cambiar confidencialidad de un caso existente. En EN_REVISION, pasar a confidencial exige reasignar atómicamente a un Admin RH activo e independiente; si no existe, se devuelve a PENDIENTE, conserva historial y queda sin responsable. Este retroceso solo se admite para protección de acceso, con motivo obligatorio. En RESUELTA/CERRADA se exige reapertura antes del cambio.

Retirar confidencialidad exige motivo y no puede hacerse mientras siga involucrado un Supervisor/Admin RH. La corrección de participantes también exige motivo y auditoría; nunca puede realizarla el involucrado. El acceso no se restaura por haber empezado RH a atender el caso, sino por cambiar válidamente la restricción.

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

La IA devuelve categoría, prioridad y sugerencia estructuradas. Validar contra catálogo y esquema; rechazar instrucciones incrustadas como órdenes de sistema. No ejecuta acciones, correos ni decisiones disciplinarias. Guardar la primera respuesta válida y la versión del texto enviado, modelo y versión de prompt, sin claves.

Hasta tres intentos ante fallos transitorios; si falla, marcar FALLIDA y permitir clasificación manual. Respuesta tardía nunca cambia decisión humana. PENDIENTE, COMPLETADA, FALLIDA y OMITIDA describen el trabajo IA, no el estado del caso.

**Aceptación:** UI muestra sugerencia y decisión por separado; validación explícita actualiza bandera/actor/fecha; caso confidencial no inicia una llamada; una falla no impide atención manual; auditoría conserva correcciones.

### RF-4 Asignación y ciclo

Gestores solo asignan a usuarios activos autorizados y no involucrados. Cumplir matriz de transiciones; no basta ser responsable para acceder. Registrar cada ciclo y evitar actualizaciones concurrentes que omitan validación o acceso.

**Aceptación:** rechazar saltos, responsable sin acceso y resolución sin revalidación; reapertura conserva historia; protección por confidencialidad nunca deja un supervisor como responsable de un caso restringido.

### RF-5 Correo por eventos

Eventos: creación hacia RH elegible sin asignado; asignación/reasignación al nuevo responsable; resolución al reportante y afectado si pueden consultar; reapertura al responsable. Verificar acceso e independencia justo antes de enviar; deduplicar destinatarios/eventos. Sin destinatario autorizado, registrar omisión. Un caso confidencial nunca notifica al reportante o afectado sin permiso.

Asunto con ID de caso y cuerpo con enlace; sin nombres, descripción o resolución. En desarrollo usar SMTP de pruebas con buzón capturador, sin correo real. Configuración por variables; servicio concreto configurable. Correos asíncronos, hasta tres reintentos transitorios; fallo final visible a RH autorizado. No bloquea creación.

**Aceptación:** comprobar eventos, exclusiones por acceso, deduplicación, reintentos y fallo sin revertir el caso. No se prometen alertas por vencimiento ni SLA.

### RF-6 Analítica agregada

Power BI Desktop de uso Admin RH y Gerencia. Importación solo desde vistas agregadas con cuenta de lectura; sin registros individuales, nombres, emails, texto de casos o resoluciones. Agrupar por mes, categoría y departamento histórico. Actualización manual con fecha de corte visible. Casos confidenciales solo contribuyen a agregados sin texto ni identificadores; no usar filtros que revelen expedientes individuales.

- **Volumen:** contar IDs únicos por fecha de creación y dimensiones.
- **Resolución del último ciclo:** promedio en horas de resolved_at − cycle_start_at para casos cuyo último ciclo esté resuelto/cerrado; excluir ciclos abiertos. Consultas históricas usan ciclos archivados.
- **Reapertura:** población = casos con al menos una resolución en el periodo; numerador = IDs de esa población reabiertos después de la primera resolución del periodo hasta fecha de corte; cada ID una vez. Denominador cero: «Sin datos».
- **Concordancia operativa:** coincidencia de categoría sugerida y humana en casos con ambas; excluir IA omitida/fallida y contarlas aparte. No equivale a precisión contra referencia.

**Aceptación:** fórmulas con conjuntos conocidos, ciclos múltiples y población vacía; modelo Power BI sin datos prohibidos. No sustituye al panel de expedientes React.

### RF-7 Administración de usuarios y departamentos

Admin RH crea cuentas y asigna roles/departamentos. No hay registro público ni contraseña común de seed. Registrar altas, cambios, bajas y restablecimientos sin guardar contraseñas en auditoría. Cambiar rol/departamento o desactivar exige revisar casos asignados y reasignar si se pierde acceso. Revocar sesiones al cambiar privilegios o credencial. Impedir dejar el sistema sin Admin RH activo con acceso local.

Bootstrap y recuperación por operador quedan separados de las operaciones de RH. Las cuentas DEMO no pueden iniciar sesión hasta asignarles contraseña explícitamente. Usuarios externos futuros solo por vinculación verificada, sin unificación automática por email.

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
| incident_involved_users | incidencia_id, user_id; pareja única; participantes declarados para conflicto de interés |
| historial_incidencias | id, incidencia_id nullable, affected_user_id nullable, usuario_id nullable para sistema, accion, detalle JSONB con valores anteriores/nuevos, fecha; exigir al menos un destino |

Acciones de auditoría: CREADO, ESTADO_CAMBIADO, ASIGNADO, REAPERTURA, VALIDACION_IA, CAMBIO_CONFIDENCIALIDAD, CONTENIDO_EDITADO, USUARIO_ACTUALIZADO. Los detalles distinguen operaciones específicas y ciclos; no contienen contraseñas, tokens o claves. USUARIO_ACTUALIZADO usa affected_user_id sin forzar incidencia_id. El nombre usuario_id significa actor, no siempre el usuario modificado.

La historia de ciclos se conserva completa en eventos de transición con inicio y fechas finales. Historial inmutable mediante servicios y privilegios de aplicación separados de migración antes de entrega externa.

**Diferencia con el código actual:** 0001 y 0002 no se reescriben. scope, reported_department_id, participantes, classification_valid y campos adicionales de control IA todavía requieren una migración futura y servicios. El esquema actual exige afectado y no permite OMITIDA; no debe afirmarse que ya soporta este modelo objetivo. La migración deberá rellenar casos existentes como PERSONA y obtener su departamento histórico, sin pérdida de datos.

## 7. Seguridad y datos

### 7.1 Uso permitido y minimización

Solo datos simulados en el MVP académico y pruebas. No introducir expedientes reales, información médica ni identificadores reales en la IA. Casos confidenciales o con conflicto de interés: clasificación manual, sin envío externo. Credenciales solo en .env local excluido de Git; variables de ejemplo sin secretos. No registrar tokens, contraseñas ni cuerpos de login en logs/capturas.

La revisión del texto antes de IA no garantiza anonimización de datos reales. El uso real queda bloqueado hasta definir base de tratamiento, información a las personas, responsables, proveedores, conservación y medidas aplicables con los responsables de la organización. Este PRD no acredita cumplimiento legal ni fija una retención obligatoria para expedientes reales.

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

Metas de ingeniería iniciales, no garantías estadísticas: al menos 45/50 categorías correctas y 40/50 prioridades correctas. Revisión obligatoria de todos los falsos negativos de prioridad Alta; cualquier Alta etiquetada que salga Baja debe corregirse y reevaluarse antes de aceptar la sugerencia de prioridad. No se ajusta la referencia para mejorar la puntuación. Si se usa el conjunto para ajustar el prompt, se prepara otro conjunto independiente antes de la aceptación final.

Los 20 casos anteriores quedan como smoke test histórico, sin sustituir esta evaluación. Si no se cumplen metas, la gestión manual sigue operativa, pero RF-3 no se marca aceptado. Evaluar también omisión de confidenciales, JSON inválido, cola fallida, duplicación y respuesta tardía.

### 9.2 Flujos y pruebas

Validar autenticación, roles, IDOR, departamentos, riesgos sin víctima, conflictos sobre Supervisor y Admin RH, falta de gestor independiente, cambio de participantes, confidencialidad y notificaciones. Probar edición con clasificación inválida, revalidación, transiciones, reaperturas múltiples, concurrencia y rollback. Diez incidencias simuladas de demostración se crean mediante el servicio auditado; los fixtures no eluden reglas.

Cada RF requiere evidencia en REPORTE_QA.md y trazabilidad al código/prueba. No marcar aprobado por existencia de pantalla o captura de ejemplo. Aceptación global: RF-1 a RF-8 implementados y verificados, sin fallos pendientes de acceso o pérdida de datos, instalación reproducible y documentos académicos completos.

## 10. Plan de entrega

El cronograma de seis semanas anterior se reemplaza por secuencia de hitos con estimación revisable de esfuerzo. No se ha comunicado una fecha límite definitiva ni disponibilidad semanal; no se inventan fechas de término. Fecha de arranque documentada: 15 de octubre de 2026. Antes de comprometer calendario, registrar fecha límite y horas disponibles en BACKLOG.md.

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
| Riesgo | Presupuesto/calendario aún no fijados | No prometer fecha o costo; registrar antes de comprometer entrega |

Entra ID no es dependencia ni bloqueo activo. Una integración futura implica un cambio de alcance y vinculación verificada.

## 12. Glosario y cambios

- **Reportante:** created_by; quien registra.
- **Afectado:** affected_employee_id; persona sobre quien versa el caso personal.
- **Involucrado:** afectado o participante declarado; determina conflictos de interés de gestores.
- **Responsable:** assigned_to; usuario que atiende con autorización vigente.
- **Clasificación vigente:** bandera verdadera tras confirmación humana sobre el contenido actual.
- **Confidencial:** acceso solo a Admin RH independiente.
- **Ciclo:** periodo de revisión hasta resolución; una reapertura inicia otro.
- **Sesión opaca:** token aleatorio revocable; no JWT ni identidad Microsoft.

La versión 1.8 consolida organización, roles, revalidación, riesgos de entorno, conflictos de interés, datos para IA, alcance de correos, RF-7/RF-8, modelo objetivo, evaluación y dependencias. No cambia código ni aplica migraciones. Las diferencias funcionales necesitan implementación y pruebas posteriores, registradas en BACKLOG.md.
