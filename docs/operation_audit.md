# CeayDocs Phase 2B — Operation Audit & Compatibility Report

This document audits the existing operations and their adapter layer.

> **Scope**: Phase 2B deliverables (audit/documentation/contract alignment). 
> **Constraint**: No runtime behavior changes.

---

## PDF → Word

### Purpose
Convert a PDF document into a DOCX (Word) document.

### Current implementation location
- `CeayDocs/utils/convert.py`: `pdf_to_word()`

### Adapter location
- `CeayDocs/services/operations/pdf_to_word_adapter.py`: `pdf_to_word_adapter()`

### Current signature
In `utils.convert`:
- `pdf_to_word(pdf: bytes | Path | str, output: Path | str | None = None)`
  - **bytes input + no output** → returns `docx_bytes`
  - **path input + output provided** → writes output and returns `True`

In adapter:
- `pdf_to_word_adapter(pdf_bytes: bytes) -> bytes`

### Canonical signature (recommended)
```python
pdf_to_word_bytes(pdf_bytes: bytes) -> bytes
```

### Input types
- bytes (canonical for adapter)
- additionally: `Path | str` for legacy utility use

### Output types
- bytes (adapter)
- additionally: `True` (legacy path-based write)

### Side effects
- Temp files are created in `utils.convert` during conversion.
- If used in path mode: writes a `.docx` file.

### External dependencies
- `pdf2docx` (`pdf2docx.Converter`)

### Error conditions
- Conversion failures from `pdf2docx`.
- Invalid inputs (non-PDF bytes, empty data).

### Compatibility concerns
- Utility supports both bytes→bytes and path→True write semantics.
- Adapters currently enforce bytes→bytes.

### Recommended future contract
- Adopt bytes→bytes as the stable interface for UI/API.

---

## Word → PDF

### Purpose
Convert a Word (DOCX) document into a PDF.

### Current implementation location
- `CeayDocs/utils/convert.py`: `word_to_pdf()`

### Adapter location
- `CeayDocs/services/operations/word_to_pdf_adapter.py`: `word_to_pdf_adapter()`

### Current signature
In `utils.convert`:
- `word_to_pdf(docx: bytes | Path | str, output: Path | str | None = None)`
  - **bytes input + no output** → returns `pdf_bytes`
  - **path input + output provided** → writes output and returns `True`

In adapter:
- `word_to_pdf_adapter(docx_bytes: bytes) -> bytes`

### Canonical signature (recommended)
```python
word_to_pdf_bytes(docx_bytes: bytes) -> bytes
```

### Input types
- bytes (canonical for adapter)
- additionally: `Path | str` for legacy utility use

### Output types
- bytes (adapter)
- additionally: `True` (legacy path-based write)

### Side effects
- Temp files are created in `utils.convert`.
- If LibreOffice is missing, `utils.convert` returns a minimal dummy PDF to keep tests/dev working.
- If LibreOffice is present: runs LibreOffice subprocess.

### External dependencies
- `libreoffice` (LibreOffice executable)
- `subprocess.run`

### Error conditions
- LibreOffice required for true conversion may be missing.
- Subprocess errors when LibreOffice fails.

### Compatibility concerns
- Utility’s “missing LibreOffice” behavior returns dummy PDF bytes, which is a behavioral inconsistency relative to “real conversion”.
- Adapters currently wrap exceptions rather than validating conversion quality.

### Recommended future contract
- Make “dummy PDF fallback” an explicit policy (or remove in production) while keeping adapter interface stable.

---

## Merge PDFs

### Purpose
Merge multiple PDFs into a single PDF.

### Current implementation location
- `CeayDocs/utils/merge.py`: `merge_pdfs(pdf_files, output_path=None)`

### Adapter location
- `CeayDocs/services/operations/merge_pdf_adapter.py`: `merge_pdfs_adapter()`

