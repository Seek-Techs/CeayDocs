import fitz  # PyMuPDF
import tempfile
from io import BytesIO
from PIL import Image
import os
from pathlib import Path

def _ensure_temp_file(input_obj, suffix=".pdf"):
    if isinstance(input_obj, (str, Path)):
        return str(input_obj), False
    else:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(input_obj.read())
        tmp.close()
        return tmp.name, True

def pdf_to_images(pdf_file):
    """Convert PDF pages to images and return a list of BytesIO PNG images."""
    pdf_path, created_tmp = _ensure_temp_file(pdf_file, suffix=".pdf")

    doc = fitz.open(pdf_path)
    images = []

    try:
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img_bytes = BytesIO(pix.tobytes("png"))
            img_bytes.seek(0)
            images.append(img_bytes)
    finally:
        doc.close()
        if created_tmp and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception:
                pass

    return images


def images_to_pdf(image_files):
    """Convert uploaded images to a single PDF and return bytes."""
    images = []

    for img_file in image_files:
        if isinstance(img_file, (str, Path)):
            img = Image.open(str(img_file))
        else:
            img = Image.open(img_file)

        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    if not images:
        return b""

    output = BytesIO()
    images[0].save(output, format="PDF", save_all=True, append_images=images[1:])
    output.seek(0)

    return output.read()
