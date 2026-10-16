"""Pruebas del contrato de disponibilidad y documentación de arranque."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_contract():
    with TestClient(create_app()) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("application/json")
        assert response.json() == {"status": "ok", "service": "plurione-api"}


def test_openapi_publishes_health_schema():
    with TestClient(create_app()) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        endpoint = schema["paths"]["/health"]["get"]
        assert endpoint["responses"]["200"]["content"]["application/json"]["schema"] == {
            "$ref": "#/components/schemas/HealthResponse"
        }
        assert "/incidencias" not in schema["paths"]


def test_docs_are_available():
    with TestClient(create_app()) as client:
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "/openapi.json" in response.text
