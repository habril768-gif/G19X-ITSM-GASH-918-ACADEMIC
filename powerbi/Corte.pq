// Referencia opcional para diagnóstico: deshabilitar carga.
// La tarjeta de corte del informe utiliza Indicadores[corte_consulta], nunca otra consulta SQL.
let
    Metadata = Table.Distinct(Table.SelectColumns(Indicadores,
        {"corte_consulta", "periodo_observacion", "poblacion", "granularidad"}))
in
    Metadata
