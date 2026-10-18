# Panel React — primera entrega (0.1.0)

Implementado el 17 de octubre de 2026, conectado a la API 0.8.0 existente. Incluye login, listado paginado con filtros, detalle e historial de lectura. RF-8 parcial: todavía no hay formulario de registro, validación/asignación/transiciones ni administración de usuarios en pantalla. Las operaciones de escritura siguen disponibles en Swagger. No se presenta el frontend como MVP completo.

## Inicio local

Desde la raíz del proyecto mantener Docker Desktop abierto y servicios activos con docker compose up -d --wait. Para el frontend:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

Abrir http://127.0.0.1:5173/. Node 24 fue usado para verificar esta entrega. Versiones fijadas en package.json y package-lock.json: React/React DOM 19.3.1, Vite 8.3.4, plugin React 6.1.2, Vitest 5.0.5, jsdom 29.1.1. Guía de Vite consultada: https://vite.dev/guide/ . En Windows se usa npm.cmd para evitar restricciones de npm.ps1.

El servidor escucha solo en 127.0.0.1:5173, con puerto estricto: si está ocupado falla en vez de cambiar de dirección. Vite reenvía /api a 127.0.0.1:8000, sin modificar CORS del backend ni introducir claves en el navegador. No necesita .env frontend. Nunca copiar contraseñas, claves OpenAI ni POSTGRES_PASSWORD a variables VITE_. No editar el .env del backend para iniciar la interfaz.

Si el proceso iniciado por el asistente termina, volver a ejecutar npm.cmd run dev en la carpeta frontend. La terminal debe permanecer abierta. npm run build genera dist ignorado por Git; no despliega. Publicar requiere proxy /api, HTTPS y configuración de servidor aprobada: Vite dev no constituye despliegue productivo.

## Uso

Iniciar sesión con una cuenta local ya provisionada y su contraseña. No hay registro público ni contraseña compartida. Tras entrar se consultan solo incidencias autorizadas por la API. Total corresponde a la consulta filtrada autorizada, no a un total global. Paginación de 20. Filtros: ID/título, estado, prioridad, categoría, responsable y fechas de creación UTC. El rango se valida antes de enviar. Categorías/directorio mínimo provienen de /incidents/options.

Abrir un título para consultar descripción, ámbito, prioridad, acceso, validación, responsable (ID), resolución y eventos. Historial paginado por API; se muestran acciones/fechas y motivo cuando está permitido. No se exponen copias completas de detalle de auditoría en esta vista. La ausencia de acción de creación en pantalla no afecta las rutas API existentes. IA pendiente/omitida/fallida se comunica como estado; no se invoca IA desde el frontend.

El token vive solo en memoria de la instancia de cliente. No localStorage, sessionStorage, URL ni cookies. Recargar la página exige nuevo login. Logout intenta revocar en API y limpia identidad/detalle/listados inmediatamente; si no se confirma servidor se informa que puede seguir vigente hasta expiración. 401/403 de la sesión retiran datos y vuelven a login. Una respuesta tardía de una sesión anterior no elimina la nueva. Fetch con cache no-store, AbortController y comprobación de respuesta vigente evitan recuperar listas anteriores tras navegar. Ante 404 del historial se retira el detalle; nunca se sustituyen controles API con botones. No se usan HTML del usuario ni renderizado sin escape.

Accesibilidad básica: campos etiquetados, formularios con teclado, foco visible, mensajes de error alert/carga status y tablas con encabezados; estilos adaptables a móvil. No se declara auditoría WCAG ni revisión visual exhaustiva. La vista de detalle interna no implementa enlaces profundos persistentes todavía.

## Verificación realizada

