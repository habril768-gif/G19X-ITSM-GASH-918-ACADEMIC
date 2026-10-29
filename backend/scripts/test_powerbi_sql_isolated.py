"""Ensayo SQL aislado: exportar agregados antes/después de confidencialidad para QA Desktop."""
import argparse
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
from uuid import UUID
from zoneinfo import ZoneInfo

BACKEND=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BACKEND))
from test_support import validate_test_database
from test_postgres_isolated import find_bin
from test_recovery_isolated import connect, sql_engine, reporting

METRICS=('volumen','resolucion_casos','resolucion_horas','reapertura_poblacion','reapertura_casos','reapertura_porcentaje','concordancia_poblacion','concordancia_coincidencias','concordancia_porcentaje','ia_omitida','ia_fallida')
EXPECTED_FIELDS=('corte_consulta','periodo_observacion','poblacion','granularidad','mes_creacion','categoria_id','categoria','departamento_id','departamento','volumen','resolucion_casos','resolucion_horas','resolucion_estado','reapertura_poblacion','reapertura_casos','reapertura_porcentaje','reapertura_estado','concordancia_poblacion','concordancia_coincidencias','concordancia_porcentaje','concordancia_estado','ia_omitida','ia_fallida','privacidad')

def checksum(data): return hashlib.sha256(data).hexdigest()

def json_value(value):
    if isinstance(value,datetime):
        return value.astimezone(ZoneInfo('America/Mexico_City')).replace(tzinfo=None).isoformat()
    if isinstance(value,date): return value.isoformat()+'T00:00:00'
    if isinstance(value,Decimal): return float(value)
    if isinstance(value,UUID): return str(value)
    raise TypeError(type(value).__name__)

def seed(env):
    from sqlalchemy import text
    from sqlalchemy.orm import Session
    from app.models import Department,User,Incident,AuditEvent
    engine=sql_engine(env)
    with Session(engine) as db:
        dep=Department(nombre='QA SQL - datos ficticios')
        db.add(dep);db.flush()
        users=[User(email=f'qa-sql-{i}@example.invalid',nombre_completo=f'Cuenta ficticia {i}',departamento_id=dep.id,rol_id=3) for i in range(20)]
        manager=User(email='qa-sql-manager@example.invalid',nombre_completo='Gestor ficticio',departamento_id=dep.id,rol_id=1)
        db.add_all(users+[manager]);db.flush()
        info=db.execute(text('SELECT * FROM analytics.export_info')).mappings().one()
        span=info['corte']-info['periodo_inicio']
        assert span>timedelta(days=1),'Ejecutar fuera del primer día del periodo anual'
        old=info['periodo_inicio']+span/4
        reopened=info['periodo_inicio']+span/2
        latest=info['periodo_inicio']+span*0.75
        cases=[]
        for i in range(20):
            values=dict(titulo='QA SQL persona ficticia',descripcion='Contenido ficticio privado, no exportar',incident_date=info['corte'].date(),created_at=info['periodo_inicio']-timedelta(days=1),created_by=users[i].id,affected_employee_id=users[i].id,scope='PERSONA',reported_department_id=dep.id,department_id_at_creation=dep.id,category_id=2,assigned_to=manager.id,priority=2,classification_valid=True,validated_by=manager.id,validated_at=latest)
            if i<10:
                values.update(status='RESUELTA',cycle_start_at=latest-timedelta(hours=6),resolved_at=latest,resolution_text='Resolución ficticia',ai_status='COMPLETADA',ai_suggestion={'result':'CLASIFICADA','category_id':2 if i<5 else 3})
            else:
                values.update(status='EN_REVISION',cycle_start_at=reopened,ai_status='OMITIDA' if i<15 else 'FALLIDA',ai_skip_reason='QA sin proveedor' if i<15 else None)
            case=Incident(**values);db.add(case);db.flush();cases.append(case)
            if i>=10:
                db.add(AuditEvent(incidencia_id=case.id,usuario_id=manager.id,accion='REAPERTURA',fecha=reopened,detalle={'before':{'resolved_at':old.isoformat(),'cycle_start_at':(old-timedelta(hours=2)).isoformat()}}))
        for stamp in (reopened,reopened+span/10):
            db.add(AuditEvent(incidencia_id=cases[0].id,usuario_id=manager.id,accion='REAPERTURA',fecha=stamp,detalle={'before':{'resolved_at':old.isoformat(),'cycle_start_at':(old-timedelta(hours=2)).isoformat()}}))
        for i in range(20):
            db.add(Incident(titulo='QA SQL entorno ficticio',descripcion='Contenido ficticio privado, no exportar',incident_date=info['corte'].date(),created_at=info['periodo_inicio']-timedelta(days=1),created_by=users[i].id,scope='ENTORNO',reported_department_id=dep.id,department_id_at_creation=dep.id,category_id=4,ai_status='OMITIDA',ai_skip_reason='QA sin proveedor'))
        db.commit()
        selected_id=cases[0].id
    engine.dispose()
    return selected_id

