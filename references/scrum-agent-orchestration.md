***

# Technical Design: Scrum-Agent Orchestration

This system transforms Claude Code from a reactive assistant into an **accountable engineering agent**. It replaces ad-hoc prompting with a **deterministic 6-phase lifecycle** governed by "Hard Gates" and append-only auditing.

## 1. The Three-Level Architecture
To maintain high performance and low token usage, the system follows the **Progressive Disclosure** pattern:
*   **Level 1 (Metadata)**: YAML frontmatter tells Claude *when* to activate a specific phase.
*   **Level 2 (SOP)**: The `SKILL.md` body provides the immediate logic. **Constraint**: This file must remain **under 500 lines** to preserve context.
*   **Level 3 (Resources)**: Detailed checklists, templates, and deterministic scripts located in `references/` and `scripts/` folders, discovered only as needed.

## 2. Core Operational Principles
The agent is programmatically bound to the **Karpathy Principles** to mitigate common LLM coding pitfalls:
*   **Think Before Coding**: Explicitly state assumptions and seek clarification for ambiguity before execution.
*   **Simplicity First**: Implement the minimum code required; reject speculative abstractions or unrequested "flexibility".
*   **Surgical Changes**: Modify only the necessary files, matching existing styles and avoiding "orthogonal edits" to adjacent code.
*   **Goal-Driven Execution**: Define success via **failing tests (TDD)** and loop execution until verification is achieved.

## 3. The 6-Phase Orchestration Lifecycle
Every unit of work is assigned a unique **BKI-ID** (e.g., `BKI-001`) and must move through these phases in order.

| Phase | Role | Trigger Condition (YAML Description) | Deliverable & "Hard Gate" |
| :--- | :--- | :--- | :--- |
| **1** | **BA** | New requirements or project goals provided. | **DoR Gate**: Validated story in `backlog/`. |
| **2** | **Architect** | Validated BKI story is ready for planning. | Surgical Impact Map & Tradeoff Analysis. |
| **3** | **QA** | Technical plan finalized; implementation pending. | Failing test suite (Success Criteria). |
| **4** | **Developer** | Failing test suite verified (Red Phase). | Surgical implementation passing tests. |
| **5** | **Auditor** | Implementation complete; tests pending. | **DoD Gate**: Results committed to `tests/`. |
| **6** | **Scrum Master** | Sprint closed; artifacts verified. | Log rotation; update `retro-knowledge.md`; Skills ↔ Commands sync verified. |

## 4. State Management & Persistence
To ensure continuity across sessions, the agent utilizes specific Claude Code substitutions and protocols:
*   **Log-Before-Act Protocol**: The agent MUST write a log entry to `logs/log.md` **before** starting a phase.
*   **Session Correlation**: Every log entry uses the **`${CLAUDE_SESSION_ID}`** variable to link actions to a specific session.
*   **Session Resume Protocol**: Every session begins by reading `logs/log.md` to identify any BKI without a `[DONE]` entry, preventing "ghost work".
*   **BKI Seed Protocol**: Plan artifacts (`docs/plans/`) may not be executed directly. Phase 6 registers them as "Pending BKI Seeds" in `references/retro-knowledge.md`. They re-enter the workflow only when Phase 1 (BA) converts the seed to a `requirements/BKI-XXX.md` story.

## 5. Deterministic "Hard Gates"
Process integrity is enforced by **executable logic** rather than natural language alone:
*   **Definition of Ready (DoR)** *(Phase 1 → 2)*: A task cannot enter Phase 2 until programmatically verified as **INVEST** via `invest_validator.py`.
*   **Red Phase Gate** *(Phase 3 → 4)*: A task cannot enter Phase 4 until the test suite is confirmed **failing** via `run_unit_tests.py` / `run_e2e_tests.py`. Implementation must not exist yet.
*   **Definition of Done (DoD)** *(Phase 5 → 6)*: A task is not complete until 100% of Gherkin ACs pass and test artifacts exist in `test-results/Sprint-N-BKI-XXX/`.
*   **Log Integrity**: All logging is handled via specialized scripts (e.g., `scrum_guard.py`) to ensure an **append-only** audit trail.

## 6. Directory Specification
| Folder | Purpose |
| :--- | :--- |
| `backlog/` | Unique `BKI-XXX_story.md` files (prevents concurrent overwriting). |
| `references/` | Level 3 static documentation (DoR/DoD checklists, style guides). |
| `scripts/` | Executable deterministic logic for validation and TDD. |
| `logs/log.md` | Append-only audit trail recording phase transitions. |
| `tests/` | Unit and E2E test code (`app.test.js`, `tests/e2e/*.spec.js`). |
| `test-results/Sprint-N-BKI-XXX/` | Per-sprint artifacts: `BKI-XXX_unit.txt`, `BKI-XXX_e2e.txt`, `BKI-XXX_ui.png`, `regression_unit.txt`. |