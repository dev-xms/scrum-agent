---
name: scrum-architect-design
description: Phase 2: Architect. Creates a surgical technical plan and ADR log based on validated BKI requirements, Use when asks to "architect/p".
allowed-tools:
  - Bash(python3 scripts/scrum_guard.py *)
  - Bash(python3 scripts/read_file.py *)
  - Bash(python3 scripts/list_dir.py *)
metadata:
  role: Architect
  phase: 2
  principle: Surgical Changes
---

# Phase 2: Architecture Design & Impact Mapping

## 1. Pre-Execution Protocol
You MUST record the start of this phase in the audit trail to ensure full session traceability.
!python3 scripts/scrum_guard.py --phase 2 --session ${CLAUDE_SESSION_ID} --msg "START: Initiating architectural design and impact mapping."

## 2. Context Discovery & Analysis
1. **Read Requirements**: Extract the validated User Story and Gherkin Acceptance Criteria (AC) from `backlog/BKI-XXX_story.md` — run `python3 scripts/read_file.py backlog/BKI-XXX_story.md`.
2. **Ambiguity Check**: If any technical constraints or requirements are unclear, you MUST stop and seek clarification before planning.

## 3. Surgical Impact Analysis
Apply the **Surgical Changes** principle to ensure high-precision implementation.
1. **File Selection**: Identify the **minimum set of files** required to fulfill the ACs — run `python3 scripts/list_dir.py src/` to survey the codebase.
2. **Dependency Mapping**: Analyze the codebase to ensure your changes do not cause "orthogonal edits" or side effects in unrelated modules.
3. **Orphan Management**: Identify any imports, variables, or functions that will be rendered unused by your proposed changes and plan for their immediate removal.

## 4. Technical Design & Tradeoffs
Document your decisions in a technical plan or Architectural Decision Record (ADR).
1. **State Assumptions**: Explicitly list any technical assumptions made during the design.
2. **Tradeoff Analysis**: Present multiple interpretations or technical paths and explain why the chosen approach was selected over others.
3. **Simplicity Audit**: If your proposed solution involves complex abstractions for single-use code, rewrite it to be simpler.

## 5. Handoff
1. **Log Completion**: !python3 scripts/scrum_guard.py --phase 2 --session ${CLAUDE_SESSION_ID} --msg "COMPLETED: Technical design and impact map finalized."
2. **User Confirmation**: Present the technical plan and impact map to the user. Ask: "Phase 2 complete. Proceed to Phase 3 (TDD Spec Generation)?"

