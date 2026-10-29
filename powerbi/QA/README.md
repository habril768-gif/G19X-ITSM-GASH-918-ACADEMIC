# Validación de presentación en Desktop

Agregados ficticios escritos a mano: dos celdas y 24 campos. No provienen de expedientes ni de una extracción SQL. Las fechas de enero de 2026 son constantes de prueba, no la fecha de ejecución. Resultados observados el 20 de octubre de 2026 en [106](../../docs/evidencias/106-powerbi-qa.json).

## Archivos y reproducción

- `publicado.json`: celda A con volumen 20, media 6 horas, reapertura 55 % y concordancia 50 %; celda B con volumen 20 y sin denominadores.
- `suprimido.json`: retira todos los números de A; B conserva sus valores. Corte ficticio avanza un minuto.
- `entrada_actual.json`: fuente local activa; al terminar quedó igual a `suprimido.json`.
- `Indicadores_QA.pq`: lee ese JSON y asigna tipos a las 24 columnas. Su ruta absoluta debe ajustarse si se mueve el proyecto.
- `Comprobaciones.dax`: ejecutar en vista DAX de la copia QA. Cinco controles deben devolver True para cada instantánea; comprobar también cuál instantánea se cargó y sus valores visibles, porque la consulta admite ambos estados.
- `plurione_bi_QA_publicado.pbix`: copia con caché publicable guardada antes de sustituir la entrada. Al actualizar lee la entrada activa, actualmente suprimida.
- `../plurione_bi_QA_agregados_ficticios.pbix`: copia guardada después del refresco y controles de supresión.

Desde la raíz del proyecto, preparar la instantánea deseada:

```powershell
Copy-Item -LiteralPath .\powerbi\QA\publicado.json -Destination .\powerbi\QA\entrada_actual.json
```

Abrir la copia QA, pulsar Actualizar y ejecutar las comprobaciones. Observar 20, 6.00, 55.0% y 50.0% en A; B mantiene vacíos sus indicadores sin denominador. Los totales de las cuatro medidas son BLANK.

```powershell
Copy-Item -LiteralPath .\powerbi\QA\suprimido.json -Destination .\powerbi\QA\entrada_actual.json
```

Actualizar de nuevo y repetir Ejecutar: A muestra «Suprimido por privacidad» y sus números desaparecen, B conserva volumen 20, y el corte ficticio avanza un minuto. Guardar solo la copia QA. No cambiar el origen PostgreSQL de `../plurione_bi.pbix`.

## Alcance

Verifica presentación, tipos, medidas heredadas, ausencia de denominadores/totales y sustitución de datos importados en Desktop. No evalúa el SQL con estos datos ni demuestra que un cambio de confidencialidad en un expediente recorra automáticamente todas las capas. SQL y ACL tienen pruebas previas separadas; falta el recorrido integrado en un entorno aislado y la custodia/retirada de copias. No reducir k=5 ni convertir NULL en cero. No publicar ni presentar estos archivos QA como métricas reales.
