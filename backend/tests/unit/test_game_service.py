import pytest

from app.schemas.game import FlagQuestion, GamePatch, GameReplace
from app.services.game_service import GameNotFoundError, GameService


def question(country: str = "Brasil") -> FlagQuestion:
    return FlagQuestion(
        correct_country=country,
        flag_url=f"https://example.com/{country.lower()}.png",
    )


def test_create_game_sets_initial_state() -> None:
    service = GameService()

    game = service.create_game(question())

    assert game.id == 1
    assert game.correct_country == "Brasil"
    assert game.score == 0
    assert game.streak == 0
    assert game.is_active is True


def test_list_games_respects_limit() -> None:
    service = GameService()
    service.create_game(question("Brasil"))
    service.create_game(question("Canadá"))

    games = service.list_games(limit=1)

    assert len(games) == 1
    assert games[0].correct_country == "Brasil"


def test_replace_game_replaces_all_fields() -> None:
    service = GameService()
    game = service.create_game(question())

    updated = service.replace_game(
        game.id,
        GameReplace(
            correct_country="Argentina",
            flag_url="https://example.com/ar.png",
            score=5,
            streak=3,
            is_active=False,
        ),
    )

    assert updated.correct_country == "Argentina"
    assert updated.score == 5
    assert updated.streak == 3
    assert updated.is_active is False


def test_patch_game_changes_only_requested_fields() -> None:
    service = GameService()
    game = service.create_game(question())

    updated = service.patch_game(game.id, GamePatch(score=2))

    assert updated.score == 2
    assert updated.correct_country == game.correct_country
    assert updated.flag_url == game.flag_url
    assert updated.streak == 0


def test_correct_guess_increments_score_and_streak() -> None:
    service = GameService()
    game = service.create_game(question())

    updated, is_correct, correct_country = service.submit_guess(
        game.id,
        " brasil ",
        next_question=question("Canadá"),
    )

    assert is_correct is True
    assert correct_country is None
    assert updated.score == 1
    assert updated.streak == 1
    assert updated.correct_country == "Canadá"


def test_wrong_guess_resets_streak_and_reveals_answer() -> None:
    service = GameService()
    game = service.create_game(question())
    service.patch_game(game.id, GamePatch(streak=2))

    updated, is_correct, correct_country = service.submit_guess(
        game.id,
        "Chile",
    )

    assert is_correct is False
    assert correct_country == "Brasil"
    assert updated.score == 0
    assert updated.streak == 0


def test_delete_game_removes_it() -> None:
    service = GameService()
    game = service.create_game(question())

    service.delete_game(game.id)

    with pytest.raises(GameNotFoundError):
        service.get_game(game.id)


@pytest.mark.parametrize("game_id", [0, 10])
def test_get_missing_game_raises_error(game_id: int) -> None:
    service = GameService()

    with pytest.raises(GameNotFoundError):
        service.get_game(game_id)