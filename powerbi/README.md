# Informe y fuentes para Power BI Desktop

Seguir [ANALITICA.md](../docs/ANALITICA.md). Fuente principal: `Indicadores.pq`, una sola consulta con corte/población y métricas desde las dos vistas agregadas de analytics; `consulta.sql` documenta el SELECT. `Corte.pq` es diagnóstico opcional sin carga. `Medidas.dax` contiene plantillas por celda, sin totales; crear cada medida por separado. Usar cuenta de lectura y no pegar contraseñas en archivos.

## Informe principal

[plurione_bi.pbix](plurione_bi.pbix) conserva PostgreSQL como fuente. Modelo revisado en [104](../docs/evidencias/104-powerbi-modelo.json): una tabla Indicadores, sin fechas automáticas; cinco medidas válidas. Ambos porcentajes dividen por 100 y usan Porcentaje/un decimal; Resolución horas usa Número decimal/dos decimales. Fecha de corte procede del mismo dataset. La plantilla Población del informe no está creada como medida; existe una leyenda estática de población parcial/datos simulados.

Refresco confirmado y guardado en [105](../docs/evidencias/105-powerbi-refresco.json): tarjeta 20/10/2026 10:06:02 a.m.; tres celdas suprimidas y números vacíos. El intento fallido previo se conserva en 104. La definición de visuales mantiene tabla con cuatro medidas, sin totales y con filas vacías visibles, tarjeta y leyenda.

## Comprobación con valores visibles

[Guía QA](QA/README.md) y [evidencia 106](../docs/evidencias/106-powerbi-qa.json): copia independiente con dos agregados ficticios manuales, visual 20/6.00/55.0%/50.0%, indicadores sin denominador vacíos, totales BLANK y retirada de números al sustituir la entrada y refrescar. Cinco controles DAX pasan en cada una de las dos instantáneas. La prueba no modifica el principal ni evalúa el SQL con esos datos.

[Ensayo SQL aislado](QA_SQL/README.md), evidencias 108–109: la cuenta BI extrae las vistas antes/después de confidencialidad y Desktop retira los valores mediante un puente JSON agregado; seis controles pasan por fase y el control negativo detecta la caché antigua. No es conexión directa Desktop→PostgreSQL temporal. Quedan conector directo aislado si se exige, custodia/retirada de copias y aceptación integral. No reducir supresión, sustituir NULL por cero, compartir o publicar automáticamente. Las capturas con el nombre real de cuenta permanecen fuera de Git.
