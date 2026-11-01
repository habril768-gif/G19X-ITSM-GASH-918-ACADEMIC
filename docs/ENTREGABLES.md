# Entregables de residencia

## RNF-2: aprobado en HTTP QA Linux CI del31/10/2026

[Validación270](evidencias/270-rnf2-linux-ci-aprobado.json) y [reporte íntegro271](evidencias/271-rnf2-linux-ci-reporte-completo.json): commit2bbf4a5, tres procesos API, diez clientes, cien casos iniciales,30+300 s completos y71079 solicitudes sin errores. P95 listado31,85/detalle52,60/creación62,17/actualización60,15 ms, todos<200 ms. Auditoría, outbox, HTTP posterior, diez logout204 y detención QA comprobados. Runner Linux con4CPU y15,61 GiB Docker, servidor28.0.4; hardware y hashes exactos en270. Acredita ese alcance HTTP QA, sin IA/SMTP externos ni rendimiento universal. Los fallos Windows de la versión actual se conservan separados; no se afirma corregida la laptop. Despliegue actualizado del principal pendiente.

### Referencia histórica Windows


[Primera formal aprobada220](evidencias/220-rnf2-formal-local-aprobada-tres-procesos.json):10 clientes,100 casos iniciales,30+300s,API de 3 procesos,35.216 solicitudes sin errores. P95 listado123,81/detalle113,27/creación194,04/actualización167,77ms, todos<200 ms; auditoría/colas/logout/parada correctos. Acredita este alcance HTTP Docker local y hardware declarado, no rendimiento universal ni proveedores externos. Diez fallos históricos se conservan. [Perfil opcional 221](evidencias/221-perfil-compose-rnf2-reproducible.json) y [protocolo](PRUEBA_RENDIMIENTO.md) permiten reproducir configuración/medición. Los demás pendientes de entrega siguen vigentes.


La matriz organiza las actividades del descriptivo del proyecto y su estado verificable. La implementación de una función no acredita por sí sola la finalización de su entregable académico.

| Actividad | Entregable | Ubicación | Estado actual y pendiente |
| --- | --- | --- | --- |
| Detección de necesidades | Requerimientos y alcance | [PRD](PRD.md), [MVP](MVP.md) | Reglas documentadas; análisis de campo no acreditado |
| Propuesta | Propuesta técnica | [Propuesta](PROPUESTA_TECNICA.md) | Documento elaborado: objetivos, alternativas, recursos, riesgos y aceptación; no acredita análisis de campo ni aprobación institucional |
| Arquitectura | Arquitectura del sistema | [Arquitectura](ARQUITECTURA.md) y [manual técnico](MANUAL_TECNICO.md) | Componentes, diagramas, flujos, datos y límites documentados contra código; operación productiva y aceptación pendientes |
| Planificación | Plan y seguimiento | [Backlog](BACKLOG.md) | Prioridades y dependencias definidas; fecha límite/capacidad sin confirmar |
| Desarrollo | Sistema funcional local | Backend, frontend, Compose e [informe Power BI](../powerbi/README.md) | Núcleo, IA, correo y SQL implementados; aceptación integral pendiente según MVP |
| Pruebas | Reporte QA y evidencias | [QA](REPORTE_QA.md), [trazabilidad](TRAZABILIDAD.md), evidencias | Pruebas automáticas y recorridos registrados; RNF-2 aprobado en220. Matriz integral de escenarios y aceptación pendientes |
| Documentación | Manuales técnico y de usuario | [Manual técnico](MANUAL_TECNICO.md), [manual de usuario](MANUAL_USUARIO.md) y guías | Manuales documentados; revisión mediante matriz completa de roles y capacitación pendientes |
| Mantenimiento | Plan de soporte y recuperación | [Plan de mantenimiento](PLAN_MANTENIMIENTO.md) | Recuperación lógica nativa103 y Docker230, salud234 y custodia/condición de conservación235–236 documentadas. Instalación integral, disposición posterior y custodia de analítica pendientes |
| Capacitación | Sesión y acta | Por realizar | Sin sesión real ni aprobación registradas; no generar acta retrospectiva |
| Cierre | Informe final y lecciones | [Borrador](INFORME_ENTREGA_BORRADOR.md) | Borrador basado en evidencias; adaptar a formato institucional y completar aceptación real. No acta de cierre |

## Integraciones y evidencia

Correo cuenta con pruebas y recorrido Mailpit/React (85–92). Analítica cuenta con pruebas SQL y de permisos (93), conexión Desktop (94–95) e informe guardado/revisión de visuales (98). Modelo/formatos revisados (104), refresco principal confirmado (105) y QA visual/retirada por sustitución de agregados ficticios en Desktop aprobada (106). Ensayo SQL→JSON→Desktop aislado verificado (108–109): exclusión por confidencialidad, supresión SQL y refresco de la copia. Quedan conector directo aislado si se exige, custodia y aceptación integral. Esto corrige la lectura antigua que los consideraba ausentes, pero no elimina sus pendientes de aceptación.

La evaluación IA y sus diferencias se conservan en [resultados](evaluacion_ia/RESULTADOS_V4.md). La API directa OpenAI fue la elección registrada en [decisiones](DECISIONES.md), en lugar del servicio Azure mencionado en el descriptivo. La confirmación de casos simulados no constituye una revisión independiente del sistema completo.

## Criterio de registro

Los resultados y las limitaciones pertenecen a QA; los cambios cronológicos, a la bitácora. No se inventan entrevistas, firmas, capacitación o aprobación. Las capturas con información personal no deben publicarse; los originales locales excluidos de Git no equivalen a evidencia sanitizada.


## Comprobación manual de Supervisor y Empleado

[Evidencia 111](evidencias/111-supervisor-empleado-ui.json): Supervisor consulta listado y detalle de Retardo; la autora confirma que no permite reabrir. Empleado 1 registra un caso simulado de Entorno, consulta su detalle/historial y lo encuentra en el listado; confirma que no dispone de más acciones. Capturas aportadas y confirmaciones textuales, sin ejecución directa del agente. La ocultación de controles no acredita restricciones API ni acceso a casos ajenos/confidenciales; aceptación por roles todavía parcial.


## Recorrido manual de RH y estado tras reapertura

[Evidencia 112](evidencias/112-rh-ciclo-reapertura-ui.json), registrada el 21 de octubre de 2026: la autora confirma resolución, cierre y registro de reapertura del caso simulado de la evidencia 111. Capturas posteriores muestran En revisión tanto en el detalle de RH como en el listado de Empleado; RH muestra aviso de reapertura, prioridad Baja y validación vigente. El bloqueo previo al confirmar clasificación fue visible. Transiciones intermedias reportadas por la autora, sin capturas de cada paso ni inspección del historial completo. No acredita restricciones API, correo ni aceptación integral. Caso conservado en revisión.


## Vista estrecha de Empleado

[Evidencia 113](evidencias/113-vista-estrecha-empleado.json): emulación a 390 × 844, filtros en columna y detalle apilado; la autora confirma lectura sin desplazamiento horizontal y retorno al panel sin problemas. Revisión visual parcial, sin teléfono físico ni auditoría de accesibilidad. Los 404 capturados son de detalle/historial del expediente anterior conservado en el enlace; su existencia y autorización siguen sin comprobar. No se declara fallo de autenticación ni prueba negativa aprobada.


## Acceso a caso ajeno entre empleados

[Evidencia 114](evidencias/114-empleado-caso-ajeno-ui.json), 21 de octubre de 2026: Empleado Operaciones Dos Demo muestra listado vacío y, al abrir el enlace del caso conocido de Empleado 1 según la autora, aviso de caso no disponible/sin permiso sin contenido del expediente. Resultado esperado observado en capturas, coherente con la regla de ENTORNO para empleados. Existencia del caso sustentada por 111–112; URL objetivo reportada por la autora, sin tráfico HTTP inspeccionado. Cubre este escenario manual de lectura, no restricciones de escritura, confidencialidad ni aceptación completa.


## Confidencialidad: retirada de consulta al creador

[Evidencia 115](evidencias/115-confidencialidad-empleado-ui.json), 21 de octubre de 2026: la autora confirma marcar el caso simulado como confidencial y conservar consulta desde RH. Capturas posteriores de Empleado 1 muestran aviso de caso no disponible/sin permiso al enlace indicado y listado con cero casos. Resultado esperado en este recorrido manual; cambio y acceso RH reportados, denegación/consulta vacía observadas en capturas. No acredita restricciones de escritura, auditoría, cachés, API directa ni todos los roles. Caso conservado confidencial.


## Restricciones de escritura: ejecución pendiente

[Evidencia 116](evidencias/116-escritura-ejecucion-bloqueada.json): se seleccionaron cuatro pruebas existentes de permisos de escritura. El runtime del proyecto no devolvió salida y se interrumpió; el auxiliar con dependencias del entorno falló en importación de pydantic_core. No hubo resultados pytest ni pruebas aprobadas nuevas. Revisión estática preparada; ejecución compatible pendiente. No se diagnostica daño del entorno original a partir del fallo auxiliar.


## Cuatro pruebas de escritura ejecutadas por la autora

[Evidencia 118](evidencias/118-escritura-cuatro-tests-confirmados.json): capturas de terminal acreditan una prueba aprobada en 5,85 s y otras tres aprobadas/22 deseleccionadas en 5,13 s. Cubren clasificación y asignaciones, protección independiente, revalidación y cierre/reapertura por supervisor, y registro para pares/autor adulterado según los tests existentes. Ejecución con SQLite en memoria y dependencias de sesión/usuario sustituidas; no es autenticación real, PostgreSQL ni suite completa. Se resuelve la ejecución pendiente de esta selección de 116–117; ambos antecedentes se conservan. Autoload de plugins deshabilitado para la ejecución satisfactoria, sin plugin culpable identificado.


## Salud de la instalación actual

[Evidencia 119](evidencias/119-salud-instalacion-actual.json): capturas de la autora muestran respuestas ok de /health y /health/db, y docker compose ps con API, PostgreSQL y Redis healthy. Estado disponible en ese momento; sin cambios de servicios. No acredita instalación limpia, reinicio controlado, workers, carga ni recuperación completa. La restauración aislada de 103 es evidencia separada.


## Consulta después del reinicio de API reportado

[Evidencia 120](evidencias/120-api-reinicio-consulta-rh.json): tras la instrucción de reiniciar solo API, la autora confirma finalización; capturas muestran consulta del listado/detalle desde RH, mismo caso En revisión con prioridad Baja, validación vigente y confidencialidad restringida a RH independiente. Confirma /health/db con status ok/database postgresql. No hay captura del comando ni medición del reinicio; prueba manual acotada, sin instalación limpia, reinicio de base/Redis o recuperación completa.


## Medición RNF-2 preparada

[Protocolo de rendimiento](PRUEBA_RENDIMIENTO.md) preparado contra el criterio del PRD: Docker QA separado, cien casos iniciales, diez sesiones/clientes, 30 s de calentamiento y 300 s medidos; listado, detalle, creación y edición con p95 por operación, errores y hardware. Incluye crecimiento del conjunto, encolado y límites de modo IA. No hay ejecutor nuevo ni carga ejecutada; RNF-2 continúa pendiente.


## Ejecutor RNF-2 preparado

[Protocolo y uso](PRUEBA_RENDIMIENTO.md), [evidencia 121](evidencias/121-ejecutor-rendimiento-unitarias.json): generador HTTP de diez clientes con cuatro operaciones, modo corto, métricas y validación de fixture QA. Trece pruebas locales aprobadas y manifiesto de ejemplo rechazado antes de HTTP. No se provisionó QA ni se ejecutó carga real; RNF-2 sigue pendiente. El ejecutor no certifica automáticamente aislamiento Docker, recursos o colas/auditoría.


## Provisionador de rendimiento disponible

[Protocolo y comandos](PRUEBA_RENDIMIENTO.md), [evidencia 122](evidencias/122-provisionador-rendimiento-unitarias.json): entorno Docker QA nuevo por corrida, fixture de diez cuentas/cien casos, modos smoke/full, recursos y auditoría/colas, parada sin borrados. Nueve tests de provisionador y trece de generador aprobados con simulación; CLI plan revisado. Sin Docker real ni RNF-2 medido. Pendiente smoke real y después carga formal.


## Primer smoke real de rendimiento incompleto

[Evidencia 123](evidencias/123-smoke-qa-conexion-rechazada.json): build/migraciones/fixture completados según reporte real; cien casos/eventos, mil entregas y cero intentos SMTP/trabajos IA. HTTP rechazó conexión antes de carga, sin p95; contenedores detenidos. Ajustada red de entrada exclusiva de API y comprobación de salud previa al fixture; doce tests simulados aprobados. Corrección pendiente de nuevo smoke real; RNF-2 aún no medido.


## Segundo smoke: preparación correcta, calentamiento incompleto

[Evidencia 124](evidencias/124-smoke-qa-calentamiento-incompleto.json): salud/preflight correctos, diez listados de calentamiento con seis éxitos y cuatro excepciones; sin fase medida. Diez sesiones revocadas y QA detenido. Generador corregido para renovar sockets entre fases y registrar tipo de excepción sin reintentos; quince pruebas locales aprobadas. Hipótesis de keep-alive aún sin confirmación real; RNF-2 pendiente.


## Smoke de rendimiento real completado

[Evidencia 125](evidencias/125-smoke-rendimiento-real-satisfactorio.json): diez clientes, calentamiento 2 s y medición 5 s completos, 70 + 150 solicitudes sin errores. Casos 100→120→160; SQL confirma 160 creaciones auditadas, 40 ediciones y 1600 entregas, cero intentos SMTP/trabajos IA. Diez logout 204 y QA detenido. p95 corto: listado 199,3 ms, detalle 190,5 ms, creación 931,9 ms y edición 434,0 ms. Smoke satisfactorio funcional, sin acreditar RNF-2; medición formal y diagnóstico de latencias pendientes.


## Línea base formal RNF-2: fuera de umbral

[Evidencia 126](evidencias/126-rendimiento-formal-fuera-umbral.json): treinta segundos de calentamiento y cinco minutos medidos con diez clientes; 7813 solicitudes, cero errores, diez logout 204 y QA detenido. p95: listado 283,1 ms, detalle 253,9 ms, creación 1245,9 ms y edición 476,0 ms; todas superan el límite inferior a 200 ms. Casos 100→295→2249; SQL confirma 2249 eventos CREADO, 2139 ediciones y 22490 entregas, cero intentos SMTP/trabajos IA. RNF-2 medido y no cumplido en esta configuración; requiere diagnóstico/optimización, no repetir sin cambio.


## Optimización de consultas del encolado preparada para regresión API

[Evidencia 127](evidencias/127-encolado-consultas-agrupadas.json): selección RH y búsqueda de entregas agrupadas, predicado de independencia compartido y transacción/UUID5 conservados. Perfil SQL aislado de funciones reales mediante AST/modelos SQLite: para 2/10/30 destinatarios, 10/42/122 sentencias antes y 4/4/4 después; mismas entregas, sin duplicados. Nueve comprobaciones de acceso equivalentes a versión previa y rollback correctos en ese alcance. Trece regresiones pytest de API añadidas, aún pendientes de ejecutar; sin nuevo p95 ni aprobación RNF-2.


## Regresión de la optimización de encolado aprobada

[Evidencia 128](evidencias/128-regresion-encolado-60-aprobadas.json): captura de la autora muestra 60 passed in 15.07s para test_mail.py, test_incidents.py y test_mail_batching.py, con integraciones DB desactivadas y autoload de plugins deshabilitado. Hashes del cambio coinciden con 127. Se completa esta regresión de API/SQLite y encolado; no es PostgreSQL concurrente ni suite completa. Pendiente nueva medición formal para comparar con la línea base fallida 126; no se acredita mejora de p95 todavía.


## Comparación formal después de agrupar encolado

[Evidencia 129](evidencias/129-rendimiento-encolado-comparacion.json): 11226 solicitudes en 300 s, cero errores, diez logout 204 y QA detenido. p95 antes→después: listado 283,1→301,8 ms; detalle 253,9→267,7 ms; creación 1245,9→609,0 ms; edición 476,0→485,9 ms. Creación mejora aproximadamente 51,1% y solicitudes aumentan 43,7%, pero las cuatro siguen fuera del umbral. Casos finales 3205, 3096 ediciones auditadas y 32050 entregas, cero intentos SMTP/trabajos IA. Conjuntos finales distintos por mayor throughput; no se afirma causalidad exclusiva. RNF-2 permanece incumplido.


