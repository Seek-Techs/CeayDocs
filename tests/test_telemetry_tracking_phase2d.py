from __future__ import annotations

from core.telemetry import elapsed_time


def test_elapsed_time_records_loggable_output():
    # This test ensures telemetry API remains functional.
    with elapsed_time("unit-test-operation") as e:
        assert hasattr(e, "seconds")

