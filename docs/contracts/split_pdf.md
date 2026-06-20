# Split PDFs Adapter Contract

## Purpose
Split a PDF and return bytes for the selected page range.

## Adapter
- File: `CeayDocs/services/operations/split_pdf_adapter.py`
- Function: `split_pdf_adapter(pdf_bytes: bytes, start: int, end: int) -> bytes`

## Inputs
- `pdf_bytes: bytes`
- `start: int` (1-based start page)
- `end: int` (1-based end page)

## Outputs
- `split_pdf_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.ConversionError` on split failures.

## Dependencies
- `CeayDocs/services/operations/split_ops.py` → `split_pdf_op(pdf_bytes, start, end) -> bytes`
- `CeayDocs/utils/split.py` → internal `_split_pdf_bytes(...) -> bytes`
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp directory creation inside `utils.split`.

## Compatibility notes
- Phase 2B.0 repaired adapter/ops contract by using a bytes-compatible call path.
- The historical `utils.split.split_pdf` path-based signature (writing files/returning None) is treated as legacy.

## Future migration notes
- Optionally expose a stable public `split_pdf_bytes(...)` wrapper in `utils.split`.

