# PluriOne

Plataforma Inteligente de Gestión de Incidencias Laborales para PluriOne S.A. de C.V.

**Proyecto:** G19X-ITSM-GASH-918-ACADEMIC  
**Autora:** Gilian Abril Sánchez Hernández

## Estado actual

Primera API FastAPI implementada: `/health`, `/docs` y `/openapi.json`. El flujo de incidencias, autenticación, base de datos, frontend e IA siguen pendientes. El PRD 1.6 es la base de desarrollo elegida por la autora.

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

`backend/` contiene las capas previstas de FastAPI; `frontend/`, las vistas React; `infra/`, el despliegue por implementar. El backend tiene un punto de entrada ejecutable; frontend e infraestructura siguen pendientes.

## Ejecutar la API

Consultar [instalación y arranque del backend](backend/README.md). No se necesita configurar claves para la API inicial.

## Configuración

Copiar `.env.example` a `.env` y completar las variables locales cuando se implementen los servicios. Nunca publicar `.env`, credenciales o datos reales de empleados. La plantilla no permite autenticación ni conexión a servicios hasta configurar valores válidos.

## Trabajo en Git

Crear commits pequeños al completar cambios verificables. Cada mensaje debe describir el avance real. Las revisiones del PRD se registran cuando se modifica su contenido; no se generan commits retrospectivos para aparentar actividad. No hacer commits vacíos para cumplir una frecuencia.
