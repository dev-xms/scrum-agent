---
name: tdd-verifier
description: Phase 5: Auditor. Performs final verification against the Definition of Done (DoD), updates the project changelog, and enforces the final Hard Gate. Use after the Developer has confirmed a passing test suite in Phase 4.
allowed-tools: 
  - Bash(python3 scripts/scrum_guard.py *)
  - Bash(pytest *)
  - Bash(npm test *)
  - Bash(cat)
  - Bash(ls)
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
1.  **Read Requirements**: Review `backlog/BKI-XXX_story.md` to identify all **Gherkin Acceptance Criteria**.
2.  **Independent Test Run**: Do not rely on Phase 4 logs. Re-run the full test suite one final time to ensure environment consistency and functional compliance.
3.  **Traceability Audit**: Verify that all new or modified files include the `backlog_id: BKI-XXX` in their frontmatter.

#### 3. Documentation & Changelog Update
Maintain the project's historical record by documenting the successful implementation.
1.  **Update CHANGELOG.md**: Append a new entry detailing the changes made for `BKI-XXX`, linking them to the validated requirements and technical decisions.
2.  **Artifact Review**: Ensure the final implementation matches the **Surgical Impact Map** from Phase 2. Confirm no "ghost work" or unrequested features were added.

#### 4. Hard Gate: Definition of Done (DoD)
The **Definition of Done** is the final barrier. A story cannot be closed until these criteria are met:
1.  **Surgical Integrity**: Confirm that only the minimum required code was touched and that the codebase is clean of "orphans" (unused imports or variables).
2.  **Functional Verification**: Confirm that 100% of Gherkin scenarios defined in Phase 1 pass the verified tests.

#### 5. Handoff & Logging
1.  **Log Completion**: 
    `!python3 scripts/scrum_guard.py --phase 5 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: DoD Gate passed. BKI-XXX verified and CHANGELOG.md updated."`
2.  **Next Step**: Notify the user: "Phase 5 complete. The implementation meets the Definition of Done. Proceed to Phase 6 (Scrum Retro) to archive the logs and update retro-knowledge?"