def extract(env,password,query):
    from psycopg.rows import dict_row
    with connect(env,'qa_bi_sql',password) as db:
        with db.cursor(row_factory=dict_row) as cursor:
            rows=cursor.execute(query).fetchall()
    assert len(rows)==2
    assert all(tuple(row)==EXPECTED_FIELDS for row in rows),'Columnas de extracción inesperadas'
    return sorted(rows,key=lambda row:row['categoria_id'])

def assert_rows(rows,suppressed):
    a,b=rows
    assert a['categoria_id']==2 and b['categoria_id']==4
    assert b['privacidad']=='Publicado' and b['volumen']==20
    assert b['resolucion_horas'] is None and b['reapertura_porcentaje'] is None and b['concordancia_porcentaje'] is None
    if suppressed:
        assert a['privacidad']=='Suprimido por privacidad'
        assert all(a[key] is None for key in METRICS)
    else:
        assert a['privacidad']=='Publicado' and a['volumen']==20
        assert a['resolucion_casos']==10 and a['resolucion_horas']==6
        assert a['reapertura_poblacion']==20 and a['reapertura_casos']==11 and a['reapertura_porcentaje']==55
        assert a['concordancia_poblacion']==10 and a['concordancia_coincidencias']==5 and a['concordancia_porcentaje']==50
        assert a['ia_omitida']==5 and a['ia_fallida']==5
    assert rows[0]['corte_consulta']==rows[1]['corte_consulta']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pg-bin')
    parser.add_argument('--output-dir',required=True,help='Carpeta QA nueva para agregados, sin sobrescribir')
    parser.add_argument('--report',required=True,help='JSON nuevo de resultados sin secretos')
    args=parser.parse_args()
    output=Path(args.output_dir).resolve();report_path=Path(args.report).resolve()
    if output.exists() or report_path.exists():parser.error('Se requieren carpeta y reporte nuevos')
    report={'fecha_utc':datetime.now(timezone.utc).isoformat(),'status':'FAILED','test':'isolated_sql_eligibility_aggregate_export','development_database_accessed':False,'workers_started':False,'external_calls':False,'desktop_verified':False,'steps':[]}
    pg_bin,suffix=find_bin(args.pg_bin)
    root=(BACKEND.parent/'.pgdata').resolve();root.mkdir(exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix='powerbi-sql-',dir=root)).resolve()
    assert folder.parent==root
    data=folder/'data';pw=folder/'password'
    env={key:value for key,value in os.environ.items() if not key.startswith('PG')}
    with socket.socket() as listener:
        listener.bind(('127.0.0.1',0));port=listener.getsockname()[1]
    env.update(POSTGRES_HOST='127.0.0.1',POSTGRES_PORT=str(port),POSTGRES_USER='qa_sql_owner',POSTGRES_PASSWORD=secrets.token_urlsafe(32),POSTGRES_DB='plurione_test_bi_sql',RUN_DB_TESTS='1',AI_ENABLED='false',MAIL_ENABLED='false',SSLKEYLOGFILE='')
    env['PGPASSWORD']=env['POSTGRES_PASSWORD'];validate_test_database(env)
    def binary(name):return pg_bin/(name+suffix)
    started=False;failed=False;stage='init'
    def command(label,args):
        nonlocal stage
        stage=label
        result=subprocess.run([str(x) for x in args],cwd=BACKEND,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if result.returncode:raise RuntimeError(label)
        report['steps'].append(label);print(label+': OK',flush=True)
    try:
        report['postgres']=subprocess.check_output([str(binary('postgres')),'--version'],text=True).strip()
        pw.write_text(env['POSTGRES_PASSWORD']+'\n',encoding='utf-8');pw.chmod(0o600)
        command('initdb',[binary('initdb'),'-D',data,'-U',env['POSTGRES_USER'],'--pwfile='+str(pw),'--encoding=UTF8','--locale=C','--auth-host=scram-sha-256','--auth-local=scram-sha-256'])
        pw.unlink();started=True
        command('start',[binary('pg_ctl'),'-D',data,'-l',folder/'server.log','-o',f'-h 127.0.0.1 -p {port}','-w','-t','30','start'])
        command('createdb',[binary('createdb'),'-h','127.0.0.1','-p',port,'-U',env['POSTGRES_USER'],env['POSTGRES_DB']])
        command('migrate',[sys.executable,'-m','alembic','upgrade','head'])
        command('schema_check',[sys.executable,'-m','alembic','check'])
        stage='fixture';selected_id=seed(env)
        password=reporting(env,'qa_bi_sql')
        stage='read_only_negative'
        import psycopg
        try:
            with connect(env,'qa_bi_sql',password) as db:db.execute('SELECT * FROM public.incidencias LIMIT 0')
        except psycopg.errors.InsufficientPrivilege:report['bi_operational_access_denied']=True
        else:raise AssertionError('Acceso operativo inesperado')
        query=(BACKEND.parent/'powerbi/consulta.sql').read_text(encoding='utf-8')
        report['query_sha256']=checksum(query.encode('utf-8'))
        stage='published_sql';before=extract(env,password,query);assert_rows(before,False)
        stage='confidentiality_change'
        from sqlalchemy import text
        from sqlalchemy.orm import Session
        from app.models import Incident,AuditEvent
        engine=sql_engine(env)
        with Session(engine) as db:
            case=db.get(Incident,selected_id);assert case is not None and not case.is_confidential
            case.is_confidential=True
            db.add(AuditEvent(incidencia_id=case.id,usuario_id=case.validated_by,accion='CAMBIO_CONFIDENCIALIDAD',detalle={'simulado':True,'before':{'is_confidential':False},'after':{'is_confidential':True}}))
            db.commit()
        with engine.connect() as db:
            assert db.scalar(text('SELECT count(*) FROM incidencias'))==40
            assert db.scalar(text('SELECT count(*) FROM incidencias WHERE is_confidential'))==1
        engine.dispose()
        stage='suppressed_sql';after=extract(env,password,query);assert_rows(after,True)
        assert after[0]['corte_consulta']>before[0]['corte_consulta']
        output.mkdir(parents=True)
        for name,rows in [('publicado.json',before),('suprimido.json',after),('entrada_actual.json',before)]:
            (output/name).write_text(json.dumps(rows,default=json_value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        report.update(status='PASSED',fixture={'incidents':40,'confidential_after':1,'cells':2,'distinct_affected_people':20,'origin':'ORM fixtures in new native PostgreSQL, not API/business acceptance'},published={'volume':20,'hours':6,'reopening_percent':55,'concordance_percent':50},suppressed={'all_11_numbers_null':True,'other_cell_volume':20},exports={name:{'sha256':checksum((output/name).read_bytes()),'bytes':(output/name).stat().st_size} for name in ('publicado.json','suprimido.json')},cuts={name:json_value(rows[0]['corte_consulta']) for name,rows in [('published',before),('suppressed',after)]})
    except Exception as exc:
        failed=True;report['failure']={'stage':stage,'type':type(exc).__name__}
        original=getattr(exc,'orig',None)
        constraint=getattr(getattr(original,'diag',None),'constraint_name',None)
        if constraint:report['failure']['constraint']=constraint
        print('Ensayo falló en '+stage+' ('+type(exc).__name__+'); sin datos de conexión.',flush=True)
    finally:
        if pw.exists():pw.unlink()
        if started:
            try:command('stop',[binary('pg_ctl'),'-D',data,'-m','fast','-w','-t','30','stop'])
            except Exception:pass
        status=subprocess.run([str(binary('pg_ctl')),'-D',str(data),'status'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        report['server_stopped']=status.returncode==3
        if not report['server_stopped']:report['status']='FAILED';failed=True
        report['retained_local_folder']=folder.name
        report['limits']=['Exportación agregada JSON como puente de QA, no conector directo Desktop→PostgreSQL aislado','Cambio ORM de confidencialidad, sin API/UI ni workers','Permisos BI reales y SELECT de consulta.sql; sin credenciales en agregados o reporte','Desktop se verifica por separado; este reporte por sí solo no lo acredita','No es carga, custodia, distribución ni aceptación integral']
        with report_path.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
        print('Resultado: '+report['status'],flush=True)
    return 1 if failed else 0

if __name__=='__main__':raise SystemExit(main())
