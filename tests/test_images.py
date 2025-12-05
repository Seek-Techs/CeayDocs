from utils.images import pdf_to_images, images_to_pdf
from PyPDF2 import PdfWriter
from pathlib import Path
from PIL import Image
import io
import os
def test_pdf_to_images(tmp_path):
    pdf_path = tmp_path / "pages.pdf"

    writer = PdfWriter()
    writer.add_blank_page(200,200)
    writer.add_blank_page(200,200)
    with open(pdf_path, "wb") as f:
        writer.write(f)

    with open(pdf_path, "rb") as f:
        result = pdf_to_images(f)

    assert isinstance(result, list)
    assert len(result) == 2

def test_images_to_pdf(tmp_path):
    img = Image.new("RGB", (200,200), "white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    images = [img_bytes]
    pdf_bytes = images_to_pdf(images)

    assert isinstance(pdf_bytes, bytes)
