# Operations & Resources (Phase 2D)

## Goals
Improve operational reliability while preserving existing behavior and APIs.

## Resource Lifecycle
CeayDocs uses temporary files heavily (PDF → DOCX/PDF, PDF splitting, PDF → images, merges).

This phase introduces a minimal, opt-in resource lifecycle utility:

- `core/resource_manager.py`
  - `ResourceManager.register(path)` tracks temp paths
  - `ResourceManager.cleanup()` safely deletes registered paths
  - `ResourceManager` supports context-manager usage

### Usage (optional / future integration)
```python
from core.resource_manager import ResourceManager

with ResourceManager() as mgr:
    mgr.register(tmp_path)
    # perform operation
```

## Metrics Collection
`core/metrics.py` adds lightweight in-process metrics recording.

- `MetricsCollector.track(operation=..., file_size_bytes=...)`
- `get_metrics_collector()` provides a shared collector for unit tests and gradual adoption

Metrics are recorded in memory and optionally logged via `core.logger`.

## Telemetry
Existing `core.telemetry.elapsed_time()` continues to provide operation duration logging.

This phase keeps telemetry backward compatible; later phases can add a decorator-based API.

## Large-File Safeguards
Configuration:

- `core/config.py`
  - `MAX_FILE_SIZE` (default 25MB)

This phase adds unit tests ensuring the safeguard configuration exists and is valid.

> Note: Actual enforcement hooks are intentionally not wired into adapter/util flows in Phase 2D to avoid behavior changes.

## Cleanup Strategy (future)
A safe cleanup strategy should ensure registered temporary files are removed
on both success and failure paths.

This is implemented in the resource manager; integration into the existing
utils will be performed in a later phase.

