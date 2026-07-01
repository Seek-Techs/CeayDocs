# Coverage Gap Analysis (Phase 4A)

Generated from local run:
- `pytest ... --cov=core --cov=services --cov=utils --cov=api --cov=models`
- TOTAL: **54%** (branch enabled)
- 57 passed, 1 skipped (Ghostscript not installed)

## Highest-impact low-coverage modules
(Highest impact = low coverage + directly relevant to core workflows)

### 1) Services / Core workflow primitives (0–21% coverage)
- **services/analyzer.py**: 0% (104 stmts, all missed)
- **services/drawing_index.py**: 0% (65 stmts)
- **services/drawing_register.py**: 0% (16 stmts)
- **services/overrides.py**: 0% (12 stmts)
- **services/pdf_to_word.py**: 0% (15 stmts)
- **services/rule_engine.py**: 0% (21 stmts)
- **services/rules.py**: 0% (1 stmt)
- **services/scale_detector.py**: 0% (17 stmts)
- **services/view_classifier.py**: 0% (24 stmts)
- **services/view_splitter.py**: 0% (20 stmts)

**Expected gains:** very large (multiple files at 0%); likely the main reason overall coverage is far below target.

### 2) Models (0% / 100% imbalance)
- **models/operation_response.py**: 0% (10 stmts)

### 3) API / Adapters entrypoints (0% coverage)
- **api/main.py**: 0% (10 stmts)
- **services/operations/convert_ops.py**: 0% (6 stmts)
- **services/operations/images_ops.py**: 0% (6 stmts)
- **services/operations/images_to_pdf_adapter.py**: 0% (17 stmts)
- **services/operations/pdf_to_images_adapter.py**: 0% (17 stmts)
- **services/operations/pdf_to_word.py / services/operations/pdf_to_word_adapter.py**: varies (adapter is 91%, core pdf_to_word is 0)
- **api/deps.py**: 0 stmts so effectively irrelevant for coverage.

### 4) Utilities with sizable missed logic
- **utils/convert.py**: 67% (57 stmts, 15 miss + several missing branch paths)
- **utils/images.py**: 61% (56 stmts, 20 miss)
- **utils/compress.py**: 58% (27 stmts, 12 miss)
- **core/resource_manager.py**: 75% (36 stmts, 8 miss)
- **core/telemetry.py**: 74% (27 stmts, 7 miss)

## Uncovered branches / exception paths (from `term-missing` summary)
Known branch holes (examples surfaced by coverage report):

- **core/metrics.py**: missing branch path (`69` / `53->exit`)
- **services/operations/exception_mapper.py**: partial coverage; multiple missed exception branches
- **services/operations/merge_ops.py**: 88% with 1 missed line
- **services/operations/merge_pdf_adapter.py**: 79% with range misses
- **services/operations/pdf_to_word_adapter.py**: 91% with missing branch
- **services/operations/exception_mapper.py**: multiple missed exception mapping branches + branch part coverage
- **utils/convert.py**: several missing ranges and multiple missed call-sites
- **utils/images.py**: several missing ranges
- **utils/extract.py**: 88% with 1 missed line/branch

## Untested models
- **models/operation_response.py** (0%)

## Untested workflows
Based on 0% coverage in:
- `services/analyzer.py`
- `services/workflow.py` is 100% (already covered)
- rule engine + view classifier/splitter/scale detection are all 0% => likely workflow sub-stages are untested in their own modules.

## Untested utility functions
Primary missed utility functions:
- `utils/convert.py`
- `utils/compress.py`
- `utils/images.py`
- plus smaller holes in `utils/extract.py` and `utils/split.py` (80%)

## Suggested ranking by expected coverage gain
1. **services/** (analyzer, rule engine, drawing index/register, overrides, view classifier/splitter, scale detector, pdf_to_word)
2. **models/operation_response.py**
3. **API main/ops entrypoints** (`api/main.py`, `services/operations/*_ops.py` entrypoints, adapters with 0%)
4. **utils/** (`convert`, `compress`, `images`)
5. **core/resource_manager.py** and **core/telemetry.py**

## Estimated coverage gains (coarse)
- Fixing the suite of 0%-covered service workflow modules should provide the largest jump (likely tens of percentage points). Without those, raising from ~54% to 80% solely by patching small gaps is unlikely.

## Notes / constraints
- No production behavior changes are required for coverage-only work.
- Tests may need lightweight unit tests using mocks/stubs to avoid requiring external tools (e.g., Ghostscript), aligning with the repo’s existing test strategy (one test already skipped for missing Ghostscript).

