# Trazabilidad inicial

Base funcional: docs/PRD.md. Base académica: matriz docs/ENTREGABLES.md.

| Requisito | Implementación prevista | Validación prevista | Estado |
| --- | --- | --- | --- |
| RF-1 Autenticación | backend/app/core y API | Token inválido, usuario no autorizado/inactivo, roles | Pendiente |
| RF-2 Registro | API, modelos y formulario | Creación propia y por terceros, edición auditada | Pendiente |
| RF-3 IA y validación | Servicios y worker | Fallas, respuesta tardía, validación humana, 20 casos etiquetados | Pendiente |
| RF-4 Asignación y ciclo | Servicios y detalle de incidencia | Transiciones, responsable activo y permisos | Pendiente |
| RF-5 Notificaciones | Servicio de correo y worker | SMTP de prueba, permisos, reintentos y deduplicación | Pendiente |
| RF-6 Analítica | Vistas agregadas y Power BI | Fórmulas, fecha de corte y ausencia de datos personales | Pendiente |
| Confidencialidad | Autorización transversal | Acceso por ID, departamento, reasignación y pérdida de acceso | Pendiente |
| RNF-1 Seguridad | API y despliegue | Validación JWT y HTTPS en entorno de entrega | Pendiente |
| RNF-2 Rendimiento | API y colas | p95 < 200 ms, 10 usuarios, condiciones documentadas | Pendiente |

Al implementar se añadirán rutas de archivos, nombres de pruebas y resultados reales. Esta tabla no equivale a pruebas aprobadas.

RF-3: proveedor seleccionado por la autora: API directa de OpenAI. Modelo, conexión e implementación pendientes.

## Infraestructura de API inicial

Endpoint público de disponibilidad en `backend/app/api/health.py`, aplicación en `backend/app/main.py` y pruebas en `backend/tests/test_api.py`. Es una base técnica y no implica cumplimiento de RF-1 a RF-6. Resultados reales en REPORTE_QA.md.
