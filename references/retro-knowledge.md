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
    *   *Rule*: UI stories must produce `logs/test-results/BKI-XXX_e2e.txt` and `logs/screenshots/BKI-XXX_ui.png`. Spec lives in `tests/e2e/BKI-XXX.spec.js`. Hard gate enforced in Phase 5.

*   **Skills ↔ Commands Drift**: `.claude/commands/` files were never updated during Sprint 1 — stale by end of sprint, causing `/slash-commands` to use outdated tool permissions.
    *   *Rule*: Phase 6 Section 4b drift check required before closing. `skills/*.md` = source of truth.

*   **Log Rotation Scope Incomplete**: Only `logs/log.md` rotated in Sprint 1 — `logs/scripts-records.log` was not archived.
    *   *Rule*: Phase 6 rotates both `logs/log.md` and `logs/scripts-records.log`. See `references/workflow-guidance.md` — Log Rotation Scope.

---

## 🌱 Pending BKI Seed — Playwright E2E Testing (registered: 2026-04-20)
- **Plan file**: `docs/superpowers/plans/2026-04-20-playwright-e2e-and-skill-updates.md`
- **Summary**: Add Playwright E2E test infrastructure, data-testid attributes to src/index.html, E2E specs for all BKI-001/002/003 Gherkin scenarios.
- **Action**: Phase 1 of next sprint — BA must convert this to a `requirements/BKI-XXX.md` story before any execution.