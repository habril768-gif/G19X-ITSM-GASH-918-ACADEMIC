// Solo esta consulta se carga al modelo. Corte y datos proceden de un SELECT.
let
    Servidor = "127.0.0.1:5433",
    BaseDatos = "plurione",
    Origen = PostgreSQL.Database(Servidor, BaseDatos, [CreateNavigationProperties=false]),
    Indicadores = Value.NativeQuery(Origen, "SELECT e.corte AS corte_consulta, e.periodo_inicio AS periodo_observacion, e.poblacion, e.granularidad,        m.mes_creacion, m.categoria_id, m.categoria, m.departamento_id, m.departamento, m.volumen, m.resolucion_casos, m.resolucion_horas, m.resolucion_estado, m.reapertura_poblacion, m.reapertura_casos, m.reapertura_porcentaje, m.reapertura_estado, m.concordancia_poblacion, m.concordancia_coincidencias, m.concordancia_porcentaje, m.concordancia_estado, m.ia_omitida, m.ia_fallida,        coalesce(m.privacidad, 'Sin datos') AS privacidad FROM analytics.export_info e LEFT JOIN analytics.incident_metrics m ON true", null, [EnableFolding=false])
in
    Indicadores
