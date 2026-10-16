from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Game


class GameRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, limit: int) -> list[Game]:
        statement = select(Game).order_by(Game.id).limit(limit)
        return list(self.session.scalars(statement).all())

    def get(self, game_id: int) -> Game | None:
        return self.session.get(Game, game_id)

    def create(self, **values: object) -> Game:
        game = Game(**values)
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def save(self, game: Game) -> Game:
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def delete(self, game: Game) -> None:
        self.session.delete(game)
        self.session.commit()
