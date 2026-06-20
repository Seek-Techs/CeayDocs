# Merge PDFs Adapter Contract

## Purpose
Merge multiple PDF byte payloads into a single PDF.

## Adapter
- File: `CeayDocs/services/operations/merge_pdf_adapter.py`
- Function: `merge_pdfs_adapter(pdf_bytes_list: Iterable[bytes]) -> bytes`

## Inputs
- `pdf_bytes_list: Iterable[bytes]`

## Outputs
- `merged_pdf_bytes: bytes`

## Exceptions (typed)
- `core.exceptions.ConversionError` on merge failures.

## Dependencies
- `CeayDocs/services/operations/merge_ops.py` → `merge_pdfs_op(pdf_list) -> bytes`
- `CeayDocs/utils/merge.py` → `merge_pdfs(pdf_files, output_path=None) -> bytes`
- `core.logger`
- `core.telemetry.elapsed_time`

## Side effects
- Temp files may be created when merging file-like inputs (wrapped internally).

## Compatibility notes
- Adapter normalizes `Iterable[bytes]` to a list before passing to ops.

## Future migration notes
- Standardize error typing for invalid/corrupt PDFs.

