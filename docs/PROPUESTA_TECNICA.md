# Propuesta técnica de PluriOne

## Propósito y base

Proponer una solución local para registrar y atender incidencias laborales simuladas con acceso restringido, decisiones humanas y evidencia de las operaciones. Este documento consolida las decisiones del sistema ya implementado; no acredita entrevistas, mejora operativa medida ni aprobación institucional.

La fuente funcional es el [PRD](PRD.md); el [MVP](MVP.md) distingue funciones disponibles y condiciones de aceptación. La [arquitectura](ARQUITECTURA.md) describe componentes y flujos comprobables en el repositorio.

## Necesidad que se atiende

El proyecto requiere un expediente con hechos, ámbito, categoría, prioridad, responsable y seguimiento, limitado a quienes pueden intervenir. La confidencialidad y los conflictos de interés deben prevalecer sobre la asignación. Las decisiones y cambios necesitan una historia auditable; los reportes no deben exponer información individual.

Estas necesidades proceden del alcance documentado. No se dispone de una medición de tiempos, errores o satisfacción en la organización que permita afirmar una mejora porcentual. Esa evaluación requeriría un protocolo y datos autorizados separados de la demostración académica.

## Objetivos verificables

| Objetivo | Comportamiento esperado | Cómo comprobarlo |
| --- | --- | --- |
| Ordenar el registro | Casos PERSONA/ENTORNO con datos y catálogos válidos | Formularios, contrato API y pruebas de esquema/registro |
| Restringir acceso | Sesión vigente, rol, departamento y ausencia de conflicto en cada operación | Matriz de permisos y pruebas negativas de consulta/mutación |
| Dar seguimiento | Clasificación humana, asignación y transiciones controladas | Recorrido completo con historial y rechazo de estados inválidos |
| Apoyar la clasificación | Sugerencia sobre texto simulado revisado, sin decidir automáticamente | Evaluación de referencias y verificación de validación humana separada |
| Comunicar eventos | Avisos mínimos solo a destinatarios elegibles | Outbox, seguimiento de intentos y captura SMTP de pruebas |
| Presentar indicadores | Población parcial, agregados protegidos y corte visible | Pruebas SQL/ACL y revisión del informe Power BI |

## Cobertura de requisitos

| Requisito | Elementos de la solución |
| --- | --- |
| RF-1 | Autenticación local, sesiones y cambio de contraseña |
| RF-2 | Formularios y servicios de registro, edición y consulta |
| RF-3 | Worker IA, texto revisado, salida estructurada y validación humana |
| RF-4 | Asignación, ciclo, participantes, confidencialidad y auditoría |
| RF-5 | Outbox, worker SMTP y seguimiento de notificaciones |
| RF-6 | Vistas protegidas, cuenta de lectura e informe Power BI |
| RF-7 | Administración de usuarios y departamentos, con procedimientos de operador |
| RF-8 | Panel React con navegación, filtros y acciones según permisos |

La [trazabilidad](TRAZABILIDAD.md) relaciona estos elementos con evidencia y aceptación pendiente; la tabla no certifica requisitos completos.

## Solución y decisiones de tecnología

| Elemento | Decisión adoptada | Motivo y límite |
| --- | --- | --- |
| Interfaz | React con Vite en desarrollo | Pantallas por tarea y componentes que pueden probarse por separado; requiere servidor y HTTPS distintos para producción |
| API | FastAPI y contratos tipados | Validación de entradas y OpenAPI; autorización y reglas permanecen en servidor |
| Persistencia | PostgreSQL, SQLAlchemy y Alembic | Transacciones, restricciones y cambios de esquema reproducibles; no implica respaldo o alta disponibilidad |
| Identidad | Credenciales locales y sesiones opacas revocables | Permite operar el MVP sin un tenant externo; exige custodia y recuperación por operador |
| Trabajo asíncrono | PostgreSQL durable y workers separados | Conservar solicitudes aunque un worker esté detenido; Redis avisa sobre IA sin ser la fuente del trabajo |
| IA | OpenAI mediante LangChain, salida estructurada y revisión humana | Asistencia acotada; coste, errores y límites del proveedor requieren control |
| Correo | Outbox transaccional y SMTP, con Mailpit local | Separa evento de negocio de transporte; aceptación SMTP no confirma lectura ni garantiza envío único |
| Analítica | Vistas agregadas y Power BI Desktop con cuenta de lectura | Excluir y suprimir antes de importar; una copia distribuida no puede revocarse automáticamente |
| Entorno | Compose local y dependencias fijadas | Facilita reconstrucción; no instala herramientas del equipo ni sustituye operación productiva |

La decisión de autenticación local y API directa OpenAI está registrada en [DECISIONES.md](DECISIONES.md). Las dependencias y migraciones conservan los identificadores necesarios para reproducibilidad, sin organizar el producto por antiguas entregas.

## Alternativas y compromisos

