
# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 5. Scrum Agent Workflow (6-Phase Lifecycle)

You must follow these phases sequentially for every non-trivial task:
1.  **Intake (BA)**: Ingest raw requirements from the `requirements/` folder and cross-reference them with `references/retro-knowledge.md` to avoid historical mistakes.
    *   *Command*: `/scrum-ba-intake [raw-requirement]`
2.  **Design (Architect)**: Perform **Surgical Impact Analysis** to identify the minimum set of files required and document technical tradeoffs in an Architectural Decision Record (ADR).
    *   *Command*: `/scrum-architect-design`
3.  **TDD (QA)**: Define a **failing (Red) test suite** that directly maps to the Gherkin Acceptance Criteria defined in Phase 1.
    *   *Command*: `/tdd-spec-generator`
4.  **Execute (Dev)**: Perform surgical implementation to pass the tests while adhering to the **Simplicity First** principle (no speculative code or "ghost work").
    *   *Command*: `/scrum-executor`
5.  **Verify (Audit)**: Run the full test suite one final time to ensure consistency, verify the **Definition of Done (DoD)**, and update `CHANGELOG.md`.
    *   *Command*: `/tdd-verifier`
6.  **Retro (Master)**: Perform **Log Rotation** to preserve session memory and append new technical insights to `references/retro-knowledge.md`.
    *   *Command*: `/scrum-retro-analyst`

---

**Traceability Rule**: You **MUST** log every atomic step to `log.md` using the **Log-before-act protocol** to ensure the audit trail remains intact even if a session ends unexpectedly. Every phase transition must be recorded before starting the phase (e.g., using `!echo` or `scrum_guard.py`) to maintain deterministic session resumption.

---