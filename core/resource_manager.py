from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable

from core.logger import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class RegisteredTempPath:
    path: Path


class ResourceManager:
    """Track temporary file paths and delete them safely.

    This is intentionally minimal to avoid rewrites of existing adapters.
    """

    def __init__(self):
        self._temps: list[RegisteredTempPath] = []

    def register(self, path: str | os.PathLike[str]) -> None:
        p = Path(path)
        self._temps.append(RegisteredTempPath(path=p))

    def cleanup(self) -> None:
        for item in self._temps:
            try:
                item.path.unlink(missing_ok=True)
            except Exception as e:  # noqa: BLE001
                logger.warning("temp cleanup failed path=%s err=%s", item.path, e)

    def __enter__(self) -> "ResourceManager":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.cleanup()


@contextmanager
def managed_temp_paths(paths: Iterable[str | os.PathLike[str]]) -> Generator[Path, None, None]:
    """Register temp paths for cleanup within a context.

    Usage pattern (optional):
      with managed_temp_paths([p1, p2]):
          ...

    Provides ergonomic cleanup without forcing adapter rewrites.
    """

    mgr = ResourceManager()
    for p in paths:
        mgr.register(p)
    try:
        yield Path(".")
    finally:
        mgr.cleanup()


# Backward-compatible alias used by future code
managed_temp_file = None  # type: ignore[assignment]

