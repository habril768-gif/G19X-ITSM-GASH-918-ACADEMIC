# Plan de desarrollo del MVP

Los siguientes hitos se completan en orden. Estado inicial: pendientes.

| Hito | Resultado verificable | Evidencia |
| --- | --- | --- |
| 1. Base del repositorio | README, PRD, exclusión de secretos y plantilla | Archivos versionados |
| 2. Estructura técnica | API de salud y cliente inicial ejecutables | Instrucciones y comprobaciones locales |
| 3. Datos | Modelos, migraciones, categorías y usuarios simulados | Base creada desde cero |
| 4. Autenticación y permisos | Entra ID, lista autorizada, roles, departamentos | Pruebas de rechazo y acceso por ID |
| 5. Incidencias | Registro, listado, asignación y confidencialidad | Pruebas entre departamentos |
| 6. Ciclo y auditoría | Validar, resolver, cerrar y reabrir | Pruebas de transiciones y conservación histórica |
| 7. IA | Worker Redis, clasificación, reintentos y validación humana | Fallas controladas y evaluación etiquetada |
| 8. Correo | Eventos, permisos previos al envío y deduplicación | SMTP de pruebas |
| 9. Analítica | Vistas agregadas y reporte Power BI | Fórmulas verificadas sin datos personales |
| 10. Entrega | Docker, CI, manuales y pruebas de carga | Instalación reproducible y reporte QA |

## Criterios de evaluación

- Funcionalidad: demostrar los flujos completos del MVP.
- Calidad técnica: separar capas, validar entradas y probar permisos.
- Documentación: mantener README, PRD y decisiones al día.
- Reproducibilidad: dependencias declaradas, entorno de ejemplo y arranque documentado.
- Alcance: completar el MVP acordado antes de incorporar funciones nuevas.

## Secuencia de commits propuesta

1. `docs: documentar PRD y plan inicial del MVP`
2. `chore: crear estructura de backend y frontend`
3. `feat: agregar modelos y migraciones iniciales`
4. `feat: implementar autenticacion y permisos por rol`
5. `feat: registrar y consultar incidencias con confidencialidad`
6. `feat: implementar transiciones e historial`
7. `feat: integrar clasificacion asincrona con IA`
8. `feat: agregar notificaciones y analitica`
9. `test: validar flujos y reproducibilidad de entrega`

Los hitos pueden requerir varios commits. Se registra solo trabajo realizado, con su validación y limitaciones.

## Proveedor IA definido

Se usará API directa de OpenAI con LangChain. Modelo y prueba de conectividad pendientes. Véase DECISIONES.md.
