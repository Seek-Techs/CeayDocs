from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture(autouse=True)
def _patch_mp3_fitz_open(monkeypatch):
    """Prevent real conversion utilities (fitz/pdf2docx/PIL) from running."""
    # Patch the most sensitive conversion call sites used by our tests.
    _ensure_pdf_to_word_patched(monkeypatch)
    import utils.convert as _conv
    import utils.images as _images

    # Patch ONLY the plumbing needed to avoid heavy external conversions.
    # Do not override exception/behavior-oriented call sites used by specific tests.

    # Ensure we don't call real image/pdf converters when tests only want adapter wiring.
    monkeypatch.setattr(_conv, "word_to_pdf", lambda _: b"pdf")
    monkeypatch.setattr(_images, "images_to_pdf", lambda _: b"pdf")
    monkeypatch.setattr(_images, "pdf_to_images", lambda _: b"zip")





def _ensure_pdf_to_word_patched(monkeypatch):
    # services.operations.convert_ops imports these at module import time:
    #   from utils.convert import pdf_to_word, word_to_pdf
    # so patch the production module attributes instead of utils.convert.
    import services.operations.convert_ops as _convert_ops

    monkeypatch.setattr(_convert_ops, "pdf_to_word", lambda b: b"out")
    monkeypatch.setattr(_convert_ops, "word_to_pdf", lambda b: b"pdf")





def test_pdf_to_word_op_success(monkeypatch):
    from services.operations.convert_ops import pdf_to_word_op


    def _fake_pdf_to_word(b: bytes) -> bytes:
        assert b == b"in"
        return b"out"

    monkeypatch.setattr("utils.convert.pdf_to_word", _fake_pdf_to_word)
    assert pdf_to_word_op(b"in") == b"out"


def test_pdf_to_word_op_propagates_exception(monkeypatch):
    from services.operations.convert_ops import pdf_to_word_op

    def _fake_pdf_to_word(_: bytes) -> bytes:
        raise ValueError("bad")

    import services.operations.convert_ops as _convert_ops

    monkeypatch.setattr(_convert_ops, "pdf_to_word", _fake_pdf_to_word)
    with pytest.raises(ValueError, match="bad"):
        pdf_to_word_op(b"in")



def test_word_to_pdf_op_success(monkeypatch):
    from services.operations.convert_ops import word_to_pdf_op

    def _fake_word_to_pdf(b: bytes) -> bytes:
        assert b == b"docx"
        return b"pdf"

    monkeypatch.setattr("utils.convert.word_to_pdf", _fake_word_to_pdf)
    assert word_to_pdf_op(b"docx") == b"pdf"


def test_word_to_pdf_op_propagates_exception(monkeypatch):
    from services.operations.convert_ops import word_to_pdf_op

    def _fake_word_to_pdf(_: bytes) -> bytes:
        raise OSError("boom")

    import services.operations.convert_ops as _convert_ops

    monkeypatch.setattr(_convert_ops, "word_to_pdf", _fake_word_to_pdf)
    with pytest.raises(OSError, match="boom"):
        word_to_pdf_op(b"docx")



def test_images_to_pdf_op_success(monkeypatch):
    from services.operations.images_ops import images_to_pdf_op

    def _fake_images_to_pdf(images: list[bytes]) -> bytes:
        assert images == [b"a", b"b"]
        return b"pdf"

    monkeypatch.setattr("utils.images.images_to_pdf", _fake_images_to_pdf)
    assert images_to_pdf_op([b"a", b"b"]) == b"pdf"


def test_pdf_to_images_op_success(monkeypatch):
    from services.operations.images_ops import pdf_to_images_op

    def _fake_pdf_to_images(pdf_bytes: bytes) -> bytes:
        assert pdf_bytes == b"pdf"
        return b"zip"

    monkeypatch.setattr("utils.images.pdf_to_images", _fake_pdf_to_images)
    assert pdf_to_images_op(b"pdf") == b"zip"


def test_pdf_to_word_service_execute_empty_bytes():
    from services.pdf_to_word import PdfToWordService

    svc = PdfToWordService()
    with pytest.raises(ValueError, match="No input bytes provided"):
        svc.execute(b"")


def test_pdf_to_word_service_execute_none_from_util(monkeypatch):
    from services.pdf_to_word import PdfToWordService
    import services.pdf_to_word as _pdf_to_word




    monkeypatch.setattr(_pdf_to_word, "util_pdf_to_word", lambda _: None)

    # Ensure util_pdf_to_word is a clean stub for this test.

    svc = PdfToWordService()

    with pytest.raises(RuntimeError, match="Conversion returned no output"):
        svc.execute(b"in")


