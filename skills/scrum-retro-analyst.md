---
name: scrum-retro-analyst
description: Phase 6: Scrum Master. Finalizes the session, performs log rotation, and updates retrospective knowledge. Use after Phase 5 (Auditor Verification) is complete to archive the current sprint logs and preserve session memory.
allowed-tools:
  - Bash(python3 scripts/scrum_guard.py *)
  - Bash(cat)
  - Bash(ls)
  - Bash(mv)
  - Bash(cp)
metadata:
  role: Scrum Master
  phase: 6
  principle: Simplicity First
---

### Phase 6: Scrum Retrospective & Log Rotation

#### 1. Log-Before-Act Protocol
You **MUST** record the start of the retrospective phase in the audit trail to ensure the final record is captured.
`!python3 scripts/scrum_guard.py --phase 6 --session ${CLAUDE_SESSION_ID} --msg "START: Initiating retrospective, log rotation, and knowledge archival for BKI-XXX."`

#### 2. Log Rotation & Archival
To prevent the active log from exceeding context limits, you must perform log rotation.
1.  **Analyze Log Volume**: Check the size of the current `log.md`.
2.  **Archive History**: Move the detailed logs for the completed BKI-XXX to an archive directory (e.g., `logs/archive/BKI-XXX_log.md`) to preserve the full audit trail.
3.  **Summarization**: Generate a high-level summary of the implementation and technical decisions. This summary will be carried forward to preserve "session memory" efficiently in future sprints.

#### 3. Update Retro-Knowledge
Maintain the project's long-term intelligence by capturing lessons learned.
1.  **Synthesize Findings**: Identify any recurring issues, technical debt, or mistakes encountered during the lifecycle of BKI-XXX.
2.  **Update retro-knowledge.md**: Append these insights to `references/retro-knowledge.md`. This ensures future Phase 1 "Think Before Acting" steps can avoid repeating historical mistakes.

#### 4. Final Cleanup
Ensure the project is ready for the next BKI.
1.  **Orphan Check**: Final verification that no temporary artifacts or "ghost work" remain in the workspace.
2.  **Session Closure**: Clear any temporary session-specific variables or state.

#### 5. Handoff & Completion
1.  **Log Completion**: 
    `!python3 scripts/scrum_guard.py --phase 6 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: BKI-XXX cycle closed. Logs rotated and knowledge base updated."`
2.  **Final Step**: Notify the user: "Phase 6 complete. BKI-XXX is officially closed and archived. Would you like to review the updated retro-knowledge or start a new BKI (Phase 1)?".
