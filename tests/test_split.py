from utils.split import split_pdf
from PyPDF2 import PdfWriter
from pathlib import Path

def test_split_pdf(tmp_path):
    # Create a 3-page PDF
    input_pdf = tmp_path / "input.pdf"
    writer = PdfWriter()
    writer.add_blank_page(200,200)
    writer.add_blank_page(200,200)
    writer.add_blank_page(200,200)

    with open(input_pdf, "wb") as f:
        writer.write(f)

    output = tmp_path / "output.pdf"
    split_pdf(str(input_pdf), str(output), start=1, end=2)

    assert output.exists()
