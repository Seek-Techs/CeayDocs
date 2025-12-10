import re
import fitz

SCALE_PATTERNS = [
    r"SCALE\s*[:=]?\s*(1\s*[:/]\s*\d+)",
    r"SCALE\s*\(?(1\s*[:/]\s*\d+)\)?",
    r"(1\s*[:/]\s*\d+)"
]

def detect_scales(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    result = []

    for i, page in enumerate(doc):
        text = page.get_text("text").upper()
        detected = None

        for pattern in SCALE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                detected = match.group(1).replace(" ", "")
                break

        result.append({
            "page": i + 1,
            "scale": detected or "Unknown"
        })

    doc.close()
    return result