- npm test: 9 pruebas en 2 archivos aprobadas, 17.97s. UI en jsdom con fetch simulado; no acredita login real, navegador completo ni matriz de permisos del servidor.
- npm run build: compilación correcta con Vite 8.3.4 (17 módulos, 442ms en ejecución final).
- HTTP real: / en puerto 5173 devuelve 200 y /api/health devuelve status=ok/service=plurione-api a través del proxy.
- Instalación: npm reportó 0 vulnerabilidades en 94 paquetes al instalar; no sustituye una auditoría futura.
- CI frontend preparado con npm ci/test/build; ejecución remota no observada todavía.
- No se ejecutó otra vez el backend: la evidencia previa de 77 aprobadas/3 PostgreSQL omitidas/1 advertencia permanece separada.

Primera instalación encontró error de certificado; se completó con NODE_OPTIONS=--use-system-ca limitado al proceso de instalación, usando certificados del sistema y manteniendo TLS. No se modificó configuración persistente ni se desactivó verificación de certificados. Se conserva lockfile reproducible.

## Verificación manual pendiente

Abrir login, iniciar sesión con Admin RH, comprobar listado, filtrar y abrir un caso. Cerrar sesión y comprobar que no queda información privada; repetir con empleado/supervisor habilitado. Validar visualmente escritorio/móvil y recorrido con API real. No guardar contraseña/token en capturas. Evidencia prevista 58-panel-react-incidencias.png: únicamente área del listado con datos simulados, evitando identidad real y cualquier consola de red. La apertura del navegador por el asistente no acredita estas pruebas.
Validación manual inicial: evidencia 58 revisada el 17 de octubre de 2026 confirma panel/listado con 2 casos simulados y estado de acceso. No equivale a todos los pasos del plan manual; detalle, filtros, cierre de sesión y vista móvil siguen pendientes.

Detalle manual: evidencia 59 revisada el 17 de octubre de 2026 muestra descripción, restricción, validación, IA omitida y fragmento de historial. No acredita historial completo ni otros roles. Responsable se presenta como UUID en esta primera entrega.

Filtro manual: evidencia 60 revisada el 17 de octubre de 2026 muestra búsqueda Ausencia simulada con una fila y contador 1. Otros filtros y roles no se consideran verificados por esa imagen.

Logout manual: evidencia 61 revisada el 17 de octubre de 2026 muestra login vacío con aviso de cierre y sin expedientes. Recorrido inicial 58–61 completo; no sustituye prueba de revocación de servidor ni revisión móvil/otros roles.

## Registro desde React — versión 0.2.0 (17 de octubre de 2026)

Esta ampliación sustituye el pendiente de formulario de alta de la entrega 0.1.0. Disponible en el menú Nueva incidencia. No necesita dependencias nuevas, migración ni cambios al backend. Con Vite activo, actualizar la página; al recargar se solicita nueva sesión porque token solo vive en memoria.

- PERSONA: empleado reporta sobre sí mismo; gestor elige afectado del directorio permitido por /incidents/options.
- ENTORNO: exige departamento permitido y no envía empleado ficticio. El empleado no incorpora participantes en ENTORNO; gestores pueden declarar según contrato API.
- Participantes opcionales con motivo obligatorio, sin duplicados ni afectado repetido, máximo 20. Empleado solo los declara en caso personal.
- Al solicitar confidencialidad o detectar gestor involucrado se muestra aviso y confirmación de comprensión. Aviso general siempre visible porque permisos pueden cambiar entre cargar opciones y registrar. El servidor mantiene la decisión definitiva.
- No se acepta en formulario autor, estado, asignación ni decisión IA. Fecha local inicial editable; título/descripción y motivos se validan también por servidor.
- Acuse con ID: can_view=true permite abrir detalle; can_view=false ofrece solo referencia y regreso al listado, sin estado posterior ni enlace al expediente.
- Se bloquea envío mientras está pendiente y se conserva el formulario ante errores de validación. Una respuesta de red/servidor no confirmada no se reintenta automáticamente: se indica comprobar el listado/RH para evitar duplicados. No hay idempotencia ni garantía de entrega exactamente una vez del backend; el bloqueo cubre interacción local del formulario.
- No hay persistencia de borradores ni envío a OpenAI. La descripción/relaciones se retiran del formulario al recibir acuse; sesión expirada desmonta la vista como el resto del panel.

