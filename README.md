# Scrum-Agent

> **An AI agent that works like a Scrum team member — not a chatbot.**

Most AI knowledge work fails after a few sessions. The agent ingests documents, builds summaries, connects ideas — then the session ends and nothing persists. You come back and restart from scratch. The problem isn't the AI. It's the absence of process.

**Scrum-Agent** extends [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with Scrum process discipline: every unit of work is a Sprint Backlog Item, every session is logged, and no sprint closes without a Definition of Done check.

---

## The Core Insight

```
No work without a contract.
No close without a check.
No session without a log.
```

The agent is accountable to a **process**, not just a prompt. That accountability loop is what separates an agent you can trust to work unsupervised from one you have to babysit.

---

## How It Works

### Architecture — 4 Layers

```
project/
├── requirements/     ← Source of Truth. READ-ONLY. Agent never modifies.
├── sprints/          ← One BKI-XXX.md per backlog item
├── increment/        ← The wiki: sources, entities, concepts, overviews
│   ├── index.md
│   ├── sources/
│   ├── entities/
│   ├── concepts/
│   ├── comparisons/
│   └── overview/
├── src/              ← App/code output (for software projects)
├── tests/            ← Test results, screenshots, artifacts
└── log.md            ← Append-only audit trail
```

### The Sprint Lifecycle

Every backlog item moves through exactly 5 phases, in order. **The log entry is written before each phase begins** — not after. If a session ends unexpectedly, the log shows where work stopped. The next session resumes from there.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  PLANNING   │────▶│ REFINEMENT  │────▶│  EXECUTION  │────▶│  INCREMENT  │────▶│    DONE     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
  Create BKI          DoR gate            Analyze +            Write files         DoD gate
  INVEST check        Source verified     Plan output          Update index        Orphan scan
  status: backlog     status: ready       status: in-progress  Artifacts           Sprint closed
                                                                                          │
                                                               ┌──────────────────────────┘
                                                               ▼
                                                    ┌─────────────────────┐
                                                    │   POST-SPRINT       │
                                                    │  [REVIEW] → [RETRO] │
                                                    └──────────┬──────────┘
                                                      Demo increment        Reflect on process
                                                      Collect feedback      1–3 action items
                                                      New BKI stubs         Schema update if needed
                                                               │
                                                               ▼
                                                    (next sprint) [PLANNING]
```

**DoR is a hard gate** — if any Definition of Ready item fails, the sprint stays in `backlog`. No skipping.

**DoD is a hard gate** — if any Definition of Done item fails, the sprint stays open. No silent closes.

**Review ≠ Retro** — Review asks "did we build the right thing?"; Retro asks "did we work the right way?"

---

## Sprint Backlog Item (BKI) Format

Every sprint file follows INVEST and contains:

```markdown
---
id: BKI-001
title: "Verb + noun description"
status: backlog | ready | in-progress | done | blocked
sprint: 1
created: 2026-04-17
closed: 2026-04-17
sources: ["requirements/filename.md"]
increment_pages: ["overview/Overview_Sprint1"]
---

## User Story
As a [role], I want [goal] so that [value].

## INVEST Check        ← evaluated at Planning
## Definition of Ready ← gate before Execution
## Acceptance Criteria ← Gherkin (Given/When/Then) + NFR checklist
## Definition of Done  ← gate before closing
```

### Acceptance Criteria Format

**Functional behaviour** → Gherkin:
```gherkin
AC-1: Save recipe with all fields
  Given the user is on the recipe form
  When  the user enters Title and clicks Save
  Then  the recipe appears in the list
  And   data persists after page reload
```

**Non-functional requirements** → Checklist:
```markdown
- [ ] AC-N1: Layout usable on 375px viewport (mobile-first)
- [ ] AC-N2: No console errors on load, save, or delete
```

---

## Session Resume Protocol

**Every session starts by reading `project/log.md`.** The agent surfaces any sprint with no `[DONE]` entry:

```
⚠ Open sprints found:
  BKI-002 — last phase: [REFINEMENT] — next: EXECUTION
  
Resume BKI-002, start new sprint, or something else?
```

No silent resumption. No ghost work.

---

## Audit Log Format

`log.md` is append-only. One entry per phase transition. Format:

```markdown
## [2026-04-17]

### BKI-001 — Build Basic Digital Recipe Box
- 09:00 | [PLANNING]   Created backlog item. INVEST: pass. Awaiting DoR.
- 09:02 | [REFINEMENT] DoR: pass. Source parsed. Status → ready.
- 09:05 | [EXECUTION]  Planned 3 pages + 3 src files. Contradictions: none.
- 09:08 | [INCREMENT]  Created overview/Overview_Sprint1. Updated index.md.
- 09:10 | [DONE]       DoD: pass. Orphans: none. Sprint closed.
```

A sprint is **closed** when all 5 phases appear with no gaps. A sprint is **open** if any phase is missing.

After closing, two post-sprint ceremonies are logged before the next Planning:

```markdown
### SPRINT REVIEW — Sprint 1
- 09:11 | [REVIEW] Increment: accepted. Feedback: form too long, cards need detail. Backlog candidates: BKI-003, BKI-004.

### SPRINT RETRO — Sprint 1
- 09:12 | [RETRO] Went well: AC coverage complete, tests automated. Hard: form UX took longer than estimated. Actions: (1) flag BKIs > 3 SP for splitting at Planning. Schema updated: no.
```

---

## Increment Wiki Structure

Every page carries `sprint_id` in frontmatter — full traceability from artifact back to requirement:

```yaml
---
type: source | entity | concept | comparison | overview
sprint_id: BKI-001
summary: "one sentence"
sources: ["requirements/filename.md"]
updated: 2026-04-17
---
```

Internal cross-references use `[[wikilink]]` syntax (Obsidian-compatible).

| Page type | Lives in | Purpose |
|-----------|----------|---------|
| `source` | `sources/` | Summary of a source document |
| `entity` | `entities/` | People, systems, products, organisations |
| `concept` | `concepts/` | Methods, theories, models, standards |
| `comparison` | `comparisons/` | Side-by-side analysis of two+ things |
| `overview` | `overview/` | Synthesis pages summarising a theme |

---

## Testing Strategy

Every sprint produces a `tests/BKI-XXX_test_results.md`:

```markdown
| AC   | Description           | Tool                  | Result | Notes              |
|------|-----------------------|-----------------------|--------|--------------------|
| AC-1 | Save happy path       | browser_run_code      | pass   | Form cleared after save |
| AC-N1| Mobile 375px usable   | browser_take_screenshot | pass | See screenshot below |

![BKI-001 mobile](BKI-001_mobile-375px.png)
```

**DoD gate**: no sprint closes without test artifacts committed to `tests/`.

---

## Scrum-Agent vs LLM Wiki

| Capability | LLM Wiki | Scrum-Agent |
|-----------|----------|-------------|
| Knowledge accumulation | ✅ | ✅ |
| Cross-references maintained | ✅ | ✅ |
| Process visibility | Ad-hoc | ✅ Formal 5 phases |
| Session continuity | Implicit | ✅ Explicit log + resume |
| Definition of Done | ❌ | ✅ Enforced checklist |
| Contradiction handling | Mentioned | ✅ Blocking step |
| Artifact traceability | ❌ | ✅ `sprint_id` in every page |
| Test artifacts | ❌ | ✅ Per-sprint test results |
| Post-sprint ceremonies | ❌ | ✅ Review + Retro, both logged |

---

## What Gets Prevented

| Failure mode | How Scrum-Agent prevents it |
|-------------|----------------------------|
| Agent silently overwrites conflicting content | Contradiction check in Execution is a blocking step |
| Session ends mid-task, work lost | Log-before-act: resume protocol reads log at session start |
| "Done" but acceptance criteria never verified | DoD is a gate — sprint stays open until every AC is checked |
| Artifact exists but no one knows why | `sprint_id` in frontmatter traces every page to its BKI |
| Backlog items started without enough info | DoR gate prevents Execution until source is verified readable |
| Orphan wiki pages accumulate | Orphan scan at Closing + periodic Lint pass |
| Process lessons lost between sprints | Retro logged after every sprint — actions written before next Planning |
| Review feedback never becomes backlog items | Review produces explicit BKI stubs or notes before next sprint starts |

---

## Lint (Health Check)

Run `lint the increment` to scan for:

1. **Orphan pages** — no inbound `[[links]]`
2. **Contradictions** — conflicting claims across pages
3. **Stale content** — superseded by newer sprints
4. **Missing cross-refs** — mentioned but not linked
5. **Incomplete sprints** — `in-progress` with no recent log entry
6. **Index gaps** — pages in `increment/` not in `index.md`

Lint produces a report. It never auto-fixes. You decide what to act on.

---

## Quick Start

1. Copy `SCRUM-AGENT.md` into your project root
2. Add to your `CLAUDE.md`:
   ```markdown
   ## Scrum-Agent Workflow
   When working in a `project/` directory, follow SCRUM-AGENT.md.
   ```
3. Drop your source documents into `project/requirements/`
4. Tell the agent: _"Create backlog for [goal]"_

The agent will create `BKI-001.md`, evaluate INVEST, and ask you to confirm DoR before doing anything else.

---

## Example Project

See [`sample-project/`](sample-project/) — a fully worked demo (The Smart Plate recipe app) showing:
- 2 completed sprints (BKI-001, BKI-002)
- Playwright-automated AC verification
- Test result markdown with inline screenshots
- Sprint Review log entries
- 2 backlog items (BKI-003, BKI-004) triaged from Review feedback

---

## Use Cases

- **Security research** — ingest CVE reports, build a threat model wiki traceable to source docs
- **Competitive analysis** — entity-per-competitor wiki updated sprint by sprint
- **Legal/compliance** — map regulations to controls, auditable by sprint
- **Engineering knowledge base** — RFCs, ADRs, incident reports as interlinked wiki
- **Software delivery** — full CRUD app built, tested, and documented sprint by sprint
- **Research synthesis** — contradictions flagged, not silently overwritten

---

## Credits

Built on the shoulders of:

**Andrej Karpathy — LLM Wiki**
The original pattern: an LLM should *build and maintain* a persistent wiki, not re-derive answers from raw documents.
→ https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**Blink — Obsidian LLM Wiki**
Concrete implementation with disciplined schema, directory conventions, and Ingest/Query/Lint workflow.
→ https://github.com/iBlinkQ/llm-wiki-obsidian-blink

The knowledge layer is theirs. The sprint discipline is new.

---

## Files

| File | Purpose |
|------|---------|
| `SCRUM-AGENT.md` | The schema — constitution the agent follows |
| `CLAUDE.md` | Behavioral guidelines + Scrum-Agent activation |
| `sample-project/` | Fully worked demo project |
| `docs/article-github.md` | Long-form writeup of the pattern |
| `docs/article-linkedin.md` | Summary post |
