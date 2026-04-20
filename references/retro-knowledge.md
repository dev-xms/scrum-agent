# Retro Knowledge & Lessons Learned

This document tracks historical process failures and successes to ensure continuous improvement of the Scrum Agent.

## ⚠️ Known Pitfalls (Conflict Detection)
*   **Assumption Trap**: In Sprint BKI-002, the agent assumed the database schema was SQL without checking. 
    *   *Rule*: Always run `python3 scripts/list_dir.py <path>` to verify technology stack before drafting ACs. (`ls -R` and `grep` are banned — use gate scripts only.)
*   **Over-Engineering**: In Sprint BKI-005, a simple utility was implemented as a class factory.
    *   *Rule*: Apply the "50-line test." If it can be done in 50 lines, reject 500-line abstractions.

## ✅ Process Best Practices
*   **Gherkin Clarity**: Acceptance Criteria (AC) written in Given/When/Then format reduced Phase 3 (TDD) generation errors by 40%.
*   **Log-Before-Act**: Writing the start of a phase to `log.md` prevented "ghost work" during session timeouts.

## 🔄 Active Improvement Actions
*   [ ] Improve the "Contradiction Check" in Phase 1 to specifically look for naming convention conflicts.
*   [ ] Ensure `tdd-spec-generator` (Phase 3) always includes edge-case testing for null inputs.

---

## 🏁 Sprint 1 Retrospective (BKI-001/002/003) — 2026-04-20

### Lessons Learned

*   **Gate Scripts Required**: Phase 3–5 raw bash commands (`npm test`, `cat`, `ls`) bypassed the audit trail. Discovered during Sprint 1 retro.
    *   *Rule*: No raw bash in skills/commands. Use `scripts/` equivalents only. Full policy in `references/workflow-guidance.md`.

*   **E2E Gap in Phase 5 DoD**: Sprint 1 had no UI test results, no screenshot, no Playwright spec — DoD was incomplete for UI stories.
    *   *Rule*: UI stories must produce `tests/results/Sprint-N-BKI-XXX/BKI-XXX_e2e.txt` and `tests/results/Sprint-N-BKI-XXX/BKI-XXX_ui.png`. Spec lives in `tests/e2e/BKI-XXX.spec.js`. Hard gate enforced in Phase 5.

*   **Skills ↔ Commands Drift**: `.claude/commands/` files were never updated during Sprint 1 — stale by end of sprint, causing `/slash-commands` to use outdated tool permissions.
    *   *Rule*: Phase 6 Section 4b drift check required before closing. `skills/*.md` = source of truth.

*   **Log Rotation Scope Incomplete**: Only `logs/log.md` rotated in Sprint 1 — `logs/scripts-records.log` was not archived.
    *   *Rule*: Phase 6 rotates both `logs/log.md` and `logs/scripts-records.log`. See `references/workflow-guidance.md` — Log Rotation Scope.

---

## ~~🌱 Pending BKI Seed — Playwright E2E Testing (registered: 2026-04-20)~~ ✅ EXECUTED as BKI-004 (2026-04-20)
- **Plan file**: `docs/superpowers/plans/2026-04-20-playwright-e2e-and-skill-updates.md`
- **Summary**: Delivered in Sprint 2 — Playwright infrastructure, data-testid attrs, 9 E2E specs, skills updated.

---

## 🏁 Sprint 2 Retrospective (BKI-004) — 2026-04-20

### Lessons Learned

*   **Jest picks up Playwright specs by default**: When `@playwright/test` is added to a Jest project, Jest will attempt to run `tests/e2e/*.spec.js` and fail with "Playwright Test did not expect test.beforeEach() to be called here."
    *   *Rule*: Any sprint adding Playwright to a Jest project MUST add `"testPathIgnorePatterns": ["<rootDir>/tests/e2e/"]` to the Jest config in `package.json` as part of Phase 4 implementation.

*   **New gate scripts need README documentation before Phase 6 closes**: `scripts/make_dir.py` was created mid-sprint (Phase 3) but was not in `scripts/README.md` until Phase 6. This created a temporary audit gap.
    *   *Rule*: When a new script is created in any phase, add its `scripts/README.md` entry in the same phase before moving on — not deferred to Phase 6.

*   **Executed BKI Seeds must be closed, not re-registered**: The Playwright seed was registered in Sprint 1 retro. Sprint 2 executed it. Phase 6 must mark the seed as executed rather than leaving it as an open action item.
    *   *Rule*: Phase 6 retro-knowledge update: search for any seed whose plan file maps to the completed BKI, strike it through and mark `✅ EXECUTED`, do not re-register.

---

## 🏁 Sprint 2 Retrospective Addendum — Test Artifacts Restructure (2026-04-20)

### Lessons Learned

*   **Test artifacts belong at top-level, not in `logs/`**: `logs/test-results/` and `logs/screenshots/` mixed test output with audit logs. `logs/` is for audit trail only.
    *   *Rule*: All test artifacts (unit txt, e2e txt, screenshots) go to `tests/results/Sprint-N-BKI-XXX/`. `logs/` is audit-only.

*   **Artifacts not sprint-scoped → overwritten on next sprint**: Flat `test-results/` means Sprint 3 artifacts overwrite Sprint 2 artifacts.
    *   *Rule*: Sprint folder format `Sprint-N-BKI-XXX` (e.g. `Sprint-2-BKI-004`). All 3 gate scripts take `[sprint-folder]` as second arg; defaults to `BKI-XXX` for backwards compat.

*   **No regression gate in Phase 5**: Phase 5 only ran BKI-scoped tests — no check that previous BKIs were still passing.
    *   *Rule*: Phase 5 Section 2c (HARD GATE) — after BKI suite passes, run full suite as `regression` and save `regression_unit.txt` + `regression_e2e.txt` to same sprint folder. Regression failure = blocker, do not close story.

---

## ~~🌱 Pending BKI Seed — Regression Gate Formalization (registered: 2026-04-20)~~ ✅ EXECUTED as BKI-001 (2026-04-20)
- **Summary**: Delivered in Sprint 3 — test runner scripts relocated to `tests/scripts/`, regression artifacts enforced, 11-test suite covers all 4 ACs.

---

## 🏁 Sprint 3 Retrospective (BKI-001) — 2026-04-20

### Lessons Learned

*   **Test runner scripts belong in `tests/scripts/`, not `scripts/`**: `scripts/` is for workflow gate scripts (scrum_guard, invest_validator, read_file, etc). Mixing test runners in the same dir couples workflow infra to project-specific test tooling.
    *   *Rule*: All `run_unit_tests.py`, `run_e2e_tests.py`, `capture_screenshot.py` variants live in `tests/scripts/`. The `sys.path.insert` in these scripts must resolve `script_logger.py` from `scripts/` via `os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts')`.

*   **Skills loaded from disk at skill-invoke time — stale skill content shown in session**: When a skill is invoked via the `Skill` tool, the skill file content at that moment is loaded. If Phase 4 updates a skill file, Phase 5's loaded skill content will show old paths. The executor must use the updated paths from the implementation, not the loaded skill text.
    *   *Rule*: Phase 5 and Phase 6 executors must cross-check loaded skill content against the current file on disk when path references are involved. If drift is detected, use the on-disk version.

*   **Regression artifact naming is inherent in the BKI-ID pattern**: `f"{artifact_dir}/{bki}_unit.txt"` with `bki="regression"` already produces `regression_unit.txt`. No branching or special-casing needed. The `regression` mode is just a conventional BKI-ID value.
    *   *Rule*: Document this invariant in `tests/scripts/README.md` so future sprints don't add unnecessary branching.