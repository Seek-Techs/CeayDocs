from __future__ import annotations

from typing import Optional

from utils.convert import pdf_to_word, word_to_pdf


def pdf_to_word_op(pdf_bytes: bytes) -> bytes:
    return pdf_to_word(pdf_bytes)


def word_to_pdf_op(docx_bytes: bytes) -> bytes:
    return word_to_pdf(docx_bytes)

