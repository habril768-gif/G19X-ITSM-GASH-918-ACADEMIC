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
| Administración | Usuarios, roles, departamentos, baja lógica y revisión independiente | API y React; departamentos Admin RH verificados en223, matriz restante pendiente |
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


## Departamentos: aceptación Admin RH observada

[223](evidencias/223-departamentos-admin-rh-recorrido-ui.json): D01–D08 conforme en panel integrado; alta ficticia, duplicado rechazado, renombrado, baja/reactivación y baja final; cinco eventos con motivos y persistencia tras actualizar. Estado final inactivo, sin borrar datos ni tocar departamentos usados. [224: historial](evidencias/224-departamentos-admin-rh-historial-final.jpg),[225: duplicado](evidencias/225-departamento-duplicado-rechazado.jpg). A02 verificado; A03 parcial y A04 pendiente según [matriz](ACEPTACION_ENTREGA.md). No implica aceptación integral ni institucional.


### 2026-10-31 — Usuarios: confirmación de recorrido ficticio

[227](evidencias/227-usuario-ficticio-alta-edicion-baja-confirmadas.json): autora confirma alta/listado, nombre revisado, estado Inactiva y acceso rechazado con aviso genérico. A05 parcial: sin comprobación independiente, auditoría o revocación de sesión previa; no atribuir el rechazo solo a la baja sin verificar credenciales previamente. Registro local, sin repetir pruebas ni publicación remota.


### 2026-10-31 — Consolidación de recuperación Docker y controles de departamentos

Propósito: integrar los resultados manuales aportados por la usuaria, sin repetir pruebas ni modificar código. [230](evidencias/230-restauracion-docker-confirmada.json): respaldo `plurione-20261031-092101.dump`, 75624 bytes, SHA256 `A21826DB6F16EBEA761D83B0DB1BD27D89A801E54CAAB5568AC1A0BB0F0F13B0`; pg_restore sin errores reportados, revisión 0008, cantidades y huellas de contenido de todas las tablas public coincidentes. Destino `plurione-restore-c368a6c78bd8` sin red/puertos según comando, luego detenido; origen reanudado y acceso Admin RH confirmado. La salida ps aún mostraba API health: starting; no declarar healthy posterior del API/worker. No se compararon independientemente secuencias, restricciones, índices, vistas, ACL ni roles globales; no es recuperación completa de instalación ni medición de RTO/RPO.

[231](evidencias/231-departamento-motivo-obligatorio-confirmado.json): la usuaria confirma bloqueo del formulario al omitir motivo. [232](evidencias/232-departamento-bloqueo-usuario-activo-confirmado.json): tras reactivar el departamento ficticio y vincular la cuenta ficticia activa, la baja se rechaza con aviso genérico; después confirma que se guardan las bajas de cuenta y departamento. Ambos quedan inactivos según reporte. Bloqueo por incidencias abiertas sigue pendiente por separado. No inferir respuesta HTTP, auditoría, atomicidad SQL ni validación API a partir del formulario o aviso genérico.

Archivos: evidencias 230–232, matriz de aceptación, mantenimiento, QA, bitácora, backlog, entregables, trazabilidad y MVP. Validación documental: JSON reabiertos, enlaces locales comprobados y matriz contrastada con las confirmaciones. Registros 228/229 conservan revocación, correo duplicado y motivo de usuarios; A05 sigue parcial por auditoría/historial. Sin nuevas pruebas de código, publicación remota ni cambios al cumplimiento de RNF-2. Pendientes: A03 incidencias abiertas, negativos por roles, auditoría de usuarios, recuperación integral, custodia y aceptación humana conforme a la matriz.


### 2026-10-31 — Instalación nueva del núcleo comprobada

[255](evidencias/255-instalacion-nueva-nucleo-reinicio.json): proyecto Docker nuevo con configuración QA propia,0usuarios/0casos iniciales, revisión0008, backend/frontend construidos, HTTP/proxy ok, primer Admin, creación/consulta de caso por autora y persistencia tras reiniciar mismos contenedores. Cierre confirmado con volúmenes conservados. Fallo de redes previo conservado en254. No se acredita recuperación integral de datos/roles de instalación anterior, Node nativoWindows literal, perfiles externos o aceptación institucional.


### 2026-10-31 — Recuperación de copia con aplicación y permisos BI

[Evidencia256](evidencias/256-recuperacion-copia-app-permisos-bi.json): respaldo identificado de75624bytes restaurado a otra base del proyecto QA; catálogo14tablas/2vistas/2secuencias/15índices no asociados a restricciones/20restricciones PK-UQ/25FK coincide por nombres/tipos,0restricciones sin validar, secuencias last_value/is_called coincidentes,9usuarios/8casos, revisión0008. API/panel contra copia y check Alembic sin diferencias;30sesiones históricas revocadas solo en copia. Autora confirma login Admin RH y consulta de expediente. Tras reinicio inesperado Windows41/6008, contenedores exited255: comprobación posterior conserva recuentos/revisión/secuencias. Causa del reinicio desconocida; no inferir fallo Docker o memoria a partir de esos registros.

Cuenta BI nueva creada por CLI después de un intento rechazado por longitud; siete comprobaciones reales de permisos: dos vistas permitidas, cinco42501 (lectura/UPDATE/DELETE users y CREATE public/analytics), sin atributos privilegiados. default_transaction_read_only desactivado solo en sesión de prueba para verificar ACL; ROLLBACK por prueba. Fuente: salidas/reporte local y confirmaciones de autora, sin daemon independiente del agente. Cuatro contenedores detenidos y volúmenes conservados al cierre.

Propósito: ampliar recuperación lógica230 e instalación nueva255 hacia uso de copia y reconstrucción acotada de permisos BI. No equivalencia literal de todos los propietarios/ACL/globales, definiciones o filas del origen actual; no proveedores externos/BI Desktop, RTO/RPO o aceptación institucional. Archivos: evidencia256, matriz, resumen, informe, mantenimiento, MVP, bitácora, QA, backlog, entregables, trazabilidad y decisiones. Validación: JSON/reporte, hash del respaldo, resultados de siete ACL y cierre contrastados; auxiliares probados offline/simulados según manifiesto. Credenciales, dump y datos individuales no publicados; registro local pendiente de publicación.
