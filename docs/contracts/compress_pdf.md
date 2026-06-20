# Compress PDFs Adapter Contract

## Purpose
Compress PDF bytes.

## Adapter
- File: `CeayDocs/services/operations/compress_pdf_adapter.py`
- Function: `compress_pdf_adapter(pdf_bytes: bytes) -> bytes`

## Inputs
- `pdf_bytes: bytes`

## Outputs
- `compressed_pdf_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.CompressionError` on compression failures.

## Dependencies
- `CeayDocs/services/operations/compress_ops.py` → `compress_pdf_op(filelike) -> bytes`
- `CeayDocs/utils/compress.py` → `compress_pdf(pdf_file_like) -> bytes`
- Ghostscript (`gs*`) if available
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp files created by util.
- May invoke Ghostscript subprocess.

## Compatibility notes
- `utils.compress` may fall back to a pure-Python fallback when Ghostscript is unavailable.

## Future migration notes
- Improve exception typing for Ghostscript-specific failures.

