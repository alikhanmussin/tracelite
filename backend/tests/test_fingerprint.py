from main import ErrorEvent, create_fingerprint


def test_same_error_produces_same_fingerprint():
    event_1 = ErrorEvent(
        type="ZeroDivisionError",
        message="division by zero",
        timestamp="2026-09-14T10:00:00+00:00",
        app_name="demo-app",
        environment="development",
        stack_trace="trace 1",
    )

    event_2 = ErrorEvent(
        type="ZeroDivisionError",
        message="division by zero",
        timestamp="2026-09-14T11:00:00+00:00",
        app_name="demo-app",
        environment="development",
        stack_trace="trace 2",
    )

    assert create_fingerprint(event_1) == create_fingerprint(event_2)

def test_different_errors_produce_different_fingerprints():
    event_1 = ErrorEvent(
        type="ZeroDivisionError",
        message="division by zero",
        timestamp="2026-09-14T10:00:00+00:00",
        app_name="demo-app",
        environment="development",
        stack_trace="trace 1",
    )

    event_2 = ErrorEvent(
        type="ValueError",
        message="invalid value",
        timestamp="2026-09-14T10:00:00+00:00",
        app_name="demo-app",
        environment="development",
        stack_trace="trace 2",
    )

    assert create_fingerprint(event_1) != create_fingerprint(event_2)

def test_same_error_in_different_environments_has_different_fingerprint():
    event_1 = ErrorEvent(
        type="ZeroDivisionError",
        message="division by zero",
        timestamp="2026-09-14T10:00:00+00:00",
        app_name="demo-app",
        environment="development",
        stack_trace="trace 1",
    )

    event_2 = ErrorEvent(
        type="ZeroDivisionError",
        message="division by zero",
        timestamp="2026-09-14T10:00:00+00:00",
        app_name="demo-app",
        environment="production",
        stack_trace="trace 2",
    )

    assert create_fingerprint(event_1) != create_fingerprint(event_2)