from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OperationResponse:
    """A future-ready domain model for operation outputs."""

    success: bool
    data: Any = None
    error: str | None = None
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

