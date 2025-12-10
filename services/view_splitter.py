import fitz
from io import BytesIO
from collections import defaultdict
from services.view_classifier import classify_pdf_views


def split_views_into_pdfs(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    view_info = classify_pdf_views(pdf_bytes)

    grouped_pages = defaultdict(list)

    for info in view_info:
        grouped_pages[info["view_type"]].append(info["page"] - 1)

    output_pdfs = {}

    for view_type, pages in grouped_pages.items():
        out_doc = fitz.open()

        for p in pages:
            out_doc.insert_pdf(doc, from_page=p, to_page=p)

        buffer = BytesIO()
        out_doc.save(buffer)
        buffer.seek(0)

        output_pdfs[view_type.lower()] = buffer.read()

    return output_pdfs
