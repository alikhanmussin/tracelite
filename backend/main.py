from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ErrorEvent(BaseModel):
    type: str
    message: str
    timestamp: str
    app_name: str
    environment: str
    stack_trace: str


@app.get("/")
def root():
    return {"status": "TraceLite API is running"}


@app.post("/events")
def receive_event(event: ErrorEvent):
    return {
        "status": "received",
        "event": event,
    }