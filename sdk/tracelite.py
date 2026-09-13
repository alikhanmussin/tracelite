from datetime import datetime, timezone
import traceback


def capture_exception(exc: Exception):
    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stack_trace": "".join(
            traceback.format_exception(
                type(exc),
                exc,
                exc.__traceback__,
            )
        ),
    }