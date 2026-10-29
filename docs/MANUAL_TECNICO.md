# Manual técnico de PluriOne

## Arquitectura implementada

El navegador ejecuta React y envía solicitudes al proxy de desarrollo, que las dirige a FastAPI. Las rutas validan sesión, rol y acceso al expediente; los servicios realizan las operaciones y su auditoría en PostgreSQL. SQLAlchemy representa el esquema y Alembic aplica sus cambios.

La asistencia IA utiliza trabajos durables en PostgreSQL y avisos Redis. Un worker procesa solicitudes elegibles con LangChain/OpenAI; el resultado queda como sugerencia y no valida la clasificación oficial. Otro worker procesa la outbox de correo mediante SMTP; Mailpit captura los envíos de desarrollo. Power BI usa una cuenta de lectura sobre dos vistas agregadas, sin consultar expedientes individuales.

Esta descripción refleja el sistema local. La [propuesta técnica](PROPUESTA_TECNICA.md) y la [arquitectura](ARQUITECTURA.md) detallan objetivos, componentes, flujos y decisiones; su elaboración no acredita aceptación productiva.

## Instalar y actualizar

El [README principal](../README.md#arranque-local-en-cinco-pasos) contiene el procedimiento de instalación. Para actualizar una instalación existente, conserva `.env`, los volúmenes y las cuentas. Reconstruye las imágenes afectadas, aplica `alembic upgrade head`, verifica `alembic check` y reinicia los componentes coordinadamente. No repitas bootstrap ni seed.

Usa [Docker](../infra/README.md) para el núcleo y las guías [IA](IA.md), [correo](CORREO.md) y [analítica](ANALITICA.md) para activar perfiles u overrides. La aplicación no carga `.env` directamente; Compose suministra variables. La clave del proveedor solo se entrega al worker IA.

## Acceso y seguridad

- Contraseñas Argon2id y sesiones opacas revocables, con vencimiento y bloqueo temporal tras intentos fallidos.
- Token del panel en memoria; no se persiste en LocalStorage. El servidor vuelve a comprobar usuario, departamento y permisos.
- Visibilidad por objeto, confidencialidad y revisión independiente de participantes. Los controles del navegador no sustituyen los del servidor.
- Historial y cambios de negocio transaccionales; errores SQL revierten la operación y responden sin exponer credenciales.
- Analítica con exclusión de casos restringidos, supresión de celdas pequeñas y acceso limitado a vistas.

El entorno local no implementa por sí solo HTTPS externo, MFA ni límite global por IP. Antes de uso productivo se requiere una preparación adicional y aceptación expresa con evidencia.

## Operación por componente

| Componente | Verificación | Guía |
| --- | --- | --- |
| API | `/health` HTTP; `/health/db` conexión y esquema; contrato `/openapi.json` | [Backend](../backend/README.md) |
| PostgreSQL | Estado Compose, revisión actual y `alembic check` | [Datos](DATOS.md) |
| Redis | `docker compose exec redis redis-cli ping` devuelve PONG | [Docker](../infra/README.md) |
| Panel | Acceso y recorrido según rol; build no sustituye pruebas reales | [Frontend](FRONTEND.md) |
| IA | Elegibilidad, trabajo, intentos y sugerencia separada de decisión humana | [IA](IA.md) |
| Correo | Estado de la outbox y captura Mailpit; SMTP aceptado no confirma lectura | [Correo](CORREO.md) |
| Power BI | Cuenta de lectura, corte, población parcial y privacidad | [Analítica](ANALITICA.md) |

## Diagnóstico

Si `/health` falla, revisa el estado del contenedor y el puerto. Si responde pero `/health/db` devuelve 503, revisa conexión y migraciones. Un error de contraseña después de editar `.env` puede deberse a un volumen ya inicializado; no borres la base para resolverlo.

Si el panel no conecta, confirma que el proxy de `frontend/vite.config.js` apunta al puerto API vigente. Si una operación es rechazada, revisa sesión, rol, estado del caso y clasificación humana vigente antes de reintentar. No relajes permisos para pasar una prueba.

IA y correo requieren sus workers; un proceso API sano no acredita que se estén procesando trabajos. En Power BI, números vacíos con «Suprimido por privacidad» son el comportamiento previsto: no conviertas NULL en cero ni reduzcas el mínimo para obtener gráficos.

## Pruebas y evidencia

Usa [pruebas PostgreSQL aisladas](PRUEBAS_POSTGRESQL.md) para evitar tocar datos operativos. El [reporte QA](REPORTE_QA.md) registra resultados y limitaciones; la [trazabilidad](TRAZABILIDAD.md) muestra el cierre pendiente por requisito. No se ejecutan evaluaciones de pago como parte del arranque ni por un cambio documental.

## Conservación y soporte

`docker compose stop` detiene los servicios sin eliminar los volúmenes. No uses `down --volumes` sobre datos que deban conservarse. Un volumen persistente no es un respaldo: el [plan de mantenimiento](PLAN_MANTENIMIENTO.md) prepara copia, ensayo aislado y soporte; el ensayo lógico nativo ya pasó (103), mientras la secuencia Docker, instalación completa y retención/custodia siguen pendientes. Las copias de Power BI requieren custodia propia; retirar permisos de origen no revoca una copia ya distribuida.

Consulta [MVP](MVP.md), [backlog](BACKLOG.md) y [entregables](ENTREGABLES.md) antes de declarar terminado o desplegar el sistema.

## Actualización de correo y esquema vigente

La versión que añade correo de cierre requiere Alembic0008. Usa `scripts/ACTUALIZAR_CORREO.ps1`: construye, migra con `upgrade head` y actualiza API/worker sin borrar datos. `/health/db` exige la nueva revisión. La migración amplía un CHECK; no genera avisos retrospectivos. Pool base: cinco conexiones retenidas y diez temporales por proceso, máximo quince, pre_ping activo, espera30s y conexión3s. No hay ajuste nuevo de rendimiento en esta revisión. Ver [respuesta de auditoría](AUDITORIA_2026-10-23.md).