## Consulta de autenticación agrupada, pendiente de regresión API

[Evidencia 130](evidencias/130-autenticacion-consulta-agrupada.json): current_user reúne sesión/usuario/departamento en una consulta, sin cachear permisos y refrescando identidad ORM. Perfil SQLite del cuerpo real: 3→1 consultas para sesión válida; doce escenarios mantienen estados/mensajes y tres cambios externos son detectados. Trece regresiones API nuevas preparadas, todavía no ejecutadas. Bloqueos, lifecycle, get_session, login y política de claves sin cambios. Sin nuevo p95: RNF-2 sigue fuera de umbral en 129.


Regresión de autenticación completada: [evidencia 131](evidencias/131-autenticacion-22-aprobadas.json), captura de la autora con 22 passed in 13.84s en test_auth.py y test_auth_queries.py. Hashes coinciden con 130. Validación SQLite/TestClient, sin nueva latencia PostgreSQL; pendiente medición formal después de agrupar consulta de autenticación. RNF-2 continúa fuera de umbral según 129.


## Tercera medición formal tras agrupar autenticación

[Evidencia 132](evidencias/132-rendimiento-auth-comparacion.json): 13072 solicitudes en 300 s, diez clientes, cero errores y QA detenido. p95 anterior→nuevo: listado 301,8→236,6 ms; detalle 267,7→206,2 ms; creación 609,0→521,6 ms; edición 485,9→398,7 ms. Las cuatro mejoran, pero ninguna cumple <200 ms. Casos 100/360/3629; SQL confirma 3629 creaciones, 3516 ediciones y 36290 entregas, cero intentos SMTP/trabajos IA; diez logout 204. Throughput aumenta 16,4%; poblaciones finales distintas y host no controlado impiden atribución causal exclusiva. RNF-2 sigue incumplido.


## 22 de octubre de 2026 — Respuestas de escritura antes del commit

[Evidencia 133](evidencias/133-respuestas-escritura-sin-recarga.json): creación prepara el recibo bajo la transacción y las cuatro rutas de gestión capturan CaseDetail antes de confirmar. Solo se devuelve éxito tras commit; el servicio mantiene retorno ORM por defecto y Session conserva expire_on_commit. El cuerpo previo a queue_event de manage_case mantiene bloqueos, relectura de visibilidad, permisos y auditoría sin cambios por comparación AST.

Perfil aislado SQLite con cuerpos reales por AST: creación 14 → 11 consultas (después del commit: 4 → 0); edición 10 → 9 (1 → 0). Tres fallos simulados —commit de creación, commit de edición y presentador— conservaron caso, auditoría y cola sin cambios parciales. No ejecuta HTTP/Pydantic ni demuestra concurrencia PostgreSQL. Se prepararon 11 casos en backend/tests/test_write_responses.py, todavía pendientes de ejecutar con la regresión existente. Sin nueva medición Docker: RNF-2 continúa pendiente y la evidencia 132 conserva FALLA_UMBRAL.


## 22 de octubre de 2026 — Regresión de respuestas: preparación de tres casos corregida

[Evidencia 134](evidencias/134-regresion-escritura-correccion-fixtures.json): la autora ejecutó cinco archivos y obtuvo **79 aprobadas y 3 fallidas en 18,27 s**. Los tres fallos pertenecen al nuevo test_write_responses.py: dos peticiones de RH omitían el empleado afectado y devolvían 422; el fixture de transición marcaba clasificación vigente sin los campos exigidos por ck_incident_classification_valid. Se corrigió la preparación: afectado explícito y clasificación/asignación mediante las rutas reales antes de observar SQL. Las aserciones de respuesta, cero consultas posteriores al commit y rollback se conservan.

Solo cambió la preparación de backend/tests/test_write_responses.py; sin cambio de aplicación ni relajación de restricciones. AST comprobado, reejecución de los 11 casos pendiente. Los otros cuatro archivos pasaron en la ejecución aportada. RNF-2 continúa pendiente; no repetir carga hasta confirmar estos casos.


## 22 de octubre de 2026 — Respuestas de escritura: 11 pruebas aprobadas

[Evidencia 135](evidencias/135-respuestas-escritura-11-aprobadas.json): captura de terminal de la autora confirma **11 passed in 5.52s** para backend/tests/test_write_responses.py después de corregir la preparación documentada en 134. Cubre recibos, cuatro respuestas de gestión sin consultas posteriores al commit, rollback por fallos de commit/presentador y retorno ORM compatible. SQLite y dependencias sustituidas; no acredita concurrencia PostgreSQL, autenticación real ni suite completa. El resultado inicial de 134 se conserva.

La regresión del archivo corregido queda aprobada; los otros cuatro archivos ya pasaron en la ejecución de 134. No se atribuyen a una ejecución conjunta nueva. Siguiente paso: una medición formal full aislada con el ajuste de 133. RNF-2 sigue pendiente hasta ese reporte; 132 conserva FALLA_UMBRAL.


## 22 de octubre de 2026 — Medición posterior al ajuste de respuestas

[Evidencia 136](evidencias/136-rendimiento-respuestas-comparacion.json): corrida 3dabef717c5549c6 ejecutada por la autora; reporte original conserva FALLIDA_UMBRAL. Diez clientes, 30 s de calentamiento y 300 s completos de medición; 14346 solicitudes, cero errores, frente a 13072 anteriores.

| Operación | p95 anterior (ms) | p95 actual (ms) | Cambio |
| --- | ---: | ---: | ---: |
| listado | 236.55 | 249.83 | +5.6 % |
| detalle | 206.16 | 217.49 | +5.5 % |
| creacion | 521.57 | 449.40 | -13.8 % |
| actualizacion | 398.67 | 358.22 | -10.1 % |

Creación y edición mejoraron; listado y detalle aumentaron. Las cuatro siguen sobre el umbral de 200 ms. Conteos 100 → 439 → 4026; SQL confirma 4026 creaciones auditadas, 3919 ediciones, 40260 entregas en cola, cero intentos SMTP y cero trabajos IA. Diez sesiones revocadas con 204 y contenedores QA detenidos. Los hashes reportados de los tres archivos del ajuste coinciden con el código local.

Comparación observacional: población creciente y distinta, host compartido con generador, sin control exclusivo del entorno ni CPU del generador medida. No atribuir causalidad exclusiva ni identificar un cuello de botella a partir de estos agregados. RNF-2 sigue pendiente. No repetir full sin cambio; siguiente diagnóstico: medir coste por fase/consulta antes de optimizar de nuevo.


## 22 de octubre de 2026 — Diagnóstico por etapas preparado

[Evidencia 137](evidencias/137-diagnostico-etapas-qa-preparado.json): entrada ASGI de diagnóstico exclusiva de QA y opción --diagnostic del provisionador, permitida solo con smoke. Mide por fase/operación total ASGI, autenticación real, endpoint, SQL, commit y cantidad de consultas. Guard de base/usuario/run_id, proveedores deshabilitados y sin datos privados en agregados. Las respuestas, permisos y bloqueos de producto se mantienen. Los agregados se recogen al detener QA y sus conteos se cruzan con las peticiones HTTP.

Validación local final: **40 unitarias aprobadas en 1,681 s**, con dobles ASGI sin sockets, propagación de contexto a hilos y Docker simulado. Incluye 13 casos nuevos y 27 anteriores. No hubo ejecución real de API/Docker; no se afirma integración aprobada. Dos intentos previos se interrumpieron durante creación de loop asyncio Windows; traza en socketpair/accept. Las dobles se adaptaron para no requerir sockets; esos intentos no se cuentan como aprobados.

RNF-2 sigue pendiente y 136 conserva FALLIDA_UMBRAL. El diagnóstico añade coste y dura 2+5 s de carga; no acredita rendimiento. SQL/commit se solapan con auth/endpoint: no sumar sus p95. SQL excluye pool/pre_ping interno y parte ORM; total ASGI excluye red/cliente. Primera corrida diagnóstica real pendiente.


## 22 de octubre de 2026 — Diagnóstico QA real revisado

[Evidencia 138](evidencias/138-diagnostico-etapas-qa-resultados.json): corrida e22ded0274034faf, estado DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2. Captura y reporte aportados por la autora: 231 peticiones en los 5 s medidos, cero errores; conteos de ocho grupos coinciden con las dos fases HTTP según validación del provisionador.

Medias por petición, en ms salvo cantidad de consultas. SQL y commit son subconjuntos solapados: no sumar columnas.

| Operación | ASGI | Auth | Endpoint | SQL | Commit | Consultas |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| listado | 196.86 | 49.33 | 41.63 | 62.59 | 0.00 | 4.00 |
| detalle | 159.85 | 43.17 | 25.96 | 46.38 | 0.00 | 3.00 |
| creacion | 355.41 | 34.46 | 246.59 | 239.82 | 12.18 | 13.00 |
| actualizacion | 239.97 | 36.42 | 127.13 | 127.43 | 10.89 | 11.00 |

Creación concentra el mayor coste observado; SQL acumulado supera ampliamente al commit. Esto orienta la revisión a las 13 consultas y sus viajes, sin identificar una sentencia o causa única. Residual fuera de auth/endpoint entre 74,37 y 105,90 ms de media; no atribuirlo directamente a red o base: incluye planificación, dependencias, serialización y potencial limpieza posterior al envío. Total ASGI no equivale al tiempo HTTP cliente; sus p95 no son intercambiables.

Conteos 100 → 120 → 175; SQL confirma 175 creaciones auditadas, 73 ediciones, 1750 entregas, cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido. Smoke instrumentado corto, 54–61 muestras por operación; no acredita RNF-2 ni mejora frente a 136. Sin nueva modificación de código o carga completa. Pendiente: revisar coste y necesidad de consultas de creación preservando permisos/bloqueos; medir por familias si falta detalle.


## 22 de octubre de 2026 — Relectura administrativa agrupada

[Evidencia 139](evidencias/139-relectura-administrativa-agrupada.json): administration_lock conserva el advisory compartido/exclusivo con clave 71419322 y, después de adquirirlo, relee usuario y departamento en una consulta con populate_existing. Sustituye tres lecturas del helper; no cachea permisos ni cambia transacciones. La identidad se obtiene sin cargar atributos expirados y el actor debe pertenecer a la Session actual. Filas ausentes o inactivas reciben 403 explícito. Llamadas sin actor conservan su comportamiento.

Perfil aislado SQLite de cuerpos reales por AST: creación **11 → 9** consultas; edición **9 → 7**, sin lecturas posteriores al commit. Catorce comprobaciones locales aprobaron actividad, cambios de rol/departamento, expiración, ausencias, identidad de Session y orden del SQL advisory simulado. No prueban concurrencia PostgreSQL ni HTTP/Pydantic. Se prepararon 14 casos pytest en test_administration_lock_queries.py, cuya ejecución con los servicios afectados sigue pendiente.

Sin medición formal nueva: el ahorro de consultas no garantiza p95. RNF-2 continúa pendiente y 136 conserva FALLIDA_UMBRAL. Próximo paso: regresión API/servicios; no repetir full hasta aprobarla.


## 22 de octubre de 2026 — Regresión administrativa aprobada: 128 pruebas

[Evidencia 140](evidencias/140-regresion-administrativa-128-aprobadas.json): captura de la autora confirma **128 passed in 27.84s** en los ocho archivos seleccionados: relectura administrativa, incidencias, administración de usuarios, departamentos, IA, correo, respuestas de escritura y autenticación. Incluye los 14 casos nuevos preparados en 139. RUN_DB_TESTS=0 y autoload de plugins deshabilitado según terminal.

La regresión seleccionada del ajuste queda aprobada. No es suite completa ni demuestra concurrencia PostgreSQL. Próximo paso: una corrida full QA sin instrumentación diagnóstica para comparar con 136. RNF-2 sigue pendiente hasta el nuevo reporte; no se declara mejora de p95 a partir de estos tests.


## 22 de octubre de 2026 — Relectura administrativa: sin mejora de p95 en carga formal

[Evidencia 141](evidencias/141-rendimiento-relectura-administrativa.json): corrida e0b63b390b764550 sin instrumentación diagnóstica, diez clientes, 30 s de calentamiento y 300 s medidos completos. Resultado FALLIDA_UMBRAL: **13873 solicitudes sin errores**, frente a 14346 en 136.

| Operación | p95 anterior (ms) | p95 actual (ms) | Cambio |
| --- | ---: | ---: | ---: |
| listado | 249.83 | 286.91 | +14.8 % |
| detalle | 217.49 | 258.43 | +18.8 % |
| creacion | 449.40 | 505.98 | +12.6 % |
| actualizacion | 358.22 | 393.49 | +9.8 % |

Las cuatro aumentaron en p95; creación y edición bajaron ligeramente en mediana, lo cual no cumple ni sustituye el criterio. El ahorro local de consultas de 139 y la regresión aprobada de 140 no demostraron mejora de p95 aquí. El hash del helper coincide con el declarado por el reporte. Conteos 100 → 368 → 3837; SQL confirma 3837 creaciones auditadas, 3730 ediciones, 38370 entregas, cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido.

Comparación observacional con host compartido y población creciente distinta; las muestras CPU de contenedores no miden el generador ni explican por sí solas el resultado. No afirmar causa única ni relajar controles. RNF-2 continúa pendiente. No repetir full sin cambio justificado: investigar variabilidad, coste residual, consultas por familias y carga del generador/host.


## 22 de octubre de 2026 — Diagnóstico v2: familias SQL, respuesta y CPU

[Evidencia 142](evidencias/142-diagnostico-familias-cpu-preparado.json): diagnóstico smoke ampliado para separar familias SQL y el tiempo de envío/cierre ASGI, más CPU del generador y del equipo Windows por fase. Sin cambios en servicios de negocio ni umbral RNF-2. Etiquetas SQL proceden de verbos/tablas conocidos; no se guardan consultas, parámetros o datos de casos. Las sumas por familia deben coincidir con cantidad y tiempo SQL global.

Validación local: **46 unitarias aprobadas en 2,536 s** (seis nuevas y 40 anteriores), con ASGI/Docker simulados y CPU sintética. Callbacks reales cargados por AST con SQLite agruparon las 9 consultas de creación y 7 de edición sin pérdidas. Sondeo GetSystemTimes disponible, pero intervalo inmediato sin delta válido se reportó NO_DISPONIBLE; no hubo medida real bajo carga. AST de siete archivos comprobado. Integración v2 real pendiente.

CPU del generador usa todos sus hilos y se presenta por núcleo/equipo; CPU host incluye otras aplicaciones/VM. Son medias de fase, sin atribución causal. hasta_envio marca entrega a ASGI, no recepción cliente; cierre cubre el resto. Familias pueden combinar consultas distintas y no equivalen a EXPLAIN. SQL/commit se solapan con auth/endpoint; no sumar p95. Instrumentación añade coste. RNF-2 continúa pendiente y 141 conserva FALLIDA_UMBRAL.


## 22 de octubre de 2026 — Diagnóstico v2 real: inserción de correo como mayor familia de creación

[Evidencia 143](evidencias/143-diagnostico-familias-cpu-resultados.json): corrida f7457a68919e4fb2 terminó DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2. Diez clientes, 2+5 s, **249 solicitudes medidas sin errores**. Los ocho grupos concuerdan con HTTP y sus familias suman consultas y tiempo SQL. Creación mantiene 11 consultas/petición y edición nueve, coherentes con el ahorro local de 139 más autenticación y advisory PostgreSQL.

En creación INSERT/mail_deliveries es la mayor familia: **66,05 ms de media por petición**, frente a 11–13,4 ms en la mayoría de otras familias y 22,25 ms de autenticación SQL. SQL acumulado medio 198,93 ms. Conteos confirman diez entregas por creación; una ejecución instrumentada no prueba cuántos viajes hace internamente el driver. Próxima revisión: forma de insertar varias MailDelivery juntas, conservando destinatarios, IDs, idempotencia y transacción.

