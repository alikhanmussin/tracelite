from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_duplicate_events_are_grouped():
    event = {
        "type": "ZeroDivisionError",
        "message": "division by zero",
        "timestamp": "2026-09-14T10:00:00+00:00",
        "app_name": "test-app",
        "environment": "test",
        "stack_trace": "test trace",
    }

    first_response = client.post("/events", json=event)
    second_response = client.post("/events", json=event)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert first_response.json()["occurrence_count"] == 1
    assert second_response.json()["occurrence_count"] == 2

    events_response = client.get("/events")

    assert events_response.status_code == 200

    events = events_response.json()

    assert len(events) == 1
    assert events[0]["type"] == "ZeroDivisionError"
    assert events[0]["occurrence_count"] == 2