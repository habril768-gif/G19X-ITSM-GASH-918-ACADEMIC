CREATE SCHEMA analytics;
REVOKE ALL ON SCHEMA analytics FROM PUBLIC;
-- statement
CREATE VIEW analytics.export_info WITH (security_barrier=true) AS
SELECT transaction_timestamp() AS corte,
       date_trunc('year', transaction_timestamp() AT TIME ZONE 'America/Mexico_City')
           AT TIME ZONE 'America/Mexico_City' AS periodo_inicio,
       'Solo población exportable; no representa el total de la empresa'::text AS poblacion,
       'Mes de creación, categoría oficial y departamento histórico'::text AS granularidad,
       5::integer AS minimo_casos_y_personas,
       'Sin totales, subtotales ni detalle individual'::text AS restricciones;
-- statement
CREATE VIEW analytics.incident_metrics WITH (security_barrier=true) AS
WITH params AS MATERIALIZED (SELECT * FROM analytics.export_info),
eligible AS MATERIALIZED (
    SELECT i.id, i.scope, i.affected_employee_id, i.status, i.created_at,
           i.cycle_start_at, i.resolved_at, i.ai_status, i.ai_suggestion,
           i.classification_valid, i.category_id,
           date_trunc('month',i.created_at AT TIME ZONE 'America/Mexico_City')::date AS mes_creacion,
           coalesce(i.category_id,0) AS category_key,
           i.department_id_at_creation AS department_key
    FROM public.incidencias i CROSS JOIN params p
    WHERE NOT i.is_confidential AND i.created_at <= p.corte
      AND NOT EXISTS (SELECT 1 FROM public.incident_involved_users r
          WHERE r.incidencia_id=i.id AND r.review_status IN ('DECLARADO','CONFIRMADO'))
      AND NOT EXISTS (SELECT 1 FROM public.users u JOIN public.roles role ON role.id=u.rol_id
          WHERE u.id=i.affected_employee_id AND role.nombre IN ('ADMIN_RH','SUPERVISOR'))
), resolutions AS MATERIALIZED (
    SELECT id AS case_id, resolved_at FROM eligible WHERE resolved_at IS NOT NULL
    UNION
    SELECT a.incidencia_id, (a.detalle->'after'->>'resolved_at')::timestamptz
    FROM public.historial_incidencias a JOIN eligible e ON e.id=a.incidencia_id CROSS JOIN params p
    WHERE a.fecha<=p.corte AND a.accion='ESTADO_CAMBIADO' AND a.detalle->'after'->>'status'='RESUELTA'
      AND a.detalle->'after'->>'resolved_at' IS NOT NULL
    UNION
    SELECT a.incidencia_id, (a.detalle->'before'->>'resolved_at')::timestamptz
    FROM public.historial_incidencias a JOIN eligible e ON e.id=a.incidencia_id CROSS JOIN params p
    WHERE a.fecha<=p.corte AND a.accion='REAPERTURA' AND a.detalle->'before'->>'resolved_at' IS NOT NULL
), first_resolution AS (
    SELECT case_id,min(resolved_at) AS first_at FROM resolutions CROSS JOIN params
    WHERE resolved_at >= periodo_inicio AND resolved_at <= corte GROUP BY case_id
), classified AS (
    SELECT e.*, f.first_at,
           (e.status IN ('RESUELTA','CERRADA') AND e.cycle_start_at IS NOT NULL
              AND e.resolved_at IS NOT NULL AND e.resolved_at >= e.cycle_start_at
              AND e.resolved_at <= p.corte) AS last_resolved,
           (f.first_at IS NOT NULL AND EXISTS (
               SELECT 1 FROM public.historial_incidencias a WHERE a.incidencia_id=e.id
                 AND a.accion='REAPERTURA' AND a.fecha > f.first_at AND a.fecha <= p.corte
           )) AS reopened,
           (e.ai_status='COMPLETADA' AND e.classification_valid AND e.category_id IS NOT NULL
              AND coalesce(e.ai_suggestion->>'result','')='CLASIFICADA'
              AND coalesce(e.ai_suggestion->>'category_id','') IN ('1','2','3','4','5')) AS comparable
    FROM eligible e LEFT JOIN first_resolution f ON f.case_id=e.id CROSS JOIN params p
), annotated AS MATERIALIZED (
    SELECT c.*,
           (c.comparable AND c.ai_suggestion->>'category_id'=c.category_id::text) AS matching,
           CASE WHEN last_resolved THEN extract(epoch FROM (resolved_at-cycle_start_at))/3600.0 END AS hours
    FROM classified c
), members AS (
    SELECT a.mes_creacion,a.category_key,a.department_key,a.id,a.scope,a.affected_employee_id,v.tag
    FROM annotated a CROSS JOIN LATERAL (VALUES
        ('volumen',true),('resolucion',a.last_resolved),('resolucion_complemento',NOT a.last_resolved),
        ('reapertura_poblacion',a.first_at IS NOT NULL),('reapertura_fuera',a.first_at IS NULL),
        ('reapertura_si',a.reopened),('reapertura_no',a.first_at IS NOT NULL AND NOT a.reopened),
        ('concordancia_poblacion',a.comparable),('concordancia_fuera',NOT a.comparable),
        ('concordancia_si',a.matching),('concordancia_no',a.comparable AND NOT a.matching),
        ('ia_omitida',a.ai_status='OMITIDA'),('ia_fallida',a.ai_status='FALLIDA'),
        ('ia_otros',a.ai_status NOT IN ('OMITIDA','FALLIDA'))
    ) AS v(tag,included) WHERE v.included
), group_sizes AS (
    SELECT mes_creacion,category_key,department_key,tag,count(DISTINCT id) AS n,
           count(*) FILTER (WHERE scope='PERSONA') AS personal,
           count(DISTINCT affected_employee_id) FILTER (WHERE scope='PERSONA') AS people
    FROM members GROUP BY mes_creacion,category_key,department_key,tag
), safety AS (
    SELECT mes_creacion,category_key,department_key,
           bool_and(n>=5 AND (personal=0 OR people>=5)) AS publish
    FROM group_sizes GROUP BY mes_creacion,category_key,department_key
), stats AS (
    SELECT mes_creacion,category_key,department_key,count(*) AS volume,
           count(*) FILTER (WHERE last_resolved) AS resolved_n,
           avg(hours) FILTER (WHERE last_resolved) AS resolution_hours,
           count(*) FILTER (WHERE first_at IS NOT NULL) AS reopening_population,
           count(*) FILTER (WHERE reopened) AS reopening_n,
           count(*) FILTER (WHERE comparable) AS comparison_population,
           count(*) FILTER (WHERE matching) AS matching_n,
           count(*) FILTER (WHERE ai_status='OMITIDA') AS ai_omitted,
           count(*) FILTER (WHERE ai_status='FALLIDA') AS ai_failed
    FROM annotated GROUP BY mes_creacion,category_key,department_key
)
SELECT p.corte,p.periodo_inicio,s.mes_creacion,nullif(s.category_key,0) AS categoria_id,
       coalesce(c.nombre,'Sin clasificación oficial') AS categoria,
       s.department_key AS departamento_id,d.nombre AS departamento,
       CASE WHEN k.publish THEN 'Publicado' ELSE 'Suprimido por privacidad' END AS privacidad,
       CASE WHEN k.publish THEN s.volume END AS volumen,
       CASE WHEN k.publish THEN s.resolved_n END AS resolucion_casos,
       CASE WHEN k.publish THEN s.resolution_hours END AS resolucion_horas,
       CASE WHEN NOT k.publish THEN 'Suprimido por privacidad' WHEN s.resolved_n=0 THEN 'Sin datos' ELSE 'Disponible' END AS resolucion_estado,
       CASE WHEN k.publish THEN s.reopening_population END AS reapertura_poblacion,
       CASE WHEN k.publish THEN s.reopening_n END AS reapertura_casos,
       CASE WHEN k.publish AND s.reopening_population>0 THEN 100.0*s.reopening_n/s.reopening_population END AS reapertura_porcentaje,
       CASE WHEN NOT k.publish THEN 'Suprimido por privacidad' WHEN s.reopening_population=0 THEN 'Sin datos' ELSE 'Disponible' END AS reapertura_estado,
       CASE WHEN k.publish THEN s.comparison_population END AS concordancia_poblacion,
       CASE WHEN k.publish THEN s.matching_n END AS concordancia_coincidencias,
       CASE WHEN k.publish AND s.comparison_population>0 THEN 100.0*s.matching_n/s.comparison_population END AS concordancia_porcentaje,
       CASE WHEN NOT k.publish THEN 'Suprimido por privacidad' WHEN s.comparison_population=0 THEN 'Sin datos' ELSE 'Disponible' END AS concordancia_estado,
       CASE WHEN k.publish THEN s.ai_omitted END AS ia_omitida,
       CASE WHEN k.publish THEN s.ai_failed END AS ia_fallida
FROM stats s JOIN safety k USING(mes_creacion,category_key,department_key)
JOIN public.departamentos d ON d.id=s.department_key
LEFT JOIN public.categorias_incidencia c ON c.id=s.category_key CROSS JOIN params p;
-- statement
REVOKE ALL ON ALL TABLES IN SCHEMA analytics FROM PUBLIC;
