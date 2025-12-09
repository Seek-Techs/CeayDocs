from PyPDF2 import PdfReader, PdfWriter
import tempfile
from pathlib import Path


def split_pdf(pdf_bytes: bytes, start: int, end: int) -> bytes:
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
