import fitz
import io
from PIL import Image

def compress_pdf_fallback(pdf_file, dpi=120, jpeg_quality=60):
    """
    Basic PDF compressor using rasterization + JPEG compression (no Ghostscript).
    """

    input_bytes = pdf_file.read()
    doc = fitz.open(stream=input_bytes, filetype="pdf")

    output_pdf = fitz.open()

    for page in doc:
        # Render page → pixmap
        pix = page.get_pixmap(dpi=dpi)

        # Convert pixmap → PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Compress image using JPEG quality
        img_bytes_io = io.BytesIO()
        img.save(img_bytes_io, format="JPEG", quality=jpeg_quality)
        img_bytes = img_bytes_io.getvalue()

        # Insert compressed image into output PDF
        new_page = output_pdf.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=img_bytes)

    result = output_pdf.tobytes()
    return result
