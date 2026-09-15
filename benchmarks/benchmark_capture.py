import sys
from pathlib import Path

# Allow this script to import the TraceLite SDK.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "sdk"))

from tracelite import capture_exception, send_event


def zero_division():
    return 10 / 0


def invalid_integer():
    return int("hello")


def missing_dictionary_key():
    data = {"name": "TraceLite"}
    return data["missing"]


def list_index_error():
    values = [1, 2, 3]
    return values[10]


def type_error():
    return "TraceLite" + 10


def attribute_error():
    value = None
    return value.upper()


def file_not_found():
    with open("this_file_does_not_exist.txt") as file:
        return file.read()


def name_error():
    return variable_that_does_not_exist


def assertion_error():
    assert False, "Simulated assertion failure"


def runtime_error():
    raise RuntimeError("Simulated runtime failure")

def overflow_error():
    raise OverflowError("Simulated overflow")


def not_implemented_error():
    raise NotImplementedError("Simulated unsupported operation")


def import_error():
    raise ImportError("Simulated import failure")


def module_not_found_error():
    raise ModuleNotFoundError("Simulated missing module")


def timeout_error():
    raise TimeoutError("Simulated timeout")


def connection_error():
    raise ConnectionError("Simulated connection failure")


def permission_error():
    raise PermissionError("Simulated permission failure")


def os_error():
    raise OSError("Simulated operating system failure")


def eof_error():
    raise EOFError("Simulated end-of-file condition")


def lookup_error():
    raise LookupError("Simulated lookup failure")


def arithmetic_error():
    raise ArithmeticError("Simulated arithmetic failure")


def floating_point_error():
    raise FloatingPointError("Simulated floating-point failure")


def memory_error():
    raise MemoryError("Simulated memory failure")


def reference_error():
    raise ReferenceError("Simulated reference failure")


def buffer_error():
    raise BufferError("Simulated buffer failure")


def unicode_error():
    raise UnicodeError("Simulated Unicode failure")


def syntax_error():
    raise SyntaxError("Simulated syntax failure")


def recursion_error():
    raise RecursionError("Simulated recursion failure")


def system_error():
    raise SystemError("Simulated system failure")


def stop_iteration():
    raise StopIteration("Simulated iteration completion")

TEST_CASES = [
    ("ZeroDivisionError", zero_division),
    ("ValueError", invalid_integer),
    ("KeyError", missing_dictionary_key),
    ("IndexError", list_index_error),
    ("TypeError", type_error),
    ("AttributeError", attribute_error),
    ("FileNotFoundError", file_not_found),
    ("NameError", name_error),
    ("AssertionError", assertion_error),
    ("RuntimeError", runtime_error),
    ("OverflowError", overflow_error),
    ("NotImplementedError", not_implemented_error),
    ("ImportError", import_error),
    ("ModuleNotFoundError", module_not_found_error),
    ("TimeoutError", timeout_error),
    ("ConnectionError", connection_error),
    ("PermissionError", permission_error),
    ("OSError", os_error),
    ("EOFError", eof_error),
    ("LookupError", lookup_error),
    ("ArithmeticError", arithmetic_error),
    ("FloatingPointError", floating_point_error),
    ("MemoryError", memory_error),
    ("ReferenceError", reference_error),
    ("BufferError", buffer_error),
    ("UnicodeError", unicode_error),
    ("SyntaxError", syntax_error),
    ("RecursionError", recursion_error),
    ("SystemError", system_error),
    ("StopIteration", stop_iteration),
]


successful = 0
failed = 0


for expected_type, trigger_exception in TEST_CASES:
    try:
        trigger_exception()

    except Exception as exc:
        try:
            event = capture_exception(
                exc,
                app_name="tracelite-benchmark",
                environment="benchmark",
            )

            response = send_event(event)

            if (
                event["type"] == expected_type
                and response.get("status") in {"received", "grouped"}
            ):
                successful += 1
                print(f"PASS  {expected_type}")
            else:
                failed += 1
                print(f"FAIL  {expected_type}")

        except Exception as benchmark_error:
            failed += 1
            print(
                f"FAIL  {expected_type} "
                f"({benchmark_error})"
            )


total = len(TEST_CASES)
capture_rate = (successful / total) * 100


print("\nTraceLite Capture Benchmark")
print("---------------------------")
print(f"Successful:   {successful}")
print(f"Failed:       {failed}")
print(f"Total:        {total}")
print(f"Capture rate: {capture_rate:.1f}%")