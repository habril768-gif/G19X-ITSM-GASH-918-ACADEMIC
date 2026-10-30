# Correo por eventos

RF-5 implementa avisos asíncronos con una outbox PostgreSQL, worker separado y captura SMTP de desarrollo. Crear una incidencia no espera a SMTP. Los trabajos se guardan en la misma transacción que el evento auditado, incluso con el worker apagado; un fallo al guardar la outbox revierte toda la operación para evitar eventos perdidos. La migración 0006 añade la tabla sin generar avisos para expedientes históricos.

## Eventos y destinatarios

| Evento | Destinatarios candidatos |
| --- | --- |
| Creación sin responsable | Admin RH activo, departamento activo y acceso independiente |
| Asignación/reasignación | Nuevo responsable elegible; también por protección o cambios administrativos |
| Resolución | Reportante y afectado, deduplicados y solo con permiso de consultar |
| Cierre | Reportante y afectado, deduplicados y solo con permiso vigente |
| Reapertura | Responsable del nuevo ciclo |

Clasificación, edición de texto y guardar el mismo responsable no crean avisos adicionales. El cierre genera su propio aviso; al reabrir o cerrar de nuevo se omiten los cierres anteriores todavía pendientes. Sin destinatario autorizado se registra OMITIDA sin dirección de correo. Cada evento/destinatario tiene identidad única; mismo evento no se encola dos veces. Se consulta la dirección vigente justo antes de enviar, sin copiarla a la cola. Permisos y contexto se verifican al reclamar y de nuevo antes del despacho; asignaciones sustituidas, ciclos anteriores o resoluciones reabiertas se omiten. Los destinatarios no se amplían retrospectivamente si luego cambia su rol.

El asunto contiene solo el ID; cuerpo genérico con enlace `/?incident=UUID`. Sin título, nombres, categoría, descripción, estado o resolución. Cada destinatario recibe un mensaje individual. El enlace abre el expediente después de iniciar sesión y vuelve a pasar por la autorización de la API. Quien pierde acceso no recibe seguimiento ni resultado de casos confidenciales.

## Preparar la captura local

Desde la raíz, con Docker Desktop abierto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ACTUALIZAR_CORREO.ps1
```

Construye API/worker, aplica las migraciones hasta 0008 y actualiza ambos. No hace seed/bootstrap, no borra datos, no muestra .env y no activa ni evalúa IA. Conserva otros servicios existentes. El perfil `mail` añade Mailpit v1.27.4; solo el panel 8025 se publica en 127.0.0.1, SMTP 1025 queda interno. Si `MAILPIT_PORT` es distinto, abrir ese puerto. El primer recorrido Docker/Mailpit debe verificarse en el equipo; una prueba con SMTP local no acredita ese despliegue.

1. Abrir `http://127.0.0.1:8025` y crear una incidencia simulada nueva sin participantes RH implicados. Verificar los avisos a RH independiente. Puede haber eventos pendientes de nuevas operaciones registradas con esta versión aunque el worker todavía no estuviera activo.
2. Abrir el enlace, iniciar sesión como destinatario autorizado y comprobar que abre el expediente correcto.
3. Asignar, resolver, cerrar y reabrir. Revisar los destinatarios según la tabla, incluyendo deduplicación cuando reportante y afectado coinciden.
4. Con Admin RH autorizado, abrir «Notificaciones por correo» en el expediente y actualizar. Un empleado o supervisor no tiene acceso a este seguimiento. Registrar una captura sin sesiones ni credenciales visibles.

Mailpit captura mensajes sin entregarlos a buzones reales. No requiere cuenta de correo ni clave de OpenAI.

## Configuración y operación

