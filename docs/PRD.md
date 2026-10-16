# PRD PluriOne 1.6

Base de desarrollo elegida por la autora. No requiere aprobación de terceros para iniciar el proyecto. La copia Word conserva el documento recibido; esta versión Markdown elimina las condiciones de aprobación que ya no aplican.

PRODUCT REQUIREMENTS DOCUMENT (PRD)

Plataforma Inteligente de Gestión de Incidencias Laborales

Documento de requisitos del producto

| Empresa | PluriOne S.A. de C.V. (Develop Talent & Technology) |
| --- | --- |
| Versión | 1.6  |
| Fecha | 15 de octubre de 2026 |
| Autora | Gilian Abril Sánchez Hernández |

1. Visión del Producto

Desarrollar una plataforma HRTech para PluriOne S.A. de C.V. que automatice la gestión de incidencias laborales mediante Inteligencia Artificial (OpenAI + LangChain), garantizando la confidencialidad desde el origen, trazabilidad humana y eficiencia operativa.

2. Alcance del Proyecto (MVP)

| In-Scope (Fase 1) | Out-of-Scope (Fase 2+) |
| --- | --- |
| Registro y seguimiento de incidencias laborales. | Integración nativa con Nómina. |
| Clasificación automática por IA (Categoría/Prioridad). | App móvil nativa (iOS/Android). |
| Notificaciones automatizadas de alertas. | Chatbots para empleados finales. |
| Panel administrativo y analítica (Power BI). | Gestión de nómina o pagos. |
| Autenticación con Microsoft Entra ID. | Eliminación física y lógica de incidencias. |

3. Stack Tecnológico

Frontend: React.js (Interfaz de usuario y dashboards).

Backend: Python con FastAPI (API REST y lógica de negocio).

Inteligencia Artificial: LangChain + OpenAI API (Clasificación de texto y sugerencias).

Base de Datos: PostgreSQL (Almacenamiento de incidencias, usuarios e historial).

Cache/Colas: Redis (Cola asíncrona para clasificación IA y caché de sesiones).

Seguridad: Microsoft Entra ID (Autenticación SSO/OIDC).

Infraestructura: Docker y GitHub Actions (CI/CD).

Analítica: Power BI Desktop (Visualización de KPIs).

4. Catálogo de Categorías y Prioridades

| Categoría | Definición | Ejemplo |
| --- | --- | --- |
| Ausencias | Faltas injustificadas, retardos recurrentes o permisos no autorizados. | "El empleado faltó 3 días sin avisar." |
| Conflictos | Problemas interpersonales entre compañeros o con superiores. | "Discusión verbal por uso de recursos compartidos." |
| Incumplimientos | Violación de políticas internas o normas de conducta. | "Uso indebido de equipo de cómputo en horario laboral." |
| Riesgos | Condiciones inseguras en el entorno laboral. | "Piso mojado sin señalización en pasillo principal." |
| Solicitudes Administrativas | Trámites internos que requieren seguimiento de RRHH. | "Solicitud de constancia laboral para trámite bancario." |

Niveles de Prioridad:

Alta: Riesgo inminente de seguridad, conflicto activo o impacto legal.

Media: Afecta la operación diaria o requiere intervención pronta.

Baja: Trámite administrativo o situación menor sin urgencia.

5. Ciclo de Vida de la Incidencia (Estados y Transiciones)

Se define un flujo lineal con opción de reapertura controlada. La clasificación oficial (category_id) se valida antes de entrar a revisión.

| Estado | Descripción |
| --- | --- |
| PENDIENTE | Pendiente de completar validación de clasificación y asignación. |
| EN_REVISION | Asignada a un responsable para análisis y resolución. |
| RESUELTA | Caso cerrado internamente, esperando confirmación final. |
| CERRADA | Finalizada administrativamente. Solo admite reapertura. |

Matriz de Transiciones y Reglas:

