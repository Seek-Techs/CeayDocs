from __future__ import annotations

from datetime import datetime

from services.drawing_register import build_register, infer_discipline


def test_infer_discipline_structural_detail() -> None:
    assert infer_discipline("PLAN") == "STRUCTURAL"
    assert infer_discipline("section") == "STRUCTURAL"
    assert infer_discipline("elevation") == "STRUCTURAL"
    assert infer_discipline("detail") == "STRUCTURAL"


def test_infer_discipline_unknown_general() -> None:
    assert infer_discipline("UNKNOWN") == "GENERAL"


def test_build_register_shapes_and_status_discipline_and_dates(monkeypatch) -> None:
    fixed = datetime(2026, 1, 2, 3, 4, 5)

    class _DT:
        @staticmethod
        def now():
            return fixed

        @staticmethod
        def strftime(*args, **kwargs):
            return fixed.strftime(*args, **kwargs)

    # Monkeypatch datetime in module under test
    import services.drawing_register as dr

    monkeypatch.setattr(dr, "datetime", _DT)

    index = [
        {
            "page": 3,
            "view_type": "PLAN",
            "scale": "1:100",
            "status": "OK",
            "confidence": 0.8,
        },
        {
            "page": 5,
            "view_type": "UNKNOWN",
            "scale": "Unknown",
            "status": "NOT_OK",
            "confidence": None,
        },
    ]

    reg = build_register(index, project_code="ABC", revision="B")
    assert len(reg) == 2

    r0 = reg[0]
    assert r0["drawing_no"] == "ABC-S-003"
    assert r0["title"] == "Plan Drawing"
    assert r0["sheet_no"] == 3
    assert r0["view_type"] == "PLAN"
    assert r0["scale"] == "1:100"
    assert r0["revision"] == "B"
    assert r0["status"] == "FOR CONSTRUCTION"
    assert r0["discipline"] == "STRUCTURAL"
    assert r0["confidence"] == 0.8
    assert r0["source"] == "AUTO"
    assert r0["created_on"] == "2026-01-02"

    r1 = reg[1]
    assert r1["discipline"] == "GENERAL"
    assert r1["status"] == "FOR REVIEW"

