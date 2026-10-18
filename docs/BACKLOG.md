# Backlog y plan vigente



Base: [PRD 1.9](PRD.md). Estado consolidado al 15 de octubre de 2026. Las entradas históricas permanecen en Git y BITACORA.md; este archivo muestra el estado actual.



## Estado de los hitos



| Hito | Alcance | Estado verificable | Próxima evidencia |

| --- | --- | --- | --- |

| H1 Requisitos y propuesta | PRD, decisiones y propuesta técnica | PRD 1.9 consolidado; propuesta independiente pendiente | Revisión documental y propuesta |

| H2 Arquitectura y entorno | API base, Docker, diseño y estructura React | API y contenedores verificados manualmente; arquitectura formal y React pendientes | Documento de arquitectura |

| H3 Datos | Esquema y fixtures de QA | 0001 y seis usuarios DEMO verificados; 0002 implementada, aplicación real pendiente; cambios 1.8 sin implementar | Migración 0002 y diseño de próxima migración |

| H4 Identidad y administración | RF-1 y RF-7 | Autenticación local y alta básica implementadas; 20 pruebas locales aprobadas en último avance, 2 PostgreSQL omitidas; administración completa pendiente | Login real, logout y gestión de bajas/roles |

| H5 Registro y panel | RF-2 y RF-8 | Pendiente; modelos iniciales no equivalen al servicio | Casos PERSONA/ENTORNO y filtros autorizados |

| H6 Ciclo y confidencialidad | RF-4 y reglas transversales | Pendiente | Revalidación, recusa y auditoría atómica |

| H7 IA | RF-3 | Pendiente; proveedor OpenAI elegido | Worker, omisión de confidenciales y evaluación independiente |

| H8 Correo | RF-5 | Pendiente; solo eventos, sin SLA | SMTP capturador y pruebas de permisos |

| H9 Analítica | RF-6 | Pendiente | Vistas agregadas y fórmulas verificadas |

| H10 Entrega | QA, manuales, soporte, capacitación e informe | Manuales/QA iniciales; entrega final pendiente | Instalación y evaluación integral |



## Orden inmediato



1. Aplicar 0002 desde terminal autorizada y verificar primer administrador/login. Seguir AUTENTICACION.md.

2. Diseñar la siguiente migración sin modificar 0001/0002: scope, afectado nullable condicional, departamento reportado, participantes, classification_valid y control de IA. Actualizar DATOS.md como diseño vigente antes de implementarla.

3. Implementar permisos por objeto y conflictos de interés junto con RF-2/RF-4; no construir un CRUD sin restricciones como solución final.

4. Crear diez casos simulados mediante servicio auditado. Implementar panel React y pruebas de acceso/filtrado.

5. Integrar IA solo sobre texto simulado revisado, sin confidenciales; preparar 50 referencias independientes. Integrar correo por eventos y analítica.



## Calendario y capacidad



Arranque documentado: 15 de octubre de 2026. No se ha recibido fecha límite definitiva ni horas disponibles por semana. El cronograma anterior de seis semanas no constituye compromiso vigente. Registrar esos dos datos antes de fijar fechas por hito. Mientras tanto, el orden de trabajo se define por dependencias y evidencia, no por fechas inventadas.



Los hitos se relacionan con las diez actividades académicas mediante la sección 10 del PRD y ENTREGABLES.md. Documentación y pruebas acompañan cada avance. Capacitación requiere sesión real y el cierre requiere resultados reales.



## Criterios de término por avance



Código y configuración revisables, pruebas pertinentes con resultado/limitaciones, manual e instrucciones actualizados, evidencia sin secretos, bitácora y trazabilidad al día, y commit por cambio real. Una prueba omitida o una configuración no ejecutada no equivale a aprobación. Las versiones previas del PRD no se convierten en actividad retrospectiva.



## Decisiones que no amplían el MVP



Sin Entra ID, SLA, alertas por tiempo, nómina, app móvil, registro público o uso productivo de datos reales. La conservación de campos externos permite una futura integración sin prometerla. Modelo OpenAI, librería worker y SMTP concreto se eligen antes de sus hitos y se documentan.


## Ajustes de la revisión 1.9

Núcleo: H1–H6 y QA/documentación necesarios de H10. Después integrar H7–H9 (IA, correo y Power BI), sin eliminarlos de la entrega final. No hay esfuerzo estimado ni fechas comprometidas hasta conocer capacidad y fecha límite.

Antes de implementar incidencias: validar participantes y recusa mediante estados de revisión; agregar procedimiento auditado de administrador independiente (el CLI actual no lo soporta). Antes de RF-6: vistas excluyen confidenciales y participantes pendientes, suprimen grupos pequeños y totales reconstruibles. Antes de aceptar RF-7: tanto API como pantalla React, no solo comandos. Preparar respuesta IA SIN_CLASIFICACION y prueba separada de abstención. No se afirma implementación por corregir el documento.

## 16 de octubre de 2026 — Esquema de incidencias

