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
