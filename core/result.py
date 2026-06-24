from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class OperationResult:
    success: bool
    data: Any | bytes | None = None
    error: Exception | None = None
    message: str = ""

