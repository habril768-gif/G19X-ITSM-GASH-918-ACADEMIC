# Ensayo SQL → agregado JSON → Desktop

Prueba aislada realizada con 40 incidencias ficticias. A diferencia de [QA manual](../QA/README.md), estas instantáneas son resultados de las vistas SQL, sin escribir a mano las métricas. Evidencia SQL [108](../../docs/evidencias/108-powerbi-sql-aislado.json) y Desktop [109](../../docs/evidencias/109-powerbi-sql-desktop.json). El intento [107](../../docs/evidencias/107-powerbi-sql-aislado.json) falló por una acción de auditoría inválida del fixture y se conserva; la restricción del sistema no se modificó.

## Qué se ejecutó

1. Clúster PostgreSQL nuevo en loopback, credenciales efímeras, esquema migrado/check, sin leer .env ni conectar a la base de uso. Veinte casos PERSONA y veinte ENTORNO, todos ficticios; cuenta BI separada con acceso operativo rechazado.
2. SELECT exacto de `../consulta.sql` con la cuenta BI: dos celdas/24 campos. A: volumen 20, media 6 horas, reapertura 55 % y concordancia 50 %. B: volumen 20, sin denominadores.
3. Cambio ORM de un caso A a confidencial y evento CAMBIO_CONFIDENCIALIDAD. Nueva transacción/consulta BI: SQL excluye ese caso y suprime toda A por protección de subconjuntos; sus once números son NULL. B conserva su volumen. No se reescribieron métricas en el exportador.
4. Se detuvo el servidor y se conservó su carpeta en .pgdata ignorado. Las dos extracciones agregadas se cargaron en una copia QA mediante JSON; las medidas heredadas no cambiaron.
5. Publicado: visual 20/6.00/55.0%/50.0%, seis controles DAX True. Antes de refrescar, las expectativas de suprimido rechazaron correctamente estado, números y corte antiguos. Después de Actualizar: los números de A desaparecieron y los seis controles de suprimido pasaron. Corte comparado con la extracción a precisión de segundos.

## Archivos y reproducción Desktop

- `publicado.json` y `suprimido.json`: resultados agregados de SQL; fechas reales del ensayo, no constantes ficticias del QA manual.
- `entrada_actual.json`: fuente de la copia, al terminar igual a suprimido.
- `Indicadores_QA_SQL.pq`: carga las 24 columnas con tipos; ajustar su ruta absoluta si se mueve el proyecto.
- `Comprobaciones_publicado.dax` y `Comprobaciones_suprimido.dax`: expectativas distintas y explícitas, incluidos estado y corte de cada extracción.
- `plurione_bi_QA_SQL_publicado.pbix`: caché publicable guardada; al refrescar leerá la entrada activa.
- `../plurione_bi_QA_SQL_aislado.pbix`: caché suprimida y comprobaciones finales guardadas.

Desde la raíz del proyecto, copiar publicado a entrada_actual, abrir **solo la copia QA SQL**, pulsar Actualizar y ejecutar su DAX publicado:

```powershell
Copy-Item -LiteralPath .\powerbi\QA_SQL\publicado.json -Destination .\powerbi\QA_SQL\entrada_actual.json
```

Luego preparar la segunda extracción, Actualizar y ejecutar el DAX suprimido:

```powershell
Copy-Item -LiteralPath .\powerbi\QA_SQL\suprimido.json -Destination .\powerbi\QA_SQL\entrada_actual.json
```

Cada fase debe devolver seis True; no reutilizar el resultado visual de una consulta DAX anterior sin pulsar Ejecutar. No cambiar el origen del informe principal ni cargar expedientes individuales. El control negativo solo se espera antes de actualizar, cuando el modelo conserva el estado anterior.

## Repetir SQL en otro entorno aislado

Usar nombres nuevos de carpeta/reporte, porque el ejecutor rechaza sobrescribir evidencias. Desde la raíz:

```powershell
.\backend\.venv\Scripts\python.exe .\backend\scripts\test_powerbi_sql_isolated.py --output-dir .\powerbi\QA_SQL_NUEVA --report .\docs\evidencias\powerbi-sql-nueva-ejecucion.json
```

Requiere los binarios PostgreSQL instalados y dependencias existentes del backend. Inicializa y detiene su propio servidor, sin Docker ni workers. El fixture requiere haber transcurrido el primer día del año de observación. La nueva ejecución produce otros cortes; adaptar la fuente QA y sus expectativas, sin sobrescribir las evidencias anteriores.

## Límites

El recorrido validado usa un **puente agregado JSON**. No certifica una conexión directa Desktop→PostgreSQL temporal, ni permisos de la API/UI para cambiar confidencialidad. El conector del principal tiene un refresco real separado (105). Esta prueba no autoriza distribución, no retira copias ya entregadas ni acredita carga, privacidad integral o aceptación institucional. Solo datos simulados; custodiar y diferenciar los archivos QA.
