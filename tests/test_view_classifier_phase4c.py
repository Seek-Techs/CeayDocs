from __future__ import annotations

from unittest.mock import MagicMock

from services.view_classifier import classify_page, classify_pdf_views


def test_classify_page_plan_section_elevation_unknown() -> None:
    page = MagicMock()

    page.get_text.return_value = "This is a FLOOR PLAN layout"
    assert classify_page(page)["view_type"] == "PLAN"

    page.get_text.return_value = "SECTION sec s/s"
    assert classify_page(page)["view_type"] == "SECTION"

    page.get_text.return_value = "ELEVATION front view side view"
    assert classify_page(page)["view_type"] == "ELEVATION"

    page.get_text.return_value = "random text"
    assert classify_page(page)["view_type"] == "UNKNOWN"


def test_classify_pdf_views_iterates_pages_sets_page_and_snippet() -> None:
    class _Page:
        def __init__(self, text: str):
            self._text = text

        def get_text(self, mode: str) -> str:  # noqa: ARG002
            return self._text

    class _Doc(list):
        pass

    # Patch fitz.open so classify_pdf_views runs without real PDFs.
    import services.view_classifier as vc
    
    doc = _Doc([_Page("PLAN"), _Page("SECTION")])
    
    def _open(*args, **kwargs):  # noqa: ANN001
        return doc

    vc.fitz.open = _open  # type: ignore[assignment]

    res = classify_pdf_views(b"pdf")
    assert len(res) == 2
    assert res[0]["page"] == 1
    assert res[1]["page"] == 2

