---
name: scrum-retro-analyst
description: Phase 6: Scrum Master. Finalizes the session, performs log rotation, and updates retrospective knowledge. Use after Phase 5 (Auditor Verification) is complete to archive the current sprint logs and preserve session memory, Use when asks to "review" or "retro".
allowed-tools:
  - Bash(python3 scripts/scrum_guard.py *)
  - Bash(python3 scripts/read_file.py *)
  - Bash(python3 scripts/list_dir.py *)
  - Bash(python3 scripts/move_file.py *)
  - Bash(python3 scripts/copy_file.py *)
  - Bash(python3 scripts/make_dir.py *)
metadata:
  role: Scrum Master
  phase: 6
  principle: Simplicity First
---

### Phase 6: Scrum Retrospective & Log Rotation

#### 1. Log-Before-Act Protocol
You **MUST** record the start of the retrospective phase in the audit trail to ensure the final record is captured.
`!python3 scripts/scrum_guard.py --phase 6 --session ${CLAUDE_SESSION_ID} --msg "START: Initiating retrospective, log rotation, and knowledge archival for BKI-XXX."`

#### 1b. Sprint Retrospective Dialog (Required)
Before any automated steps, engage the user in a retro dialog. User input enriches the retro-knowledge entry.

1. **Present Sprint Summary** (synthesize from `logs/log.md` and CHANGELOG.md):
   ```
   Sprint Summary — BKI-XXX
   ✅ Delivered: [feature summary]
   🔧 Technical Decisions: [key ADR decisions]
   ⚠️  Issues Encountered: [rework or blockers from logs]
   🧪 Coverage: [N unit tests, N E2E tests]
   ```

2. **Ask the three retro questions**:
   > "Sprint BKI-XXX is ready to close. Before I archive the logs:
   > 1. What went well this sprint?
   > 2. What should we improve next time?
   > 3. Anything specific to capture in retro-knowledge.md?
   >
   > (Answer all, skip any, or say 'nothing to add' to proceed.)"

3. **Capture user response**:
   - User answers → incorporate into retro-knowledge entry (pitfalls, best practices, sprint block)
   - "nothing to add" / skipped → note in sprint block: `(No additional user input this sprint.)`

4. **Do not proceed to Section 2 until user responds or explicitly declines.**

#### 2. Log Analysis & Summarization
Read the active log to synthesize a sprint summary for retro-knowledge. Do NOT rotate yet — rotation happens in Section 5b after the COMPLETED entry is written.
1.  **Read Log**: Run `python3 scripts/read_file.py logs/log.md` to review all phase transitions for BKI-XXX.
2.  **Summarization**: Generate a high-level summary of the implementation and technical decisions. This summary will feed into Section 3 (retro-knowledge) and Section 3b (CHANGELOG).

#### 3. Update Retro-Knowledge
Maintain long-term intelligence by capturing lessons and keeping the file token-lean.

##### 3a. Synthesize Findings
1. Identify recurring issues, technical debt, or process mistakes from BKI-XXX.
2. Incorporate user input from Section 1b dialog.
3. Draft the sprint block:
   ```
   ## 🏁 Sprint N Retrospective (BKI-XXX) — YYYY-MM-DD
   ### Lessons Learned
   * [Lesson 1]: [rule or action]
   (User-noted during retro: [user input, or "No additional user input this sprint."])
   ```

##### 3b. Rotation Gate — Sprint Count + Token Budget
1. Read current file: `python3 scripts/read_file.py references/retro-knowledge.md`
2. Count `## 🏁 Sprint` header lines in the file. Call this **S**.
3. Count total lines. Call this **L**.
4. **Rotation required if EITHER:**
   - **S >= 1** (appending new sprint block would create 2+ sprints — enforce "keep last 2" invariant), OR
   - **L > 120** (token budget exceeded)
5. **Rotation required** → Proceed to 3c before appending.
6. **No rotation** (S == 0 AND L ≤ 120) → Skip 3c. Append new sprint block, proceed to 3d.

##### 3c. Archive Excess Sprints + Executed Seeds (Only If Rotation Triggered)

**Classification rules — apply before writing anything:**
- **KEEP (sprint)**: The single most recent `## 🏁 Sprint N Retrospective` block by `YYYY-MM-DD` in header. If no sprint blocks exist, nothing to keep in this category.
- **ARCHIVE (sprint)**: All other sprint blocks (older dates), oldest first in archive.
- **KEEP (seeds)**: Any `## 🌱 Pending BKI Seed` entry whose header does NOT start with `~~`. Open/incomplete seeds — MUST NOT be archived.
- **ARCHIVE (seeds)**: Any seed entry whose header starts with `~~## 🌱 Pending BKI Seed~~` or contains `✅ EXECUTED as`. Executed seeds.
- **KEEP (static)**: All content before the first sprint/seed block (Known Pitfalls, Best Practices, Active Improvement Actions) — verbatim.

