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

Actualización 16 de octubre de 2026: evidencia 17 inspeccionada; clasificación humana HTTP 200, categoría 1, prioridad 2 y bandera vigente. RF-3 parcial, sin llamada IA. Asignación y ciclo manual pendientes; detalles en REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 18 revisada; asignación HTTP 200 con responsable y clasificación vigente, aún PENDIENTE. RF-4 parcial: transiciones manuales y verificación de concurrencia siguen pendientes. Alcance en REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 19 inspeccionada, transición HTTP 200 a EN_REVISION con clasificación vigente y responsable. RF-4 continúa parcial; resolución/cierre/reapertura manuales y concurrencia real pendientes. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 20 revisada; resolución HTTP 200 con texto y fecha, caso RESUELTA. RF-4 parcial; cierre/reapertura e historial de ciclos manuales pendientes. Límites en REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 21 revisada; HTTP 200, caso CERRADA con closed_at y resolución anterior conservada. RF-4 parcial: reapertura e historial de ciclos manuales y concurrencia pendientes. Detalles en REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 22 inspeccionada; reapertura HTTP 200 a EN_REVISION con campos finales nulos. Pendiente confirmar motivo y conservación del ciclo anterior en historial, además de concurrencia real. RF-4 parcial; límites en REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 23 revisada parcialmente; historial HTTP 200 con REAPERTURA y estado/fechas anteriores. Texto previo y motivo fuera del recorte, pendientes de evidencia complementaria. Ver REPORTE_QA.md; no se declara RF-4 completo.

Actualización 16 de octubre de 2026: evidencia 23b completa la 23; resolución anterior y motivo de reapertura verificados. Recorrido manual básico registro/revisión/resolución/cierre/reapertura e historial acreditado para el caso simulado. RF-4 sigue parcial por controles restantes; ver REPORTE_QA.md.

API 0.7.0 (16 de octubre de 2026): RF-2/RF-4 parciales, declaración/revisión independiente de participantes y confidencialidad con reasignación/retroceso protector en services/protection.py. Ocho pruebas nuevas HTTP/SQLite, total 59 aprobadas/3 omitidas. Validación manual 0.7.0, concurrencia PostgreSQL, provisión adicional por operador y gestión de cambios de usuarios siguen pendientes. Ver REPORTE_QA.md; no equivale a RF completos ni UI entregada.

Actualización 16 de octubre de 2026: evidencia 24b completa la 24; detalle HTTP 200 con confidencialidad activa y ai_status OMITIDA. Verificación manual parcial de protección; permisos entre roles, revisión de participantes y concurrencia real pendientes. Límites en REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 25 inspeccionada; detalle HTTP 200 con is_confidential=false y ai_status OMITIDA. Retiro explícito verificado parcialmente, sin reactivar IA. Declaración/revisión de participantes y permisos manuales pendientes; ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 26 inspeccionada, acuse HTTP 201 de participante. Relación y protección automática pendientes de GET; revisión independiente no completada. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 27 inspeccionada, participante DECLARADO con motivo y campos de revisión nulos. Pendientes revisión y comprobación de protección posterior al alta. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 28 inspeccionada, participante CONFIRMADO con revisor/fecha/motivo y declaración original conservada. Prueba manual de rechazo al retirar protección y descarte pendientes; ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 29 inspeccionada; rechazo 409 esperado al retirar confidencialidad con gestor involucrado. Control protector verificado parcialmente; descarte e historial manuales pendientes. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 30 revisada; participante DESCARTADO con declaración original y revisión completa. Confidencialidad posterior e historial previo pendientes de evidencia manual; ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencias 30/31 verifican descarte y conservación de confidencialidad con IA omitida. Pendientes retiro explícito posterior e historial de revisiones; controles completos y concurrencia no se declaran terminados. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 32 inspeccionada; retiro explícito posterior al descarte reflejado en detalle HTTP 200, confidencialidad desactivada e IA omitida. Prueba básica de protección/revisión/retiro verificada para el caso simulado. Auditoría histórica, permisos entre roles y concurrencia real pendientes; RF-4 parcial. Ver REPORTE_QA.md.

