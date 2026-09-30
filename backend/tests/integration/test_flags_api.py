from fastapi.testclient import TestClient


FLAGS_URL = "/api/v1/flags"


def flag_payload(
    country: str = "Brasil",
    country_code: str = "BR",
    flag_url: str = "https://example.com/br.png",
) -> dict[str, str]:
    return {
        "country": country,
        "country_code": country_code,
        "flag_url": flag_url,
    }


def test_get_flags_accepts_limit_query(client: TestClient) -> None:
    client.post(FLAGS_URL, json=flag_payload("Brasil"))
    client.post(
        FLAGS_URL,
        json=flag_payload("Canadá", "CA", "https://example.com/ca.png"),
    )

    response = client.get(FLAGS_URL, params={"limit": 1})

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_flag_by_id(client: TestClient) -> None:
    created = client.post(FLAGS_URL, json=flag_payload()).json()

    response = client.get(f"{FLAGS_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["country"] == "Brasil"


def test_post_creates_flag(client: TestClient) -> None:
    response = client.post(FLAGS_URL, json=flag_payload())

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["country"] == "Brasil"


def test_put_replaces_flag(client: TestClient) -> None:
    created = client.post(FLAGS_URL, json=flag_payload()).json()

    response = client.put(
        f"{FLAGS_URL}/{created['id']}",
        json=flag_payload("Argentina", "AR", "https://example.com/ar.png"),
    )

    assert response.status_code == 200
    assert response.json()["country"] == "Argentina"
    assert response.json()["country_code"] == "AR"


def test_patch_updates_flag_partially(client: TestClient) -> None:
    created = client.post(FLAGS_URL, json=flag_payload()).json()

    response = client.patch(
        f"{FLAGS_URL}/{created['id']}",
        json={"country": "Portugal"},
    )

    assert response.status_code == 200
    assert response.json()["country"] == "Portugal"
    assert response.json()["country_code"] == "BR"


def test_delete_removes_flag(client: TestClient) -> None:
    created = client.post(FLAGS_URL, json=flag_payload()).json()

    response = client.delete(f"{FLAGS_URL}/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"{FLAGS_URL}/{created['id']}").status_code == 404


def test_get_missing_flag_returns_404(client: TestClient) -> None:
    response = client.get(f"{FLAGS_URL}/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Flag 999 not found"