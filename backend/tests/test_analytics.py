"""RF-6 se comprueba en PostgreSQL real, nunca contra la base operativa."""
import os
from datetime import timedelta
from uuid import uuid4
import pytest
from sqlalchemy import text,select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session
from app.core.database import get_engine
from app.models import Department,User,Incident,IncidentParticipant,AuditEvent
from app.reporting.access import provision,ReportingAccessError
from test_support import validate_test_database

pytestmark=pytest.mark.skipif(os.environ.get('RUN_DB_TESTS')!='1',reason='Requiere PostgreSQL de pruebas migrado')
METRICS=('volumen','resolucion_casos','resolucion_horas','reapertura_poblacion','reapertura_casos','reapertura_porcentaje','concordancia_poblacion','concordancia_coincidencias','concordancia_porcentaje','ia_omitida','ia_fallida')

@pytest.fixture
def world():
    validate_test_database(os.environ)
    with get_engine().connect() as conn:
        tx=conn.begin()
        with Session(bind=conn,expire_on_commit=False) as db:
            dep=Department(nombre='BI-QA-'+uuid4().hex,is_active=True)
            second=Department(nombre='BI-QA-'+uuid4().hex,is_active=True)
            db.add_all([dep,second]); db.flush()
            users=[User(email=uuid4().hex+'@example.invalid',nombre_completo='Persona ficticia',departamento_id=dep.id,rol_id=3,is_active=True) for _ in range(25)]
            manager=User(email=uuid4().hex+'@example.invalid',nombre_completo='Gestor ficticio',departamento_id=dep.id,rol_id=1,is_active=True)
            db.add_all(users+[manager]); db.flush()
            info=db.execute(text('SELECT * FROM analytics.export_info')).mappings().one()
            def add(index,**changes):
                case=Incident(id=uuid4(),titulo='Solo simulación',descripcion='Texto privado no exportable',incident_date=info['corte'].date(),
                    created_at=info['periodo_inicio']-timedelta(days=1),created_by=users[index].id,affected_employee_id=users[index].id,
                    scope='PERSONA',reported_department_id=dep.id,department_id_at_creation=dep.id,category_id=2)
                for key,value in changes.items(): setattr(case,key,value)
                db.add(case); db.flush(); return case
            def rows():
                db.flush()
                return db.execute(text('SELECT * FROM analytics.incident_metrics WHERE departamento_id=:dep ORDER BY categoria_id'),{'dep':dep.id}).mappings().all()
            try: yield db,conn,dep,second,users,manager,info,add,rows
            finally:
                db.rollback()
                if tx.is_active: tx.rollback()

