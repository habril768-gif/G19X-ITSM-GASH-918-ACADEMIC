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
