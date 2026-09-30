import pytest
from fastapi.testclient import TestClient


def test_home_returns_success(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200


def test_home_returns_greeting(client: TestClient) -> None:
    response = client.get("/")

    assert response.json() == {"message": "Olá, Sistemas Distribuídos!"}


def test_home_returns_json(client: TestClient) -> None:
    response = client.get("/")

    assert response.headers["content-type"].startswith("application/json")


@pytest.mark.parametrize("path", ["/missing", "/health", "/api/unknown"])
def test_unknown_routes_return_not_found(
    client: TestClient, path: str
) -> None:
    response = client.get(path)

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}