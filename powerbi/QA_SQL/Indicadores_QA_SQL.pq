// SOLO QA: agregados extraidos por cuenta BI de SQL aislado; no base operativa.
let
    Filas = Json.Document(File.Contents("C:/Users/sanch/Documents/Codex/Desarrollo de una Plataforma Inteligente de Gestión de Incidencias Laborales - G19X-ITSM-GASH-918-ACADEMIC/powerbi/QA_SQL/entrada_actual.json")),
    Origen = Table.FromRecords(Filas),
    Indicadores = Table.TransformColumnTypes(Origen, {{"corte_consulta", type datetime}, {"periodo_observacion", type datetime}, {"poblacion", type text}, {"granularidad", type text}, {"mes_creacion", type datetime}, {"categoria_id", type text}, {"categoria", type text}, {"departamento_id", type text}, {"departamento", type text}, {"volumen", Int64.Type}, {"resolucion_casos", Int64.Type}, {"resolucion_horas", type number}, {"resolucion_estado", type text}, {"reapertura_poblacion", Int64.Type}, {"reapertura_casos", Int64.Type}, {"reapertura_porcentaje", type number}, {"reapertura_estado", type text}, {"concordancia_poblacion", Int64.Type}, {"concordancia_coincidencias", Int64.Type}, {"concordancia_porcentaje", type number}, {"concordancia_estado", type text}, {"ia_omitida", Int64.Type}, {"ia_fallida", Int64.Type}, {"privacidad", type text}}, "en-US")
in
    Indicadores
