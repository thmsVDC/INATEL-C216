from fastapi.testclient import TestClient


GAMES_URL = "/api/v1/games"


def test_post_starts_game_without_revealing_answer(
    client: TestClient,
) -> None:
    response = client.post(GAMES_URL)

    assert response.status_code == 201
    assert response.json()["flag_url"] == "https://example.com/br.png"
    assert response.json()["score"] == 0
    assert "correct_country" not in response.json()


def test_get_games_accepts_limit_query(client: TestClient) -> None:
    client.post(GAMES_URL)
    client.post(GAMES_URL)

    response = client.get(GAMES_URL, params={"limit": 1})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "correct_country" not in response.json()[0]


def test_get_game_by_id_hides_answer(client: TestClient) -> None:
    created = client.post(GAMES_URL).json()

    response = client.get(f"{GAMES_URL}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["flag_url"] == "https://example.com/br.png"
    assert "correct_country" not in response.json()


def test_put_replaces_game(client: TestClient) -> None:
    created = client.post(GAMES_URL).json()
    replacement = {
        "correct_country": "Argentina",
        "flag_url": "https://example.com/ar.png",
        "score": 5,
        "streak": 3,
        "is_active": False,
    }

    response = client.put(
        f"{GAMES_URL}/{created['id']}",
        json=replacement,
    )

    assert response.status_code == 200
    assert response.json()["flag_url"] == "https://example.com/ar.png"
    assert response.json()["score"] == 5
    assert "correct_country" not in response.json()


def test_patch_updates_game_partially(client: TestClient) -> None:
    created = client.post(GAMES_URL).json()

    response = client.patch(
        f"{GAMES_URL}/{created['id']}",
        json={"score": 2},
    )

    assert response.status_code == 200
    assert response.json()["score"] == 2
    assert "correct_country" not in response.json()


def test_correct_guess_advances_to_next_flag(client: TestClient) -> None:
    created = client.post(GAMES_URL).json()

    response = client.post(
        f"{GAMES_URL}/{created['id']}/guess",
        json={"answer": "brasil"},
    )

    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert response.json()["game"]["score"] == 1
    assert response.json()["game"]["streak"] == 1
    assert response.json()["game"]["flag_url"] == "https://example.com/ca.png"
    assert response.json()["correct_country"] is None


def test_wrong_guess_returns_answer_and_resets_streak(
    client: TestClient,
) -> None:
    created = client.post(GAMES_URL).json()

    response = client.post(
        f"{GAMES_URL}/{created['id']}/guess",
        json={"answer": "Chile"},
    )

    assert response.status_code == 200
    assert response.json()["is_correct"] is False
    assert response.json()["correct_country"] == "Brasil"
    assert response.json()["game"]["streak"] == 0


def test_delete_removes_game(client: TestClient) -> None:
    created = client.post(GAMES_URL).json()

    response = client.delete(f"{GAMES_URL}/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"{GAMES_URL}/{created['id']}").status_code == 404


def test_get_missing_game_returns_404(client: TestClient) -> None:
    response = client.get(f"{GAMES_URL}/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game 999 not found"