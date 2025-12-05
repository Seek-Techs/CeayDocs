import tempfile
from pdf2docx import Converter
from docx2pdf import convert as docx_to_pdf
from io import BytesIO
import pythoncom
import os
from pathlib import Path

def pdf_to_word(pdf_file, output_path=None, start=0, end=None):
    """
    Convert PDF to DOCX.
    - If pdf_file is a Path/str and output_path provided -> write file and return True (tests expect this)
    - If pdf_file is file-like and output_path is None -> return bytes (for Streamlit)
    """
    def _convert_file(pdf_path, out_path):
        cv = Converter(pdf_path)
        cv.convert(out_path, start=start, end=end, fancy_table=True)
        cv.close()

    if isinstance(pdf_file, (str, Path)):
        pdf_path = str(pdf_file)
        if output_path:
            _convert_file(pdf_path, str(output_path))
            return True
        else:
            tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
            tmp_out.close()
            try:
                _convert_file(pdf_path, tmp_out.name)
                with open(tmp_out.name, "rb") as f:
                    data = f.read()
                return data
            finally:
                if os.path.exists(tmp_out.name):
                    os.remove(tmp_out.name)
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_file.read())
            pdf_path = tmp_pdf.name

        output_path_local = output_path or pdf_path.replace(".pdf", ".docx")
        try:
            _convert_file(pdf_path, output_path_local)
            if output_path:
                return True
            with open(output_path_local, "rb") as f:
                data = f.read()
            return data
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            if os.path.exists(output_path_local):
                os.remove(output_path_local)


def word_to_pdf(docx_file, output_path=None):
    """
    Convert DOCX to PDF.
    - If docx_file is a Path/str and output_path provided -> write file and return True (tests expect this)
    - If docx_file is file-like and output_path is None -> return bytes (Streamlit)
    """
    try:
        pythoncom.CoInitialize()
    except Exception:
        pass

    if isinstance(docx_file, (str, Path)):
        docx_path = str(docx_file)
        pdf_path = str(output_path) if output_path else docx_path.replace(".docx", ".pdf")
        docx_to_pdf(docx_path, pdf_path)
        if output_path:
            return True
        with open(pdf_path, "rb") as f:
            data = f.read()
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return data
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_doc:
            tmp_doc.write(docx_file.read())
            docx_path = tmp_doc.name

        pdf_path = output_path or docx_path.replace(".docx", ".pdf")

        try:
            docx_to_pdf(docx_path, pdf_path)
            if output_path:
                return True
            with open(pdf_path, "rb") as f:
                data = f.read()
            return data
        finally:
            if os.path.exists(docx_path):
                os.remove(docx_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