Actualización 16 de octubre de 2026: evidencia 33 revisada y validada estructuralmente, 15/15 eventos con alta, confirmación, descarte, protección automática y retiro explícito; conserva motivos y revisiones anteriores. Recorrido manual básico de protección y auditoría acreditado para el caso simulado. RF-4 parcial: matriz de acceso completa, concurrencia y provisión adicional por operador pendientes. Ver REPORTE_QA.md.

RF-7 y escalamiento de 3.2/3.3: CLI provision-independent-admin preparado en copia, test_manage_users.py verifica cuenta nueva, auditoría/rollback y exclusión original. 24 pruebas seleccionadas aprobadas; suite HTTP completa no verificada. Pendiente aplicar paquete y probar Docker; no acredita independencia humana ni RF-7 completo.

Actualización 16 de octubre de 2026: procedimiento de RH adicional aplicado y ejecutado según reporte de la autora; evidencias 34–37 revisadas y documentadas en REVISION_RH_INDEPENDIENTE.md. RF-7 parcial: cuenta/sesión independiente acreditadas, recorrido de acceso permitido y rechazo reportados con límites del recorte. Administración completa, frontend y concurrencia pendientes.

RF-7: services/users.py, api/users.py y test_user_administration.py preparados; cubren cambios, bajas/reactivación, último RH local y ajustes atómicos. Gate compartido coordina RF-2/RF-4 con cambios de acceso. 35 pruebas seleccionadas, sin validación HTTP completa ni concurrencia. Aplicación/manual pendientes. Ver ADMIN_USUARIOS.md.

Actualización 16 de octubre de 2026: backend de administración 0.8.0 aplicado según la autora; suite completa acreditada por evidencia 38, 77 aprobadas/3 omitidas/1 advertencia. Recorrido manual 39–46 de listado, desactivación/reactivación y revocación documentado con límites en REVISION_ADMIN_USUARIOS.md. RF-7 parcial: UI/CRUD departamentos, pruebas reales PostgreSQL/concurrencia y reasignación manual pendientes.

Actualización 17 de octubre de 2026: evidencias 47–57 acreditan recorrido manual de traslado con reasignación/auditoría y protección por promoción, conservada al restaurar rol. RF-4/RF-7 parciales; no se acredita concurrencia ni UI completa. Ver REVISION_TRASLADO_ROL.md y REPORTE_QA.md.

Actualización 17 de octubre de 2026: RF-1/RF-8 frontend parciales, login y lectura de casos/lista/filtros/historial en React. 9 pruebas simuladas y build aprobados; frontend HTTP 200 y proxy health ok. Formularios de escritura, administración UI, deep links y pruebas manuales pendientes. Ver FRONTEND.md; no se declara RF-8 completo.

Actualización 17 de octubre de 2026: evidencia 58 inspeccionada, panel React con 2 casos reales de prueba autorizados. Primera lectura/listado manual acreditada; RF-8 parcial. Detalle, filtros/logout manuales y formularios de gestión pendientes; ver REPORTE_QA.md.

Actualización 17 de octubre de 2026: evidencia 59 revisada, detalle React y fragmento de historial de caso simulado renderizados. RF-8 parcial: filtros/logout/móvil manuales y formularios pendientes. Límites en REPORTE_QA.md.

Actualización 17 de octubre de 2026: evidencia 60 inspeccionada, búsqueda React por título con una fila y total 1. RF-8 parcial; no acredita todos los filtros. Logout/móvil manuales y formularios pendientes. Ver REPORTE_QA.md.

Actualización 17 de octubre de 2026: evidencia 61 revisada, logout React vuelve a login vacío sin datos de casos visibles. Evidencias 58–61 completan recorrido manual inicial de lectura/búsqueda/salida, sin acreditar móvil ni todos los roles. RF-8 parcial; formularios pendientes. Ver REPORTE_QA.md.