| Transición | Quién puede ejecutarla | Condiciones Obligatorias |
| --- | --- | --- |
| PENDIENTE → EN_REVISION | Admin RH o Supervisor autorizado | assigned_to activo y autorizado, category_id, priority, validated_by y validated_at definidos. Registrar cycle_start_at al entrar. |
| EN_REVISION → RESUELTA | Admin RH o Supervisor autorizado | resolution_text obligatorio. El sistema registra resolved_at. |
| RESUELTA → CERRADA | Admin RH | El sistema registra closed_at. |
| RESUELTA/CERRADA → EN_REVISION | Admin RH | Motivo obligatorio y responsable activo autorizado. Archivar ciclo previo, limpiar resolución y fechas de cierre; actualizar cycle_start_at. |

Nota sobre reapertura: Antes de cambiar a EN_REVISION, se archivan en historial los valores de cycle_start_at, resolution_text, resolved_at y closed_at del ciclo anterior. Se limpian resolution_text, resolved_at y closed_at; cycle_start_at toma la fecha de reapertura. Se exige motivo y responsable activo con acceso al caso. La operación completa es atómica.

6. Reglas de Confidencialidad y Visibilidad

Confidencialidad desde el Origen:

Al crear una incidencia, cualquier rol puede marcar "Solicitar Confidencialidad".

Política explícita: Al solicitar confidencialidad, is_confidential pasa a TRUE desde el registro. Solo Admin RH puede consultar el caso. El reportante pierde acceso mientras se mantenga la marca, aunque RH ya esté atendiendo el caso. El formulario informa esta consecuencia antes del envío. Retirar la marca restablece únicamente el acceso que corresponda al rol y al empleado afectado.

Cambio a Confidencial (Edición):

Solo Admin RH puede marcar como confidencial un caso existente. Si assigned_to es un Supervisor y el caso está EN_REVISION, debe seleccionar un Admin RH activo en la misma operación; el cambio de confidencialidad y la reasignación son atómicos. En PENDIENTE puede quedar sin responsable en la bandeja de RH. En RESUELTA o CERRADA se requiere reapertura para cambiar confidencialidad o asignación. La marca inicial al crear está permitida para todos los roles.

Retirar Confidencialidad:

Solo Admin RH puede quitar la marca.

Requiere motivo obligatorio registrado en el historial.

Al retirar la marca, el caso vuelve a ser visible para Supervisores/Empleados según sus reglas estándar.

Reglas de visibilidad por rol: cada usuario debe satisfacer la regla correspondiente a su rol. Las mismas restricciones se aplican en listados, consulta por ID, búsquedas, cambios y notificaciones.

Empleado: affected_employee_id = user_id e is_confidential = FALSE. Se usa el empleado afectado, no necesariamente created_by.

Supervisor: el departamento actual del empleado afectado coincide con el del supervisor e is_confidential = FALSE. Los cambios de departamento actualizan el acceso; se auditan y exigen revisar responsables que pierdan autorización.

Admin RH: Todos los casos (incluyendo confidenciales).

7. Requisitos Funcionales (RF) con Criterios de Aceptación

RF-1: Autenticación SSO (Microsoft Entra ID)

Descripción: Inicio de sesión único usando OIDC/OAuth2.

Lógica de Validación:

Validar firma JWT contra llaves públicas de Azure AD.

Verificar emisores (iss), audiencia (aud) y vigencia (exp).

Extraer oid y tid del token validado. Persistir oid en external_id y tid en tenant_id, con restricción única sobre ambos.

Buscar usuario por tenant_id y external_id. Solo se aceptan tokens del tenant empresarial configurado. Si el usuario no está registrado o está inactivo, se deniega acceso. Para el MVP, Admin RH administra una lista autorizada manual; la sincronización automática queda fuera del alcance.

Verificar is_active = TRUE en BD local.

Desactivación: Admin RH debe actualizar is_active al dar de baja a un usuario y la API lo comprueba en cada solicitud. No se presupone revocación inmediata por una baja solo en Entra ID. La operación de baja registra actor y fecha; si hay casos activos asignados, exige reasignarlos a usuarios activos autorizados.

Criterio de Aceptación: Un token válido pero con un oid no registrado o con usuario inactivo en BD es rechazado con error 403.

RF-2: Registro de Incidencias

Descripción: Formulario para crear incidencias.

Restricciones por Rol:

