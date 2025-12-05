from PyPDF2 import PdfMerger
import tempfile
from io import BytesIO
import os
from pathlib import Path

def merge_pdfs(pdf_files, output_path=None):
    """
    Merge PDFs.
    - pdf_files: iterable of Paths/str or file-like objects
    - output_path: if provided, write merged file to this path and return True
                   otherwise return bytes of merged PDF
    """
    merger = PdfMerger()
    tmp_paths = []

    try:
        for file in pdf_files:
            if isinstance(file, (str, Path)):
                merger.append(str(file))
            else:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp.write(file.read())
                tmp.close()
                tmp_paths.append(tmp.name)
                merger.append(tmp.name)

        if output_path:
            out_path = str(output_path)
            # ensure parent directory exists
            parent = Path(out_path).parent
            if not parent.exists():
                parent.mkdir(parents=True, exist_ok=True)
            merger.write(out_path)
            merger.close()
            return True
        else:
            output = BytesIO()
            merger.write(output)
            output.seek(0)
            merger.close()
            return output.read()

    finally:
        for path in tmp_paths:
            try:
                os.remove(path)
            except Exception:
                pass
