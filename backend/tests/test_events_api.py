def test_event_crud_persists_and_supports_filters(client, event_payload):
    created_response = client.post("/api/v1/events", json=event_payload)

    assert created_response.status_code == 201
    created = created_response.json()
    assert created["title"] == event_payload["title"]
    assert created["id"] > 0

    listed = client.get("/api/v1/events?q=distribuidos&category=tecnologia")
    assert listed.status_code == 200
    assert [event["id"] for event in listed.json()] == [created["id"]]

    updated_payload = {**event_payload, "title": "Encontro atualizado"}
    updated = client.put(
        f"/api/v1/events/{created['id']}",
        json=updated_payload,
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Encontro atualizado"

    fetched = client.get(f"/api/v1/events/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Encontro atualizado"

    deleted = client.delete(f"/api/v1/events/{created['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/events/{created['id']}").status_code == 404


def test_event_validation_and_missing_event(client, event_payload):
    invalid_payload = {**event_payload, "capacity": 0}
    assert client.post("/api/v1/events", json=invalid_payload).status_code == 422

    naive_date_payload = {
        **event_payload,
        "starts_at": "2026-12-10T19:00:00",
    }
    assert client.post("/api/v1/events", json=naive_date_payload).status_code == 422
    assert client.get("/api/v1/events/9999").status_code == 404


def test_filter_rejects_inverted_date_range(client):
    response = client.get(
        "/api/v1/events?starts_after=2026-12-20T09:00:00-03:00"
        "&starts_before=2026-12-10T09:00:00-03:00"
    )

    assert response.status_code == 422