Empleado: Solo puede registrar sobre sí mismo (affected_employee_id = user_id).

Supervisor: Puede registrar sobre empleados de su propio departamento.

Admin RH: Puede registrar sobre cualquier empleado.

Edición: Solo Admin RH y Supervisores autorizados pueden editar título y descripción en PENDIENTE o EN_REVISION; el Supervisor únicamente en casos no confidenciales de su departamento. El Empleado no puede editar tras crear. Cada edición guarda actor, fecha y valores anteriores/nuevos en el historial. Se conserva así el contenido original. En RESUELTA o CERRADA no se permite editar contenido, clasificación, prioridad, asignación o confidencialidad sin reapertura.

Eliminación: No se permite eliminación física ni lógica de incidencias. Los registros creados por error siguen el flujo normal: asignación y clasificación, resolución con texto «Registro creado por error; sin acción correctiva» y cierre por Admin RH. Las correcciones conservan historial; no se incorpora un estado ANULADA.

Criterio de Aceptación: La API rechaza (403) intentos de crear incidencias fuera del ámbito autorizado del rol.

RF-3: Clasificación IA y Validación Humana

Descripción: Envío de texto a OpenAI vía LangChain (cola Redis).

Permisos de edición: Solo Admin RH y Supervisores autorizados pueden validar o cambiar category_id y priority en PENDIENTE o EN_REVISION. Los Supervisores solo acceden a casos no confidenciales de su departamento. RESUELTA y CERRADA requieren reapertura para cambiar la clasificación.

Manejo de Errores: Si la IA falla, se registra ai_error. El usuario autorizado puede ingresar manualmente categoría y prioridad para continuar.

Trazabilidad: ai_suggestion conserva la primera respuesta válida de IA para el texto original analizado. Se registran validated_by y validated_at tanto al aceptar como al corregir o clasificar manualmente por falla. Las respuestas tardías nunca sobrescriben valores humanos. Una edición posterior de descripción no relanza ni sustituye la sugerencia original; invalida la validación previa y exige nueva validación manual antes de resolver. Todos los cambios conservan auditoría.

Criterio de Aceptación: El dashboard muestra la sugerencia de IA vs. la decisión final. Se permite guardar cambios manuales si la IA falló.

RF-4: Asignación y Gestión de Casos

Descripción: Flujo de trabajo para responsables.

Reglas:

Quién asigna: Admin RH (todos) y Supervisores (solo su depto).

A quién: Usuarios con rol Admin RH o Supervisor que tengan permiso de ver el caso.

Obligatoriedad: Para cambiar de PENDIENTE a EN_REVISION, assigned_to es obligatorio.

Criterio de Aceptación: La API rechaza la asignación si el usuario seleccionado no tiene permisos sobre la incidencia.

RF-5: Notificaciones Automatizadas

Eventos:

Creación de incidencia (Notifica a Admins si no hay asignado).

Asignación/Reasignación: Notifica al nuevo assigned_to.

Cambio de estado a RESUELTA (Notifica a created_by y affected_employee solo si tienen permiso de ver).

Reapertura (Notifica a assigned_to actual).

Contenido: Asunto: "Incidencia #[ID] Actualizada". Cuerpo: Enlace directo al caso.

Errores: Si el correo falla, se registra en log pero no bloquea la operación.

RF-6: Analítica (Power BI)

Acceso: El archivo .pbix es de uso exclusivo de Admin RH y Gerencia.

Datos Permitidos: Para el MVP, el reporte se limita a datos agregados: Conteo de incidencias, Promedios de tiempo, Categorías, Departamentos. Prohibido: Nombres de empleados, descripciones de texto libre, resoluciones textuales o correos electrónicos.

KPIs Clave:

Total de incidencias por categoría/mes.

Tiempo promedio de resolución del último ciclo: promedio de (resolved_at - cycle_start_at), expresado en horas, para casos cuyo último ciclo esté resuelto o cerrado. Los ciclos actualmente abiertos no se incluyen. El historial conserva los ciclos previos para consultas históricas.

