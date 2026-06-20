# PDF → Word Adapter Contract

## Purpose
Convert PDF bytes to DOCX bytes.

## Adapter
- File: `CeayDocs/services/operations/pdf_to_word_adapter.py`
- Function: `pdf_to_word_adapter(pdf_bytes: bytes) -> bytes`

## Inputs
- `pdf_bytes: bytes`

## Outputs
- `docx_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.ConversionError` on conversion failures.

## Dependencies
- `CeayDocs/utils/convert.py` → `pdf_to_word(pdf_bytes) -> docx_bytes`
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp files created by `utils.convert`.

## Compatibility notes
- Uses the bytes→bytes form of `utils.convert.pdf_to_word`.
- Preserves legacy behavior by not changing underlying utility signatures.

## Future migration notes
- Standardize exception mapping granularity across all adapters.
- Optionally document quality/validity checks for produced DOCX bytes.

