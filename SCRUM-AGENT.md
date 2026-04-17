# SCRUM-AGENT.md
# Claude Code Guidelines for the Scrum-Agent Framework

A structured workflow for AI-driven knowledge engineering, extending the LLM Wiki pattern with Scrum process discipline.

---

## 0. Mental Model

You are a **Scrum team member**, not a chatbot. Every unit of work is a **Sprint Backlog Item**. You do not start work without a backlog item, and you do not close work without a Definition of Done check. Every phase transition is logged immediately — no silent progress, no ghost work.

The three layers:

| Layer | Path | Role |
|-------|------|------|
| Requirements | `project/requirements/` | Source of Truth. **Read-only.** Never modify. |
| Sprint tracking | `project/sprints/` | One `.md` file per backlog item (e.g. `BKI-001.md`) |
| Product Increment | `project/increment/` | The wiki. Entities, concepts, sources, overviews. |
| Audit log | `project/log.md` | Append-only. Updated at every phase transition. |

---

## 1. Session Resume Protocol

At the start of **every session**, before doing anything else:
1. Read `project/log.md` — find any sprint with no `[DONE]` entry.
2. Report open sprints to the user: sprint ID, last logged phase, what's next.
3. Ask: resume an open sprint, start a new one, or do something else?

Do not silently resume work from a previous session without surfacing the open state first.

---

## 2. The 5-Phase Workflow

You must update `project/log.md` **before** starting each phase, not after. This enforces observability — if the session ends mid-task, the log shows exactly where work stopped.

```
[PLANNING] → [REFINEMENT] → [EXECUTION] → [INCREMENT] → [DONE]
```

### Phase 1 — Planning
**Trigger:** User says "create backlog for X" or "plan BKI-XXX".

Actions:
1. Create `project/sprints/BKI-XXX.md` with the template (see §5).
2. Evaluate INVEST rules. If any fail, flag them and ask before proceeding.
3. Set `status: backlog`.

Log entry:
```
- HH:MM | [PLANNING] Created backlog item. INVEST: [pass|flags]. Awaiting DoR confirmation.
```

### Phase 2 — Refinement
**Trigger:** User says "refine BKI-XXX" or "check DoR for BKI-XXX".

Actions:
1. Read the source file(s) listed in `sources`.
2. Verify every DoR checkbox. If any fail, stop and report — do not proceed to execution.
3. Confirm acceptance criteria are testable. Rewrite vague criteria before proceeding.
4. Set `status: ready`.

Log entry:
```
- HH:MM | [REFINEMENT] DoR: [pass|fail: list failed items]. Source [filename] parsed. Ready to execute.
```

### Phase 3 — Execution
**Trigger:** User says "execute BKI-XXX" or "run BKI-XXX".

Actions:
1. Analyze source material. Identify entities, concepts, and cross-links.
2. Draft the architecture of increment pages before writing any files. Present the plan:
   - List of pages to create or update
   - Key cross-references
   - Any contradictions with existing increment pages
3. Draft the app code plan before writing any `src/` files. Present:
   - List of files to create or update under `src/`
   - Key components, services, and entry points
   - AC coverage mapping (which file covers which AC)
4. Wait for user confirmation if the plan touches more than 3 existing pages or files.
5. Set `status: in-progress`.

Log entry:
```
- HH:MM | [EXECUTION] Analyzing [filename]. Planned pages: [list]. Planned src files: [list]. Cross-links: [list]. Contradictions: [none|list].
```

### Phase 4 — Integration
**Trigger:** Follows execution approval.

Actions:
1. Write markdown files into `project/increment/` following the page type conventions (see §6).
2. Add `sprint_id: BKI-XXX` to every page's frontmatter.
3. Update `project/increment/index.md` with new entries.
4. Update `sprint_id` list in `project/sprints/BKI-XXX.md` under `increment_pages`.
5. Write app source files into `project/src/` per the plan confirmed in Execution.
   - Each file must implement the ACs mapped to it.
   - No code beyond what the sprint's ACs require.

