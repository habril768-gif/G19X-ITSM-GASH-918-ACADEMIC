# Plan de mantenimiento, recuperación y soporte

## Alcance y estado

Plan operativo para el entorno local con datos simulados. Define responsables por función, tareas, un procedimiento de copia y una prueba de restauración aislada. **La copia y restauración lógica entre dos clústeres PostgreSQL nativos ya se verificó con datos ficticios (evidencia 103). La secuencia Docker descrita abajo sigue preparada, sin ejecución acreditada desde herramientas.** No se asignan RPO, RTO, disponibilidad ni SLA sin una medición y acuerdo específicos.

El operador realiza acciones técnicas; Admin RH verifica el funcionamiento de negocio que le corresponde. La persona responsable del proyecto conserva evidencias y decide si el resultado cumple el [MVP](MVP.md). Estos papeles no asignan personas nuevas ni acreditan capacitación.

## Soporte por niveles

| Nivel | Responsabilidad | Información y escalamiento |
| --- | --- | --- |
| Atención inicial | Ayudar con navegación, sesión, filtros y mensajes usando el manual | Registrar pantalla, acción y resultado sanitizados; escalar si afecta permisos o persiste |
| Operación técnica | Revisar servicios, esquema, conexión, colas, configuración y copias | Corresponde al operador autorizado; no solicitar al usuario contraseñas ni tokens |
| Desarrollo | Analizar errores reproducibles, concurrencia y regresiones | Usar entorno de prueba aislado, corrección revisable y pruebas pertinentes antes de actualizar |

Los niveles son responsabilidades de soporte y no prioridades Alta/Media/Baja de un expediente. No hay canal externo, guardia ni tiempos de respuesta comprometidos. Una incidencia de acceso indebido o pérdida de datos requiere contener el acceso afectado y escalar al operador antes de nuevas pruebas.

## Registro y tratamiento de una solicitud

1. Registrar un identificador de soporte, hora, componente, pasos, resultado y alcance aparente, sin datos personales reales o credenciales.
2. Verificar si es una restricción prevista: confidencialidad, conflicto, sesión revocada, clasificación inválida o supresión BI.
3. Reproducir con datos ficticios en aislamiento cuando haga falta; no ejecutar seeds ni pruebas destructivas en la base de uso.
4. Documentar diagnóstico, acción, prueba de verificación y resultado. Un resultado incierto no se registra como resuelto.
5. Confirmar recuperación con el usuario autorizado y conservar evidencia sanitizada. Si requiere cambio de código, relacionarlo con pruebas y documentación.

## Rutina propuesta

Estas tareas no están programadas automáticamente:

| Momento | Tarea | Criterio de resultado |
| --- | --- | --- |
| Antes de una sesión de pruebas | Revisar servicios, `/health` y `/health/db`; acceso de la cuenta adecuada | Proceso, conexión y esquema disponibles; sin acreditar por ello todo el negocio |
| Antes de migrar o cambiar dependencias | Registrar código/configuración, copiar base y verificar recuperación en aislamiento | Existe copia identificada y prueba de restauración satisfactoria |
| Al finalizar una jornada con cambios de datos | Realizar copia si deben conservarse, registrar corte y hash | Archivo fuera del repositorio y custodia confirmada; no basta con que exista |
| Tras una actualización | Revisar migración, pruebas pertinentes y recorridos afectados | Resultados y límites en QA, sin confundir CI preparado con CI ejecutado |
| En cada revisión de soporte | Revisar trabajos fallidos/omitidos, acceso y uso de almacenamiento | Diagnóstico sin reenvíos masivos, eliminación de historial ni exposición de datos |
| Antes de compartir un PBIX | Revisar corte, elegibilidad, modelo, supresión y destinatarios | Copia autorizada con riesgo residual de distribución documentado |

Revisar dependencias, certificados y privilegios de forma planificada según el entorno; no actualizar ciegamente a una edición distinta. Las tareas de limpieza de sesiones, retención de textos IA, outbox e historial requieren política aprobada y pruebas previas. No se incluye un borrado automático.

## Qué conservar y qué no cubre la copia