Generador: 5,15 % de un núcleo / **1,29 % del equipo** de cuatro CPU; host global medio **73,64 %**. No demuestra saturación continua ni causa única. Creación: media hasta entregar último cuerpo a ASGI 303,97 ms y cierre 19,14 ms; total 323,11 ms. El cierre no explica todo el residual; no equivale a tiempo de recepción HTTP cliente. No sumar p95 de componentes solapados.

Conteos 100 → 124 → 185; SQL: 185 creaciones auditadas, 80 ediciones, 1850 entregas, cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido. Smoke con 60–66 muestras por operación y coste instrumental: no acredita RNF-2. 141 conserva FALLIDA_UMBRAL. No repetir full sin un cambio justificado y regresión previa.


## 22 de octubre de 2026 — Entregas de correo en INSERT multirregistro

[Evidencia 144](evidencias/144-correo-insert-multirregistro.json): queue_event prepara las mismas filas y usa INSERT VALUES múltiples de hasta 50 entregas por sentencia. Diez destinatarios caben en una sentencia; se conservan UUID5, consulta de IDs existentes, destinatarios, contexto/estados y la misma transacción del caso/auditoría. Sin commit propio, SMTP o Redis. El worker y sus comprobaciones permanecen idénticos por AST.

Perfil local con SQLAlchemy/SQLite y cuerpos reales por AST: antes executemany con 2/10/30/123 juegos; ahora execute único para 2/10/30 y tres sentencias para 123. Compilación PostgreSQL válida, máximo 600 parámetros por bloque. No prueba viajes ni rendimiento PostgreSQL. Nueve escenarios de destinatarios coinciden con el control previo y revierten correctamente. Reintento parcial conserva fila ENVIADA y rellena la ausente; fallo del segundo bloque revierte filas previas y auditoría al hacer rollback.

Se prepararon seis casos en test_mail_multivalues.py. El test existente de fallo de outbox ahora intercepta INSERT real en lugar de objetos ORM pendientes; mantiene 503 y conteos cero de caso/auditoría/entregas. Pytest de API pendiente; no se declaran estas pruebas aprobadas. Sin p95 nuevo: RNF-2 sigue pendiente y 141 conserva FALLIDA_UMBRAL. Próximo paso: regresión de correo/incidencias/respuestas; después diagnóstico breve, sin repetir full automáticamente.


## 22 de octubre de 2026 — Correo multirregistro: 77 pruebas aprobadas

[Evidencia 145](evidencias/145-correo-multirregistro-77-aprobadas.json): captura de la autora confirma **77 passed in 23.15s** en test_mail_multivalues.py, test_mail.py, test_mail_batching.py, test_incidents.py y test_write_responses.py. Incluye los seis casos nuevos preparados en 144 y el test de fallo de outbox adaptado al INSERT real. Variables visibles: SSLKEYLOGFILE vacío, RUN_DB_TESTS=0 y PYTEST_DISABLE_PLUGIN_AUTOLOAD=1.

Regresión seleccionada aprobada; no es suite completa ni medición PostgreSQL/rendimiento. Siguiente paso: una corrida smoke diagnóstica v2 para contrastar la familia INSERT/mail_deliveries con 143, preservando límites de comparación y verificación de conteos. No repetir full automáticamente. RNF-2 sigue pendiente y 141 conserva FALLIDA_UMBRAL.


## 22 de octubre de 2026 — Menor coste de INSERT correo, CPU host alta

[Evidencia 146](evidencias/146-diagnostico-correo-mejora-host-alto.json): diagnóstico 4fc3ea94293a4348 completó **150 solicitudes medidas sin errores**. La familia INSERT/mail_deliveries bajó de **66,05 a 16,94 ms medios por petición** (aprox. −74,4 %); hash del servicio coincide con el ajuste de 144. No es mejora global: creación ASGI media subió de 323,11 a 423,33 ms. CPU global media subió de **73,64 % a 95,27 %**, mientras generador bajó de 1,29 % a 0,68 % del equipo. Comparación observacional de smoke con cargas distintas; no causa única ni cumplimiento RNF-2.

Ocho grupos y sumas SQL/HTTP coherentes. SQL confirma 155 casos/creaciones auditadas, 41 ediciones, 1550 entregas y cero SMTP/IA. Diez sesiones revocadas con 204 y QA detenido. La muestra actual de procesos desde herramientas solo expuso pwsh; no sirve de inventario del host ni para identificar responsables.

Se preparó backend/scripts/check_performance_host.ps1, solo lectura y muestra breve de CPU por proceso en terminal de la autora. No cierra procesos ni cambia configuración; datos posteriores no explican retrospectivamente la corrida. Antes de repetir carga, revisar consumidores actuales. No repetir full automáticamente. RNF-2 continúa pendiente; 141 conserva FALLIDA_UMBRAL.


## 22 de octubre de 2026 — Sondeo parcial de procesos y CPU global pendiente

[Evidencia 147](evidencias/147-sondeo-procesos-baseline-global.json): la autora aportó salida de 5,7 s, cuatro CPU, 252 procesos comparados y 214 lecturas no disponibles. Mayor consumidor visible 4,8 % del equipo; suma parcial del top 10, 19,47 %. Esa suma no es CPU global ni permite atribuir los 95,27 % de 146 a una aplicación: es una muestra posterior con cobertura parcial. No se indicó ni ejecutó cierre de procesos.

Se agregó `performance_host.py --baseline`, solo lectura: tres intervalos globales Windows de dos segundos, sin generar carga ni consultar procesos. Media ponderada con medidas válidas; ausencia se conserva como null. **48 pruebas locales aprobadas en 1,880 s**, dos nuevas, con CPU sintética y Docker/ASGI simulados. Baseline en terminal de la autora pendiente. RNF-2 sigue pendiente; no repetir full automáticamente.


## 22 de octubre de 2026 — CPU global 97,42 % sin carga generada

[Evidencia 148](evidencias/148-cpu-global-baseline-97-4.json): salida aportada por la autora de performance_host.py --baseline. Tres intervalos válidos: 92,12 %, 99,82 % y 100,00 %; media ponderada **97,42 %** durante aproximadamente 6,4 s. El script no genera carga de prueba, pero otras aplicaciones/servicios/VM pueden estar activos. La medida es actual y no atribuye retrospectivamente los resultados anteriores a una causa exclusiva.

No repetir benchmark bajo estas condiciones. Próximo paso: contrastar CPU global y procesos ordenados por consumo en Administrador de tareas; no cerrar procesos automáticamente. La lista parcial de 147 no identifica al responsable. RNF-2 sigue pendiente y 141 conserva FALLIDA_UMBRAL; no cambiar el umbral ni declarar correcto el rendimiento del producto.


## 22 de octubre de 2026 — Rendimiento: informe consolidado y mediciones diferidas

[Evidencia 149](evidencias/149-rendimiento-informe-consolidado.json): PRUEBA_RENDIMIENTO.md consolidado en el mismo archivo; corrige el encabezado obsoleto «medición real no ejecutada», reúne cinco formales cotejadas con sus JSON, protocolo y uso actual, diagnóstico v2 y pendientes. Todos los enlaces JSON previos se conservan; no se reescriben reportes originales ni se crean versiones paralelas del informe.

Revisión estática acotada de correo: mismo hash que diagnóstico 146, sin commit propio, UUID5 y lotes de 50 conservados; consumidores consultan filas persistidas. Sin cambio de servicios ni repetición de tests/carga. La autora usa Brave para videollamada; última captura CPU 32 %/memoria 84 % es observación instantánea. Mantener actividad y diferir mediciones de carga hasta después de la llamada. RNF-2 permanece pendiente; última formal 141 no incluye INSERT multirregistro y no se declara mejora global.


## 22 de octubre de 2026 — Sexta formal: mejora observada, umbral pendiente

[Evidencia 150](evidencias/150-rendimiento-formal-correo-multirregistro.json): corrida c0baad3867644ad2 sin diagnóstico, diez clientes y 30+300 s completos; **15349 solicitudes sin errores** frente a 13873 de 141. p95 listado 286,91 → 259,28 ms; detalle 258,43 → 221,32; creación 505,98 → 385,49; edición 393,49 → 347,43. Las cuatro mejoran y siguen >=200 ms. No acreditar RNF-2 ni atribuir causalidad exclusiva: el host y la población difieren.

Conteos 100 → 502 → 4341; auditoría confirma 4341 creaciones, 4231 ediciones y 43410 entregas; cero SMTP/IA. Diez logout 204 y QA detenido. Hash de correo coincide con INSERT multirregistro; captura previa CPU 19 %/memoria 86 % es instantánea, sin medir toda la ventana. Informe consolidado actualizado en el mismo archivo con sexta fila y estado vigente. No repetir full sin otro cambio/diagnóstico justificado.


## 22 de octubre de 2026 — Rol validado reutilizado dentro de la gestión

[Evidencia 151](evidencias/151-gestion-rol-leido-una-vez.json): helper privado puro para construir el mismo predicado de visibilidad con rol ya validado. La entrada pública sigue leyendo rol; manage_case lo valida tras bloqueo administrativo y eligible_manager al validar responsable. Reuso local a esa operación, sin cachear entre peticiones ni cambiar bloqueo de caso antes de reevaluar visibilidad.

Perfil aislado SQLite de funciones reales por AST: edición **7 → 6** consultas, creación **9 → 9**. Seis comprobaciones locales aprobaron gestores permitidos, empleado denegado, responsables y bajada de rol entre peticiones con actor obsoleto. Nueve escenarios de destinatarios conservaron resultados/rollback. Predicado y SELECT de bloqueo del caso idénticos por AST. No prueba FastAPI/Pydantic ni concurrencia PostgreSQL. Seis casos pytest preparados en test_lifecycle_role_queries.py; ejecución pendiente. Sin p95 nuevo: 150 sigue fuera de umbral y es anterior a este cambio.


## 22 de octubre de 2026 — Reutilización del rol: 75 pruebas aprobadas

[Evidencia 152](evidencias/152-gestion-rol-regresion-75-aprobadas.json): captura de la autora confirma **75 passed in 12.91s** en cinco archivos: consultas de rol en gestión, incidencias, administración de usuarios, correo y respuestas de escritura. Incluye los seis casos nuevos de 151. Variables y comando visibles; RUN_DB_TESTS=0. Regresión seleccionada aprobada, sin suite completa o prueba de concurrencia PostgreSQL.

Informe consolidado actualizado: 151 ya tiene regresión API seleccionada, pero no diagnóstico/formal posterior. Las 77 pruebas anteriores son otra selección y no se suman como únicas. Próximo paso: una corrida smoke diagnóstica para revisar SELECT/roles, conteos y condiciones; no repetir full automáticamente. RNF-2 continúa pendiente y 150 conserva FALLIDA_UMBRAL.


## 22 de octubre de 2026 — Una lectura de rol confirmada en diagnóstico real

[Evidencia 153](evidencias/153-gestion-rol-diagnostico-real.json): corrida 33d131e588f1435a terminó DIAGNOSTICO_QA_SIN_ACREDITAR_RNF2. **229 solicitudes medidas sin errores**; edición pasó de 9 a 8 consultas y SELECT/roles de dos a una por petición. Hashes de los dos servicios coinciden con el código del ajuste. Ocho grupos y sumas por familia concordantes.

CPU global media 81,06 %; generador 0,38 % del equipo. Edición ASGI media 247,80 ms: auth 49,56 ms, endpoint 110,98 ms y residual 87,25 ms. No sumar p95 ni atribuir a una causa única; smoke corto y condiciones distintas. SQL confirma 178 casos/creaciones auditadas, 70 ediciones, 1780 entregas, cero SMTP/IA. Diez logout 204 y QA detenido.

Reducción SQL prevista confirmada, sin acreditar latencia formal. Informe consolidado actualizado; 150 sigue siendo la última de seis formales fallidas. RNF-2 pendiente. Revisar costes comunes antes de otra formal y no repetir full automáticamente.


## 22 de octubre de 2026 — Diagnóstico v3 de espera/retorno de hilos preparado

[Evidencia 154](evidencias/154-diagnostico-esperas-hilos-preparado.json): instrumentación opcional solo en la entrada QA de anyio.to_thread.run_sync. Categorías fijas distinguen autenticación, endpoint, validación de respuesta, apertura/cierre de dependencia y otras. Mide espera/ejecución/retorno, sin guardar argumentos/resultados o cambiar limiter/cancelación, sin reintentos. Llamadas incompletas y sumas discordantes invalidan el agregado. No cambia aplicación normal ni servicios de negocio.

**56 unitarias locales aprobadas en 1,251 s**, ocho nuevas; dobles ASGI/ejecutor y contexto en hilo real, sin servidor FastAPI/AnyIO o Docker real. Primera corrida v3 pendiente. Instrumentación añade coste y sus componentes se solapan: no sumar p95 ni atribuir causa única. RNF-2 pendiente y 150 conserva FALLIDA_UMBRAL. Solo un smoke diagnóstico nuevo se justifica; no repetir full automáticamente.


## 22 de octubre de 2026 — Esperas y retornos de hilos medidos

[Evidencia 155](evidencias/155-diagnostico-hilos-resultados.json): diagnóstico 19f2fbae76134abb completó **224 solicitudes medidas sin errores**, ocho grupos, sumas SQL/hilos concordantes y cero llamadas incompletas. En edición, cinco pasos por hilo: espera media 42,09 ms, retorno 36,24 ms y ejecución 130,01 ms; ASGI total medio 215,31 ms. Apertura y validación de respuesta ejecutan menos de 0,1 ms cada una, pero espera/retorno suman unos 15,00 y 13,85 ms respectivamente.

Cierre posterior al envío: ejecución 0,049 ms y espera/retorno 17,71 ms en estas escrituras; no representa todo el cierre posible de lecturas ni toda la latencia cliente. CPU host media 80,26 %. No sumar p95 ni atribuir a limiter/OS/GIL una causa única. SQL confirma 184 casos/creaciones, 73 ediciones, 1840 entregas, cero SMTP/IA. Diez logout 204 y QA detenido.

Orientación: evaluar reducción acotada de pasos de tareas pequeñas, manteniendo SQL y rollback/cierre bloqueante en worker, validación y limpieza ante errores/cancelación. Sin modificación funcional nueva o p95 formal; 150 conserva FALLIDA_UMBRAL y RNF-2 pendiente. No repetir carga automáticamente.


## 22 de octubre de 2026 — Apertura de sesión sin paso por worker

[Evidencia 156](evidencias/156-sesion-apertura-sin-salto-hilo.json): get_session es generador asíncrono. Construye Session sin consultas/checkout; mantiene autenticación, endpoints y SQL en sus workers. El cierre potencialmente bloqueante usa worker, CapacityLimiter(1) independiente y protección CancelScope(shield=True). Sin commit implícito ni supresión/reintentos de errores. Busca retirar únicamente el paso de apertura señalado por 155; no cambia permisos, auditoría o cola.

**7 pruebas locales aprobadas en 0,143 s**, con SQLAlchemy/SQLite y worker reales, dobles de AnyIO sin event loop. Comprueban entrada sin SQL/salto, rollback en worker, commit conservado, cierre único, errores/CancelledError inyectada, fallo de cierre y factory. **Tres integraciones AnyIO/FastAPI preparadas, todavía no ejecutadas**, y regresión API pendiente; las locales no acreditan cancelación real. No repetir carga antes de esa regresión. RNF-2 pendiente, sin nuevo p95; 150 conserva FALLIDA_UMBRAL.


## 22 de octubre de 2026 — Regresión de sesión asíncrona: 93 aprobadas

[Evidencia 157](evidencias/157-sesion-asincrona-regresion-93-aprobadas.json): la autora ejecutó los siete archivos solicitados con RUN_DB_TESTS=0 y plugins automáticos desactivados; captura muestra **93 passed in 17.43s**, 100 %, sin errores. Incluye los diez casos de test_database_session.py y sus tres integraciones AnyIO/FastAPI reales: cierre con limiter general ocupado, limpieza ante cancelación de ámbito y rollback de la dependencia original tras HTTP 200/409. Hashes actuales coinciden con 156; no son prueba retrospectiva del proceso capturado.

La regresión seleccionada del ajuste 156 queda aprobada, sin equivaler a suite completa ni PostgreSQL/Docker real. No sumar siete locales como pruebas adicionales. RNF-2 continúa pendiente, sin nuevo p95; 150 conserva FALLIDA_UMBRAL. Próximo paso: un smoke diagnóstico para contrastar retirada del salto de apertura, integridad de auditoría/colas y cierre; no repetir full automáticamente.