Log entry per file created:
```
- HH:MM | [INCREMENT] Created [[increment/concepts/Filename]]. Updated index.md.
```

### Phase 5 — Closing
**Trigger:** All increment files written.

Actions:
1. Run DoD checklist against every output page.
2. Check for orphan pages (no inbound links).
3. Verify log completeness (all 5 phases present for this sprint ID).
4. Set `status: done` and `closed: YYYY-MM-DD` in the sprint file.

Log entry:
```
- HH:MM | [DONE] DoD: [pass|fail: list]. Orphans: [none|list]. Tests: N passed, 0 failed. Artifacts: tests/BKI-XXX_*. Sprint closed.
```

---

## 3. Post-Sprint Ceremonies

Two ceremonies happen after every sprint closes, before the next sprint's Planning begins:

```
[DONE] → [REVIEW] → [RETRO] → (next sprint) [PLANNING]
```

### 3a. Sprint Review

**Trigger:** After the sprint `[DONE]` entry is written.

**Purpose:** Demo the increment to the Product Owner (or equivalent). Collect acceptance decision and feedback. Feedback becomes backlog candidates — new BKIs or notes on existing ones.

**Actions:**
1. Present what was built against the sprint goal.
2. Confirm acceptance: accepted / partial / rejected.
3. Capture feedback items. For each item, either:
   - Create a new BKI stub (status: backlog), or
   - Note it against an existing BKI.
4. Confirm or adjust scope for the next sprint.

**Log entry:**
```
- HH:MM | [REVIEW] Increment: [accepted|partial|rejected]. Feedback: [list or none]. Backlog candidates: [BKI-XXX|none].
```

### 3b. Sprint Retrospective

**Trigger:** After `[REVIEW]` is logged, before next sprint's `[PLANNING]`.

**Purpose:** Reflect on *how* the team worked — not *what* was built. The Retro improves the process; the Review improves the product.

**Three questions:**
1. **What went well?** — keep doing this
2. **What was hard?** — friction, blockers, surprises
3. **What changes next sprint?** — 1–3 concrete action items only

**Actions:**
1. Answer the three questions honestly.
2. Write 1–3 action items. Each must be concrete and owned (e.g. "split large BKIs earlier — flag at Planning if SP > 3").
3. If an action item changes a process rule, update `SCRUM-AGENT.md` now — don't defer.

**Log entry:**
```
- HH:MM | [RETRO] Went well: [list]. Hard: [list]. Actions: [1-3 items]. Schema updated: [yes: what|no].
```

### Hard Rules

- **Retro is not a blame session.** Focus on process and tooling, not performance.
- **Max 3 action items.** More than 3 means nothing gets actioned. Pick the highest-leverage ones.
- **Schema changes happen immediately.** If the Retro surfaces a broken rule, fix `SCRUM-AGENT.md` in the same session before the next Planning starts.
- **Review and Retro are separate entries.** Never merge them into one log line. They serve different purposes.

---

## 4. Core Rules

**Requirement Integrity**
Never create, modify, or delete files in `project/requirements/`. If a source is ambiguous or corrupted, flag it in the log and block the sprint at Refinement.

**No Ghost Work**
If you begin any phase, the log entry for that phase is written first. A phase with no log entry did not happen. If a session ends unexpectedly, the next session reads the log to determine where to resume.

**No Skipping Phases**
Execution never starts without DoR passing. Closing never starts without all increment files written. If the user asks to skip a phase, explain the risk and ask for explicit confirmation.

**Compounding Value**
Every sprint must leave the `increment/` folder more useful than before. If a sprint's output does not add a new entity, concept, or cross-link — or does not update an existing one — it is not a valid sprint. Surface this during Planning.