| Elemento | Conservación necesaria |
| --- | --- |
| PostgreSQL | Copia lógica de esquema y datos, con registro de procedencia y comprobación de restauración |
| Configuración privada | Custodia separada y restringida de credenciales; nunca Git, capturas o archivo de soporte público |
| Código y migraciones | Estado identificable del repositorio y dependencias; Git no respalda los datos de PostgreSQL |
| Power BI y evidencia | Copia autorizada del archivo y fuentes, con corte/hash; no incluir capturas personales sin sanitizar |
| Redis | Los trabajos IA son durables en PostgreSQL; no se exige recuperar avisos como única fuente de trabajo |
| Mailpit | El buzón de captura no es registro duradero garantizado; la outbox y auditoría no prueban recepción externa |

Una copia lógica de una base no incluye todos los objetos globales del servidor, como roles. La recuperación de QA descrita abajo omite propietarios y permisos para no depender de cuentas del origen; **no valida la reproducción de privilegios de una instalación completa**. La cuenta BI y sus ACL deben reconstruirse y probarse por separado antes de conectar consumidores.

Las copias contienen hashes de credenciales, sesiones, textos de prueba y trabajos pendientes. Trátalas como material restringido aunque el conjunto sea ficticio; no subirlas al repositorio. Debe definirse retención y destino de custodia antes de uso real. No elimines la última copia comprobada para ahorrar espacio.

## Custodia y retirada de informes Power BI

Procedimiento preparado; no acredita una entrega, autorización o retirada real. Antes de distribuir debe quedar designada la persona responsable de autorizar destinatarios y la persona operadora que conservará el archivo y su registro.

1. **Preparar la copia.** Usar el informe principal `powerbi/plurione_bi.pbix`, actualizarlo sin errores y comprobar corte, población parcial, supresión y ausencia de totales. Las copias QA, sus instantáneas y capturas de cuenta se conservan separadas del material de entrega.
2. **Identificarla.** Registrar el corte visible del dataset y el hash SHA-256 del archivo guardado. La fecha de guardado no sustituye al corte. Desde la raíz del proyecto puede obtenerse el hash con `Get-FileHash -LiteralPath .\powerbi\plurione_bi.pbix -Algorithm SHA256`.
3. **Autorizar y custodiar.** Confirmar destinatarios RH/Gerencia autorizados, finalidad, ubicación restringida y plazo o condición de conservación. Si falta alguna decisión, la copia queda pendiente de distribución. Conservar el registro operativo en una ubicación privada; no introducir nombres, correos, rutas privadas o aprobaciones personales en Git.
4. **Entregar y sustituir.** Registrar la entrega solo después de realizarla. Cuando cambie la elegibilidad, actualizar y verificar una copia nueva; identificar por hash la anterior y solicitar su retirada a cada destinatario y ubicación registrados. Mantener por separado las retiradas solicitadas y las confirmadas.
5. **Cerrar la retirada.** Registrar confirmación efectiva de devolución/eliminación o la imposibilidad de obtenerla y escalar al responsable. Revocar la cuenta BI impide consultas futuras, pero no borra datos ya importados ni copias distribuidas. No declarar una retirada automática o completa sin evidencia.

El registro privado debe contener: identificador de entrega, corte, hash, responsable/autorización, destinatarios, canal y ubicación, fecha real de entrega, plazo o condición de conservación y estado/evidencia de retirada. Es una estructura por completar, no un registro de hechos ocurridos. No se fija una retención arbitraria ni se elimina la última copia comprobada sin una decisión autorizada.

Pendiente operativo: designar responsables, ubicación, destinatarios y conservación; practicar una entrega/sustitución autorizada y registrar su resultado. La aceptación por roles permanece separada.

## Copia lógica preparada para el entorno local

Ejecutar solo por operador, desde la raíz del proyecto, en una ventana acordada. Guardar fuera del repositorio. Los bloques siguientes son instrucciones, no evidencia de ejecución. Si utilizas archivos Compose adicionales, conserva la misma combinación que inició el entorno.

