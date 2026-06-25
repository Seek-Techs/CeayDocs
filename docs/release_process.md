# Release Process (Phase 4)

## Release Checklist
- Tests pass (`pytest`)
- Coverage >= 80%
- ruff passes
- mypy passes
- bandit scan completed

## Versioning Strategy
- Use semantic versioning for additive, non-breaking changes.

## Tagging Strategy
- Tag releases as `vX.Y.Z`.

## Rollback Strategy
- Revert the release commit; verify CI gate conditions.