React 0.2.0 (17 de octubre de 2026): RF-2/RF-8 parciales, alta persona/entorno con participantes, aviso y acuse según permiso en pages/NewIncident.jsx. Seis pruebas nuevas, 15 UI aprobadas y build correcto. Prueba real de registro desde UI pendiente; no equivale a RF completos. Formularios de gestión/admin y demás límites en FRONTEND.md.

Actualización 17 de octubre de 2026: evidencia 62 inspeccionada, acuse de alta React con referencia y acceso permitido. Primera prueba manual del registro acreditada con límites en REPORTE_QA.md. RF-2/RF-8 parciales; gestión UI y otros escenarios manuales pendientes.

React 0.3.0, 17 de octubre de 2026: edición, validación, asignación y transiciones en components/CaseManagement.jsx, con 26 pruebas frontend aprobadas y build correcto. RF-3/RF-4/RF-8 parciales; prueba real agrupada pendiente, así como protección/admin UI y otras funciones. Integración de UI completa con API simulada no sustituye PostgreSQL. Ver FRONTEND.md y REPORTE_QA.md.

Actualización 17 de octubre de 2026: evidencia 63 revisada; caso creado en React muestra cierre con resolución, fechas y validación vigente. Resultado manual de gestión inicial acreditado con límites en REPORTE_QA.md. Reapertura/edición manuales y pantallas de protección/admin pendientes; no se declaran RF completos.

## Estado complementario vigente — React 0.4.0, 17 de octubre de 2026

| Requisito | Implementación y prueba UI | Límite pendiente |
| --- | --- | --- |
| RF-1 | App retira token/directorio ante revocación propia; integración App.test.jsx | Revocación real de esta pantalla |
| RF-4 | CaseProtection.jsx: confidencialidad, participantes, revisión y retiro de expediente sin acceso; CaseProtection.test.jsx y App.test.jsx | Recorrido real y concurrencia |
| RF-7 | Users.jsx: alta/listado/edición, roles/departamento/activación con motivo; Users.test.jsx | CRUD departamentos y verificación UI real |
| RF-8 | Navegación administrativa y formularios por rol/estado | Móvil, matriz de roles y enlaces profundos |

40 pruebas UI simuladas aprobadas y build correcto. Sustituye pendientes históricos de estas pantallas, sin afirmar cumplimiento completo. Backend 0.8.0/esquema 0003 conservados. Evidencia 64 pendiente.

Actualización 17 de octubre de 2026: evidencias 64/64b revisadas; listado administrativo React y aviso de guardado sin cambio de permisos, 0 casos ajustados. Primera comprobación manual de Usuarios acreditada con límites en REPORTE_QA.md; no acredita protección, auditoría persistida ni administración completa. RF-7/RF-8 parciales. Pruebas de código no repetidas por este registro documental.

Actualización 17 de octubre de 2026: evidencias 65–66 inspeccionadas, primera comprobación React de caso confidencial/IA omitida y participante CONFIRMADO con declaración y motivo de revisión conservados. Sustituye el pendiente total del recorrido inicial de protección UI; no completa matriz de roles, auditoría ni concurrencia. El recorte 66 no contiene ID de expediente. RF-4/RF-8 parciales; límites en REPORTE_QA.md. No se repitieron pruebas de código para esta actualización documental.

React 0.5.0, 17 de octubre de 2026: pantalla de cambio de contraseña para todos los roles, reutilizando /auth/change-password. Confirma nueva credencial, limpia campos y vuelve al login al guardar; resultado incierto retira sesión local sin reenvío. Sin migración ni backend nuevo. RF-1/RF-8 parciales; comprobación real/evidencia 67 y departamentos pendientes. Uso y límites en FRONTEND.md.

Actualización 17 de octubre de 2026: evidencia 67 revisada, login vacío con aviso de contraseña actualizada. La autora confirmó nuevo inicio de sesión; registro manual reportado, sin exposición de credenciales. Sustituye el pendiente del recorrido básico de cambio personal; otras sesiones/contraseña anterior no comprobadas. RF-1/RF-8 parciales. Límites en REPORTE_QA.md; no se requieren más capturas de este recorrido.