Pruebas finales: npm test, 15 aprobadas en 3 archivos, 17.63s; npm run build, 18 módulos y compilación correcta en 379ms. Seis pruebas nuevas de formulario usan API simulada: persona propia, entorno sin víctima, acuse restringido, relación de gestor y aviso, respuesta incierta y bloqueo de doble clic en respuesta pendiente. Nueve pruebas anteriores regresaron sin fallo. No acredita creación real en PostgreSQL ni todo el control entre roles; autorización sigue respaldada por pruebas del backend y necesita recorrido manual de alta desde UI.

Verificación manual agrupada: iniciar sesión como RH; Nueva incidencia; elegir Empleado RH Demo, introducir título/fecha/descripción simulados y registrar sin confidencialidad ni participantes. Confirmar acuse y abrir expediente si can_view=true. Una sola evidencia prevista: 62-registro-react-acuse.png, con ID de caso ficticio y sin contraseñas/tokens. No se requieren capturas de cada campo ni repetir todo el ciclo ya probado en Swagger. Esta comprobación todavía no se ejecutó ni se presenta como aprobada.

Pendientes: edición, validación, asignación/transiciones y administración en React; enlaces profundos, comprobación móvil y permisos de otros roles. RF-2/RF-8 siguen parciales. El navegador no sustituye reglas API.
Prueba manual de alta inicial: evidencia 62 revisada el 17 de octubre de 2026 muestra acuse de recepción con ID y acceso permitido. Sustituye el pendiente total de primera prueba; no acredita todos los campos enviados ni apertura del detalle por sí sola. Escenarios restringidos/entorno siguen pendientes de prueba real. No se requiere más captura para este caso.

## Gestión del expediente — React 0.3.0 (17 de octubre de 2026)

Amplía el detalle con clasificación humana, asignación, edición y ciclo completo. Sustituye los pendientes de estas operaciones en 0.1/0.2; no añade endpoints, migraciones ni dependencias. Backend 0.8.0 y esquema 0003 conservados. Actualizar navegador con Vite activo; iniciar sesión de nuevo tras recarga.

Sección Gestionar incidencia visible solo a Supervisor/Admin RH tras detalle autorizado. Empleado conserva vista de lectura. Opciones proceden de /incidents/options y relaciones de /participants; se descartan afectados y relaciones DECLARADO/CONFIRMADO como candidatos gestores. Caso confidencial ofrece solo Admin RH; supervisor candidato requiere departamento actual del afectado o departamento de entorno. Esto ayuda al formulario; el backend vuelve a comprobar elegibilidad, estado y cuenta activa en cada operación.

- Confirmar clasificación: categoría y prioridad juntas, solo PENDIENTE/EN_REVISION. ENTORNO solo Riesgos.
- Guardar responsable: gestor elegible, solo estados editables. No inicia revisión automáticamente.
- Iniciar revisión: exige clasificación vigente y responsable elegido. API valida antes de entrar.
- Registrar resolución: EN_REVISION con clasificación vigente y resolución obligatoria, máximo 10000 caracteres.
- Cerrar caso: únicamente Admin RH, caso RESUELTA y confirmación explícita de cierre. No se ofrece cierre a supervisor.
- Reabrir: Admin RH desde RESUELTA/CERRADA, motivo obligatorio y responsable elegible. Se informa conservación del ciclo anterior. Reabrir no exige clasificación vigente como condición adicional que el PRD no establece, pero resolver después sí.
- Editar contenido: título/descripción completos en PENDIENTE/EN_REVISION. Aviso de revalidación al cambiar descripción, sin borrar validación anterior en el servidor.

Las escrituras usan las rutas existentes classification, assignment, transitions y content. Después del éxito se recargan detalle e historial desde servidor y el historial vuelve a primera página; no se inventa estado local como resultado definitivo. Botones bloqueados mientras guarda. 404 retira expediente/historial; 401/403 limpian sesión como antes; 409 indica actualizar y revisar requisitos. Respuesta de red/servidor incierta bloquea reenvío hasta Actualizar expediente: no hay reintentos automáticos ni garantía de idempotencia. El botón de actualización vuelve a consultar estado sin escribir.

