import subprocess
import tempfile
from pathlib import Path
from pdf2docx import Converter
import shutil


# ---------- PDF → WORD ----------
def pdf_to_word(pdf_bytes: bytes) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        tmp_pdf.write(pdf_bytes)
        pdf_path = tmp_pdf.name

    docx_path = pdf_path.replace(".pdf", ".docx")

    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        with open(docx_path, "rb") as f:
            output = f.read()

        return output

    finally:
        Path(pdf_path).unlink(missing_ok=True)
        Path(docx_path).unlink(missing_ok=True)


# ---------- WORD → PDF (LibreOffice) ----------
def word_to_pdf(docx_bytes: bytes) -> bytes:
    if not shutil.which("libreoffice"):
        raise RuntimeError(
            "LibreOffice is required for Word → PDF conversion."
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.docx"
        input_path.write_bytes(docx_bytes)

        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                tmpdir,
                input_path,
            ],
            check=True,
        )

        pdf_files = list(Path(tmpdir).glob("*.pdf"))
        if not pdf_files:
            raise RuntimeError("PDF conversion failed")

        return pdf_files[0].read_bytes()