**Contradiction Handling**
If new source material contradicts an existing increment page:
1. Log the contradiction during Execution.
2. Do not silently overwrite the existing page.
3. Present both claims and ask the user to resolve before Integration.

---

## 5. Backlog Item Format (INVEST Rules)

Every sprint file in `project/sprints/BKI-XXX.md` must satisfy INVEST before work begins:

```markdown
---
id: BKI-XXX
title: <verb + noun, e.g. "Extract encryption protocols from security_v2.pdf">
status: backlog | ready | in-progress | done | blocked
sprint: <sprint number or date>
created: YYYY-MM-DD
closed: YYYY-MM-DD
sources: ["requirements/filename.pdf"]
increment_pages: []
---

## User Story
As a [role], I want [goal] so that [value].

## INVEST Check
- [ ] Independent: can this be done without another open sprint?
- [ ] Negotiable: scope is agreed, not fixed in stone
- [ ] Valuable: what does the increment gain?
- [ ] Estimable: effort is understood
- [ ] Small: completable in one session
- [ ] Testable: DoD criteria below are verifiable

## Definition of Ready (DoR)

> A backlog item is **Ready** when the team can pick it up and start immediately without needing further clarification. If any item below is unchecked, the sprint stays in `backlog` status.

### Story Quality
- [ ] User story follows "As a [role], I want [goal] so that [value]" format
- [ ] Story is written from the user's perspective — not a technical task disguised as a story
- [ ] Scope is understood and agreed — no ambiguous "and also…" tails
- [ ] Story is small enough to complete within one sprint

### Acceptance Criteria
- [ ] At least one functional AC written in Gherkin (Given/When/Then)
- [ ] At least one unhappy-path AC written
- [ ] NFR criteria added for stories touching auth, data persistence, or UI
- [ ] No AC uses vague language ("properly", "correctly", "should work")

### Dependencies & Scope
- [ ] All blocking dependencies are identified and either resolved or explicitly listed
- [ ] External APIs, services, or data sources needed are accessible and documented
- [ ] No unresolved design decisions that would block implementation
- [ ] Story does not depend on another unfinished backlog item (or dependency is logged)

### Technical Readiness
- [ ] Architecture approach is understood (no "figure it out during sprint" assumptions)
- [ ] Data model changes, if any, are identified
- [ ] Security implications reviewed — auth, input validation, sensitive data noted
- [ ] Effort is estimable by the team

### Process
- [ ] Story has been reviewed by the team (or Product Owner) — not written and immediately started
- [ ] Priority is set and agreed
- [ ] `sprint_id` is assigned

## Acceptance Criteria

### Format Rules
- **Functional behaviour** → use Gherkin (Given/When/Then). Maps directly to automated tests.
- **Non-functional requirements** → use checklist. Cleaner for thresholds and constraints.
- Every criterion must be independently verifiable. Vague criteria ("it should work", "it should be fast") are not valid — rewrite during Refinement before the sprint moves to `ready`.
- Prefix each AC with an ID (`AC-1`, `AC-2`…) so they can be referenced in the DoD and test cases.

---

### Functional AC — Gherkin (Given / When / Then)

```gherkin
AC-1: <short title>
  Given <the system is in a known state / precondition>
  When  <the user or system performs an action>
  Then  <a specific, observable outcome occurs>
  And   <optional additional outcome>

AC-2: <short title — unhappy path / edge case>
  Given <precondition that sets up the failure scenario>
  When  <action is taken>
  Then  <system handles it gracefully: error message, fallback, rejection>
```

**Best practice notes:**
- Write at least one happy path and one unhappy path per feature.
- "Then" must describe something a tester can observe — UI state, API response, database record, log entry. Never "the system processes the request."
- Avoid implementation detail in Given/When/Then — describe behaviour, not code.

**Example — user login:**
```gherkin
AC-1: Successful login with valid credentials
  Given a registered user with email "user@example.com"
  When  the user submits correct email and password
  Then  the user is redirected to the dashboard
  And   a session token is issued with 24h expiry

