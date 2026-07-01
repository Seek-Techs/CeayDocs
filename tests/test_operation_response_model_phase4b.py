from __future__ import annotations

from models.operation_response import OperationResponse


def test_operation_response_defaults() -> None:
    r = OperationResponse(success=True)
    assert r.success is True
    assert r.data is None
    assert r.error is None
    assert r.message == ""
    assert r.metadata == {}


def test_operation_response_custom_fields() -> None:
    r = OperationResponse(
        success=False,
        data={"k": 1},
        error="E",
        message="failed",
        metadata={"job_id": "123"},
    )
    assert r.success is False
    assert r.data == {"k": 1}
    assert r.error == "E"
    assert r.message == "failed"
    assert r.metadata == {"job_id": "123"}

