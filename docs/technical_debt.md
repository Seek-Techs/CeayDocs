# CeayDocs Technical Debt Report (Phase 2B)

## Scope
Documents remaining weaknesses observed in the Phase 2B adapter/contract layer.

## Remaining duplication
- Adapters currently implement similar `try/except + logging + elapsed_time` scaffolding per operation.
- Some utilities expose mixed signatures (bytes/path, bytes/True/None), forcing adapter/ops normalization.

## Coupling concerns
- Adapters depend directly on `core.logger` and `core.telemetry` logging format.
- Ops layer wraps util functions in a way that can expose util contract quirks (e.g., split-PDF historical signature mismatch).

## Potential bottlenecks
- Converters relying on external processes:
  - LibreOffice (Word→PDF)
  - Ghostscript (compression)
- PDF image rendering via PyMuPDF can be CPU/memory heavy.

## Risk areas
- **Exception mapping consistency**: adapters mostly rethrow as `ConversionError` / `CompressionError` without distinguishing file validation vs unsupported formats vs OCR/extraction-specific failures.
- **Behavioral policy drift**: utilities may return dummy outputs when external dependencies are missing (e.g., LibreOffice fallback), which can mask real conversion issues.
- **Contract ambiguity in utils**: split/merge/convert utilities have legacy compatibility behaviors that require adapter normalization.

## Refactoring candidates (future)
- Introduce a shared adapter base helper to eliminate repeated logging/elapsed_time/typing patterns.
- Standardize util signatures (or wrap them with clean internal bytes APIs) to reduce adapter/ops complexity.
- Centralize exception translation per operation category.

## Migration risks
- Tightening adapter exception mapping might change what exception type callers observe.
- Introducing stricter validation (e.g., empty image list handling) could break legacy callers relying on current utility behavior.

## Priority ranking (highest first)
1. Strengthen exception mapping granularity across adapters.
2. Add adapter test coverage for failure-paths, exception translation, telemetry, and logging.
3. Standardize/encapsulate utility fallback policies (LibreOffice/Ghostscript).
4. Reduce adapter boilerplate via shared internal helpers.

