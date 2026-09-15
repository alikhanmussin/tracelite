import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib import request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "sdk"))

from tracelite import send_event


API_URL = "http://127.0.0.1:8000"

TOTAL_EVENTS = 100
UNIQUE_ISSUES = 20
REPEATS_PER_ISSUE = TOTAL_EVENTS // UNIQUE_ISSUES

# Unique app name keeps this benchmark separate from previous test data.
BENCHMARK_APP = f"grouping-benchmark-{uuid.uuid4().hex[:8]}"
BENCHMARK_ENVIRONMENT = "benchmark"


def get_events():
    with request.urlopen(f"{API_URL}/events") as response:
        return json.loads(response.read().decode("utf-8"))


print("TraceLite Duplicate Grouping Benchmark")
print("--------------------------------------")
print(f"Sending {TOTAL_EVENTS} events...")
print(f"Unique logical issues: {UNIQUE_ISSUES}")
print(f"Repeats per issue: {REPEATS_PER_ISSUE}")
print()


sent = 0

for issue_number in range(UNIQUE_ISSUES):
    for occurrence in range(REPEATS_PER_ISSUE):
        event = {
            "type": "RuntimeError",
            "message": f"Simulated benchmark issue {issue_number + 1}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "app_name": BENCHMARK_APP,
            "environment": BENCHMARK_ENVIRONMENT,
            "stack_trace": (
                f"Simulated stack trace for issue "
                f"{issue_number + 1}, occurrence {occurrence + 1}"
            ),
        }

        response = send_event(event)

        if response.get("status") not in {"received", "grouped"}:
            raise RuntimeError(
                f"Unexpected API response: {response}"
            )

        sent += 1


all_events = get_events()

benchmark_events = [
    event
    for event in all_events
    if event["app_name"] == BENCHMARK_APP
    and event["environment"] == BENCHMARK_ENVIRONMENT
]

grouped_records = len(benchmark_events)

duplicate_records_removed = sent - grouped_records

reduction_rate = (
    duplicate_records_removed / sent
) * 100


expected_occurrence_count = REPEATS_PER_ISSUE

counts_correct = all(
    event["occurrence_count"] == expected_occurrence_count
    for event in benchmark_events
)


print("Results")
print("-------")
print(f"Events sent:               {sent}")
print(f"Grouped issue records:     {grouped_records}")
print(f"Duplicate records avoided: {duplicate_records_removed}")
print(f"Duplicate reduction:       {reduction_rate:.1f}%")
print(f"Occurrence counts correct: {counts_correct}")