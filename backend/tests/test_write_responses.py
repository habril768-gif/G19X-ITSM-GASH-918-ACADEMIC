"""Respuestas de escritura con expiración real y fallos transaccionales."""
from contextlib import contextmanager
from uuid import UUID

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import SQLAlchemyError

from app.api.incidents import CaseDetail, ContentInput
from app.models import AuditEvent, Incident, MailDelivery
from app.services.lifecycle import manage_case
from test_incidents import create, payload, world


@contextmanager
def watch_committed_sql(db):
    engine = db.get_bind()
    state = {"commits": 0, "after_commit_sql": []}
    previous = db.expire_on_commit
    db.expire_on_commit = True

    def committed(session):
        state["commits"] += 1

    def query(conn, cursor, statement, parameters, context, executemany):
        if state["commits"]:
            state["after_commit_sql"].append(statement)

    event.listen(db, "after_commit", committed)
    event.listen(engine, "before_cursor_execute", query)
    try:
        yield state
    finally:
        event.remove(engine, "before_cursor_execute", query)
        event.remove(db, "after_commit", committed)
        db.expire_on_commit = previous


def counts(db):
    return tuple(db.scalar(select(func.count()).select_from(model))
                 for model in (Incident, AuditEvent, MailDelivery))


@pytest.mark.parametrize("actor,confidential,visible", [
    ("employee", False, True), ("employee", True, False), ("admin", False, True),
])
def test_receipt_needs_no_sql_after_commit(world, actor, confidential, visible):
    c, db, actors, selected, one, two = world
    selected["user"] = actors[actor]
    body = payload(is_confidential=confidential)
    if actor == "admin":
        body["affected_employee_id"] = str(actors["employee"].id)
    with watch_committed_sql(db) as observed:
        response = c.post("/incidents", json=body)
    assert response.status_code == 201, response.text
    assert observed == {"commits": 1, "after_commit_sql": []}
    receipt = response.json()
    assert set(receipt) == {"id", "received", "can_view"}
    assert receipt["received"] is True and receipt["can_view"] is visible
    assert db.get(Incident, UUID(receipt["id"])) is not None


@pytest.mark.parametrize("operation", ["classification", "assignment", "content", "transition"])
def test_detail_response_needs_no_sql_after_commit(world, operation):
    c, db, actors, selected, one, two = world
    cid = create(c)
    selected["user"] = actors["admin"]
    manager_id = str(actors["admin"].id)
    if operation == "transition":
        # Preparar un estado válido por las rutas reales antes de observar SQL.
        classified = c.put(f"/incidents/{cid}/classification", json={"category_id": 4, "priority": 3})
        assert classified.status_code == 200, classified.text
        assigned = c.put(f"/incidents/{cid}/assignment", json={"assigned_to": manager_id})
        assert assigned.status_code == 200, assigned.text
    body = {
        "classification": {"category_id": 4, "priority": 3},
        "assignment": {"assigned_to": manager_id},
        "content": {"titulo": "Título corregido", "descripcion": "Descripción corregida"},
        "transition": {"status": "EN_REVISION"},
    }[operation]
    path = f"/incidents/{cid}/" + ("transitions" if operation == "transition" else operation)
    with watch_committed_sql(db) as observed:
        response = c.request("POST" if operation == "transition" else "PUT", path, json=body)
    assert response.status_code == 200, response.text
    assert observed == {"commits": 1, "after_commit_sql": []}
    result = response.json()
    assert set(result) == set(CaseDetail.model_fields)
    assert result["id"] == cid
    if operation == "classification":
        assert result["classification_valid"] is True and result["priority"] == 3
    elif operation == "assignment":
        assert result["assigned_to"] == manager_id
    elif operation == "content":
        assert result["titulo"] == body["titulo"]
        assert result["descripcion"] == body["descripcion"]
        assert result["classification_valid"] is False
    else:
        assert result["status"] == "EN_REVISION"
    # La respuesta representa la fila confirmada; no se exponen campos internos.
    persisted = CaseDetail.model_validate(db.get(Incident, UUID(cid))).model_dump(mode="json")
    for field in result:
        if field not in {"created_at", "validated_at", "resolved_at", "closed_at"}:
            assert result[field] == persisted[field]


@pytest.mark.parametrize("operation", ["create", "edit"])
def test_commit_failure_returns_no_success_and_rolls_back(world, monkeypatch, operation):
    c, db, actors, selected, one, two = world
    cid = create(c) if operation == "edit" else None
    selected["user"] = actors["admin"]
    creation_body = payload(affected_employee_id=str(actors["employee"].id))
    before = counts(db)

    def fail_commit():
        raise SQLAlchemyError("Fallo de commit simulado")

    monkeypatch.setattr(db, "commit", fail_commit)
    with watch_committed_sql(db) as observed:
        if operation == "create":
            response = c.post("/incidents", json=creation_body)
        else:
            response = c.put(f"/incidents/{cid}/content", json={
                "titulo": "No debe persistir", "descripcion": "Cambio simulado"})
    assert response.status_code == 503
    assert observed["commits"] == 0
    assert counts(db) == before
    if cid:
        assert db.get(Incident, UUID(cid)).titulo == "Caso de prueba"


def test_presenter_failure_rolls_back_case_audit_and_outbox(world):
    c, db, actors, selected, one, two = world
    cid = UUID(create(c))
    before = counts(db)

    def broken_presenter(case):
        assert case.titulo == "No debe persistir"
        raise ValueError("Fallo de esquema simulado")

    with pytest.raises(ValueError, match="Fallo de esquema"):
        manage_case(db, actors["admin"], cid, "content", ContentInput(
            titulo="No debe persistir", descripcion="Cambio simulado"), presenter=broken_presenter)
    assert counts(db) == before
    assert db.get(Incident, cid).titulo == "Caso de prueba"


def test_service_default_still_returns_orm(world):
    c, db, actors, selected, one, two = world
    cid = UUID(create(c))
    result = manage_case(db, actors["admin"], cid, "content", ContentInput(
        titulo="Cambio compatible", descripcion="Cambio simulado"))
    assert isinstance(result, Incident)
    assert result.id == cid and result.titulo == "Cambio compatible"