Validación final: npm test, 26 pruebas aprobadas en 4 archivos, 15.80s. Incluye 10 nuevas de componentes y una integración de UI con ciclo completo/recarga del historial, además de 15 regresiones previas. Todas usan API simulada; no acreditan ciclo real PostgreSQL por esta entrega. npm run build correcto, 19 módulos y 262ms. Primer intento detectó un error JSX (dos suites sin ejecutar), corregido antes de pasar 25 pruebas; se añadió integración completa y se repitió suite con 26 aprobadas. Backend no modificado ni repetido.

Comprobación manual agrupada: iniciar sesión como Admin RH, abrir el caso simulado creado desde React, confirmar categoría/prioridad, seleccionar RH responsable, iniciar revisión, escribir resolución simulada y cerrar confirmando la casilla. Una sola captura del detalle final: 63-gestion-react-caso-cerrado.png, solo datos ficticios y sin credenciales. Opcionalmente reabrir con motivo y comprobar historial; no pedir captura por cada paso. Este recorrido real aún está pendiente y no se presenta como aprobado por las pruebas simuladas.

Siguen pendientes interfaces de participantes/confidencialidad y administración de usuarios/departamentos, móvil y matriz completa de roles, enlaces profundos e integraciones IA/correo/analítica. RF-3/RF-4/RF-8 parciales. No hay borrado ni retroceso libre a PENDIENTE en UI. Las nuevas funciones no ejecutan IA ni correo.
Prueba manual de gestión: evidencia 63 revisada el 17 de octubre de 2026 muestra Retardo cerrado con resolución/fechas y clasificación vigente. Corresponde al ID del acuse 62. Completa resultado final del recorrido guiado, sin sustituir pruebas de cada transición/rol. No se requieren capturas intermedias adicionales para este caso.

## Usuarios y protección — React 0.4.0 (17 de octubre de 2026)

Esta entrega sustituye los pendientes históricos de interfaz de administración de cuentas y protección. Menú Usuarios solo para Admin RH: listado paginado, alta local y edición de nombre, departamento, rol y activación con motivo. El correo no se modifica y la contraseña inicial se limpia tras el intento; recuperación continúa por el procedimiento administrativo existente. No incorpora CRUD de departamentos.

En detalle autorizado, RH dispone de confidencialidad, declaración y revisión de participantes con motivo, conservando declaración original. Solo en PENDIENTE/EN_REVISION; casos finalizados exigen reapertura. La reasignación protectora la decide la API mediante su selección automática existente. Descartar una relación no retira confidencialidad; no se ofrece autorrevisión. Candidatos de asignación y candidatos a participante son listas distintas.

Cada escritura se confirma en servidor y recarga datos. Si el acuse indica can_view=false, desaparecen expediente, formularios e historial. Cambiar los propios permisos con sessions_revoked=true limpia token y vuelve al login sin consultar otra vez el directorio. Respuestas inciertas no se reintentan automáticamente y requieren consulta antes de repetir. Permisos, último RH activo y ajustes atómicos siguen siendo responsabilidad del backend.

Validación: 40 pruebas aprobadas en 6 archivos, 23.66s; compilación de 21 módulos en 358ms. Incluye 12 pruebas nuevas de componentes y 2 integraciones de navegación/retiro de datos. Se corrigió una prueba anterior con selector ambiguo entre párrafo y textarea, y se completó su fixture de participantes. API simulada; no acredita ejecución real de estas operaciones contra PostgreSQL ni concurrencia. Backend no cambiado ni repetido; conserva 0.8.0/esquema 0003. Sin dependencias ni migraciones nuevas.

