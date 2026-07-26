# services/rule_engine.py
from typing import Any, Dict, List, cast

from services.rules import RULE_TEMPLATES


def apply_rules(index: List[Dict[str, Any]], project_type: str) -> Dict[str, Any]:
    rules: dict[str, Any] | None = RULE_TEMPLATES.get(project_type.upper())
    if not rules:
        return {
            "status": "UNKNOWN_PROJECT_TYPE",
            "issues": [f"No rules defined for {project_type}"],
        }

    issues: list[str] = []

    # Check required views
    present_views = {row["view_type"] for row in index}
    allowed_scales: dict[str, list[str]] = cast(dict[str, list[str]], rules.get("allowed_scales", {}))
    for rv in cast(list[str], rules.get("required_views", [])):
        if rv not in present_views:
            issues.append(f"Missing required view: {rv}")

    # Check scales & confidence
    for row in index:
        vt = row["view_type"]
        sc = row["scale"]
        conf = row["confidence"]

        if vt in allowed_scales:
            if sc not in allowed_scales[vt]:
                issues.append(
                    f"Invalid scale on page {row['page']} "
                    f"for {vt}: {sc}"
                )

        if conf is not None and conf < cast(float, rules.get("min_confidence", 0.0)):
            issues.append(
                f"Low confidence on page {row['page']} ({vt})"
            )

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }
