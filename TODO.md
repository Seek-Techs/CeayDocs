# CeayDocs Refactor (Incremental)

## Phase 1 — Repository Audit (completed)
- [x] Inventory current architecture (Streamlit UI, FastAPI API, utils/services layers, existing tests).
- [x] Identify code smells, duplication, coupling, naming issues, exception handling weaknesses, dependency/performance risks.
- [x] Provide severity-ranked weaknesses + incremental refactoring recommendations.
- [x] Confirm Phase 1 is done; Phase 2 not yet implemented.

## Phase 2 — Architecture Refactoring (next: scaffolding, no behavior change)
- [ ] Create/standardize cross-cutting foundation:
  - [ ] `core/logger.py` (structured logging; timing + subprocess stderr capture hooks)
  - [ ] `core/exceptions.py` (typed internal exceptions)
  - [ ] `core/contracts.py` (byte-in/byte-out interfaces; adapters)
  - [ ] `core/telemetry.py` (optional: elapsed time helper, spans)
- [ ] Add adapters around existing `utils/*` to enforce stable operation contracts:
  - [ ] `services/operations/*` review for consistent signatures (bytes->bytes or path->bool)
  - [ ] Document the supported signatures per operation (including legacy compatibility)
- [ ] Normalize exception mapping:
  - [ ] single place to translate internal exceptions -> FastAPI HTTP responses
  - [ ] Streamlit-safe error formatting helpers
- [ ] Instrument subprocess-based ops:
  - [ ] LibreOffice (Word -> PDF)
  - [ ] Ghostscript (PDF compression)
  - [ ] Add logs for command + non-zero exit + stderr/stdout capture
- [ ] Improve temp-file hygiene + memory notes:
  - [ ] ensure temp files always removed via context managers / finally blocks
  - [ ] add bounded-memory notes where full-file reads occur

## Phase 3 — API-ready + job/execution model (optional but recommended after scaffolding)
- [ ] Introduce `services/jobs.py` (in-process job registry)
- [ ] Add job endpoints:
  - [ ] `POST /jobs` (create job)
  - [ ] `GET /jobs/{id}` (status)
  - [ ] map operations -> existing adapters
- [ ] Add request/response models (`models/`):
  - [ ] JobCreate, JobStatus, OperationResult

## Phase 4 — Testing & deployment readiness
- [ ] Expand unit tests:
  - [ ] contract tests for adapters (type guarantees)
  - [ ] error-path tests (empty upload, invalid ranges)
  - [ ] subprocess-failure tests (mock Ghostscript/LibreOffice)
- [ ] Add API tests using TestClient for at least convert/merge/compress
- [ ] Add CI updates:
  - [ ] run `python -m compileall`
  - [ ] run pytest
  - [ ] ensure optional deps are handled deterministically

## Phase 5 — Folder reorganization to target layout (no-op for runtime)
- [ ] Reorganize into target structure:
  - ceaydocs/
  - app/
  - ui/
  - streamlit/
  - components/
  - services/
  - pdf/
  - word/
  - image/
  - ocr/
  - compression/
  - core/
  - config.py
  - exceptions.py
  - logger.py
  - constants.py
  - models/
  - utils/
  - tests/
  - docs/
  - assets/
  - examples/
- [ ] Maintain compatibility import paths via shims until all callers updated.
- [ ] Update entrypoints (`app.py`, `api/main.py`) to new imports.

