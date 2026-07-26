from __future__ import annotations

from utils.split import split_pdf


def split_pdf_op(pdf_bytes: bytes, start: int, end: int) -> bytes:
    # utils.split.split_pdf has a historical signature and can raise a TypeError
    # for the bytes API. Prefer the canonical internal bytes implementation.
    result = split_pdf(pdf_bytes, output="__bytes_output__", start=start, end=end)
    if result is None:
        raise RuntimeError("split_pdf returned None unexpectedly")
    return result


