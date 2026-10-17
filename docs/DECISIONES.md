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
