> Estado documental vigente: PRD 1.8, backlog y trazabilidad consolidados. Los requisitos nuevos están pendientes de implementación; esto no completa los entregables de desarrollo o QA.

# Entregables de residencia

Fuente: secciÃ³n 7 del Descriptivo de Proyecto proporcionado por la autora. Esta matriz organiza los entregables; un archivo o carpeta por sÃ­ solo no demuestra que la actividad estÃ© terminada.

| Actividad | Entregable | UbicaciÃ³n prevista o actual | Estado real |
| --- | --- | --- | --- |
| 1. DetecciÃ³n de necesidades | Documento de requerimientos | PRD.md | Base documentada; anÃ¡lisis de campo no acreditado |
| 2. Propuesta | Propuesta tÃ©cnica | PROPUESTA_TECNICA.md | Pendiente; reglas iniciales en PRD |
| 3. Arquitectura | Documento de arquitectura | ARQUITECTURA.md | Pendiente; stack y estructura inicial definidos |
| 4. PlanificaciÃ³n | Plan del proyecto | BACKLOG.md y cronograma en PRD.md | Inicial; seguimiento por completar |
| 5. Desarrollo | Sistema funcional | ../backend, ../frontend, ../infra | API y esquema inicial implementados; migraciÃ³n y conexiÃ³n verificadas manualmente; carga DEMO y repeticiÃ³n verificadas manualmente; Compose verificado manualmente; autenticación local implementada con migración 0002 pendiente; flujos de incidencias pendientes |
| 6. Pruebas | Reporte QA | REPORTE_QA.md | Reporte de validaciÃ³n inicial en REPORTE_QA.md; QA del MVP pendiente |
| 7. DocumentaciÃ³n | Manual tÃ©cnico y manual de usuario | MANUAL_TECNICO.md y MANUAL_USUARIO.md | Manual tÃ©cnico inicial disponible; manual de usuario pendiente |
| 8. Mantenimiento | Plan de mantenimiento y soporte multinivel | PLAN_MANTENIMIENTO.md | Pendiente |
| 9. CapacitaciÃ³n | Acta de capacitaciÃ³n | CAPACITACION.md | Pendiente de sesiÃ³n real |
| 10. Cierre | Informe final y lecciones aprendidas | INFORME_FINAL.md | Pendiente |

Las rutas previstas no implican archivos ya creados. Los documentos se elaborarÃ¡n conforme exista contenido verificable. La capacitaciÃ³n y la evaluaciÃ³n final solo se registrarÃ¡n como realizadas cuando ocurran.

## Evidencia por avance

Cada entrada de bitÃ¡cora registra propÃ³sito, cambio, validaciÃ³n, resultado y pendientes. Las evidencias pueden ser cÃ³digo, comandos y salidas sanitizadas, reportes de pruebas, capturas sin datos sensibles y commits. Git conserva autor y fecha; no sustituye actas ni evidencia de actividades con personas.

## Diferencia documentada

El descriptivo enumera Azure OpenAI Service. El 15 de octubre de 2026 la autora eligiÃ³ la API directa de OpenAI, consistente con el PRD. DecisiÃ³n registrada en DECISIONES.md. La conexiÃ³n, el modelo y la integraciÃ³n siguen pendientes; no se ha realizado una llamada de prueba.

Actualización 16 de octubre de 2026: autenticación verificada manualmente en evidencias 09–11; esquema 0003 de incidencias implementado, no aplicado todavía desde el asistente. No equivale a sistema de casos funcional; resultados actuales en REPORTE_QA.md.

Entrega 0.5.0: registro y consulta de casos implementados como avance backend parcial; prueba manual pendiente. No marca sistema funcional completo ni panel React entregado.

Validación manual de entrega 0.5.0 (16 de octubre de 2026): registro y listado básicos acreditados por evidencias 14/15 inspeccionadas. Los pendientes históricos anteriores se conservan como historial; esto no declara entregado el sistema completo.

Actualización 16 de octubre de 2026: evidencia 16 revisada, historial HTTP 200 con evento CREADO. Registro, listado e historial básicos verificados manualmente; RF-2/RF-4/RF-8 continúan parciales. Validación, asignación y transiciones pendientes. Alcance de la prueba en REPORTE_QA.md.

Entrega parcial API 0.6.0: clasificación humana, asignación, edición y ciclo auditado implementados, con 51 pruebas locales aprobadas y 3 PostgreSQL omitidas. Manuales actualizados; verificación manual del nuevo ciclo pendiente. No equivale a sistema completo ni reporte QA final.

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

Procedimiento técnico adicional: ADMIN_INDEPENDIENTE.md y CLI auditado preparados; aplicación al repositorio y prueba manual pendientes. No se presenta como capacitación ni entrega completa del módulo administrativo.

Actualización 16 de octubre de 2026: procedimiento de RH adicional aplicado y ejecutado según reporte de la autora; evidencias 34–37 revisadas y documentadas en REVISION_RH_INDEPENDIENTE.md. RF-7 parcial: cuenta/sesión independiente acreditadas, recorrido de acceso permitido y rechazo reportados con límites del recorte. Administración completa, frontend y concurrencia pendientes.

Entrega 0.8.0 preparada, todavía no aplicada: administración backend y manual ADMIN_USUARIOS.md. No constituye administración React completa ni reporte QA final. Pruebas y límites en REPORTE_QA.md.

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

Actualización 17 de octubre de 2026, React 0.4.0: desarrollo incluye directorio/alta/edición de cuentas y protección/revisión de participantes desde UI. QA: 40 pruebas frontend con API simulada y build aprobados; manual técnico/guía de uso actualizados. Prueba real agrupada/evidencia 64 pendiente; no completa desarrollo/QA del MVP ni administración de departamentos.
