import fitz  # PyMuPDF
import tempfile
from pathlib import Path
import zipfile
from PIL import Image
from io import BytesIO


# ==============================
# PDF → IMAGES
# ==============================
def pdf_to_images(pdf: object):
    """Convert a PDF into PNG images.

    Test/backwards-compatible behavior:
    - if input is file-like (e.g., BufferedReader) -> returns list[PIL.Image]

    API behavior (used by Streamlit/API routes):
    - if you pass raw bytes -> returns ZIP bytes containing PNGs
    """
    # Accept file-like
    if hasattr(pdf, "read"):
        pdf_bytes = pdf.read()
        return _pdf_to_images_list(pdf_bytes)

    # Raw bytes -> ZIP bytes
    return _pdf_to_images_zip_bytes(pdf)


def _pdf_to_images_list(pdf_bytes: bytes) -> list[Image.Image]:
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / "input.pdf"
        pdf_path.write_bytes(pdf_bytes)

        doc = fitz.open(pdf_path)
        images: list[Image.Image] = []
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img = Image.open(BytesIO(pix.tobytes("png")))
            images.append(img)
        doc.close()
        return images


def _pdf_to_images_zip_bytes(pdf_bytes: bytes) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = Path(tmpdir) / "input.pdf"
        pdf_path.write_bytes(pdf_bytes)

        doc = fitz.open(pdf_path)
        image_paths = []

        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = Path(tmpdir) / f"page_{i+1}.png"
            pix.save(img_path)
            image_paths.append(img_path)

        doc.close()

        zip_path = Path(tmpdir) / "images.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for img in image_paths:
                zf.write(img, img.name)

        return zip_path.read_bytes()


# ==============================
# IMAGES → PDF
# ==============================
def images_to_pdf(image_bytes_list):
    """Convert images into a single PDF.

    Test/backwards-compatible behavior:
    - input may be list[BytesIO] or list[bytes]

    API behavior:
    - expects iterable of raw image bytes
    """
    images = []

    for item in image_bytes_list:
        if hasattr(item, "read"):
            img_bytes = item.read()
        else:
            img_bytes = item

        img = Image.open(BytesIO(img_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    if not images:
        return b""

    output = BytesIO()
    images[0].save(
        output,
        format="PDF",
        save_all=True,
        append_images=images[1:],
    )
    output.seek(0)
    return output.read()

