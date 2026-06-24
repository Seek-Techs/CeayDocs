# Error handling + standardized operation results (Phase 2C)

## Purpose
Prepare CeayDocs for multiple frontends (Streamlit, FastAPI, CLI, desktop) by introducing a small
standard model for operation outcomes and user-safe error message translation.

## Components
### `core/result.py`
Defines `OperationResult`:
- `success: bool`
- `data: bytes | Any | None`
- `error: Exception | None`
- `message: str`

### `core/error_handlers.py`
Defines helpers to translate internal CeayDocs exceptions into user-facing messages
without exposing internal details.

### Message philosophy
- No stack traces or subprocess output are returned.
- Messages remain generic for unknown failures.

## Migration notes
- Existing adapters and API routes are not changed.
- Frontends can adopt `OperationResult` and `translate_error()` gradually.

