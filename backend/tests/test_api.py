from fastapi.testclient import TestClient

from app.main import create_app


def test_register_application_endpoint() -> None:
    client = TestClient(create_app())

    response = client.post("/applications", json={"client_name": "Frontend"})

    assert response.status_code == 201
    body = response.json()
    assert body["client_name"] == "Frontend"
    assert isinstance(body["client_id"], str)
    assert body["client_id"]


def test_register_application_rejects_blank_client_name() -> None:
    client = TestClient(create_app())

    response = client.post("/applications", json={"client_name": "   "})

    assert response.status_code == 422
    assert response.json()["detail"] == "client_name must not be blank"
