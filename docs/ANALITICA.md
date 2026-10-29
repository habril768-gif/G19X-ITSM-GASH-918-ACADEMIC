# Analítica agregada

RF-6 se prepara en PostgreSQL antes de conectar Power BI Desktop. No se importan expedientes para ocultarlos después con filtros. Las vistas exportables no incluyen IDs de casos/personas, nombres personales, correos, descripción, sugerencias o resoluciones. Departamento y categoría son dimensiones de catálogo; el ID de departamento identifica la entidad histórica, no una persona. Gerencia sigue siendo destinataria del reporte, no un rol de la aplicación.

## Qué población se cuenta

Se excluyen confidenciales, afectados que actualmente sean gestores y cualquier relación DECLARADO o CONFIRMADO. Se adopta exclusión conservadora de todas las relaciones activas, incluidas las de no gestores. DESCARTADO no excluye por sí solo, pero tampoco desmarca confidencialidad. Las condiciones se vuelven a evaluar en cada consulta. La población exportable es parcial y su etiqueta aparece en la extracción: no es el total de la empresa.

Solo existe una granularidad: mes de creación en America/Mexico_City, categoría oficial actual y department_id_at_creation. Un traslado del afectado no mueve el caso de su departamento histórico. El nombre mostrado es el nombre actual del catálogo de esa entidad; no se inventa una etiqueta histórica inexistente. Sin categoría oficial se muestra ese estado, sin añadir una sexta categoría al sistema de clasificación.

Cada subconjunto que contribuye a una métrica exige al menos cinco casos distintos y, si contiene personas, cinco afectados distintos. ENTORNO no cuenta como afectado personal. Se comprueban también complementos (resueltos/no resueltos, comparables/no comparables, coincidencias/discrepancias, reabiertos/no reabiertos e IA omitida/fallida/restante). Si cualquier subconjunto no vacío incumple, se suprime toda la celda y todos sus números quedan NULL con «Suprimido por privacidad». Es deliberadamente más conservador que publicar volumen y ocultar solo un promedio. Cero real puede publicarse cuando no hay contribuyentes de ese tipo; cero no reemplaza a una supresión.

No hay filas de totales/subtotales, vistas de detalle, granularidades alternativas ni conteos de excluidos. Las métricas usan la misma celda/población. No inferir un total real sumando solo valores publicados ni completar nulos con datos operacionales. Un conjunto pequeño puede quedar totalmente suprimido: es el comportamiento esperado; no reducir el mínimo para obtener gráficos.

## Fórmulas y periodo

El corte es transaction_timestamp() y el periodo de observación de reapertura va del primer día del año en curso, en America/Mexico_City, hasta ese corte. El mes de la fila siempre corresponde a creación: una cohorte de diciembre del año anterior puede tener resoluciones en el periodo anual actual. No es una tasa por mes de resolución ni se limita la población de casos a los creados en el año. No hay un parámetro para consultar ventanas arbitrarias superpuestas; otro periodo requiere una definición y revisión explícitas.

| Indicador | Definición antes de supresión |
| --- | --- |
| Volumen | Casos únicos elegibles en cada cohorte |
| Resolución horas | Media de resolved_at − cycle_start_at del último ciclo RESUELTA/CERRADA a corte; excluye abiertos/fechas incompletas o invertidas |
| Reapertura | IDs con una reapertura posterior a su primera resolución del periodo / IDs con al menos una resolución en el periodo; cada ID una vez, aunque tenga múltiples reaperturas |
| Concordancia | Categoría sugerida igual a la categoría humana vigente / casos comparables con ambas; solo IA COMPLETADA/CLASIFICADA y validación humana vigente |
| IA omitida/fallida | Conteos separados dentro de población elegible, con la misma protección de subconjuntos |

Las resoluciones anteriores se recuperan de eventos ESTADO_CAMBIADO/after y REAPERTURA/before además del campo vigente; UNION elimina duplicados. Auditoría posterior al corte no entra. Así una reapertura que limpió resolved_at no borra su contribución histórica. El promedio de resolución publicado es del último ciclo, no un promedio combinado de ciclos históricos. No hay aún una vista de promedios históricos por ventana arbitraria. Sin denominador, porcentaje NULL y «Sin datos», sin división por cero. La concordancia es operativa y no sustituye a la precisión contra referencias de RF-3.

## Actualizar y crear la cuenta