## 22 de octubre de 2026 — Diagnóstico de sesión interrumpido en arranque QA

[Evidencia 158](evidencias/158-sesion-smoke-arranque-incompleto.json): corrida cc10cf1d32dd4a8d terminó **INCOMPLETA**, código ARRANQUE_QA_SALIDA_1 después de validar configuración. Compose falló construyendo/iniciando; no llegó a migraciones, fixture, carga ni tiempos por hilos. Parada no confirmada (contenedores_detenidos=false, parada_requiere_revision=true); comprobar estados sin asumir que siguen en ejecución. Recursos retenidos sin borrar volúmenes.

Causa raíz no disponible en el reporte resumido; no atribuir a código, RAM, disco o permisos. Antes de repetir: comprobar servidor Docker y estados del proyecto exacto. La regresión seleccionada 157 de 93 aprobadas se conserva; efecto de 156 y RNF-2 pendientes. No hay p95 nuevo ni cambio de producto en este avance.


## 22 de octubre de 2026 — Docker disponible y proyecto QA sin contenedores

[Evidencia 159](evidencias/159-docker-disponible-qa-sin-contenedores.json): captura de la autora confirma servidor Docker 29.6.1 y listado sin filas para el filtro exacto del proyecto cc10cf1d32dd4a8d. En esta consulta no hay contenedores de esa corrida por detener. No demuestra ausencia de volúmenes/redes/imágenes ni reconstruye el estado durante el fallo; reporte 158 intacto.

Causa de arranque todavía pendiente. Dockerfile/specification revisados: siguiente diagnóstico acotado es construir solo la imagen QA con salida plain, sin servicios ni carga. Sin nueva medición, borrados, cambios funcionales o pruebas adicionales; 157 conserva 93 aprobadas y RNF-2 sigue pendiente.


## 22 de octubre de 2026 — Construcción explícita de imagen QA completada

[Evidencia 160](evidencias/160-imagen-qa-construida-diagnostico-pendiente.json): salida aportada por la autora muestra construcción/exportación/naming/unpacking completos de plurione-qa-perf-cc10cf1d32dd4a8d-api:latest, sin ERROR. Pasos de aplicación/dependencias en caché; no es instalación limpia ni arranque de servicios. El fallo 158 no se reprodujo en esta construcción, pero su causa histórica sigue desconocida.

Tras disponibilidad y ausencia de contenedores comprobadas en 159, corresponde un único reintento de smoke diagnóstico con proyecto nuevo para verificar arranque completo y efecto de 156. Sin full, sobrescritura o borrado de la corrida fallida. 157 mantiene 93 aprobadas; no hay p95 nuevo y RNF-2 pendiente.


## 22 de octubre de 2026 — Segundo fallo QA antes de generar carga

[Evidencia 161](evidencias/161-segundo-fallo-arranque-qa-sin-medicion.json): corrida 6bcb02bfdbe040ad vuelve a INCOMPLETA/ARRANQUE_QA_SALIDA_1 tras validar configuración, antes de migraciones/fixture/carga; parada no confirmada. Reporte original y hash conservados. La construcción correcta 160 no explica este fallo; command() solo conserva el código por privacidad.

Se observaron 16 carpetas de corridas; cada configuración reserva dos redes y stop las conserva. Posible agotamiento de direcciones por comprobar, sin inferir inventario real a partir de carpetas. Siguiente paso acotado: crear red interna temporal vacía con nombre aleatorio y retirar solo esa red si se creó correctamente; observar error original. No repetir smoke/full, iniciar servicios o borrar redes existentes. Sin resultados nuevos de rendimiento; 157 mantiene 93 aprobadas y RNF-2 pendiente.


## 22 de octubre de 2026 — Pools de direcciones agotados: limpieza QA acotada preparada

[Evidencia 162](evidencias/162-redes-direcciones-agotadas-limpieza-preparada.json): la prueba de red devolvió «all predefined address pools have been fully subnetted», confirmando el agotamiento actual. Es consistente con los fallos de arranque 158/161, sin recuperar su stderr histórico. La red de prueba no se creó.

Nueva release_performance_networks.py: revisión por defecto; --apply --limit 2 retira hasta dos redes QA vacías con nombre/etiquetas, reporte y compose originales concordantes. Exige contexto Docker local, revalida ID/uso/propiedad antes de rm, no toca contenedores, imágenes, volúmenes o reportes. No hace prune global ni cambia la retención automática del provisionador.

**63 pruebas locales aprobadas en 1,401 s**, siete nuevas de limpieza, con Docker simulado. AST de dos archivos correcto. Liberación real pendiente de ejecutar por la autora; no repetir carga antes de comprobarla. La selección API 157 mantiene 93 aprobadas y RNF-2 pendiente, sin nuevo p95.


## 22 de octubre de 2026 — Dos redes QA liberadas sin errores

[Evidencia 163](evidencias/163-liberacion-real-dos-redes-qa.json): la autora ejecutó release_performance_networks.py --apply --limit 2. La salida enumera 28 redes elegibles antes de aplicar y confirma únicamente dos eliminadas: 897c25b02d4340d6_net y d1c2d490b7df42b4_net, con prefijo plurione-qa-perf-. Sin omitidas al revalidar ni fallidas. No equivale a eliminar las 28 listadas ni a inventario global; herramienta limitada a redes QA vacías registradas, sin contenedores/volúmenes/imágenes/reportes o prune.

La limpieza real de 162 queda observada. Procede un smoke diagnóstico nuevo para comprobar reserva efectiva de dos redes, arranque completo y efecto del ajuste de sesión 156; no liberar más automáticamente ni lanzar full. No hay medición nueva, RNF-2 pendiente y 157 mantiene 93 aprobadas. Reportes 158/161 intactos.


## 22 de octubre de 2026 — Diagnóstico real: cuatro pasos por hilo confirmados

[Evidencia 164](evidencias/164-sesion-diagnostico-cuatro-hilos-resultados.json): corrida 077bbcf2cb8d4142 completó **249 peticiones medidas sin errores** tras liberar dos redes en 163. Ocho grupos v3 y sumas concordantes, cuatro pasos por hilo en todos los grupos (antes cinco), sin dependency_enter ni llamadas incompletas. Hash de database.py coincide con 156. Cierre registrado como other, SQL en worker conservado.

SQL por petición listado/detalle/creación/edición: 4/3/11/8. Conteo HTTP 100 → 120 → 181; PostgreSQL confirma 181 casos/creaciones auditadas, 73 ediciones, 1810 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido.

El objetivo estructural se confirma; no hay mejora global de latencia demostrada. Edición ASGI media 269,85 ms frente a 215,31 en 155; commit medio 66,42 frente a 11,14 ms, p95 de commit actual 356,23 ms. Espera/retorno medios de hilos 32,71/32,02 ms frente a 42,09/36,24. CPU global media 68,02 %, generador 1,16 % del equipo. Smoke corto instrumentado y condiciones variables: no sumar p95 ni atribuir causa única.

HTTP p95 de este smoke: listado 190,86; detalle 203,76; creación 465,74; edición 488,66 ms. No acredita RNF-2 ni sustituye la formal 150 FALLIDA_UMBRAL. Siguiente revisión: coste de commit/endpoint y alcance de la temporización antes de otro ajuste; no repetir full automáticamente.


## 22 de octubre de 2026 — Alcance del commit revisado sin cambios de durabilidad

[Evidencia 165](evidencias/165-revision-alcance-commit-sin-sql-pendiente.json): revisión de servicios y SQLAlchemy instalado, más dos comprobaciones locales con funciones extraídas por AST y modelos/SQLite reales. Creación y edición con presenter confirman una vez en Session y driver, con cero objetos nuevos/sucios/borrados al entrar en before_commit y cero SQL/flush hasta after_commit. No hay trabajo redundante identificado dentro de ese intervalo en los escenarios comprobados.

El cronómetro QA acaba antes de expiración (_remove_snapshot) y cierre; el servicio ya ejecutó flush y captura del esquema antes de commit. Los 66,42 ms medios de edición en 164 no representan esas tareas posteriores. Incluyen confirmación del driver y esperas no separadas; no atribuir a WAL/disco/red/GIL una causa única con estos agregados. No se cambian commit, durabilidad, atomicidad, auditoría o permisos.

Otra oportunidad acotada de 164: validación de respuesta ejecuta 0,029 ms dentro del hilo y espera/retorna 15,45 ms. Siguiente revisión de implementación: consolidar preparación/validación de DTO en el worker del endpoint, preservando validación y sin SQL en el event loop. Sin nueva instrumentación, carga o latencia en este avance. RNF-2 pendiente; regresión 157 y formal 150 conservan su alcance.


## 22 de octubre de 2026 — DTO validado en el worker del endpoint preparado

[Evidencia 166](evidencias/166-respuesta-validada-en-worker-preparada.json): worker_response agrupa ejecución original y captura/validación de Receipt/CasePage/CaseDetail en un trabajo de hilo para listado, detalle, registro y edición. La ruta es async con firma preservada; response_model y serialización de FastAPI se conservan sobre DTO ya preparado. No pasa ORM/SQL al event loop, ni cambia seguridad, SQL, locks, commit, auditoría, cola o cierre. Errores de salida mantienen ResponseValidationError y loc=response; excepciones del servicio se propagan.

Diagnóstico QA adaptado para medir el worker y conservar async. Endpoint incluye ahora la preparación/validación de DTO, sin espera/retorno: declarar esa diferencia de alcance al comparar. Se esperan tres pasos por hilo frente a cuatro, todavía sin ejecución QA real. Misma versión v3 y categorías, con clasificación del worker conocido como endpoint.

**7 pruebas locales del ajuste aprobadas en 0,054 s** con hilo/Pydantic reales y offload simulado; **64 unitarias de herramientas aprobadas en 1,661 s**, una nueva. AST de seis archivos y cuatro rutas correcto. Dos integraciones FastAPI nuevas preparadas, sin ejecutar; regresión API pendiente. Sin nueva carga/latencia ni aprobación RNF-2. Las 93 de 157 corresponden al ajuste anterior y no validan este cambio.


## 22 de octubre de 2026 — Regresión DTO en worker: 102 aprobadas

[Evidencia 167](evidencias/167-respuesta-worker-regresion-102-aprobadas.json): captura de la autora muestra **102 passed in 16.77s**, 100 %, ocho archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye nueve casos del nuevo helper y sus dos integraciones FastAPI reales: un offload de endpoint sin otro de validación de salida, y HTTP 500 ante DTO inválido. También incluye sesión/AnyIO, autenticación, incidencias, administración, correo y respuestas de escritura.

Hashes actuales de los seis archivos coinciden con preparación 166; no prueba retrospectiva de identidad del proceso. Selección aprobada, sin sumar siete locales anteriores ni extrapolar a suite completa/PostgreSQL. Antes de otro smoke diagnóstico, liberar como máximo dos redes QA vacías con herramienta validada y comprobar que se retiraron dos sin fallos; la corrida 164 volvió a reservar dos. No iniciar carga si esa comprobación falla. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL; sin nueva latencia o limpieza ejecutada por el agente.


## 22 de octubre de 2026 — DTO en worker: tres pasos por hilo confirmados

[Evidencia 168](evidencias/168-respuesta-worker-diagnostico-tres-hilos.json): limpieza previa de d1c2d490b7df42b4_entry y 42486b8ff1264162_net (prefijo plurione-qa-perf-) retiró dos redes sin fallos; el bloque condicionó la carga a ese resultado. Corrida 485d89bb828f4582 completó **236 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Tres pasos por hilo en todos los grupos (auth/endpoint/other), frente a cuatro en 164; sin validación en otro hilo, apertura o llamadas incompletas. Hashes de cuatro archivos de aplicación/instrumentación coinciden con 166.

Consultas por listado/detalle/creación/edición conservadas en 4/3/11/8. HTTP 100 → 130 → 190 casos; PostgreSQL confirma 190 casos/creaciones auditadas, 78 ediciones, 1900 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido.

HTTP p95 del smoke: listado 302,70; detalle 243,36; creación 427,86; edición 312,76 ms. Frente a 164, escritura mejora y lectura empeora; no hay mejora general o atribución causal demostrada. CPU global media 84,20 % frente a 68,02 %, generador 1,00 %. Commit de edición vuelve a 11,89 ms medios/p95 34,69, sin cambiar durabilidad: el pico previo no se repitió. ASGI edición media 220,86 ms; cierre 30,64 ms. Endpoint incluye ahora preparación/validación de DTO, alcance distinto declarado en 166.

Objetivo estructural confirmado y regresión 167 de 102 aprobadas conservada. RNF-2 pendiente; no sustituir formal 150 FALLIDA_UMBRAL ni repetir full automáticamente. Próxima revisión: viajes SQL y condiciones del entorno con base en evidencia, sin rebajar controles o durabilidad.


## 22 de octubre de 2026 — Rol agrupado en relectura posterior al bloqueo preparado

[Evidencia 169](evidencias/169-rol-agrupado-tras-bloqueo-preparado.json): administration_lock mantiene su modo anterior (None y lectura de usuario/departamento) y añade include_role=True para devolver el rol válido leído con LEFT JOIN en esa misma relectura posterior al advisory lock. Creación y gestión usan ese rol; el recibo usa el mismo predicado con rol validado. Sin caché entre solicitudes ni cambios de lock de expediente, escritura/commit, auditoría, colas o cierre. Ausencias/inactividad/rol desconocido conservan denegaciones y mensajes.

**9 unitarias locales aprobadas en 0,188 s** con servicios/modelos/SQLite reales. Cubren frescura de usuario/rol, no caché entre llamadas, rol ausente/desconocido, cuenta inactiva, compatibilidad previa, actor persistente y orden del lock compartido/exclusivo simulado. Perfil con funciones extraídas por AST antes/después: creación 9 → 8 y edición 6 → 5 consultas, sin SQL después de commit; no incluye autenticación ni advisory PostgreSQL. En QA se espera 11 → 10 y 8 → 7, sin acreditarlo todavía. AST de cinco archivos correcto.

Regresión API pendiente: las 102 de 167 validan el cambio anterior. No se ejecutó nueva carga o limpieza de redes ni se demostró latencia; RNF-2 pendiente y formal 150 FALLIDA_UMBRAL. Las escrituras usan advisory compartido; el perfil SQLite no lo ejecuta. No repetir diagnóstico antes de regresión.


## 22 de octubre de 2026 — Rol agrupado: 98 pruebas y cuatro subpruebas aprobadas

[Evidencia 170](evidencias/170-rol-agrupado-regresion-98-aprobadas.json): captura de la autora muestra **98 passed, 4 subtests passed in 11.72s**, 100 %, siete archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye nueve nuevas pruebas de rol agrupado y regresión de lock/rol de gestión, incidencias, administración, correo y respuestas transaccionales. Cuatro subpruebas registradas por separado; no convertir en 102 pruebas únicas ni sumar selecciones anteriores.

Hashes actuales de cinco archivos coinciden con preparación 169, sin prueba retrospectiva de identidad del proceso. Regresión seleccionada aprobada, sin acreditar PostgreSQL/concurrencia o latencia. Próximo paso justificado: un smoke diagnóstico tras liberar y verificar dos redes QA vacías, condicionado a dos eliminaciones sin fallos. Creación 11 → 10 y edición 8 → 7 consultas siguen siendo expectativa en QA, no observación real. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL.


## 22 de octubre de 2026 — Rol agrupado confirmado en PostgreSQL QA

[Evidencia 171](evidencias/171-rol-agrupado-diagnostico-sql-confirmado.json): limpieza previa retiró 42486b8ff1264162_entry y d1c50f8001464425_entry (prefijo plurione-qa-perf-), sin omitidas/fallidas, antes del smoke condicionado. Corrida b2bda80fd89d433c completó **202 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Hashes de los tres servicios coinciden con 169. Creación pasó de 11 a 10 consultas y edición de 8 a 7; listado/detalle mantienen 4/3. SELECT de usuario/área/rol sustituye al SELECT/roles individual en las dos escrituras y ambas fases. Tres pasos por hilo, sin incompletas.

HTTP 100 → 128 → 178 casos; PostgreSQL confirma 178 casos/creaciones auditadas, 68 ediciones, 1780 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido. Regresión 170 de 98 pruebas/cuatro subpruebas conservada.

