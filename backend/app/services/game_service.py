from app.models import Game
from app.repositories.game_repository import GameRepository
from app.schemas.game import FlagQuestion, GamePatch, GameReplace


class GameNotFoundError(Exception):
    pass


class GameService:
    def __init__(self, repository: GameRepository) -> None:
        self.repository = repository

    def list_games(self, limit: int) -> list[Game]:
        return self.repository.list(limit)

    def get_game(self, game_id: int) -> Game:
        game = self.repository.get(game_id)
        if game is None:
            raise GameNotFoundError(f"Game {game_id} not found")
        return game

    def create_game(self, question: FlagQuestion) -> Game:
        return self.repository.create(
            correct_country=question.correct_country,
            flag_url=question.flag_url,
        )

    def replace_game(self, game_id: int, data: GameReplace) -> Game:
        game = self.get_game(game_id)
        for field, value in data.model_dump().items():
            setattr(game, field, value)
        return self.repository.save(game)

    def patch_game(self, game_id: int, data: GamePatch) -> Game:
        game = self.get_game(game_id)
        updates = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in updates.items():
            setattr(game, field, value)
        return self.repository.save(game)

    @staticmethod
    def is_correct_answer(correct_country: str, answer: str) -> bool:
        return correct_country.strip().casefold() == answer.strip().casefold()

    def submit_guess(
        self,
        game_id: int,
        answer: str,
        next_question: FlagQuestion | None = None,
        finish: bool = False,
    ) -> tuple[Game, bool, str | None]:
        game = self.get_game(game_id)
        is_correct = self.is_correct_answer(game.correct_country, answer)
        correct_country = None

        if is_correct:
            game.score += 1
            game.streak += 1
        else:
            game.streak = 0
            correct_country = game.correct_country

        if finish:
            game.is_active = False
        elif next_question is not None:
            game.correct_country = next_question.correct_country
            game.flag_url = next_question.flag_url

        return self.repository.save(game), is_correct, correct_country

    def delete_game(self, game_id: int) -> None:
        self.repository.delete(self.get_game(game_id))
