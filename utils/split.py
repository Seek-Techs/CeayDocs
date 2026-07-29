from __future__ import annotations

import tempfile
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def split_pdf(pdf: str | bytes | bytearray,  # noqa: PLR0911
              output: str | None = None,
              start: int = 1,
              end: int = 1) -> bytes | None:
    """Split a PDF page range.

    Supports two calling conventions:

    1. Path-based:  split_pdf(input_path, output_path, start=..., end=...) -> None
    2. Bytes API:   split_pdf(pdf_bytes, start=..., end=...) -> bytes
    """
    # --- Bytes API (clean) ---
    if isinstance(pdf, (bytes, bytearray)):
        pdf_bytes = bytes(pdf)
        return _split_pdf_bytes(pdf_bytes, start, end)

    # --- Path-based API ---
    input_path = Path(pdf)
    if output is None:
        raise TypeError("output is required for path-based split")
    output_path = Path(output)

    pdf_bytes = input_path.read_bytes()
    out_bytes = _split_pdf_bytes(pdf_bytes, start, end)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(out_bytes)
    return None


def _split_pdf_bytes(pdf_bytes: bytes, start: int, end: int) -> bytes:
    """
    Split a PDF from start page to end page (1-based indexing).
    """
    if start < 1 or end < start:
        raise ValueError("Invalid page range")

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.pdf"
        input_path.write_bytes(pdf_bytes)

        reader = PdfReader(str(input_path))
        total_pages = len(reader.pages)

        if end > total_pages:
            raise ValueError(
                f"PDF has only {total_pages} pages, but end={end}"
            )

        writer = PdfWriter()

        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        output_path = Path(tmpdir) / "split.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path.read_bytes()
