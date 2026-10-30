# Prueba de rendimiento local

Estado vigente al 27/10/2026: **RNF-2 pendiente; siete formales completas FALLIDA_UMBRAL**. Ultima: 0769b0ce07b943e5, [evidencia 182](evidencias/182-septima-formal-completa-fallida-umbral.json); 9.603 solicitudes sin errores, p95 438,45/361,19/687,49/554,30 ms. Las referencias anteriores a seis formales describen el estado historico.

Actualizado: 27 de octubre de 2026.

**RNF-2 medido y todavía no cumplido.** Las seis corridas formales completaron su ventana sin errores HTTP, pero superaron el p95 menor de 200 ms en las cuatro operaciones. La última ya incluye el INSERT multirregistro de correo: mejoraron las cuatro operaciones frente a la anterior, sin alcanzar el umbral.

La regresión seleccionada más reciente pasó con **117 pruebas y 63 subpruebas en 22,73 s** ([176](evidencias/176-plantilla-detalle-regresion-117-aprobadas.json)), para la plantilla SQL de detalle sin datos por petición. La selección anterior 173 pasó con 111 pruebas/63 subpruebas para listado/detalle agrupados; no son conteos acumulables. La selección anterior 170 pasó con 98 pruebas/cuatro subpruebas para el rol agrupado posterior al bloqueo; los conteos no se acumulan. La selección anterior 167 pasó con 102 pruebas, incluidas las dos integraciones FastAPI nuevas de DTO en worker y las tres anteriores de sesión; son selecciones distintas y no acumulables. La selección 157 de 93 aprobadas corresponde al ajuste anterior. Las selecciones anteriores de rol y del INSERT multirregistro pasaron con 75 y 77, respectivamente; no son totales acumulables. Después del diagnóstico que mostró mejora localizada del INSERT (66,05 → 16,94 ms medios), la nueva formal completó 15349 solicitudes sin errores: p95 de listado 259,28 ms, detalle 221,32 ms, creación 385,49 ms y edición 347,43 ms. Son resultados todavía fuera del umbral.

Durante la revisión se evitó generar carga mientras la autora usaba Brave para una videollamada. Al indicar que estaba lista para retomar, una captura mostró CPU al 19 % y memoria al 86 %. Es contexto instantáneo previo, sin demostrar condiciones constantes durante el ensayo. No repetir la carga formal sin otro cambio o diagnóstico justificado; conservar criterio y resultados anteriores.

Después de la sexta formal se preparó la reutilización del rol validado dentro de cada operación de gestión: [evidencia 151](evidencias/151-gestion-rol-leido-una-vez.json). Perfil local de edición 7 → 6 consultas, creación sin cambios; seis comprobaciones locales y matriz de nueve destinatarios correctas. La regresión seleccionada de API ya pasó con 75 pruebas ([152](evidencias/152-gestion-rol-regresion-75-aprobadas.json)); el diagnóstico real [153](evidencias/153-gestion-rol-diagnostico-real.json) confirmó edición de 9 → 8 consultas y SELECT/roles de 2 → 1 por petición, con 229 solicitudes medidas sin errores. No hay nueva formal posterior y RNF-2 sigue pendiente.

El ajuste previo de [apertura asíncrona de Session](evidencias/156-sesion-apertura-sin-salto-hilo.json), basada en el diagnóstico 155: elimina solo el paso de construcción sin SQL; conserva el cierre bloqueante en worker con limiter independiente y protección ante cancelación AnyIO. Siete locales aprobadas inicialmente; la regresión seleccionada de 93 ([157](evidencias/157-sesion-asincrona-regresion-93-aprobadas.json)) ya incluye las tres integraciones reales AnyIO/FastAPI. La integración PostgreSQL/Docker del ajuste quedó observada en [164](evidencias/164-sesion-diagnostico-cuatro-hilos-resultados.json), con 249 peticiones medidas sin errores. La apertura no añade commit ni cambia permisos/auditoría/cola. No hay p95 formal nuevo ni mejora global de latencia demostrada. El cierre se registró como `other` en v3 y se confirmaron cuatro pasos por hilos en todos los grupos, frente a cinco antes.

El primer smoke tras el ajuste de sesión ([158](evidencias/158-sesion-smoke-arranque-incompleto.json), cc10cf1d32dd4a8d) quedó **INCOMPLETA** por ARRANQUE_QA_SALIDA_1, antes de migraciones/fixture/carga. No aportó tiempos por hilos y su parada no quedó confirmada. La comprobación posterior [159](evidencias/159-docker-disponible-qa-sin-contenedores.json) mostró Docker 29.6.1 disponible y cero contenedores para el filtro exacto del proyecto. No quedan contenedores de esa corrida por detener según esa consulta; causa concreta aún desconocida. La construcción explícita posterior [160](evidencias/160-imagen-qa-construida-diagnostico-pendiente.json) completó la imagen API usando caché; no prueba arranque completo ni explica el fallo histórico. El reintento [161](evidencias/161-segundo-fallo-arranque-qa-sin-medicion.json), 6bcb02bfdbe040ad, volvió a fallar en arranque sin generar carga y sin parada confirmada. La prueba posterior [162](evidencias/162-redes-direcciones-agotadas-limpieza-preparada.json) confirmó agotamiento actual de los pools predeterminados de direcciones. Es consistente con los fallos previos, cuyo stderr no se conserva. Los dos reportes permanecen intactos. La liberación real [163](evidencias/163-liberacion-real-dos-redes-qa.json) retiró dos redes QA vacías sin omitidas ni fallidas. El diagnóstico posterior [164](evidencias/164-sesion-diagnostico-cuatro-hilos-resultados.json) completó arranque y carga sin errores, con QA detenido. Incidencia de asignación de redes resuelta para esa corrida; cada nueva corrida reserva otras dos redes y requiere revisar capacidad o mantenimiento acotado antes de arrancar. La regresión 157 permanece aprobada y la última formal sigue siendo 150.

El diagnóstico anterior [164](evidencias/164-sesion-diagnostico-cuatro-hilos-resultados.json) confirmó la retirada del paso de apertura, integridad SQL/colas y cierre QA. Edición tuvo espera/retorno medios por hilos 32,71/32,02 ms, pero ASGI medio 269,85 ms y commit medio 66,42 ms (antes 215,31 y 11,14 ms en 155). CPU global media 68,02 %. No demuestra mejora global ni causa única; la revisión [165](evidencias/165-revision-alcance-commit-sin-sql-pendiente.json) ya comprobó el alcance de commit: una confirmación, sin SQL/flush dentro de ese intervalo en dos escenarios SQLite. El cronómetro termina antes de expiración/cierre; no identifica la causa PostgreSQL. El ajuste [166](evidencias/166-respuesta-validada-en-worker-preparada.json) ya agrupa ejecución y validación de DTO en un worker para las cuatro operaciones medidas, con ruta async y response_model conservados. Siete locales y 64 de herramientas aprobadas inicialmente; las dos integraciones nuevas y la regresión API seleccionada ya pasaron con 102 casos en [167](evidencias/167-respuesta-worker-regresion-102-aprobadas.json). La ejecución 168 ya liberó y verificó dos redes vacías antes del smoke; conservación de volúmenes y reportes mantenida. La integración real [168](evidencias/168-respuesta-worker-diagnostico-tres-hilos.json) ya confirmó tres pasos por hilo en los ocho grupos, con 236 peticiones medidas sin errores y QA detenido. HTTP p95 del smoke: listado 190,86, detalle 203,76, creación 465,74 y edición 488,66 ms; alcance corto instrumentado, sin acreditar RNF-2.

En 166, la métrica QA endpoint conserva medición dentro del worker, pero añade captura/validación de DTO al cuerpo de negocio; no incluye espera/retorno. Tener en cuenta ese cambio pequeño de alcance al compararla con 164. Los demás componentes siguen solapándose; no sumar p95. La regresión 167 de 102 aprobadas ya valida esta selección del nuevo cambio; la 157 de 93 corresponde al ajuste anterior. No son conteos acumulables.

El diagnóstico anterior [168](evidencias/168-respuesta-worker-diagnostico-tres-hilos.json), tras 102 pruebas seleccionadas aprobadas en 167, confirmó tres pasos por hilo y SQL 4/3/11/8 por listado/detalle/creación/edición. PostgreSQL: 190 casos/creaciones auditadas, 78 ediciones y 1900 entregas, cero SMTP/IA; diez logout 204 y QA detenido. HTTP p95 302,70/243,36/427,86/312,76 ms. Escritura mejoró y lectura empeoró respecto de 164, con CPU global media 84,20 %: sin mejora general demostrada o causa única. Commit de edición medio 11,89 ms, sin cambios de durabilidad; el pico anterior no se repitió. RNF-2 pendiente, sin nueva formal ni instrucción de repetir full automáticamente. Revisar viajes SQL y entorno antes de otro cambio/medición.

El ajuste posterior [169](evidencias/169-rol-agrupado-tras-bloqueo-preparado.json) incorpora el rol al SELECT fresco de usuario/departamento después del bloqueo administrativo. Solo creación/gestión solicitan ese retorno; los demás llamadores conservan su contrato. Perfil SQLite de servicios: creación 9 → 8 y edición 6 → 5 consultas, sin autenticación/advisory PostgreSQL; nueve unitarias locales aprobadas y regresión API seleccionada ya aprobada con 98 pruebas/cuatro subpruebas en [170](evidencias/170-rol-agrupado-regresion-98-aprobadas.json). Integración PostgreSQL QA observada en [171](evidencias/171-rol-agrupado-diagnostico-sql-confirmado.json): 202 peticiones medidas sin errores, ahorro SQL confirmado y QA detenido. QA confirmó creación 11 → 10 y edición 8 → 7, pero las latencias del diagnóstico empeoraron; no se acredita mejora de rendimiento. No cambia permisos, orden de locks, commit, auditoría o outbox, ni cachea autorización entre operaciones. Las 102 pruebas de 167 corresponden al código anterior. El smoke 171 ya se completó después de liberar dos redes QA vacías; no lanzar full o repetir smoke automáticamente.

El diagnóstico anterior [171](evidencias/171-rol-agrupado-diagnostico-sql-confirmado.json) confirmó ahorro SQL del rol agrupado: creación 10 y edición 7 consultas, tres pasos por hilo; listado/detalle 4/3. **202 peticiones medidas sin errores**, auditoría/colas consistentes y QA detenido. HTTP p95 366,18/273,95/760,44/423,13 ms, todos peores que 168. CPU global media 88,72 %, generador 0,76 %. Esto confirma la estructura SQL, sin mejora de latencia demostrada ni causa exclusiva. RNF-2 sigue pendiente; formal 150 FALLIDA_UMBRAL se conserva. No repetir cargas sin una nueva hipótesis o cambio justificado.

