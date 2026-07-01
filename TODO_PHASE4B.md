# TODO_PHASE4B (tests-only) — Phase 4B Coverage Expansion

## Step 0 — Coverage targets
- [x] Establish baseline coverage (~54%) and identify 0%-covered targets.

## Step 1 — Add focused tests (analyzer / drawing_index / rule_engine / model)
- [ ] Create new test file for `services/analyzer.py` with dependency mocks.
  - [ ] Success path output structure
  - [ ] `_read_bytes` invalid input exception path
  - [ ] classify_pdf exception path
  - [ ] classify_pdf_views/detect_scales/split_views_into_pdfs exception paths
  - [ ] CSV generation exception swallowed path

- [ ] Create new test file for `services/drawing_index.py`
  - [ ] generate_index confidence None / below threshold / OK
  - [ ] UNKNOWN view_type => REVIEW behavior
  - [ ] index sorting with None page
  - [ ] generate_qa missing required views
  - [ ] generate_qa scale inconsistency
  - [ ] generate_qa low_confidence_pages population
  - [ ] index_to_csv confidence formatting (None => empty string)

- [ ] Create new test file for `services/rule_engine.py`
  - [ ] UNKNOWN_PROJECT_TYPE branch
  - [ ] PASS branch
  - [ ] FAIL missing required view
  - [ ] FAIL invalid scale
  - [ ] FAIL low confidence

- [ ] Create new test file for `models/operation_response.py`
  - [ ] Cover dataclass initialization lines/fields.

## Step 2 — Run verification
- [ ] `pytest -q` (ensure all tests pass)
- [ ] `pytest --cov=core --cov=services --cov=utils --cov=api --cov=models --cov-fail-under=80`
- [ ] `python -m ruff check .`
- [ ] `python -m mypy .`
- [ ] `python -m bandit -r .`

## Step 3 — Update reporting
- [ ] Update `docs/phase4_report.md` with new coverage, new tests, ruff/mypy/bandit results.

