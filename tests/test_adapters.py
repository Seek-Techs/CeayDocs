from __future__ import annotations

from pathlib import Path

from services.operations.compress_pdf_adapter import compress_pdf_adapter
from services.operations.extract_text_adapter import extract_text_adapter
from services.operations.merge_pdf_adapter import merge_pdfs_adapter
from services.operations.pdf_to_word_adapter import pdf_to_word_adapter
from services.operations.split_pdf_adapter import split_pdf_adapter
from services.operations.word_to_pdf_adapter import word_to_pdf_adapter


def _sample_pdf_bytes() -> bytes:
    # Resolve relative to this test file, so tests are robust to CWD.
    base = Path(__file__).resolve().parent
    sample = base / "sample.pdf"
    if not sample.exists():
        sample = base / "sample.pdf"  # no-op; kept for clarity
    # Fallback to repo tests/ location if needed.
    if not sample.exists():
        sample = base.parent / "tests" / "sample.pdf"
    return sample.read_bytes()


def test_pdf_to_word_adapter(tmp_path):

    pdf_bytes = _sample_pdf_bytes()
    out = pdf_to_word_adapter(pdf_bytes)
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0


def test_word_to_pdf_adapter(tmp_path):
    from docx import Document

    doc = Document()
    doc.add_paragraph("Hello")
    docx_bytes = (tmp_path / "sample.docx")
    doc.save(docx_bytes)

    out = word_to_pdf_adapter(docx_bytes.read_bytes())
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0


def test_compress_pdf_adapter():
    pdf_bytes = _sample_pdf_bytes()
    out = compress_pdf_adapter(pdf_bytes)
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0


def test_merge_pdfs_adapter():
    pdf_bytes = _sample_pdf_bytes()
    out = merge_pdfs_adapter([pdf_bytes, pdf_bytes])
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0


def test_split_pdf_adapter():
    pdf_bytes = _sample_pdf_bytes()
    # sample.pdf is small; split first page only
    out = split_pdf_adapter(pdf_bytes, 1, 1)
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0


def test_extract_text_adapter():
    pdf_bytes = _sample_pdf_bytes()
    out = extract_text_adapter(pdf_bytes)
    assert isinstance(out, str)
    assert len(out) >= 0

