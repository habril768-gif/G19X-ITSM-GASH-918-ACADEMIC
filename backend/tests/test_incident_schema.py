from datetime import date, datetime, timezone
from io import StringIO
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Base, Category, Department, Incident, IncidentParticipant, Role, User

@pytest.fixture
def records():
    engine=create_engine("sqlite://")
    @event.listens_for(engine,"connect")
    def fk(connection,_):
        connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add(Role(id=1,nombre="ADMIN_RH"))
        dep=Department(nombre="QA",is_active=True)
        db.add(dep); db.flush()
        user=User(email="one@example.invalid",nombre_completo="QA Uno",departamento_id=dep.id,rol_id=1,is_active=True)
        reviewer=User(email="two@example.invalid",nombre_completo="QA Dos",departamento_id=dep.id,rol_id=1,is_active=True)
        db.add_all([user,reviewer,Category(id=4,nombre="Riesgos",descripcion="QA"),Category(id=2,nombre="Conflictos",descripcion="QA")]);db.commit()
        yield db,dep,user,reviewer
    engine.dispose()

def new_case(dep,user,**changes):
    values=dict(titulo="Caso simulado",descripcion="Dato ficticio",incident_date=date(2026,10,16),created_by=user.id,affected_employee_id=user.id,department_id_at_creation=dep.id,reported_department_id=dep.id)
    values.update(changes)
    return Incident(**values)

@pytest.mark.parametrize("changes",[
    {"scope":"PERSONA","affected_employee_id":None},
    {"scope":"ENTORNO"},
    {"scope":"ENTORNO","affected_employee_id":None,"category_id":2},
    {"scope":"INVALIDO"},
    {"classification_valid":True},
    {"ai_status":"OMITIDA","ai_skip_reason":" "},
    {"ai_input_reviewed_at":datetime.now(timezone.utc)},
])
def test_invalid_combinations_rejected(records,changes):
    db,dep,user,_=records
    db.add(new_case(dep,user,**changes))
    with pytest.raises(IntegrityError):db.flush()
    db.rollback()

def test_environment_and_manual_classification_possible(records):
    db,dep,user,_=records
    case=new_case(dep,user,scope="ENTORNO",affected_employee_id=None,category_id=4,ai_status="OMITIDA",ai_skip_reason="Confidencial; atención manual")
    db.add(case);db.commit()
    assert case.affected_employee_id is None
    assert case.classification_valid is False

def test_review_can_be_invalidated_but_resolution_requires_revalidation(records):
    db,dep,user,_=records
    case=new_case(dep,user,status="EN_REVISION",assigned_to=user.id,category_id=4,priority=2,cycle_start_at=datetime.now(timezone.utc),validated_by=user.id,validated_at=datetime.now(timezone.utc),classification_valid=False)
    db.add(case);db.commit()
    case.status="RESUELTA";case.resolution_text="Resuelto en prueba";case.resolved_at=datetime.now(timezone.utc)
    with pytest.raises(IntegrityError):db.flush()
    db.rollback()
    case.classification_valid=True;case.status="RESUELTA";case.resolution_text="Resuelto en prueba";case.resolved_at=datetime.now(timezone.utc)
    db.commit()
    assert case.status=="RESUELTA"

@pytest.mark.parametrize("review",["self","missing_reason","missing_declaration"])
def test_participant_invalid_reviews_rejected(records,review):
    db,dep,user,reviewer=records
    case=new_case(dep,user);db.add(case);db.flush()
    values=dict(incidencia_id=case.id,user_id=user.id,declaration_reason="Participación simulada",review_status="CONFIRMADO",reviewed_by=reviewer.id,reviewed_at=datetime.now(timezone.utc),review_reason="Revisión QA")
    if review=="self":values["reviewed_by"]=user.id
    if review=="missing_reason":values["review_reason"]=" "
    if review=="missing_declaration":values["declaration_reason"]=" "
    db.add(IncidentParticipant(**values))
    with pytest.raises(IntegrityError):db.flush()
    db.rollback()

def test_participant_independent_review_keeps_declaration(records):
    db,dep,user,reviewer=records
    case=new_case(dep,user);db.add(case);db.flush()
    row=IncidentParticipant(incidencia_id=case.id,user_id=user.id,declaration_reason="Motivo original")
    db.add(row);db.commit()
    assert row.review_status=="DECLARADO"
    with db.no_autoflush:
        row.reviewed_by=reviewer.id
        row.review_status="DESCARTADO"
        row.reviewed_at=datetime.now(timezone.utc)
        row.review_reason="Relación corregida"
    db.commit()
    assert row.declaration_reason=="Motivo original"

def test_migration_0003_is_frozen_and_compiles_offline():
    config=Config(str(Path(__file__).resolve().parents[1]/"alembic.ini"),output_buffer=StringIO())
    command.upgrade(config,"0002:0003",sql=True)
    sql=config.output_buffer.getvalue()
    assert "reported_department_id = department_id_at_creation" in sql
    assert "CREATE TABLE incident_involved_users" in sql
    assert "DROP TABLE" not in sql
    assert "classification_valid = true WHERE validated_by IS NOT NULL" in sql