El ajuste posterior [172](evidencias/172-lecturas-listado-detalle-agrupadas-preparadas.json) reduce un viaje en listado y detalle: count+página en una sentencia y rol+caso autorizado en otra, respectivamente. Once locales aprobadas inicialmente; la regresión API seleccionada ya pasó con 111 pruebas/63 subpruebas en [173](evidencias/173-lecturas-agrupadas-regresion-111-aprobadas.json), incluida la matriz de permisos/orden/total vacío. Ejecución PostgreSQL y latencias observadas en [174](evidencias/174-lecturas-agrupadas-diagnostico-sql-confirmado.json); plan detallado no capturado. Listado local 3 → 2 y detalle 2 → 1 sin autenticación; QA confirmó listado 4 → 3 y detalle 3 → 2, manteniendo escrituras 10/7. No cambia autenticación ni cachea autorización. SQL más complejo requiere comprobar plan/latencia real: no deducir rendimiento del conteo. El diagnóstico 174 ya se ejecutó tras liberar dos redes vacías; no repetir full/smoke automáticamente.

El diagnóstico anterior [174](evidencias/174-lecturas-agrupadas-diagnostico-sql-confirmado.json) confirmó listado/detalle 3/2 consultas, escrituras 10/7 y tres pasos por hilo. **203 peticiones medidas sin errores**, auditoría/colas consistentes y QA detenido. HTTP p95 listado/detalle/creación/edición 285,30/347,96/474,43/371,37 ms: tres operaciones mejoran respecto de 171 y detalle empeora. CPU global media 83,16 %. SQL medio de detalle baja, pero endpoint/ASGI suben; revisar el tramo fuera del cursor, sin atribuir causa única ni deducir mejora general. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL conservada. No repetir cargas sin una hipótesis/cambio nuevo justificado.

El ajuste posterior [175](evidencias/175-detalle-plantilla-sql-parametrizada-preparada.json) reutiliza exclusivamente la estructura SQL de detalle con bindparams; cada llamada ejecuta la consulta con parámetros nuevos y relee permisos/datos. Perfil SQLite propio de treinta llamadas calientes: construcción/parámetros 7,53 → 0,005 ms y total 9,01 → 0,52 ms; no p95 HTTP/PostgreSQL ni mejora de llamada fría. Diecisiete unitarias locales aprobadas, seis nuevas de parámetros/rol/confidencialidad y dos sesiones concurrentes. La regresión API seleccionada ya pasó con 117 pruebas/63 subpruebas en [176](evidencias/176-plantilla-detalle-regresion-117-aprobadas.json); las 111/63 de 173 corresponden al código anterior. El diagnóstico real [177](evidencias/177-plantilla-detalle-diagnostico-endpoint-reducido.json) ya completó la integración tras liberar dos redes: endpoint medio de detalle 54,40 → 25,98 ms, sin mejora de p95 ni cumplimiento RNF-2. No repetir carga automáticamente. Sin nueva carga o acreditación RNF-2.

El diagnóstico más reciente [177](evidencias/177-plantilla-detalle-diagnostico-endpoint-reducido.json) completó **218 peticiones medidas sin errores**, SQL 3/2/10/7, tres pasos por hilo e integridad/parada correctas. El endpoint de detalle bajó de 54,40 a 25,98 ms medios y su mediana HTTP a 148,69 ms, pero p95 subió a 360,31 ms. HTTP p95 listado/detalle/creación/edición 588,84/360,31/479,34/313,43 ms, con CPU global media 80,43 %. Mejora localizada del endpoint, sin mejora global ni acreditación RNF-2. Esperas/residual siguen variables y no tienen causa exclusiva demostrada. No repetir cargas sin hipótesis/cambio justificado; formal 150 FALLIDA_UMBRAL conservada.

Revisión del 27/10 ([178](evidencias/178-formal-condicionada-preparada-cpu-previa-alta.json)): aplicación y regresiones siguen coincidiendo con sus hashes. Sin generar carga, CPU global media actual 70,29 % en tres intervalos; no iniciar otra corrida ahora. Se preparó un comando formal explícito con control previo (74 unitarias locales aprobadas), descrito abajo. No modifica aplicación ni umbral RNF-2. Última formal sigue siendo 150; el nuevo comando no se ha ejecutado en Docker real.

## Objetivo y alcance

