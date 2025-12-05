import pytest
from utils.convert import pdf_to_word, word_to_pdf
from pathlib import Path

def test_pdf_to_word(tmp_path):
    pdf_file = Path("tests/sample.pdf")
    output = tmp_path / "output.docx"

    result = pdf_to_word(pdf_file, output)
    assert output.exists()
    assert result is True

def test_word_to_pdf(tmp_path):
    from docx import Document
    # Create a sample DOCX
    docx_path = tmp_path / "sample.docx"
    doc = Document()
    doc.add_paragraph("Hello Test")
    doc.save(docx_path)

    output = tmp_path / "output.pdf"
    result = word_to_pdf(docx_path, output)
    assert output.exists()
    assert result is True
