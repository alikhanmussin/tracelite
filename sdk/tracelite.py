from datetime import datetime, timezone
import traceback
import json
from urllib import request

def capture_exception(
    exc: Exception,
    app_name: str = "unknown-app",
    environment: str = "development",
):
    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "app_name": app_name,
        "environment": environment,
        "stack_trace": "".join(
            traceback.format_exception(
                type(exc),
                exc,
                exc.__traceback__,
            )
        ),
    }
    
def send_event(event: dict, endpoint: str = "http://127.0.0.1:8000/events"):
    data = json.dumps(event).encode("utf-8")

    req = request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))