# services/drawing_index.py
from typing import List, Dict, Any, Tuple
import io
import csv

# Thresholds and rules (tweakable)
CONFIDENCE_THRESHOLD = 0.6

REQUIRED_VIEWS = {"PLAN", "SECTION", "ELEVATION"}

def normalize_page(p: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure page dict has expected fields with safe defaults."""
    page_num = p.get("page")
    try:
        page_num = int(page_num) if page_num is not None else None
    except Exception:
        page_num = None

    view_type = (p.get("view_type") or "UNKNOWN").upper()
    # normalize confidence to float or None
    raw_conf = p.get("confidence", None)
    confidence = None
    try:
        if raw_conf is not None:
            confidence = float(raw_conf)
    except Exception:
        confidence = None

    scale = p.get("scale") or "Unknown"

    return {
        "page": page_num,
        "view_type": view_type,
        "confidence": confidence,
        "scale": scale
    }

def generate_index(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Turn the pages list (from analyzer) into a stable index:
    [{page, view_type, confidence, scale, status}, ...]
    """
    index = []
    for p in pages:
        np = normalize_page(p)
        # status logic
        if np["confidence"] is None:
            status = "LOW CONF"  # explicit low confidence
        elif np["confidence"] < CONFIDENCE_THRESHOLD:
            status = "LOW CONF"
        else:
            status = "OK"

        # Unknown view_type is suspicious
        if np["view_type"] == "UNKNOWN":
            status = "REVIEW" if status == "OK" else status

        row = {
            "page": np["page"],
            "view_type": np["view_type"],
            "scale": np["scale"],
            "confidence": np["confidence"],
            "status": status
        }
        index.append(row)
    # sort by page number when possible
    index.sort(key=lambda r: (r["page"] is None, r["page"]))
    return index

def generate_qa(index: List[Dict[str, Any]]) -> Dict[str, Any]:
    qa: Dict[str, Any] = {
        "missing_views": [],
        "scale_issues": [],
        "low_confidence_pages": []
    }

    seen_views = set()
    scales_by_view = {}

    for row in index:
        vt = row["view_type"]

        # Track only real drawing views
        if vt in REQUIRED_VIEWS:
            seen_views.add(vt)

        scales_by_view.setdefault(vt, set()).add(row.get("scale", "Unknown"))

        if row["confidence"] is None or (
            isinstance(row["confidence"], (int, float))
            and row["confidence"] < CONFIDENCE_THRESHOLD
        ):
            qa["low_confidence_pages"].append({
                "page": row["page"],
                "view_type": vt,
                "confidence": row["confidence"]
            })

    # Missing required views
    qa["missing_views"] = [v for v in REQUIRED_VIEWS if v not in seen_views]

    # Scale inconsistencies
    for vt, scales in scales_by_view.items():
        if vt == "UNKNOWN":
            continue

        known_scales = [s for s in scales if s and str(s).lower() != "unknown"]
        unique_known = sorted(set(known_scales))

        if len(unique_known) > 1:
            qa["scale_issues"].append(
                f"Multiple scales detected for {vt}: {', '.join(unique_known)}"
            )
        elif len(unique_known) == 0:
            qa["scale_issues"].append(
                f"No declared scale found for {vt}"
            )

    return qa


def index_to_csv(index: List[Dict[str, Any]]) -> str:
    """Return CSV string for download."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["page", "view_type", "scale", "confidence", "status"])
    for r in index:
        writer.writerow([
            "" if r["page"] is None else r["page"],
            r["view_type"],
            r["scale"],
            "" if r["confidence"] is None else f"{r['confidence']:.2f}",
            r["status"]
        ])
    return output.getvalue()
