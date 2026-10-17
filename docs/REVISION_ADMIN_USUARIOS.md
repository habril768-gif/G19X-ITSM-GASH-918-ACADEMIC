# Administración de usuarios — revisión del 16 de octubre de 2026

API 0.8.0 aplicada y reconstruida según reporte de la autora; evidencia 38 inspeccionada confirma suite completa ejecutada por ella: 77 passed, 3 skipped, 1 warning in 16.49s. Las tres omitidas son las integraciones PostgreSQL optativas y no se declaran aprobadas; advertencia conocida de TestClient/httpx. La ejecución completa posterior sustituye el pendiente histórico de suite HTTP de este avance. No prueba concurrencia PostgreSQL. Evidencias 39–46 inspeccionadas: listado 200, desactivación y estado inactivo, reactivación y estado activo, rechazo de sesión anterior y nueva sesión RH permitida. La autora reporta prueba en dos pestañas con modificación administrativa desde la cuenta original; los recortes 401 no muestran identidad/token/solicitud previa, por lo que se documentan como respuestas consistentes con la secuencia reportada, sin afirmar causalidad exclusiva frente a expiración. No se observaron contraseñas ni tokens en las capturas revisadas. No se cambiaron .env ni datos por el asistente durante esta consolidación. No hay prueba manual nueva de cambio de rol, traslado con reasignación ni concurrencia; esas comprobaciones no se infieren de las capturas. RF-7 permanece parcial por frontend y administración de departamentos pendientes.

| Evidencia | Observación |
| --- | --- |
| [38](evidencias/38-suite-completa-77-passed.png) | Suite 77 aprobadas, 3 omitidas, 1 advertencia, 16.49s |
| [39](evidencias/39-admin-usuarios-listado-200.png) | Listado 200 con usuarios ficticios; recorte sin total/paginación |
| [40](evidencias/40-usuario-demo-desactivado-200.png) | Acuse 200, updated/sessions_revoked verdaderos, cases_adjusted=0 |
| [41](evidencias/41-usuario-demo-inactivo-listado-200.png) | Empleado Operaciones Dos Demo, is_active=false |
| [42](evidencias/42-usuario-demo-reactivado-200.png) | GET del mismo empleado, is_active=true; imagen reemplaza acuse anterior |
| [43](evidencias/43-sesion-revocada-401.png) | 401 posterior a logout reportado; no confundir con revocación administrativa |
| [44](evidencias/44-revocacion-administrativa-401.png) | 401 tras desactivación administrativa reportada de RH Independiente Demo |
| [45](evidencias/45-token-anterior-tras-reactivacion-401.png) | 401 con token anterior tras reactivación reportada |
| [46](evidencias/46-rh-reactivado-nueva-sesion-200.png) | /auth/me 200 con RH Independiente Demo, ADMIN_RH, tras nuevo login reportado |

La reactivación no restaura tokens revocados. sessions_revoked=true indica ejecución de revocación, no cuántas sesiones había. El intento de JSON inválido mostró 422 de formato y no se cuenta como actualización exitosa. La captura 42 actual es el GET con estado activo; el acuse que ocupaba antes ese nombre no se presenta como archivo independiente conservado. No es necesaria captura 42b. Las cabeceras UTC del 17 de octubre corresponden a la noche local del 16 de octubre.

Pendientes: PostgreSQL de pruebas para las tres integraciones, concurrencia real, pruebas manuales de reasignación por cambio de rol/departamento, UI y CRUD de departamentos. No se ejecutó de nuevo la suite durante esta revisión documental.