0003 implementada para ámbitos/participantes/clasificación y control IA; aplicación real pendiente. Evidencias 09–11 acreditan manualmente 0002, consulta autenticada y rechazo 401 posterior, no la nueva revisión. Próximo paso tras validar 0003: servicios de autorización por objeto y registro auditado, antes del formulario React.

## 16 de octubre de 2026 — 0003 verificada

Evidencias 12/13 confirman migración 0003, alembic check sin diferencias y conexión HTTP 200. El siguiente avance es implementar autorización por objeto y registro/listado/detalle de incidencias, con auditoría y pruebas de ámbitos, departamentos y conflicto de interés. No hay todavía endpoints de casos aceptados.

## 16 de octubre de 2026 — Registro y consultas

RF-2 parcial: alta PERSONA/ENTORNO auditada, confidencialidad preventiva y declaración de participantes. RF-8 backend parcial: opciones, listado con filtros/paginación, detalle, participantes e historial restringidos. API 0.5.0 mantiene esquema 0003. Validación manual PostgreSQL de estos endpoints pendiente. Siguiente: validación/edición y asignación/transiciones auditadas; frontend e integraciones no están terminados.

Actualización 16 de octubre de 2026: evidencias 14/15 verificadas, registro 201 y listado 200 del mismo caso PENDIENTE. Se cierra esta prueba manual básica; detalle/historial manuales y validación/asignación/transiciones continúan pendientes. RF-2 y RF-8 siguen parciales.

Actualización 16 de octubre de 2026: evidencia 16 revisada, historial HTTP 200 con evento CREADO. Registro, listado e historial básicos verificados manualmente; RF-2/RF-4/RF-8 continúan parciales. Validación, asignación y transiciones pendientes. Alcance de la prueba en REPORTE_QA.md.

## 16 de octubre de 2026 — Clasificación y ciclo backend

API 0.6.0 implementa validación conjunta de categoría/prioridad, asignación a gestor elegible, edición con invalidación y transiciones/reapertura auditadas. RF-3/RF-4 continúan parciales: faltan revisión de participantes, cambios de confidencialidad y retroceso protector; integración IA, frontend y pruebas reales de concurrencia pendientes. Validación local 51 pruebas aprobadas/3 omitidas; reconstrucción y evidencias 17/18 pendientes.

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

Procedimiento de RH adicional preparado en paquete, con siete pruebas nuevas; pendiente aplicar/reconstruir/verificar manualmente. No declarar RF-7 terminado: gestión completa de cuentas/roles/departamentos y UI pendientes. Ver ADMIN_INDEPENDIENTE.md y REPORTE_QA.md.

Actualización 16 de octubre de 2026: procedimiento de RH adicional aplicado y ejecutado según reporte de la autora; evidencias 34–37 revisadas y documentadas en REVISION_RH_INDEPENDIENTE.md. RF-7 parcial: cuenta/sesión independiente acreditadas, recorrido de acceso permitido y rechazo reportados con límites del recorte. Administración completa, frontend y concurrencia pendientes.

Administración backend 0.8.0 preparada: modificación de cuentas y revisión de casos con auditoría/revocación. 35 pruebas seleccionadas aprobadas; pendiente aplicación, suite HTTP completa, prueba real PostgreSQL/concurrencia, UI y CRUD departamentos. RF-7 parcial.

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

React 0.4.0, 17 de octubre de 2026: cuentas desde Usuarios y protección/participantes desde expediente implementados; sustituyen pendientes históricos de estas pantallas. 40 pruebas frontend simuladas y build correctos. RF-4/RF-7/RF-8 parciales: validación real agrupada/evidencia 64, CRUD departamentos, matriz de roles/móvil e integraciones pendientes. Ver FRONTEND.md.

Actualización 17 de octubre de 2026: evidencias 64/64b revisadas; listado administrativo React y aviso de guardado sin cambio de permisos, 0 casos ajustados. Primera comprobación manual de Usuarios acreditada con límites en REPORTE_QA.md; no acredita protección, auditoría persistida ni administración completa. RF-7/RF-8 parciales. Pruebas de código no repetidas por este registro documental.

Actualización 17 de octubre de 2026: evidencias 65–66 inspeccionadas, primera comprobación React de caso confidencial/IA omitida y participante CONFIRMADO con declaración y motivo de revisión conservados. Sustituye el pendiente total del recorrido inicial de protección UI; no completa matriz de roles, auditoría ni concurrencia. El recorte 66 no contiene ID de expediente. RF-4/RF-8 parciales; límites en REPORTE_QA.md. No se repitieron pruebas de código para esta actualización documental.

React 0.5.0, 17 de octubre de 2026: pantalla de cambio de contraseña para todos los roles, reutilizando /auth/change-password. Confirma nueva credencial, limpia campos y vuelve al login al guardar; resultado incierto retira sesión local sin reenvío. Sin migración ni backend nuevo. RF-1/RF-8 parciales; comprobación real/evidencia 67 y departamentos pendientes. Uso y límites en FRONTEND.md.
