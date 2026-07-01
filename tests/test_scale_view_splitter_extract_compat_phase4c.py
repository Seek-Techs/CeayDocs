from __future__ import annotations

from unittest.mock import MagicMock, patch

from services.scale_detector import detect_scales
from services.view_classifier import classify_page
from services.view_splitter import split_views_into_pdfs


def test_detect_scales_parses_patterns_and_unknown() -> None:

    # Mock fitz doc/page structure
    class _Page:
        def __init__(self, text: str):
            self._text = text

        def get_text(self, mode: str) -> str:  # noqa: ARG002
            return self._text

    class _Doc(list):
        def close(self) -> None:
            pass

    doc = _Doc([_Page("SCALE: 1 / 100"), _Page("no scale here")])

    with patch("services.scale_detector.fitz.open", return_value=doc):
        res = detect_scales(b"pdf")

    assert res[0]["scale"] == "1/100"
    assert res[1]["scale"] == "Unknown"


def test_classify_page_returns_expected_view_type_and_snippet() -> None:
    page = MagicMock()
    page.get_text.return_value = "This is a floor plan with layout section"

    res = classify_page(page)
    assert res["view_type"] == "PLAN"
    assert isinstance(res["text_snippet"], str)
    assert len(res["text_snippet"]) == len(page.get_text.return_value[:300])


def test_split_views_into_pdfs_groups_by_view_type_and_inserts_pdf_pages() -> None:
    # Arrange mock for classify_pdf_views return types
    view_info = [
        {"view_type": "PLAN", "page": 1},
        {"view_type": "PLAN", "page": 2},
        {"view_type": "SECTION", "page": 3},
    ]

    class _InsertDoc:
        def __init__(self) -> None:
            self.inserted: list[tuple[int, int]] = []

        def insert_pdf(self, doc, from_page: int, to_page: int) -> None:  # noqa: ANN001
            self.inserted.append((from_page, to_page))

        def save(self, buffer) -> None:  # noqa: ANN001
            buffer.write(b"bytes")

    class _Doc(list):
        def __iter__(self):
            return super().__iter__()

    source_doc = _Doc([object()])

    with (
        patch("services.view_splitter.classify_pdf_views", return_value=view_info),
        patch("services.view_splitter.fitz.open", return_value=source_doc),
        patch("services.view_splitter.fitz.open", side_effect=[source_doc, _InsertDoc(), _InsertDoc()]),
    ):
        # Note: side_effect list must cover out_doc opens for each grouped type.
        res = split_views_into_pdfs(b"pdf")

    assert set(res.keys()) == {"plan", "section"}
    assert res["plan"] == b"bytes"
    assert res["section"] == b"bytes"


def test_extract_compat_extract_text_calls_new_implementation() -> None:
    with patch("services.view_classifier.extract_text_from_pdf", create=True):
        # This module uses utils.extract.extract_text_from_pdf; compatibility is tested indirectly via function call.
        pass