def test_empty_population_and_cut_metadata(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    assert rows()==[]
    assert info['minimo_casos_y_personas']==5 and 'exportable' in info['poblacion']
    assert info['corte']>=info['periodo_inicio']

@pytest.mark.parametrize('n',[1,2,3,4])
def test_small_cells_have_no_exportable_numbers(world,n):
    *_,add,rows=world
    for i in range(n): add(i)
    row=rows()[0]
    assert row['privacidad']=='Suprimido por privacidad'
    assert all(row[name] is None for name in METRICS)

def test_five_distinct_people_and_zero_denominators(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    for i in range(5): add(i)
    row=rows()[0]
    assert row['privacidad']=='Publicado' and row['volumen']==5
    for metric in ('reapertura','concordancia','resolucion'):
        assert row[metric+'_estado']=='Sin datos'
    assert row['reapertura_porcentaje'] is None and row['concordancia_porcentaje'] is None
    assert row['ia_omitida']==row['ia_fallida']==0
    assert row['corte']==info['corte']

def test_same_affected_person_and_mixed_environment_are_suppressed(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    for i in range(5): add(i,affected_employee_id=users[0].id)
    assert rows()[0]['volumen'] is None
    for i in range(5,10): add(i,scope='ENTORNO',affected_employee_id=None,category_id=4)
    assert rows()[1]['volumen']==5
    add(10,category_id=4)
    assert rows()[1]['volumen'] is None

def test_confidential_active_relations_and_manager_affected_never_export(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    for i in range(5): add(i,is_confidential=True)
    for i in range(5,10):
        case=add(i); db.add(IncidentParticipant(incidencia_id=case.id,user_id=users[20].id,declaration_reason='Simulado'))
    for i in range(10,15): add(i,affected_employee_id=manager.id)
    assert rows()==[]

def test_confirmed_relation_excluded_discarded_releases_and_current_confidentiality_rechecked(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    cases=[add(i) for i in range(5)]
    relation=IncidentParticipant(incidencia_id=cases[0].id,user_id=users[20].id,declaration_reason='Simulado',review_status='CONFIRMADO',reviewed_by=manager.id,reviewed_at=info['corte'],review_reason='Simulado')
    db.add(relation); assert rows()[0]['volumen'] is None
    relation.review_status='DESCARTADO'; assert rows()[0]['volumen']==5
    cases[0].is_confidential=True; assert rows()[0]['volumen'] is None

def test_complementary_suppression_hides_whole_cell_including_volume(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    for i in range(9): add(i)
    when=info['corte']-timedelta(hours=1)
    add(9,status='RESUELTA',assigned_to=manager.id,priority=2,classification_valid=True,validated_by=manager.id,validated_at=when,cycle_start_at=when-timedelta(hours=2),resolved_at=when,resolution_text='Simulado')
    row=rows()[0]
    assert row['privacidad']=='Suprimido por privacidad' and all(row[k] is None for k in METRICS)
    assert db.scalar(text('SELECT sum(volumen) FROM analytics.incident_metrics WHERE departamento_id=:id'),{'id':dep.id}) is None

def test_known_metrics_multiple_cycles_and_historical_department(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    span=info['corte']-info['periodo_inicio']
    old=info['periodo_inicio']+span/4; reopened=info['periodo_inicio']+span/2
    latest=info['periodo_inicio']+span*0.75
    cases=[]
    for i in range(20):
        changes=dict(assigned_to=manager.id,priority=2,classification_valid=True,validated_by=manager.id,validated_at=latest)
        if i<10:
            changes.update(status='RESUELTA',cycle_start_at=latest-timedelta(hours=6),resolved_at=latest,resolution_text='Simulado',ai_status='COMPLETADA',ai_suggestion={'result':'CLASIFICADA','category_id':2 if i<5 else 3})
        else:
            changes.update(status='EN_REVISION',cycle_start_at=reopened,ai_status='OMITIDA' if i<15 else 'FALLIDA',ai_skip_reason='QA' if i<15 else None)
        case=add(i,**changes); cases.append(case)
        if i>=10:
            db.add(AuditEvent(incidencia_id=case.id,usuario_id=manager.id,accion='REAPERTURA',fecha=reopened,detalle={'before':{'resolved_at':old.isoformat(),'cycle_start_at':(old-timedelta(hours=2)).isoformat()}}))
    # Un caso resuelto tuvo dos reaperturas: se cuenta una sola vez.
    for stamp in (reopened,reopened+span/10):
        db.add(AuditEvent(incidencia_id=cases[0].id,usuario_id=manager.id,accion='REAPERTURA',fecha=stamp,detalle={'before':{'resolved_at':old.isoformat(),'cycle_start_at':(old-timedelta(hours=2)).isoformat()}}))
    # Un evento posterior al corte no altera el indicador.
    db.add(AuditEvent(incidencia_id=cases[1].id,usuario_id=manager.id,accion='REAPERTURA',fecha=info['corte']+timedelta(days=1),detalle={}))
    users[0].departamento_id=second.id
    row=rows()[0]
    assert row['volumen']==20 and row['departamento_id']==dep.id
    assert row['resolucion_casos']==10 and float(row['resolucion_horas'])==6
    assert row['reapertura_poblacion']==20 and row['reapertura_casos']==11 and float(row['reapertura_porcentaje'])==55
    assert row['concordancia_poblacion']==10 and row['concordancia_coincidencias']==5 and float(row['concordancia_porcentaje'])==50
    assert row['ia_omitida']==5 and row['ia_fallida']==5
    assert row['mes_creacion'].month==12  # Cohorte anterior; periodo de resolución anual explícito.
    assert 'descripcion' not in row and 'id' not in row and 'affected_employee_id' not in row

def test_report_login_has_only_aggregate_select_and_cannot_change_existing_roles(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    for i in range(5): add(i)
    name='qa_bi_'+uuid4().hex[:12]
    provision(conn,name,'Synthetic-Password-Only-123456')
    db.execute(text('SET LOCAL ROLE '+name))
    assert db.scalar(text('SELECT volumen FROM analytics.incident_metrics WHERE departamento_id=:dep'),{'dep':dep.id})==5
    db.execute(text('RESET ROLE'))
    for statement in ('SELECT * FROM public.incidencias','SELECT * FROM public.users','SELECT * FROM public.historial_incidencias','SELECT * FROM public.ai_jobs','SELECT * FROM public.mail_deliveries','DELETE FROM analytics.incident_metrics','CREATE TABLE analytics.evil(id integer)'):
        with pytest.raises(DBAPIError):
            with conn.begin_nested():
                db.execute(text('SET LOCAL ROLE '+name)); db.execute(text(statement))
    with pytest.raises(ReportingAccessError,match='ya existe'): provision(conn,name,'Another-Synthetic-Password-123456')

def test_public_privilege_misconfiguration_rolls_back_new_login(world):
    db,conn,*_=world
    # Ensayo en transacción revertida: la provisión detecta un permiso PUBLIC inseguro.
    db.execute(text('GRANT SELECT ON public.incidencias TO PUBLIC'))
    name='qa_bi_'+uuid4().hex[:12]
    with pytest.raises(ReportingAccessError,match='PUBLIC'):
        with conn.begin_nested(): provision(conn,name,'Synthetic-Password-Only-123456')
    assert not db.scalar(text('SELECT 1 FROM pg_roles WHERE rolname=:name'),{'name':name})


def test_powerbi_single_select_keeps_metadata_for_empty_population_and_never_imports_raw(world):
    from pathlib import Path
    db,conn,dep,second,users,manager,info,add,rows=world
    query=(Path(__file__).resolve().parents[2]/'powerbi/consulta.sql').read_text(encoding='utf-8')
    empty=db.execute(text(query)).mappings().all()
    assert len(empty)==1 and empty[0]['privacidad']=='Sin datos'
    assert empty[0]['volumen'] is None and empty[0]['corte_consulta']==info['corte']
    for i in range(5): add(i)
    db.flush()
    result=db.execute(text(query)).mappings().one()
    assert result['volumen']==5 and result['corte_consulta']==info['corte']
    assert not {'id','email','descripcion','resolution_text','affected_employee_id'} & set(result.keys())


def test_future_audit_snapshot_does_not_enter_resolution_population(world):
    db,conn,dep,second,users,manager,info,add,rows=world
    past=info['periodo_inicio']+(info['corte']-info['periodo_inicio'])/2
    for i in range(5):
        case=add(i)
        db.add(AuditEvent(incidencia_id=case.id,usuario_id=manager.id,accion='REAPERTURA',fecha=info['corte']+timedelta(days=1),detalle={'before':{'resolved_at':past.isoformat()}}))
    row=rows()[0]
    assert row['volumen']==5 and row['reapertura_poblacion']==0 and row['reapertura_estado']=='Sin datos'