Desde raíz, con Docker Desktop abierto:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ACTUALIZAR_ANALITICA.ps1
docker compose exec api python -m app.manage_reporting_user
```

El primero construye API, migra a 0007 y aplica compose.bi.yaml, publicando PostgreSQL solo en 127.0.0.1:5433 (BI_POSTGRES_PORT configurable). Conserva volúmenes y no crea datos de ejemplo; PostgreSQL puede reiniciarse brevemente al añadir el puerto. No activa ni evalúa IA. Los workers existentes recuperan conexión; sus imágenes no se reconstruyen con este script. Para futuras operaciones que deban conservar el puerto, usar `docker compose -f compose.yaml -f compose.bi.yaml ...`.

El segundo solicita una contraseña de 16–128 caracteres sin mostrarla y crea plurione_bi (nombre configurable con --username). No pegarla en chat, código, línea de comandos o Power Query. Solo concede SELECT en analytics.incident_metrics y analytics.export_info, USAGE en analytics y CONNECT; sin privilegios de escritura, roles privilegiados o acceso a tablas públicas. También fija lectura por defecto y timeout de 30s, pero la seguridad real depende de ACL, no de ese ajuste. Rechaza un usuario ya existente sin cambiarlo y falla/revierte si PUBLIC concede acceso operativo o creación de objetos. No cambia privilegios globales de PUBLIC. Si la provisión falla, revisar con el operador sin usar una cuenta administradora como alternativa en Power BI.

El script no revela .env ni reutiliza la contraseña del administrador. Cuenta de lectura separada por destinatario cuando corresponda; revocación de acceso y custodia de credenciales requieren operación autorizada. La aplicación no distribuye contraseñas de base a usuarios empleados/supervisores.

## Importar en Power BI Desktop

1. Crear un archivo nuevo. Obtener datos → Consulta en blanco → Editor avanzado. Pegar powerbi/Indicadores.pq y nombrar la consulta **Indicadores**. Ajustar solo servidor/base si difieren de 127.0.0.1:5433/plurione.
2. Autenticación de base de datos con plurione_bi y la contraseña recién creada. No usar POSTGRES_USER ni su contraseña administradora. Si aparece aprobación de consulta nativa, comprobar que solo lee las dos vistas analytics; no habilitar consultas de tablas public.
3. Cargar únicamente Indicadores en modo Importar. powerbi/consulta.sql documenta el mismo SELECT. En una sola sentencia incorpora corte/población y celdas; si no hay celdas devuelve solo una fila de metadata, números NULL y «Sin datos». Así el corte queda visible incluso con población vacía.
4. No cargar Corte.pq: es referencia opcional de diagnóstico. Para la tarjeta de fecha usar la medida Fecha de corte de Medidas.dax, derivada del mismo dataset cargado. No usar hora local de NOW() ni otra consulta como corte del informe.
5. Crear las medidas de Medidas.dax, una por bloque. Porcentajes: esas medidas dividen por 100; usar formato Porcentaje. Horas: decimal. No resumir columnas numéricas automáticamente.

El conector ya se usó en Desktop por la responsable: consulta de tres celdas agregadas y 24 columnas, con supresión visible en 94–95. powerbi/plurione_bi.pbix está guardado; su definición de visuales fue inspeccionada en 98. No se ha publicado. La revisión posterior del modelo en Desktop está en [104](evidencias/104-powerbi-modelo.json): cinco medidas válidas, ambas medidas porcentuales con formato Porcentaje/un decimal y división entre 100, horas guardadas con dos decimales. Desactivadas las fechas automáticas del archivo; el inventario pasó de cinco tablas a solo Indicadores. La única partición coincide con Indicadores.pq al ignorar espacios/saltos y su comentario inicial. El intento de refresco fue rechazado por conexión; no se acreditó extracción nueva ni valores positivos de QA.

## Diseño del informe sin reconstrucciones

Tabla principal con mes_creacion, categoria, departamento, privacidad, Volumen visible, Resolución horas, Reapertura porcentaje y Concordancia porcentaje. Mostrar «Suprimido por privacidad»/«Sin datos» mediante las columnas de estado; mantener los números vacíos. Desactivar totales/subtotales y resumen automático; las medidas devuelven BLANK con más de una celda. No sumar/ponderar promedios o porcentajes, ni mostrar el total de casos de la empresa.

Slicers solo de las dimensiones ya exportadas; si se usa gráfico, elegir un departamento y categoría y un punto por mes de creación. Desactivar fecha/hora automática, jerarquías temporales, drill-down/drill-through, páginas de detalle y conexiones a otras granularidades o fuentes individuales. No agregar prioridades, estados, usuarios, días o participantes. Mantener leyenda de población parcial, fecha de corte y periodo de observación visibles. No publicar en web ni compartir fuera de RH/Gerencia autorizados.

## Actualización y límites

Actualización manual antes de compartir cada nueva versión. Rehacer extracción desde vistas vigentes, reemplazar datos importados anteriores, comprobar supresiones y retirar copias antiguas según procedimiento. Un archivo ya entregado no se revoca automáticamente. Cambios entre versiones o información externa pueden permitir inferencias: k=5 no garantiza anonimato. Solo datos simulados en este MVP; no presentar la salida como autorización de datos reales.

Documentación primaria: [vistas PostgreSQL](https://www.postgresql.org/docs/17/sql-createview.html), [conector Microsoft](https://learn.microsoft.com/en-us/power-query/connectors/postgresql), [PostgreSQL.Database](https://learn.microsoft.com/en-us/powerquery-m/postgresql-database).

## Comportamiento visual y prueba local observada

Con todos los valores de una medida BLANK, Power BI puede ocultar filas. Activar «Mostrar elementos sin datos» en mes_creacion dentro de Columnas conserva las etiquetas sin sustituir números. En el PBIX guardado showAll=true, totals=false y mes_creacion usa columna directa sin jerarquía. Mantener una celda por mes/categoría/departamento.

Para 127.0.0.1:5433 local de desarrollo se configuró manualmente la conexión sin cifrado porque el contenedor no tiene TLS; no extender ese ajuste a conexiones remotas. Los valores vacíos actuales solo acreditan supresión: no prueban formato 0.0% ni precisión visual. No actualizar el corte con NOW() ni una fecha manual. Capturas originales 96–97 muestran nombre de cuenta: quedan locales y requieren una copia sin esa cabecera antes de versionarlas.


## Resolver conexión local rechazada después de reiniciar Docker

Docker puede estar operativo y postgres en ejecución sin publicar el puerto que usa Desktop. En la revisión 104, postgres-1 no mostraba puerto publicado y Actualizar falló; el corte siguió siendo el de la carga anterior. Un refresco fallido no acredita datos actuales.

Desde la terminal propia, en la raíz del proyecto, habilitar el puerto con la capa existente:

```powershell
docker compose -f compose.yaml -f compose.bi.yaml up -d --wait postgres
docker compose -f compose.yaml -f compose.bi.yaml ps postgres
```

Esto puede recrear/reiniciar brevemente solo postgres conservando su volumen; no crea incidencias ni reconstruye los workers. Comprobar `127.0.0.1:5433->5432/tcp` (o BI_POSTGRES_PORT si se configuró otro). Cerrar el aviso en Power BI, pulsar Actualizar y comprobar que finaliza sin error y avanza la tarjeta de corte antes de guardar. Si solicita credenciales o aprobación de consulta nativa, la responsable debe revisarlas en Desktop. Mantener la cuenta de lectura y las dos vistas analytics; no sustituirla por una cuenta administradora.

La CLI de las herramientas recibió permiso denegado para la tubería de Docker; no se cambiaron ACL ni ajustes de seguridad para eludirlo. Los formatos configurados y la supresión existente no sustituyen la prueba con valores publicables ni la retirada de valores al cambiar elegibilidad.


## Refresco y QA de Desktop comprobados

[105](evidencias/105-powerbi-refresco.json): tras la orden de la autora para aplicar compose.bi.yaml, la tarjeta del principal avanzó a 20/10/2026 10:06:02 a.m. sin aviso de error visible y se guardó. Las tres celdas siguen suprimidas. No se sobrescribió la evidencia 104 del fallo anterior.

[106](evidencias/106-powerbi-qa.json) y [guía QA](../powerbi/QA/README.md): copia separada, con agregados ficticios manuales y las medidas heredadas. Se observaron 20 casos, 6.00 horas, 55.0% y 50.0%; la celda sin denominadores conserva indicadores vacíos. Cinco controles DAX pasaron en cada instantánea, incluidos totales BLANK. Tras sustituir la entrada ficticia por otra con A suprimida y refrescar, desaparecieron los cuatro números y avanzó el corte ficticio. B conservó volumen 20. El principal mantuvo su hash durante QA.

Las fechas de QA son constantes simuladas, no hora de ejecución. Se probó la presentación y sustitución de datos importados, sin ejecutar el SQL con ese fixture ni cambiar confidencialidad real. Quedan el recorrido integrado de elegibilidad SQL→Desktop en aislamiento, custodia/retirada de copias y aceptación integral. No presentar la prueba de una copia como revocación de archivos ya distribuidos.


## Cambio SQL y refresco mediante puente de QA

[Guía SQL QA](../powerbi/QA_SQL/README.md), evidencias [108](evidencias/108-powerbi-sql-aislado.json) y [109](evidencias/109-powerbi-sql-desktop.json): PostgreSQL aislado con 40 casos ficticios y cuenta BI, SELECT exacto de consulta.sql, antes/después de marcar un caso confidencial. La vista excluye el caso y suprime los once números de su celda; la otra conserva volumen 20. Exportador sin sustitución manual de cifras; servidor detenido.

En Desktop se cargaron esas dos extracciones mediante JSON: 20/6.00/55.0%/50.0% antes y números retirados tras refrescar. Seis controles por fase verifican valores, estado, dos celdas, denominadores, totales BLANK y corte a precisión de segundos. Antes de actualizar, el DAX de la fase final rechaza estado/números/corte antiguos: se comprueba que un resultado en caché no se acepta como extracción nueva.

Es SQL→agregado JSON→Desktop, sin conectar Desktop directamente al servidor temporal ni probar permisos de cambio en API/UI. El principal conserva su conector y refresco independiente (105), con hash sin cambios durante QA. Persisten custodia/retirada de copias, aceptación por roles y prueba del conector directo aislado si se exige. Intento fallido 107 conservado: acción de auditoría no admitida en el fixture, corregida sin relajar la restricción. No se redujo k=5 ni se publicaron datos reales.