**Steps:**
1. `python3 scripts/make_dir.py references/archive`
2. Classify all content using rules above into ARCHIVE set and KEEP set.
3. **If ARCHIVE set is non-empty**, write `references/archive/retro-YYYY-MM-DD.md` (today's date):
   ```
   # Retro Archive — YYYY-MM-DD
   Archived from `references/retro-knowledge.md` during BKI-XXX Phase 6 rotation.

   ## Archived Sprint Retrospectives
   [Each archived 🏁 sprint block verbatim, oldest first]

   ## Archived Executed Seeds
   [Each archived ~~🌱~~ seed entry verbatim, original order]
   ```
   Omit a section if its content is empty.
4. Rewrite `references/retro-knowledge.md` (in this exact order):
   - Static header sections — verbatim
   - Open `## 🌱 Pending BKI Seed` entries — verbatim, original order
   - 1 kept sprint block (most recent prior) — verbatim
   - New sprint block from 3a
   - If archive file was written: `<!-- Last archive: references/archive/retro-YYYY-MM-DD.md -->`
5. Verify: `python3 scripts/read_file.py references/retro-knowledge.md`
   - File has ≤ 2 `## 🏁 Sprint` headers
   - Zero `~~` struck-through seed headers remain
   - All open seeds from original file are present

##### 3d. Plan Artifact Registration (BKI Seeds)
Check `docs/superpowers/plans/` for plan files created this sprint. For each, append a "Pending BKI Seed" entry to `references/retro-knowledge.md`:

```
## 🌱 Pending BKI Seed — [Plan Title] (registered: YYYY-MM-DD)
- **Plan file**: `docs/superpowers/plans/<filename>.md`
- **Summary**: [one-line description of what the plan proposes]
- **Action**: Phase 1 of next sprint — BA must convert this to a `requirements/BKI-XXX.md` story before any execution.
```

Also strike through any seeds that map to the just-completed BKI: `~~## 🌱 Pending BKI Seed~~` → `✅ EXECUTED as BKI-XXX (DATE)`.

This is the **only** mechanism by which plan artifacts re-enter the workflow. Do not execute plan files directly.

#### 3b. Write CHANGELOG.md (Full Sprint Entry)
Phase 6 owns the full CHANGELOG entry. Phase 5 verified the implementation; Phase 6 documents it.

**Step 1 — Write the feature block** (append to CHANGELOG.md):

```markdown
## [BKI-XXX] — YYYY-MM-DD — [Story Title]

### Summary
[One-paragraph summary of what was delivered]

### Changes
- **Created/Modified** `path/to/file` — [what it does]
[... one line per impacted file from Phase 2 Impact Map ...]

### Requirements Traceability
- AC-1: [test name(s)] — PASS
- AC-2: [test name(s)] — PASS
[... one line per AC ...]

### Test Artifacts
- `tests/results/Sprint-N-BKI-XXX/BKI-XXX_unit.txt` — N passed
- `tests/results/Sprint-N-BKI-XXX/regression_unit.txt` — N passed
[Add E2E and screenshot lines if UI story]
```

**Step 2 — Append the retro addendum** (append under the feature block):

```markdown
### Retro Addendum (Post-Sprint N — YYYY-MM-DD)
- **Sprint closure**: BKI-XXX officially closed by Phase 6 retro.
- **Post-sprint fixes**: [Process/workflow fixes found during retro. If none: "None."]
- **BKI Seeds registered**: [Seeds added to retro-knowledge.md. If none: "None."]
- **Retro-knowledge rotation**: ["Sprints [list] + executed seeds archived to references/archive/retro-YYYY-MM-DD.md. Open seeds preserved." or "No rotation — first sprint, no prior blocks to archive." or "Rotation triggered by L>120; executed seeds archived."]
```

Rules:
- Feature block sources from Phase 2 Impact Map + Phase 5 test results
- Retro addendum = process/workflow changes only (not code changes)
- Never modify an existing CHANGELOG entry
- Both steps are append-only

#### 4. Final Cleanup
Ensure the project is ready for the next BKI.
1.  **Orphan Check**: Final verification that no temporary artifacts or "ghost work" remain in the workspace.
2.  **Session Closure**: Clear any temporary session-specific variables or state.

#### 4b. Skills ↔ Commands Sync & Scripts Audit
These checks prevent silent drift between the canonical skills and the slash-commands Claude Code exposes.

1. **Skill/Command Drift Check**: Run `python3 scripts/list_dir.py skills/` to enumerate all skill files. For each skill file, verify `.claude/commands/<name>.md` has identical content. If any diff is found, overwrite the command file with the skill content. This ensures `/slash-commands` always use current tool permissions and instructions.

2. **Scripts Audit**: Run `python3 scripts/list_dir.py scripts/` and verify every `.py` and `.sh` file is documented in `scripts/README.md`. If any script is missing, add it before proceeding to Section 5.

3. **Retro-Knowledge Raw Command Check**: Scan `references/retro-knowledge.md` for any raw shell commands (`ls`, `cat`, `mv`, `cp`, `npm`, `pytest`, `npx`) that violate the Script Execution Policy. Update them to their `scripts/` equivalents and note the fix in the retro synthesis.

#### 5. Handoff & Completion
1.  **Log Completion**: 
    `!python3 scripts/scrum_guard.py --phase 6 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: BKI-XXX cycle closed. Logs rotated and knowledge base updated."`
2.  **Final Step**: Notify the user: "Phase 6 complete. BKI-XXX is officially closed and archived. Would you like to review the updated retro-knowledge or start a new BKI (Phase 1)?".

#### 5b. Log Rotation & Archival (After Completion Entry)
Rotate AFTER Section 5 so the COMPLETED entry is captured in the archive — not orphaned outside it.
1.  **Ensure archive dir**: `python3 scripts/make_dir.py logs/archive`
2.  **Archive log.md**: `python3 scripts/move_file.py logs/log.md logs/archive/BKI-XXX_log.md`
3.  **Archive scripts-records.log**: `python3 scripts/move_file.py logs/scripts-records.log logs/archive/BKI-XXX_scripts-records.log`
