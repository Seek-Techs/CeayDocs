from utils.extract import extract_text
from PyPDF2 import PdfWriter
from pathlib import Path
import io

def test_extract_text(tmp_path):
    # Create small text PDF
    pdf_path = tmp_path / "test.pdf"
    writer = PdfWriter()
    writer.add_blank_page(200,200)

    with open(pdf_path, "wb") as f:
        writer.write(f)

    # open as file-like
    with open(pdf_path, "rb") as f:
        pdf_data = io.BytesIO(f.read())

    result = extract_text(pdf_data)

    assert isinstance(result, str)
