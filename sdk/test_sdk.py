from tracelite import capture_exception


try:
    1 / 0
except Exception as exc:
    event = capture_exception(exc)
    print(event)