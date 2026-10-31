# Informe de desarrollo y resultados de PluriOne

**Borrador para revisión académica — 31 de octubre de 2026**

Proyecto: Desarrollo de una Plataforma Inteligente de Gestión de Incidencias Laborales. Clave: G19X-ITSM-GASH-918-ACADEMIC. Autoría y requisitos de identificación: [PRD](PRD.md). Este documento todavía requiere ajuste al formato institucional y aceptación correspondiente; no acredita trabajo de campo, capacitación ni aprobación que no se hayan registrado.

## Resumen

Se desarrolló una plataforma local de gestión de incidencias con cuentas por rol, seguimiento de expedientes, auditoría de cambios, asistencia de clasificación mediante IA, avisos de correo y analítica agregada. La solución integra React, FastAPI, PostgreSQL, Redis, workers de IA y correo, Docker Compose y Power BI Desktop. La validación combina pruebas automatizadas, ensayos aislados y recorridos de la autora; cada evidencia conserva su procedencia y límites. El desempeño HTTP RNF-2 fue aprobado en el entorno QA documentado. La entrega integral y la operación productiva no se consideran aprobadas por este informe.

## Problema y objetivo

El proyecto organiza el registro y seguimiento de situaciones laborales mediante un expediente con estados y acceso restringido. El objetivo implementado es disponer de un núcleo que permita registrar, consultar y gestionar incidencias según rol, departamento, confidencialidad y participación, conservando el historial y apoyando la revisión humana. Las necesidades y reglas se describen en el [PRD](PRD.md); no se presentan entrevistas, diagnósticos de campo o impactos empresariales medidos que no estén acreditados.

## Alcance desarrollado

- Acceso local con contraseñas privadas, sesiones revocables y perfiles Admin RH, Supervisor y Empleado.
- Registro y consulta de incidencias, clasificación oficial humana, asignación y ciclo de revisión, resolución, cierre y reapertura conforme a permisos.
- Administración de cuentas y departamentos, motivos de cambios, baja lógica y controles de dependencias.
- Auditoría de expedientes y cambios administrativos. El historial de departamentos existe en pantalla; la auditoría administrativa de usuarios se consulta internamente por el operador.
- Asistencia IA como sugerencia revisable, sin sustituir decisión humana; integración opcional con credenciales propias.
- Outbox de correo con worker y captura local Mailpit. Los ensayos locales no acreditan entrega a buzones externos.
- Analítica agregada con exclusiones y supresión por privacidad; los valores suprimidos permanecen vacíos y no representan cero.

El [MVP](MVP.md) y la [matriz de aceptación](ACEPTACION_ENTREGA.md) delimitan los escenarios pendientes y las condiciones de cierre.

## Diseño e implementación

El panel React consulta la API FastAPI. El servidor verifica identidad y permisos por solicitud y aplica las reglas del expediente antes de acceder a datos o confirmar cambios. PostgreSQL conserva entidades, sesiones, trabajos y eventos; Alembic versiona el esquema. Las operaciones externas de IA/correo se procesan mediante workers para separar el trabajo externo del acuse HTTP. Power BI utiliza vistas agregadas mediante una cuenta de lectura separada.

La [arquitectura](ARQUITECTURA.md), las [decisiones](DECISIONES.md) y el [manual técnico](MANUAL_TECNICO.md) contienen los detalles. No se deduce alta disponibilidad, HTTPS externo, MFA o preparación productiva a partir del despliegue local.

## Validación y resultados

