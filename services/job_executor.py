from __future__ import annotations

from typing import Any, Callable

from core.metrics import get_metrics_collector
from core.result import OperationResult
from core.telemetry import elapsed_time
from models.operation_request import OperationRequest


class JobExecutor:
    """Execute an OperationRequest using a provided operation handler.

    This wraps existing adapter calls via dependency injection.
    """

    def __init__(
        self,
        operation_handler: Callable[[OperationRequest], Any],
    ) -> None:
        self._handler = operation_handler

    def execute(self, request: OperationRequest) -> OperationResult:
        collector = get_metrics_collector()
        op_name = request.operation_type

        with collector.track(operation=op_name):
            try:
                with elapsed_time(f"job_executor.operation={op_name}"):
                    data = self._handler(request)
                return OperationResult(success=True, data=data, message="Operation completed")
            except Exception as e:  # noqa: BLE001
                # Never leak internals in message.
                return OperationResult(
                    success=False,
                    data=None,
                    error=e,
                    message=f"Operation failed: {type(e).__name__}",
                )

