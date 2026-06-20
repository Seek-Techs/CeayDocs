from __future__ import annotations

from utils.extract import extract_text_from_pdf


def extract_text_op(pdf_bytes: bytes) -> str:
    return extract_text_from_pdf(pdf_bytes)