El perfil de desarrollo fija MAIL_ENABLED=true, MAIL_MODE=capture, SMTP_HOST=mailpit, SMTP_PORT=1025, SMTP_TLS=none y SMTP_FROM=no-reply@plurione.invalid. WEB_BASE_URL configura el origen de React (por defecto http://127.0.0.1:5173); no debe contener sesión, consulta o fragmento. Detener únicamente `mail-worker` pausa los envíos sin perder la cola. No borrar MailDelivery para forzar repeticiones.

Fuera de Compose, `python -m app.mail.worker --once` procesa como máximo un trabajo con MAIL_ENABLED=true y las variables de PostgreSQL configuradas. Desactivado por defecto. Sondeo durable cada dos segundos: no depende de Redis; Redis sigue dedicado a avisos IA. No se añade librería de tareas ni secreto de OpenAI al worker de correo.

Adaptador externo preparado por variables SMTP_HOST/SMTP_PORT/SMTP_USERNAME/SMTP_PASSWORD/SMTP_FROM, MAIL_MODE=external, SMTP_TLS=starttls o ssl y WEB_BASE_URL HTTPS. El perfil de captura no cambia por editar esas variables: para usar otro servicio hace falta una configuración Compose deliberada. No se ha conectado ni enviado a un proveedor externo. El modo captura rechaza hosts fuera de mailpit/loopback y autenticación. No publicar .env ni registrar diálogos SMTP.

## Reintentos y límites

Un intento inicial y hasta tres reintentos transitorios (cuatro intentos totales), con esperas 5/10/20 segundos. Errores permanentes finalizan sin reintento; al agotarse quedan FALLIDA con mensaje genérico visible a RH autorizado mediante `GET /incidents/{id}/mail` paginado y sin caché. Sin reenvío manual automático ni alertas SLA.

El reclamo se confirma antes de SMTP, usa token y reserva de 120 segundos; un worker caído puede recuperarse sin crear otro evento. La transacción del despacho conserva el bloqueo del expediente y el bloqueo administrativo compartido, impidiendo que protección o cambios de rol se interpongan entre comprobación y envío. Cada operación de socket tiene timeout de cinco segundos; SMTP lento puede demorar brevemente mutaciones del caso/cambios administrativos. No se mantienen estos bloqueos durante la espera entre reintentos.

SMTP y PostgreSQL no comparten transacción: caída tras aceptación SMTP y antes de confirmar ENVIADA puede producir duplicados o entrega incierta. Message-ID estable ayuda a identificarlos, pero no garantiza exactly-once ni evita todos los duplicados. ENVIADA significa aceptada por SMTP, no lectura o entrega final. No se pueden retirar mensajes ya aceptados; su enlace siempre requiere acceso vigente.

Fuentes de implementación: [SMTP de Python](https://docs.python.org/3.11/library/smtplib.html), [bloqueos PostgreSQL](https://www.postgresql.org/docs/current/explicit-locking.html) y [contenedor oficial Mailpit](https://mailpit.axllent.org/docs/install/docker/).

## Recorrido de captura observado

Recorrido aportado por responsable: capturas 86–91 verifican tres avisos de creación a RH distintos, un aviso de asignación al supervisor, resolución al reportante del caso ENTORNO y reapertura al supervisor. Enlace abre el expediente correcto bajo cuenta RH; panel React muestra seis aceptaciones SMTP al primer intento. Mensaje mínimo con ID/enlace, sin descripción/resolución. Evidencia estructurada 92 con hashes; capturas conservadas sin edición ni credenciales visibles. SMTP de captura Mailpit, no entrega a buzones reales. No se consultó la base operativa ni se repitieron pruebas o llamadas IA. RF-5 tiene recorrido básico real; exclusiones/fallos reales y aceptación integral pendientes (cobertura automatizada previa: 85).

## Aviso de cierre añadido el 29 de octubre

Aplica migración0008 antes de usar esta versión (script ACTUALIZAR_CORREO.ps1). CIERRE tiene aviso propio; incluye solo ID/enlace, nunca texto de resolución. Se coteja closed_at contra el cierre vigente, además de permiso al reclamar y al despachar. No se rellenan cierres históricos. [Auditoría y pasos de verificación](AUDITORIA_2026-10-23.md). El recorrido previo92 no demuestra este tipo nuevo. El recorrido local de cierre se verificó posteriormente en [evidencia204](evidencias/204-correo-cierre-recorrido-local-verificado.json), con [captura206 de Mailpit](evidencias/206-correo-cierre-mailpit.jpg); el panel mostró el aviso Cierre aceptado al primer intento. No acredita entrega externa ni los recorridos negativos pendientes.
