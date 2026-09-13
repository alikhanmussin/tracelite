from tracelite import capture_exception, send_event

try:
    1 / 0
except Exception as exc:
    event = capture_exception(
        exc,
        app_name="demo-app",
        environment="development",
    )
    response = send_event(event)
    print(response)