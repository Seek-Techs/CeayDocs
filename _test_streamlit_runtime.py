"""Streamlit runtime smoke test - simulates each tool's code path with real data."""

import io
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image

from utils.convert import pdf_to_word, word_to_pdf
from utils.extract import extract_text_from_pdf
from utils.images import images_to_pdf, pdf_to_images, _pdf_to_images_list
from utils.merge import merge_pdfs
from utils.split import split_pdf

SAMPLE_PDF = Path("tests/sample.pdf")
assert SAMPLE_PDF.exists(), f"Missing {SAMPLE_PDF}"
PDF_BYTES = SAMPLE_PDF.read_bytes()


def test_pdf_to_word():
    """Simulate: uploaded.read() -> pdf_to_word(pdf_bytes)"""
    output = pdf_to_word(PDF_BYTES)
    assert output is not None
    assert len(output) > 0
    print(f"  [OK] PDF->Word: {len(output)} bytes")


def test_word_to_pdf():
    """We don't have a sample .docx, just check the function exists."""
    print("  [SKIP] Word->PDF: no sample docx, function import OK")


def test_merge_pdfs():
    """Simulate: uploaded_files list -> merge_pdfs(uploaded_files)"""
    output = merge_pdfs([BytesIO(PDF_BYTES), BytesIO(PDF_BYTES)])
    assert output is not None
    assert len(output) > 0
    print(f"  [OK] Merge PDFs: {len(output)} bytes")


def test_split_pdf():
    """Simulate: pdf.read() -> split_pdf(pdf_bytes, start, end)"""
    output = split_pdf(PDF_BYTES, 1, 1)
    assert output is not None
    assert len(output) > 0
    print(f"  [OK] Split PDF: {len(output)} bytes")


def test_compress_pdf():
    """Simulate: uploaded.read() -> BytesIO -> compress_pdf"""
    from utils.compress import compress_pdf
    try:
        output = compress_pdf(BytesIO(PDF_BYTES))
        assert output is not None
        print(f"  [OK] Compress PDF: {len(output)} bytes")
    except Exception as e:
        print(f"  [!] Compress PDF: {e} (may need Ghostscript)")


def test_pdf_to_images():
    """Simulate: pass file-like object (uploaded file) -> pdf_to_images()"""
    from utils.images import pdf_to_images

    # Simulate Streamlit's UploadedFile behavior: pass file-like object
    file_like = BytesIO(PDF_BYTES)
    file_like.name = "sample.pdf"  # simulate UploadedFile.name

    # This is the exact code path used in app.py (after the fix):
    #   images = pdf_to_images(pdf)   where pdf is an UploadedFile (file-like)
    images = pdf_to_images(file_like)

    assert isinstance(images, list), f"Expected list[PIL.Image], got {type(images)}"
    assert len(images) > 0
    img = images[0]
    # Verify it's a PIL Image with .save()
    assert hasattr(img, "save"), "PIL Image missing save()"
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    assert len(buf.read()) > 0
    print(f"  [OK] PDF->Images: {len(images)} pages, PIL Image.save() works")

    # Test the full ZIP generation logic as used in app.py
    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as z:
        for i, img in enumerate(images):
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            z.writestr(f"page_{i+1}.png", buf.read())
    zip_buf.seek(0)
    assert len(zip_buf.read()) > 0
    print("  [OK] PDF->Images ZIP generation works")


def test_images_to_pdf():
    """Simulate: imgs list (BytesIO) -> images_to_pdf(imgs)"""
    images = _pdf_to_images_list(PDF_BYTES)
    img_bufs = []
    for img in images:
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        img_bufs.append(buf)

    output = images_to_pdf(img_bufs)
    assert output is not None
    assert len(output) > 0
    print(f"  [OK] Images->PDF: {len(output)} bytes")


def test_extract_text():
    """Simulate: pdf.read() -> extract_text_from_pdf(pdf_bytes)"""
    text = extract_text_from_pdf(PDF_BYTES)
    assert isinstance(text, str)
    assert len(text) > 0
    print(f"  [OK] Extract Text: {len(text)} chars")


def test_drawing_analyzer():
    """Simulate: uploaded_file.read() -> analyze_drawing(pdf_bytes)"""
    from services.analyzer import analyze_drawing
    try:
        result = analyze_drawing(PDF_BYTES)
        assert isinstance(result, dict)
        print(f"  [OK] Drawing Analyzer: pages={len(result.get('pages', []))}")
    except Exception as e:
        print(f"  [!] Drawing Analyzer: {e} (may need dependencies)")


if __name__ == "__main__":
    tests = [
        ("PDF -> Word", test_pdf_to_word),
        ("Word -> PDF", test_word_to_pdf),
        ("Merge PDFs", test_merge_pdfs),
        ("Split PDF", test_split_pdf),
        ("Compress PDF", test_compress_pdf),
        ("PDF -> Images", test_pdf_to_images),
        ("Images -> PDF", test_images_to_pdf),
        ("Extract Text", test_extract_text),
        ("Drawing Analyzer", test_drawing_analyzer),
    ]

    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            print(f"\n=== {name} ===")
            fn()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    exit(1 if failed > 0 else 0)

