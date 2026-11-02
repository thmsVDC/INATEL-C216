import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.routes.games import get_flag_provider
from app.database import get_db
from app.models import Base
from app.repositories.game_repository import GameRepository
from app.schemas.game import FlagQuestion
from app.services.game_service import GameService
from main import app


class FakeFlagProvider:
    def __init__(self) -> None:
        self.questions = [
            FlagQuestion(
                correct_country="Brasil",
                flag_url="https://example.com/br.png",
            ),
            FlagQuestion(
                correct_country="Canadá",
                flag_url="https://example.com/ca.png",
            ),
        ]
        self.index = 0

    async def get_random_flag(self) -> FlagQuestion:
        question = self.questions[min(self.index, len(self.questions) - 1)]
        self.index += 1
        return question


@pytest.fixture
def db_session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    test_session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    with test_session_factory() as session:
        yield session
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def game_service(db_session: Session) -> GameService:
    return GameService(GameRepository(db_session))


@pytest.fixture
def client(db_session: Session) -> TestClient:
    provider = FakeFlagProvider()

    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_flag_provider] = lambda: provider

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
