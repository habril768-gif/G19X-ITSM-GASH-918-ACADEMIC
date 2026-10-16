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
