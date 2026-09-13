from datetime import datetime


def capture_exception(exc: Exception):
    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "timestamp": datetime.utcnow().isoformat(),
    }