Evaluación inicial de IA: comparar ai_suggestion.category_id con la etiqueta de referencia definida antes de ejecutar cada uno de los 20 casos simulados. Se exige un mínimo de 18 aciertos de 20 (90 %, superior al 85 %). La validación humana posterior no modifica la referencia de esta prueba.

Tasa de reapertura: seleccionar casos con al menos una resolución en el periodo y contar cada ID una sola vez. Numerador: casos de esa población reabiertos después de su primera resolución dentro del periodo y hasta la fecha de corte. Denominador: total de casos de esa población. Resultado = numerador / denominador × 100. Si el denominador es cero, mostrar «Sin datos». Calcular con eventos históricos, no solo con las fechas actuales.

Concordancia operativa de IA: porcentaje de casos con sugerencia válida y decisión humana validada en que ambas categorías coinciden. Se informa por separado de la evaluación etiquetada; los casos sin sugerencia válida se excluyen y se contabilizan aparte.

Reglas generales de notificación: verificar de nuevo el permiso del destinatario justo antes del envío. Si perdió acceso, omitir el correo. Deduplicar destinatarios y eventos; registrar intentos y reintentar como máximo tres veces ante fallos transitorios. Después, dejar el fallo para revisión de Admin RH. El correo no incluye descripciones, resoluciones ni datos personales.

Gestión de usuarios del MVP: solo Admin RH puede dar de alta usuarios previamente identificados en Entra ID, asignar roles y departamentos, desactivar y reasignar casos. Se realiza mediante comandos administrativos documentados y auditados; no se exige una pantalla adicional. El primer Admin RH se provisiona con un comando de instalación. Nunca se aceptan roles enviados por el cliente como fuente de autorización.

8. Estructura de Base de Datos (PostgreSQL)

users: id, email, external_id (UUID oid), tenant_id (UUID tid), nombre_completo, departamento_id (FK departamentos), rol_id (FK roles), is_active. Unicidad: (tenant_id, external_id).

roles: id, nombre (ADMIN_RH, SUPERVISOR, EMPLEADO).

categorias_incidencia: id, nombre, descripcion.

incidencias:

id, titulo, descripcion

incident_date (Date)

created_at, updated_at (Timestamp)

status (Enum: PENDIENTE, EN_REVISION, RESUELTA, CERRADA)

priority (Integer: 1=Baja, 2=Media, 3=Alta)

category_id (FK categorias_incidencia) -> Oficial

ai_suggestion (JSONB) -> Original IA

ai_error (Text) -> Mensaje de error si falla

validated_by (FK users), validated_at (Timestamp)

resolution_text (Text) -> Obligatorio al resolver

resolved_at, closed_at (Timestamp)

cycle_start_at (Timestamp) -> Fecha de entrada a EN_REVISION actual

reopening_reason (Text) -> Obligatorio al reabrir

is_confidential (Boolean, Default False)

created_by (FK users), affected_employee_id (FK users), assigned_to (FK users)

historial_incidencias:

id, incidencia_id (FK), usuario_id (FK), accion (CREADO, ESTADO_CAMBIADO, ASIGNADO, REAPERTURA, VALIDACION_IA, CAMBIO_CONFIDENCIALIDAD), detalle (JSONB con cambios previos/nuevos), fecha.

Departamentos: id, nombre, is_active. Los usuarios se vinculan por departamento_id. El departamento usado para seguridad es el actual del empleado afectado; los reportes por departamento del evento utilizan department_id_at_creation, guardado al registrar la incidencia.

Campos y restricciones adicionales de incidencias: department_id_at_creation (FK departamentos), ai_status (PENDIENTE, COMPLETADA, FALLIDA) y clasificación/validación inicialmente nullable. EN_REVISION exige responsable activo, category_id, priority, validated_by y validated_at. Priority solo admite 1, 2 o 3. created_by se obtiene de la identidad autenticada. Fechas operativas en UTC con zona horaria; incident_date conserva la fecha del evento.

Historial ampliado: agregar acciones CONTENIDO_EDITADO y USUARIO_ACTUALIZADO según la entidad auditada. Los eventos de transición guardan estado anterior/nuevo, responsable, inicio de ciclo y fechas de resolución/cierre. Los eventos de cambio de contenido y clasificación conservan valores anteriores/nuevos. El historial es de solo lectura para usuarios de aplicación.

