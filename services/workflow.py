from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from models.operation_request import OperationRequest
from services.job_executor import JobExecutor


@dataclass(slots=True)
class Workflow:
    """A thin orchestration interface.

    For Phase 3 we only support single-operation execution.
    """

    executor: JobExecutor

    def run(self, request: OperationRequest) -> Any:
        return self.executor.execute(request)


def make_single_operation_workflow(operation_handler: Callable[[OperationRequest], Any]) -> Workflow:
    return Workflow(executor=JobExecutor(operation_handler=operation_handler))

