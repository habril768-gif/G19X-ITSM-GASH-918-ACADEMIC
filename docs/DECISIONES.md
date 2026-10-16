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
