# Registro y gestión de incidencias

Registro, consultas, clasificación humana, asignación, edición, transiciones y protección de participantes/confidencialidad están implementados en API y panel React. IA y correo tienen guías propias. Aplica las migraciones pendientes antes de usar las rutas; los recorridos históricos no sustituyen la aceptación integral.

## Rutas protegidas

| Método y ruta | Comportamiento |
| --- | --- |
| GET /incidents/options | Afectados permitidos, participantes/contactos mínimos, departamentos y categorías; sin correos ni credenciales |
| POST /incidents | Crea caso PENDIENTE con auditoría en misma transacción; devuelve solo acuse |
| GET /incidents | Lista paginada y conteo del conjunto autorizado |
| GET /incidents/{id} | Detalle visible; 404 si no existe o no está autorizado |
| GET /incidents/{id}/participants | Participantes y revisión para gestores autorizados; empleado recibe lista vacía |
| GET /incidents/{id}/history | Historial paginado del caso; empleado ve solo acción/fecha/ID, sin copias de contenido ni relaciones de terceros |

Se utiliza el token local Bearer. Respuestas con Cache-Control: no-store. El autor se obtiene de la sesión; no se acepta created_by, rol, asignación, estado o resultado IA en el formulario. Campos adicionales son rechazados. No hay rutas públicas para casos.

## Validación y acceso

Empleado solo registra PERSONA sobre sí mismo. Supervisor sobre su departamento. Admin RH sobre cualquier empleado habilitado. ENTORNO exige departamento permitido y no admite afectado; categoría inicial Riesgos, aún sin validación humana. Departamento histórico se deriva del afectado/ámbito y no se acepta uno contradictorio.

Participantes requieren ID válido y motivo; máximo técnico de 20 por petición para evitar incorporación masiva. No se admiten duplicados ni volver a declarar al afectado. Usuarios/departamentos inactivos se rechazan. Para empleado/supervisor, participantes de su departamento o contactos gestores activos; admin tiene ámbito global.

Solicitar confidencialidad o involucrar a Supervisor/Admin RH hace el caso confidencial desde la creación, sin llamada IA (OMITIDA y motivo). No se asigna responsable automáticamente: puede permanecer PENDIENTE hasta disponer de RH independiente. El afectado gestor o participante gestor DECLARADO/CONFIRMADO no tiene acceso, aunque sea Admin RH. El reportante no se considera involucrado automáticamente.

El predicado SQL verifica nuevamente la participación y el rol actual del afectado/participantes para no exponer un caso si una promoción dejó una marca de confidencialidad desactualizada. El servicio administrativo coordina la actualización persistente de restricciones y reasignaciones por cambios de rol; las pruebas no sustituyen la aceptación completa de la recusa.

Si un caso no es confidencial, el empleado ve sus personales o riesgos generales que creó y siguen en su departamento; supervisor ve su departamento; Admin RH ve todo excepto los casos en que esté involucrado. Conteo, filtros, búsqueda, detalle, participantes e historial aplican el mismo conjunto autorizado. El historial del empleado se reduce a eventos para no exponer texto anterior o terceros.

Acuse: id, received=true y can_view. Un acuse con can_view=false no entrega expediente, estado posterior ni participantes; no significa error de creación.

## Filtros y límites

page >=1; page_size 20 por defecto y máximo 100. Filtros status, priority (1–3), category_id, assigned_to, created_from y created_to (fechas UTC inclusivas). q busca ID exacto o título literal sin convertir comodines %/_ en búsquedas globales. Orden estable por fecha e ID descendentes. Título 1–200 caracteres, descripción 1–10000, motivo de participante 1–2000; texto solo en blanco se rechaza.

## Prueba manual desde la raíz

Con las migraciones al día y Docker Desktop abierto:

```powershell
docker compose up -d --build --wait
```

Abrir /docs y comprobar el contrato disponible. Login local y Authorize como indica AUTENTICACION.md. Ejecutar GET /incidents/options para obtener el ID de un empleado DEMO, por ejemplo Empleado RH Demo; no elegir al propio administrador como afectado para esta primera prueba.

POST /incidents, sustituyendo el UUID con el obtenido:

