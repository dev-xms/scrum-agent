---
name: tdd-verifier
description: Phase 5: Auditor. Performs final verification against the Definition of Done (DoD), updates the project changelog, and enforces the final Hard Gate. Use after the Developer has confirmed a passing test suite in Phase 4, Use when asks to "test" or "validate".
allowed-tools: 
  - Bash(python3 scripts/scrum_guard.py *)
  - Bash(python3 tests/scripts/run_unit_tests.py *)
  - Bash(python3 tests/scripts/run_e2e_tests.py *)
  - Bash(python3 tests/scripts/capture_screenshot.py *)
  - Bash(python3 scripts/read_file.py *)
  - Bash(python3 scripts/list_dir.py *)
metadata:
  role: Auditor
  phase: 5
  principle: Goal-Driven Execution
---

### Phase 5: Final Verification & DoD Gate

#### 1. Log-Before-Act Protocol
You **MUST** record the start of the verification phase in the audit trail to maintain the append-only record.
`!python3 scripts/scrum_guard.py --phase 5 --session ${CLAUDE_SESSION_ID} --msg "START: Initiating final auditor verification and DoD gate for BKI-XXX."`

#### 2. Requirement Reconciliation & Traceability
Before closure, you must verify that the implementation aligns perfectly with the initial intent.
1.  **Read Requirements**: Review `backlog/BKI-XXX_story.md` — run `python3 scripts/read_file.py backlog/BKI-XXX_story.md` to identify all **Gherkin Acceptance Criteria**.
2.  **Independent Test Run**: Do not rely on Phase 4 logs. Determine the sprint folder (format: `Sprint-N-BKI-XXX`). Run both suites independently:
    - Unit: `python3 tests/scripts/run_unit_tests.py BKI-XXX Sprint-N-BKI-XXX` — exits non-zero on failure; artifact saved to `tests/results/Sprint-N-BKI-XXX/`.
    - E2E (UI stories only): `python3 tests/scripts/run_e2e_tests.py BKI-XXX Sprint-N-BKI-XXX` — exits non-zero on failure; artifact saved.
    - If story has no UI (Phase 2 impact map contains no HTML/CSS), note: "E2E not applicable."
3.  **Traceability Audit**: Verify that all new or modified files include the `backlog_id: BKI-XXX` in their frontmatter.
4.  **Screenshot Artifact** (UI stories only): `python3 tests/scripts/capture_screenshot.py BKI-XXX Sprint-N-BKI-XXX` — starts static server, saves `tests/results/Sprint-N-BKI-XXX/BKI-XXX_ui.png`, kills server.

#### 2c. Regression Gate (All Stories) — HARD GATE
You **MUST** run this after Section 2 passes and before proceeding to Section 3.
1.  **Unit Regression**: `python3 tests/scripts/run_unit_tests.py regression Sprint-N-BKI-XXX` — saves `tests/results/Sprint-N-BKI-XXX/regression_unit.txt`. Exits non-zero on failure.
2.  **E2E Regression** (UI stories only): `python3 tests/scripts/run_e2e_tests.py regression Sprint-N-BKI-XXX` — saves `tests/results/Sprint-N-BKI-XXX/regression_e2e.txt`. Exits non-zero on failure.
3.  **Failure Triage**: If any regression fails on a test **outside** BKI-XXX scope — STOP. Do not proceed to Section 3. Log the blocker:
    `!python3 scripts/scrum_guard.py --phase 5 --session ${CLAUDE_SESSION_ID} --msg "BLOCKER: Regression failed outside BKI-XXX scope. Sprint closure blocked. Open new BKI to fix before closing."`
    Raise as a blocker and open a new BKI to fix the regression before closing this story.

#### 3. Artifact Review
Verify the implementation matches the Phase 2 Surgical Impact Map.
1.  **Impact Map Check**: Ensure the final implementation matches the **Surgical Impact Map** from Phase 2. Confirm no "ghost work" or unrequested features were added.

#### 4. Hard Gate: Definition of Done (DoD)
The **Definition of Done** is the final barrier. A story cannot be closed until these criteria are met:
1.  **Surgical Integrity**: Confirm that only the minimum required code was touched and that the codebase is clean of "orphans" (unused imports or variables).
2.  **Functional Verification**: Confirm that 100% of Gherkin scenarios defined in Phase 1 pass the verified tests.
3.  **E2E Verification** (UI stories): `python3 tests/scripts/run_e2e_tests.py BKI-XXX Sprint-N-BKI-XXX` passes. `tests/results/Sprint-N-BKI-XXX/BKI-XXX_e2e.txt` exists with passing output.
4.  **Test Artifacts**: `tests/results/Sprint-N-BKI-XXX/BKI-XXX_unit.txt` exists. Screenshot `tests/results/Sprint-N-BKI-XXX/BKI-XXX_ui.png` exists (UI stories only).
5.  **Regression Gate**: `tests/results/Sprint-N-BKI-XXX/regression_unit.txt` exists with 100% pass. For UI stories: `regression_e2e.txt` also exists with 100% pass.

#### 5. Handoff & Logging
1.  **Log Completion**: 
    `!python3 scripts/scrum_guard.py --phase 5 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: DoD Gate passed. BKI-XXX verified. CHANGELOG.md will be written in Phase 6."`
2.  **Next Step**: Notify the user: "Phase 5 complete. The implementation meets the Definition of Done. Proceed to Phase 6 (Scrum Retro) to archive the logs and update retro-knowledge?"