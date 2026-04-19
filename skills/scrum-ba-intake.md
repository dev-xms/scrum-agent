---
name: scrum-ba-intake
description: Phase 1: Business Analyst. Refines raw requirements into validated User Stories. Use when the user provides new project goals, requirements, or asks to "create backlog" or "plan a sprint".
allowed-tools: Bash(ls) Bash(python3 scripts/scrum_guard.py *) Bash(python3 scripts/invest_validator.py *)
metadata:
  role: Business Analyst
  phase: 1
  principle: Think Before Acting
---

# Phase 1: Requirement Discovery & BA Refinement

## 1. Log-Before-Act Protocol
Before any refinement begins, you MUST record the phase start in the audit trail to ensure session traceability.
!python3 scripts/scrum_guard.py --phase 1 --session ${CLAUDE_SESSION_ID} --msg "START: Initiating requirement intake and folder scan."

## 2. Source Discovery & Synthesis
Apply the **Think Before Acting** principle by identifying all project context before drafting solutions..
1. **Raw Intake**: Scan the `requirements/` folder for new source documents [8].
2. **Context Check**: Cross-reference raw input with `references/retro-knowledge.md` to avoid repeating historical mistakes.
3. **Ambiguity Triage**: If the requirement is vague, you MUST stop and seek clarification from the user before proceeding.

## 3. Backlog Drafting
Create a dedicated story file: `backlog/BKI-XXX_story.md` (replacing XXX with the next available ID).
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
