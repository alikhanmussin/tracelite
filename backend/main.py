import hashlib
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import ErrorEventModel



app = FastAPI()

Base.metadata.create_all(bind=engine)


class ErrorEvent(BaseModel):
    type: str
    message: str
    timestamp: str
    app_name: str
    environment: str
    stack_trace: str

def create_fingerprint(event: ErrorEvent) -> str:
    fingerprint_source = (
        f"{event.app_name}|"
        f"{event.environment}|"
        f"{event.type}|"
        f"{event.message}"
    )

    return hashlib.sha256(
        fingerprint_source.encode("utf-8")
    ).hexdigest()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "TraceLite API is running"}


@app.post("/events")
def receive_event(
    event: ErrorEvent,
    db: Session = Depends(get_db),
):
    fingerprint = create_fingerprint(event)

    existing_event = (
        db.query(ErrorEventModel)
        .filter(ErrorEventModel.fingerprint == fingerprint)
        .first()
    )

    if existing_event:
        existing_event.occurrence_count += 1
        existing_event.timestamp = event.timestamp
        existing_event.stack_trace = event.stack_trace

        db.commit()
        db.refresh(existing_event)

        return {
            "status": "grouped",
            "event_id": existing_event.id,
            "occurrence_count": existing_event.occurrence_count,
        }

    db_event = ErrorEventModel(
        type=event.type,
        message=event.message,
        timestamp=event.timestamp,
        app_name=event.app_name,
        environment=event.environment,
        stack_trace=event.stack_trace,
        fingerprint=fingerprint,
        occurrence_count=1,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {
        "status": "received",
        "event_id": db_event.id,
        "occurrence_count": db_event.occurrence_count,
    }