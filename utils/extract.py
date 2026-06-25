import tempfile
from pathlib import Path

from pdfminer.high_level import extract_text as pdfminer_extract_text


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using pdfminer."""

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        return pdfminer_extract_text(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# Backwards-compatible alias (older code/tests import `extract_text`)

def extract_text(pdf: bytes | object):
    """Backwards-compatible wrapper.

    Accepts either:
    - bytes (current utils API)
    - file-like objects (tests pass BytesIO)
    """
    if hasattr(pdf, "read"):
        pdf_bytes = pdf.read()
    else:
        pdf_bytes = pdf
    return extract_text_from_pdf(pdf_bytes)