Antes de detener procesos, deja finalizar las operaciones externas que puedas verificar. Detener un worker no deshace una llamada o SMTP ya iniciados; registrar cualquier resultado incierto. Pausa el uso del panel y detén los procesos que escriben, manteniendo PostgreSQL:

```powershell
docker compose --profile ai --profile mail stop api ai-worker mail-worker
if ($LASTEXITCODE -ne 0) { throw 'No se confirmó la pausa de los procesos.' }
```

No usar `down --volumes`, copiar un volumen activo como si fuera una copia lógica ni canalizar el archivo binario por redirección de texto de PowerShell.

```powershell
$backupRoot = Join-Path $env:USERPROFILE 'Documents\RespaldosPluriOne'
New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
$backupStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$containerArchive = "/tmp/plurione-$backupStamp.dump"
$backupArchive = Join-Path $backupRoot "plurione-$backupStamp.dump"
if (Test-Path -LiteralPath $backupArchive) { throw 'El destino ya existe; no sobrescribir.' }

docker compose exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=custom --file="$1"' sh $containerArchive
if ($LASTEXITCODE -ne 0) { throw 'Falló la copia; no marcar respaldo válido.' }
docker compose cp "postgres:$containerArchive" $backupArchive
if ($LASTEXITCODE -ne 0) { throw 'No se confirmó la transferencia al equipo.' }
Get-Item -LiteralPath $backupArchive | Select-Object Name, Length
Get-FileHash -LiteralPath $backupArchive -Algorithm SHA256
```

El archivo se genera dentro del contenedor con sus herramientas y se copia como binario. Registrar nombre, tamaño, hash, revisión del código y resultado de cada paso sin secretos. El hash detecta cambios del archivo, pero no acredita que pueda recuperarse. Si falla un paso, mantener el estado como no verificado y decidir la reanudación; no perder de vista que los procesos quedaron pausados. El temporal del contenedor se conserva hasta completar la comprobación y limpieza manual controlada.

## Restauración de ensayo en un destino aislado

Usar una copia propia y de procedencia confiable: restaurar un archivo puede ejecutar contenido definido en él. No apuntar estos comandos a la base operativa ni publicar puertos. La imagen de origen en Compose es `postgres:17-bookworm`; el ensayo usa esa misma línea para evitar una actualización mayor implícita. No modifica los volúmenes del proyecto.

Continúa en la misma sesión, con `$backupArchive` del bloque anterior, o asígnale explícitamente la ruta de la copia elegida. El nombre de contenedor es nuevo; no se reutiliza un destino existente. La credencial temporal no se imprime ni se escribe en el comando como valor literal:

```powershell
$restoreContainer = 'plurione-restore-' + [guid]::NewGuid().ToString('N').Substring(0,12)
$previousRestorePassword = [Environment]::GetEnvironmentVariable('POSTGRES_PASSWORD', 'Process')
try {
    $env:POSTGRES_PASSWORD = [guid]::NewGuid().ToString('N')
    docker run --detach --name $restoreContainer --network none --env POSTGRES_PASSWORD --env POSTGRES_USER=restore_operator --env POSTGRES_DB=plurione_restore postgres:17-bookworm
    if ($LASTEXITCODE -ne 0) { throw 'No se creó el destino aislado.' }
} finally {
    [Environment]::SetEnvironmentVariable('POSTGRES_PASSWORD', $previousRestorePassword, 'Process')
}

$restoreReady = $false
for ($restoreAttempt=0; $restoreAttempt -lt 30; $restoreAttempt++) {
    docker exec $restoreContainer pg_isready -U restore_operator -d plurione_restore *> $null
    if ($LASTEXITCODE -eq 0) { $restoreReady=$true; break }
    Start-Sleep -Seconds 2
}
if (-not $restoreReady) { throw 'Destino sin disponibilidad; revisar sin restaurar al origen.' }

docker cp $backupArchive "${restoreContainer}:/tmp/restore.dump"
if ($LASTEXITCODE -ne 0) { throw 'No se transfirió la copia al destino.' }
docker exec $restoreContainer pg_restore --list /tmp/restore.dump
if ($LASTEXITCODE -ne 0) { throw 'No se pudo leer el catálogo del archivo.' }
docker exec $restoreContainer pg_restore --exit-on-error --no-owner --no-privileges --username=restore_operator --dbname=plurione_restore /tmp/restore.dump
if ($LASTEXITCODE -ne 0) { throw 'Restauración fallida o incompleta; no aceptar el ensayo.' }
```

