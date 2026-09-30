from app.schemas.game import (
    FlagQuestion,
    GamePatch,
    GameReplace,
    GameState,
)


class GameNotFoundError(Exception):
    pass


class GameService:
    def __init__(self) -> None:
        self._games: dict[int, GameState] = {}
        self._next_id = 1

    def list_games(self, limit: int) -> list[GameState]:
        return list(self._games.values())[:limit]

    def get_game(self, game_id: int) -> GameState:
        try:
            return self._games[game_id]
        except KeyError as error:
            raise GameNotFoundError(
                f"Game {game_id} not found"
            ) from error

    def create_game(self, question: FlagQuestion) -> GameState:
        game = GameState(
            id=self._next_id,
            correct_country=question.correct_country,
            flag_url=question.flag_url,
        )
        self._games[game.id] = game
        self._next_id += 1
        return game

    def replace_game(self, game_id: int, data: GameReplace) -> GameState:
        self.get_game(game_id)
        game = GameState(id=game_id, **data.model_dump())
        self._games[game_id] = game
        return game

    def patch_game(self, game_id: int, data: GamePatch) -> GameState:
        current_game = self.get_game(game_id)
        updates = data.model_dump(exclude_unset=True, exclude_none=True)
        updated_game = current_game.model_copy(update=updates)
        self._games[game_id] = updated_game
        return updated_game

    @staticmethod
    def is_correct_answer(correct_country: str, answer: str) -> bool:
        return correct_country.strip().casefold() == answer.strip().casefold()

    def submit_guess(
        self,
        game_id: int,
        answer: str,
        next_question: FlagQuestion | None = None,
    ) -> tuple[GameState, bool, str | None]:
        current_game = self.get_game(game_id)
        is_correct = self.is_correct_answer(
            current_game.correct_country,
            answer,
        )

        if is_correct:
            updates: dict[str, object] = {
                "score": current_game.score + 1,
                "streak": current_game.streak + 1,
            }

            if next_question is not None:
                updates["correct_country"] = next_question.correct_country
                updates["flag_url"] = next_question.flag_url

            updated_game = current_game.model_copy(update=updates)
            correct_country = None
        else:
            updated_game = current_game.model_copy(update={"streak": 0})
            correct_country = current_game.correct_country

        self._games[game_id] = updated_game
        return updated_game, is_correct, correct_country

    def delete_game(self, game_id: int) -> None:
        self.get_game(game_id)
        del self._games[game_id]