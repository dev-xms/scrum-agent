---
name: scrum-ba-intake
description: Phase 1: Business Analyst. Refines raw requirements into validated User Stories. Use when the user provides new project goals, requirements, or asks to "create backlog" or "plan a sprint".
allowed-tools:
  - Bash(python3 scripts/list_dir.py *)
  - Bash(python3 scripts/read_file.py *)
  - Bash(python3 scripts/make_dir.py *)
  - Bash(python3 scripts/copy_file.py *)
  - Bash(python3 scripts/move_file.py *)
  - Bash(python3 scripts/scrum_guard.py *)
  - Bash(python3 scripts/invest_validator.py *)
metadata:
  role: Business Analyst
  phase: 1
  principle: Think Before Acting
---

# Phase 1: Requirement Discovery & BA Refinement

## 1. Log-Before-Act Protocol
Before any refinement begins, you MUST record the phase start in the audit trail to ensure session traceability.
!python3 scripts/scrum_guard.py --phase 1 --session ${CLAUDE_SESSION_ID} --msg "START: Initiating requirement intake and folder scan."

## 1b. Sprint Closure Guard (Hard Gate)
Before any new intake work begins, verify no prior sprint is open.

1. **Read the active log**: `python3 scripts/read_file.py logs/log.md`
2. **Scan for open sprints**: Find any `[PHASE 1] START` entry with no matching `[PHASE 6] COMPLETED` for the same BKI.
   - All sprints closed (or log is empty after rotation) → proceed to Section 2.
   - Open sprint found → **STOP IMMEDIATELY**:
     > "BLOCKED: Sprint [BKI-XXX] is still open — Phase 6 not completed. Run `/scrum-retro-analyst` to close the current sprint before starting a new one."

> Note: An empty `logs/log.md` means prior sprint was closed and logs were archived. This is safe — proceed.

## 2. Source Discovery & Synthesis
> **Script Enforcement (Hard Rule):** For ALL file/directory operations, use scripts in the `scripts/` folder ONLY. NEVER use raw Bash (`mkdir`, `cp`, `mv`, `cat`, `ls`, `find`). Available scripts: `make_dir.py`, `read_file.py`, `list_dir.py`, `copy_file.py`, `move_file.py`. If no suitable script exists, STOP and ask the user to create one before proceeding.

Apply the **Think Before Acting** principle by identifying all project context before drafting solutions.
1. **Raw Intake**: Scan the `requirements/` folder for new source documents — run `python3 scripts/list_dir.py requirements/`.
2. **Context Check**: Cross-reference raw input with `references/retro-knowledge.md` to avoid repeating historical mistakes.
3. **Ambiguity Triage**: If the requirement is vague, you MUST stop and seek clarification from the user before proceeding.

## 3. Backlog Drafting
If `backlog/` does not exist, run `python3 scripts/make_dir.py backlog` before creating the file.
Create a dedicated story file: `backlog/BKI-XXX_story.md` (replacing XXX with the next available ID).

> **Story Format:** Follow `references/gherkin-templates.md` exactly — bold markers, blockquote style, one phrase per line:
> ```
> **As a** [user type]
> **I want to** [specific action]
> **So that** [derived benefit/value]
> ```

- **Functional Requirements**: Use **Gherkin** syntax (Given/When/Then) for all Acceptance Criteria.
- **Non-Functional Requirements**: Use the standard checklist format found in `references/gherkin-templates.md`.

## 4. Deterministic DoR Gate (Hard Gate)
Requirements must be **Ready** before they can be **Designed**. You MUST run the automated validator to enforce the **INVEST** (Independent, Negotiable, Valuable, Estimable, Small, Testable) standard. 

**CRITICAL**: You are FORBIDDEN from transitioning to Phase 2 if this script fails.
!python3 scripts/invest_validator.py backlog/BKI-XXX_story.md

## 5. Handoff
If the DoR Gate passes:
- **Log Completion**: !python3 scripts/scrum_guard.py --phase 1 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: DoR passed. Ready for Phase 2."
- **Next Step**: Present the validated story to the user and ask: "Phase 1 complete. Proceed to Phase 2 (Architecture Design)?".
