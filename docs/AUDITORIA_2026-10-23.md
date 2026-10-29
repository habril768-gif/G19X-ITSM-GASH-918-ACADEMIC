# Respuesta a la auditoría del 23 de octubre de 2026

Revisión realizada el **29 de octubre de 2026** sobre el código local y la rama pública `main`. La referencia 7.7 del corte es orientativa, no una calificación final. Este documento registra cambios verificables; no sustituye la evaluación del docente.

| Observación | Respuesta y evidencia revisable | Límite |
| --- | --- | --- |
| Sin avances en GitHub desde el 17 de octubre | Se recuperó el historial local posterior a `7886d1e`, incluidos correo, evaluación IA y Power BI, y se preparó una publicación del estado actual. Los commits originales se conservan localmente en un bundle, sin reescribir la rama remota. Consultar el historial Git remoto para confirmar recepción. | Una copia local o un commit preparado no equivale a un push confirmado. |
| README como guía, no bitácora | [README](../README.md): propósito, requisitos, cinco pasos, `.env`, Compose, migraciones, primer RH, `npm ci` y `npm run dev`; enlaces a manuales y cuentas ficticias. [DEMO](DATOS_DEMO.md) corrige la referencia antigua a Entra y explica contraseñas locales interactivas. | No hay contraseñas públicas; no se sobrescribe `.env` existente. |
| Codificación dañada | Se comprobó UTF-8 y ausencia de patrones de mojibake en 89 archivos de app, pruebas y documentos señalados; se corrigieron dos comentarios de pruebas restantes. La descripción OpenAPI mantiene «Gestión» legible. | No se reescriben capturas o citas históricas. La comprobación de fuente no es una captura visual de Swagger. |
| RF-5: correo al registrar, asignar y cerrar | Ya existían creación, asignación, resolución y reapertura con outbox/worker y Mailpit ([85](evidencias/85-correo-eventos-pruebas.json), [92](evidencias/92-correo-recorrido-verificado.json)). Se añade cierre con migración 0008, permisos vigentes, deduplicación, misma transacción del evento y descarte de cierres de ciclos anteriores. React identifica «Cierre». | El nuevo cierre tiene pruebas automatizadas; su recorrido Docker/Mailpit aún no se ha ejecutado en este equipo por el agente. |

## Actualizar una instalación existente

Con Docker Desktop iniciado, desde la raíz:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ACTUALIZAR_CORREO.ps1
docker compose exec api python -m alembic current
docker compose exec api python -m alembic check
```

La revisión vigente es **0008**. El script aplica `upgrade head` antes de arrancar la API/worker nuevos, conserva volúmenes y no genera avisos retrospectivos ni casos. La comprobación `/health/db` exige esta revisión.

Para la captura nueva, usa un caso ficticio visible al reportante: clasifícalo, asígnalo, resuélvelo y ciérralo con RH autorizado. Revisa el aviso de cierre en [Mailpit](http://127.0.0.1:8025) y en «Notificaciones por correo». Reabrir antes del despacho debe omitir el cierre anterior. La aceptación SMTP no demuestra entrega a un buzón externo. No es necesario activar IA.

## Comprobaciones de esta revisión

- Ocho pruebas nuevas de servicios con SQLAlchemy/SQLite: cierre deduplicado, dos destinatarios distintos, confidencialidad, baja posterior, reapertura, segundo ciclo, rollback ante fallo de outbox y DDL Alembic offline.
- Regresión directa de outbox: ocho unitarias y diecinueve casos de servicios anteriores, aprobados. Sin HTTP ni PostgreSQL real en esta ejecución.
- 102 pruebas unitarias de las herramientas de rendimiento, aprobadas; no se generó otra carga.
- Cuatro pruebas React de MailStatus, aprobadas; compilación de producción Vite aprobada.
- Se conserva pendiente RNF-2: las siete formales anteriores fallaron el umbral. Ningún diagnóstico breve acredita el requisito.

La ejecución completa de backend y la migración en PostgreSQL se delegan a los workflows ya definidos de GitHub al publicar; su resultado debe leerse en Actions, no suponerse aprobado. Registro estructurado: [evidencia 201](evidencias/201-respuesta-auditoria-cierre-correo.json).

## Publicación y comprobación remota confirmadas

**Publicado el 29 de octubre:** [commit1794299 en main](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/commit/179429934fb632e1874bd0dcd67ae00747e0f4ff). Código y documentación ya están disponibles para el siguiente corte. La instantánea preserva los archivos revisados; los commits locales originales permanecen respaldados en un bundle local.

GitHub Actions: [backend y PostgreSQL](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40946040298) aprobados; [frontend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40946040141) aprobado. Se verificó además la generación OpenAPI con descripción UTF-8 correcta. [Evidencia202](evidencias/202-publicacion-auditoria-ci-aprobada.json). Estas comprobaciones resuelven la publicación y validan el código/migración en CI; la captura del aviso de cierre en Mailpit del equipo y RNF-2 siguen pendientes.
