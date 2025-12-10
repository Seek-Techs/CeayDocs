# services/rule_engine.py
from typing import Dict, Any, List
from services.rules import RULE_TEMPLATES

def apply_rules(index: List[Dict[str, Any]], project_type: str) -> Dict[str, Any]:
    rules = RULE_TEMPLATES.get(project_type.upper())
    if not rules:
        return {
            "status": "UNKNOWN_PROJECT_TYPE",
            "issues": [f"No rules defined for {project_type}"],
        }

    issues = []

    # Check required views
    present_views = {row["view_type"] for row in index}
    for rv in rules["required_views"]:
        if rv not in present_views:
            issues.append(f"Missing required view: {rv}")

    # Check scales & confidence
    for row in index:
        vt = row["view_type"]
        sc = row["scale"]
        conf = row["confidence"]

        if vt in rules["allowed_scales"]:
            if sc not in rules["allowed_scales"][vt]:
                issues.append(
                    f"Invalid scale on page {row['page']} "
                    f"for {vt}: {sc}"
                )

        if conf is not None and conf < rules["min_confidence"]:
            issues.append(
                f"Low confidence on page {row['page']} ({vt})"
            )

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }
