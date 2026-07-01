# Security Scan Results (Phase 4A)

Source: `python -m bandit -r core services utils api models -f json -o bandit_results.json`

## Findings (non-zero issues)
Total detected issues (Low severity): **8**

### B110: `try/except/pass`
- `services/analyzer.py:22` (pass in exception handler)
- `services/analyzer.py:158` (pass in exception handler)

### B404: blacklist: subprocess module import
- `utils/compress.py:4` (import subprocess)
- `utils/convert.py:2` (import subprocess)

### B603: subprocess call (partial path / execution safety)
- `utils/compress.py:49` (`subprocess.run(cmd, check=True)`)
- `utils/convert.py:97` (`subprocess.run([...], check=True)`) 

### B607: start process with partial executable path
- `utils/convert.py:97` (libreoffice invocation)

### utils/merge.py
- `utils/merge.py:50` B110 try/except/pass

## False positive assessment / accepted risks
- These are mostly “policy” Bandit findings around subprocess usage and `except: pass` patterns.
- In this repo, document conversion typically requires invoking external tools (e.g., LibreOffice / Ghostscript / platform utilities). Therefore, these findings are **likely contextual** rather than indicative of injection.
- However, we should avoid behavior changes unless necessary; for Phase 4A gates, bandit “passes” depends on the CI thresholds (not adjusted yet).

## Recommended follow-up (if gates require strictness)
- If CI fails due to specific rules, address with targeted refactors:
  - replace broad `except Exception: pass` with explicit exception types and logging
  - ensure subprocess commands are constructed without untrusted string interpolation
  - restrict executables (e.g., configurable allowlist) and avoid partial executable paths


