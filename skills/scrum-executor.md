---
name: scrum-executor
description: Phase 4: Developer. Performs surgical implementation of the technical plan to pass Phase 3 TDD specs. Use after the QA has verified a failing (Red) test suite, Use when asks to "code" or "execute".
allowed-tools: Bash(python3 scripts/scrum_guard.py *) Bash(*)
metadata:
  role: Developer
  phase: 4
  principles: ["Surgical Changes", "Simplicity First"]
---

# Phase 4: Surgical Implementation (Green Phase)

## 1. Log-Before-Act Protocol
You MUST record the start of the execution phase in the audit trail to ensure deterministic resumption.
!python3 scripts/scrum_guard.py --phase 4 --session ${CLAUDE_SESSION_ID} --msg "START: Executing surgical implementation for BKI-XXX."

## 2. Context Re-Attachment
1. **Read Requirement**: Ingest `backlog/BKI-XXX_story.md` to confirm the target Acceptance Criteria (AC).
2. **Read Design**: Consult the Phase 2 Technical Plan and Surgical Impact Map to identify the exact files to modify.
3. **Analyze Tests**: Review the failing test suite from Phase 3 to understand the verifiable success criteria.

## 3. Surgical Implementation
Apply the **Surgical Changes** and **Simplicity First** principles:
1. **Minimal Edits**: Modify ONLY the files identified in the Phase 2 plan. Do not perform "drive-by refactoring" of adjacent code.
2. **Style Matching**: Follow the existing codebase style, even if you would do it differently.
3. **No Speculation**: Do not add features, abstractions, or "flexibility" not explicitly requested in the BKI.
4. **Orphan Cleanup**: Immediately remove any imports, variables, or functions that YOUR changes have rendered unused.

## 4. Verification (The Green Phase)
Execution is not complete until the goal-driven criteria are met.
1. **Run Tests**: Execute the Phase 3 test suite using the appropriate test runner.
2. **Loop Until Pass**: If tests fail, analyze the failure, adjust the implementation surgically, and re-run until all tests pass.
3. **Artifact Traceability**: Ensure any new files created include the `backlog_id: BKI-XXX` in their frontmatter.

## 5. Handoff & Logging
1. **Log Completion**: !python3 scripts/scrum_guard.py --phase 4 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: Implementation finalized and verified against TDD specs."
2. **Next Step**: Notify the user: "Phase 4 complete. Implementation passes all tests. Proceed to Phase 5 (Auditor Verification)?"