El destino está sin red y sin API/workers. No se envían notificaciones ni peticiones IA por restaurar tablas. No conectes después los workers a la copia: podría contener trabajos y sesiones históricos capaces de provocar reenvíos o accesos inesperados si se reactivaran sin una política específica.

La lectura del catálogo no sustituye la restauración ni las comprobaciones siguientes. No se usan `--clean`, borrado de base o sustitución de la instalación de uso.

## Comprobar el ensayo y reanudar

Sobre el destino aislado, el operador debe verificar al menos:

- Revisión de `alembic_version` correspondiente al código de la copia y presencia de las tablas y vistas previstas.
- Conteos y relaciones coherentes con el corte: casos, participantes, historial, trabajos y outbox; una copia vacía no demuestra recuperar casos.
- Un caso ficticio conocido, su clasificación y ciclo/historial; no consultar ni exportar filas personales reales.
- Datos analíticos y supresión coherentes. Para probar permisos BI se necesita reconstruir la cuenta y ejecutar verificaciones negativas separadas; el ensayo sin ACL no los acredita.
- Ausencia de errores de restauración, duración medida y hash del archivo utilizado. No inventar tiempo de recuperación ni pérdida tolerable.

Ejemplo de lectura limitada, solo sobre el contenedor de ensayo:

```powershell
docker exec $restoreContainer psql -U restore_operator -d plurione_restore -v ON_ERROR_STOP=1 -c 'SELECT version_num FROM alembic_version;'
if ($LASTEXITCODE -ne 0) { throw 'No se confirmó la revisión restaurada.' }
```

Registrar el ensayo como aprobado únicamente si cumple su alcance comprobado; la recuperación de permisos, credenciales de infraestructura, consumidores e instalación completa sigue siendo un trabajo adicional. No migrar el archivo restaurado para ocultar un fallo de correspondencia con el código original.

La base de uso no fue sustituida. Para reanudarla, confirma que corresponde al mismo código/configuración y arranca API y únicamente los workers que estaban activados antes de la pausa. Ejemplo si solo corresponde API: `docker compose start api`. Si estaban activos IA o correo, usa sus perfiles y servicios explícitos, sin habilitar integraciones que antes estaban apagadas. Comprueba `/health/db`, el panel y los resultados inciertos antes de permitir nueva actividad.

Conserva el contenedor aislado detenido para diagnóstico si hay fallos: `docker stop $restoreContainer`. La eliminación posterior requiere comprobar el nombre exacto creado, que no sea un servicio de trabajo y que el registro/copia se hayan conservado. Este procedimiento no ejecuta limpieza automática ni borra volúmenes.

## Actualizaciones y recuperación ante fallos

Antes de una actualización, identifica código, dependencias, migraciones pendientes y copia recuperable. Reconstruye los componentes afectados y aplica el esquema según el manual técnico. Ejecuta pruebas y recorridos que cubran el cambio. No se promete reversión con downgrade: algunas migraciones protegen credenciales y auditoría y no admiten una vuelta automática segura.

Si falla, registra el punto de fallo y limita el uso afectado. No mezcles código antiguo con un esquema incompatible ni restaures una copia encima de la base activa. Una recuperación real exige evaluar datos posteriores al corte, sesiones, permisos, trabajos con efectos externos y una ventana de cambio autorizada; validar primero en un destino separado.

## Condiciones de cierre del plan

La recuperación lógica nativa y los permisos de la cuenta BI reconstruida tienen evidencia satisfactoria. Para cerrar operación y soporte faltan: probar la secuencia Docker, recuperar una instalación completa con configuración privada y roles aplicables, definir custodia/retención y responsables efectivos, revisar capacidad y practicar escalamiento. El ensayo pequeño no fija RPO/RTO ni acredita capacitación o recuperación productiva.

