from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Generator

from core.logger import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class MetricEvent:
    operation: str
    success: bool
    duration_s: float
    file_size_bytes: int | None = None
    extra: dict[str, Any] | None = None


class MetricsCollector:
    """Lightweight in-process metrics.

    No external telemetry; events are recorded in memory for tests
    and optionally logged.
    """

    def __init__(self, log: bool = True):
        self._events: list[MetricEvent] = []
        self._log = log

    @property
    def events(self) -> list[MetricEvent]:
        return list(self._events)

    @contextmanager
    def track(self, *, operation: str, file_size_bytes: int | None = None) -> Generator[Any, None, None]:
        start = time.perf_counter()
        success = False
        try:
            yield
            success = True
        finally:
            duration = time.perf_counter() - start
            event = MetricEvent(
                operation=operation,
                success=success,
                duration_s=duration,
                file_size_bytes=file_size_bytes,
            )
            self._events.append(event)
            if self._log:
                logger.info(
                    "metrics operation=%s success=%s duration=%.3fs file_size_bytes=%s",
                    operation,
                    success,
                    duration,
                    file_size_bytes,
                )


_default_collector = MetricsCollector(log=True)


def track_operation_metrics(operation: str, *, file_size_bytes: int | None = None):
    """Convenience wrapper around the default collector."""

    return _default_collector.track(operation=operation, file_size_bytes=file_size_bytes)


def get_metrics_collector() -> MetricsCollector:
    return _default_collector

