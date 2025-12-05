import pytest
from utils.compress import compress_pdf
import shutil
from pathlib import Path
from PyPDF2 import PdfWriter

HAS_GS = shutil.which("gswin64c") or shutil.which("gs") or shutil.which("gswin32c")

@pytest.mark.skipif(not HAS_GS, reason="Ghostscript not installed.")
def test_compress_pdf(tmp_path):
    input_pdf = tmp_path / "test.pdf"

    writer = PdfWriter()
    writer.add_blank_page(200,200)
    with open(input_pdf, "wb") as f:
        writer.write(f)

    with open(input_pdf, "rb") as f:
        output_data = compress_pdf(f)

    assert output_data is not None
    assert isinstance(output_data, bytes)
