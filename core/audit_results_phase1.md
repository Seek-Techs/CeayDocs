# CeayDocs — Phase 1 Audit Results

> Scope: incremental refactor audit only (no functional rewrite).

## Current Architecture (as implemented today)

### 1) UI Layer
- **Streamlit**: `CeayDocs/app.py`
  - Renders tool selection + upload widgets.
  - Calls `utils/*` functions directly.
  - Contains orchestration logic for the AEC drawing analyzer using `st.session_state`.

### 2) API Layer
- **FastAPI**: `CeayDocs/api/main.py`
  - Includes routers:
    - `api/routers/convert.py`, `compress.py`, `merge.py`, `split.py`, `extract.py`, `images.py`, `drawings.py`.
- Routers validate file types and dispatch to:
  - `utils/*` directly (e.g. convert)
  - or `services/operations/*` wrappers (e.g. compress/merge).

### 3) Operations / Domain Layer
- **Core document operations** live in:
  - `CeayDocs/utils/`
    - `convert.py`, `merge.py`, `split.py`, `extract.py`, `images.py`, `compress.py`, etc.
  - `CeayDocs/services/operations/`
    - Thin byte-in/byte-out adapters around `utils/*`.
- **AEC drawing/domain services** live in `CeayDocs/services/` (analyzer, rule engine, indexing/register/export).

### 4) Test Layer
- `CeayDocs/tests/` contains pytest smoke-ish tests for convert/compress/extract/images/merge/split.

### 5) Cross-cutting concerns (partially implemented)
- Error helpers exist at `CeayDocs/api/core/errors.py`.
- No consistent logging framework in the current code.

---

## Weaknesses / Smells (with severity)

### High severity
1) **Tight coupling & mixed responsibilities**
   - Streamlit `app.py` mixes:
     - UI rendering
     - orchestration
     - business/domain workflow for AEC analyzer
   - Impact:
     - hard to unit test (UI event loop entangled with processing)
     - harder to reuse the same logic for API/desktop

2) **Inconsistent contracts in `utils/*`**
   - Multiple functions accept different input shapes (bytes vs path vs file-like objects).
   - Multiple output types: `bytes` vs `True` vs `None`.
   - Example risks:
     - `utils/split.py` has an awkward/fragile signature pattern.
   - Impact:
     - brittle integration
     - increased chance of runtime errors
     - blocks “API-ready” and “desktop-ready” clean integration

### Medium severity
3) **Exception handling is fragmented**
   - Some routers raise inline `HTTPException`.
   - Error helpers exist but are not used consistently.
   - No single mapping layer for internal errors → user/API responses.

4) **Missing structured logging & subprocess visibility**
   - Operations that rely on external tools (Ghostscript, LibreOffice) do not consistently capture/log:
     - command
     - stdout/stderr
     - duration
     - exit codes
   - Impact:
     - poor debugging in production

5) **Performance & memory scaling risks**
   - Several operations read full files into memory.
   - PDF → Images may materialize many PIL images.
   - Impact:
     - may not scale to larger PDFs
     - risk of high RAM usage

### Low severity
6) **Naming/organization drift**
   - Current structure uses `utils/` for operations, but target architecture expects more granular domains (`pdf/`, `word/`, `image/`, `compression/`, etc.).
   - Docs don’t fully describe the current implementation layout.

---

## Refactoring Recommendations (incremental, preserve functionality)

### Recommendation 1: Define stable operation contracts
- Create adapters with strict signatures (byte-in/byte-out) around current implementations.
- Preserve legacy functions as shims.
- Example contract per operation:
  - `pdf_to_word_bytes(pdf_bytes: bytes) -> bytes`
  - `word_to_pdf_bytes(docx_bytes: bytes) -> bytes`
  - `compress_pdf_bytes(pdf_bytes: bytes, settings: …) -> bytes`
  - `merge_pdfs_bytes(pdfs: list[bytes]) -> bytes`
  - `split_pdf_bytes(pdf_bytes: bytes, start: int, end: int) -> bytes`
  - `extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str`
  - `pdf_to_images_zip_bytes(pdf_bytes: bytes) -> bytes`
  - `images_to_pdf_bytes(images: list[bytes]) -> bytes`

### Recommendation 2: Centralize exception types + mapping
- Add internal typed exceptions in `core/exceptions.py`.
- Add one mapper from internal exceptions to FastAPI HTTP responses and Streamlit messages.

### Recommendation 3: Add `core/logger.py`
- Standardize structured logging.
- For subprocess-based operations:
  - log command
  - capture stdout/stderr on failure
  - log duration and file sizes

### Recommendation 4: Improve test depth
- Keep existing tests.
- Add:
  - contract/type tests for adapter signatures
  - negative tests for invalid ranges/empty uploads
  - error-path tests (missing Ghostscript/LibreOffice)

---

## Phase Completion Check
- **Phase 1 (Repository Audit)**: Completed as a deliverable.
- **Phase 2 (Architecture Refactoring)**: Not started in code beyond wrappers; follow TODO.md for next steps.