def test_pdf_to_word_service_execute_propagates_util_exception(monkeypatch):
    from services.pdf_to_word import PdfToWordService

    def _boom(_: bytes) -> bytes:
        raise OSError("util fail")

    import services.pdf_to_word as _pdf_to_word

    monkeypatch.setattr(_pdf_to_word, "util_pdf_to_word", _boom)


    svc = PdfToWordService()
    with pytest.raises(OSError, match="util fail"):
        svc.execute(b"in")


def test_images_to_pdf_adapter_success(monkeypatch):
    from services.operations.images_to_pdf_adapter import images_to_pdf_adapter

    monkeypatch.setattr("services.operations.images_ops.images_to_pdf_op", lambda _: b"pdf")

    out = images_to_pdf_adapter([b"img"])
    assert out == b"pdf"


def test_images_to_pdf_adapter_maps_exception(monkeypatch):
    from services.operations import images_to_pdf_adapter as mod

    class _Mapped(Exception):
        pass

    monkeypatch.setattr(
        "services.operations.images_to_pdf_adapter.images_to_pdf_op",
        lambda _: (_ for _ in ()).throw(ValueError("bad")),
    )



    monkeypatch.setattr(
        "services.operations.images_to_pdf_adapter.map_exception_for_operation",
        lambda op, e: _Mapped(str(op)),
    )

    with pytest.raises(_Mapped):
        mod.images_to_pdf_adapter([b"img"])


def test_pdf_to_images_adapter_zip_success(monkeypatch):
    from services.operations.pdf_to_images_adapter import pdf_to_images_adapter_zip

    monkeypatch.setattr("utils.images.pdf_to_images", lambda _: b"zip")
    assert pdf_to_images_adapter_zip(b"pdf") == b"zip"


def test_pdf_to_images_adapter_zip_maps_exception(monkeypatch):
    from services.operations.pdf_to_images_adapter import pdf_to_images_adapter_zip

    class _Mapped(Exception):
        pass

    import services.operations.pdf_to_images_adapter as _adapter

    monkeypatch.setattr(
        _adapter,
        "pdf_to_images",
        lambda _: (_ for _ in ()).throw(RuntimeError("util failed")),
    )

    monkeypatch.setattr(
        "services.operations.pdf_to_images_adapter.map_exception_for_operation",
        lambda op, e: _Mapped(f"mapped:{op}"),
    )

    with pytest.raises(_Mapped, match="mapped:pdf_to_images"):
        pdf_to_images_adapter_zip(b"pdf")


def _make_fitz_mocks(*, pages: list[dict[str, Any]]):
    """Create minimal doc/page mocks for core.classify.classify_pdf."""

    class _Page:
        def __init__(self, d: dict[str, Any]):
            self._d = d

        def get_text(self) -> str:
            return self._d.get("text", "")

        def get_images(self):
            return self._d.get("images", [])

    class _Doc:
        def __init__(self, p: list[dict[str, Any]]):
            self._pages = [_Page(x) for x in p]

        def __iter__(self):
            return iter(self._pages)

        def __len__(self):
            return len(self._pages)

    return _Doc(pages)


def test_classify_pdf_scanned_branch(monkeypatch):
    import core.classify as mod

    monkeypatch.setattr(
        "core.classify.fitz.open",
        lambda stream, filetype: _make_fitz_mocks(
            pages=[{"text": "   ", "images": [1]}, {"text": "", "images": [2]}]
        ),
    )

    res = mod.classify_pdf(b"pdf")
    assert res["pdf_type"] == "scanned"
    assert res["has_images"] is True
    assert res["has_text"] is False


def test_classify_pdf_vector_branch(monkeypatch):
    import core.classify as mod

    monkeypatch.setattr(
        "core.classify.fitz.open",
        lambda stream, filetype: _make_fitz_mocks(
            pages=[{"text": "hello", "images": []}]
        ),
    )

    res = mod.classify_pdf(b"pdf")
    assert res["pdf_type"] == "vector"
    assert res["has_images"] is False
    assert res["has_text"] is True


def test_classify_pdf_hybrid_else_branch(monkeypatch):
    import core.classify as mod

    # Both text and images present -> hybrid
    monkeypatch.setattr(
        "core.classify.fitz.open",
        lambda stream, filetype: _make_fitz_mocks(
            pages=[{"text": "hello", "images": [1, 2]}]
        ),
    )

    res = mod.classify_pdf(b"pdf")
    assert res["pdf_type"] == "hybrid"
    assert res["has_images"] is True
    assert res["has_text"] is True

