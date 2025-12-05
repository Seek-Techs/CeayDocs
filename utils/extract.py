from pdfminer.high_level import extract_text as pdfminer_extract_text
import tempfile
import os

def extract_text(pdf_file):
    """Extract text from a PDF uploaded via Streamlit."""
    
    # pdf_file is a file-like object (BytesIO)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name

    try:
        # Use pdfminer to extract actual text
        text = pdfminer_extract_text(tmp_path)
        return text
    finally:
        os.remove(tmp_path)
