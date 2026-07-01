# Linting Strategy (Phase 4A)

Goal: reach CI-quality gate without breaking functionality or introducing new features.

## Ruff configuration (current)
`pyproject.toml` sets:
- `select = ["F", "E", "W", "I", "B"]` (lightweight checks)
- `line-length = 120`

## Current Ruff findings
From `python -m ruff check .`:

### Genuine issues (need code change)
- **B008**: `File(...)` used as argument default in FastAPI routers.
- **E501**: Several lines exceed configured line length.

Files reported:
- `api/routers/compress.py`
- `api/routers/convert.py`
- `api/routers/drawings.py`
- `api/routers/extract.py`
- `api/routers/images.py`
- `api/routers/merge.py`
- `api/routers/split.py`
- `app.py`
- `convert_pdf_to_docx.py`
- `services/operations/merge_pdf_adapter.py`

### Legacy / intentional patterns
No legacy categories were applied yet because only a single ruff run was executed and we have not inspected each violation in context.

## Planned remediation approach (no blanket disables)
1. Fix **E501** with safe line wrapping/refactoring.
2. Fix **B008** by restructuring FastAPI endpoint signatures so `File(...)` is created inside the function body or via module-level singleton.
3. Re-run `python -m ruff check .` and iterate until clean.
4. If a specific legacy violation is discovered to be intentional and changing it would add risk, apply:
   - per-file ignores, or
   - rule-specific ignores
   with justification in this document.


