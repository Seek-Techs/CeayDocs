from PyPDF2 import PdfReader, PdfWriter
import tempfile
from io import BytesIO
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

def split_pdf(pdf_file, output_path=None, start=1, end=1):
    """
    Split pages [start..end] (1-based).
    - pdf_file: path or file-like
    - output_path: optional path to write the output file; if None returns bytes
    """
    pdf_path, created_tmp = _ensure_temp_file(pdf_file, suffix=".pdf")

    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # ensure bounds
    total = len(reader.pages)
    start_idx = max(0, start - 1)
    end_idx = min(total, end)

    for i in range(start_idx, end_idx):
        writer.add_page(reader.pages[i])

    if output_path:
        out_path = str(output_path)
        parent = Path(out_path).parent
        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            writer.write(f)
        if created_tmp and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception:
                pass
        return True
    else:
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        if created_tmp and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception:
                pass
        return output.read()
