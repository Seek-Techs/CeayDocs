# Jobs & Workflows (Phase 3)

This document introduces domain models and a job execution architecture to prepare CeayDocs for:
- FastAPI
- CLI
- Desktop
- Batch processing
- Queued execution
- Future distributed workers

## Key Design Constraints
- **No changes to existing adapter APIs**
- **No behavior changes** in current flows
- Additive-only architecture for gradual migration

## Models
- `models/operation_request.py`
- `models/operation_response.py`
- `models/job.py`
- `models/operation_types.py`

These are lightweight dataclasses used by future frontends.

## Job Lifecycle (Proposed)
- PENDING
- RUNNING
- COMPLETED
- FAILED
- CANCELLED

## Job Executor
- `services/job_executor.py`
- Uses dependency injection: you provide an `operation_handler(request)`.
- Wraps execution with:
  - `core.telemetry.elapsed_time()`
  - `core.metrics.MetricsCollector.track()`

## Workflow Layer
- `services/workflow.py`
- Current Phase: single operation execution only.
- Future: chaining/batching/queue workers.

