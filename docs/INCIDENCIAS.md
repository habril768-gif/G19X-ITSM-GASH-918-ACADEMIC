# Registro y consulta de incidencias

API 0.5.0, esquema 0003. Entrega parcial de RF-2/RF-4/RF-8: registro auditado, consultas y opciones mínimas. No incluye aún asignación, cambios de estado, edición, revisión de participantes, envío IA ni correo.

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

El predicado SQL verifica nuevamente la participación y el rol actual del afectado/participantes para no exponer un caso si una promoción dejó una marca de confidencialidad desactualizada. La actualización persistente de marca y reasignación por cambios de roles todavía pertenece al servicio administrativo pendiente; por eso no se declara terminada toda la recusa del PRD.

Si un caso no es confidencial, el empleado ve sus personales o riesgos generales que creó y siguen en su departamento; supervisor ve su departamento; Admin RH ve todo excepto los casos en que esté involucrado. Conteo, filtros, búsqueda, detalle, participantes e historial aplican el mismo conjunto autorizado. El historial del empleado se reduce a eventos para no exponer texto anterior o terceros.

Acuse: id, received=true y can_view. Un acuse con can_view=false no entrega expediente, estado posterior ni participantes; no significa error de creación.

## Filtros y límites

page >=1; page_size 20 por defecto y máximo 100. Filtros status, priority (1–3), category_id, assigned_to, created_from y created_to (fechas UTC inclusivas). q busca ID exacto o título literal sin convertir comodines %/_ en búsquedas globales. Orden estable por fecha e ID descendentes. Título 1–200 caracteres, descripción 1–10000, motivo de participante 1–2000; texto solo en blanco se rechaza.

## Prueba manual desde la raíz

No hay migración nueva respecto a 0003. Con Docker Desktop abierto:

```powershell
docker compose up -d --build --wait
```

Abrir /docs y comprobar versión 0.5.0. Login local y Authorize como indica AUTENTICACION.md. Ejecutar GET /incidents/options para obtener el ID de un empleado DEMO, por ejemplo Empleado RH Demo; no elegir al propio administrador como afectado para esta primera prueba.

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

Suite nueva tests/test_incidents.py usa SQLite con claves foráneas y HTTP TestClient; sustituye únicamente la dependencia de identidad por actores de prueba. No prueba credenciales reales ni reemplaza pruebas PostgreSQL. La autenticación local tiene sus propias pruebas existentes.

Se verifica rollback completo ante fallo de auditoría, filtros/count sin fuga, 404/IDOR, límites PERSONA/ENTORNO, participantes, confidencialidad y recusa incluso si cambia el rol del afectado. No se simula que ya existan worker, frontend o transiciones. Los endpoints de mutación restantes se implementarán con sus pruebas antes de aceptar el ciclo de vida completo.
