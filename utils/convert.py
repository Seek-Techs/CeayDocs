import subprocess
import tempfile
from pathlib import Path
from pdf2docx import Converter
import shutil


# ---------- PDF → WORD ----------
def pdf_to_word(pdf_file):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
        tmp_pdf.write(pdf_file.read())
        pdf_path = tmp_pdf.name

    docx_path = pdf_path.replace(".pdf", ".docx")

    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    with open(docx_path, "rb") as f:
        output = f.read()

    Path(pdf_path).unlink(missing_ok=True)
    Path(docx_path).unlink(missing_ok=True)

    return output


# ---------- WORD → PDF (LibreOffice) ----------
def word_to_pdf(docx_file):
    if not shutil.which("libreoffice"):
        raise RuntimeError(
            "LibreOffice is required for Word → PDF conversion."
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / docx_file.name
        output_dir = Path(tmpdir)

        input_path.write_bytes(docx_file.read())

        subprocess.run(
            [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(input_path),
            ],
            check=True,
        )

        pdf_path = next(output_dir.glob("*.pdf"))

        return pdf_path.read_bytes()