### Current signature
In `utils.merge`:
- `merge_pdfs(pdf_files, output_path=None) -> bytes | True`
  - if `output_path` provided → writes output and returns `True`
  - else → returns merged PDF bytes

In adapter:
- `merge_pdfs_adapter(pdf_bytes_list: Iterable[bytes]) -> bytes`

### Canonical signature (recommended)
```python
merge_pdfs_bytes(pdf_bytes_list: Iterable[bytes]) -> bytes
```

### Input types
- adapter: iterable of bytes
- util: paths/str or file-like objects

### Output types
- bytes (adapter)
- additionally: `True` in path-mode util

### Side effects
- Temp files may be created when file-like objects are provided.
- If `output_path` used: writes file.

### External dependencies
- `PyPDF2.PdfMerger`
- uses `tempfile` and `os` for temp cleanup

### Error conditions
- Invalid PDFs / read errors.

### Compatibility concerns
- `merge_pdfs` accepts a wider range than adapters.
- Adapters normalize to bytes-only.

### Recommended future contract
- Standardize bytes input/output across UI/API.

---

## Split PDFs

### Purpose
Split a PDF and return a sub-range of pages.

### Current implementation location
- `CeayDocs/utils/split.py`: `split_pdf(pdf, output=None, start=1, end=1)`

### Adapter location
- `CeayDocs/services/operations/split_pdf_adapter.py`: `split_pdf_adapter()`

### Current signature
In `utils.split`:
- Historically mixed semantics exist:
  - path-based mode: writes output file and returns `None`
  - bytes-based mode is supported via internal `_split_pdf_bytes(...)`

In adapter:
- `split_pdf_adapter(pdf_bytes: bytes, start: int, end: int) -> bytes`

### Canonical signature (recommended)
```python
split_pdf_bytes(pdf_bytes: bytes, start_page: int, end_page: int) -> bytes
```

### Input types
- adapter: bytes

### Output types
- adapter: bytes

### Side effects
- Uses temp directory for PDF page extraction.

### External dependencies
- `PyPDF2.PdfReader`, `PyPDF2.PdfWriter`

### Error conditions
- Invalid page ranges.
- Corrupt PDFs.

### Compatibility concerns
- `split_pdf` historically had an ambiguous signature; contract was repaired for adapter compatibility (Phase 2B.0).

### Recommended future contract
- Expose a clean bytes→bytes API and keep path-based write as legacy.

---

## Compress PDFs

### Purpose
Compress a PDF file.

### Current implementation location
- `CeayDocs/utils/compress.py`: `compress_pdf(pdf_file)`

### Adapter location
- `CeayDocs/services/operations/compress_pdf_adapter.py`: `compress_pdf_adapter()`

### Current signature
In `utils.compress`:
- `compress_pdf(pdf_file)` expects a file-like object with `.read()`.
- returns compressed PDF bytes.

In adapter:
- `compress_pdf_adapter(pdf_bytes: bytes) -> bytes`

### Canonical signature (recommended)
```python
compress_pdf_bytes(pdf_bytes: bytes) -> bytes
```

### Input types
- adapter: bytes
- util: file-like

### Output types
- bytes

### Side effects
- Writes temp input/output files.
- Runs Ghostscript if available.

### External dependencies
- Ghostscript executable (`gs*`)
- fallback implementation (local module `compress_fallback`)
- `subprocess.run`

### Error conditions
- Ghostscript failures.
- Fallback failures.

### Compatibility concerns
- Adapters wrap generic errors into `CompressionError` but mapping granularity is not yet standardized.

### Recommended future contract
- Bytes→bytes stable interface with explicit error mapping.

---

## Extract Text

### Purpose
Extract text from a PDF.

### Current implementation location
- `CeayDocs/utils/extract.py`: `extract_text_from_pdf(pdf_bytes: bytes) -> str`

### Adapter location
- `CeayDocs/services/operations/extract_text_adapter.py`: `extract_text_adapter()`