Comprobación manual agrupada pendiente: actualizar página con Vite activo, entrar como Admin RH y abrir Usuarios. Editar únicamente el nombre de una cuenta DEMO, conservar rol/departamento/activación, indicar motivo y guardar; comprobar confirmación y listado actualizado. No modificar los propios permisos para esta primera comprobación. Una captura final del listado/aviso: 64-admin-react-usuarios.png. Solo identidades ficticias; contraseña inicial y tokens fuera de captura. Protección puede recorrerse sobre un caso simulado abierto, sin exigir captura de cada paso; resultado real todavía no acreditado.

Pendientes: comprobación real de esta entrega, matriz completa de roles/móvil, CRUD departamentos, enlaces profundos e integraciones IA/correo/analítica. RF-4/RF-7/RF-8 siguen parciales.

Actualización 17 de octubre de 2026: evidencias 64/64b revisadas; listado administrativo React y aviso de guardado sin cambio de permisos, 0 casos ajustados. Primera comprobación manual de Usuarios acreditada con límites en REPORTE_QA.md; no acredita protección, auditoría persistida ni administración completa. RF-7/RF-8 parciales. Pruebas de código no repetidas por este registro documental.

Actualización 17 de octubre de 2026: evidencias 65–66 inspeccionadas, primera comprobación React de caso confidencial/IA omitida y participante CONFIRMADO con declaración y motivo de revisión conservados. Sustituye el pendiente total del recorrido inicial de protección UI; no completa matriz de roles, auditoría ni concurrencia. El recorte 66 no contiene ID de expediente. RF-4/RF-8 parciales; límites en REPORTE_QA.md. No se repitieron pruebas de código para esta actualización documental.

## Contraseña personal — React 0.5.0 (17 de octubre de 2026)

Botón Cambiar contraseña en la cabecera para todos los roles. Solicita contraseña actual, nueva de 12–128 caracteres no compuesta únicamente por espacios y confirmación idéntica. No altera espacios válidos de la credencial. Reutiliza POST /auth/change-password: la API verifica la actual, guarda el hash, revoca todas las sesiones y audita sin registrar contraseñas. Una respuesta 204 limpia sesión/vistas y vuelve al login con aviso; la nueva credencial se usa al entrar otra vez.

El formulario envía solo current_password y new_password. Limpia los tres campos después de un intento de envío y no usa almacenamiento persistente. Un 400 informa que no se pudo verificar la actual; 401/403 siguen el cierre global de sesión. Red/5xx deja resultado no confirmado y retira sesión local por precaución, sin reintento de escritura. Login con credencial válida o recuperación por operador resuelven ese caso. Mientras espera respuesta se bloquean envío, cancelación y navegación de la aplicación; recargar/cerrar navegador sigue siendo posible.

No añade rutas, dependencias, migración ni cambios al backend 0.8.0/esquema 0003. Con Vite activo, actualizar página e iniciar sesión. Este avance no completa CRUD de departamentos ni recuperación pública de contraseña.

Comprobación manual agrupada pendiente: iniciar con una cuenta DEMO cuya contraseña actual se conozca, usar Cambiar contraseña y guardar una nueva elegida por la autora. Confirmar regreso al login con aviso. Guardar únicamente ese login vacío como 67-react-password-actualizada.png; no capturar el formulario ni enviar credenciales al asistente. Luego comprobar acceso con la nueva contraseña. La captura por sí sola no demuestra revocación de otras sesiones ni inicio con la nueva credencial.

Validación de esta entrega: 48 pruebas UI simuladas aprobadas en 7 archivos/67.31s y build de 22 módulos/749ms. Primer intento tuvo dos timeout en pruebas anteriores; repetición con dos workers pasó. Configuración Vitest conserva maxWorkers=2 para npm.cmd test. Backend no repetido. Detalle en REPORTE_QA.md.

Actualización 17 de octubre de 2026: evidencia 67 revisada, login vacío con aviso de contraseña actualizada. La autora confirmó nuevo inicio de sesión; registro manual reportado, sin exposición de credenciales. Sustituye el pendiente del recorrido básico de cambio personal; otras sesiones/contraseña anterior no comprobadas. RF-1/RF-8 parciales. Límites en REPORTE_QA.md; no se requieren más capturas de este recorrido.
