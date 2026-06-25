# Dependency Management (Phase 4)

## Update Process
1. Prefer small, single-purpose updates.
2. Pin versions in `requirements.txt`.
3. Run full test suite + ruff + mypy + bandit.

## Security Update Process
- Apply security patches first.
- Re-run security scan (bandit) and tests.

## Version Pinning Strategy
- Use explicit pins where possible in `requirements.txt`.

## Supported Python Versions
- Primary: 3.11+