El [PRD, RNF-2](PRD.md#8-requisitos-no-funcionales) exige p95 menor de 200 ms para lectura, creación y actualización simples con diez usuarios simultáneos, cien incidencias simuladas y cinco minutos sostenidos después de calentamiento, en Docker local. La creación incluye su encolado; la duración de proveedores externos queda fuera. No modificar el umbral para acomodar resultados.

Esta prueba mide latencia HTTP desde un generador local hasta recepción completa de la respuesta. Incluye transporte loopback, autenticación/autorización, aplicación y persistencia; no es tiempo de renderizado del navegador ni una medida exclusiva del servidor.

## Entorno separado

Antes de ejecutar debe existir un despliegue QA identificado, con proyecto Compose, volúmenes, red, puertos y credenciales propios. No usar los volúmenes de la plataforma actual ni restaurar encima de ella. Verificar recursos resueltos antes de arrancar. Registrar versión de código o hashes si Git no está disponible, versiones de imágenes y migración, sistema operativo, CPU, RAM, recursos asignados a Docker, almacenamiento, ubicación del generador y otros servicios activos.

La base QA debe estar vacía antes de migrar. Comprobar /health y /health/db. Mantener IA externa y SMTP externos desactivados; no iniciar workers de proveedores. Documentar la configuración real de encolado y comprobar su comportamiento: no excluir artificialmente la inserción de trabajos de la creación. Si se mide solo el modo IA desactivada, declarar ese límite; no afirmar rendimiento con IA activada. No cambiar configuración a mitad de la medición.

Usar diez cuentas ficticias activas de ADMIN_RH independientes, sin relaciones ni afectación personal en los casos; un departamento ficticio activo. Iniciar sesión mediante /auth/login, con una sesión diferente por cuenta. No sustituir current_user/get_session: se requiere la API real contra PostgreSQL de QA. Tokens y contraseñas solo en memoria del ejecutor; no incluirlos en evidencia, URLs o logs. Cerrar sesiones al terminar si la API responde.

Preparar exactamente cien casos ENTORNO iniciales, no confidenciales y sin afectados/participantes, diez por usuario. Cada usuario modifica únicamente sus diez casos reservados para evitar conflictos de actualización en esta prueba de operaciones simples. Las pruebas de carreras sobre un mismo objeto son distintas. Registrar cantidad y tamaño aproximado de textos y filas auxiliares; usar solo datos simulados.

## Carga y operaciones

El generador será cerrado: diez clientes concurrentes, una petición activa por cliente, conexiones persistentes y sin reintentos automáticos. No confundir diez clientes con diez peticiones por segundo. El rendimiento observado depende del equipo; registrar solicitudes por segundo y distribución de operaciones. El recorrido HTTP real y las cinco corridas formales están documentados abajo; las pruebas locales de herramientas no equivalen a latencia de la aplicación.

Cada cliente repite esta secuencia:

| Operación | Solicitud API directa | Éxito esperado |
| --- | --- | --- |
| Listado | GET /incidents?page=1&page_size=20 | 200; estructura y límite de página válidos |
| Detalle | GET /incidents/{id_reservado} | 200; mismo ID |
| Creación | POST /incidents con título, descripción, fecha, scope ENTORNO y departamento QA | 201; recibo con ID; comprobar persistencia fuera de ventana |
| Actualización | PUT /incidents/{id_reservado}/content con título/descripción simulados que cambian por vuelta | 200; contenido esperado en respuesta |

Rotar los diez IDs reservados por usuario. Actualizar casos pendientes permitidos por el ciclo, sin enviar clasificación, asignación o transiciones extra para facilitar la medición. Validar previamente un recorrido completo de cada operación en el fixture; abortar si no se cumplen los éxitos esperados.

Calentar durante 30 segundos con los diez clientes. Separar todos los registros de calentamiento y excluirlos de estadísticas. Las escrituras de calentamiento permanecen en la base y deben contarse. Después medir 300 segundos con el mismo entorno. La población inicial es de cien incidencias; creación aumenta ese total. Registrar conteo después de calentamiento y al final; no presentar el conjunto como fijo ni borrar casos durante la medición. Rotar fecha/títulos solo con datos ficticios.

Usar reloj monotónico de alta resolución. No lanzar peticiones nuevas al vencer los 300 segundos; recoger las que ya estaban en vuelo con tiempo límite de diez segundos por petición. Registrar ventana efectiva y peticiones que concluyen después del corte por separado. No omitir las lentas ni excluir errores para mejorar el p95.

## Resultados y criterio

Registrar por operación: número de intentos, éxitos, errores HTTP, excepciones, timeouts, estados HTTP, tasa de error, solicitudes por segundo, mínimo, mediana, p95, p99 y máximo. p95 por rango más cercano: ordenar duraciones y tomar índice ceil(0.95 × n) - 1. Separar listado y detalle; un promedio global no basta. Conservar duración hasta fallo y timeouts; informar percentiles de éxitos junto con fallos, nunca como si estos no existieran.

La propuesta de aprobación exige que cada una de las cuatro operaciones tenga muestras, p95 de éxitos inferior a 200 ms, cero errores inesperados y exactamente diez clientes activos durante los cinco minutos. Umbral y concurrencia proceden del PRD; exigir cero errores inesperados es un criterio adicional de este protocolo. Falta de muestras, duración insuficiente o clientes caídos significa prueba incompleta. Una respuesta 401/403/404/409/422 inesperada no cuenta como éxito de rendimiento. No relajar reglas de negocio para obtener cifras mejores.

Registrar CPU/memoria de contenedores al inicio y durante la ejecución con baja frecuencia, y verificar que el generador no sea el cuello de botella. El muestreo añade carga y debe declararse. Si hay errores o saturación, conservar el resultado, diagnosticar y repetir únicamente después de un cambio justificado. No elegir la mejor corrida ocultando las anteriores.

Al terminar comprobar conteos y muestras de contenido/auditoría, salud de la base y ausencia de solicitudes a proveedores externos según el alcance observado. Detener solo recursos QA identificados; no ejecutar down -v sobre el proyecto de uso. No borrar evidencia o recursos de una ejecución fallida automáticamente.

## Evidencia mínima

El reporte debe contener identificador único, fecha real, estado (aprobada, fallida o incompleta), configuración sin secretos, hardware, versión de código/imágenes, modo de proveedores/encolado, número de usuarios/clientes, conteos de casos, calentamiento y duración medida. Añadir tabla de métricas por operación, errores sanitizados, observaciones, comprobaciones posteriores y recursos QA detenidos o retenidos. Guardar los agregados; no guardar credenciales, cookies, tokens, datos personales ni cuerpos completos de expedientes.


## Herramientas y uso actual

El recorrido normal usa [provision_performance_qa.py](../backend/scripts/provision_performance_qa.py), [performance_runner.py](../backend/scripts/performance_runner.py) y [performance_seed.py](../backend/scripts/performance_seed.py). Los comandos siguientes son referencia para cuando se retomen las mediciones; no son una instrucción de ejecutarlos durante la videollamada.

### Entorno y custodia de recursos

Desde la raíz del repositorio y con Docker Desktop disponible, el provisionador valida un contexto Docker local y crea un proyecto `plurione-qa-perf-<run_id>`, volúmenes, dos redes y un puerto nuevos. PostgreSQL y Redis quedan en red interna propia, sin puertos publicados; la API también usa una red de entrada bridge y publica solo un puerto alternativo en `127.0.0.1`. Rechaza colisiones y recursos ajenos. No utiliza el puerto de la instalación operativa.

El API de QA tiene salida de red posible por su red de entrada; proveedores desactivados no equivalen a un bloqueo de red. No se configuran claves ni workers externos. Después del build y migraciones se comprueban `/health` y `/health/db` desde el host antes de crear datos. Solo se reintentan lecturas de salud, nunca escrituras inciertas de carga.

El fixture genera contraseñas aleatorias en memoria y crea diez cuentas/cien casos mediante el servicio real, con auditoría y cola. El seed se envía como código fijo al intérprete de la imagen y contraseñas por stdin. Manifiesto y reporte no guardan valores de contraseñas; los metadatos privados de los contenedores sí retienen su contraseña de base. No publicar `docker inspect` sin filtrar. Esto no sustituye la custodia de una instalación permanente.

Al finalizar se verifican conteos SQL de casos, auditoría y entregas, ausencia de intentos SMTP/trabajos IA según este alcance, y sesiones revocadas. El provisionador intenta detener solo su proyecto y conserva volúmenes/imágenes y `.pgdata/performance-<run_id>/report.json`. No hace `down`/`rm` ni borra evidencia fallida. Una parada no confirmada no se informa como éxito. Su eliminación futura es una operación separada; no eliminar volúmenes operativos.

### Elegir una comprobación

Plan sin Docker, credenciales ni archivos nuevos:

```powershell
.ackend.venvScriptspython.exe -B backend/scripts/provision_performance_qa.py --plan
```

Línea base global Windows de solo lectura, unos seis segundos, sin generar carga:

```powershell
.ackend.venvScriptspython.exe -B backend/scripts/performance_host.py --baseline
```

Tres intervalos; media ponderada solo con los válidos. Las lecturas ausentes son `null`, no cero. El script no identifica procesos ni recrea una corrida previa. No se exige un nuevo porcentaje arbitrario de CPU para aprobar RNF-2: sirve para documentar condiciones e interpretar la siguiente medición.

Sondeo opcional de procesos actuales, unos cinco segundos:

```powershell
.ackendscriptscheck_performance_host.ps1
```

Es de solo lectura. Puede omitir procesos nuevos, terminados o inaccesibles. El top visible no es CPU global; no usarlo para terminar procesos por nombre ni atribuir consumo de una corrida anterior. Mantener los servicios necesarios para la aplicación y evitar interrumpir el trabajo de la autora.

Smoke funcional: fixture nuevo, 2 s de calentamiento y 5 s medidos:

```powershell
.ackend.venvScriptspython.exe -B backend/scripts/provision_performance_qa.py --mode smoke --confirm-isolated-qa
```

Diagnóstico instrumentado actual (v3), con la misma carga breve y recursos nuevos:

```powershell
.ackend.venvScriptspython.exe -B backend/scripts/provision_performance_qa.py --mode smoke --diagnostic --confirm-isolated-qa
```

Medición formal, solo después de un cambio justificado/regresión y revisión de condiciones:

```powershell
.ackend.venvScriptspython.exe -B backend/scripts/provision_performance_qa.py --mode full --confirm-isolated-qa
```

`full` conserva 30 s de calentamiento y 300 s medidos. La construcción/fixture puede tardar varios minutos; hay límites por etapa y no se debe repetir o interrumpir solo porque el build no muestra detalle. Cada corrida crea un conjunto nuevo; nunca reutiliza los casos ya aumentados de un smoke para `full`. Conservar y analizar cualquier reporte incompleto antes de repetir. No se sobrescriben reportes existentes.

### Ejecutor sin provisionador: uso avanzado

El [manifiesto de ejemplo](../backend/scripts/performance_manifest.example.json) usa IDs ficticios y `isolated_resources_confirmed=false`; no es carga ejecutable. Una copia privada requiere proyecto QA y metadatos reales de hardware/código/imágenes/proveedores. Confirmar aislamiento solo después de verificarlo. Las cuentas son `qa-perf-<run_id>-0@example.invalid` hasta `-9`; cien casos iniciales exclusivos con título `QA-PERF-<run_id>-`, diez por cuenta, creados por ella, ENTORNO, pendientes, sin confidencialidad ni participantes. Definir contraseñas únicamente en variables privadas `PLURIONE_PERF_PASSWORD_0` a `_9`; no copiarlas a manifiesto, comandos compartidos o evidencia.

```powershell
.ackend.venvScriptspython.exe -B backend/scripts/performance_runner.py --manifest RUTA_MANIFIESTO_QA.json --report RUTA_REPORTE_SMOKE_NUEVO.json --confirm-isolated-qa --smoke
```

El ejecutor directo no crea/inspecciona/detiene Docker ni verifica SQL; esas tareas las hace el provisionador. Para formal se omite `--smoke`, con fixture y recursos nuevos validados. No reutilizar el conjunto que modificó el modo corto.

### Estados del reporte

| Estado | Interpretación |
| --- | --- |
| `FALLIDA_UMBRAL` | Carga completa cuyo p95 supera el criterio; no aprobación. |
| `SMOKE_SIN_ACREDITAR_RNF2` | Recorrido corto satisfactorio, sin acreditar RNF-2. |
| `DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2` | Agregados breves completos y coherentes, sin acreditar RNF-2. |
| `APROBADA_ALCANCE_HTTP_QA` | Cumple el alcance HTTP implementado; requiere revisar recursos/configuración/colas y no es aceptación integral. |
| `INCOMPLETA`, `INTERRUMPIDA`, `INCOMPLETA_DIAGNOSTICO`, `INCOMPLETA_PARADA_QA` | No cumplen su recorrido; conservar resultado y diagnóstico. |

## Interpretar el diagnóstico actual (v3)

La entrada ASGI optativa es `app.core.performance_diagnostics:app`; `app.main` permanece sin instrumentar. El guard exige run_id/base/usuario QA concordantes, host `postgres` y proveedores desactivados. `--diagnostic` se limita a `smoke`. Las cabeceras de fase se añaden solo a la carga; login, preflight y verificaciones quedan fuera de los grupos. No se reemplazan autenticación, autorización o Session por dobles en la corrida real.

`diagnostico.grupos.<fase/operacion>` contiene número de solicitudes y medias/p95/máximos de:

| Medida | Qué incluye y límites |
| --- | --- |
| `auth` | Ejecución de la dependencia real `current_user`; incluye parte del tiempo SQL. |
| `endpoint` | Ejecución de la función de la ruta; incluye servicios, SQL y commit dentro de ella. |
| `sql` / `consultas` | Tiempo de cursor y cantidad instrumentada. Excluye pool/pre_ping interno y parte ORM; incluye esperas durante execute, no solo CPU PostgreSQL. |
| `commit` | Desde before_commit hasta after_commit, incluido flush. Se solapa con endpoint/SQL. |
| `hasta_envio` | Hasta entregar el último cuerpo a ASGI send; no recepción completa del cliente. |
| `cierre` | Resto hasta terminar la aplicación, potencialmente con limpieza de dependencias. |
| `total` / `fuera_auth_endpoint` | Tiempo ASGI completo y residual fuera de funciones instrumentadas. Puede exceder tiempo HTTP por tareas posteriores al envío. |

No sumar los componentes solapados ni restar sus p95. Medias, p95 ASGI y p95 HTTP son medidas distintas. La instrumentación añade coste y sus muestras breves no acreditan RNF-2.

`familias_sql` usa verbo y tablas de una lista fija; no guarda SQL, parámetros, literales o IDs de casos. Informa cantidad/tiempo total y medias por petición/consulta. Puede agrupar consultas distintas o marcar otras; no equivale a huella exacta ni EXPLAIN. El provisionador exige que sus sumas coincidan con cantidad y tiempo SQL global y coteja los ocho grupos con HTTP. Al shutdown se imprime solo el agregado marcado; se lee después de detener QA. Un agregado ausente, truncado, incoherente o anterior a v3 no se acepta como nuevo diagnóstico v3. Los reportes anteriores conservan su versión y validez histórica.

`http.<fase>.cpu_generador_host` distingue CPU de todos los hilos del generador (`time.process_time`, por un núcleo y normalizada por CPU lógicas) y CPU global Windows (`GetSystemTimes`). El host incluye otras aplicaciones/VM; son medias de fase, sin atribución exclusiva. Medidas ausentes se conservan como `null`. Las corridas normales no añaden este sondeo. `recursos` conserva muestreo Docker CPU/memoria de baja frecuencia, que también añade carga. No interpretar CPU mayor de 100 % de un contenedor como porcentaje de todo el equipo sin normalización.

### Espera y retorno de hilos (v3)

La [evidencia 154](evidencias/154-diagnostico-esperas-hilos-preparado.json) preparó esta ampliación y la primera integración real [155](evidencias/155-diagnostico-hilos-resultados.json) completó su alcance: 224 solicitudes medidas sin errores, ocho grupos y sumas concordantes, sin llamadas de hilo incompletas. Se instrumenta `anyio.to_thread.run_sync` únicamente en el proceso de la entrada QA protegida. Fuera de contexto de carga se delega al original. No se cambian `app.main`, permisos, consultas, bloqueos, argumentos/opciones de cancelación o capacidad del limiter.

`thread_stages` agrupa llamadas por categorías fijas: `auth`, `endpoint`, `response_validation`, `dependency_enter`, `dependency_exit` y `other`. Cada etapa informa `calls`, `wait_ms`, `run_ms`, `resume_ms`, `incomplete` y medias por petición. Las métricas globales equivalentes son `thread_calls`, `thread_wait`, `thread_run`, `thread_resume` y `thread_incomplete`. No se guardan nombres arbitrarios, argumentos, tokens, resultados o mensajes de excepción.

Espera: desde programar el trabajo hasta entrar en el worker; puede incluir limiter y planificación. Ejecución: cuerpo dentro del hilo, que contiene SQL/servicios según la etapa. Retorno: desde terminar el cuerpo hasta reanudar la corutina; puede incluir event loop/planificación. No distingue por sí solo causa de SO, CPU o cola y no se suma con componentes solapados. Una llamada incompleta o sumas discordantes invalidan el diagnóstico. Se conservan retornos/excepciones originales y no se reintenta.

Validación local: **56 pruebas aprobadas en 1,251 s**, ocho nuevas, con tiempos/dobles y un hilo real para contexto. No acredita integración FastAPI/AnyIO real ni rendimiento. La corrida real [155](evidencias/155-diagnostico-hilos-resultados.json) ya está revisada; no repetirla ni lanzar otra formal automáticamente. El ajuste 156 reduce solo la apertura; su regresión seleccionada ya pasó en 157; corresponde un smoke diagnóstico antes de valorar otra formal.

El resultado [155](evidencias/155-diagnostico-hilos-resultados.json) muestra cinco pasos por hilo en edición: espera media 42,09 ms, retorno 36,24 ms y ejecución 130,01 ms, dentro de 215,31 ms medios ASGI. Apertura de sesión (`dependency_enter`) ejecuta 0,043 ms pero espera/retorna en unos 15,00 ms; validación de respuesta ejecuta 0,017 ms pero espera/retorna en 13,85 ms. Cierre ejecuta 0,049 ms y espera/retorna en 17,71 ms, posterior al envío en este recorrido de escritura. No confundir ese cierre con latencia HTTP ni asumir que cerrar una lectura con rollback es no bloqueante.

Esto orienta a reducir saltos de tareas pequeñas; no autoriza pasar SQL/commit/rollback al event loop ni eliminar validación o limpieza. CPU host media 80,26 %, sin atribuir por sí sola causa o saturación del limiter. RNF-2 continúa pendiente.

## Resultados formales conservados

Todas las siguientes corridas usaron diez clientes y completaron 30 + 300 s con cero errores HTTP. **Todas siguen fuera del umbral en las cuatro operaciones.** Valores p95 HTTP en milisegundos; no elegir la mejor corrida ocultando las otras.

| Configuración del cambio acumulado | Solicitudes medidas | Listado | Detalle | Creación | Edición | Evidencia |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Línea base | 7813 | 283.08 | 253.94 | 1245.89 | 476.01 | [126](evidencias/126-rendimiento-formal-fuera-umbral.json) |
| Encolado agrupado | 11226 | 301.76 | 267.72 | 608.95 | 485.95 | [129](evidencias/129-rendimiento-encolado-comparacion.json) |
| Autenticación agrupada | 13072 | 236.55 | 206.16 | 521.57 | 398.67 | [132](evidencias/132-rendimiento-auth-comparacion.json) |
| Respuesta antes del commit | 14346 | 249.83 | 217.49 | 449.40 | 358.22 | [136](evidencias/136-rendimiento-respuestas-comparacion.json) |
| Relectura administrativa | 13873 | 286.91 | 258.43 | 505.98 | 393.49 | [141](evidencias/141-rendimiento-relectura-administrativa.json) |
| INSERT multirregistro de correo | 15349 | 259.28 | 221.32 | 385.49 | 347.43 | [150](evidencias/150-rendimiento-formal-correo-multirregistro.json) |

El equipo declarado en los reportes tiene cuatro CPU lógicas; Docker cuatro CPU y aproximadamente 3,77 GB de memoria asignada. Windows y generador comparten el host con Docker, sin límites exclusivos por contenedor. El conjunto crece y termina con cantidades distintas en cada corrida; los cambios de carga del host no se controlaron de forma exclusiva. Comparaciones observacionales, sin atribución causal única.

La última corrida formal ([150](evidencias/150-rendimiento-formal-correo-multirregistro.json)) terminó con 4341 casos y creaciones auditadas, 4231 ediciones, 43410 entregas, cero intentos SMTP y cero trabajos IA. Diez sesiones revocadas con 204 y QA detenido. Incluye la inserción multirregistro. Se conservan los resultados anteriores, sin sustituirlos por esta corrida.

## Ajustes y validación: estado actual

| Ajuste | Validación disponible | Límite |
| --- | --- | --- |
| Selección agrupada de destinatarios y IDs existentes | [127](evidencias/127-encolado-consultas-agrupadas.json), regresión 60 aprobadas [128](evidencias/128-regresion-encolado-60-aprobadas.json); corrida formal [129](evidencias/129-rendimiento-encolado-comparacion.json) | Preserva controles de worker; no acredita RNF-2. |
| Lectura agrupada de sesión/usuario/departamento en autenticación | [130](evidencias/130-autenticacion-consulta-agrupada.json), 22 pruebas aprobadas [131](evidencias/131-autenticacion-22-aprobadas.json); formal [132](evidencias/132-rendimiento-auth-comparacion.json) | Sin caché de revocación/actividad; umbral pendiente. |
| Captura de recibo/CaseDetail antes del commit | [133](evidencias/133-respuestas-escritura-sin-recarga.json), errores de preparación y corrección [134](evidencias/134-regresion-escritura-correccion-fixtures.json), 11 aprobadas [135](evidencias/135-respuestas-escritura-11-aprobadas.json); formal [136](evidencias/136-rendimiento-respuestas-comparacion.json) | Éxito solo tras commit; retorno ORM por defecto y expiración conservados. |
| Relectura agrupada tras el advisory lock | [139](evidencias/139-relectura-administrativa-agrupada.json), regresión 128 aprobadas [140](evidencias/140-regresion-administrativa-128-aprobadas.json); formal [141](evidencias/141-rendimiento-relectura-administrativa.json) | Misma clave/orden compartido o exclusivo; ahorro local no mejoró el p95 formal observado. |
| INSERT VALUES múltiple de MailDelivery, lotes de 50 | [144](evidencias/144-correo-insert-multirregistro.json), regresión 77 aprobadas [145](evidencias/145-correo-multirregistro-77-aprobadas.json) y diagnóstico real [146](evidencias/146-diagnostico-correo-mejora-host-alto.json) | IDs/destinatarios/idempotencia/atomicidad conservados. Compilación PostgreSQL, ejecución QA y formal [150](evidencias/150-rendimiento-formal-correo-multirregistro.json) observadas; p95 aún fuera de umbral. |

El ajuste posterior de [lectura única del rol en gestión](evidencias/151-gestion-rol-leido-una-vez.json) mantiene el predicado y la revalidación tras bloqueo, sin caché entre peticiones. Sus seis casos nuevos están incluidos en las 75 pruebas aprobadas de [152](evidencias/152-gestion-rol-regresion-75-aprobadas.json). La selección 77 aprobada corresponde al ajuste anterior; no sumar ambas como casos únicos.

Los conteos de pruebas son selecciones diferentes y solapadas, no una suma de pruebas únicas ni una suite completa. Las regresiones API usan fixtures/dobles y no acreditan carreras/advisory locks reales de PostgreSQL. La selección 152 incluye seis casos nuevos de rol y el fallo del INSERT real, con rollback de caso/auditoría/cola; la más reciente, 157, añade la validación seleccionada de sesión asíncrona.

La inserción de correo pasó de 66,05 ms medios por petición ([143](evidencias/143-diagnostico-familias-cpu-resultados.json)) a 16,94 ms ([146](evidencias/146-diagnostico-correo-mejora-host-alto.json)), aproximadamente −74,4 %. Se mantuvieron diez entregas por creación y cero SMTP/IA. Sin embargo, el host pasó de 73,64 % a 95,27 % de CPU media y empeoró la latencia general del diagnóstico. Es una mejora localizada, no una aprobación o mejora global demostrada.

Herramientas: evolución del ejecutor/provisionador en [121](evidencias/121-ejecutor-rendimiento-unitarias.json) y [122](evidencias/122-provisionador-rendimiento-unitarias.json); diagnóstico por etapas [137](evidencias/137-diagnostico-etapas-qa-preparado.json)–[138](evidencias/138-diagnostico-etapas-qa-resultados.json), ampliación por familias/CPU [142](evidencias/142-diagnostico-familias-cpu-preparado.json) y resultados [143](evidencias/143-diagnostico-familias-cpu-resultados.json). La selección local más reciente de herramientas es 48 pruebas aprobadas en 1,880 s ([147](evidencias/147-sondeo-procesos-baseline-global.json)), con CPU sintética y Docker/ASGI simulados, no tiempos del producto.

El diagnóstico [153](evidencias/153-gestion-rol-diagnostico-real.json) confirmó el ahorro de consultas en PostgreSQL QA. CPU global media 81,06 %; edición ASGI media 247,80 ms, con autenticación 49,56 ms, endpoint 110,98 ms y residual 87,25 ms. Son medias de componentes, no p95 formal ni atribución causal. La siguiente revisión se centra en costes comunes antes de repetir carga formal.

## Condiciones del equipo y siguiente medición

Los sondeos posteriores no reconstruyen retrospectivamente las corridas. La lista parcial de procesos ([147](evidencias/147-sondeo-procesos-baseline-global.json)) dio 214 lecturas no disponibles; su top 10 no era CPU global. La línea base global posterior ([148](evidencias/148-cpu-global-baseline-97-4.json)) sí informó media de 97,42 % en tres intervalos sin generar carga; no significa que otras aplicaciones estuvieran inactivas ni identifica al responsable.

Después la autora compartió capturas del Administrador de tareas: primero CPU 76 %/memoria 91 %, y finalmente CPU 32 %/memoria 84 % durante una videollamada en Brave. Conservar esa actividad necesaria; no detener servicios Windows, SQL Server o PostgreSQL por su nombre. Estas capturas no miden p95 ni descartan problemas del producto.

La medición se retomó después de que la autora indicó estar lista; la corrida [150](evidencias/150-rendimiento-formal-correo-multirregistro.json) constituye la sexta formal y sigue fallida por umbral. Registrar condiciones y evitar carga durante actividades necesarias como la videollamada. El próximo paso es revisar coste restante y escoger un cambio justificado, no repetir suites o `full` sin cambios. Cualquier nuevo resultado fallido se conserva y analiza.

Para cerrar RNF-2 falta acreditar p95 menor de 200 ms en las cuatro operaciones durante la ventana formal y revisar hardware, recursos, errores, auditoría/colas y alcance. Si vuelve a fallar, mantener el requisito pendiente, sin relajar permisos, auditoría, encolado o el umbral.

## Mantenimiento de redes QA

Las corridas retienen redes además de volúmenes. Detener contenedores no garantiza liberar rangos; el error `all predefined address pools have been fully subnetted` impide crear otra red. La herramienta de [162](evidencias/162-redes-direcciones-agotadas-limpieza-preparada.json) permite revisar sin modificar:

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/release_performance_networks.py
```

Para retirar hasta dos redes elegibles (predeterminado):

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/release_performance_networks.py --apply --limit 2
```

Solo considera redes QA bridge/local vacías, con nombres y etiquetas Compose exactos y reporte/configuración originales bajo .pgdata. Revalida por ID antes de eliminar; una red conectada se omite o Docker rechaza su eliminación. No detiene/elimina contenedores, volúmenes, imágenes ni reportes, y no hace prune global. `redes_elegibles`, `eliminadas`, `omitidas_al_revalidar` y `fallidas` permiten revisar el resultado. Si no hay elegibles, no ampliar el alcance automáticamente: revisar vínculos de los contenedores QA y conservar datos. Las 63 unitarias son con Docker simulado; la primera ejecución real [163](evidencias/163-liberacion-real-dos-redes-qa.json) retiró dos redes sin errores. Sus 28 elegibles eran el inventario previo de redes QA reconocidas, no redes eliminadas ni inventario global. El contexto se fija y debe ser local. No cambiar subredes globales ni repetir carga mientras siga el fallo.


## Corrida formal con control previo

Los cambios posteriores a 150 están validados en selecciones de API y diagnósticos, pero no se ha medido el conjunto actual durante la ventana formal. La [herramienta de 178](evidencias/178-formal-condicionada-preparada-cpu-previa-alta.json) evita iniciarla con CPU previa ya alta. Ejecutar manualmente cuando haya menos actividad en el equipo:

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/run_performance_full_guarded.py --confirm-isolated-qa
```

Primero toma tres intervalos de dos segundos, sin generar carga. Deben ser válidos, con media ponderada <=30 % y cada intervalo <=50 %. Es una condición operativa de arranque, independiente del requisito p95<200 ms con diez clientes; no acredita RNF-2 ni demuestra estabilidad durante construcción o medición. La línea base del 27/10, ejecutada por el agente, dio 70,29 % y no justifica una nueva carga inmediata.

Si no cumple, imprime NO_INICIADA_CPU_PREVIA y termina con código 2 sin comandos Docker, limpieza o carga. Si cumple, comprueba contexto local y aplica la limpieza existente de hasta dos redes QA vacías registradas. Solo continúa si se retiraron dos sin fallos ni omitidas; de otro modo imprime NO_INICIADA_REDES_QA y termina sin carga. Conserva contenedores, imágenes, volúmenes y reportes. No usa prune global ni repite intentos.

Cuando todo cumple, ejecuta una sola formal sin la instrumentación de API de los diagnósticos: 30 s de calentamiento y 300 s de medición, con el resto del protocolo sin cambios. Construcción/migraciones/fixture añaden tiempo antes de la carga. precondiciones_arranque guarda línea base, umbrales operativos y redes liberadas en el reporte nuevo. El muestreo Docker existente sigue presente. La línea base es previa a construcción: no asegura CPU baja durante toda la corrida, por lo que el resultado y las condiciones requieren revisión. Un resultado fallido se conserva; cumplir la guardia no cambia el veredicto. Las 74 unitarias usan Docker/CPU simulados; integración real del nuevo comando pendiente.


## Antecedentes y fuentes

Los primeros smoke fallidos de conectividad/keep-alive se conservan en [123](evidencias/123-smoke-qa-conexion-rechazada.json) y [124](evidencias/124-smoke-qa-calentamiento-incompleto.json). El smoke funcional satisfactorio [125](evidencias/125-smoke-rendimiento-real-satisfactorio.json) valida su alcance corto; no acredita RNF-2. Los cambios de red y renovación de sockets están descritos en esas evidencias. La causa de cada fallo no se amplía más allá de lo observado.

Reportes originales: `.pgdata/performance-<run_id>/report.json`, fuera de Git y sin sobrescritura. Los JSON de evidencia enlazados contienen IDs, hashes y límites; [BITACORA.md](BITACORA.md) conserva el historial de avances y correcciones. El presente documento consolida el estado vigente en el mismo archivo, sin crear versiones paralelas.

Referencias de contexto del entorno, sin sustituir las pruebas: [red de Docker Desktop](https://docs.docker.com/desktop/features/networking/networking-how-tos/), [publicación de puertos](https://docs.docker.com/engine/network/port-publishing/) y [Uvicorn](https://www.uvicorn.org/).


## 27 de octubre de 2026 — Formal no iniciada por CPU previa del usuario

[Evidencia 179](evidencias/179-formal-no-iniciada-cpu-previa-usuario.json): ejecución real del comando condicionado compartida por el usuario, estado **NO_INICIADA_CPU_PREVIA**. Tres intervalos válidos: 77,82/94,93/78,52 %, media ponderada **83,74 %**. Supera los límites operativos de media <=30 % e intervalo <=50 %. El flujo se detuvo antes de Docker, limpieza o carga; no produjo séptima formal ni p95 nuevo. Se comprobó el rechazo real por CPU alta; el camino con CPU baja y la formal completa siguen pendientes.

Sin cambios de aplicación o herramientas ni nuevas pruebas de API. Se conservan las seis formales FALLIDA_UMBRAL, las 117 pruebas/63 subpruebas de 176 y el criterio RNF-2 p95<200 ms por operación con diez clientes. El requisito continúa pendiente. La medición no identifica procesos responsables ni explica retrospectivamente las formales. Siguiente paso: observación actual de solo lectura o esperar a menor actividad; preservar Brave si continúa la videollamada y evitar reintentos en bucle.


## 27 de octubre de 2026 — Sondeo parcial de procesos tras rechazo de arranque

[Evidencia 180](evidencias/180-sondeo-procesos-lecturas-incompletas.json): salida aportada por el usuario, 5,34 s, cuatro CPU lógicas, 156 procesos comparados y 201 lecturas no disponibles (no necesariamente procesos distintos). Diez consumos visibles suman aproximadamente 8,12 %; máximo Docker Desktop 4,31 %. No es CPU global ni muestra simultánea con el 83,74 % de 179, por lo que no identifica responsable ni demuestra una contradicción. La frase genérica del script «posterior a la carga» no acredita carga nueva: el intento 179 no inició.

Sin cambios de código, carga o pruebas adicionales. RNF-2 pendiente, seis formales conservadas. Pendiente: observar CPU global y procesos simultáneamente en Administrador de tareas, orden descendente por CPU, sin cerrar servicios por conjetura ni afectar la videollamada. No repetir benchmarks mientras se identifica la actividad del equipo.


## 27 de octubre de 2026 — Arranque QA incompleto; excepciones y tiempos distinguibles

[Evidencia 181](evidencias/181-arranque-incompleto-diagnostico-excepciones.json): tras detener desarrollo, CPU previa 28,35 % y dos redes QA retiradas sin errores permitieron iniciar 66f8604531244a51. Resultado INCOMPLETA / ARRANQUE_QA_NO_COMPLETADO, antes de migraciones, fixture y carga; parada confirmada. API creada 20:38:31 UTC, iniciada 20:38:38 y detenida 20:38:46 con salida 0, sin OOM y check /health correcto. Redis tuvo dos PONG y salida 0; PostgreSQL listo y luego detenido ordenadamente. No demuestra un fallo de salud durante arranque. La fecha inicial del reporte no marca el comienzo exacto de compose up; el codigo anterior agrupaba TimeoutExpired/OSError y no permite confirmar retrospectivamente cual ocurrio.

Se distingue ahora *_TIEMPO_AGOTADO de *_ERROR_INVOCACION y se guarda arranque_qa con inicio/fin UTC, duracion, limite y resultado. Limite de 900 s y carga formal sin cambios; no se publican stdout/stderr/argumentos privados. **76 unitarias locales aprobadas en 2,722 s**, dos nuevas; Docker simulado y AST valido. Sin nueva ejecucion Docker/carga ni cambios de producto. Reporte original preservado con hash. RNF-2 pendiente; no septima medicion formal completada. Pendiente: un intento explicito condicionado con diagnostico preciso, sin bucle ni aumento especulativo de plazo.


## 27 de octubre de 2026 — Septima formal completa: FALLIDA_UMBRAL

[Evidencia 182](evidencias/182-septima-formal-completa-fallida-umbral.json), run 0769b0ce07b943e5: CPU previa 21,53 %, dos redes vacias liberadas sin errores; arranque QA OK en 30,54 s. Se completo 30 s de calentamiento y 300 s de medicion con diez clientes, sin instrumentacion diagnostica de API. **9.603 solicitudes de medicion, cero errores HTTP**. p95: listado **438,45 ms**, detalle **361,19 ms**, creacion **687,49 ms**, actualizacion **554,30 ms**. Las cuatro operaciones incumplen p95<200 ms; RNF-2 sigue pendiente. Es la septima formal completada, diferente de los intentos no iniciados o incompletos.

Conteos 100 iniciales ->326 tras calentamiento ->2.725 finales. SQL: 2.725 incidencias y eventos de creacion, 2.620 eventos de edicion, 27.250 entregas encoladas, cero intentos SMTP y trabajos IA. Comprobaciones HTTP posteriores OK, diez logout 204 y contenedores detenidos. Hashes declarados coinciden con archivos actuales. Reporte original preservado mediante hash; sin nueva carga ni cambios de producto.

Los cuatro p95 son mayores que en formal 150 (259,28/221,32/385,49/347,43 ms). No atribuir causalidad: codigo, entorno y crecimiento de datos difieren. La CPU previa baja no garantiza CPU baja durante la carga; la formal no registra CPU global Windows durante medicion ni desglose interno. No permite culpar a Avast o una optimizacion concreta. Conservar las siete formales fallidas. Pendiente: revisar perfiles existentes del camino de creacion y costes compartidos antes de otra carga; no repetir sin hipotesis nueva ni relajar permisos/auditoria/durabilidad/umbral.


## 27 de octubre de 2026 — Outbox: compilacion reutilizada por lote

[Evidencia 183](evidencias/183-outbox-insertmanyvalues-compilacion-reutilizada.json): perfil local acotado de 31 creaciones ENTORNO reales (una fria +30 calientes con cProfile, diez RH ficticios, SQLite/Session nueva) detecto recompilacion de INSERT multirregistro: queue_event 575,20/860,44 ms acumulados de create_case; compilacion 250,02 ms en 30 llamadas. No es perfil HTTP/PostgreSQL. Se cambia solo insercion final del outbox a Core INSERT..RETURNING(id) con lista de parametros en execute, insertmanyvalues_page_size=50 y segmentos de 50, cerrando resultado. Mismos destinatarios, UUID, campos, idempotencia y transaccion; sin cache de autorizacion, commits adicionales o proveedores externos.

Perfil despues: primera CACHE_MISS y 30 CACHE_HIT, frente a 31 NO_CACHE_KEY; media caliente **28,78->18,35 ms** (36,23 % menor localmente). Fria 53,43->66,30 ms: no se demuestra mejora en frio. No extrapolar al p95 HTTP. Se comprobo ejecucion fisica de tres INSERT para 123 filas, cero cursor.executemany, <=600 parametros por lote. SQLAlchemy 2.1.4/dialecto psycopg anuncian soporte y se compila RETURNING para PostgreSQL; ejecucion real PostgreSQL pendiente. [Documentacion oficial](https://docs.sqlalchemy.org/en/20/core/dml.html).

**8 nuevas unitarias aprobadas en 0,659 s y 19 casos existentes de servicios, total 27 finales en 2,450 s**. Incluyen campos/UUID, mezcla de eventos/casos, destinatarios vigentes/omision, reintentos, fallo en segundo lote y rollback completo de creacion con 503. Casos existentes ejecutados por puente directo SQLite, no HTTP/TestClient. Primer puente habia usado ENTORNO donde el caso affected_rh requiere PERSONA; se corrigio fixture y se aprobaron todos sin relajar restriccion. Conteos SQL locales mantienen creacion 8 (5 SELECT/3 INSERT), edicion 5 (3 SELECT/1 INSERT/1 UPDATE), sin SQL posterior al commit. AST de tres archivos correcto.

Pendiente regresion API por el usuario y comprobacion real PostgreSQL antes de decidir otra formal. Sin nueva carga Docker, formal o smoke; RNF-2 pendiente y siete formales FALLIDA_UMBRAL conservadas, ultima 182. No atribuir el resultado a Avast ni declarar mejora formal por este perfil.


## 27 de octubre de 2026 — Regresion de outbox: 85 pruebas aprobadas

[Evidencia 184](evidencias/184-regresion-api-outbox-85-aprobadas.json): el usuario ejecuto pytest con seis archivos (outbox_cached_insert, mail_multivalues, mail_batching, mail, incidents, write_responses), resultado **85 passed in 17.90s**. Seleccion mixta de unitarias y API; no son 85 HTTP exclusivamente. RUN_DB_TESTS=0, autoload de plugins deshabilitado y sin cacheprovider. Tres hashes de implementacion/pruebas de 183 coinciden; tambien se registran hashes de los seis archivos seleccionados. Sin cambios de codigo en este avance.

Valida la seleccion funcional/atomica de la mejora 183; no valida PostgreSQL real ni p95. Las siete formales fallidas se conservan y RNF-2 continua pendiente. Pendiente un unico smoke diagnostico PostgreSQL QA aislado, con liberacion acotada de dos redes vacias previamente comprobada; revisar conteos/auditoria/outbox, cero proveedores externos, errores HTTP, perfil SQL/hilos y parada. No repetir formal ni acreditar por smoke.


## 27 de octubre de 2026 — Outbox integrado en PostgreSQL QA; escrituras aun sobre umbral

[Evidencia 185](evidencias/185-outbox-diagnostico-postgresql-integrado.json), run 746faa7071714c1e: usuario libero dos redes QA vacias sin fallos/omitidas e inicio unico smoke diagnostico 2+5 s, diez clientes. Arranque OK en 17,52 s. **318 solicitudes medidas, cero errores HTTP**. p95: listado **191,75 ms**, detalle **142,32 ms**, creacion **305,37 ms**, actualizacion **231,60 ms**. Solo lecturas quedan bajo 200 en esta muestra; el smoke no acredita RNF-2.

Conteos 100->128->208; SQL 208 incidencias/eventos creados, 96 editados, 2.080 entregas, cero SMTP/IA. Verificacion HTTP posterior OK, diez logout 204 y parada confirmada. Un INSERT outbox por creacion con diez entregas en PostgreSQL real; no se inyectan fallos PostgreSQL ni se registra cache_hit QA. Ocho grupos v3 validados por read_diagnostics con conteos/sumas SQL/hilos; tres workers y cero incompletas, consultas por peticion 3/2/10/7. Hashes actuales coincidentes; frente a 177 cambia solo mail.py.

Comparacion descriptiva con 177: endpoint de creacion medio 179,61->145,66 ms, p95 HTTP 479,34->305,37 ms. CPU global medida 80,43->66,56 % y tamaños/carga distintos; no prueba causalidad exclusiva ni ganancia formal. No sumar temporizadores solapados ni p95. Sin nueva formal del agente; se conservan siete FALLIDA_UMBRAL, ultima 182 previa a mejora 183 y regresion API de 85 aprobadas 184. Pendiente revisar viajes SQL/costes compartidos de escritura con hipotesis concreta; no repetir full ahora.


## 27 de octubre de 2026 — Creacion reutiliza departamento ya revalidado

[Evidencia 186](evidencias/186-creacion-reutiliza-departamento-validado.json): el perfil185 muestra un SELECT/departamentos aislado dentro de diez consultas de creacion. administration_lock ya lo carga y revalida bajo bloqueo pero retornaba solo el rol; crear con Session nueva volvia a consultarlo. Nueva opcion include_department=True junto a include_role=True retorna (rol,departamento); modos previos mantienen None/string. create_case conserva la referencia solo dentro de esa operacion y reutiliza si coincide el departamento, manteniendo consulta/validacion independiente para otro. Sin cache entre peticiones ni Session.info.

Conteo local real con Session nueva/expire_on_commit=True: creacion **8->7 sentencias (5->4 SELECT, tres INSERT)**; edicion conserva cinco. Prueba de otro departamento conserva ocho y sus IDs correctos. No SQL postcommit en respuestas de creacion. Se espera 10->9 consultas QA en ENTORNO del departamento propio incluyendo autenticacion/advisory, todavia no observado en PostgreSQL real; no extrapolar ahorro de milisegundos ni p95.

**25 unitarias locales aprobadas en 0,658 s**, ocho nuevas mas nueve de rol/lock y ocho de outbox. SQLite real; cubren traslado obsoleto refrescado, departamento propio inactivo403/otro inactivo422, fronteras empleado/supervisor, compatibilidad anterior, orden simulado del mismo advisory y rollback completo. AST correcto en tres archivos. Se mantienen bloqueo antes de relectura y, en gestion, bloqueo de expediente antes de reevaluar acceso. No fusionar esas lecturas para ahorrar viajes sin demostrar semantica concurrente. [Bloqueos PostgreSQL17](https://www.postgresql.org/docs/17/explicit-locking.html).

Pendiente regresion API y comprobacion real PostgreSQL de reduccion/seguridad. Sin nueva formal/smoke ni cambios en umbral/durabilidad/auditoria/outbox. RNF-2 pendiente; siete formales fallidas conservadas. Las85 pruebas184 corresponden a revision anterior y no sustituyen regresion de este cambio.


## 27 de octubre de 2026 — Departamento revalidado: 97 pruebas y ocho subpruebas aprobadas

[Evidencia187](evidencias/187-regresion-api-departamento-97-aprobadas.json): salida del usuario **97 passed, 8 subtests passed in 8.56s** para ocho archivos: creation_department_reuse, administration_role_join, administration_lock_queries, lifecycle_role_queries, incidents, departments, user_administration y write_responses. Seleccion mixta de unitarias/API con RUN_DB_TESTS=0 y plugins/caches deshabilitados; no prueba PostgreSQL real. Tres hashes de186 coinciden, sin cambio de producto en este avance.

La reduccion local 8->7 sentencias de creacion propia queda cubierta por regresion seleccionada, junto con permisos/departamentos/roles/rollback. Pendiente unico smoke instrumentado PostgreSQL QA para comprobar 10->9 consultas con autenticacion/advisory y conteos reales. El generador actual usa ENTORNO del propio departamento; ese smoke no sustituye regresion de otros departamentos o carrera PostgreSQL. Sin nueva formal del agente; RNF-2 pendiente, siete formales FALLIDA_UMBRAL conservadas.


## 27 de octubre de 2026 — Nueve consultas por creacion confirmadas; p95 sin mejora

[Evidencia188](evidencias/188-creacion-nueve-consultas-postgresql-p95-pendiente.json), run19a673b3854f44ff: dos redes QA vacias retiradas sin fallos/omitidas, arranque OK17,15s, unico smoke instrumentado2+5s con diez clientes. **312 solicitudes medidas, cero errores HTTP**. Consultas por peticion3/2/**9**/7; en calentamiento y medicion de creacion desaparece SELECT/departamentos aislado. Se confirma reduccion prevista10->9 para ENTORNO propio; no se extrapola a otros departamentos.

p95 HTTP: listado **181,25ms**, detalle **188,44ms**, creacion **371,32ms**, actualizacion **258,60ms**. Escrituras siguen sobre200 y empeoran frente185 (305,37/231,60ms). Endpoint de creacion medio145,66->129,83ms; CPU global66,56->70,77%. Menos consultas y menor media interna no acreditan mejora del p95; condiciones y muestras distintas impiden atribuir causa exclusiva. Mantener el resultado adverso.

Conteos100->130->209; SQL209 incidencias/eventos creados,103 editados,2.090 entregas, cero SMTP/IA. HTTP posterior OK, diez logout204, contenedores detenidos. Ocho grupos v3 y sumas validados, tres workers y cero incompletas. Hashes actuales coincidentes; frente185 cambian solo administration_lock.py e incidents.py de servicios. Reporte original preservado por hash. Regresion187 de97 pruebas/ocho subpruebas corresponde a esta revision.

Sin nueva formal del agente; siete formales FALLIDA_UMBRAL conservadas y RNF-2 pendiente. El smoke no prueba carreras ni rollback PostgreSQL. No sumar temporizadores solapados/p95 ni repetir full por consulta eliminada. Pendiente revisar esperas y costes compartidos de escritura con hipotesis concreta antes de otra carga.


## 27 de octubre de 2026 — Cierre limpio de Session sin salto a worker

[Evidencia189](evidencias/189-cierre-session-limpia-sin-worker.json): tercer worker del cierre en188 ejecuta solo0,03379ms (creacion) /0,04781ms (edicion) de media, con espera+retorno23,33/22,26ms. Al ocurrir despues del envio, no se resta ese tiempo al p95 HTTP; hipotesis de reducir planificacion/carga compartida, no ganancia formal demostrada. Se reviso SQLAlchemy2.1.4 instalado: Session._close_impl sin _transaction solo expunge_all; in_transaction refleja existencia de transaccion. [Semantica oficial de Session](https://docs.sqlalchemy.org/en/21/orm/session_api.html).

get_session conserva shield. Solo para tipo exacto de Session estandar original y sin transaccion, close local limpia objetos sin SQL/rollback/pool. Sesiones activas, subclases y dobles conservan worker con limiter1 independiente; SELECT posterior a commit vuelve a requerirworker. Sin cambios de consultas, commit, permisos/auditoria/atomicidad, pool, aislamiento o umbral. Excepcion acotada a decision156 de cerrar siempre enworker: todo cierre con posible IO siguefuera del loop. No custom callbacks de detach con IO en esta revision; futuros cambios de ese tipo requeririan revisar criterio.

**14 unitarias locales aprobadas en0,116s**, siete nuevas: ORM expirado tras commit se separa sin SQL/rollback/checkout/checkin; lecturas/escrituras pendientes, fallo de flush, SELECT postcommit, sesiones custom, cancelacion y errores de cierre. Workers reales/SQLite y dobles async sin eventloop. Nueva prueba FastAPI/TestClient para commit/cierre sinIO lista, mas pruebas AnyIO/TestClient previas: pendientes de ejecucion por el usuario. AST correcto en dos archivos. Se espera2 workers por escritura comprometida y3 por lectura, mismo SQL3/2/9/7; aun no observado enQA.

No nueva carga, formal o p95. RNF-2 pendiente; siete formales FALLIDA_UMBRAL conservadas. Regresion187 precede este cambio y no lo valida. Pendiente regresion de sesion/AnyIO/API antes de considerar otro diagnostico; no repetir full ahora.


## 27 de octubre de 2026 — Cierre de Session: 99 pruebas aprobadas con AnyIO/API

[Evidencia190](evidencias/190-regresion-session-anyio-api-99-aprobadas.json): el usuario ejecuto siete archivos database_session, database, auth, incidents, mail, write_responses y worker_response; resultado **99 passed in12.03s**. Incluye pruebas AnyIO/TestClient pendientes de189, cierre postcommit sinIO y rutas de cierre activo/custom protegidas. Seleccion mixta de unitarias/API, no99HTTP. RUN_DB_TESTS=0, plugins/caches deshabilitados. Ambos hashes189 coinciden; sin cambio de producto en este avance.

Pendiente unico smoke PostgreSQL QA para contrastar dos workers en escrituras comprometidas/tres en lecturas y consultas3/2/9/7, auditoria/outbox/errores/parada. Cierre postenvio: no estimar ahorro directo p95. Sin nueva carga/formal por el agente. RNF-2 pendiente; siete formales FALLIDA_UMBRAL conservadas.


## 27 de octubre de 2026 — Dos workers por escritura confirmados; SQL intacto

[Evidencia191](evidencias/191-cierre-limpio-dos-workers-escritura-postgresql.json), run0e18dbd01e554b2e: dos redes vacias QA retiradas sin fallos/omitidas, arranque OK16,95s y unico smoke instrumentado2+5s con diez clientes. **330 solicitudes medidas, cero errores HTTP**. En ambos periodos, creacion/actualizacion bajan3->2 llamadas a worker; lecturas conservan3. Consultas3/2/9/7 y cero incompletas; no se altera instrumentacion para lograrlo. Frente188 cambia solo core/database.py; hashes actuales coincidentes.

Cierre medio creacion23,53->0,16ms y edicion22,48->0,15ms. Desaparece etapa other de escritura, permanece en lectura para rollback enworker. p95 listado **190,30ms**, detalle **150,90ms**, creacion **271,85ms**, actualizacion **248,74ms**. Escrituras siguen sobre200; frente188 (371,32/258,60) son menores, pero CPU70,77->67,42% y muestras/carga diferentes impiden atribuir toda mejora al codigo. Cierre postenvio: no restar su reduccion al p95 HTTP ni sumar p95 solapados.

Conteos100->130->212; SQL212 incidencias/eventos creados,104 editados,2.120 entregas, cero SMTP/IA. HTTP posterior OK, diez logout204, contenedores detenidos. Ocho grupos v3 y sumas SQL/hilos verificados. Regresion190 de99aprobadas cubre revision; smoke no inyecta fallos ni demuestra carreras PostgreSQL. Reporte original conservado por hash.

RNF-2 pendiente, siete formales FALLIDA_UMBRAL conservadas; sin nueva formal ni carga del agente. Pendiente explicar costes de nueve/siete viajes SQL y autenticacion compartida antes de nueva modificacion/carga; mantener locks, relecturas, durabilidad y criterio. No repetir full ahora.


## 27 de octubre de 2026 — Diagnostico v4 separa ping de conexion

[Evidencia192](evidencias/192-diagnostico-pool-pre-ping-separado.json): revision de SQLAlchemy2.1.4 instalado confirma que pool_pre_ping usa PGDialect_psycopg.do_ping con SELECT1 directo DBAPI, fuera de before_cursor_execute. Por tanto, las9consultas de creacion son sentencias observadas por motor, no todos los viajes; tampoco incluyen BEGIN/COMMIT/ROLLBACK o apertura de conexion. No cambia p95/formales anteriores. [Semantica oficial de pre_ping](https://docs.sqlalchemy.org/en/21/core/pooling.html).

Entrada QA protegida envuelve do_ping sin cambiar argumentos/resultado/excepcion/recuperacion. Nuevas metricas pool_ping(ms), pool_ping_calls y pool_ping_errors; formato4 con marca de instrumentacion. Contexto ausente no mide; no guarda SQL/conexion/parametros/errores privados. app.main/pool_pre_ping intactos. Reader acepta3/4 y exige metricas v4 finitas/no negativas y conteos coherentes, permite cero si conexion fresca. Reportes185/188/191 v3 revalidados sin reescritura.

**85 unitarias de herramientas aprobadas en1,569s y tres pruebas SQLAlchemy en0,049s**. Nueve nuevas stdlib: resultado/excepcion sin reintentos, privacidad, contextos concurrentes, v3/v4 y pipeline ASGI->snapshot->reader de ocho grupos. Tres nativas: ping SQLite real no aparece en evento de motor, psycopg conserva cursor/autocommit, clasificacion de desconexion original se mantiene. Sin PostgreSQL real ni HTTP/Docker/carga nueva. AST de seis archivos y orden guard/parche comprobados.

Hipotesis por verificar: ping podria explicar parte de autenticacion fuera del SQL cronometrado. No se conoce aun coste ni frecuencia real; no desactivar ping ni atribuirle cuello de botella sin medir. pool_ping solapa auth y no se suman sus p95. Pendiente unico smoke v4; no nueva formal. Siete formales FALLIDA_UMBRAL conservadas, RNF-2 pendiente.


## 27 de octubre de 2026 — Ping medido; retencion del pool para diez clientes

[Evidencia193](evidencias/193-ping-postgresql-coste-medido-sin-fallos.json), run7b1abe6c5dc54abc: diagnostico4 valido con **296 solicitudes medidas, cero errores y258pings sin fallos**. Tiempo ping medio por peticion8,85/10,70/10,78/10,93ms; no sumarlo a auth ni a sus p95. p95 listado211,39/detalle196,50/creacion383,47/actualizacion304,76ms; solo detalle bajo200 en esta muestra. CPU global78,42%. Conteos100->130->204, SQL204casos/eventos creados,98editados,2.040entregas, cero SMTP/IA. PostHTTP OK,diez logout204,parada confirmada; SQL3/2/9/7 y workers3/3/2/2. Reporte original conservado porhash y codigo previo a194 validado.

38peticiones sinping son compatibles con conexiones frescas (source instalado lo omite), pero no prueban por si solas que todas sean recreaciones poroverflow. Se mantiene pre_ping. [Evidencia194](evidencias/194-pool-retiene-diez-maximo-quince.json): experimento local de tres oleadas de diez conexiones simultaneas con QueuePool/SQLite: default5+overflow10 crea20conexiones y cierra15antes de dispose; retencion10+overflow5 crea10y reutiliza todas despues de primera oleada. No mide tiemposPG/HTTP.

get_engine ahora retiene hasta10conexiones y permite5extra: **mismo maximo15por proceso**, pre_pingTrue, pool_timeout30 y connect_timeout3 sin cambios. Creacion diferida, cachedeengine, transacciones/aislamiento/reset/permisos/auditoria intactos. Puede mantener cinco ociosas adicionales y su memoria; no garantiza ahorro p95.

**20 locales aprobadas en0,211s**, seis nuevas de pool y14deSession. Puente con opciones reales de get_engine hacia SQLite, sinred. Verifica tresoleadas10/0/0 nuevas, max15/rechazo16a, espera/reuso al devolver, recuperacion deconexion obsoleta ydispose. AST valido en dos archivos. Pendiente regresionAPI y diagnosticoPG de194. No nueva carga del agente ni formal; siete FALLIDA_UMBRAL conservadas,RNF-2 pendiente.


## 27 de octubre de 2026 — Pool ajustado: 105 pruebas aprobadas

[Evidencia195](evidencias/195-regresion-api-pool-105-aprobadas.json): salida del usuario **105 passed in16.15s** para ocho archivos database_pool, database_session, database, auth, incidents, mail, write_responses y worker_response. Seleccion mixta de unitarias/API con RUN_DB_TESTS=0; no105HTTP ni prueba PostgreSQL real. Dos hashes194 coinciden, sin cambios de producto en este avance.

Pendiente unico smoke PostgreSQL QA instrumentado v4 para pool10retenidas+5extra, max15. Contrastar frecuencia/coste de ping/auth, SQL3/2/9/7, workers3/3/2/2, errores/auditoria/outbox/recursos/parada. Mayor frecuencia de ping puede indicar reuso, no acredita latencia; mantener todos los resultados adversos. RNF-2 pendiente y siete formales FALLIDA_UMBRAL conservadas. Sin carga adicional del agente ni nueva formal.


## 27 de octubre de 2026 — Pool10 sin ganancia p95; experimento retirado

[Evidencia196](evidencias/196-pool-diez-diagnostico-sin-ganancia-p95.json), runb61bb77e73b94128 (UTC28oct/local27oct): unico diagnostico instrumentado2+5s,267solicitudes medidas sin errores,262pings sinfallos. Frecuencia87,16->98,13% frente193 compatible con mas reuso, no conteo directo completo de creaciones. Pero **los cuatro p95 son mayores: listado249,52/detalle225,90/creacion456,68/actualizacion365,13ms**. Ninguno bajo200 en esta muestra. CPU78,42->79,03%; no atribuir regresion causal con una sola ventana y dataset/carga distintos.

Datos100->130->196; SQL196incidencias/eventos creados,92editados,1.960entregas,ceroSMTP/IA. PostHTTP OK,diez logout204,parada confirmada; SQL3/2/9/7 y workers3/3/2/2. v4/sumas/hash del codigo experimental194validados; solo database.py cambia respecto193. Reporte original intacto.

[Evidencia197](evidencias/197-pool-base-restaurado-experimento-retirado.json): se retira **solo ajuste194 de retener10** porque no demuestra beneficio p95 que justifique hasta5conexiones ociosas mas. database.py vuelve byteporbyte al hash de190: defaults5retenidas+10extra,max15,pre_pingTrue,tiempos30/3. Conserva cierre limpio189,mail183 y departamento186. Diagnostico192tambien conservado. No se afirma que pool10causara por si solo el empeoramiento ni se ocultan194/195/196.

**20 pruebas locales aprobadas en0,294s**, seis de poolbase y catorce deSession. Pruebas de saturacion/capacidad15,obsoletas/pre_ping,liberacion/lazy y cierre activo/limpio preservadas. El codigo productivo restaurado coincide con revision de99pruebas190; no nueva pruebaAPI/PG ejecutada por agente. AST/JSON/hash verificados,README actualizado. RNF-2 pendiente;siete formales FALLIDA_UMBRAL conservadas. No otra formal por restauracion; pendiente hipotesis basada en costes de driver/servidor/planificacion.


## 27 de octubre de 2026 — Diagnostico5: CPU del worker frente a tiempo transcurrido

[Evidencia198](evidencias/198-diagnostico-cpu-worker-separada-de-tiempo.json): thread_run de versiones anteriores incluye esperas/IO/planificacion dentro del worker. Nueva metrica thread_cpu y cpu_ms por etapa mide diferencia de time.thread_time dentro del mismo hilo. Excluye tiempo no ejecutado por ese hilo, eventloop/otros hilos/PostgreSQL/hipervisor. No es CPU global ni permite atribuir todo wall-CPU a una causa. [Definicion de Python](https://docs.python.org/3.11/library/time.html#time.thread_time).

Solo diagnostico protegido QA: formato5 con marca CPU, campos agregados y opciones/cancelacion/excepciones/limiter intactos. Fuera de contexto no mide. Reader acepta3/4/5; en5 exige marca, CPU finita/no negativa y sumas por etapas concordantes; CPU0permitida por granularidad. No guardar argumentos/SQL/errores privados. No sumar/restar p95. No imponerCPU<=wall por diferencias de resolucion.

**94 unitarias stdlib aprobadas en2,125s**, nueve nuevas. Relojes separados, mismo hilo real, ContextVar, excepcion exacta, no inicio, privacidad, legado y validacion corrupta. Pipeline ASGI simulado genera ocho grupos formato5y pasa lector. Reportes177/191v3 y193/196v4 revalidados; AST seisarchivos correcto. Sin nueva carga/Docker/PostgreSQL/HTTP real. database.py conserva hash190restaurado197: poolbase5+10 y todas las otras mejoras permanecen.

Pendiente unico smoke5para decidir si predomina CPU del worker o tiempo fuera deCPU; no es cambio de rendimiento ni acreditacion. Siete formales FALLIDA_UMBRAL conservadas,RNF-2 pendiente. No otraformal sin hipotesis y evidencia.


## 27 de octubre de 2026 — CPU de workers medida; control driver/servidor preparado

[Evidencia199](evidencias/199-cpu-worker-baja-frente-a-tiempo-transcurrido.json), runde6481fae3c04e19: diagnostico5 valido,260solicitudes medidas sinerrores. P95 listado233,84/detalle257,01/creacion509,12/edicion285,46ms, todos sobre200. CPUglobal80,20%. Creacion usa23,07msCPU enworkers frente192,29mstranscurridos; endpoint18,06CPU/135,75ms. Edicion14,99CPU/140,83ms; endpoint11,29CPU/99,98ms. Predomina tiempo no ejecutando esos hilos, pero no se identifica aun servidor/IO/GIL/SO/VM; no incluyeCPUeventloop/otrosprocesos.

Conteos100->130->192; SQL192incidencias/eventoscreados,90editados,1.920entregas,ceroSMTP/IA. PostHTTP OK,diezlogout204,parada confirmada. SQL3/2/9/7 y workers3/3/2/2; sumasCPU/hilos y hashesvalidados. Reporteoriginalconservado. No acreditaRNF-2;sieteformalesfallidas vigentes.

[Evidencia200](evidencias/200-control-driver-servidor-select1-preparado.json): control opcional --db-probe solo smoke diagnostico QA nuevo, despues de HTTP y verificacionSQL antes de parada.55lecturas fijas EXPLAIN ANALYZE SELECT1:5en1conexion y50en10conexiones/hilos coninicioalineado. Reporta driver/CPU/planificacion/ejecucionservidor sin SQL/plan/parametros/credenciales. No admite consultas arbitrarias; identidadDB/user real y envQA comprobados. Sin extensiones, cambioPG o API/pool/producto. SETLOCAL timeout3s solo transaccionescontrol; procesoexterno60s. Error conservaHTTP/SQL y marcaINCOMPLETA/parada.

**102 unitarias de herramientas aprobadas en2,266s**, ochonuevas; guard,55muestras/liberacion,privacidad,rechazoformaly recuperaciondeerror, con motoresdobles e hilosreales. Primer fallo deexpectativaregexcorregido sinrelajar guarda. AST4archivoscorrecto; ejecucionPGreal pendiente. El control no reproduce consultas de negocio ni comparte cargaHTTP simultanea; no atribuir diferencia a red pura ni restarp95. Pendiente unico smoke --db-probe, no otraformal.

## 2026-10-29 — Control SELECT1 real; estadísticas de consultas de negocio preparadas

[Evidencia207](evidencias/207-control-select1-postgresql-real-rnf2-pendiente.json), runee6fcc5a7e8c411e (UTC30-oct/local29-oct): arranque18,51s; diagnóstico5 válido y control DB completo. **286 solicitudes medidas, cero errores HTTP**, conteos100->130->201; SQL201casos/creaciones,96ediciones y2.010entregas, cero SMTP/IA. Diez logout204, postHTTP OK y QA detenido. Reporte original intacto por hash;54hashes de producto coinciden. SQL3/2/9/7, workers3/3/2/2 y cero incompletas conservados.

P95 HTTP ms: listado231,82; detalle207,12; creación363,92; edición289,96: ninguno bajo200. CPUhost74,54%, generador0,84%. Workers creación23,51msCPU frente184,33mstranscurridos; edición14,95CPU/137,03ms. Control después de HTTP: con1conexión5muestras, driver4,370ms/ejecución servidor0,507ms medios; con10conexiones50muestras, driver4,952ms/CPUworker0,665ms, planificación0,02052ms/ejecución0,01944ms medios. P95 driver concurrente8,686ms. No mide consultas reales bajo carga, no restar p95 ni atribuir diferencia a red/IO/GIL/SO/VM únicos. Tampoco permite afirmar que PostgreSQL explique o no explique el coste de negocio. No octava formal; RNF-2 pendiente.

[Evidencia208](evidencias/208-estadisticas-sql-servidor-qa-preparadas.json): opción --server-stats solo smoke diagnóstico, protegida antes de crear recursos. Añade pg_stat_statements/compute_query_id únicamente al PostgreSQL QA nuevo, crea extensión con guard de identidad y toma snapshots sin reset. Deltas por consulta se agregan a familias: llamadas, ejecución/filas y media ponderada; no SQL, parámetros o IDs de consulta en reporte. Detecta reset global/individual por stats_since, desalojo y disminución de contadores. Ventana incluye login/logout, calentamiento, carga y verificación SQL, excluye seed y sondeo SELECT1 posterior. La extensión mantiene textos en su QA privado y añade coste; planning tracking off, sin p95 servidor. No cambia el sitio, Compose operativo, pool, durabilidad ni criterio formal.

**113 unitarias stdlib aprobadas en2,441s**, once nuevas:9helper y2provisionador. Incluyen guard, privacidad, deltas/ponderación, reset/evicción/contadores, configuración solo opt-in, orden alrededor de HTTP/control y parada conservando HTTP/SQL ante fallo posterior. AST4archivos correcto; --plan confirmado sin Docker. Lectores actuales revalidan el reporte real207. No ejecución PG real de208 ni optimización de producto nueva; pendiente un único smoke opcional de estadísticas. No repetir formal sin evidencia/hipótesis nueva.

### Consultas reales: estadísticas de ejecución del servidor QA

Después de liberar, con la herramienta de mantenimiento, dos redes QA elegibles vacías, ejecutar desde la raíz:

```powershell
.\backend\.venv\Scripts\python.exe -B backend/scripts/provision_performance_qa.py --mode smoke --diagnostic --server-stats --confirm-isolated-qa
```

Activa exclusivamente en PostgreSQL QA nuevo el módulo pg_stat_statements (imagen17). No requiere alterar la instalación operativa ni detener el sitio. El reporte añade `servidor_sql`: deltas de llamadas, tiempo total de ejecución, filas y media por familia. Excluye el seed; incluye login/logout, calentamiento, carga y verificación SQL. No compara directamente esa ventana con los conteos solo de medición. Los snapshots rechazan resets/desalojos; no ejecutan reset. No conserva texto SQL/IDs en el reporte, aunque la extensión guarda texto en su volumen QA privado.

Disponible únicamente con smoke+diagnostic; sin la opción no cambia la configuración PostgreSQL. Puede combinarse con --db-probe, cuyo SELECT1 se ejecuta después del snapshot final. El seguimiento de planificación está apagado; no hay p95 servidor y no se deduce latencia HTTP por resta. El coste añadido impide acreditar RNF-2 con este diagnóstico. **113unitarias aprobadas; ejecución PostgreSQL real del nuevo control pendiente.** No invocar esta opción sobre la base operativa ni reutilizar recursos QA de otra corrida.
