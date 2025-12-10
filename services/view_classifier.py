import re
import fitz

PLAN_KEYWORDS = ["plan", "floor plan", "layout"]
SECTION_KEYWORDS = ["section", "sec", "s/s"]
ELEVATION_KEYWORDS = ["elevation", "front view", "side view"]

def classify_page(page) -> dict:
    text = page.get_text("text").lower()

    def contains(keywords):
        return any(k in text for k in keywords)

    if contains(PLAN_KEYWORDS):
        view_type = "PLAN"
    elif contains(SECTION_KEYWORDS):
        view_type = "SECTION"
    elif contains(ELEVATION_KEYWORDS):
        view_type = "ELEVATION"
    else:
        view_type = "UNKNOWN"

    return {
        "view_type": view_type,
        "text_snippet": text[:300]
    }


def classify_pdf_views(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    results = []

    for i, page in enumerate(doc):
        page_result = classify_page(page)
        page_result["page"] = i + 1
        results.append(page_result)

    return results
