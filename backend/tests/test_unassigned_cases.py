"""Bandeja sin responsable: predicado compartido de filas/total y visibilidad."""
from uuid import UUID
import pytest
from app.models import Incident
from test_incidents import world, create


@pytest.fixture
def queue_cases(world):
    client, db, actors, selected, *_ = world
    selected["user"] = actors["employee"]
    own = create(client, titulo="Bandeja coincidencia")
    assigned = create(client, titulo="Bandeja coincidencia asignado")
    db.get(Incident, UUID(assigned)).assigned_to = actors["super"].id
    db.commit()
    selected["user"] = actors["peer"]
    peer = create(client, titulo="Caso par")
    selected["user"] = actors["outsider"]
    outsider = create(client, titulo="Caso otro departamento")
    selected["user"] = actors["employee"]
    confidential = create(client, titulo="Caso confidencial", is_confidential=True)
    conflict = create(client, titulo="Caso con gestor declarado", participants=[
        {"user_id": str(actors["admin"].id), "declaration_reason": "Conflicto ficticio"}])
    return world, {"own": own, "assigned": assigned, "peer": peer,
                   "outsider": outsider, "confidential": confidential, "conflict": conflict}


@pytest.mark.parametrize("actor,expected", [
    ("employee", {"own"}),
    ("super", {"own", "peer"}),
    ("admin", {"own", "peer", "outsider", "confidential"}),
    ("admin2", {"own", "peer", "outsider", "confidential", "conflict"}),
])
def test_unassigned_rows_and_total_obey_access(queue_cases, actor, expected):
    (client, _, actors, selected, *_), cases = queue_cases
    selected["user"] = actors[actor]
    response = client.get("/incidents", params={"unassigned": "true"})
    assert response.status_code == 200, response.text
    page = response.json()
    assert page["total"] == len(expected)
    assert {item["id"] for item in page["items"]} == {cases[key] for key in expected}


def test_unassigned_pagination_keeps_authorized_total_on_empty_page(queue_cases):
    (client, _, actors, selected, *_), _ = queue_cases
    selected["user"] = actors["admin"]
    first = client.get("/incidents", params={"unassigned": True, "page_size": 1}).json()
    assert len(first["items"]) == 1 and first["total"] == 4
    empty = client.get("/incidents", params={"unassigned": True, "page_size": 1, "page": 99}).json()
    assert empty["items"] == [] and empty["total"] == 4


def test_unassigned_combines_with_search_and_status(queue_cases):
    (client, _, actors, selected, *_), cases = queue_cases
    selected["user"] = actors["admin"]
    page = client.get("/incidents", params={
        "unassigned": True, "q": "Bandeja coincidencia", "status": "PENDIENTE"}).json()
    assert page["total"] == 1 and [item["id"] for item in page["items"]] == [cases["own"]]


def test_unassigned_rejects_conflicting_or_invalid_filter(queue_cases):
    (client, _, actors, selected, *_), _ = queue_cases
    selected["user"] = actors["admin"]
    assert client.get("/incidents", params={
        "unassigned": True, "assigned_to": str(actors["super"].id)}).status_code == 422
    assert client.get("/incidents", params={"unassigned": "invalid"}).status_code == 422


def test_default_and_assigned_filter_are_unchanged(queue_cases):
    (client, _, actors, selected, *_), cases = queue_cases
    selected["user"] = actors["admin"]
    default = client.get("/incidents").json()
    explicit_false = client.get("/incidents", params={"unassigned": False}).json()
    assert default == explicit_false and default["total"] == 5
    assigned = client.get("/incidents", params={"assigned_to": str(actors["super"].id)}).json()
    assert assigned["total"] == 1 and assigned["items"][0]["id"] == cases["assigned"]
