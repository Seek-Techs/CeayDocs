# TODO - Phase 4A Completion (Coverage & Quality Gates)

## Phase 4A Steps
- [ ] Understand repo quality gate configuration (coverage/ruff/mypy/bandit, CI workflow)
- [ ] Coverage gap analysis:
  - [ ] Identify lowest-covered modules
  - [ ] Identify uncovered branches
  - [ ] Identify untasted exception paths/workflows/models/utilities
  - [ ] Rank modules by impact and estimate coverage gains
  - [ ] Create docs/coverage_gap_analysis.md
- [ ] Ruff compliance plan:
  - [ ] Run ruff check
  - [ ] Classify violations (genuine/legacy/intentional)
  - [ ] Fix genuine issues
  - [ ] Document rationale in docs/linting_strategy.md
- [ ] Add tests only to raise coverage to >=80%
  - [ ] Target modules: core/, services/, models/, utils introduced in Phases 2–3
  - [ ] Cover success, failure, edge, boundary, and exception-handling paths
- [ ] Ensure mypy passes
  - [ ] Narrow types / add annotations only if needed
  - [ ] Document exclusions if any
- [ ] Ensure bandit passes
  - [ ] Run bandit and document findings/false positives/accepted risks
  - [ ] Create docs/security_scan_results.md
- [ ] Restore quality gates
  - [ ] Update coverage configuration to fail_under=80
  - [ ] Ensure CI fails on coverage/ruff/mypy/bandit
- [ ] CI verification
  - [ ] Run the same commands as GitHub workflow locally
  - [ ] Record results in final report
- [ ] Final report (docs + completion)
  - [ ] Coverage %, coverage increase, # new tests, ruff status, mypy status, bandit status, CI status, remaining debt, Phase 4 completion state