Power BI: solo Admin RH y Gerencia reciben el archivo. La extracción utiliza vistas agregadas con cuenta de servicio de solo lectura; el modelo no importa registros individuales ni campos prohibidos. Actualización manual antes de cada entrega del reporte, mostrando fecha de corte. Gerencia es destinataria de reportes, no un nuevo rol de la aplicación.

9. Requisitos No Funcionales (RNF)

RNF-1: Seguridad: Comunicación HTTPS obligatoria. Tokens JWT validados criptográficamente.

RNF-2: Rendimiento: clasificación IA y correos se ejecutan en segundo plano mediante cola Redis y un proceso worker. Para lectura, creación y actualización simples, p95 de API inferior a 200 ms en Docker local con 10 usuarios simultáneos y datos simulados. Se excluye la duración de servicios externos; la aceptación del trabajo en cola sí forma parte de la respuesta de creación. El informe registra hardware, volumen de datos, duración, errores y latencias.

RNF-3: Pruebas: Se utilizarán datos simulados (Mock Data) para QA. Pruebas de aceptación deben incluir: transiciones inválidas, acceso directo por ID (IDOR), creación en nombre de terceros, fallas de IA y notificaciones confidenciales.

QA de aceptación: verificar creación válida y rechazos por rol; accesos por ID y departamento; pérdida de acceso al marcar confidencial; reasignación atómica; protección de casos cerrados; todas las transiciones válidas e inválidas; historial de cada ciclo; edición auditada y revalidación; falla y respuesta tardía de IA; baja de usuarios; permisos y deduplicación de correos; fórmulas con denominador cero; y prueba de carga. Los 20 casos de IA usan datos simulados etiquetados antes de la ejecución y cubren las cinco categorías.

Cola IA: máximo tres intentos ante fallos transitorios; después marcar ai_status = FALLIDA y permitir clasificación manual. Un JSON inválido no se presenta como clasificación válida. No se generan respuestas simuladas fuera de QA. La API confirma creación sin esperar a OpenAI; la interfaz muestra pendiente, completada o fallida.

10. Cronograma Detallado (Semanas)

| Semana | Actividad Principal | Entregable |
| --- | --- | --- |
| 1 | Setup Infraestructura (Docker, Postgres, Redis) y Auth (Entra ID con OID). | Repo Git con Docker Compose funcional y Login básico seguro. |
| 2 | Backend Core: CRUD Incidencias, Lógica de Roles/Permisos y Confidencialidad. | Endpoints protegidos funcionando con filtros de seguridad. |
| 3 | Integración IA (LangChain + OpenAI), Cola Redis, Manejo de Errores y Auditoría. | Endpoint /analizar asíncrono y tabla de historial completa. |
| 4 | Frontend React: Formularios, Dashboard y Visualización de IA. | UI completa conectada al backend. |
| 5 | Power BI Desktop: Modelado de datos, KPIs y Notificaciones (Email Service). | Archivo .pbix y servicio de emails configurado. |
| 6 | QA Integral: Pruebas de permisos, confidencialidad, historial y documentación. | Reporte de pruebas y Manuales de Usuario. |

11. Gestión de Configuración y Seguridad

Para garantizar la seguridad de las credenciales y facilitar el despliegue del proyecto, se implementará la siguiente estrategia:

Archivo .env (Entorno Local): Se utilizará para almacenar las credenciales reales (Claves de OpenAI, ID de Azure, contraseña de PostgreSQL). Este archivo será excluido del control de versiones mediante un archivo .gitignore.

Archivo .env.example (Control de Versiones): Se entregará una plantilla en el repositorio para guiar a los desarrolladores, utilizando valores simulados.

Documentación en README.md: Instrucciones claras sobre cómo configurar el entorno local.

Control de versión 1.6: consolida reglas de confidencialidad, asignación, edición, baja de usuarios, reapertura, evaluación de IA y reportes. Sustituye la versión 1.5 como base de desarrollo. No incorpora consulta del reportante a casos confidenciales.
