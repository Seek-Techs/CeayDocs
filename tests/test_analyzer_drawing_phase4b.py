from __future__ import annotations

import io
from unittest.mock import patch

from services.analyzer import analyze_drawing





def test_analyze_drawing_invalid_input_returns_error_list() -> None:
    result = analyze_drawing(123)  # type: ignore[arg-type]
    assert result["classification"] == {}
    assert result["summary"] == {}
    assert result["pages"] == []
    assert result["split_pdfs"] == {}
    assert result["files"] == []
    assert "errors" in result
    assert any("Failed to read input" in e for e in result["errors"])


def test_analyze_drawing_success_happy_path_builds_index_and_qa() -> None:
    pdf_bytes = b"%PDF-1.4 dummy"

    fake_classification = {"project_type": "structural"}
    fake_views = [
        {"page": 1, "view_type": "PLAN", "confidence": 0.9},
        {"page": 2, "view_type": "SECTION", "confidence": None},
    ]
    fake_scales = [
        {"page": 1, "scale": "1:100"},
        {"page": 2, "scale": "1:25"},
    ]
    fake_splits = {
        "plan": b"plan-bytes",
        "section": b"section-bytes",
    }

    # Stub index generation helpers indirectly through analyzer's imported functions.
    # We only need to ensure downstream functions return deterministic values.
    with (
        patch("services.analyzer.classify_pdf", return_value=fake_classification),
        patch("services.analyzer.classify_pdf_views", return_value=fake_views),
        patch("services.analyzer.detect_scales", return_value=fake_scales),
        patch("services.analyzer.split_views_into_pdfs", return_value=fake_splits),
    ):
        result = analyze_drawing(pdf_bytes)

    assert result["classification"] == fake_classification
    assert result["split_pdfs"] == fake_splits
    assert set(result["files"]) == {"plan", "section"}

    pages = result["pages"]
    assert len(pages) == 2
    assert pages[0]["page"] == 1
    assert pages[0]["view_type"] == "PLAN"
    assert pages[0]["confidence"] == 0.9
    assert pages[0]["scale"] == "1:100"

    # Summary counts: "PLAN @ 1:100" and "SECTION @ 1:25"
    assert result["summary"]["PLAN @ 1:100"] == 1
    assert result["summary"]["SECTION @ 1:25"] == 1

    # analyzer should have index + qa (from drawing_index)
    assert "index" in result
    assert "qa" in result
    assert isinstance(result["qa"], dict)

    # index_csv may be present; it can fail silently. In our controlled case it should exist.
    assert "index_csv" in result
    assert "page,view_type" in result["index_csv"]


def test_analyze_drawing_swallow_csv_generation_exception() -> None:
    pdf_bytes = b"%PDF-1.4 dummy"

    fake_classification = {"project_type": "structural"}
    fake_views = [{"page": 1, "view_type": "PLAN", "confidence": 0.9}]
    fake_scales = [{"page": 1, "scale": "1:100"}]
    fake_splits = {"plan": b"plan-bytes"}

    with (
        patch("services.analyzer.classify_pdf", return_value=fake_classification),
        patch("services.analyzer.classify_pdf_views", return_value=fake_views),
        patch("services.analyzer.detect_scales", return_value=fake_scales),
        patch("services.analyzer.split_views_into_pdfs", return_value=fake_splits),
        patch("services.analyzer.index_to_csv", side_effect=RuntimeError("csv fail")),
    ):
        result = analyze_drawing(pdf_bytes)

    # CSV failure is swallowed: key may be absent, but function should still succeed overall.
    assert result["classification"] == fake_classification
    assert result["split_pdfs"] == fake_splits
    assert "errors" not in result or not any("csv" in e.lower() for e in result.get("errors", []))


def test_analyze_drawing_dependency_exception_records_error() -> None:
    pdf_bytes = b"%PDF-1.4 dummy"

    with (
        patch("services.analyzer.classify_pdf", side_effect=ValueError("bad pdf")),
        patch("services.analyzer.classify_pdf_views", return_value=[]),
        patch("services.analyzer.detect_scales", return_value=[]),
        patch("services.analyzer.split_views_into_pdfs", return_value={}),
    ):
        result = analyze_drawing(pdf_bytes)

    assert result["classification"] == {}
    assert "errors" in result
    assert any("classify_pdf error" in e for e in result["errors"])


def test_analyze_drawing_file_like_input_is_supported() -> None:
    pdf_stream = io.BytesIO(b"%PDF-1.4 dummy")

    with (
        patch("services.analyzer.classify_pdf", return_value={}),
        patch("services.analyzer.classify_pdf_views", return_value=[]),
        patch("services.analyzer.detect_scales", return_value=[]),
        patch("services.analyzer.split_views_into_pdfs", return_value={}),
    ):
        result = analyze_drawing(pdf_stream)

    assert result["pages"] == []
    assert result["split_pdfs"] == {}

