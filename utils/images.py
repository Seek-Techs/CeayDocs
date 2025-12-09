import fitz  # PyMuPDF
import tempfile
from pathlib import Path
import zipfile
from PIL import Image
from io import BytesIO


# ==============================
# PDF → IMAGES
# ==============================
def pdf_to_images(pdf_bytes: bytes) -> bytes:
    """
    Convert a PDF into PNG images.
    Returns a ZIP file (bytes) containing images.
    """
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
def images_to_pdf(image_bytes_list: list[bytes]) -> bytes:
    """
    Convert a list of image bytes into a single PDF.
    """
    images = []

    for img_bytes in image_bytes_list:
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
        append_images=images[1:]
    )
    output.seek(0)
    return output.read()
