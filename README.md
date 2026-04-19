# Scrum Agent: Technical Specification

**Scrum Agent** is a high-precision, stateful engineering workflow designed for Claude Code. It implements a "persistent, compounding artifact" architecture—inspired by the **LLM Wiki** pattern—and enforces strict **Scrum process discipline** to ensure every unit of work is verifiable, surgical, and documented in an append-only audit trail. 

Unlike standard RAG systems that "rediscover" knowledge on every query by retrieving fragments from raw files, the Scrum Agent incrementally builds a structured repository of requirements, technical designs, and logs. This ensures that project knowledge accumulates and remains current rather than disappearing into chat history.

---

### 🧠 Foundational Philosophy: The Karpathy Quadrant
To prevent common AI pitfalls like silent assumptions and scope creep, the agent follows four core philosophies:
1.  **Think Before Coding**: Surface all ambiguities and technical tradeoffs before writing a single line of implementation code.
2.  **Simplicity First**: Implement the minimum code required for the current goal, rejecting bloated abstractions or unrequested "flexibility".
3.  **Surgical Changes**: Apply high-precision edits. Touch only the necessary files and match the existing codebase style exactly.
4.  **Goal-Driven Execution**: Utilize a **tests-first (TDD) methodology** to transform imperative tasks into verifiable success criteria.

---

### 🏗️ Technical Architecture & Progressive Disclosure
The system utilizes a three-layer architecture to maximize context efficiency. By defining procedures as **Claude Code Skills**, the full playbook for a role loads into context only when that specific skill is invoked, saving significant token usage.

*   **Layer 1: Raw Sources (`requirements/`)**: Immutable source documents and project intake materials that the LLM reads but never modifies.
*   **Layer 2: The Wiki (`backlog/`, `references/`, `logs/`)**: A structured collection of LLM-maintained markdown files, including User Stories (`BKI-XXX_story.md`), Architectural Decision Records (ADRs), and the project `log.md`.
*   **Layer 3: The Schema (`CLAUDE.md` & Skills)**: The core configuration and playbooks that define the agent's behavior, lifecycle phases, and tool permissions.

---

### 🔄 The 6-Phase Engineering Lifecycle
Every unit of work is assigned a unique **BKI-ID** and moves through these sequential phases, governed by **Hard Gates**.

| Phase | Role | Skill Name | Technical Objective |
| :--- | :--- | :--- | :--- |
| **1: Intake** | Business Analyst | `scrum-ba-intake` | Refines raw input into **Gherkin Acceptance Criteria**. Enforces the **Definition of Ready (DoR)**. |
| **2: Design** | Architect | `scrum-architect-design` | Performs **Surgical Impact Analysis** to identify the minimum file set. Produces an ADR and Impact Map. |
| **3: QA** | QA Engineer | `tdd-spec-generator` | Generates a **failing (Red)** test suite mapped directly to Gherkin scenarios to define success. |
| **4: Dev** | Developer | `scrum-executor` | Performs surgical implementation to reach a **"Green"** test state. Cleans up "orphan" code. |
| **5: Audit** | Auditor | `tdd-verifier` | Final reconciliation against the **Definition of Done (DoD)**. Updates the project `CHANGELOG.md`. |
| **6: Retro** | Scrum Master | `scrum-retro-analyst` | Conducts **Log Rotation**, archives the audit trail, and updates `retro-knowledge.md`. |

---

### 🛡️ Core Governance Mechanisms

#### 1. Deterministic Audit Trail (`Log-before-act`)
The agent is forbidden from acting without first recording its intent. Every phase transition utilizes the `scrum_guard.py` script to append a timestamped entry to the log. It utilizes the `${CLAUDE_SESSION_ID}` to correlate session activity with specific BKIs, ensuring a transparent record even if a session ends unexpectedly.

#### 2. Hard Gate Enforcement
*   **Definition of Ready (DoR)**: A story cannot enter Phase 2 until it meets the **INVEST** criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable), verified by an automated validator script.
*   **Definition of Done (DoD)**: A task is not complete until an independent test run verifies 100% of Gherkin scenarios and confirms the absence of "ghost work" or unrequested features.

#### 3. Context Window Optimization (Log Rotation)
To prevent the active `log.md` from exceeding LLM context limits, Phase 6 enforces **Log Rotation**. Detailed logs for completed BKIs are moved to an archive directory, while a high-level summary is carried forward to preserve "session memory" efficiently.

#### 4. Traceability & Retro-Knowledge
Every artifact created or modified includes a `backlog_id: BKI-XXX` in its frontmatter to trace it back to the original requirement. The `retro-knowledge.md` file serves as the project's long-term intelligence, capturing lessons learned to prevent future sprints from repeating historical mistakes.

---

### 🚀 Implementation Requirements
1.  **Deployment**: Copy the `.claude/skills/` directory and supporting `scripts/` (e.g., `scrum_guard.py`, `invest_validator.py`) to the project root.
2.  **Frontmatter Standards**: Skills must define `allowed-tools` to grant Claude permission to execute scripts without per-use approval.
3.  **Session Resume**: Users should begin every session with the **Session Resume Protocol**, asking Claude to review the log and report open sprints to prevent redundant "ghost work".