| Área | Resultado comprobado | Evidencia y límite |
| --- | --- | --- |
| Rendimiento RNF-2 | 35216 solicitudes sin errores con10 clientes,100 casos iniciales,30 s de calentamiento y300 s de medición; API3procesos. P95 listado123.81, detalle113.27, creación194.04 y actualización167.77ms, cada uno menor de200ms | [220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json). Un entorno/hardware/protocolo; no latencia universal, p99 o proveedores externos |
| Permisos administrativos | Supervisor y Empleado obtuvieron403 en lecturas e historial, e intentos POST/PUT vacíos; logout204 | [240](evidencias/240-rechazos-api-supervisor-empleado-confirmados.json), [241](evidencias/241-rechazos-administrativos-ampliados.json). No todos los cuerpos válidos o recursos existentes |
| Privacidad del expediente | Otro Empleado obtiene404 en detalle/historial/participantes; Admin RH obtiene200 en control posterior | [242](evidencias/242-empleado-expediente-ajeno-404.json), [243](evidencias/243-control-admin-expediente-200.json). Dos cuentas y un caso, sesiones sucesivas |
| Usuarios y departamentos | Recorridos de alta/edición/baja, revocación, validaciones y dependencias documentados; consulta de11 eventos administrativos del usuario ficticio | [Resumen](RESUMEN_ENTREGA.md), [239](evidencias/239-auditoria-usuario-ficticio-consulta-lectura.json). Confirmaciones/capturas y consulta aportada, no matriz integral de todas las combinaciones |
| Correo y navegación | Captura Mailpit de aviso genérico con enlace; destino muestra el expediente correcto en Admin RH | [248](evidencias/248-ensayo-mailpit-aviso-generico.json), [251](evidencias/251-enlace-mailpit-expediente-confirmado.json). Sin correo externo ni comprobador automático de enlaces acreditado |
| Respaldo | Restauración lógica Docker sin error reportado, revisión0008 y filas/huellas de tablas public coincidentes; origen reanudado y health/db ok | [230](evidencias/230-restauracion-docker-confirmada.json), [234](evidencias/234-salud-posterior-reanudacion-docker.json). No recuperación integral de roles/ACL/secuencias/infraestructura |
| Instalación nueva | Núcleo y frontend construidos en proyecto QA separado, base vacía, migraciones0008, primer Admin, creación/consulta UI de caso y persistencia tras stop/start; servicios propios detenidos con datos conservados | [255](evidencias/255-instalacion-nueva-nucleo-reinicio.json). Configuración QA generada; no instalación NodeWindows literal ni restauración de datos/roles de la instalación anterior. Fallo inicial de redes conservado en [254](evidencias/254-instalacion-nueva-bloqueada-redes.json) |
| Analítica | Power BI refrescado y guardado con corte31/10/2026 02:47:05p.m.; cuatro filas suprimidas, leyenda conservada y API→PostgreSQL ok | [253](evidencias/253-powerbi-refresco-guardado-20261031.json). Identidad SQL efectiva y medidas de esta ejecución no inspeccionadas |
| Clasificación IA | Evaluación v4 registrada: categoría47/50, prioridad50/50 y cinco abstenciones correctas | [Resultados v4](evaluacion_ia/RESULTADOS_V4.md). Conjunto simulado, tres errores de categoría del mismo patrón; aceptación humana integral pendiente |

Los ensayos fallidos de rendimiento y los límites de cada validación se conservan. Las pruebas simuladas no se presentan como sesiones reales; las confirmaciones de la autora no se convierten en observación directa del agente. No se repitieron cargas o llamadas externas para redactar este informe.

## Operación, respaldo y custodia

El [README](../README.md) explica la configuración y el arranque. Los [manuales de usuario](MANUAL_USUARIO.md) y [técnico](MANUAL_TECNICO.md) describen uso y operación. El [plan de mantenimiento](PLAN_MANTENIMIENTO.md) contiene copia y restauración aislada. La autora asumió la custodia del respaldo local en RespaldosPluriOne de su computadora y conservarlo hasta concluir evaluación y atender observaciones finales ([235](evidencias/235-custodia-respaldo-confirmada.json), [236](evidencias/236-conservacion-respaldo-acordada.json)). La disposición posterior sigue pendiente; no se programa eliminación automática. No se publican credenciales, respaldo binario o capturas con identidad personal.

## Limitaciones y trabajo pendiente

Se requiere contrastar la rúbrica institucional y registrar la aceptación real. La instalación nueva acotada está documentada en255; no sustituye recuperación integral de una instalación anterior. Siguen pendientes, según el alcance que se exija, combinaciones adicionales de permisos/conflictos/concurrencia, recuperación integral, fallos y reintentos externos, custodia de copias analíticas y capacitación. Los controles locales y los casos simulados no prueban impacto organizacional ni sustituyen una evaluación con usuarios autorizados en un contexto real. No se asigna una calificación o porcentaje medido sin criterios acordados.

## Conclusiones y aprendizajes

La implementación y sus evidencias permiten revisar un flujo local desde registro hasta seguimiento, administración y analítica, con decisiones humanas y restricciones de acceso. El resultado formal de rendimiento corresponde al protocolo declarado y fue alcanzado después de fallos documentados. Como aprendizaje técnico, la aceptación funcional, los permisos del servidor, el desempeño y la recuperación deben comprobarse por separado: un botón oculto, un correo capturado o un archivo de respaldo existente no acreditan por sí solos esos aspectos.

## Material de revisión

- [Resumen y demostración](RESUMEN_ENTREGA.md).
- [Matriz de aceptación](ACEPTACION_ENTREGA.md) y [trazabilidad](TRAZABILIDAD.md).
- [Reporte QA](REPORTE_QA.md) y [bitácora](BITACORA.md).
- [Repositorio](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC).

El borrador no incluye firmas, actas, entrevistas o capacitaciones ficticias. Fecha de entrega, formato final y aprobación institucional permanecen por confirmar.
