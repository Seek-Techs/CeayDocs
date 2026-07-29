from __future__ import annotations

from utils.split import split_pdf


def split_pdf_op(pdf_bytes: bytes, start: int, end: int) -> bytes:
    """Split a PDF page range via the clean bytes API."""
    result = split_pdf(pdf_bytes, start=start, end=end)
    if result is None:
        raise RuntimeError("split_pdf returned None unexpectedly")
    return result