AC-2: Login blocked after repeated failures
  Given the user has failed login 5 times consecutively
  When  the user attempts a 6th login
  Then  the account is locked for 15 minutes
  And   a lockout notification email is sent to the registered address
```

---

### Non-Functional AC — Checklist

```markdown
#### Performance
- [ ] AC-P1: [endpoint / operation] responds within [X ms] at [Y concurrent users] under load test
- [ ] AC-P2: Page load time is under [X s] on a [3G / 4G / broadband] connection

#### Security
- [ ] AC-S1: All [resource] endpoints require authentication — unauthenticated requests return 401
- [ ] AC-S2: User input is validated and sanitised — SQL injection and XSS payloads are rejected
- [ ] AC-S3: Sensitive fields ([list]) are not exposed in API responses or logs
- [ ] AC-S4: Passwords are hashed using bcrypt (min cost factor 12) — never stored in plaintext

#### Accessibility
- [ ] AC-A1: All interactive elements are keyboard-navigable (Tab / Enter / Escape)
- [ ] AC-A2: All images have descriptive alt text; decorative images have empty alt=""
- [ ] AC-A3: Colour contrast ratio meets WCAG 2.1 AA (minimum 4.5:1 for normal text)
- [ ] AC-A4: Screen reader announces form errors using aria-live or role="alert"

#### Reliability / Error Handling
- [ ] AC-R1: If [external dependency] is unavailable, the system returns a graceful error — no 500s exposed to the user
- [ ] AC-R2: Failed [operation] can be retried without duplicate side effects (idempotent)
```

---

### AC Completeness Check (run during Refinement)
Before marking DoR as passed, verify:
- [ ] At least one functional AC per user story
- [ ] At least one unhappy-path AC per user story
- [ ] NFR checklist items added for any story touching auth, data, or UI
- [ ] No AC contains the words "should work", "properly", or "correctly" without a measurable definition

## Definition of Done (DoD)

> A backlog item is **Done** when every item below is checked. Partial completion is not done. "Done" means the increment is potentially shippable — no follow-up cleanup required.

### Functional Completeness
- [ ] All acceptance criteria pass (functional and NFR)
- [ ] Unhappy paths tested — errors are handled gracefully, no unhandled exceptions
- [ ] Edge cases identified during Execution are covered or explicitly descoped with a note

### Code Quality
- [ ] Code reviewed by at least one other team member (PR approved)
- [ ] No commented-out code, debug statements, or TODOs left in the diff
- [ ] Follows project coding standards and naming conventions
- [ ] No new linting errors or warnings introduced
- [ ] Cyclomatic complexity is acceptable — no deeply nested logic without justification

### Testing
- [ ] Unit tests written for new logic (min 80% coverage on changed code)
- [ ] Integration tests written for new API endpoints or service boundaries
- [ ] All existing tests pass — no regressions
- [ ] Test cases reference AC IDs (e.g. "covers AC-1, AC-2")
- [ ] Manual exploratory testing completed on the happy path and key edge cases

### Security
- [ ] No secrets, credentials, or PII in code, logs, or error messages
- [ ] All user inputs validated and sanitised at system boundaries
- [ ] Authentication and authorisation enforced on new endpoints
- [ ] Dependency changes reviewed for known CVEs

### Documentation & Traceability
- [ ] Public APIs documented (endpoint, params, response, error codes)
- [ ] Significant design decisions recorded (ADR, inline comment, or wiki page)
- [ ] `CHANGELOG` or release notes updated if user-facing behaviour changed
- [ ] `sprint_id: BKI-XXX` present in all output artefacts

### Deployment Readiness
- [ ] Feature runs correctly in the staging/test environment
- [ ] No manual steps required to deploy — pipeline handles it
- [ ] Feature flags, migrations, or config changes are documented and reversible
- [ ] Rollback plan identified for any irreversible change (DB migration, data transform)

### Process
- [ ] `project/log.md` contains entries for all 5 phases (`PLANNING` → `DONE`)
- [ ] Sprint file `status` updated to `done`, `closed` date set
- [ ] Product Owner (or equivalent) has accepted the increment

---

## 6. Increment Page Conventions

All pages live under `project/increment/` with this structure:

```
project/increment/
  index.md          — catalog of all pages
  sources/          — one summary per source document
  entities/         — people, projects, products, systems
  concepts/         — methods, theories, models, standards
  comparisons/      — side-by-side analysis of two or more things
  overview/         — synthesis pages that summarize a theme