HTTP p95: listado 366,18; detalle 273,95; creación 760,44; edición 423,13 ms, todos peores que 168 y fuera del umbral. CPU global media 88,72 % frente a 84,20 %, generador 0,76 % del equipo. Ahorro SQL confirmado, sin mejora de latencia demostrada. No atribuir a CPU/código una causa exclusiva: smoke corto, instrumentado, conjunto final y condiciones distintos. RNF-2 pendiente; formal 150 FALLIDA_UMBRAL sigue vigente. No repetir full/smoke sin otra hipótesis o cambio justificado.


## 22 de octubre de 2026 — Listado y detalle con un viaje SQL menos preparados

[Evidencia 172](evidencias/172-lecturas-listado-detalle-agrupadas-preparadas.json): listado agrupa count y página autorizada en una sentencia con LEFT JOIN desde el agregado; conserva total con página vacía/fuera de rango, filtros y orden created_at/id descendente. Detalle/visible_case lee Role.nombre y expediente autorizado en un SELECT; conserva 403 para rol no habilitado y 404 para caso ausente/oculto, sin caché. Los tres roles usan los mismos predicados previos. Autenticación/escrituras/transacciones y DTO/worker no cambian; visible_case compartido mantiene contrato para historial/participantes/correo.

**11 pruebas locales aprobadas en 1,323 s**, con funciones/modelos/Pydantic/SQLite reales. Matriz de 56 actor/caso y listado para siete actores coinciden con predicado anterior. Cubren páginas vacías/fuera de rango, filtros, orden empatado/sin duplicados, 403/404, no SQL al capturar DTO y compilación PostgreSQL. Listado local 3 → 2 consultas y detalle 2 → 1, sin autenticación; se espera QA 4 → 3 y 3 → 2. AST de tres archivos correcto.

Regresión HTTP/API pendiente. SQL más complejo puede tener otro coste de planificación/ejecución; no se acredita latencia por reducir viajes. Sin nueva carga/limpieza o cambios de permisos/commit. Las 98 pruebas/cuatro subpruebas de 170 validan código anterior; RNF-2 pendiente y formal 150 FALLIDA_UMBRAL. No repetir diagnóstico hasta regresión.


## 22 de octubre de 2026 — Lecturas agrupadas: 111 pruebas y 63 subpruebas aprobadas

[Evidencia 173](evidencias/173-lecturas-agrupadas-regresion-111-aprobadas.json): captura de la autora muestra **111 passed, 63 subtests passed in 22.41s**, 100 %, ocho archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye once nuevos casos de agrupación y subpruebas de matriz de permisos/listado, además de regresión seleccionada de incidencias, correo, respuestas/DTO, autenticación y administración. Subpruebas reportadas por separado; no son 174 pruebas únicas ni se suman selecciones anteriores.

Hashes actuales de tres archivos coinciden con 172, sin prueba retrospectiva de identidad del proceso. Regresión seleccionada aprobada; plan/ejecución y latencia PostgreSQL siguen pendientes. Próximo paso: smoke diagnóstico de listado 4 → 3 y detalle 3 → 2, condicionado a liberar/verificar dos redes QA vacías. No full automático ni resultado anticipado de mejora. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL.


## 23 de octubre de 2026 — Lecturas agrupadas confirmadas en PostgreSQL QA

[Evidencia 174](evidencias/174-lecturas-agrupadas-diagnostico-sql-confirmado.json): limpieza previa retiró d1c50f8001464425_net y 791d2288a84d4872_net (prefijo plurione-qa-perf-), sin fallos/omitidas; el bloque verificó el resultado antes de cargar. Corrida 1c455546c34c4d0f completó **203 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Hashes de los dos archivos coinciden con 172. Listado pasó de 4 a 3 consultas y detalle de 3 a 2 en ambas fases; escrituras 10/7 sin cambios. Tres pasos por hilo y cero incompletas.

HTTP 100 → 123 → 173 casos. PostgreSQL confirma 173 casos/creaciones auditadas, 69 ediciones, 1730 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido. Regresión 173 de 111 pruebas/63 subpruebas conservada.

HTTP p95: listado 285,30; detalle 347,96; creación 474,43; edición 371,37 ms. Tres operaciones mejoran frente a 171 y detalle empeora (273,95 → 347,96), sin causa exclusiva demostrada. CPU global media 83,16 %, generador 1,14 %. En detalle, SQL medio baja 61,37 → 52,85 ms, pero endpoint sube 40,52 → 54,40 y ASGI 198,27 → 230,48. La diferencia incluye construcción/compilación, fetch/ORM, validación y planificación; no identifica por sí sola el origen. SQL combinado de rol/caso medio 21,26 ms frente a 36,45 de los dos SELECT anteriores; no sumar p95.

Ahorro de viajes confirmado, sin mejora general o cumplimiento RNF-2. Mantener formal 150 FALLIDA_UMBRAL y todos los reportes. Siguiente revisión: tramo de detalle fuera del cursor antes de más cambios/cargas. No repetir full/smoke automáticamente.


## 23 de octubre de 2026 — Plantilla SQL de detalle sin datos por petición preparada

[Evidencia 175](evidencias/175-detalle-plantilla-sql-parametrizada-preparada.json): perfil local de 174 identificó reconstrucción de predicados/aliases. _visible_case_statement conserva solo una estructura SQL con cuatro bindparams tipados, sin recibir actor/Session/UUID real/rol vigente/resultados. visible_case pasa diccionario nuevo con parámetros actuales y vuelve a consultar Role.nombre y caso autorizado en cada ejecución. Misma SQL/política/403/404 y cantidad de viajes; ninguna caché de permisos o datos. Primera construcción concurrente duplicada es inocua y no comparte parámetros.

Perfil propio SQLite, una muestra fría y treinta calientes por proceso: construcción media caliente 7,53 → 0,005 ms, total 9,01 → 0,52 ms; frío 18,17 → 20,14 ms (una muestra, sin mejora demostrada). No equivale a latencia HTTP/PostgreSQL o RNF-2. **17 pruebas locales aprobadas en 1,371 s**, seis nuevas de ausencia de datos en plantilla, parámetros frescos, confidencialidad/rol cambiantes y dos sesiones/hilos concurrentes sin mezcla de permisos. Once anteriores conservan matriz/orden/total/filtros, conteo SQL y compilación PostgreSQL. AST de dos archivos válido.

Regresión API pendiente; las 111 pruebas/63 subpruebas de 173 validan código anterior. Sin nueva carga/Docker/limpieza, cambios de autenticación, writes/commit, locks, auditoría/colas o DTO. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL conservada. No medir antes de regresión.


## 23 de octubre de 2026 — Plantilla de detalle: 117 pruebas y 63 subpruebas aprobadas

[Evidencia 176](evidencias/176-plantilla-detalle-regresion-117-aprobadas.json): captura de la autora muestra **117 passed, 63 subtests passed in 22.73s**, 100 %, nueve archivos y variables solicitadas (RUN_DB_TESTS=0). Incluye seis casos nuevos de estructura sin datos, parámetros independientes, permisos/rol cambiantes y sesiones concurrentes SQLite, además de la matriz y regresión API seleccionada anterior. Conteos separados; no son 180 pruebas únicas ni se acumulan con selecciones anteriores.

Hashes actuales de dos archivos coinciden con 175, sin prueba retrospectiva de identidad del proceso. Regresión seleccionada aprobada; el microperfil local no demuestra p95 HTTP/PostgreSQL. Corresponde un smoke diagnóstico para contrastar el tramo de endpoint y latencia de detalle, conservando conteos SQL e integridad. Antes, liberar/verificar dos redes QA vacías. No full automático. RNF-2 pendiente y formal 150 FALLIDA_UMBRAL.


## 23 de octubre de 2026 — Plantilla de detalle: mejora localizada, p95 pendiente

[Evidencia 177](evidencias/177-plantilla-detalle-diagnostico-endpoint-reducido.json): limpieza previa retiró 791d2288a84d4872_entry y c7ad7be7ff304f58_net (prefijo plurione-qa-perf-), sin fallos/omitidas, antes de cargar. Corrida fd78431c613f4e14 completó **218 peticiones medidas sin errores**, ocho grupos y sumas concordantes. Hash de incidents.py coincide con 175; diferencias de código declarado registradas. SQL listado/detalle/creación/edición 3/2/10/7 y tres pasos por hilo sin incompletas, como antes.

HTTP 100 → 110 → 164 casos. PostgreSQL confirma 164 casos/creaciones auditadas, 60 ediciones, 1640 entregas, cero SMTP/IA. Comprobaciones posteriores OK, diez logout 204 y QA detenido. Regresión 176 de 117 pruebas/63 subpruebas conservada.

Detalle: endpoint medio 54,40 → 25,98 ms, ASGI medio 230,48 → 209,92 y mediana HTTP 186,72 → 148,69. Mejora localizada compatible con retirar construcción repetida; p95 HTTP empeora 347,96 → 360,31 ms. HTTP p95 listado/detalle/creación/edición actual 588,84/360,31/479,34/313,43 ms: solo edición mejora frente a 174. CPU global media 80,43 %, generador 0,99 %. Espera media de hilos de detalle 61,42 ms y residual ASGI 126,52; cierre medio 50,72 ms incluye trabajo posterior al envío y no equivale a latencia cliente. No sumar p95 ni atribuir causa única.

El ahorro de trabajo local aparece en endpoint, sin mejora general o cumplimiento RNF-2. Formal 150 FALLIDA_UMBRAL y todos los reportes se conservan. No repetir full/smoke sin otra hipótesis o cambio justificado.


## 27 de octubre de 2026 — Formal condicionada preparada; CPU previa alta

[Evidencia 178](evidencias/178-formal-condicionada-preparada-cpu-previa-alta.json): quince archivos cubiertos por regresiones y 53 de la identidad QA 177 coinciden sin diferencias. Aplicación sin cambios desde 175; no se implementó otra refactorización de autenticación tras la interrupción. Sondeo real de solo lectura del agente, sin carga generada: tres intervalos válidos 67,63/91,62/51,56 %, media ponderada **70,29 %**. No identifica responsable ni condiciones de corridas anteriores.

Nuevo run_performance_full_guarded.py: requiere confirmación QA, mide CPU antes de comandos Docker; solo sigue con tres muestras válidas, media <=30 % e intervalos <=50 %. Son umbrales operativos de arranque, no RNF-2 ni garantía de carga constante. Si no cumple, NO_INICIADA_CPU_PREVIA sin Docker/redes. Si cumple, verifica Docker local y libera hasta dos redes QA vacías; exige dos eliminadas sin fallos/omitidas. Después llama full una vez, sin diagnóstico API, manteniendo protocolo 30+300 s, diez clientes y p95<200 ms. precondiciones_arranque conserva línea base/umbrales/redes en el reporte original, sin reescribir anteriores.

**74 unitarias locales aprobadas en 1,839 s**, diez nuevas; CPU/Docker simulados. AST de cuatro archivos correcto. El nuevo comando completo no se ejecutó en Docker real; con la línea base observada no corresponde iniciar carga ahora. No se ejecutó séptima formal o smoke, no hay p95 nuevo; RNF-2 pendiente y formal 150 FALLIDA_UMBRAL conservada. Las 117 pruebas/63 subpruebas de 176 siguen siendo la última regresión de aplicación.


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

## 2026-10-29 — Revisión de auditoría 23-oct

[Respuesta verificable](AUDITORIA_2026-10-23.md) y [evidencia201](evidencias/201-respuesta-auditoria-cierre-correo.json): README de arranque en cinco pasos y cuentas DEMO locales; UTF-8 comprobado; RF-5 amplía creación/asignación/resolución/reapertura con aviso de **cierre**, migración0008 y permisos/deduplicación/ciclo vigente. Ocho nuevas pruebas de servicios/SQLite+DDL offline,27casos de regresión de outbox,102herramientas y4React aprobados; buildVite correcto. No atribuir esos resultados a PostgreSQL/Mailpit nuevo. Historial local conservado y copia de publicación preparada; confirmar push/Actions y recorrido nuevo de cierre antes de declararlo aceptado. RNF-2 sigue pendiente con siete formales fuera de umbral. No se requiere resolver RNF-2 para entregar estas correcciones.

## 2026-10-29 — Publicación y CI confirmados

La rama pública main recibió el commit [1794299](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/commit/179429934fb632e1874bd0dcd67ae00747e0f4ff), confirmado por GitHub y git ls-remote. Su árbol a0bf144c395d8795621e8db87ef2eead29c6c587 coincide con la instantánea revisada de495archivos. Se publicó mediante la conexión GitHub autorizada porque el gestor Git local no proporcionó autenticación. Se conserva el historial local original en bundle; no se sobrescribió historial remoto ni se publicó el cambio ajeno de REVISION.md o .env/.pgdata.

**GitHub Actions aprobado:** [Backend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40946040298), trabajos tests y postgres-integration SUCCESS; [Frontend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40946040141) SUCCESS. PostgreSQL ejecutó upgrade head dos veces, alembic check y pytest con RUN_DB_TESTS=1. Son resultados remotos sobre1794299, no se atribuyen a Docker local. Generación local del contrato OpenAPI3.1.0:25rutas y descripción «Gestión» correcta, sin base de datos o servidor HTTP; no captura visual de Swagger.

[Registro202](evidencias/202-publicacion-auditoria-ci-aprobada.json). Se corrigen además dos instrucciones obsoletas de DEMO: exigir migraciones vigentes y crear casos desde el panel, pues seed no crea incidencias. Pendiente instalar esta versión en Docker local mediante ACTUALIZAR_CORREO.ps1 y capturar cierre en Mailpit. RNF-2 continúa pendiente; CI y correo no lo acreditan.

## 2026-10-29 — Verificación local posterior a actualización

[Evidencia203](evidencias/203-actualizacion-local-servicios-y-mailpit.json): API /health y /health/db HTTP200; Mailpit /livez HTTP200. OpenAPI0.12.0 describe «Gestión» correctamente y expone seguimiento mail. Docker API npipe sigue denegada al agente; no se afirma lectura directa de alembic current o contenedores. Panel5173 inicialmente rechazaba conexión: se inició npm run dev -- --host127.0.0.1 y se observó login en navegador integrado. Vite usa su caché local, sin cambio de código.

Mailpit muestra un mensaje mínimo de caso ficticio; el asunto genérico no demuestra tipo CIERRE. Sin sesión RH no se accedió al seguimiento autenticado ni se modificaron expedientes. Se pidió iniciar sesión en el panel, sin compartir contraseña en chat. Verificación funcional de cierre continúa pendiente; no confundir disponibilidad con aceptación. RNF-2 pendiente y sin otra carga. Registro local hasta completar el recorrido autenticado; publicación previa y CI202 conservados.

## 2026-10-29 — Correo de cierre verificado en el entorno local

[Evidencia204](evidencias/204-correo-cierre-recorrido-local-verificado.json) y [captura206](evidencias/206-correo-cierre-mailpit.jpg). La usuaria inició sesión RH en el navegador integrado; el agente creó únicamente el nuevo caso ficticio «Auditoría RF-5 — cierre ficticio 29-oct-2026», ámbito ENTORNO, sin afectado/participantes/confidencialidad. Clasificación manual de QA Riesgos/Media, revisión con responsable Administrador RH, resolución explícitamente ficticia y cierre. No se solicitó IA. El historial mostró creación, clasificación y tres cambios de estado; no se tocaron casos previos.

El panel mostró estado Cerrada y seis avisos Aceptada por SMTP, cada uno al primer intento: tres creaciones a RH, una asignación, una resolución al reportante y un cierre al mismo reportante (sin afectado en ENTORNO). Mailpit conserva seis mensajes del ID de prueba: tres a las17:09 y tres sucesivos a las17:10. El último muestra solo ID/enlace autorizado, sin título, descripción o resolución. Captura íntegra JPEG guardada e inspeccionada visualmente, hash en204. La atribución de tipo CIERRE proviene del panel; el asunto genérico de Mailpit por sí solo no distingue evento.

