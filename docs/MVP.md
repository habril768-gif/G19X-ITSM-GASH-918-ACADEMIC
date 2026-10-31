# Alcance y aceptación del MVP

## RNF-2: cumplido en QA local — 30 de octubre de 2026

[Primera formal aprobada220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json):10 clientes,100 casos iniciales,30+300s,API de 3 procesos,35.216 solicitudes sin errores. P95 listado123,81/detalle113,27/creación194,04/actualización167,77ms, todos<200 ms; auditoría/colas/logout/parada correctos. Acredita este alcance HTTP Docker local y hardware declarado, no rendimiento universal ni proveedores externos. Diez fallos históricos se conservan. [Perfil opcional 221](evidencias/221-perfil-compose-rnf2-reproducible.json) y [protocolo](PRUEBA_RENDIMIENTO.md) permiten reproducir configuración/medición. Los demás pendientes de entrega siguen vigentes.


## Objetivo

Gestionar incidencias laborales simuladas desde su registro hasta su seguimiento y cierre, con permisos por rol, revisión humana, auditoría y protección de información. Este documento describe la entrega actual; las reglas detalladas están en el [PRD](PRD.md).

## Funciones implementadas

| Área | Comportamiento disponible | Evidencia y límite |
| --- | --- | --- |
| Identidad | Acceso local, sesiones revocables, cambio de contraseña y bloqueo de intentos | Pruebas y recorridos registrados; matriz completa pendiente |
| Expedientes | Registro PERSONA/ENTORNO, consulta con filtros, edición y clasificación humana | Panel y servicios implementados; no basta para aceptar todos los roles |
| Gestión y protección | Responsable, revisión, resolución, cierre, reapertura, participantes y confidencialidad | Auditoría y pruebas de permisos/transacciones; faltan escenarios integrales |
| Administración | Usuarios, roles, departamentos, baja lógica y revisión independiente | API y React; recorrido completo adicional pendiente |
| IA | Texto simulado revisado, trabajo durable y sugerencia separada de decisión oficial | Último conjunto: prioridad 50/50, categoría 47/50 y abstenciones 5/5; tres diferencias de categoría conservadas. No garantiza casos nuevos |
| Correo | Avisos de creación, asignación, resolución y reapertura; seguimiento de intentos | Mailpit y panel verificados en evidencias 85–92; fallos/exclusiones reales adicionales pendientes |
| Analítica | Agregados con exclusiones, supresión y cuenta de lectura; informe Power BI guardado | SQL/conexión y visuales 93–95/98; modelo 104, refresco principal 105 y QA visual/retirada Desktop 106. SQL→JSON→Desktop aislado verificado en 108–109; quedan conector directo aislado si se exige, custodia y aceptación integral |

## Condiciones para dar la entrega por terminada

1. Completar y registrar la matriz de aceptación por rol, incluidos accesos rechazados, confidencialidad, participantes y cambios concurrentes.
2. Verificar recorridos pendientes de administración, experiencia móvil y notificaciones negativas sin exponer información.
3. Completar custodia/retirada de copias y aceptación de analítica. Modelo/refresco/QA 104–106 y SQL→JSON→Desktop 108–109 verificados sin reducir supresión. El puente JSON no acredita el conector directo contra PostgreSQL aislado; probarlo aparte si se exige.
4. Validar el [manual de usuario](MANUAL_USUARIO.md) y ejecutar el [plan de mantenimiento/recuperación](PLAN_MANTENIMIENTO.md); el ensayo lógico nativo y la cuenta BI reconstruida están verificados en 103; falta la recuperación de instalación completa y la secuencia Docker. Completar el reporte final de QA. La [propuesta](PROPUESTA_TECNICA.md) y la [arquitectura](ARQUITECTURA.md) ya están documentadas; sus límites operativos deben comprobarse antes de aceptación.
5. Registrar capacitación y aceptación solo cuando ocurran; cerrar el informe académico con evidencias reales.

La fecha límite y las horas disponibles no han sido confirmadas. No se asigna un porcentaje global ni una fecha de cierre sin acordar alcance, ponderación y evidencias. El [backlog](BACKLOG.md) fija el orden de trabajo.

## Fuera del alcance actual

Entra ID, nómina, SLA y alertas por tiempo, aplicación móvil nativa, registro público, recuperación automática por correo y despliegue productivo con datos reales. Mailpit no envía a buzones externos; el informe Power BI no representa toda la empresa.

## Cómo leer las evidencias

La [trazabilidad](TRAZABILIDAD.md) relaciona requisitos con implementación y validación. El [reporte QA](REPORTE_QA.md) distingue ejecución automática, recorrido manual y revisión estática. Una captura, una evaluación de código o una calificación orientativa no sustituyen la aceptación integral.


## Continuación de la entrega: matriz por roles

La [matriz de aceptación](ACEPTACION_ENTREGA.md) reúne14escenarios con origen/alcance de evidencia y pendientes. [Preparación222](evidencias/222-matriz-aceptacion-entrega-preparada.json): siguiente recorrido de departamentos conAdminRH,8pasos previstos y ninguna escritura ejecutada. RNF-2 aprobado220 se conserva; un plan no es aceptación real. Ver comandos de arranque con3procesos/Mailpit y registro de resultados en la matriz.
