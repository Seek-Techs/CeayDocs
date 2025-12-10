import fitz  # PyMuPDF
from io import BytesIO

def classify_pdf(pdf_bytes: bytes) -> dict:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text_len = sum(len(page.get_text().strip()) for page in doc)
    image_count = sum(len(page.get_images()) for page in doc)

    if image_count > 0 and text_len == 0:
        pdf_type = "scanned"
    elif image_count == 0 and text_len > 0:
        pdf_type = "vector"
    else:
        pdf_type = "hybrid"

    return {
        "pdf_type": pdf_type,
        "pages": len(doc),
        "has_text": text_len > 0,
        "has_images": image_count > 0,
    }
