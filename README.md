# PluriOne

Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V.

**Proyecto:** G19X-ITSM-GASH-918-ACADEMIC  
**Autora:** Gilian Abril Sánchez Hernández

## Estado actual

API FastAPI con `/health`, `/health/db`, `/docs` y `/openapi.json`; modelos y migración PostgreSQL inicial verificados manualmente. El flujo de incidencias, autenticación, base de datos, frontend e IA siguen pendientes. El PRD 1.6 es la base de desarrollo elegida por la autora.

## Alcance

Registro y seguimiento de incidencias, acceso por roles y departamento, confidencialidad, clasificación asistida por IA con validación humana, auditoría, correo y analítica agregada.

Tecnologías previstas: React, FastAPI, PostgreSQL, Redis, Microsoft Entra ID, OpenAI con LangChain, Docker y Power BI Desktop.

## Documentación

- [PRD vigente](docs/PRD.md)
- [Documento Word recibido](docs/PRD_PluriOne_v1.6.docx)
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