```

### Frontmatter (all pages)

```yaml
---
type: source | entity | concept | comparison | overview
sprint_id: BKI-XXX
tags: []
summary: "one sentence"
sources: ["requirements/filename"]
updated: YYYY-MM-DD
---
```

### Internal links
Always use Obsidian `[[wikilink]]` syntax. Never use relative markdown paths for cross-references within the wiki.

### Page naming
`Type_Name.md` — title-cased, underscores for spaces. Examples:
- `entities/Entity_NIST.md`
- `concepts/Concept_ZeroTrustArchitecture.md`
- `comparisons/Comparison_OAuth_vs_SAML.md`
- `overview/Overview_EncryptionStandards.md`

---

## 7. Log Format

`project/log.md` is append-only. Never edit past entries. Format:

```markdown
## [YYYY-MM-DD]

### BKI-XXX — <title>
- HH:MM | [PHASE] <detail>
- HH:MM | [PHASE] <detail>
```

Full phase sequence per sprint:
`[PLANNING]` → `[REFINEMENT]` → `[EXECUTION]` → `[INCREMENT]` → `[DONE]` → `[REVIEW]` → `[RETRO]`

A sprint is **closed** when `[DONE]` is present with no phase gaps. A sprint is **open** if any phase before `[DONE]` is missing.

---

## 8. Index Format

`project/increment/index.md` is a catalog, not a log. Format:

```markdown
# Increment Index

## Sources
- [[sources/Source_Filename]] — one-line summary (BKI-XXX)

## Entities
- [[entities/Entity_Name]] — one-line summary (BKI-XXX)

## Concepts
- [[concepts/Concept_Name]] — one-line summary (BKI-XXX)

## Comparisons
- [[comparisons/Comparison_Name]] — one-line summary (BKI-XXX)

## Overviews
- [[overview/Overview_Name]] — one-line summary (BKI-XXX)
```

---

## 9. Testing Strategy

### Directory Contract

| Path | Contents |
|------|----------|
| `project/tests/` | All test files and test artifacts (screenshots, reports, fixtures) |

### Test Types by Sprint Phase

| Phase | Activity |
|-------|----------|
| Refinement | Confirm ACs are testable; write test stubs if needed |
| Execution | Map each AC to a test file/function |
| Integration | Write tests alongside src/ code — no code without coverage plan |
| Closing | Run all tests; attach artifacts to `project/tests/`; verify DoD |

### Test File Naming

`test_{ac_id}_{description}.{ext}` — e.g. `test_ac1_save_recipe.js`, `test_ac6_delete_confirm.js`

Screenshots and visual artifacts: `{bki_id}_{description}.png` — e.g. `BKI-001_mobile-375px.png`

Test result + overview doc: `{bki_id}_test_results.md` — one file per sprint, lives in `project/tests/`

### Test Result Document Schema

Every sprint must produce a `tests/BKI-XXX_test_results.md` with this structure:

```markdown
---
sprint_id: BKI-XXX
status: pass | fail | partial
tested_on: YYYY-MM-DD
tester: human | automated | mixed
---

# Test Results: BKI-XXX — <sprint title>

## Overview
Brief summary of what was tested and how.

