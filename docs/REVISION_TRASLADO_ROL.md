# Traslado y cambio de rol — revisión del 17 de octubre de 2026

Se consolidan las pruebas manuales ejecutadas por la autora sobre un caso ficticio, con inspección de evidencias 47–57. No se modificó código ni se ejecutaron nuevas pruebas automáticas durante esta revisión. Se conserva API 0.8.0 y esquema 0003.

## Resultados observados

- 47: acuse 201, received=true y can_view=true. El título/afectado se confirman después en 48.
- 48: caso Prueba de traslado de departamento en EN_REVISION, clasificación vigente y supervisor asignado según directorio seleccionado por la autora.
- 49: actualización de usuario 200, sessions_revoked=true y cases_adjusted=1.
- 50: caso permanece EN_REVISION, responsable cambia a RH Independiente Demo y departamento histórico de Operaciones se conserva.
- 51: JSON válido con 4/4 eventos, incluye ASIGNADO/USER_ACCESS_REVIEW con motivo de traslado y responsables anterior/nuevo.
- 52/52b: ID de departamento del empleado coincide con catálogo DEMO - Recursos Humanos. Fragmentos sin código HTTP visible: no atribuirles 200 por sí solos.
- 53: promoción simulada reportada, acuse 200 con revocación y un caso ajustado. El acuse no muestra rol persistido.
- 54: caso confidencial, IA OMITIDA y motivo de gestor involucrado; RH y revisión conservados.
- 55: listado 200 confirma restauración del usuario a EMPLEADO (rol_id=3), activo, en el departamento de destino.
- 56: detalle 200 confirma confidencialidad e IA omitida conservadas después de restaurar rol.
- 57: JSON válido con 5/5 eventos, conserva traslado y añade CAMBIO_CONFIDENCIALIDAD/USER_ACCESS_REVIEW con motivo de promoción y false→true.

## Estado final y límites

Empleado Operaciones Dos Demo queda activo con rol EMPLEADO en DEMO - Recursos Humanos. El caso sigue EN_REVISION, asignado a RH Independiente Demo, confidencial y con IA omitida; mantiene el departamento histórico inicial. No se retira protección automáticamente al restaurar rol. Mantener el estado de prueba es deliberado; no se afirma restitución del departamento original.

Los archivos JSON del historial de caso no son auditoría administrativa completa de usuario: restaurar un rol sin cambiar el caso no genera otro evento de caso, pero la actualización registra su evento de usuario. No se inspeccionó ese evento de usuario en este recorrido. Las capturas de acuse no prueban por sí solas sesiones anteriormente abiertas ni todos los roles; los nombres/roles de responsables se comparan con el directorio y evidencias previas.

Se observaron únicamente datos ficticios y no se encontraron tokens, contraseñas ni encabezados Authorization en las evidencias revisadas. La revisión estructural de JSON no sustituye controles de datos reales. No se acredita concurrencia PostgreSQL ni matriz completa de permisos. Sigue vigente la ejecución previa por la autora de 77 pruebas aprobadas, 3 PostgreSQL omitidas y 1 advertencia, sin repetirla por esta consolidación documental.

## Archivos

- [47-caso-traslado-creado-201.png](evidencias/47-caso-traslado-creado-201.png)
- [48-traslado-en-revision-supervisor-200.png](evidencias/48-traslado-en-revision-supervisor-200.png)
- [49-traslado-usuario-ajuste-casos-200.png](evidencias/49-traslado-usuario-ajuste-casos-200.png)
- [50-caso-reasignado-tras-traslado-200.png](evidencias/50-caso-reasignado-tras-traslado-200.png)
- [51-historial-traslado.json](evidencias/51-historial-traslado.json)
- [52-empleado-departamento-destino.png](evidencias/52-empleado-departamento-destino.png)
- [52b-departamento-destino-catalogo.png](evidencias/52b-departamento-destino-catalogo.png)
- [53-cambio-rol-proteccion-200.png](evidencias/53-cambio-rol-proteccion-200.png)
- [54-caso-protegido-tras-cambio-rol-200.png](evidencias/54-caso-protegido-tras-cambio-rol-200.png)
- [55-rol-empleado-restaurado.png](evidencias/55-rol-empleado-restaurado.png)
- [56-proteccion-conservada-tras-restaurar-rol-200.png](evidencias/56-proteccion-conservada-tras-restaurar-rol-200.png)
- [57-historial-cambio-rol.json](evidencias/57-historial-cambio-rol.json)
