---
name: tdd-spec-generator
description: Phase 3: QA Engineer. Generates a failing (Red) test suite based on Phase 1 Acceptance Criteria and Phase 2 Design. Use after the Architect has finalized the technical plan, Use when asks to "tdd" or "write test".
allowed-tools:
  - Bash(python3 scripts/scrum_guard.py *)
metadata:
  role: QA Engineer
  phase: 3
  principle: Goal-Driven Execution
---

# Phase 3: TDD Specification & Red-Phase Verification

## 1. Log-Before-Act Protocol
You MUST record the start of this phase in the audit trail to ensure deterministic session resumption.
!python3 scripts/scrum_guard.py --phase 3 --session ${CLAUDE_SESSION_ID} --msg "START: Generating TDD specifications for Red Phase."

## 1c. Script Execution Policy (Hard Rule)
ALL test execution and environment checks MUST be invoked via scripts in `tests/scripts/`. Direct CLI commands (`npx`, `pytest`, `node`, `python3 -m pytest`, etc.) are **FORBIDDEN**.
If a required script does not exist, write it first, save it to `tests/scripts/`, then invoke it.
This applies to: unit runs, E2E runs, environment checks, browser setup, and any other test-related command.

## 2. Requirement Ingestion & Mapping
1. **Sync Requirements**: Read `backlog/BKI-XXX_story.md`. Focus specifically on the **Gherkin Acceptance Criteria** (Given/When/Then).
2. **Review Design**: Consult the Phase 2 Technical Plan to identify the target functions/classes designated for modification.
3. **Traceability**: Ensure every test case includes a comment or metadata referencing the `backlog_id` (BKI-XXX).

## 3. Test Suite Generation
Apply **Goal-Driven Execution** by defining exactly what success looks like.
1. **Scenario Mapping**: Create test files that directly correspond to each Gherkin scenario.
2. **Surgical Scope**: Write tests that focus strictly on the current BKI requirements. Avoid testing pre-existing features unless they are directly impacted.
3. **Environment Prep**: Initialize any necessary mock data or testing environments required for the scenarios.

## 3b. E2E Spec Generation (UI Stories Only)

**Trigger**: Required if the Phase 2 Surgical Impact Map includes `src/index.html` or any `src/*.css` file. Otherwise skip and note: "No UI — E2E not required."

1. **Selector Audit**: Verify all interactive DOM elements in `src/index.html` have `data-testid` attributes. Required standard map:
   - `input-title`, `input-ingredients`, `input-instructions` — form inputs
   - `btn-save` — save button
   - `recipe-item` — each rendered recipe `<li>`
   - `btn-delete` — delete button per recipe
   - `empty-state` — empty list message
   - `error-message` — validation error display
   If any are missing, flag them as a Phase 4 implementation task before proceeding.

2. **Generate E2E Spec**: Create `tests/e2e/BKI-XXX.spec.js`. One Playwright test per Gherkin scenario. Rules:
   - Use `data-testid` selectors only (never CSS class or tag selectors).
   - Pre-seed localStorage via `page.evaluate()` for "Given" state — do not chain UI actions to create preconditions.
   - `beforeEach`: `page.goto('/')` + `localStorage.clear()` + `page.reload()`.

3. **E2E Red Phase Confirmation**: Run `python3 tests/scripts/run_e2e_tests.py BKI-XXX`. Confirm tests fail because implementation is missing (not syntax errors). Log: `"E2E Red Phase confirmed — N tests failing as expected."`

4. **Update Phase 3 log**: Include E2E test count alongside unit test count in the COMPLETED log message.

## 4. Red Phase Execution (Hard Gate)
A task cannot proceed to Phase 4 (Execution) until success criteria are verified as **failing** [3, 7].
1. **Run Tests**: Run `python3 tests/scripts/run_unit_tests.py BKI-XXX` (and `python3 tests/scripts/run_e2e_tests.py BKI-XXX` for UI stories).
2. **Confirm Failure**: Verify that the tests fail as expected (The "Red" Phase). 
3. **Ambiguity Triage**: If a test fails for reasons unrelated to missing implementation (e.g., syntax errors in the test itself), fix the test specification until it correctly targets the requirement gap.

## 5. Handoff & Logging
1. **Log Completion**: !python3 scripts/scrum_guard.py --phase 3 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: Failing test suite verified. System is in Red Phase."
2. **Next Step**: Present the test results to the user and ask: "Phase 3 complete. Proceed to Phase 4 (Surgical Implementation)?"