La primera captura del panel no pudo guardarse por EPERM y luego hubo interrupciones/pérdida de pestaña. No se inventó ni recreó esa imagen; se conserva observación directa del árbol accesible de la sesión y captura posterior auténtica de Mailpit. No hubo inspección SQL operativa ni prueba nueva negativa de permisos/reapertura/reintentos; esas coberturas automatizadas y límites siguen vigentes. SMTP capturado no demuestra buzón externo/lectura. RF-5 tiene ahora recorrido local básico de creación, asignación, resolución y cierre. RNF-2 continúa pendiente, sin nueva carga. No se cambió código en esta verificación.

## 2026-10-29 — Control SELECT1 real; estadísticas de consultas de negocio preparadas

[Evidencia207](evidencias/207-control-select1-postgresql-real-rnf2-pendiente.json), runee6fcc5a7e8c411e (UTC30-oct/local29-oct): arranque18,51s; diagnóstico5 válido y control DB completo. **286 solicitudes medidas, cero errores HTTP**, conteos100->130->201; SQL201casos/creaciones,96ediciones y2.010entregas, cero SMTP/IA. Diez logout204, postHTTP OK y QA detenido. Reporte original intacto por hash;54hashes de producto coinciden. SQL3/2/9/7, workers3/3/2/2 y cero incompletas conservados.

P95 HTTP ms: listado231,82; detalle207,12; creación363,92; edición289,96: ninguno bajo200. CPUhost74,54%, generador0,84%. Workers creación23,51msCPU frente184,33mstranscurridos; edición14,95CPU/137,03ms. Control después de HTTP: con1conexión5muestras, driver4,370ms/ejecución servidor0,507ms medios; con10conexiones50muestras, driver4,952ms/CPUworker0,665ms, planificación0,02052ms/ejecución0,01944ms medios. P95 driver concurrente8,686ms. No mide consultas reales bajo carga, no restar p95 ni atribuir diferencia a red/IO/GIL/SO/VM únicos. Tampoco permite afirmar que PostgreSQL explique o no explique el coste de negocio. No octava formal; RNF-2 pendiente.

[Evidencia208](evidencias/208-estadisticas-sql-servidor-qa-preparadas.json): opción --server-stats solo smoke diagnóstico, protegida antes de crear recursos. Añade pg_stat_statements/compute_query_id únicamente al PostgreSQL QA nuevo, crea extensión con guard de identidad y toma snapshots sin reset. Deltas por consulta se agregan a familias: llamadas, ejecución/filas y media ponderada; no SQL, parámetros o IDs de consulta en reporte. Detecta reset global/individual por stats_since, desalojo y disminución de contadores. Ventana incluye login/logout, calentamiento, carga y verificación SQL, excluye seed y sondeo SELECT1 posterior. La extensión mantiene textos en su QA privado y añade coste; planning tracking off, sin p95 servidor. No cambia el sitio, Compose operativo, pool, durabilidad ni criterio formal.

**113 unitarias stdlib aprobadas en2,441s**, once nuevas:9helper y2provisionador. Incluyen guard, privacidad, deltas/ponderación, reset/evicción/contadores, configuración solo opt-in, orden alrededor de HTTP/control y parada conservando HTTP/SQL ante fallo posterior. AST4archivos correcto; --plan confirmado sin Docker. Lectores actuales revalidan el reporte real207. No ejecución PG real de208 ni optimización de producto nueva; pendiente un único smoke opcional de estadísticas. No repetir formal sin evidencia/hipótesis nueva.

## 2026-10-29 — CI de herramientas SQL aprobado, perfil real pendiente

