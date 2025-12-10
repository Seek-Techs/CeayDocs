from core.classify import classify_pdf
from services.view_classifier import classify_pdf_views
from services.view_splitter import split_views_into_pdfs
from services.scale_detector import detect_scales
from services.drawing_index import generate_index, generate_qa, index_to_csv
from typing import Dict, Any, List, Union
import logging
import io
import traceback

logger = logging.getLogger(__name__)


def _read_bytes(input_obj: Union[bytes, io.IOBase]) -> bytes:
    """Ensure we have raw bytes from either bytes or a file-like object."""
    if isinstance(input_obj, (bytes, bytearray)):
        return bytes(input_obj)
    if hasattr(input_obj, "read"):
        try:
            input_obj.seek(0)
        except Exception:
            pass
        return input_obj.read()
    raise TypeError("input must be bytes or a file-like object with read()")


def analyze_drawing(pdf_input: Union[bytes, io.IOBase]) -> Dict[str, Any]:
    """
    Analyze an engineering drawing PDF and return a consolidated report.

    The report includes:
    - classification: result from classify_pdf(...)
    - summary: counts of view types grouped by detected scale
    - pages: list of page-level info {page, view_type, confidence, scale}
    - split_pdfs: mapping of split file names -> bytes (as returned by split_views_into_pdfs)
    - files: list of split file names (keys of split_pdfs)
    - errors: list of error messages captured during processing
    """
    errors: List[str] = []
    try:
        pdf_bytes = _read_bytes(pdf_input)
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("Failed to read pdf input")
        return {
            "classification": {},
            "summary": {},
            "pages": [],
            "split_pdfs": {},
            "files": [],
            "errors": [f"Failed to read input: {exc}", tb],
        }

    # call services defensively
    classification = {}
    try:
        classification = classify_pdf(pdf_bytes) or {}
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("classify_pdf failed")
        errors.append(f"classify_pdf error: {exc}")
        errors.append(tb)

    views: List[Dict[str, Any]] = []
    try:
        raw_views = classify_pdf_views(pdf_bytes)
        if raw_views:
            views = list(raw_views)
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("classify_pdf_views failed")
        errors.append(f"classify_pdf_views error: {exc}")
        errors.append(tb)

    scales: List[Dict[str, Any]] = []
    try:
        raw_scales = detect_scales(pdf_bytes)
        if raw_scales:
            scales = list(raw_scales)
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("detect_scales failed")
        errors.append(f"detect_scales error: {exc}")
        errors.append(tb)

    split_pdfs: Dict[str, bytes] = {}
    try:
        sp = split_views_into_pdfs(pdf_bytes) or {}
        # ensure bytes values
        split_pdfs = {str(k): (v if isinstance(v, (bytes, bytearray)) else _read_bytes(v)) for k, v in sp.items()}
    except Exception as exc:
        tb = traceback.format_exc()
        logger.exception("split_views_into_pdfs failed")
        errors.append(f"split_views_into_pdfs error: {exc}")
        errors.append(tb)

    # Build a map of page -> scale for quick lookup
    scale_map: Dict[int, Any] = {}
    for s in scales:
        try:
            page_raw = s.get("page")
            page_num = int(page_raw) if page_raw is not None else None
            if page_num is not None:
                scale_map[page_num] = s.get("scale", "Unknown")
        except Exception:
            logger.debug("Skipping invalid scale entry: %s", s)
            continue

    enriched_pages: List[Dict[str, Any]] = []
    for v in views:
        try:
            page_raw = v.get("page")
            page_num = int(page_raw) if page_raw is not None else None
            view_type = v.get("view_type", "Unknown")
            raw_conf = v.get("confidence", None)

            confidence = (
                float(raw_conf)
                if isinstance(raw_conf, (int, float))
                else None
            )

            scale = scale_map.get(page_num, "Unknown")
            enriched_pages.append({
                "page": page_num,
                "view_type": view_type,
                "confidence": confidence,
                "scale": scale
            })
        except Exception:
            logger.debug("Skipping invalid view entry: %s", v)
            errors.append(f"Invalid view entry: {v}")

    # Build summary counts grouped by "view_type @ scale"
    summary: Dict[str, int] = {}
    for p in enriched_pages:
        key = f'{p.get("view_type","Unknown")} @ {p.get("scale","Unknown")}'
        summary.setdefault(key, 0)
        summary[key] += 1

    index = generate_index(enriched_pages)
    qa = generate_qa(index)

    result = {
        "classification": classification,
        "summary": summary,
        "pages": enriched_pages,
        "split_pdfs": split_pdfs,
        "files": list(split_pdfs.keys()),
        "index": index,
        "qa": qa,
    }

    try:
        csv_text = index_to_csv(index)
        result["index_csv"] = csv_text
    except Exception:
        # do not fail analysis if CSV generation fails
        pass
    if errors:
        result["errors"] = errors

    return result

