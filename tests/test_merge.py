from utils.merge import merge_pdfs
from PyPDF2 import PdfWriter
from pathlib import Path

def test_merge_pdfs(tmp_path):
    # Create 2 small test PDFs
    pdf1 = tmp_path / "a.pdf"
    pdf2 = tmp_path / "b.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with open(pdf1, "wb") as f:
        writer.write(f)

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with open(pdf2, "wb") as f:
        writer.write(f)

    output = tmp_path / "merged.pdf"

    merge_pdfs([pdf1, pdf2], output)
    assert output.exists()
