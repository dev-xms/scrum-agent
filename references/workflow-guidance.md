# Scrum Agent Workflow Guidance

Canonical decisions governing the scrum-agent workflow. Updated each sprint via Phase 6 retro.

---

## Script Execution Policy (enforced since Sprint 1, 2026-04-20)

All bash execution goes through `scripts/`. No raw `cat`, `ls`, `mv`, `cp`, `npm`, `npx`, `pytest` in skills or commands.

| Banned | Replacement |
|---|---|
| `cat <file>` | `python3 scripts/read_file.py <file>` |
| `ls [path]` | `python3 scripts/list_dir.py [path]` |
| `mv <src> <dst>` | `python3 scripts/move_file.py <src> <dst>` |
| `cp <src> <dst>` | `python3 scripts/copy_file.py <src> <dst>` |
| `npm test` | `python3 scripts/run_unit_tests.py BKI-XXX` |
| `npm run test:e2e` | `python3 scripts/run_e2e_tests.py BKI-XXX` |
| `npx playwright ...` / `npx serve ...` | `python3 scripts/capture_screenshot.py BKI-XXX` |
| `pytest` | `python3 scripts/run_unit_tests.py BKI-XXX` |

**Why**: Every invocation writes to `logs/scripts-records.log`. Audit trail is complete and cannot be bypassed.

---

## Execution Boundary Policy (enforced since Sprint 1, 2026-04-20)

No code, config, or file change may execute outside the 6-phase workflow.

- Plans in `docs/superpowers/plans/` are read-only. Enter via Phase 1 next sprint.
- Phase 6 retro registers plan artifacts as Pending BKI Seeds in `retro-knowledge.md`.
- Trivial tasks (single-line typo, config value) require explicit user confirmation + log entry.

---

## E2E Testing Policy (enforced since Sprint 1, 2026-04-20)

For stories where Phase 2 impact map includes HTML or CSS files:
- Phase 3 (QA): generate Playwright E2E spec in `tests/e2e/BKI-XXX.spec.js` using `data-testid` selectors only.
- Phase 5 (Audit): run `python3 scripts/run_e2e_tests.py BKI-XXX Sprint-N-BKI-XXX`, capture screenshot via `python3 scripts/capture_screenshot.py BKI-XXX Sprint-N-BKI-XXX`.
- DoD hard gate: `test-results/Sprint-N-BKI-XXX/BKI-XXX_e2e.txt` and `test-results/Sprint-N-BKI-XXX/BKI-XXX_ui.png` must exist.

For stories with no UI: note "E2E not applicable" in Phase 3 and Phase 5 logs.

---

## Skills ↔ Commands Sync Policy (enforced since Sprint 1, 2026-04-20)

`skills/*.md` are the source of truth. `.claude/commands/*.md` must be exact copies.

Phase 6 retro **must** detect and fix drift before closing. Drift check procedure:
1. `python3 scripts/list_dir.py skills/` — enumerate skill files.
2. For each skill, compare to matching `.claude/commands/<name>.md`.
3. If diff found: overwrite `.claude/commands/<name>.md` with contents of `skills/<name>.md`.

**Why**: `.claude/commands/` is what Claude Code exposes as `/slash-commands`. Stale commands silently use old tool permissions and outdated instructions.

---

## Script Audit Policy (enforced since Sprint 1, 2026-04-20)

Phase 6 retro must verify `scripts/README.md` lists every file in `scripts/`.

Procedure: `python3 scripts/list_dir.py scripts/` → compare to table in `scripts/README.md`. If any script is missing from the README, add it before closing.

---

## Log Rotation Scope (enforced since Sprint 1, 2026-04-20)

Both `logs/log.md` AND `logs/scripts-records.log` are rotated in Phase 6 to `logs/archive/BKI-XXX_log.md` and `logs/archive/BKI-XXX_scripts-records.log` respectively.
