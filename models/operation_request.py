from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OperationRequest:
    """A future-ready domain model for requested operations."""

    operation_type: str
    parameters: dict[str, Any] = field(default_factory=dict)
    # Raw payloads are intentionally generic; adapters remain unchanged.
    inputs: dict[str, Any] = field(default_factory=dict)

