# CeayDocs Operation Adapter Contracts

This folder contains thin adapter wrappers around existing operations in `utils/*`.

## Contract standard (preferred)
**bytes -> bytes** and **bytes -> str**.

Adapters are responsible for:
- logging start/end and failures
- translating low-level exceptions into typed `core.exceptions.*`
- maintaining backward compatibility by calling existing implementations

## Adapters present
- `pdf_to_word_adapter(pdf_bytes: bytes) -> bytes`
- `word_to_pdf_adapter(docx_bytes: bytes) -> bytes`
- `merge_pdfs_adapter(pdf_bytes_list: Iterable[bytes]) -> bytes`
- `split_pdf_adapter(pdf_bytes: bytes, start: int, end: int) -> bytes`
- `compress_pdf_adapter(pdf_bytes: bytes) -> bytes`
- `extract_text_adapter(pdf_bytes: bytes) -> str`
- `pdf_to_images_adapter_zip(pdf_bytes: bytes) -> bytes` (zip bytes)
- `images_to_pdf_adapter(image_bytes_list: list[bytes]) -> bytes`

## Compatibility notes
- Existing Streamlit and FastAPI endpoints are unchanged in this phase.
- These adapters are introduced for future incremental adoption.

