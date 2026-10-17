# PluriOne



Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V.



**Proyecto:** G19X-ITSM-GASH-918-ACADEMIC

**Autora:** Gilian Abril Sánchez Hernández



## Estado actual



API FastAPI con `/health`, `/health/db`, `/docs` y `/openapi.json`; modelos y migración PostgreSQL inicial verificados manualmente. Autenticación local implementada y probada en SQLite/HTTP; migración 0002 y prueba manual en PostgreSQL pendientes. Incidencias, frontend e IA siguen pendientes. PRD vigente: 1.9.



## Alcance



Registro y seguimiento de incidencias, acceso por roles y departamento, confidencialidad, clasificación asistida por IA con validación humana, auditoría, correo y analítica agregada.



Tecnologías previstas: React, FastAPI, PostgreSQL, Redis, autenticación local FastAPI, OpenAI con LangChain, Docker y Power BI Desktop.



## Documentación



- [PRD vigente](docs/PRD.md)

- [PRD Word 1.6 — referencia histórica](docs/PRD_PluriOne_v1.6.docx)

- [Plan de desarrollo y criterios de término](docs/BACKLOG.md)

- [Decisiones iniciales](docs/DECISIONES.md)

- [Entregables de residencia](docs/ENTREGABLES.md)

- [Bitácora de avances](docs/BITACORA.md)

- [Trazabilidad de requisitos](docs/TRAZABILIDAD.md)

- [Reporte QA](docs/REPORTE_QA.md)

- [Manual técnico](docs/MANUAL_TECNICO.md)



## Estructura



`backend/` contiene las capas previstas de FastAPI; `frontend/`, las vistas React; `infra/`, el despliegue por implementar. El backend tiene un punto de entrada ejecutable; frontend sigue pendiente; la configuración Docker de API, PostgreSQL y Redis está preparada, pendiente de ejecución.



## Ejecutar la API



Consultar [instalación y arranque del backend](backend/README.md). No se necesita configurar claves para la API inicial.



## Configuración



Copiar `.env.example` a `.env` y completar las variables locales cuando se implementen los servicios. Nunca publicar `.env`, credenciales o datos reales de empleados. La plantilla no permite autenticación ni conexión a servicios hasta configurar valores válidos.



## Trabajo en Git



Crear commits pequeños al completar cambios verificables. Cada mensaje debe describir el avance real. Las revisiones del PRD se registran cuando se modifica su contenido; no se generan commits retrospectivos para aparentar actividad. No hacer commits vacíos para cumplir una frecuencia.



## Arranque con contenedores



Consultar [el entorno Docker](infra/README.md). Completar POSTGRES_PASSWORD en .env y ejecutar desde la raíz `docker compose up -d --build --wait`. La conexión PostgreSQL se comprueba con /health/db tras aplicar la migración. Redis todavía no se utiliza.



## Esquema de datos



Seguir [migración y validación PostgreSQL](docs/DATOS.md).



## Datos simulados



Consultar [carga de usuarios de QA](docs/DATOS_DEMO.md). Requiere confirmación explícita y no habilita inicio de sesión.



## Autenticación local



API 0.3.0 y PRD 1.9. Se sustituye Entra ID por correo y contraseña, Argon2id y sesiones revocables. Aplicar migración 0002 y crear el primer Admin RH siguiendo [AUTENTICACION.md](docs/AUTENTICACION.md). La copia Word del PRD 1.6 es histórica; el PRD Markdown es vigente.



## Reglas consolidadas del MVP



El PRD 1.9 organiza RF-1 a RF-8 y distingue modelo objetivo de esquema implementado. Incluye riesgos de entorno, conflicto de interés y vigencia de clasificación, aún pendientes de código/migración. No asumir que el esquema actual ya los soporta. Estado vigente en BACKLOG.md y TRAZABILIDAD.md.


La revisión 1.9 refuerza privacidad de agregados, revisión independiente de participantes y límites de alcance. Son requisitos objetivo, no funciones ya terminadas.

## Actualización de esquema 0003

API 0.4.0 prepara ámbitos PERSONA/ENTORNO, participantes y clasificación vigente. Aplicar la nueva migración siguiendo [DATOS.md](docs/DATOS.md). Las cuentas existentes se conservan; no repetir bootstrap. No existen aún endpoints de incidencias.

## Registro y consultas de incidencias

API 0.5.0 añade rutas /incidents sobre esquema 0003, sin migración adicional. Seguir [INCIDENCIAS.md](docs/INCIDENCIAS.md) para registrar y consultar con sesión local, datos DEMO y auditoría. Asignación/transiciones, frontend e integraciones siguen pendientes.

API 0.6.0 incorpora gestión protegida de clasificación, responsable, contenido y ciclo. Guía y cuerpos de ejemplo en docs/INCIDENCIAS.md. Mantiene esquema 0003; reconstruir imagen sin repetir bootstrap ni seed. La comprobación manual de estas operaciones sigue pendiente.

API 0.7.0: revisión de participantes y confidencialidad con recusa, reasignación/retroceso protector y auditoría. Reconstruir imagen; sin nueva migración. Guía de rutas y prueba manual en docs/INCIDENCIAS.md. La provisión de RH independiente adicional por operador y el frontend siguen pendientes.

Procedimiento de operador para crear RH independiente adicional preparado y documentado en docs/ADMIN_INDEPENDIENTE.md. Aplicar actualización y reconstruir antes de usar el nuevo comando; conserva API 0.7.0/esquema 0003 y no cambia casos existentes.

El procedimiento de RH independiente fue aplicado y ejecutado según reporte de la autora; evidencias y límites de validación en docs/REVISION_RH_INDEPENDIENTE.md. RF-7 sigue parcial.

Administración de usuarios 0.8.0 preparada: listado/opciones y actualización auditada de rol, departamento y activación, con revisión de casos y revocación. Paquete pendiente de aplicación; instrucciones y límites en docs/ADMIN_USUARIOS.md. Mantiene esquema 0003.

Administración backend 0.8.0 aplicada según la autora; suite completa observada: 77 aprobadas, 3 PostgreSQL omitidas y 1 advertencia. Evidencias de administración y límites en docs/REVISION_ADMIN_USUARIOS.md. RF-7 sigue parcial; frontend/CRUD de departamentos y concurrencia pendientes.

## Panel web local

Primera UI React: iniciar API/Docker, luego desde frontend ejecutar npm.cmd ci y npm.cmd run dev. Abrir http://127.0.0.1:5173/. Login, listado con filtros y detalle/historial; gestión sigue en Swagger en esta entrega parcial. Guía [FRONTEND.md](docs/FRONTEND.md), sin .env frontend ni tokens persistentes. No es despliegue productivo.