### Current signature
In `utils.extract`:
- `extract_text_from_pdf(pdf_bytes: bytes) -> str`

In adapter:
- `extract_text_adapter(pdf_bytes: bytes) -> str`

### Canonical signature (recommended)
```python
extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str
```

### Input types
- bytes

### Output types
- str

### Side effects
- Temp file creation.

### External dependencies
- `pdfminer.six` (`pdfminer.high_level.extract_text`)

### Error conditions
- Corrupt PDFs.
- Extraction errors.

### Compatibility concerns
- `utils/extract_compat.py` exists as a wrapper alias: `extract_text(pdf_bytes) -> str`.

### Recommended future contract
- Keep both names, but standardize on bytes-only extraction for adapters.

---

## PDF → Images

### Purpose
Convert a PDF into images (ZIP bytes).

### Current implementation location
- `CeayDocs/utils/images.py`: `pdf_to_images(pdf)`

### Adapter location
- `CeayDocs/services/operations/pdf_to_images_adapter.py`: `pdf_to_images_adapter_zip()`

### Current signature
In `utils.images`:
- `pdf_to_images(pdf: object) -> list[PIL.Image] | bytes`
  - if file-like (has `.read`) → returns `list[Image.Image]`
  - otherwise (raw bytes) → returns ZIP bytes

In adapter:
- `pdf_to_images_adapter_zip(pdf_bytes: bytes) -> bytes`

### Canonical signature (recommended)
```python
pdf_to_images_zip(pdf_bytes: bytes) -> bytes
```

### Input types
- bytes

### Output types
- bytes (zip)

### Side effects
- Temp directory creation.

### External dependencies
- `PyMuPDF` (`fitz`)
- `PIL`
- `zipfile`

### Error conditions
- Corrupt PDFs.

### Compatibility concerns
- Utility returns `list[PIL.Image]` when passed file-like, which differs from adapter stable contract (zip bytes).

### Recommended future contract
- Make adapters always return zip bytes; keep list output for internal/UI needs.

---

## Images → PDF

### Purpose
Convert images into a PDF.

### Current implementation location
- `CeayDocs/utils/images.py`: `images_to_pdf(image_bytes_list)`

### Adapter location
- `CeayDocs/services/operations/images_to_pdf_adapter.py`: `images_to_pdf_adapter()`

### Current signature
In `utils.images`:
- `images_to_pdf(image_bytes_list)` where each item can be:
  - file-like with `.read()`
  - raw bytes
- returns PDF bytes

In adapter:
- `images_to_pdf_adapter(image_bytes_list: list[bytes]) -> bytes`

### Canonical signature (recommended)
```python
images_to_pdf_bytes(image_bytes_list: list[bytes]) -> bytes
```

### Input types
- list[bytes] (adapter)
- additionally: file-like items for util

### Output types
- bytes

### Side effects
- None beyond memory usage.

### External dependencies
- `PIL`

### Error conditions
- Invalid image bytes.
- Empty list: returns `b""`.

### Compatibility concerns
- Adapters enforce list[bytes]; callers passing file-like items should use util directly.

### Recommended future contract
- Standardize empty-list behavior (maybe raise FileValidationError in future) while keeping adapter interface stable.

---

## Inconsistencies & Technical Debt Summary

1. **Mixed signatures in utilities** (`bytes→bytes` vs `path→True/None`) require adapters/ops to normalize inputs and outputs.
2. **Operational dependency variability**:
   - Word→PDF depends on LibreOffice; in dev/CI environments it may return dummy PDFs.
3. **Bytes API ambiguity**:
   - Split-PDF historically had ambiguous bytes behavior; Phase 2B.0 repaired adapter compatibility.
4. **Exception mapping granularity** is not yet strict across adapters—many adapters raise generic conversion/compression exceptions without distinguishing file validation/unsupported format/OCR failure classes.


