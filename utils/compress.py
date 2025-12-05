import subprocess
import tempfile
import shutil
import os
import platform
from .compress_fallback import compress_pdf_fallback


def _find_ghostscript():
    """Check for Ghostscript executable on all OS."""
    candidates = ["gswin64c", "gswin32c", "gs"] if platform.system() == "Windows" else ["gs"]
    for cmd in candidates:
        if shutil.which(cmd):
            return cmd
    return None


def compress_pdf(pdf_file):
    """
    Compress PDF using Ghostscript if available,
    otherwise use pure-Python fallback.
    """
    gs = _find_ghostscript()

    # If Ghostscript NOT found → use fallback
    if not gs:
        return compress_pdf_fallback(pdf_file)

    # If Ghostscript found → use system-level compression
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        input_path = tmp.name

    output_path = input_path.replace(".pdf", "_compressed.pdf")

    cmd = [
        gs,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(cmd, check=True)

    with open(output_path, "rb") as f:
        data = f.read()

    os.remove(input_path)
    os.remove(output_path)

    return data
