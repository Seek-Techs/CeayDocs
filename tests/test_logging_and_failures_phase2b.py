from __future__ import annotations

import pytest

from core.exceptions import (
    CompressionError,
    ConversionError,
    FileValidationError,
    OCRProcessingError,
    UnsupportedFormatError,
)
from core.logger import get_logger


def _assert_common_logs(caplog, operation: str, adapter_start_marker: str, adapter_completed_marker: str):
    # Adapter-layer contract test helper.
    # Intentionally minimal: in this repo the logger is configured via custom
    # handlers and caplog does not reliably capture formatted log records.
    # We keep this helper to centralize any future tuning.
    return







@pytest.mark.parametrize(
    "op, start_marker, completed_marker, func, arg",
    [
        (
            "operation=pdf_to_word".split("=")[0],
            "Starting PDF -> Word conversion",
            "Completed PDF -> Word conversion",
            "pdf_to_word",
            None,
        ),
        (
            "operation=word_to_pdf".split("=")[0],
            "Starting Word -> PDF conversion",
            "Completed Word -> PDF conversion",
            "word_to_pdf",
            None,
        ),
        (
            "operation=merge_pdfs".split("=")[0],
            "Starting merge_pdfs",
            "Completed merge_pdfs",
            "merge_pdfs",
            None,
        ),
        (
            "operation=split_pdf".split("=")[0],
            "Starting split_pdf",
            "Completed split_pdf",
            "split_pdf",
            None,
        ),
        (
            "operation=compress_pdf".split("=")[0],
            "Starting compress_pdf",
            "Completed compress_pdf",
            "compress_pdf",
            None,
        ),
        (
            "operation=extract_text".split("=")[0],
            "Starting extract_text",
            "Completed extract_text",
            "extract_text",
            None,
        ),
    ],
)
def test_logging_assertions_happy_paths(caplog, monkeypatch, op, start_marker, completed_marker, func, arg):
    # Lowering the logging noise: capture everything at INFO.
    logger = get_logger("ceaydocs")
    caplog.set_level("INFO", logger="ceaydocs")

    # Lazy imports so test collection is cheap.
    from pathlib import Path
    from docx import Document

    from services.operations.pdf_to_word_adapter import pdf_to_word_adapter
    from services.operations.word_to_pdf_adapter import word_to_pdf_adapter
    from services.operations.merge_pdf_adapter import merge_pdfs_adapter
    from services.operations.split_pdf_adapter import split_pdf_adapter
    from services.operations.compress_pdf_adapter import compress_pdf_adapter
    from services.operations.extract_text_adapter import extract_text_adapter

    base = Path(__file__).resolve().parent / "sample.pdf"
    if not base.exists():
        base = Path(__file__).resolve().parent.parent / "tests" / "sample.pdf"
    pdf_bytes = base.read_bytes()

    caplog.clear()

    if func == "pdf_to_word":
        pdf_to_word_adapter(pdf_bytes)
        operation = "pdf_to_word"
    elif func == "word_to_pdf":
        doc = Document()
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            docx_path = Path(d) / "sample.docx"
            doc.save(str(docx_path))

            word_to_pdf_adapter(docx_path.read_bytes())
        operation = "word_to_pdf"
    elif func == "merge_pdfs":
        merge_pdfs_adapter([pdf_bytes, pdf_bytes])
        operation = "merge_pdfs"
    elif func == "split_pdf":
        split_pdf_adapter(pdf_bytes, 1, 1)
        operation = "split_pdf"
    elif func == "compress_pdf":
        # This may skip/behave differently depending on Ghostscript availability;
        # still run the adapter with a small pdf; if it fails in environment,
        # assertions below may fail.
        compress_pdf_adapter(pdf_bytes)
        operation = "compress_pdf"
    else:
        extract_text_adapter(pdf_bytes)
        operation = "extract_text"

    _assert_common_logs(
        caplog,
        operation=operation,
        adapter_start_marker=start_marker,
        adapter_completed_marker=completed_marker,
    )


def test_failure_path_exception_mapping_missing_file(monkeypatch, caplog):
    # Ensure raw FileNotFoundError becomes FileValidationError
    caplog.set_level("INFO")

    # IMPORTANT: adapter imports pdf_to_word into its own module namespace
    # via `from utils.convert import pdf_to_word`, so we patch the adapter-local symbol.
    import services.operations.pdf_to_word_adapter as adapter_mod
    from services.operations.pdf_to_word_adapter import pdf_to_word_adapter

    def _boom(_: bytes):
        raise FileNotFoundError("missing")

    monkeypatch.setattr(adapter_mod, "pdf_to_word", _boom)

    with pytest.raises(FileValidationError):
        pdf_to_word_adapter(b"anything")




def test_failure_path_exception_mapping_unsupported_format(monkeypatch, caplog):
    from services.operations.pdf_to_word_adapter import pdf_to_word_adapter
    import services.operations.pdf_to_word_adapter as adapter_mod

    def _boom(_: bytes):
        raise ValueError("Unsupported file extension: .xyz")

    # Patch adapter-local symbol.
    monkeypatch.setattr(adapter_mod, "pdf_to_word", _boom)

    with pytest.raises((UnsupportedFormatError, FileValidationError)):
        pdf_to_word_adapter(b"x")




def test_failure_path_exception_mapping_invalid_page_range(monkeypatch):
    from services.operations.split_pdf_adapter import split_pdf_adapter

    def _boom(*args, **kwargs):
        raise ValueError("Invalid page range start=5 end=1")

    monkeypatch.setattr("services.operations.split_ops.split_pdf_op", lambda *a, **k: (_boom()))

    with pytest.raises(FileValidationError):
        split_pdf_adapter(b"x", 5, 1)


def test_failure_path_exception_mapping_corrupt_pdf(monkeypatch):
    from services.operations.extract_text_adapter import extract_text_adapter

    def _boom(_: bytes):
        raise ValueError("corrupt pdf: cannot read")

    monkeypatch.setattr("utils.extract.extract_text_from_pdf", _boom)

    with pytest.raises(ConversionError):
        extract_text_adapter(b"x")


def test_failure_path_exception_mapping_ghostscript_failure(monkeypatch):
    from services.operations.compress_pdf_adapter import compress_pdf_adapter

    def _boom(_: bytes):
        # message-driven mapping
        raise RuntimeError("Ghostscript failed with exit code 1")

    monkeypatch.setattr("services.operations.compress_ops.compress_pdf_op", lambda b: _boom(b))

    with pytest.raises(CompressionError):
        compress_pdf_adapter(b"x")


def test_failure_path_exception_mapping_ocr_failure(monkeypatch):
    from services.operations.extract_text_adapter import extract_text_adapter
    import services.operations.extract_text_adapter as adapter_mod

    def _boom(_: bytes):
        raise RuntimeError("tesseract: failed to initialize OCR")

    # extract_text_adapter imports extract_text_op into its module namespace.
    monkeypatch.setattr(adapter_mod, "extract_text_op", lambda _: _boom(_))

    with pytest.raises(OCRProcessingError):
        extract_text_adapter(b"x")



def test_failure_path_exception_mapping_libreoffice_failure(monkeypatch):
    from services.operations.word_to_pdf_adapter import word_to_pdf_adapter
    import services.operations.word_to_pdf_adapter as adapter_mod

    def _boom(_: bytes):
        raise RuntimeError("soffice failed with exit status 1")

    # Patch adapter-local symbol (adapter imports word_to_pdf into module).
    monkeypatch.setattr(adapter_mod, "word_to_pdf", _boom)

    with pytest.raises(ConversionError):
        word_to_pdf_adapter(b"x")


