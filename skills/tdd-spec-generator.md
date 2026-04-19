---
name: tdd-spec-generator
description: Phase 3: QA Engineer. Generates a failing (Red) test suite based on Phase 1 Acceptance Criteria and Phase 2 Design. Use after the Architect has finalized the technical plan, Use when asks to "tdd" or "write test".
allowed-tools: Bash(python3 scripts/scrum_guard.py *) Bash(python3 *) Bash(pytest *) Bash(npm test *)
metadata:
  role: QA Engineer
  phase: 3
  principle: Goal-Driven Execution
---

# Phase 3: TDD Specification & Red-Phase Verification

## 1. Log-Before-Act Protocol
You MUST record the start of this phase in the audit trail to ensure deterministic session resumption.
!python3 scripts/scrum_guard.py --phase 3 --session ${CLAUDE_SESSION_ID} --msg "START: Generating TDD specifications for Red Phase."

## 2. Requirement Ingestion & Mapping
1. **Sync Requirements**: Read `backlog/BKI-XXX_story.md`. Focus specifically on the **Gherkin Acceptance Criteria** (Given/When/Then).
2. **Review Design**: Consult the Phase 2 Technical Plan to identify the target functions/classes designated for modification.
3. **Traceability**: Ensure every test case includes a comment or metadata referencing the `backlog_id` (BKI-XXX).

## 3. Test Suite Generation
Apply **Goal-Driven Execution** by defining exactly what success looks like.
1. **Scenario Mapping**: Create test files that directly correspond to each Gherkin scenario.
2. **Surgical Scope**: Write tests that focus strictly on the current BKI requirements. Avoid testing pre-existing features unless they are directly impacted.
3. **Environment Prep**: Initialize any necessary mock data or testing environments required for the scenarios.

## 4. Red Phase Execution (Hard Gate)
A task cannot proceed to Phase 4 (Execution) until success criteria are verified as **failing** [3, 7].
1. **Run Tests**: Execute the newly created test suite.
2. **Confirm Failure**: Verify that the tests fail as expected (The "Red" Phase). 
3. **Ambiguity Triage**: If a test fails for reasons unrelated to missing implementation (e.g., syntax errors in the test itself), fix the test specification until it correctly targets the requirement gap.

## 5. Handoff & Logging
1. **Log Completion**: !python3 scripts/scrum_guard.py --phase 3 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: Failing test suite verified. System is in Red Phase."
2. **Next Step**: Present the test results to the user and ask: "Phase 3 complete. Proceed to Phase 4 (Surgical Implementation)?"
