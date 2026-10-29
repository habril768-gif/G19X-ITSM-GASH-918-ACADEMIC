# Guía del panel web

## Acceso y navegación

Inicia API, migraciones y React siguiendo el [README](../README.md). Abre http://127.0.0.1:5173/ con una cuenta provisionada. No hay registro público. La sesión vive en memoria: recargar solicita nuevo acceso. Cerrar sesión limpia los datos locales e intenta revocar el token; si no se confirma el servidor, la interfaz informa la incertidumbre.

El menú muestra Incidencias y Nueva incidencia, y las opciones administrativas según rol. Los botones reflejan permisos, pero la API vuelve a comprobar cada operación. Un enlace de correo con `?incident=UUID` abre el expediente después de autenticar; no concede acceso por conocer su identificador.

## Consultar expedientes

El listado pagina los casos visibles y ofrece filtros por identificador/título, estado, prioridad, categoría, responsable y fechas. El total corresponde al conjunto filtrado autorizado. Abre el título para consultar descripción, ámbito, prioridad, confidencialidad, clasificación y seguimiento. El historial muestra las acciones permitidas; no expone copias completas de auditoría ni credenciales.

## Registrar una incidencia

En Nueva incidencia selecciona el ámbito y completa los hechos simulados:

- PERSONA exige un afectado permitido; un empleado reporta sobre sí mismo.
- ENTORNO exige un departamento permitido y no utiliza un afectado ficticio.
- Los participantes admitidos requieren motivo y no deben duplicarse. La declaración puede restringir el acceso de gestores involucrados.

El acuse confirma el registro. No garantiza que quien reportó conserve acceso al detalle si la protección del expediente lo impide. No uses datos personales reales ni adjuntes credenciales.

## Gestionar el caso

Los gestores autorizados pueden editar, confirmar categoría y prioridad, asignar responsable y ejecutar las transiciones disponibles. Editar los hechos invalida la clasificación anterior: hay que validarla de nuevo. La resolución y el cierre requieren cumplir las reglas de negocio; reapertura inicia otro ciclo conservando auditoría.

Confidencialidad y revisión de participantes corresponden a un Admin RH independiente. Confirmar o descartar una relación exige motivo y conserva la declaración original. Si una operación retira tu acceso, la interfaz debe retirar el expediente; no se trata de un error que deba evitarse eludiendo permisos. Detalle en [INCIDENCIAS.md](INCIDENCIAS.md).

## Asistencia IA y correo

El formulario IA empieza vacío y requiere texto simulado revisado y confirmaciones explícitas. Solicitar asistencia registra un trabajo; Actualizar asistencia consulta su seguimiento. Una respuesta completada sigue pendiente de validación humana: no confirma los campos oficiales. Si está omitida o falla, continúa la gestión manual. Consulta [IA.md](IA.md).

Admin RH autorizado puede consultar Notificaciones por correo y actualizar su estado. «Aceptada por SMTP» no confirma recepción externa ni lectura. Los mensajes de prueba se consultan en Mailpit. Consulta [CORREO.md](CORREO.md).

## Cuentas y departamentos

Admin RH dispone de gestión de usuarios y departamentos. Los cambios de rol, departamento o activación pueden revocar sesiones y ajustar casos; requieren revisar el resultado y el motivo. La baja de departamentos es lógica y está protegida. Guías: [usuarios](ADMIN_USUARIOS.md) y [departamentos](DEPARTAMENTOS.md).

Cambiar contraseña está disponible en la cabecera para todos los roles. Solicita actual, nueva y confirmación. Al guardar, vuelve al login y exige la nueva contraseña; no conserva los campos ni reenvía una escritura cuyo resultado sea incierto.

## Verificación y límites

Las pruebas de componentes y el build se ejecutan desde `frontend/` con `npm.cmd test` y `npm.cmd run build`. Las evidencias registran recorridos de acceso, registro, gestión, administración, IA y correo con sus límites. Falta completar la matriz de roles y la revisión de escritorio/móvil/accesibilidad; no se declara auditoría WCAG ni aceptación integral. Consulta [QA](REPORTE_QA.md).

El servidor Vite es de desarrollo y escucha en loopback con puerto estricto. Su proxy apunta a la API local; cambiar API_PORT exige ajustar `vite.config.js`. Nunca guardes claves en variables VITE_. Publicar el build requiere un servidor y HTTPS preparados por separado.
