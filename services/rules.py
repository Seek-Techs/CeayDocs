# services/rules.py

RULE_TEMPLATES = {
    "STRUCTURAL": {
        "required_views": ["PLAN", "SECTION", "ELEVATION"],
        "allowed_scales": {
            "PLAN": ["1:100", "1:50"],
            "SECTION": ["1:50", "1:25"],
            "ELEVATION": ["1:100", "1:50"],
        },
        "min_confidence": 0.6,
    },

    "ARCHITECTURAL": {
        "required_views": ["PLAN", "ELEVATION"],
        "allowed_scales": {
            "PLAN": ["1:100"],
            "ELEVATION": ["1:100"],
        },
        "min_confidence": 0.5,
    },

    "FOUNDATION": {
        "required_views": ["PLAN", "SECTION"],
        "allowed_scales": {
            "PLAN": ["1:50", "1:25"],
            "SECTION": ["1:25", "1:20"],
        },
        "min_confidence": 0.65,
    },
}
