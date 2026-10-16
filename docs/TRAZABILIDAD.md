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

## Configuración de infraestructura

compose.yaml, backend/Dockerfile y backend/.dockerignore preparan el entorno local reproducible de API, PostgreSQL y Redis. Relacionado con arquitectura, desarrollo y entrega. Las comprobaciones ejecutables están en infra/README.md; resultados pendientes por falta de Docker. Esto no acredita conexión real ni cumplimiento de RF-2 o RF-3.

Infraestructura: cuatro evidencias manuales recibidas y verificadas visualmente; rutas y límites en REPORTE_QA.md. La comprobación de servicios no completa RF-2 ni RF-3.

## Persistencia inicial

RF-1: users con unicidad tenant_id/external_id, rol y departamento; autenticación pendiente. RF-2/RF-4: modelo incidencias e historial; operaciones y permisos pendientes. RF-3: campos IA y validación, sin integración externa. RF-6: fechas de ciclo y departamento histórico para futuras vistas.

Implementación: backend/app/models/__init__.py; backend/app/core/database.py; migración 0001. Verificación: tests/test_database.py y pruebas PostgreSQL optativas en tests/test_postgres.py. Aplicación real y evidencia /health/db pendientes; ver REPORTE_QA.md.

Persistencia: evidencias 05 y 06 confirman revisión 0001 y conexión real. Fixtures QA: app/seed_demo.py y tests/test_seed_demo.py preparan seis usuarios y dos departamentos; no implementan RF-1 ni cuentas SSO.

Fixtures QA: carga manual PostgreSQL y repetición verificadas en evidencias 07/08. Datos de prueba disponibles para próximos servicios; no implica cumplimiento de autenticación RF-1.
