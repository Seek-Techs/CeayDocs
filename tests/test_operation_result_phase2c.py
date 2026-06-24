from __future__ import annotations

from core.result import OperationResult


def test_operation_result_defaults():
    r = OperationResult(success=True)
    assert r.success is True
    assert r.data is None
    assert r.error is None
    assert r.message == ""


def test_operation_result_fields():
    r = OperationResult(success=False, message="Failed", error=RuntimeError("x"))
    assert r.success is False
    assert r.message == "Failed"
    assert isinstance(r.error, RuntimeError)

