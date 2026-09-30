import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.routes.flags import get_flag_service
from app.services.flag_service import FlagService
from main import app


@pytest.fixture
def client() -> TestClient:
    service = FlagService()
    app.dependency_overrides[get_flag_service] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()