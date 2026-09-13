from datetime import datetime, timezone
import traceback


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