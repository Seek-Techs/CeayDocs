# Images → PDF Adapter Contract

## Purpose
Convert a list of image byte payloads into a single PDF.

## Adapter
- File: `CeayDocs/services/operations/images_to_pdf_adapter.py`
- Function: `images_to_pdf_adapter(image_bytes_list: list[bytes]) -> bytes`

## Inputs
- `image_bytes_list: list[bytes]`

## Outputs
- `pdf_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.ConversionError` on conversion failures.

## Dependencies
- `CeayDocs/services/operations/images_ops.py` → `images_to_pdf_op(list[bytes]) -> bytes`
- `CeayDocs/utils/images.py` → `images_to_pdf(image_bytes_list) -> bytes`
- PIL
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- None beyond memory/CPU usage.

## Compatibility notes
- Util accepts file-like objects too; adapter enforces `list[bytes]`.
- Empty list returns `b""` (utility behavior).

## Future migration notes
- Consider making empty input a typed validation error.