[Evidencia209](evidencias/209-ci-control-sql-servidor-aprobado.json): [GitHub Actions Backend](https://github.com/habril768-gif/G19X-ITSM-GASH-918-ACADEMIC/actions/runs/40990308380) sobre3f07628 terminó con tests y postgres-integration SUCCESS. Complementa las113unitarias locales de208. La integración PostgreSQL usa configuración normal del workflow; no ejecuta --server-stats ni demuestra todavía el preload/CREATE EXTENSION/snapshots reales del modo nuevo. Pendiente un único diagnóstico QA con esa opción; no otro full ni carga generada por el agente. RNF-2 sigue pendiente.

## 2026-10-30 — SQL real breve; comparación de capacidad API preparada

[Evidencia210](evidencias/210-sql-servidor-real-breve-latencia-http-pendiente.json), run 3ea817bdffc847fc ejecutado el 29-oct a las 20:23 local (30-oct UTC): arranque de 18,08 s; **269 solicitudes medidas sin errores**, conteos100->130->198. SQL198casos/creaciones,88ediciones y1.980entregas, cero SMTP/IA; post HTTP correcto, diez logout 204 y QA detenido. Diagnóstico 5/sumas de servidor y 54 hashes de producto coincidentes validados; reporte original intacto por hash. P95 listado286,24/detalle233,77/creación340,60/edición303,63ms, todos sobre 200. CPUhost76,06 %, generador 0,84 %. SQL 3/2/9/7 y workers 3/3/2/2.

El nuevo control funcionó realmente:28 familias, 4.160 llamadas y 521,964 ms de ejecución acumulada en su ventana amplia, no solo 5 s HTTP. Cada media por familia menor de 1 ms: autenticación 0,066 ms, advisory 0,0098 ms, INSERT incidencias 0,903 ms e INSERT mail 0,963 ms. La API observa aproximadamente12-29ms por familia SQL durante medición. No restar métricas/ventanas distintas: pg_stat_statements no mide planificación ni todo coste de confirmación, transporte o planificación de CPU. No afirmar causa única GIL/red/VM ni eliminar protección/locks/durabilidad. El resultado orienta a probar capacidad de procesos API; no acredita RNF-2 ni añade formal.

[Evidencia211](evidencias/211-comparacion-uno-dos-procesos-api-preparada.json): --api-workers 2 únicamente en smoke sin diagnóstico. validate_workers rechaza tipo/cuenta/mode inseguros antes de recursos. specification/validate_resolved habilitan comando exacto Uvicorn app.main:app --workers 2 con marcador propio; run comprueba Config.Cmd real del contenedor API y pertenencia de ID antes de migrar, y registra api_workers_declarados/comando_api_workers_verificado. Uno por defecto, Dockerfile/Compose del sitio, código productivo y modo formal permanecen sin cambios. No se mezclan logs de diagnóstico multiproceso ni se afirma reparto por PID.

compare_performance_workers.ps1 exige confirmación QA, ejecuta secuencia 1/2 sin reintentos, cada vez libera dos redes QA elegibles vacías (máximo 4 en total) y crea QA independiente con 10 clientes/100 casos iniciales, smoke de 2 + 5 s sin instrumentos. Si limpieza falla/omite o una prueba queda incompleta, detiene la secuencia. No detiene el sitio ni borra volúmenes/reportes. El pool sigue en 15 por proceso: dos duplican techo teórico API a 30, con más memoria; pendiente medir. Carga de ciclo cerrado puede producir distintos totales/dataset final; una pareja y diferente CPU no prueban causalidad.

**120 unitarias locales aprobadas en 3,309 s**, siete nuevas:5 de configuración/CLI/guardas y 2 del provisionador simulado, incluyendo comando real y parada ante fallo. AST de 3 archivos Python correcto y parser PowerShell sin errores; controlador no ejecutado. Estas pruebas se observaron durante la preparación; no son dos corridas Docker. Pendiente ejecución real y comparación de ambos reportes; no promoción a formal o cambio operativo anticipado.


### 2026-10-30 — Comparación API real, RNF-2 pendiente

[Evidencia212](evidencias/212-comparacion-real-uno-dos-procesos-api.json): smoke1/2 completado y coherente; p95 de dos procesos90,79/114,17/163,91/153,28ms frente252,57/202,21/290,63/249,18ms. Cero errores,339→583 solicitudes. Resultado breve favorable, sin nueva formal ni cambio operativo. Pendiente validar de forma sostenida y reproducible; conservar diez clientes, p95<200ms, locks y auditoría.


### 2026-10-30 — RNF-2: formal QA de dos procesos preparada

[Evidencia213](evidencias/213-formal-qa-dos-procesos-preparada.json): opcion explicita `--api-workers 2` en run_performance_full_guarded.py; conserva protocolo10clientes/30+300s/p95<200ms, guardas CPU/redes e integridad.126 unitarias aprobadas; ejecución formal real pendiente. Ver comando y límites en [prueba de rendimiento](PRUEBA_RENDIMIENTO.md). La restricción histórica de dos procesos solo smoke se amplía a full sin diagnóstico; sitio sin cambios.


### 2026-10-30 — RNF-2 pendiente tras octava formal

[Evidencia214](evidencias/214-formal-dos-procesos-fallo-escrituras.json):27.722 solicitudes sin errores con2procesos; listado/detalle160,12/156,67ms cumplen, creación/actualización264,38/227,96ms incumplen. Integridad y parada correctas. [Candidato215](evidencias/215-formal-tres-procesos-candidato.json): `--api-workers 3` en QA formal con mismo protocolo,130 pruebas aprobadas, todavía sin medición real. Más memoria/conexiones y posible competencia CPU; no cambia sitio ni umbral. Ver [prueba de rendimiento](PRUEBA_RENDIMIENTO.md).


### 2026-10-30 — RNF-2: solo creación pendiente en novena formal

[Evidencia216](evidencias/216-formal-tres-procesos-fallo-creacion.json):QA3,34.027 solicitudes sin errores; p95lecturas125,63/119,11 yactualización173,60ms cumplen; creación202,6812ms incumple. Integridad y parada correctas; RNF-2 pendiente. [Cambio217](evidencias/217-outbox-evento-nuevo-sin-lectura-redundante.json): evita una búsqueda outbox solo para evento pendiente sin identidad, preserva deduplicación de replay y atomicidad;30unitarias aprobadas. Pendiente CI y formal con mismo protocolo3procesos/10clientes/30+300s/p95<200ms.


### 2026-10-30 — RNF-2 pendiente tras décima formal

[Evidencia218](evidencias/218-decima-formal-fallida-cuatro-operaciones.json):24.450 solicitudes sin errores, QA3; p95 listado209,73/detalle200,83/creación328,30/edición289,47ms incumplen. Integridad y parada correctas, outbox217 presente; sin causalidad aislada. [219](evidencias/219-cpu-pasiva-por-fase-formal.json) añade CPU Windows/generador al inicio/fin de cada fase normal/formal, sin perfil API ni cambiar protocolo/veredicto;132 pruebas aprobadas. Pendiente CI y nueva medición; no más procesos ni cambios de negocio a ciegas.


## Continuación de la entrega: matriz por roles

La [matriz de aceptación](ACEPTACION_ENTREGA.md) reúne14escenarios con origen/alcance de evidencia y pendientes. [Preparación222](evidencias/222-matriz-aceptacion-entrega-preparada.json): siguiente recorrido de departamentos conAdminRH,8pasos previstos y ninguna escritura ejecutada. RNF-2 aprobado220 se conserva; un plan no es aceptación real. Ver comandos de arranque con3procesos/Mailpit y registro de resultados en la matriz.


## Departamentos: aceptación Admin RH observada

[223](evidencias/223-departamentos-admin-rh-recorrido-ui.json): D01–D08 conforme en panel integrado; alta ficticia, duplicado rechazado, renombrado, baja/reactivación y baja final; cinco eventos con motivos y persistencia tras actualizar. Estado final inactivo, sin borrar datos ni tocar departamentos usados. [224: historial](evidencias/224-departamentos-admin-rh-historial-final.jpg),[225: duplicado](evidencias/225-departamento-duplicado-rechazado.jpg). A02 verificado; A03 parcial y A04 pendiente según [matriz](ACEPTACION_ENTREGA.md). No implica aceptación integral ni institucional.


## 2026-10-31 — Visibilidad de administración por rol confirmada por la autora

[Evidencia226](evidencias/226-visibilidad-administracion-supervisor-empleado-confirmada.json): la usuaria informa que RH Independiente Demo ve Usuarios y Departamentos, Supervisor RH no muestra esas opciones y Empleado tampoco. Confirmación textual de visibilidad, sin observación directa/capturas nuevas del agente ni comprobación API en este recorrido. A04 avanza solo en su parte visual; rechazo de rutas API con sesiones reales sigue sin verificarse aquí. No repetir pruebas ya aprobadas ni crear cuentas para este registro. RNF-2 y recorrido223 se conservan. Registro local, sin publicación remota en este avance para reducir llamadas y consumo.


### 2026-10-31 — Usuarios: confirmación de recorrido ficticio

[227](evidencias/227-usuario-ficticio-alta-edicion-baja-confirmadas.json): autora confirma alta/listado, nombre revisado, estado Inactiva y acceso rechazado con aviso genérico. A05 parcial: sin comprobación independiente, auditoría o revocación de sesión previa; no atribuir el rechazo solo a la baja sin verificar credenciales previamente. Registro local, sin repetir pruebas ni publicación remota.


### 2026-10-31 — Revocación de sesión al desactivar usuario ficticio

[Evidencia 228](evidencias/228-revocacion-sesion-usuario-confirmada.json): la usuaria confirma inicio de sesión exitoso con `qa-entrega-20261031-01@example.invalid` y, tras el procedimiento guiado de desactivación desde Admin RH y nueva solicitud desde la sesión abierta, pérdida de acceso con el mensaje «Tu sesión terminó o cambió el acceso de tu cuenta. Inicia sesión nuevamente.» Resultado esperado confirmado por la usuaria; sin observación directa del agente ni inspección HTTP/SQL. Esta comprobación amplía la evidencia 227, cuyos límites originales se conservan.

Propósito: verificar invalidación de sesión existente al desactivar una cuenta. Archivos: evidencia 228 y seguimiento documental de aceptación, QA, bitácora, backlog, entregables y trazabilidad. Validación: registro JSON leído de nuevo y referencia de matriz comprobada. A05 continúa parcial para auditoría y conservación del historial; no se declaran esos puntos probados. Sin cambios de código, repetición de RNF-2 ni publicación remota; registro local agrupado.


### 2026-10-31 — Usuarios: conflicto por correo y motivo obligatorio

[Evidencia 229](evidencias/229-usuarios-duplicado-motivo-confirmados.json): la usuaria confirma rechazo al intentar repetir el correo ficticio existente y bloqueo del formulario al omitir el motivo administrativo. Propósito: ampliar aceptación A05. Validación manual guiada y reportada por la usuaria; JSON y enlaces locales comprobados. Sin inspección HTTP/SQL: el aviso genérico no acredita por sí solo atomicidad y la validación del formulario no sustituye pruebas directas de API. A05 sigue parcial para auditoría y conservación de historial. Evidencia 228 conserva la revocación confirmada. Sin cambios de código ni publicación remota; RNF-2 aprobado se mantiene.


### 2026-10-31 — Consolidación de recuperación Docker y controles de departamentos

Propósito: integrar los resultados manuales aportados por la usuaria, sin repetir pruebas ni modificar código. [230](evidencias/230-restauracion-docker-confirmada.json): respaldo `plurione-20261031-092101.dump`, 75624 bytes, SHA256 `A21826DB6F16EBEA761D83B0DB1BD27D89A801E54CAAB5568AC1A0BB0F0F13B0`; pg_restore sin errores reportados, revisión 0008, cantidades y huellas de contenido de todas las tablas public coincidentes. Destino `plurione-restore-c368a6c78bd8` sin red/puertos según comando, luego detenido; origen reanudado y acceso Admin RH confirmado. La salida ps aún mostraba API health: starting; no declarar healthy posterior del API/worker. No se compararon independientemente secuencias, restricciones, índices, vistas, ACL ni roles globales; no es recuperación completa de instalación ni medición de RTO/RPO.

[231](evidencias/231-departamento-motivo-obligatorio-confirmado.json): la usuaria confirma bloqueo del formulario al omitir motivo. [232](evidencias/232-departamento-bloqueo-usuario-activo-confirmado.json): tras reactivar el departamento ficticio y vincular la cuenta ficticia activa, la baja se rechaza con aviso genérico; después confirma que se guardan las bajas de cuenta y departamento. Ambos quedan inactivos según reporte. Bloqueo por incidencias abiertas sigue pendiente por separado. No inferir respuesta HTTP, auditoría, atomicidad SQL ni validación API a partir del formulario o aviso genérico.

Archivos: evidencias 230–232, matriz de aceptación, mantenimiento, QA, bitácora, backlog, entregables, trazabilidad y MVP. Validación documental: JSON reabiertos, enlaces locales comprobados y matriz contrastada con las confirmaciones. Registros 228/229 conservan revocación, correo duplicado y motivo de usuarios; A05 sigue parcial por auditoría/historial. Sin nuevas pruebas de código, publicación remota ni cambios al cumplimiento de RNF-2. Pendientes: A03 incidencias abiertas, negativos por roles, auditoría de usuarios, recuperación integral, custodia y aceptación humana conforme a la matriz.


### 2026-10-31 — Baja de departamento con incidencia pendiente

[Evidencia 233](evidencias/233-departamento-incidencia-pendiente-confirmado.json): tras la preparación guiada, la usuaria reporta incidencia ficticia `710482ca-a652-4679-9abf-13c3b3553e10` Pendiente y rechazo de baja del departamento con aviso genérico; confirma expresamente que la cuenta ficticia está inactiva. Resultado esperado del recorrido confirmado por reporte, coherente con bloqueo por incidencia abierta. No se inspeccionaron otras cuentas vinculadas, departamento histórico, HTTP/SQL ni causa exclusiva. Conservar incidencia Pendiente y departamento operativo; no borrar ni cerrar para completar evidencias.

Propósito: completar el supuesto manual pendiente de A03. Archivos: evidencia 233, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: lectura JSON y referencia en matriz comprobadas. A03 reúne ahora duplicado observado en223 y motivo/bloqueos reportados en231–233, con sus límites; no equivale a comprobación independiente de todas las precondiciones o aceptación institucional. No hay cambios de código, pruebas automáticas nuevas ni publicación remota. Persisten pendientes de otros escenarios de la matriz.


### 2026-10-31 — Salud confirmada tras reanudar Docker

[Evidencia 234](evidencias/234-salud-posterior-reanudacion-docker.json): salida aportada por la usuaria confirma API, PostgreSQL, Redis y Mailpit healthy; worker de correo Up sin estado de salud reportado. GET /health/db devuelve status ok y database postgresql. Completa la comprobación de salud posterior que seguía pendiente en230; acceso Admin RH ya confirmado. No prueba entrega de correo ni recuperación integral de instalación, roles/ACL o secuencias. Archivos: evidencia234 y seguimiento de aceptación, mantenimiento, QA, bitácora, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces locales comprobados. Sin cambios de código, pruebas automáticas nuevas o publicación remota.


### 2026-10-31 — Responsabilidad y ubicación del respaldo declaradas

[Evidencia 235](evidencias/235-custodia-respaldo-confirmada.json): la autora declara que será responsable del respaldo y que lo conservará en RespaldosPluriOne de su computadora. Se referencia el archivo y hash registrados en230, sin publicar ruta privada ni identidad personal. Propósito: registrar una decisión real de custodia, no una asignación inferida. Archivos: evidencia235, mantenimiento, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlace comprobados. Pendientes: plazo o condición de conservación, acceso restringido no inspeccionado y disposición posterior; no se declara copia adicional o entrega a terceros. A13 continúa parcial y no se extiende esta declaración a exportaciones analíticas. Sin cambios de código, pruebas nuevas ni publicación remota.


### 2026-10-31 — Condición de conservación del respaldo acordada

[Evidencia 236](evidencias/236-conservacion-respaldo-acordada.json): la usuaria acepta conservar el respaldo hasta concluir la evaluación y atender las observaciones finales. Se mantienen responsable y ubicación declarados en235. Propósito: completar condición real de retención del respaldo académico. Archivos: evidencia236, mantenimiento, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación: JSON y referencia comprobados. Sin fecha de vencimiento inventada, eliminación automática, publicación remota o nuevas pruebas. Pendientes: disposición posterior y controles de custodia no inspeccionados; analítica conserva sus decisiones independientes.


### 2026-10-31 — Revisión de frases desactualizadas del README

Propósito: atender la observación de auditoría sobre frontend pendiente y ausencia de configuración de claves. Búsqueda literal en README, backend/README, FRONTEND, MANUAL_TECNICO y ENTREGABLES: ambas frases observadas ya estaban ausentes. Se conserva el historial de bitácora como registro fechado. Se encontró y corrigió una contradicción vigente en el resumen de README: RNF-2 ya está aprobado en alcance QA local (220), y restauración lógica/reanudación Docker cuentan con230/234; recuperación integral, aceptación y capacitación siguen pendientes. Se explicitan POSTGRES_PASSWORD, contraseña privada Admin RH, OPENAI_API_KEY para IA opcional y configuración SMTP externa cuando aplique. Archivos: README y seguimiento en bitácora, backlog, entregables y trazabilidad. Validación: textos actuales contrastados con .env.example y evidencias; enlaces locales y ausencia de las frases originales comprobados. Cambio documental: sin nuevas pruebas funcionales ni credenciales publicadas.


### 2026-10-31 — Conservación de expediente tras baja de cuenta

[Evidencia 238](evidencias/238-expediente-conservado-tras-baja-usuario.json): ante la solicitud de comprobar título, descripción, estado Pendiente y evento CREADO del caso ficticio 710482ca-a652-4679-9abf-13c3b3553e10 como Admin RH, manteniendo la cuenta ficticia inactiva, la usuaria confirma globalmente «todo sigue bien». Se registra como confirmación textual guiada, sin observación directa ni verificación independiente por campo/HTTP/SQL. Propósito: comprobar conservación de ese expediente después de la baja; no acredita auditoría administrativa de usuarios ni todos los supuestos de permisos. Archivos: evidencia238, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y referencia comprobados. Sin cambios de código, nuevas pruebas automáticas, modificación indicada del caso ni publicación remota. A05 conserva pendiente auditoría administrativa; alcance de conservación acotado a este caso.


### 2026-10-31 — Auditoría administrativa del usuario ficticio consultada

[Evidencia 239](evidencias/239-auditoria-usuario-ficticio-consulta-lectura.json): salida aportada por la usuaria de consulta READ ONLY muestra11 eventos USUARIO_ACTUALIZADO de la cuenta ficticia, nueve cambios de activación con bandera sessions_revoked=true y motivos; renombrado con true→true y bandera false; evento más antiguo sin los campos proyectados. El código ALTA_LOCAL no guarda esos campos, lo cual es compatible, pero operacion no fue seleccionada y no se confirma esa identidad. La bandera no cuenta sesiones ni reemplaza la comprobación funcional228. Propósito: verificar registro administrativo del recorrido A05. Archivos: evidencia239, matriz, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y referencia comprobados; contraste con api/auth.py y services/users.py. A05 reúne alta/edición/baja reportadas, revocación228, negativos229, expediente238 y consulta239 en su alcance acotado; no aceptación integral de cambios de rol/departamento, concurrencia o todos los expedientes. Sin cambios de código, nueva pantalla, nuevas pruebas automáticas o publicación remota.


### 2026-10-31 — Resumen verificable de entrega

Propósito: facilitar revisión académica sin repetir pruebas o presentar aceptación no realizada. Creado RESUMEN_ENTREGA.md con resultados, procedencia, pendientes y guion de demostración; enlazado desde índice documental. Corregidas dos notas vigentes del índice sobre RNF-2 pendiente/resultados pendientes frente a la aprobación posterior220. Archivos: resumen, índice, bitácora, backlog, entregables y trazabilidad. Validación: enlaces relativos del resumen comprobados; sin nuevos tests funcionales por cambio documental. Evidencias238/239 y resumen siguen locales; última publicación comprobada9e1d77a. No se inventan capacitación, aprobación institucional, fecha de entrega o porcentaje medido.


### 2026-10-31 — Rechazos administrativos de lectura con dos sesiones reales

[Evidencia240](evidencias/240-rechazos-api-supervisor-empleado-confirmados.json): la usuaria aporta ejecución del auxiliar local para Supervisor RH y Empleado Operaciones2. Rol comprobado mediante /auth/me; GET /users, /users/options y /departments devuelve403 en ambas sesiones; logout204 en ambas. Propósito: complementar controles ocultos226 con denegaciones HTTP reales. Alcance: seis rechazos de lectura y dos cierres de sesión reportados; no se ejecutan escrituras ni historial de departamentos. Tres comprobaciones simuladas previas del auxiliar validaron manejo de403, rol incorrecto y200 inesperado, sin llamadas reales del agente. Archivos: evidencia240, aceptación, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. No se recopilan contraseñas ni tokens. A04 tiene lecturas verificadas por salida de la usuaria; escritura/historial en sesión real permanecen fuera del recorrido, con sus pruebas automatizadas separadas. Registro local, sin publicación en este avance ni cambios de producto.


### 2026-10-31 — Restricciones administrativas ampliadas en sesiones reales

[Evidencia241](evidencias/241-rechazos-administrativos-ampliados.json): Supervisor RH y Empleado Operaciones2, roles comprobados por /auth/me, aportan ocho403 cada uno: lecturas users/opciones/departamentos/historial y POST/PUT de usuarios/departamentos. Dos cierres204. Escrituras con cuerpo vacío y PUT a UUID nulo: se confirma rechazo de esos intentos, no la matriz completa con cuerpos válidos y registros existentes. Auxiliar local con sintaxis y cuatro escenarios simulados comprobados; sin código de producto nuevo ni credenciales registradas. Propósito: ampliar A04 sin generar altas/ediciones válidas. Archivos: evidencia241, aceptación, resumen, QA, bitácora, backlog, entregables y trazabilidad. Validación documental: JSON y referencias comprobados. Se mantienen límites de confidencialidad, concurrencia y aceptación institucional. Registro local, sin publicación remota en este avance.


### 2026-10-31 — Expediente ficticio no disponible para otro Empleado

[Evidencia242](evidencias/242-empleado-expediente-ajeno-404.json): salida aportada por la usuaria con rol EMPLEADO verificado para Empleado Operaciones2: GET detalle, historial y participantes de710482ca-a652-4679-9abf-13c3b3553e10 devuelve404; logout204. Existencia/conservación accesible previamente como Admin RH reportada en238, sin comprobación simultánea nueva. Propósito: ampliar A07 con tres respuestas HTTP reales de no disponibilidad, sin mostrar contenido. Un404 aislado no distingue inexistencia/denegación; no se infieren todos los casos de confidencialidad, relaciones, listados o escrituras. Auxiliar local con sintaxis y tres escenarios simulados verificados; sin nuevas llamadas reales del agente. Archivos: evidencia242, matriz, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. Sin cambios de código de producto o publicación remota en este avance.


### 2026-10-31 — Control positivo Admin RH del expediente ficticio

[Evidencia243](evidencias/243-control-admin-expediente-200.json): rol ADMIN_RH comprobado, detalle/historial/participantes del caso710482ca-a652-4679-9abf-13c3b3553e10 responden200; cierre204, según salida aportada por usuaria. Contrasta con los tres404 de Empleado en242 mediante sesiones sucesivas, sin mostrar contenido. Propósito: confirmar disponibilidad autorizada posterior y reforzar el recorrido A07. No prueba simultaneidad, ausencia de cambios entre sesiones o matriz integral de conflictos/participantes. Correo operativo omitido en nueva evidencia; credenciales/tokens no recogidos. Auxiliar con sintaxis y tres escenarios simulados comprobados. Archivos: evidencia243, aceptación, resumen, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON y enlaces comprobados. Sin código de producto nuevo, mutaciones de negocio solicitadas ni publicación remota en este avance.


### 2026-10-31 — Ensayo de demostración con capturas de estados

[Evidencia244](evidencias/244-ensayo-estados-capturas-autora.json) y capturas245–247 aportadas por la usuaria: evento CREADO visible, cuenta ficticia EMPLEADO Inactiva vinculada al departamento ficticio, departamento Activo. Propósito: conservar prueba visual del ensayo de demostración. ID/estado Pendiente del caso y sesión Admin RH corresponden al contexto reportado, no visibles en los recortes. Capturas no demuestran por sí solas causa de bloqueo, integridad completa ni aceptación institucional. Archivos: JSON244, tres PNG245–247 y seguimiento documental. Validación: firmas PNG, hashes SHA256 y referencias comprobados. Sin modificar datos, nuevas pruebas de aplicación o publicación remota en este avance. Ensayo no equivale a capacitación acreditada.


### 2026-10-31 — Ensayo: aviso genérico capturado en Mailpit

[Evidencia248](evidencias/248-ensayo-mailpit-aviso-generico.json), capturas249/250 de la autora: mensaje del caso ficticio710482ca-a652-4679-9abf-13c3b3553e10 para destinatario ficticio, cuerpo genérico con enlace local y UUID, sin título/descripción/nombres en texto visible. Comprobador de enlaces mostrado sin resultado; no se declara verificado. Propósito: documentar sección de correo de la demostración. Alcance Mailpit local, sin comprobar buzón externo, Raw/MIME completo, todos los destinatarios o reintentos. Archivos: JSON248, PNG249/250 y seguimiento. Validación: firmas PNG, hashes y referencias comprobados. Sin modificar aplicación, generar avisos nuevos o publicación remota en este avance.


### 2026-10-31 — Apertura del expediente desde enlace de correo

[Evidencia251](evidencias/251-enlace-mailpit-expediente-confirmado.json) y captura252: tras indicación de abrir enlace Mailpit, la autora aporta destino con parametro incident y expediente del mismo UUID, título ficticio y estado Pendiente, sesión Administrador RH visible. Propósito: completar ensayo de navegación correo→expediente. No se observó el clic/login intermedio; no se declara ejecutado el comprobador automático de Mailpit ni entrega externa. La leyenda IA pendiente no demuestra llamada o fallo del proveedor. Archivos: JSON251, PNG252 y seguimiento documental. Validación: firma PNG, hash SHA256 y referencia comprobados. Sin cambios de aplicación, nuevos avisos o publicación remota en este avance.


### 2026-10-31 — Power BI principal refrescado y guardado

[Evidencia253](evidencias/253-powerbi-refresco-guardado-20261031.json): tras habilitar PostgreSQL local5433 (healthy según salida), autora confirma nuevo corte31/10/2026 02:47:05p.m.; captura muestra ese corte, guardado Hoy2:49p.m., cuatro filas suprimidas, medidas visibles vacías y leyenda de población parcial/datos simulados. Propósito: actualizar sección analítica del ensayo. Original con nombre personal en cabecera conservado en espacio auxiliar fuera de Git; hash de imagen y PBIX local registrados, binario no publicado automáticamente. No se verificaron credenciales efectivas, DAX/SQL de esta ejecución, números positivos o permisos SQL; las pruebas previas conservan alcance independiente. Archivos: evidencia253, guía Power BI, analítica, resumen, aceptación, bitácora, QA, backlog, entregables y trazabilidad. Validación documental: JSON, hashes y referencias comprobados; sin pruebas funcionales adicionales del agente ni publicación remota en este avance.


### 2026-10-31 — Paquete del código publicado para revisión

Se genera fuera del repositorio ZIP del commit públicobbaad73eea873739a456b0b21e8438610cb392d8, SHA256 `11e96e4d838293d3ca76d76dd3f9e1b68124698f108937983fe2b35bbbed2e96`, 5323995 bytes. Propósito: facilitar entrega revisable con código, informe en borrador y guías publicadas. Comprobación: CRC ZIP, presencia de README/informe y exclusión de .env, .git, dependencias, .pgdata y dumps; sin instalación limpia nueva. Se adjuntan guía y manifiesto fuera de Git. PBIX del ZIP corresponde únicamente a versiones ya publicadas; el principal refrescado localmente y captura con nombre personal no se incorporan. La usuaria decide no implementar correo externo por ahora; Mailpit mantiene el alcance local, sin alterar requisitos institucionales. No acta de entrega o aceptación ni publicación nueva.


### 2026-10-31 — Instalación nueva del núcleo y persistencia tras reinicio

[254](evidencias/254-instalacion-nueva-bloqueada-redes.json) conserva primer intento incompleto por rangos de redes agotados, con imágenes construidas; se liberan dos redes QA antiguas elegibles según salida de autora. [255](evidencias/255-instalacion-nueva-nucleo-reinicio.json): segundo proyecto nuevo, base inicialmente0usuarios/0casos, migración0008/check, backend y frontend npm ci/build, HTTP/proxy ok; bootstrap realCLI,1Admin y creación UI de caso ficticio. Autora confirma conservación tras relogin y después de stop/start. Reporte conserva mismos cuatro contenedores, hash de fila,1evento CREADO,1usuario/1caso y salud API/proxy antes/después; puertos efímeros cambian. Código fuente contrastado con instalación de trabajo sin diferencias en alcance registrado. Propósito: acreditar instalación nueva acotada, no restauración integral o instalación literal NodeWindows del README. Sin IA/correo/BI, pruebas de carga o aceptación institucional. Archivos: evidencias254/255 y seguimiento documental. Validación: JSON, reporte local, comparación de fuentes y coincidencia antes/después; sin acceso independiente del agente al daemon. Cierre de recursos aún pendiente, sin borrado de volúmenes; publicación pendiente.


### 2026-10-31 — Cierre del ensayo de instalación nueva

La autora aporta ENSAYO_DETENIDO_DATOS_CONSERVADOS para plurione-install-da463a2d815a; reporte local registra cuatro IDs detenidos y volumes_deleted=false, después de validación de pertenencia y Running=false por auxiliar. Evidencia255 completada con cierre y hash final de reporte. El panel aislado32771 queda apagado; no se elimina base de prueba. Propósito: finalizar uso de recursos del ensayo tras persistencia comprobada. Archivos: evidencia255 y seguimiento de bitácora, QA, backlog, entregables, trazabilidad, aceptación, mantenimiento y resumen. Validación: JSON y reporte contrastados. No acredita perfiles externos o recuperación integral de instalación previa; no publicación remota en este avance.


### 2026-10-31 — Recuperación de copia con aplicación y permisos BI

[Evidencia256](evidencias/256-recuperacion-copia-app-permisos-bi.json): respaldo identificado de75624bytes restaurado a otra base del proyecto QA; catálogo14tablas/2vistas/2secuencias/15índices no asociados a restricciones/20restricciones PK-UQ/25FK coincide por nombres/tipos,0restricciones sin validar, secuencias last_value/is_called coincidentes,9usuarios/8casos, revisión0008. API/panel contra copia y check Alembic sin diferencias;30sesiones históricas revocadas solo en copia. Autora confirma login Admin RH y consulta de expediente. Tras reinicio inesperado Windows41/6008, contenedores exited255: comprobación posterior conserva recuentos/revisión/secuencias. Causa del reinicio desconocida; no inferir fallo Docker o memoria a partir de esos registros.

Cuenta BI nueva creada por CLI después de un intento rechazado por longitud; siete comprobaciones reales de permisos: dos vistas permitidas, cinco42501 (lectura/UPDATE/DELETE users y CREATE public/analytics), sin atributos privilegiados. default_transaction_read_only desactivado solo en sesión de prueba para verificar ACL; ROLLBACK por prueba. Fuente: salidas/reporte local y confirmaciones de autora, sin daemon independiente del agente. Cuatro contenedores detenidos y volúmenes conservados al cierre.

Propósito: ampliar recuperación lógica230 e instalación nueva255 hacia uso de copia y reconstrucción acotada de permisos BI. No equivalencia literal de todos los propietarios/ACL/globales, definiciones o filas del origen actual; no proveedores externos/BI Desktop, RTO/RPO o aceptación institucional. Archivos: evidencia256, matriz, resumen, informe, mantenimiento, MVP, bitácora, QA, backlog, entregables, trazabilidad y decisiones. Validación: JSON/reporte, hash del respaldo, resultados de siete ACL y cierre contrastados; auxiliares probados offline/simulados según manifiesto. Credenciales, dump y datos individuales no publicados; registro local pendiente de publicación.


### 2026-10-31 — RF-8: bandeja sin responsable

[257](evidencias/257-filtro-sin-responsable-regresion-local.json): faltaba filtro exigido enRF-8. API unassigned=true y selector React de gestores implementados; mismo predicado de visibilidad/filtros en filas y total, conflicto de filtros422, vuelve a página1 y limpiar retira selección. Sin migración o cambio de datos. Ocho nuevos escenarios backend y dos frontend.

Validación local: selección44passed/63subtests/12.74s; suite completa en copia escribible476passed/22skipped/147subtests/47.65s; frontend71tests/10archivos/68.04s; build25módulos correcto. Dos pases generales originales interrumpidos, primero con fallos y sin traza final; no aprobados. No se atribuye causa exclusiva sin traza; repetición completa en copia escribible correcta.22 integraciones PG/analítica omitidas no aprobadas aquí; CI pendiente.

Archivos: API incidents y tests nuevos, App/cliente/pruebas frontend, manual/guía, PRD informativo y seguimiento. Tres notas obsoletas de implementación del PRD actualizadas, sin cambiar reglas. Backend fuente actualizado; frontend operativo anterior hasta coordinar imagen API. Prueba UI real y formal RNF-2 para nuevos hashes pendientes:220 es resultado histórico, no aprobación automática del nuevo código. Sin proveedor externo ni aceptación institucional.


### 2026-10-31 — RF-8 actualizado y filtro/limpieza comprobados en panel

[259](evidencias/259-filtro-sin-responsable-ui-verificado.json), capturas260/261: actualización coordinada confirma API/health/db y proxy ok, OpenAPI con unassigned y frontend aplicado después; usuaria muestra filtro Sin responsable con1resultado y, tras limpiar, Responsable Todos/8resultados. Menús RH visibles, identidad no incluida en recortes; contexto según procedimiento de autora. No se infiere total global ni detalle de asignación no capturado. Propósito: completar recorrido real del filtro de RF-8. Archivos: manifiesto259, dosPNG y seguimiento. Validación: firmas/hashes PNG, reporte de actualización y JSON contrastados; sin repetir tests o alterar casos. CI257/258 conserva alcance; formal RNF-2 de nuevos hashes pendiente. Registro local para publicación agrupada.


### 2026-10-31 — Revalidación RNF-2 de RF-8: umbral no cumplido

Propósito: verificar rendimiento formal de la versión actualizada. [Evidencia 262](evidencias/262-rnf2-version-rf8-fallida-umbral.json), corrida c7a2582aa61c4e33: tres procesos API, diez clientes, cien casos iniciales, 30 s de calentamiento y 300 s de medición completos. Resultado FALLIDA_UMBRAL: 27 646 solicitudes y cero errores HTTP; p95 listado 169,961 ms, detalle 157,902 ms, creación 265,012 ms y actualización 230,765 ms. Creación/actualización exceden el umbral estricto de 200 ms. CPU global media durante medición 93,699 %; no demuestra una causa exclusiva ni atribuye regresión al filtro. SQL: 7714 incidencias/CREADO, 7609 EDITADO, 77140 entregas encoladas, cero intentos SMTP y trabajos IA. Comprobación HTTP posterior OK y diez cierres de sesión 204. Recursos QA detenidos y datos conservados según reporte leído. Archivos: manifiesto 262 y seguimiento documental; sin cambios de producto. Validación: JSON, hash del reporte, código incidents.py, protocolo y métricas contrastados. La aprobación histórica 220 sigue limitada a su versión; esta versión permanece pendiente. Siguiente: diagnóstico breve de escrituras y estadísticas SQL antes de otra formal; no reducir umbral o concurrencia. Publicación agrupada pendiente.


### 2026-10-31 — Diagnóstico de escrituras y estructuras SQL reutilizables

Propósito: reducir trabajo repetido en escrituras tras el fallo formal 262. [Evidencia 263](evidencias/263-diagnostico-sql-y-plantillas-escritura.json), diagnóstico 232a6419420e4b6c: estadísticas SQL OK, un proceso instrumentado, smoke 2+5 s; sin acreditación RNF-2. En servidor INSERT incidencias promedió 0,866 ms y notificaciones 1,189 ms; los tiempos de driver son mayores en otra ventana y no prueban una causa exclusiva. Cambio: services/incidents.py parametriza y reutiliza tres estructuras de acceso por rol; lifecycle.py usa la misma lectura vigente; services/mail.py reutiliza la selección de destinatarios. Solo se cachea estructura SQL, nunca permisos/resultados/Session/UUID de usuario; bloqueos, consultas y transacciones conservados. Cuatro regresiones nuevas en test_write_sql_templates.py comprueban cambios de confidencialidad, conflictos, roles, actividad y parámetros sin identidad ligada. Validación dirigida: 65 passed/11,88 s. General: 473 passed, 7 failed, 22 skipped y 147 subtests/45,47 s; los siete fallos fueron PermissionError al reemplazar archivos temporales en test_ai_run_evaluation.py. Repetición de ese archivo con temporal autorizado: 16 passed/5,73 s. Intentos previos interrumpidos por espera de socketpair en TestClient; red local concedida antes de la dirigida aprobada. No se declara una ejecución general única totalmente verde. Código aplicado localmente tras comparar la base y conservar copia anterior; principal detenido, sin operar Docker ni cambiar datos. Pendientes: ganancia de rendimiento, formal con tres workers y CI/publicación de este candidato. La evidencia 220 es histórica; 262 sigue siendo la última formal de esta línea.


### 2026-10-31 — Formal del candidato de plantillas SQL: no acredita RNF-2

Propósito: medir el candidato 263 con el protocolo formal sin cambios de umbral o carga. [Evidencia 264](evidencias/264-rnf2-plantillas-escritura-fallida.json), corrida 0e2e0230b104444d: tres procesos API, diez clientes, 30 s de calentamiento y 300 s de medición; hashes de los tres servicios contrastados con 263. Resultado FALLIDA_UMBRAL: 23 918 solicitudes sin errores; p95 listado 209,787 ms, detalle 192,622 ms, creación 312,022 ms y actualización 285,435 ms. Solo detalle cumple el límite estricto de 200 ms. CPU media 88,608 %. SQL: 6775 incidencias/CREADO, 6669 EDITADO, 67750 entregas encoladas, cero SMTP y trabajos IA; HTTP posterior OK, diez cierres 204 y QA detenida con datos conservados. Frente a 262 aumentaron los cuatro p95; no hay mejora demostrada ni comparación causal controlada. Archivos: manifiesto264 y seguimiento; sin cambios nuevos de producto o despliegue principal. Validación: lectura de reportes, hashes, protocolo, métricas y detención. Pendiente: comparación controlada antes de otra modificación/formal, CI/publicación y despliegue del candidato. Aprobación220 histórica, sin extenderla a esta versión. No se declara cierre integral ni se reduce el requisito.


### 2026-10-31 — Principal reanudado según salida y comparación ABBA preparada

La usuaria reporta API, worker de correo, Mailpit, PostgreSQL y Redis healthy tras up --no-build --wait. Propósito siguiente: comparación descriptiva de RF-8 antes/con plantillas263, sin repetir todavía otra formal. [Evidencia265](evidencias/265-comparacion-abba-preparada.json): ejecutor auxiliar compare_write_templates_local.py congela copias de backend, sin .env ni dependencias privadas; verifica hashes de tres servicios y usa smoke existente con tres procesos, diez clientes y cien casos nuevos en orden A–B–B–A. Pausa los cinco servicios principales y finalmente intenta reanudarlos con imágenes existentes; conserva recursos y datos de QA. Validación: preparación sin Docker y tres simulaciones aprobadas/0,147 s (ABBA/reanudación, rechazo CPU, interrupción por QA incompleta). Archivos: dos auxiliares locales de comparación/verificación, manifiesto265 y seguimiento; sin cambio adicional de producto. Pendientes: ejecución real, interpretación descriptiva con límites, decisión sobre candidato263 y formal. No se acredita RNF-2 ni se garantiza control de carga externa/temperatura.


### 2026-10-31 — ABBA completado y agrupación de lectura de recibo/destinatarios

Propósito: contrastar candidato263 y reducir un viaje SQL de creación. [266](evidencias/266-comparacion-abba-plantillas-sql.json): cuatro smoke A–B–B–A con tres procesos y diez clientes, cero errores; creación A257–279 ms/B207–239 ms, actualización A223–251 ms/B212–227 ms. Principal reanudado con cinco servicios healthy según usuaria y exitcode0 en reporte. Conservar263 por señal descriptiva favorable en creación, sin acreditar RNF-2 ni significancia/control completo del host. CPU previa de ejecución anterior impidió toda carga; ejecutor auxiliar añadió espera15 s y hasta tres controles, conservando todas las muestras y límites30/50 %; cuatro simulaciones aprobadas/0,155 s, sin prueba real por agente.

[267](evidencias/267-creacion-recibo-destinatarios-consulta-conjunta.json): services/mail.py agrupa destinatarios y EXISTS del predicado vigente de recibo; services/incidents.py consume el permiso retornado, eliminando su consulta separada. LEFT JOIN de fila única conserva resultado con cero destinatarios. No se cachean decisiones ni se cambian autorización, bloqueo, auditoría o transacción. Test nuevo cubre tres roles, dos ámbitos, confidencialidad, conflicto de gestor y cero destinatarios; conteos previos ajustados por una consulta menos. Validación dirigida81 passed/4subtests/11,87 s; general494 passed/22skipped/147subtests/52.66 s, temporal autorizado. Primera dirigida78/3fallos: dos conteos históricos y una expectativa corregida para respetar restricción por gestor implicado. Archivos: dos servicios, dos pruebas, manifiestos266/267 y seguimiento; copia previa conservada y fuente aplicada tras verificar B. Pendientes: QA real/latencia del candidato267, CI/publicación y formal; no se declara RNF-2 aprobado para estos hashes ni despliegue del candidato en principal.


### 2026-10-31 — Smoke C no acredita RNF-2; validación Linux preparada

Propósito: evaluar candidato267 y obtener evidencia separada del host Windows. [268](evidencias/268-smoke-consulta-conjunta-sin-acreditar-rnf2.json): smoke1eb4c64715574171, tres procesos/diez clientes, cero errores; p95 listado114,376 ms, detalle134,766 ms, creación275,641 ms y actualización241,840 ms. SQL265 incidencias/CREADO,162 EDITADO,2650 notificaciones, cero SMTP/IA. QA detenida y principal reanudado healthy según salida y reporte; una muestra breve no demuestra ganancia ni acredita RNF-2.

[269](evidencias/269-rnf2-linux-ci-preparado.json): workflow .github/workflows/performance.yml preparado con protocolo formal existente30+300 s, diez clientes/cien casos y tres procesos, umbral estricto200 ms. Runner ubuntu-24.04 separado del equipo de autora, commit/hardware identificados; sin proveedores ni datos reales. Solo report.json como artefacto14 días, no manifiestos/configuración/claves. El contador Windows de CPU global no aplica a Linux y conserva null; no se modifica guard ni veredicto. La eventual aprobación se limitará al entorno y hashes Linux, sin extenderse a laptop/producción. Archivos: workflow, evidencias268/269 y seguimiento. Validación local: sintaxis YAML/plan del provisionador; ejecución remota y resultado todavía pendientes al registrar. Mantener pruebas funcionales494/22omitidas/147subpruebas y fallos formales262/264 históricos. No se declara cierre integral ni aprobación Linux antes de leer el reporte.


### 2026-10-31 — RNF-2 aprobado en entorno HTTP QA Linux CI

Propósito: validar versión actual fuera del host Windows. [270](evidencias/270-rnf2-linux-ci-aprobado.json), [reporte íntegro271](evidencias/271-rnf2-linux-ci-reporte-completo.json), workflow41273320902 success, commit2bbf4a525d6734f90dfc6058e67ad4d1a597d02b y corrida15eb2b8088e9455a: tres procesos, diez clientes, cien casos,30 s calentamiento+300 s medición completos;71079 solicitudes/0errores. P95 listado31,850 ms, detalle52,603 ms, creación62,175 ms y actualización60,151 ms. Auditoría SQL19809 incidencias/CREADO,19704 EDITADO,198090 entregas, cero SMTP/IA; HTTP posteriorOK, diez logout204 y QA detenida. HardwareLinux7.0/4CPU/Docker15,61 GiB/28.0.4 identificado en reporte. ZIP descargado con SHA256 contrastado contra metadatos de GitHub; reporte preservado sin editar y todos los hashes de código cotejados contra blobs Git. BackendCI41273320913 también success en tests e integración PostgreSQL, sin inventar conteos remotos. Resultado limitado a ese commit/entorno, una corrida, no a laptop, producción, repetibilidad o proveedores externos. Fallos Windows262/264/268 conservados. Archivos:270/271, matrices, protocolo y cierre. Pendientes: publicar registro documental, paquete actualizado, desplegar imágenes en principal y comprobar salud; informe institucional sigue borrador. No repetir pruebas locales para aparentar cierre ni cambiar umbral.
