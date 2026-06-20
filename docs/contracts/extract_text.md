# Extract Text Adapter Contract

## Purpose
Extract plain text from PDF bytes.

## Adapter
- File: `CeayDocs/services/operations/extract_text_adapter.py`
- Function: `extract_text_adapter(pdf_bytes: bytes) -> str`

## Inputs
- `pdf_bytes: bytes`

## Outputs
- `text: str`

## Exceptions (typed)
- `core.exceptions.ConversionError` on extraction failures.

## Dependencies
- `CeayDocs/services/operations/extract_ops.py` → `extract_text_op(pdf_bytes) -> str`
- `CeayDocs/utils/extract.py` → `extract_text_from_pdf(pdf_bytes) -> str`
- `pdfminer.six`
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp file creation in `utils.extract`.

## Compatibility notes
- `utils/extract_compat.py` provides a legacy alias `extract_text(pdf_bytes|filelike) -> str`.

## Future migration notes
- Standardize mappings for corrupt PDFs vs unsupported/counted page failures.

