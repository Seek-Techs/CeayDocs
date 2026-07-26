from __future__ import annotations

from models.job import Job, JobStatus
from models.operation_request import OperationRequest
from models.operation_types import OperationType
from services.workflow import make_single_operation_workflow


def test_operation_request_default_structures():
    req = OperationRequest(operation_type=OperationType.PDF_TO_WORD)
    assert req.parameters == {}
    assert req.inputs == {}


def test_job_model_defaults():
    job = Job(id="1", operation_type=OperationType.PDF_TO_WORD, status="PENDING")
    assert job.started_at is None
    assert job.completed_at is None
    assert job.error is None


def test_workflow_runs_operation_handler_success():
    def handler(req: OperationRequest):
        return {"op": req.operation_type, "x": req.inputs.get("x")}

    wf = make_single_operation_workflow(handler)
    req = OperationRequest(operation_type=OperationType.PDF_TO_WORD, inputs={"x": 123})

    result = wf.run(req)
    assert result.success is True
    assert result.data["x"] == 123


def test_workflow_runs_operation_handler_failure():
    def handler(req: OperationRequest):
        raise RuntimeError("boom")

    wf = make_single_operation_workflow(handler)
    req = OperationRequest(operation_type=OperationType.PDF_TO_WORD)

    result = wf.run(req)
    assert result.success is False
    assert result.data is None
    assert result.error is not None

