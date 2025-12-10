# services/drawing_register.py
from typing import List, Dict, Any
from datetime import datetime

def infer_discipline(view_type: str) -> str:
    vt = view_type.upper()
    if vt in {"PLAN", "SECTION", "ELEVATION", "DETAIL"}:
        return "STRUCTURAL"
    return "GENERAL"

def build_register(
    index: List[Dict[str, Any]],
    project_code: str = "PRJ",
    revision: str = "A"
) -> List[Dict[str, Any]]:
    """
    Build a formal drawing register from the drawing index.
    """

    register = []

    for row in index:
        page = row["page"]
        view_type = row["view_type"]

        drawing_no = f"{project_code}-S-{page:03d}"

        title = f"{view_type.title()} Drawing"

        register.append({
            "drawing_no": drawing_no,
            "title": title,
            "sheet_no": page,
            "view_type": view_type,
            "scale": row["scale"],
            "revision": revision,
            "status": "FOR REVIEW" if row["status"] != "OK" else "FOR CONSTRUCTION",
            "discipline": infer_discipline(view_type),
            "confidence": row["confidence"],
            "source": "AUTO",
            "created_on": datetime.now().strftime("%Y-%m-%d")
        })

    return register
