def create_event(client, event_payload):
    response = client.post("/api/v1/events", json=event_payload)
    assert response.status_code == 201
    return response.json()


def test_registration_lifecycle_and_capacity(client, event_payload):
    event = create_event(client, event_payload)
    registrations_url = f"/api/v1/events/{event['id']}/registrations"

    first = client.post(
        registrations_url,
        json={
            "participant_name": "  Ana Souza  ",
            "participant_email": "  ANA@EXAMPLE.COM  ",
        },
    )
    assert first.status_code == 201
    first_registration = first.json()
    assert first_registration["participant_name"] == "Ana Souza"
    assert first_registration["participant_email"] == "ana@example.com"

    duplicate = client.post(
        registrations_url,
        json={
            "participant_name": "Ana Souza",
            "participant_email": "ana@example.com",
        },
    )
    assert duplicate.status_code == 409

    second = client.post(
        registrations_url,
        json={
            "participant_name": "Bruno Lima",
            "participant_email": "bruno@example.com",
        },
    )
    assert second.status_code == 201

    full_event = client.post(
        registrations_url,
        json={
            "participant_name": "Carla Reis",
            "participant_email": "carla@example.com",
        },
    )
    assert full_event.status_code == 409

    listed = client.get(registrations_url)
    assert listed.status_code == 200
    assert [row["participant_email"] for row in listed.json()] == [
        "ana@example.com",
        "bruno@example.com",
    ]

    canceled = client.delete(f"{registrations_url}/{first_registration['id']}")
    assert canceled.status_code == 204

    reopened_seat = client.post(
        registrations_url,
        json={
            "participant_name": "Carla Reis",
            "participant_email": "carla@example.com",
        },
    )
    assert reopened_seat.status_code == 201


def test_registration_errors_and_event_cascade(client, event_payload):
    registrations_url = "/api/v1/events/9999/registrations"
    assert client.get(registrations_url).status_code == 404

    event = create_event(client, event_payload)
    base_url = f"/api/v1/events/{event['id']}/registrations"
    created = client.post(
        base_url,
        json={
            "participant_name": "Diego Alves",
            "participant_email": "diego@example.com",
        },
    )
    assert created.status_code == 201
    registration_id = created.json()["id"]

    wrong_registration = client.delete(f"{base_url}/{registration_id + 999}")
    assert wrong_registration.status_code == 404

    invalid_email = client.post(
        base_url,
        json={"participant_name": "Eva Moraes", "participant_email": "inválido"},
    )
    assert invalid_email.status_code == 422

    assert client.delete(f"/api/v1/events/{event['id']}").status_code == 204
    assert client.get(base_url).status_code == 404
