import tempfile
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def split_pdf(pdf: str | bytes | bytearray, output: str | None = None, start: int = 1, end: int = 1) -> bytes | None:
    """Backwards-compatible.

    Supports three calling conventions:

    1. Path-based:     split_pdf(input_path, output_path, start=..., end=...) -> None
    2. Canonical bytes: split_pdf(pdf_bytes, output="__bytes_output__", start=..., end=...) -> bytes
    3. Legacy bytes:   split_pdf(pdf_bytes, start, end) -> bytes    (where start/end are positional ints)

    Test expects: split_pdf(input_path, output_path, start=..., end=...) and returns None.
    Existing code expects: split_pdf(pdf_bytes, start, end) -> bytes.
    """
    # bytes API: split_pdf(pdf_bytes, start, end)  or
    #            split_pdf(pdf_bytes, output="__bytes_output__", start=..., end=...)
    if isinstance(pdf, (bytes, bytearray)):
        pdf_bytes = bytes(pdf)

        # Canonical bytes API via sentinel
        if output == "__bytes_output__":
            return _split_pdf_bytes(pdf_bytes, start, end)

        # Legacy bytes API: called as split_pdf(pdf_bytes, start, end)
        # where 'output' param actually holds 'start' as an integer.
        if isinstance(output, int):
            # output param is actually the start page number
            return _split_pdf_bytes(pdf_bytes, output, start)

        # Legacy bytes API: called as split_pdf(pdf_bytes, start, end)
        # where output is None (start is the third positional arg 'end').
        if output is None:
            # This is the case: split_pdf(pdf_bytes, start_value, end_value)
            # where start_value got stored in 'output' param (None),
            # and end_value got stored in 'start' param, 'end' param defaulted.
            # Actually this means: called with only 2 positional args after pdf_bytes.
            if start == 1 and end == 1:
                raise TypeError("Invalid call: missing start/end page numbers")
            # start holds start page (2nd positional), end holds end page (3rd positional)
            return _split_pdf_bytes(pdf_bytes, start, end)

        raise TypeError("Use bytes API via split_pdf_bytes")


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
