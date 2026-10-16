# Trazabilidad vigente del PRD 1.9



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



01: HTTP health; 02: servicios Compose healthy; 03: SELECT 1; 04: PONG; 05: revisión 0001 y alembic check; 06: health/db real con 0001; 07/08: carga DEMO y repetición. No acreditan aún autenticación real 0002 ni reglas nuevas de PRD 1.9.


## Aceptación adicional PRD 1.9 — pendiente

| Caso | Regla | Resultado esperado |
| --- | --- | --- |
| AC-11 | Participantes | API limita selección al ámbito; declaración de gestor restringe inmediatamente; solo revisor independiente confirma/descarta con motivo |
| AC-12 | Único Admin RH declarado | Caso restringido pendiente; cuenta del señalado y otros expedientes no se bloquean; sin desbloqueo automático; provisión independiente auditada pendiente de código |
| AC-13 | Privacidad Power BI | Confidenciales y relaciones pendientes excluidos; grupos <5 suprimidos; cinco casos de un solo afectado no se publican; totales no reconstruyen celdas |
| AC-14 | Limitación de seguimiento | Acuse sin contenido; quien pierde acceso no consulta estado/resultado; la interfaz informa antes de enviar |
| AC-15 | RF-7 | Administración funciona por API y pantalla React; operador usa comandos separados |
| AC-16 | IA inconclusa | SIN_CLASIFICACION válido termina trabajo sin categoría forzada; requiere gestión manual y no mejora artificialmente el denominador de evaluación |

Todos son criterios previstos; no se han ejecutado ni se presentan como pruebas aprobadas. Los 20 casos del antiguo plan nunca se ejecutaron. La suite local previa de autenticación sigue siendo evidencia distinta.

## 16 de octubre de 2026 — Esquema 0003

RF-2/RF-3/RF-4: modelos y migración 0003 incorporan ámbitos, participantes/revisión, bandera y omisión IA. Pruebas en test_incident_schema.py; preservación de datos PostgreSQL prevista en test_postgres.py. No hay endpoints de casos ni autorización por objeto: AC-02/03 tienen cobertura de estructura parcial; AC-04/05/06/11/12 aún requieren servicios. Aplicación PostgreSQL de 0003 pendiente.

0003: validación manual de aplicación/alineación y conexión acreditada en evidencias 12/13. RF-2/RF-4 siguen pendientes de servicios y autorización; las capturas no sustituyen pruebas de conservación de casos previos ni pruebas automáticas PostgreSQL.

## 16 de octubre de 2026 — Endpoints iniciales de incidencias

RF-2: api/incidents.py y services/incidents.py implementan registro con ámbitos y auditoría. Reglas de acceso/recusa y confidencialidad se aplican a lectura SQL y acuse. RF-8: opciones/listado/detalle/historial backend, sin React. Tests/test_incidents.py cubre AC-02, parte de AC-04/05/10/11/14 y rollback; no implica RF completos. Cambios de estado/participantes, provisión de RH independiente e integraciones pendientes. Resultados y limitaciones en REPORTE_QA.md.

Evidencias 14/15 revisadas el 16 de octubre de 2026: RF-2 registro básico con acuse 201 y RF-8 listado backend 200 del mismo caso PENDIENTE. Alcance parcial; no acredita todos los criterios de acceso ni el ciclo de vida. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 16 revisada, historial HTTP 200 con evento CREADO. Registro, listado e historial básicos verificados manualmente; RF-2/RF-4/RF-8 continúan parciales. Validación, asignación y transiciones pendientes. Alcance de la prueba en REPORTE_QA.md.

API 0.6.0 (16 de octubre de 2026): RF-2 edición auditada; RF-3 clasificación humana vigente; RF-4 asignación/estados/reapertura. services/lifecycle.py y seis pruebas HTTP/SQLite adicionales en test_incidents.py cubren parcialmente revalidación, acceso, transiciones y rollback. No sustituyen concurrencia PostgreSQL, revisión de participantes, confidencialidad ni frontend. Resultados y límites en REPORTE_QA.md.
