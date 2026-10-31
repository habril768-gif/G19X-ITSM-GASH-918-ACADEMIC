# Estado para revisión de entrega

Actualizado: 31 de octubre de 2026. Proyecto académico PluriOne.

Este resumen reúne resultados y pendientes; no es un acta de aceptación institucional ni una certificación de producción. La [matriz de aceptación](ACEPTACION_ENTREGA.md) conserva el detalle y la procedencia de cada comprobación.

## Implementación y resultados comprobados

| Área | Resultado y alcance | Evidencia |
| --- | --- | --- |
| Panel web | React disponible: acceso por cuentas, incidencias, gestión RH, usuarios y departamentos. Controles ocultos reportados; GET administrativos de usuarios/opciones/departamentos rechazados con403 en dos sesiones de roles verificados, según salidas de la autora ([240](evidencias/240-rechazos-api-supervisor-empleado-confirmados.json)); ampliado a historial y POST/PUT vacíos en [241](evidencias/241-rechazos-administrativos-ampliados.json), ocho403 por rol; no se probaron cuerpos válidos de escritura | [Manual](MANUAL_USUARIO.md), [roles226](evidencias/226-visibilidad-administracion-supervisor-empleado-confirmada.json) |
| Rendimiento RNF-2 | Formal HTTP QA local aprobada: tres procesos API, diez clientes, cien casos iniciales, 30 s de calentamiento y 300 s de medición. 35216 solicitudes sin errores; p95 listado123.81, detalle113.27, creación194.04 y actualización167.77 ms. No garantiza todos los equipos ni todas las solicitudes por debajo de200 ms | [220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json) |
| Usuarios | Alta/edición/baja reportadas; revocación funcional de sesión confirmada por autora; rechazo de correo repetido y motivo vacío | [227](evidencias/227-usuario-ficticio-alta-edicion-baja-confirmadas.json), [228](evidencias/228-revocacion-sesion-usuario-confirmada.json), [229](evidencias/229-usuarios-duplicado-motivo-confirmados.json) |
| Conservación y auditoría de usuario | Autora confirma conservación de un expediente tras la baja. Consulta READ ONLY aportada muestra11 eventos administrativos y cambios de activación con motivos. Bandera de revocación no es un recuento de sesiones | [238](evidencias/238-expediente-conservado-tras-baja-usuario.json), [239](evidencias/239-auditoria-usuario-ficticio-consulta-lectura.json) |
| Departamentos | Recorrido Admin RH observado: alta, edición, baja/reactivación e historial. Motivo obligatorio y bloqueos con dependencias reportados por autora; aviso genérico no prueba causa exclusiva | [223](evidencias/223-departamentos-admin-rh-recorrido-ui.json), [231](evidencias/231-departamento-motivo-obligatorio-confirmado.json), [232](evidencias/232-departamento-bloqueo-usuario-activo-confirmado.json), [233](evidencias/233-departamento-incidencia-pendiente-confirmado.json) |
| Privacidad de expediente ajeno | Empleado Operaciones2 obtiene404 en detalle, historial y participantes del caso ficticio previamente consultado por RH; logout204. Control Admin RH posterior obtiene200 en esas tres rutas ([243](evidencias/243-control-admin-expediente-200.json)); sesiones sucesivas, alcance de un caso sin matriz integral | [242](evidencias/242-empleado-expediente-ajeno-404.json) |
| Correo RF-5 | Recorrido básico local con Mailpit por creación, asignación, resolución y cierre. No acredita buzones externos ni todos los fallos/reintentos | [204](evidencias/204-correo-cierre-recorrido-local-verificado.json) |
| Respaldo y reanudación | Restauración lógica Docker reportada sin errores, revisión0008, filas/huellas de tablas public coincidentes; ensayo detenido, origen reanudado, acceso Admin RH y health/db ok. No es recuperación integral de infraestructura | [230](evidencias/230-restauracion-docker-confirmada.json), [234](evidencias/234-salud-posterior-reanudacion-docker.json) |
| Custodia del respaldo | Autora responsable; carpeta RespaldosPluriOne de su computadora; conservación hasta concluir evaluación y atender observaciones finales. Sin eliminación automática acordada | [235](evidencias/235-custodia-respaldo-confirmada.json), [236](evidencias/236-conservacion-respaldo-acordada.json) |

## Pendientes para decidir la entrega

1. Revisar con quien evalúa los criterios de aceptación académica y registrar el resultado real. No hay aprobación institucional ni capacitación acreditadas por este resumen.
2. Completar los supuestos de la matriz que requiera esa aceptación: negativas API adicionales con cuerpos válidos/recursos existentes no cubiertas por240/241, combinaciones de confidencialidad/conflictos, cambios de rol/departamento y concurrencia. Las pruebas automatizadas existentes y los recorridos manuales tienen alcances distintos.
3. Si se exige recuperación de instalación completa, comprobar por separado configuración privada, roles/ACL, secuencias y arranque sobre la copia. La prueba lógica aprobada no cubre todos esos elementos.
4. Definir disposición posterior del respaldo y decisiones de custodia de exportaciones analíticas. No se comprobó copia adicional o acceso restringido de la carpeta.
5. Si se requiere correo externo, comprobar configuración y entrega en ese entorno. Mailpit solo acredita captura local.

Estas actividades no se convierten automáticamente en nuevos requisitos de producto: su necesidad de cierre se contrasta con el [PRD](PRD.md), el [MVP](MVP.md) y la rúbrica aplicable. No se asigna un porcentaje medido de avance sin pesos acordados.

## Preparar la demostración

- Usar datos ficticios y cuentas por rol; introducir credenciales solo en el sitio.
- Mostrar el panel y un expediente permitido, los controles RH y la evidencia de sus restricciones. Conservar los expedientes de aceptación anteriores.
- Presentar RNF-2 con su reporte y límites; no repetir carga formal únicamente para generar una demostración.
- Mostrar [manual técnico](MANUAL_TECNICO.md), [manual de usuario](MANUAL_USUARIO.md), [mantenimiento](PLAN_MANTENIMIENTO.md) y matriz de aceptación.
- Mantener fuera de Git las credenciales y el respaldo binario.

## Publicación

Última publicación comprobada al preparar este resumen: [9e1d77a](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/commit/9e1d77a83f450d2dccf5e47643acba0fa8e327ea), que corrige el README. Esta revisión agrupa las evidencias238/239 y el resumen para publicación. Para comprobar la versión remota, consultar el historial de GitHub; esta preparación no se presenta como aprobación institucional. No se atribuyen nuevas ejecuciones CI a este cambio documental.


Actualización local: evidencia240 incorpora los rechazos de lectura de Supervisor/Empleado; pendiente de publicación posterior al commit789f8ba.


Actualización local241: historial y solicitudes administrativas POST/PUT vacías rechazadas403 en ambos roles; no cubre todos los cuerpos válidos de escritura. Pendiente de publicación.


Actualización local242: tres404 reportados para otro Empleado sobre expediente ficticio, historial y participantes. Pendiente de publicación.


Actualización local243: control positivo Admin RH con tres200 y cierre204, posterior a los tres404 de Empleado242; pendiente de publicación conjunta.
