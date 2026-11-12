from datetime import UTC

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import set_committed_value
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import Event
from main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def restore_timezone(target, _context=None):
        # SQLite drops timezone offsets from DateTime columns; PostgreSQL keeps them.
        if target.starts_at.tzinfo is None:
            set_committed_value(
                target,
                "starts_at",
                target.starts_at.replace(tzinfo=UTC),
            )

    def restore_timezone_on_refresh(target, _context, _attrs):
        restore_timezone(target)

    event.listen(Event, "load", restore_timezone)
    event.listen(Event, "refresh", restore_timezone_on_refresh)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    event.remove(Event, "load", restore_timezone)
    event.remove(Event, "refresh", restore_timezone_on_refresh)


@pytest.fixture
def event_payload():
    return {
        "title": "Encontro de Sistemas Distribuidos",
        "description": "Palestras e atividades práticas.",
        "category": "Tecnologia",
        "location": "Auditório INATEL",
        "starts_at": "2026-12-10T19:00:00-03:00",
        "capacity": 2,
    }
