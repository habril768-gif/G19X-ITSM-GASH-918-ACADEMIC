# Trazabilidad vigente del PRD 1.8

Fecha de consolidación: 15 de octubre de 2026. La tabla distingue requisito objetivo, evidencia existente y trabajo pendiente. El detalle histórico y los resultados de pruebas están en REPORTE_QA.md y BITACORA.md.

| ID | Requisito | Implementación/evidencia existente | Verificación pendiente | Estado |
| --- | --- | --- | --- | --- |
| RF-1 | Sesiones locales, contraseña, revocación | core/security.py, api/auth.py, manage_users.py; tests/test_auth.py; migración 0002 | Aplicar 0002 y probar bootstrap/login/logout en PostgreSQL | Implementado parcialmente verificado |
| RF-2 | Registro PERSONA/ENTORNO y edición auditada | Modelos iniciales en app/models; solo 0001 verificada, sin rutas de incidencias | Afectado condicional, validación de participantes, scope y edición | Pendiente de servicio y migración adicional |
| RF-3 | IA sobre texto simulado revisado y validación | Campos básicos IA; OpenAI elegido | Worker, eligibility check, OMITIDA, classification_valid, prueba de 50 casos | Pendiente |
| RF-4 | Asignación, transiciones y ciclos | Campos iniciales y restricciones básicas | Servicio atómico, revalidación, gestor independiente, reapertura/retroceso protector | Pendiente |
| RF-5 | Correo por eventos | Variables SMTP de ejemplo | Capturador, eventos, acceso antes de envío, reintentos y deduplicación | Pendiente |
| RF-6 | Reportes agregados | Fechas y departamento histórico iniciales | Vistas, Power BI, métricas y fecha de corte | Pendiente |
| RF-7 | Administración de usuarios/departamentos | Alta local restringida y comandos de bootstrap/reset; tests/test_auth.py | Bajas y roles/departamentos con reasignación; no perder último admin | Parcial |
| RF-8 | Panel React y consultas | Solo estructura frontend | Login, listado paginado, filtros, detalle, acciones, errores y administración | Pendiente |
| RNF-1 | Seguridad y permisos por objeto | Hash/sesión y pruebas locales; publicación API en loopback | Reglas de expedientes, HTTPS externo y límite global de tráfico | Parcial |
| RNF-2 | p95 y condiciones de carga | Meta definida; sin medición | 100 casos, 10 usuarios, 5 minutos y reporte | Pendiente |
| RNF-3 | Reproducibilidad | Compose, migraciones, requirements y CI; evidencias 01–08 | 0002 real, futura migración, CI remoto y arranque desde base vacía actualizado | Parcial |
| RNF-4 | Auditoría transaccional | Modelo historial y eventos de alta/cambio de contraseña | Incidencias, participantes, ciclos, permisos e inmutabilidad operativa | Parcial |
| RNF-5 | Operación y entrega | Manual técnico y QA iniciales | Soporte, recuperación, capacitación real e informe final | Parcial |

## Pruebas de aceptación a implementar

| Caso | Regla | Resultado esperado |
| --- | --- | --- |
| AC-01 | RF-1 sesión | Login válido, logout y expiración consistentes; secreto no expuesto |
| AC-02 | RF-2 ámbito | Riesgo ENTORNO sin afectado aceptado; PERSONA sin afectado rechazado |
| AC-03 | RF-2/RF-4 validación | Editar descripción invalida bandera; no resolver hasta confirmar de nuevo |
| AC-04 | Conflicto de interés | Supervisor/Admin involucrado no consulta ni gestiona; RH independiente sí |
| AC-05 | Falta de gestor | Caso confidencial PENDIENTE, sin responsable; ningún involucrado gana acceso |
| AC-06 | RF-3 privacidad | Caso confidencial/inelegible no llama proveedor; clasificación manual disponible |
| AC-07 | RF-5 acceso | Correo omitido si destinatario perdió permiso; no duplica eventos |
| AC-08 | RF-6 agregados | Métricas conocidas, cero denominador y ningún campo individual importado |
| AC-09 | RF-7 bajas | Revocar sesiones y reasignar antes de perder permiso; no eliminar último admin |
| AC-10 | RF-8 filtros | Conteos, filtros y búsquedas solo sobre conjunto autorizado; IDOR rechazado |

AC son identificadores de pruebas previstas, no resultados aprobados. AC-01 tiene cobertura local parcial en test_auth.py; la aceptación real de PostgreSQL sigue pendiente. El resto requiere implementación. Las 20 pruebas aprobadas de la última entrega y las dos omitidas son un resultado histórico; esta revisión documental no las vuelve a ejecutar.

## Evidencia disponible

01: HTTP health; 02: servicios Compose healthy; 03: SELECT 1; 04: PONG; 05: revisión 0001 y alembic check; 06: health/db real con 0001; 07/08: carga DEMO y repetición. No acreditan aún autenticación real 0002 ni reglas nuevas de PRD 1.8.
