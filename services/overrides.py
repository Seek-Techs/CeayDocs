# services/overrides.py
from typing import Dict, Any, List

def apply_overrides(
    pages: List[Dict[str, Any]],
    overrides: Dict[int, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Overrides example:
    {
        2: {"view_type": "SECTION", "scale": "1:25"},
        5: {"view_type": "PLAN"}
    }
    """
    corrected = []

    for p in pages:
        page_num = p["page"]
        if page_num in overrides:
            updated = {**p, **overrides[page_num]}
            updated["overridden"] = True
            corrected.append(updated)
        else:
            p["overridden"] = False
            corrected.append(p)

    return corrected
