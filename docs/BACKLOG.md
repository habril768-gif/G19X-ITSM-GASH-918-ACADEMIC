# Plan de desarrollo del MVP

Los hitos se completan en orden. Hito 1 completado; hito 2 en curso (API inicial implementada; cliente pendiente). Los demÃ¡s estÃ¡n pendientes.

| Hito | Resultado verificable | Evidencia |
| --- | --- | --- |
| 1. Base del repositorio | README, PRD, exclusiÃ³n de secretos y plantilla | Archivos versionados |
| 2. Estructura tÃ©cnica | API de salud y cliente inicial ejecutables | Instrucciones y comprobaciones locales |
| 3. Datos | Modelos, migraciones, categorÃ­as y usuarios simulados | Base creada desde cero |
| 4. AutenticaciÃ³n y permisos | Autenticación local, cuentas administradas, roles y departamentos | Pruebas de rechazo y acceso por ID |
| 5. Incidencias | Registro, listado, asignaciÃ³n y confidencialidad | Pruebas entre departamentos |
| 6. Ciclo y auditorÃ­a | Validar, resolver, cerrar y reabrir | Pruebas de transiciones y conservaciÃ³n histÃ³rica |
| 7. IA | Worker Redis, clasificaciÃ³n, reintentos y validaciÃ³n humana | Fallas controladas y evaluaciÃ³n etiquetada |
| 8. Correo | Eventos, permisos previos al envÃ­o y deduplicaciÃ³n | SMTP de pruebas |
| 9. AnalÃ­tica | Vistas agregadas y reporte Power BI | FÃ³rmulas verificadas sin datos personales |
| 10. Entrega | Docker, CI, manuales y pruebas de carga | InstalaciÃ³n reproducible y reporte QA |

## Criterios de evaluaciÃ³n

- Funcionalidad: demostrar los flujos completos del MVP.
- Calidad tÃ©cnica: separar capas, validar entradas y probar permisos.
- DocumentaciÃ³n: mantener README, PRD y decisiones al dÃ­a.
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

Los hitos pueden requerir varios commits. Se registra solo trabajo realizado, con su validaciÃ³n y limitaciones.

## Proveedor IA definido

Se usarÃ¡ API directa de OpenAI con LangChain. Modelo y prueba de conectividad pendientes. VÃ©ase DECISIONES.md.

## Avance de infraestructura

ConfiguraciÃ³n Compose de API, PostgreSQL y Redis preparada, pendiente de ejecuciÃ³n y validaciÃ³n en Docker Desktop. PrÃ³xima tarea: comprobar servicios y crear modelos/migraciones. El cliente React y la capa de persistencia siguen pendientes.

## VerificaciÃ³n manual recibida

La autora aportÃ³ evidencia de API/PostgreSQL/Redis healthy, SELECT 1 y PONG. Infraestructura bÃ¡sica arrancada; prÃ³ximo avance: modelos, migraciones y conexiÃ³n real de FastAPI a PostgreSQL. Ver REPORTE_QA.md.

## Modelos y migraciÃ³n inicial

Hito 3 en curso: modelos, migraciÃ³n 0001 y catÃ¡logos implementados. Pendiente aplicaciÃ³n real, validaciÃ³n PostgreSQL y usuarios/departamentos simulados. Ocho pruebas locales aprobadas; dos de integraciÃ³n omitidas. El hito no se marca completado todavÃ­a.

## MigraciÃ³n validada y fixtures preparados

Evidencia manual confirma migraciÃ³n 0001, alineaciÃ³n del esquema y conexiÃ³n HTTP de la API a PostgreSQL. Usuarios/departamentos simulados implementados con carga explÃ­cita; ejecuciÃ³n PostgreSQL pendiente. Los casos de prueba y autenticaciÃ³n siguen pendientes.

## Fixtures validados en PostgreSQL

Evidencias 07/08 confirman carga de dos departamentos y seis usuarios y repeticiÃ³n sin duplicados. Del hito de datos sigue pendiente preparar los diez casos ficticios cuando exista su creaciÃ³n auditada. PrÃ³ximo avance funcional: autenticaciÃ³n y autorizaciÃ³n; requiere configurar aplicaciÃ³n/tenant Entra ID para validaciÃ³n real.

## Cambio vigente: autenticaciÃ³n local

El hito 4 utiliza FastAPI con correo/contraseÃ±a, no Entra ID. API de sesiones, alta restringida, bootstrap y pruebas implementados. ValidaciÃ³n manual Docker y provisiÃ³n de Admin RH pendientes. GestiÃ³n completa de bajas y cambios de rol/departamento con reasignaciÃ³n de casos queda para el servicio administrativo. DespuÃ©s: registro/listado de incidencias con autorizaciÃ³n por departamento y confidencialidad.