| Alternativa | Compromiso de la solución elegida |
| --- | --- |
| Identidad institucional con Entra ID | Se evita depender de autorización del tenant para la demostración; no se incorpora SSO ni MFA institucional |
| Clasificación exclusivamente manual | Sigue disponible como flujo principal; la IA añade ayuda opcional y controles, sin poder aprobar decisiones |
| Enviar correo durante la petición de registro | La outbox evita esperar a SMTP y conserva el evento, a cambio de gestionar reintentos y estados inciertos |
| Importar expedientes completos y ocultarlos con filtros BI | Se opta por restringir la extracción en PostgreSQL; la supresión conservadora puede dejar el informe sin cifras |
| Activar todos los módulos desde el inicio | Perfiles y configuración explícitos permiten usar el núcleo sin llamadas IA ni correo externo |

Son compromisos de diseño, no resultados de un estudio comparativo de rendimiento o costes.

## Alcance y exclusiones

Incluye cuentas administradas, registro, consulta, gestión, participantes, confidencialidad, auditoría, asistencia IA opcional, correo por eventos e informe agregado. Los actores son Empleado, Supervisor y Admin RH; Gerencia recibe agregados y el operador atiende configuración/credenciales, sin convertirse por ello en gestor autorizado de expedientes.

Quedan fuera nómina, decisiones disciplinarias automáticas, procedimientos legales automatizados, SLA y alertas por tiempo, aplicación móvil nativa, registro público y uso productivo con datos laborales reales. Los límites detallados están en el MVP y el PRD.

## Implantación y aceptación

1. Preparar herramientas, configuración privada y base; aplicar migraciones y crear el primer administrador únicamente en una instalación nueva.
2. Comprobar el flujo manual por roles, incluida la denegación de acceso por confidencialidad o conflicto de interés.
3. Activar integraciones de forma explícita: IA con textos simulados revisados, correo con captura local y BI con cuenta limitada.
4. Completar escenarios negativos, concurrencia pertinente, carga, refresco del informe y recuperación de respaldo.
5. Entregar manual de usuario, plan de soporte, QA e informe; registrar capacitación y aceptación solo cuando ocurran.

La implementación y varios recorridos ya tienen evidencia; esta secuencia no implica repetirlos todos ni reinicializar datos existentes. Los pendientes actuales se consultan en el [backlog](BACKLOG.md). No se fijan fechas ni duración sin capacidad y fecha límite confirmadas.

## Recursos y costes por confirmar

Se requiere un equipo capaz de ejecutar Docker Desktop y el panel local, almacenamiento para PostgreSQL y evidencias, herramientas de desarrollo y Power BI Desktop para revisar el informe. La memoria y capacidad mínimas del escenario no se han medido formalmente.

Las llamadas IA consumen recursos de la cuenta configurada; un presupuesto disponible no demuestra suficiencia para una carga futura. SMTP externo, infraestructura, copias de seguridad y distribución o licenciamiento del informe requieren definición separada si se amplía el alcance. No se presenta una cotización ni precios vigentes sin una evaluación específica.

## Riesgos y respuesta

| Riesgo | Control disponible | Trabajo pendiente o límite |
| --- | --- | --- |
| Exposición de un expediente | Permisos por objeto, independencia y confidencialidad | Completar aceptación por rol y revisión de operación |
| Sugerencia IA incorrecta | Validación humana, catálogo cerrado y abstención | Los resultados simulados no generalizan automáticamente |
| Pérdida o repetición de trabajo | Persistencia durable, propietario e intentos acotados | Una interrupción cerca de una llamada externa puede repetir coste o correo |
| Inferencia desde reportes | Exclusión, supresión de subconjuntos y ausencia de totales | Riesgo temporal/externo residual y custodia de copias |
| Pérdida de datos locales | Volúmenes persistentes | Falta documentar y probar respaldo/restauración; persistencia no es respaldo |
| Confundir avance con entrega completa | MVP, trazabilidad y QA con límites | Aceptación, capacitación e informe final aún pendientes |

## Criterios de evaluación

La aceptación funcional sigue la [trazabilidad](TRAZABILIDAD.md). Seguridad se evalúa con resultados permitidos y rechazados, sin secretos en evidencia. Rendimiento mantiene la meta del PRD: p95 menor de 200 ms para operaciones simples, con 10 usuarios, 100 casos simulados y cinco minutos tras calentamiento, excluyendo duración externa. No se ha acreditado esa medición.

La evaluación IA y la concordancia de categorías de BI son medidas distintas: la primera compara contra referencias simuladas; la segunda compara sugerencia y clasificación humana vigente en la población exportable. Ninguna por sí sola acredita calidad global ni mejora de la organización.

El resultado de esta propuesta es una solución y un plan verificables, con implementación existente y pendientes explícitos. La evidencia detallada está en [QA](REPORTE_QA.md); las decisiones anteriores permanecen en la bitácora y Git.
