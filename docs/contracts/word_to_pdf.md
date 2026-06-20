# Word → PDF Adapter Contract

## Purpose
Convert DOCX bytes to PDF bytes.

## Adapter
- File: `CeayDocs/services/operations/word_to_pdf_adapter.py`
- Function: `word_to_pdf_adapter(docx_bytes: bytes) -> bytes`

## Inputs
- `docx_bytes: bytes`

## Outputs
- `pdf_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.ConversionError` on conversion failures.

## Dependencies
- `CeayDocs/utils/convert.py` → `word_to_pdf(docx_bytes) -> pdf_bytes`
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp files created by `utils.convert`.
- May invoke LibreOffice via subprocess (if installed).

## Compatibility notes
- `utils.convert.word_to_pdf` may return a minimal dummy PDF when LibreOffice is missing.
- Adapter maintains bytes→bytes stability regardless of the underlying fallback.

## Future migration notes
- Make dummy fallback explicit/policy-controlled.
- Improve mapping of missing LibreOffice to `UnsupportedFormatError` or `FileValidationError` (if desired later).

