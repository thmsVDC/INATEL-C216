import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.routes.games import get_flag_provider, get_game_service
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
def client() -> TestClient:
    service = GameService()
    provider = FakeFlagProvider()

    app.dependency_overrides[get_game_service] = lambda: service
    app.dependency_overrides[get_flag_provider] = lambda: provider

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()