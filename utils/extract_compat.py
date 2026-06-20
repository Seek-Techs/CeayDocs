"""Compatibility helpers for extract-related utilities."""

from __future__ import annotations

from utils.extract import extract_text_from_pdf


def extract_text(pdf_bytes: bytes) -> str:
    """Backwards-compatible alias for older code/tests."""

    return extract_text_from_pdf(pdf_bytes)