```json
{
  "titulo": "Ausencia simulada",
  "descripcion": "Colaborador ficticio ausente durante una prueba académica.",
  "incident_date": "2026-10-16",
  "scope": "PERSONA",
  "affected_employee_id": "UUID_DEL_EMPLEADO_DEMO",
  "is_confidential": false,
  "participants": []
}
```

Se espera 201, received=true y can_view=true para el Admin RH independiente. Copiar el ID del acuse y consultar GET /incidents, GET /incidents/{id} y GET /incidents/{id}/history. Debe verse PENDIENTE y evento CREADO. Registro aún sin IA real ni responsable asignado.

Evidencias previstas: docs/evidencias/14-registro-incidencia-201.png y 15-listado-incidencias-200.png. Capturar solo Server response, sin Curl, token ni cabeceras Authorization; solo datos simulados. Los filtros y controles entre roles se prueban automáticamente con actores simulados; la verificación real PostgreSQL todavía debe ejecutarse y documentarse.

## Pruebas y límites

Las pruebas HTTP y de servicios cubren rollback de auditoría, filtros/count sin fuga, IDOR, ámbito, participantes, confidencialidad y ciclo. PostgreSQL aislado añade comprobaciones de persistencia y bloqueos; SQLite por sí solo no verifica concurrencia real. Los resultados y sus límites están en [QA](REPORTE_QA.md).

El panel y los workers están implementados. La aceptación completa requiere escenarios por rol y protección en un entorno real; no se deduce de una captura ni de probar una ruta aislada.

## Gestión del ciclo

Con las migraciones al día, todas las rutas exigen gestor con acceso independiente al caso; empleados no pueden modificarlos. Rechaza gestor involucrado o fuera de departamento. Operaciones y auditoría comparten transacción; PostgreSQL bloquea la fila del caso antes de reevaluar acceso y estado. Las pruebas SQLite no verifican bloqueo concurrente real.

| Método y ruta | Cuerpo y reglas |
| --- | --- |
| PUT /incidents/{case_id}/classification | category_id y priority (1 Alta, 2 Media, 3 Baja); confirma ambas, actualiza validated_by/at y classification_valid. ENTORNO solo categoría 4 |
| PUT /incidents/{case_id}/assignment | assigned_to de gestor activo, departamento activo y acceso independiente; solo PENDIENTE/EN_REVISION |
| PUT /incidents/{case_id}/content | titulo y descripcion completos; conserva valores previos en historial. Cambiar descripción invalida clasificación sin borrar último validador; solo PENDIENTE/EN_REVISION |
| POST /incidents/{case_id}/transitions | status objetivo; assigned_to opcional al entrar/reabrir revisión; resolution_text obligatorio al resolver; reason obligatorio y exclusivo de reapertura |

PENDIENTE → EN_REVISION requiere clasificación vigente y responsable autorizado. EN_REVISION → RESUELTA exige revalidación vigente, responsable todavía elegible y resolución no vacía. RESUELTA → CERRADA solo Admin RH independiente. RESUELTA/CERRADA → EN_REVISION solo Admin RH independiente, con motivo y responsable elegible; archiva resolución/fechas/ciclo anterior en auditoría y limpia campos finales. Reabrir conserva la vigencia de clasificación existente. No hay saltos ni edición de casos resueltos/cerrados sin reapertura.

Evento VALIDACION_IA identifica también confirmación humana manual por compatibilidad con el catálogo existente; detalle source=HUMANA, no implica llamada IA. Ninguna operación implementada envía texto a OpenAI. No se implementan todavía revisión de participantes, cambios de confidencialidad ni su retroceso excepcional a PENDIENTE. No aceptar RF-3/RF-4 completos por esta entrega parcial.

### Prueba manual de clasificación

Reconstruir desde la raíz con Docker Desktop abierto:

```powershell
docker compose up -d --build --wait
```

Abrir /docs y actualizar el contrato. Volver a iniciar sesión y autorizar si expiró. Obtener ID del caso Ausencia simulada con GET /incidents. Abrir PUT /incidents/{case_id}/classification, pegar ID y enviar:

```json
{"category_id":1,"priority":2}
```