Semántica de las herramientas consultada en documentación oficial: [pg_dump](https://www.postgresql.org/docs/17/app-pgdump.html) describe la copia lógica y su alcance por base; [pg_restore](https://www.postgresql.org/docs/17/app-pgrestore.html) describe archivos, restauración y tratamiento de errores/propietarios. La secuencia Docker/PowerShell es una adaptación preparada para el Compose del repositorio y requiere la prueba indicada.

## Ejecutor y estado de verificación

Está disponible [test_recovery_isolated.py](../backend/scripts/test_recovery_isolated.py). Crea dos clústeres PostgreSQL nativos nuevos en `.pgdata`, con puertos y credenciales temporales, nombres de base exclusivos de QA y variables de conexión controladas. No carga `.env`, no usa la base de trabajo y no inicia API o workers. Conserva los recursos propios detenidos para diagnóstico; no elimina carpetas antiguas ni volúmenes.

El plan del ejecutor es migrar el origen, insertar seis casos ficticios y entidades relacionadas, crear una copia lógica, restaurar al destino y comparar todas las tablas, restricciones, índices y vistas. Después reconstruye la cuenta BI en destino y comprueba lecturas permitidas y operaciones denegadas. Los propietarios y ACL originales no se trasladan como si fueran cuentas equivalentes; el chequeo BI es separado. También comprueba que un archivo inválido sea rechazado.

El ensayo vigente, [evidencia 103](evidencias/103-recuperacion-aislada.json), terminó PASSED: catorce tablas idénticas por conteos y hashes de filas, dos vistas, 144 restricciones y 35 índices comprobados, revisión de esquema sin diferencias y origen sin cambios. Se conservan seis casos ficticios, participante, historial, trabajo IA, sesión revocada y outbox. La comparación de definiciones reconoce únicamente la distribución equivalente de casts de arrays de literales varchar sin límite a text; mantiene valores, tipos acotados y opciones de seguridad. Cinco pruebas automatizadas cubren esa normalización y rechazos.

La cuenta BI se reconstruyó en el destino: leyó vistas y una celda exportable de cinco casos, mientras se rechazaron lectura, borrado y creación de tabla sobre datos operativos. Se comprobó que el rol BI del origen no se trasladó como objeto global y que un archivo inválido se rechaza. Ambos servidores quedaron detenidos. La copia tardó 0.546 s y la restauración 0.667 s en este conjunto; son duraciones de etapas, no RTO de una instalación completa.

Los intentos anteriores y el diagnóstico se conservan en QA y evidencias 99–102. En 100–102 la copia/restauración concluyó, pero la comparación textual de SQL no aceptó inicialmente las conversiones equivalentes; no hubo diferencias en los datos de las tablas. No se reescribieron esos reportes como éxitos. Docker funciona según la autora; el acceso a su API desde herramientas sigue denegado. No se consultó la base de trabajo ni se iniciaron API/workers.

Para repetir el ensayo con un reporte nuevo, desde una terminal propia en la raíz, con las dependencias del backend y PostgreSQL nativo instalados:

```powershell
.\backend\.venv\Scripts\python.exe .\backend\scripts\test_recovery_isolated.py --report .\docs\evidencias\104-recuperacion-aislada.json
```

Si no detecta los binarios, se puede indicar `--pg-bin` con su carpeta real. Un reporte existente no se sobrescribe. El JSON registra PASSED o FAILED, etapa y tiempos sin credenciales. No presentar como éxito hasta revisar su resultado, comparaciones y parada de ambos servidores. Este ejecutor nativo no verifica la secuencia Docker del procedimiento anterior.


## Consulta después del reinicio de API reportado

[Evidencia 120](evidencias/120-api-reinicio-consulta-rh.json): tras la instrucción de reiniciar solo API, la autora confirma finalización; capturas muestran consulta del listado/detalle desde RH, mismo caso En revisión con prioridad Baja, validación vigente y confidencialidad restringida a RH independiente. Confirma /health/db con status ok/database postgresql. No hay captura del comando ni medición del reinicio; prueba manual acotada, sin instalación limpia, reinicio de base/Redis o recuperación completa.
