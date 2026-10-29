"""Prueba de copia/restauración: dos clústeres propios, sin API ni proveedores."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
import re
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import tempfile
import time
from uuid import uuid4

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
from test_support import validate_test_database
from test_postgres_isolated import find_bin


def checksum(value):
    return hashlib.sha256(value).hexdigest()


def canonical_sql(definition):
    """Solo normaliza casts de arrays de literales varchar sin límite a text.

    pg_dump/restore puede distribuir ese cast sobre cada literal. No se quitan
    casts de columnas, tipos numéricos, varchar(n), ni literales o espacios internos.
    """
    literal = r"'(?:[^']|'')*'"
    item = literal + r'::character varying'
    items = r'(?P<items>' + item + r'(?:,\s*' + item + r')*)'
    # pretty=true omite paréntesis que pretty=false conserva.
    for opening,closing in ((r'\(',r'\)'),('','')):
        array = opening+r'ARRAY\['+items+r'\]'+closing+r'::text\[\]'
        definition = re.sub(array, lambda m: 'ARRAY[' + re.sub('('+literal+')::character varying',
                            r'\1::text', m['items']) + ']', definition)
    for opening,closing in ((r'\(',r'\)'),('','')):
        definition=re.sub(opening+'('+literal+r')::character varying'+closing+r'::text',r'\1::text',definition)
    return definition


def connect(env, user=None, password=None):
    import psycopg
    return psycopg.connect(host='127.0.0.1', port=int(env['POSTGRES_PORT']),
                           dbname=env['POSTGRES_DB'], user=user or env['POSTGRES_USER'],
                           password=password or env['POSTGRES_PASSWORD'], connect_timeout=3)


def sql_engine(env):
    from sqlalchemy import URL, create_engine
    return create_engine(URL.create('postgresql+psycopg', username=env['POSTGRES_USER'],
                         password=env['POSTGRES_PASSWORD'], host='127.0.0.1',
                         port=int(env['POSTGRES_PORT']), database=env['POSTGRES_DB']))


def seed(env):
    from sqlalchemy.orm import Session
    from app.models import (Department, User, Incident, AuditEvent, AIJob, MailDelivery,
                            LocalCredential, AuthSession, LoginThrottle,
                            IncidentParticipant, DepartmentAudit)
    engine = sql_engine(env)
    now = datetime.now(timezone.utc)
    with Session(engine) as db:
        department = Department(nombre='DEMO Recuperación aislada')
        db.add(department); db.flush()
        users = [User(email=f'recovery-{i}@example.invalid', nombre_completo=f'Cuenta ficticia {i}',
                      departamento_id=department.id, rol_id=i+1) for i in range(3)]
        db.add_all(users); db.flush()
        admin, supervisor, employee = users
        cases = []
        for i in range(5):
            case = Incident(titulo=f'Prueba recuperación entorno {i}', descripcion='Hechos ficticios de recuperación.',
                            incident_date=now.date(), created_by=admin.id, scope='ENTORNO',
                            reported_department_id=department.id, department_id_at_creation=department.id,
                            category_id=4, priority=3, classification_valid=True, validated_by=admin.id,
                            validated_at=now, assigned_to=supervisor.id, ai_status='OMITIDA',
                            ai_skip_reason='Prueba sin llamadas externas')
            db.add(case); cases.append(case)
        protected = Incident(titulo='Prueba recuperación confidencial', descripcion='Caso ficticio protegido.',
                             incident_date=now.date(), created_by=admin.id, scope='PERSONA',
                             affected_employee_id=employee.id, reported_department_id=department.id,
                             department_id_at_creation=department.id, category_id=2, priority=2,
                             classification_valid=True, validated_by=admin.id, validated_at=now,
                             assigned_to=admin.id, status='CERRADA', is_confidential=True,
                             cycle_start_at=now-timedelta(hours=3), resolved_at=now-timedelta(hours=1),
                             closed_at=now, resolution_text='Resolución ficticia conservada.',
                             ai_status='OMITIDA', ai_skip_reason='Confidencial')
        db.add(protected); cases.append(protected); db.flush()
        events = [AuditEvent(incidencia_id=c.id, usuario_id=admin.id, accion='CREADO',
                             detalle={'simulado': True, 'prueba': 'recuperacion'}) for c in cases]
        db.add_all(events); db.flush()
        db.add(IncidentParticipant(incidencia_id=protected.id, user_id=supervisor.id,
                                  declaration_reason='Relación ficticia para comprobar conservación.'))
        db.add(DepartmentAudit(department_id=department.id, actor_id=admin.id,
                               detalle={'simulado': True, 'motivo': 'Ensayo de recuperación'}))
        db.add(LocalCredential(user_id=admin.id, password_hash='invalid-test-only-not-a-login'))
        db.add(AuthSession(token_hash=checksum(b'no-valid-live-token'), user_id=admin.id,
                           expires_at=now-timedelta(days=1), revoked_at=now))
        db.add(LoginThrottle(email='recovery-lock@example.invalid', failures=1))
        text = 'Texto ficticio pendiente, no enviar.'
        db.add(AIJob(case_id=cases[0].id, reviewed_by=admin.id, input_text=text,
                     input_digest=checksum(text.encode()), content_revision=0, catalog=[],
                     model='test-only-no-provider', prompt_version='test-recovery-only'))
        db.add(MailDelivery(id=uuid4(), event_id=events[0].id, case_id=cases[0].id,
                            recipient_id=admin.id, kind='CREACION', context={}))
        db.commit()
    engine.dispose()


def snapshot(env):
    from psycopg import sql
    result = {'tables': {}, 'views': {}, 'constraints': [], 'indexes': []}
    with connect(env) as connection:
        tables = connection.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename").fetchall()
        for (table,) in tables:
            rows = connection.execute(sql.SQL('SELECT to_jsonb(t)::text FROM public.{} t ORDER BY to_jsonb(t)::text').format(sql.Identifier(table))).fetchall()
            result['tables'][table] = {'count': len(rows), 'sha256': checksum(json.dumps(rows).encode())}
        views = connection.execute("SELECT c.relname,pg_get_viewdef(c.oid,true),c.reloptions FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='analytics' AND c.relkind='v' ORDER BY c.relname").fetchall()
        result['views'] = {name: {'definition_sha256': checksum(canonical_sql(definition).encode()),
                                'definition_sql':canonical_sql(definition),'options': options}
                          for name, definition, options in views}
        constraints = connection.execute("SELECT c.conname,pg_get_constraintdef(c.oid) FROM pg_constraint c JOIN pg_namespace n ON n.oid=c.connamespace WHERE n.nspname='public' ORDER BY c.conname").fetchall()
        result['constraints'] = [(name, canonical_sql(definition)) for name, definition in constraints]
        result['indexes'] = connection.execute("SELECT indexname,indexdef FROM pg_indexes WHERE schemaname='public' ORDER BY indexname").fetchall()
        result['revision'] = connection.execute('SELECT version_num FROM alembic_version').fetchone()[0]
    return result


def reporting(env, username):
    from app.reporting.access import provision
    password = secrets.token_urlsafe(32)
    engine = sql_engine(env)
    try:
        with engine.begin() as db:
            provision(db, username, password)
    finally:
        engine.dispose()
    return password


def verify_reporting(env, username, password):
    import psycopg
    with connect(env, username, password) as db:
        assert db.execute('SELECT count(*) FROM analytics.export_info').fetchone()[0] == 1
        cells = db.execute('SELECT volumen FROM analytics.incident_metrics').fetchall()
        assert cells == [(5,)], 'La celda exportable no coincide con los cinco casos ficticios'
    denied = []
    for statement in ('SELECT * FROM public.incidencias',
                      'DELETE FROM public.incidencias WHERE false',
                      'CREATE TABLE public.recovery_forbidden (id integer)'):
        with connect(env, username, password) as db:
            try:
                db.execute(statement)
            except (psycopg.errors.InsufficientPrivilege, psycopg.errors.ReadOnlySqlTransaction):
                denied.append(True)
            else:
                raise AssertionError('La cuenta BI obtuvo acceso operativo inesperado')
    return {'views_readable': True, 'public_data_and_writes_denied': len(denied)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pg-bin')
    parser.add_argument('--report', help='JSON sanitizado nuevo; no se sobrescribe')
    args = parser.parse_args()
    report_path = Path(args.report).resolve() if args.report else None
    if report_path and report_path.exists():
        parser.error('El reporte ya existe; elegir otro archivo')
    pg_bin, suffix = find_bin(args.pg_bin)
    root = (BACKEND.parent/'.pgdata').resolve(); root.mkdir(exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='recovery-', dir=root)).resolve()
    assert folder.parent == root and folder.name.startswith('recovery-')
    (folder/'isolated-recovery-run').write_text(folder.name, encoding='utf-8')
    report = {'status': 'FAILED', 'date_utc': datetime.now(timezone.utc).isoformat(),
              'test': 'logical_backup_restore_two_isolated_clusters', 'stages': [],
              'development_database_accessed': False, 'workers_started': False,
              'external_calls': False, 'docker_sequence_executed': False,
              'fixture': 'Simulated SQL/ORM fixtures, not a business/API acceptance test'}
    report['schema_comparison']='Exacta tras normalizar únicamente casts de arrays de literales varchar sin límite a text; datos por hash exacto'
    clusters = []; envs = {}; current = 'initialization'; failed = False
    def command(label, arguments, env):
        nonlocal current
        current = label
        start = time.perf_counter()
        result = subprocess.run([str(a) for a in arguments], cwd=BACKEND, env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if result.returncode: raise RuntimeError(label)
        report['stages'].append({'stage': label, 'seconds': round(time.perf_counter()-start, 3)})
        print(label+': OK', flush=True)
    def binary(name): return pg_bin/(name+suffix)
    try:
        report['postgres'] = subprocess.check_output([str(binary('postgres')), '--version'], text=True).strip()
        for label in ('source', 'target'):
            with socket.socket() as listener:
                listener.bind(('127.0.0.1',0)); port=listener.getsockname()[1]
            # Ninguna variable libpq heredada puede redirigir la conexión de QA.
            env={key:value for key,value in os.environ.items() if not key.startswith('PG')}
            env.update(POSTGRES_HOST='127.0.0.1', POSTGRES_PORT=str(port), POSTGRES_USER='qa_recovery_'+label,
                       POSTGRES_DB='plurione_test_recovery_'+label, POSTGRES_PASSWORD=secrets.token_urlsafe(32),
                       PGPASSWORD='', RUN_DB_TESTS='1', AI_ENABLED='false', MAIL_ENABLED='false')
            env['PGPASSWORD']=env['POSTGRES_PASSWORD']
            validate_test_database(env)
            data=folder/label; pw=folder/(label+'.password')
            pw.write_text(env['POSTGRES_PASSWORD']+'\n',encoding='utf-8')
            command(label+'_init', [binary('initdb'),'-D',data,'-U',env['POSTGRES_USER'],
                    '--pwfile='+str(pw),'--encoding=UTF8','--locale=C',
                    '--auth-host=scram-sha-256','--auth-local=scram-sha-256'],env)
            pw.unlink()
            clusters.append((label,data,env))
            command(label+'_start',[binary('pg_ctl'),'-D',data,'-l',folder/(label+'.log'),
                    '-o',f'-h 127.0.0.1 -p {port}','-w','-t','30','start'],env)
            command(label+'_database',[binary('createdb'),'-h','127.0.0.1','-p',port,
                    '-U',env['POSTGRES_USER'],env['POSTGRES_DB']],env)
            envs[label]=env
        source, target = envs['source'], envs['target']
        command('source_migrate',[sys.executable,'-m','alembic','upgrade','head'],source)
        command('source_schema_check',[sys.executable,'-m','alembic','check'],source)
        current='fixture'; seed(source)
        assert snapshot(source)['tables']['incidencias']['count']==6
        source_bi='qa_source_bi'; source_bi_password=reporting(source,source_bi)
        report['source_bi']=verify_reporting(source,source_bi,source_bi_password)
        before=snapshot(source)
        archive=folder/'backup.dump'
        command('logical_backup',[binary('pg_dump'),'-h','127.0.0.1','-p',source['POSTGRES_PORT'],
                '-U',source['POSTGRES_USER'],'-d',source['POSTGRES_DB'],'-Fc','-f',archive],source)
        report['archive']={'bytes':archive.stat().st_size,'sha256':checksum(archive.read_bytes())}
        command('archive_catalog',[binary('pg_restore'),'--list',archive],source)
        invalid=folder/'invalid.dump'; invalid.write_bytes(b'not-a-postgresql-archive')
        current='invalid_archive'
        negative=subprocess.run([str(binary('pg_restore')),'--list',str(invalid)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        assert negative.returncode!=0, 'No se rechazo un archivo invalido'
        report['invalid_archive_rejected']=True
        command('restore_isolated',[binary('pg_restore'),'-h','127.0.0.1','-p',target['POSTGRES_PORT'],
                '-U',target['POSTGRES_USER'],'-d',target['POSTGRES_DB'],'--exit-on-error',
                '--no-owner','--no-privileges',archive],target)
        current='compare_data_schema'
        after=snapshot(target)
        # Solo conteos, hashes y definiciones de esquema, nunca filas o credenciales.
        (folder/'source_snapshot.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
        (folder/'target_snapshot.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
        if before != after:
            report['comparison_differences']={
                'sections':[key for key in before if before[key]!=after[key]],
                'tables':[name for name in set(before['tables'])|set(after['tables'])
                          if before['tables'].get(name)!=after['tables'].get(name)],
                'views':[name for name in set(before['views'])|set(after['views'])
                         if before['views'].get(name)!=after['views'].get(name)]}
        assert before==after, 'El contenido o esquema restaurado no coincide'
        report['data_comparison']={'all_tables_equal':True, 'tables':after['tables'],
                                   'revision':after['revision'],'views_equal':True,
                                   'constraints_compared':len(after['constraints']),
                                   'indexes_compared':len(after['indexes'])}
        command('target_schema_check',[sys.executable,'-m','alembic','check'],target)
        current='rebuild_bi_permissions'
        with connect(target) as db:
            assert db.execute('SELECT count(*) FROM pg_roles WHERE rolname=%s',(source_bi,)).fetchone()[0]==0
        password=reporting(target,'qa_restored_bi')
        report['restored_bi']=verify_reporting(target,'qa_restored_bi',password)
        assert snapshot(source)==before, 'El origen cambio durante el ensayo'
        assert snapshot(target)==after, 'La comprobacion altero los datos restaurados'
        report['source_unchanged']=True
        report['status']='PASSED'
    except Exception as exc:
        failed=True
        report['failure']={'stage':current,'type':type(exc).__name__}
        print('Ensayo no completado en '+current+' ('+type(exc).__name__+'). Sin datos de conexion.',flush=True)
    finally:
        stops={}
        for label,data,env in reversed(clusters):
            try:
                command(label+'_stop',[binary('pg_ctl'),'-D',data,'-m','fast','-w','-t','30','stop'],env)
                stops[label]=True
            except Exception:
                status=subprocess.run([str(binary('pg_ctl')),'-D',str(data),'status'],
                                      env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                # pg_ctl status=3 acredita que no hay servidor activo en ese directorio.
                stops[label]=status.returncode==3
                if not stops[label]: failed=True; report['status']='FAILED'
        report['servers_stopped']=stops
        report['retained_local_folder']=folder.name
        report['limits']=['PostgreSQL nativo; secuencia Docker no ejecutada',
                          'Datos ficticios insertados para recuperacion, no recorrido de negocio',
                          'Propietarios/ACL originales no restaurados; BI reconstruido y probado aparte',
                          'Sin instalacion limpia, carga, capacitacion o aceptacion integral',
                          'Archivo y clusters detenidos conservados en .pgdata ignorado por Git']
        destination=report_path or folder/'report.json'
        destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Resultado: '+report['status'],flush=True)
    return 1 if failed else 0


if __name__=='__main__':
    raise SystemExit(main())