Esperar 200 y classification_valid=true con validador/fecha. Evidencia prevista 17-clasificacion-validada-200.png; capturar únicamente Server response, sin Curl/token. Para continuar, obtener ID del Admin RH autenticado mediante GET /auth/me y usarlo como assigned_to en PUT assignment. Evidencia prevista 18-asignacion-200.png. No confundir UUID de usuario con UUID del expediente.

Iniciar revisión con POST transitions y {"status":"EN_REVISION"}; resolver con {"status":"RESUELTA","resolution_text":"Acción correctiva simulada para la prueba académica"}; cerrar con {"status":"CERRADA"}; reabrir con {"status":"EN_REVISION","reason":"Nueva información simulada"}. Comprobar historial y conservación de ciclos. Estas son instrucciones previstas, no pruebas manuales ya acreditadas.

## Protección y participantes

Las tres operaciones requieren Admin RH activo e independiente con acceso al expediente, solo PENDIENTE o EN_REVISION. Casos resueltos/cerrados deben reabrirse primero.

| Método y ruta | Cuerpo |
| --- | --- |
| POST /incidents/{case_id}/participants | user_id, declaration_reason; alta DECLARADO, máximo total 20 relaciones, sin duplicados ni afectado duplicado |
| PUT /incidents/{case_id}/participants/{participant_id}/review | review_status CONFIRMADO/DESCARTADO, reason; assigned_to opcional para ajustar responsable |
| PUT /incidents/{case_id}/confidentiality | is_confidential, reason; assigned_to opcional de gestor elegible |

Respuesta: acuse id, received y can_view. No devuelve expediente: declarar al propio administrador puede quitarle acceso inmediatamente. No puede confirmar/descartar su propia relación; debe intervenir otro Admin RH independiente. Actor, afectado y relaciones DECLARADAS/CONFIRMADAS se evalúan en servidor, no en el formulario. Las cuentas siguen activas y mantienen acceso a otros casos permitidos.

Se conserva motivo original de declaración. Revisar registra actor/fecha/motivo y anterior estado en auditoría. DESCARTADO no retira por sí solo confidencialidad. Para desmarcarla se requiere operación explícita con motivo y ningún Supervisor/Admin RH involucrado. Una relación descartada puede corregirse por otro estado con motivo, conservando cambios en historial.

Al añadir/confirmar un gestor se activa confidencialidad y ai_status=OMITIDA. Retirarla no relanza IA automáticamente. Se preservan las sugerencias históricas si existieran; no se invoca proveedor externo. El worker vuelve a comprobar elegibilidad antes del envío y al aceptar la respuesta; consultar los límites de envío en IA.md.

Cuando el responsable pierde acceso, en PENDIENTE se desasigna. En EN_REVISION se conserva uno elegible, se aplica el indicado válido o se selecciona un Admin RH activo independiente por orden de ID. Si no existe, vuelve a PENDIENTE, sin responsable ni inicio de ciclo actual; auditoría conserva valores previos y motivo. No hay retroceso libre por /transitions. Reasignación, restricciones y auditoría usan una transacción y bloqueo de fila del expediente.

El evento CAMBIO_CONFIDENCIALIDAD identifica estas operaciones por detalle.operation (participant_add, participant_review o confidentiality), incluyendo relación anterior/nueva y estado/responsable anteriores/nuevos. No se agrega un catálogo de eventos ni migración en esta entrega.

### Prueba manual de confidencialidad prevista

Reconstruir con docker compose up -d --build --wait; comprobar el contrato en /docs y renovar sesión si expiró. Sobre Ausencia simulada en EN_REVISION y con Admin RH como responsable, abrir PUT /incidents/{case_id}/confidentiality y usar:

```json
{"is_confidential":true,"reason":"Prueba académica de protección del expediente"}
```

Esperar 200 con received=true y can_view=true para RH independiente. Luego GET /incidents/{case_id} debe mostrar is_confidential=true, ai_status=OMITIDA y responsable RH. Evidencia prevista 24-confidencialidad-200.png: solo Server response del detalle, sin Curl ni token. Esta guía no afirma ejecución manual. No añadir al único Admin RH como participante en esta primera prueba: perdería acceso y requeriría otro RH independiente. El CLI auditado para provisionar otro administrador se documenta en ADMIN_INDEPENDIENTE.md.
