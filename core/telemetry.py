from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Generator, TypeVar, cast

from .logger import get_logger

_T = TypeVar("_T")
logger = get_logger(__name__)


@dataclass
class Elapsed:
    seconds: float


def measure_time(fn: Callable[..., _T]) -> Callable[..., _T]:
    """Decorator to measure execution time and emit a debug log."""

    def wrapper(*args: Any, **kwargs: Any) -> _T:
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            logger.info("%s executed in %.3fs", getattr(fn, "__name__", "<fn>"), elapsed)

    return cast(Callable[..., _T], wrapper)


@contextmanager
def elapsed_time(operation: str) -> Generator[Elapsed, None, None]:
    start = time.perf_counter()
    try:
        yield Elapsed(seconds=0.0)
    finally:
        end = time.perf_counter()
        total = end - start
        logger.info("operation=%s elapsed=%.3fs", operation, total)