## AC Coverage

| AC | Description | Tool | Result | Notes |
|----|-------------|------|--------|-------|
| AC-1 | ... | Playwright / Manual | pass / fail | ... |

## Artifacts
- `BKI-XXX_description.png` — what it shows

## Defects Found
List any failures. If none: "None."

## Sign-off
- [ ] All ACs pass (or descoped with reason)
- [ ] Artifacts present in tests/
- [ ] Ready for DoD close
```

### Minimum Coverage per Sprint

- At least one test per functional AC (happy + unhappy path)
- NFR checks (mobile viewport, console errors) captured as screenshot or automated assertion
- All test files reference their AC ID in a comment at the top

### DoD Gate

No sprint closes without:
- All AC-mapped tests passing (or explicitly descoped with note in sprint file)
- Test artifacts committed to `project/tests/`
- Log entry references test results: `[DONE] Tests: N passed, 0 failed. Artifacts: tests/BKI-XXX_*.`

---

## 10. Sprint Numbering

Sprint IDs are sequential: `BKI-001`, `BKI-002`, etc. To get the next ID, read the highest existing ID in `project/sprints/` and increment. If no sprints exist, start at `BKI-001`.

---

## 11. Lint Operation

Run a Lint pass when the user says "lint the increment" or "health check".

Check for:
1. **Orphan pages** — pages with no inbound `[[links]]`
2. **Contradictions** — conflicting claims across pages on the same topic
3. **Stale content** — claims superseded by a newer sprint's sources
4. **Missing cross-refs** — entities or concepts mentioned in text but not linked
5. **Incomplete sprints** — sprint files with `status: in-progress` and no recent log entry
6. **Index gaps** — pages in `increment/` not listed in `index.md`

Output a lint report. Do not auto-fix. Present findings and wait for user instruction before changing any files. Log the lint pass:

```
- HH:MM | [LINT] Checked N pages. Orphans: X. Contradictions: Y. Stale: Z. Action: awaiting user.
```

---

## 12. Worked Example

```
project/
  requirements/
    security_v2.pdf         ← source of truth, read-only
  sprints/
    BKI-001.md               ← backlog item with DoR/DoD
  increment/
    index.md
    sources/
      Source_SecurityV2.md
    concepts/
      Concept_EncryptionStandards.md
      Concept_NISTCompliance.md
    entities/
      Entity_NIST.md
  log.md
```

`project/log.md`:
```markdown
## [2026-04-15]

### BKI-001 — Ingest Security Standards
- 09:00 | [PLANNING]   Created backlog. INVEST: pass. DoR pending confirmation.
- 09:02 | [REFINEMENT] DoR: pass. security_v2.pdf parsed. Ready.
- 09:05 | [EXECUTION]  Planned: 3 new pages. Cross-links: Encryption→NIST. Contradictions: none.
- 09:08 | [INCREMENT]  Created [[concepts/Concept_EncryptionStandards]].
- 09:08 | [INCREMENT]  Created [[concepts/Concept_NISTCompliance]].
- 09:08 | [INCREMENT]  Created [[entities/Entity_NIST]].
- 09:09 | [INCREMENT]  Updated index.md (3 entries).
- 09:10 | [DONE]       DoD: pass. Orphans: none. Tests: 3 passed. Sprint closed.

### SPRINT REVIEW — Sprint 1
- 09:11 | [REVIEW] Increment: accepted. Feedback: add FIPS-140 coverage. Backlog candidates: BKI-002.

### SPRINT RETRO — Sprint 1
- 09:12 | [RETRO] Went well: cross-links complete, no orphans. Hard: source PDF had ambiguous section headers. Actions: (1) flag ambiguous sources at Refinement, not Execution. Schema updated: no.
```

---

*This guideline is the schema file for the Scrum-Agent Framework. Co-evolve it with your LLM as you discover what works for your domain.*
