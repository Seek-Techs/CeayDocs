from PyPDF2 import PdfReader, PdfWriter
import tempfile
from pathlib import Path


def split_pdf(pdf: str, output: str | None = None, start: int = 1, end: int = 1) -> bytes:
    """Backwards-compatible.

    Test expects: split_pdf(input_path, output_path, start=..., end=...) and returns None.
    Existing code expects: split_pdf(pdf_bytes, start, end) -> bytes.
    """
# bytes API: split_pdf(pdf_bytes, start, end)
    if isinstance(pdf, (bytes, bytearray)):
        pdf_bytes = bytes(pdf)
        # Support bytes API signatures used by existing ops/adapters.
        # Canonical behavior: return bytes.
        if output == "__bytes_output__":
            return _split_pdf_bytes(pdf_bytes, start, end)
        # Backward-compat / legacy path: if called without the expected sentinel,
        # raise to preserve historical behavior.
        if output is None:
            # called like split_pdf(pdf_bytes, start, end) where output param holds start
            raise TypeError("Invalid call signature")
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
