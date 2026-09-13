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
    db_event = ErrorEventModel(
        type=event.type,
        message=event.message,
        timestamp=event.timestamp,
        app_name=event.app_name,
        environment=event.environment,
        stack_trace=event.stack_trace,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return {
        "status": "received",
        "event_id": db_event.id,
    }