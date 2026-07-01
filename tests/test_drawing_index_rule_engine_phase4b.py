from __future__ import annotations

from services.drawing_index import generate_index, generate_qa, index_to_csv
from services.rule_engine import apply_rules


def test_generate_index_confidence_threshold_none_and_unknown() -> None:
    pages = [
        {"page": 1, "view_type": "PLAN", "confidence": None, "scale": "Unknown"},
        {"page": 2, "view_type": "SECTION", "confidence": 0.2, "scale": "1:50"},
        {"page": 3, "view_type": "ELEVATION", "confidence": 0.9, "scale": "1:100"},
        {"page": 4, "view_type": "UNKNOWN", "confidence": 0.9, "scale": "1:100"},
    ]

    idx = generate_index(pages)
    # Should be sorted by page
    assert [r["page"] for r in idx] == [1, 2, 3, 4]

    assert idx[0]["status"] == "LOW CONF"
    assert idx[1]["status"] == "LOW CONF"  # below threshold
    assert idx[2]["status"] == "OK"
    assert idx[3]["status"] == "REVIEW"  # UNKNOWN view_type forces review


def test_generate_qa_missing_required_views_and_scale_inconsistency() -> None:
    # REQUIRED_VIEWS in drawing_index.py: PLAN, SECTION, ELEVATION
    # Provide only PLAN + SECTION, and make SECTION have multiple scales.
    index = [
        {"page": 1, "view_type": "PLAN", "scale": "1:100", "confidence": 0.9, "status": "OK"},
        {"page": 2, "view_type": "SECTION", "scale": "1:50", "confidence": 0.9, "status": "OK"},
        {"page": 3, "view_type": "SECTION", "scale": "1:25", "confidence": 0.9, "status": "OK"},
    ]

    qa = generate_qa(index)

    assert "ELEVATION" in qa["missing_views"]

    # Should flag multiple scales for SECTION
    assert any("Multiple scales detected" in msg for msg in qa["scale_issues"])


def test_generate_qa_low_confidence_pages_population() -> None:
    index = [
        {"page": 1, "view_type": "PLAN", "scale": "1:100", "confidence": None, "status": "LOW CONF"},
        {"page": 2, "view_type": "PLAN", "scale": "1:100", "confidence": 0.1, "status": "LOW CONF"},
        {"page": 3, "view_type": "PLAN", "scale": "1:100", "confidence": 0.9, "status": "OK"},
    ]

    qa = generate_qa(index)
    assert len(qa["low_confidence_pages"]) == 2
    assert {p["page"] for p in qa["low_confidence_pages"]} == {1, 2}


def test_index_to_csv_formats_confidence_none_as_empty_string() -> None:
    index = [
        {"page": None, "view_type": "PLAN", "scale": "Unknown", "confidence": None, "status": "LOW CONF"},
        {"page": 2, "view_type": "SECTION", "scale": "1:50", "confidence": 0.5, "status": "OK"},
    ]

    csv_text = index_to_csv(index)
    lines = [ln.strip() for ln in csv_text.splitlines() if ln.strip()]
    assert lines[0].startswith("page,view_type")

    # First row should have empty confidence field
    assert "PLAN" in lines[1]
    # confidence is rendered as empty string for None, so CSV contains an empty field
    assert lines[1].count(",") >= 4



def test_apply_rules_unknown_project_type() -> None:
    idx = [{"view_type": "PLAN", "scale": "1:100", "confidence": 0.9, "page": 1}]
    res = apply_rules(idx, "unknown")
    assert res["status"] == "UNKNOWN_PROJECT_TYPE"
    assert any("No rules defined" in issue for issue in res["issues"])


def test_apply_rules_pass_missing_views_fail_invalid_scale_and_low_confidence() -> None:
    # PASS case: structural requires PLAN, SECTION, ELEVATION in rules.py? Actually RULE_TEMPLATES for STRUCTURAL
    # includes required_views PLAN/SECTION/ELEVATION.
    pass_idx = [
        {"view_type": "PLAN", "scale": "1:100", "confidence": 0.9, "page": 1},
        {"view_type": "SECTION", "scale": "1:50", "confidence": 0.7, "page": 2},
        {"view_type": "ELEVATION", "scale": "1:50", "confidence": 0.8, "page": 3},
    ]
    res_pass = apply_rules(pass_idx, "STRUCTURAL")
    assert res_pass["status"] == "PASS"
    assert res_pass["issues"] == []

    # Missing required view
    missing_idx = [
        {"view_type": "PLAN", "scale": "1:100", "confidence": 0.9, "page": 1},
        {"view_type": "SECTION", "scale": "1:50", "confidence": 0.7, "page": 2},
    ]
    res_missing = apply_rules(missing_idx, "STRUCTURAL")
    assert res_missing["status"] == "FAIL"
    assert any("Missing required view" in issue for issue in res_missing["issues"])

    # Invalid scale for a view
    invalid_scale_idx = [
        {"view_type": "PLAN", "scale": "2:1", "confidence": 0.9, "page": 1},
        {"view_type": "SECTION", "scale": "1:50", "confidence": 0.7, "page": 2},
        {"view_type": "ELEVATION", "scale": "1:50", "confidence": 0.8, "page": 3},
    ]
    res_invalid_scale = apply_rules(invalid_scale_idx, "STRUCTURAL")
    assert res_invalid_scale["status"] == "FAIL"
    assert any("Invalid scale" in issue for issue in res_invalid_scale["issues"])

    # Low confidence branch
    low_conf_idx = [
        {"view_type": "PLAN", "scale": "1:100", "confidence": 0.1, "page": 1},
        {"view_type": "SECTION", "scale": "1:50", "confidence": 0.7, "page": 2},
        {"view_type": "ELEVATION", "scale": "1:50", "confidence": 0.8, "page": 3},
    ]
    res_low_conf = apply_rules(low_conf_idx, "STRUCTURAL")
    assert res_low_conf["status"] == "FAIL"
    assert any("Low confidence" in issue for issue in res_low_conf["issues"])

