# PDF → Images Adapter Contract

## Purpose
Convert PDF bytes into a ZIP archive of PNG images.

## Adapter
- File: `CeayDocs/services/operations/pdf_to_images_adapter.py`
- Function: `pdf_to_images_adapter_zip(pdf_bytes: bytes) -> bytes`

## Inputs
- `pdf_bytes: bytes`

## Outputs
- `images_zip_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.ConversionError` on conversion failures.

## Dependencies
- `CeayDocs/utils/images.py` → `pdf_to_images(pdf_bytes) -> zip bytes`
- PyMuPDF (`fitz`)
- PIL
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp directory creation inside util.

## Compatibility notes
- Util supports file-like inputs returning `list[PIL.Image]`; this adapter targets the stable zip-bytes contract.

## Future migration notes
- Consider exposing both list-of-images and zip-bytes as separate explicit operations.

