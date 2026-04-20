# Scripts — Technical Reference

All automation in the Scrum Agent workflow is delegated to scripts in this directory.
No raw `bash`, `cat`, `ls`, `mv`, `cp`, `npm`, `npx`, or `pytest` commands are invoked directly by skills.

---

## Audit Log: `logs/scripts-records.log`

Every script call writes two entries to `logs/scripts-records.log` via the shared `script_logger.py` utility:

```
[YYYY-MM-DD HH:MM:SS] [INVOKE] <script> args=[...]
[YYYY-MM-DD HH:MM:SS] [RESULT] <script> status=OK|FAILED|ERROR detail=<optional>
```

**Rotation**: Phase 6 (`scrum-retro-analyst`) archives this file to
`logs/archive/BKI-XXX_scripts-records.log` in the same cycle as `logs/log.md`, using:
```
python3 scripts/move_file.py logs/scripts-records.log logs/archive/BKI-XXX_scripts-records.log
```

**Integrity**: `script_logger.py` uses append-only mode (`"a"`) — same guarantee as `scrum_guard.py` for `log.md`. Scripts resolve `script_logger.py` via `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` — safe regardless of working directory.

---

## Script Reference

| Script | Replaces | Phase(s) | Args |
| :--- | :--- | :--- | :--- |
| `init.sh` | — | Setup (once) | `[dir]` optional root dir |
| `scrum_guard.py` | — | All (1–6) | `--phase N --session ID --msg "..."` |
| `invest_validator.py` | — | 1 (DoR gate) | `<story_file>` |
| `read_file.py` | `cat` | Any | `<path>` |
| `list_dir.py` | `ls` | Any | `[path]` (default: `.`) |
| `move_file.py` | `mv` | 6 (log rotation) | `<src> <dst>` |
| `copy_file.py` | `cp` | 6 | `<src> <dst>` |
| `make_dir.py` | `mkdir -p` | Any | `<path>` |
| `run_unit_tests.py` | `npm test` / `pytest` | 3, 4, 5 | `<BKI-ID> [sprint-folder]` |
| `run_e2e_tests.py` | `npm run test:e2e` | 3, 4, 5 | `<BKI-ID> [sprint-folder]` |
| `capture_screenshot.py` | `npx serve` + `npx playwright screenshot` | 5 | `<BKI-ID> [sprint-folder]` |
| `script_logger.py` | — | Internal (imported) | N/A — not invoked directly |

---

## Script Descriptions

### `init.sh [dir]`
Creates the full project directory skeleton. Run once during project setup.
Writes INVOKE/RESULT entries directly to `logs/scripts-records.log` via `echo >>` (Python not guaranteed available at setup time).

### `scrum_guard.py`
Append-only phase logger and directory contract enforcer. Called at the start and end of every phase transition. Writes to `logs/log.md`. Also logs its own invocation to `scripts-records.log`.

### `invest_validator.py <story_file>`
DoR hard gate for Phase 1. Validates the story file against INVEST criteria: story format, Gherkin keywords, non-functional checklist, BKI traceability ID. Exits 1 if any check fails — blocks transition to Phase 2.

### `read_file.py <path>`
Replaces `cat`. Reads and prints file content. Logs invocation and result to `scripts-records.log`. Use for inspecting backlog stories, ADRs, retro-knowledge, changelogs.

### `list_dir.py [path]`
Replaces `ls`. Lists directory contents (sorted). Defaults to `.` if no path given. Use for scanning `requirements/`, `backlog/`, `logs/archive/`.

### `move_file.py <src> <dst>`
Replaces `mv`. Moves a file or directory. Creates destination parent directories as needed. Used by Phase 6 for log rotation (`log.md` → `logs/archive/`) and `scripts-records.log` rotation.

### `copy_file.py <src> <dst>`
Replaces `cp`. Copies a file. Creates destination parent directories as needed. Used by Phase 6 for archival when the source must be preserved.

### `make_dir.py <path>`
Replaces `mkdir -p`. Creates a directory and all parent directories if they don't exist. Logs invocation and result to `scripts-records.log`. Use when any phase needs to create a new directory (e.g., `tests/e2e/`).

### `run_unit_tests.py <BKI-ID> [sprint-folder]`
Runs unit tests (Jest if `package.json` present, else pytest). Saves full output to `test-results/<sprint-folder>/<BKI-ID>_unit.txt` (sprint-folder defaults to BKI-ID if omitted). Exits 1 if tests fail — hard gate in Phase 3 (Red) and Phase 5 (DoD).

### `run_e2e_tests.py <BKI-ID> [sprint-folder]`
Runs Playwright E2E test suite (`npm run test:e2e`). Saves output to `test-results/<sprint-folder>/<BKI-ID>_e2e.txt`. Required for UI stories (Phase 2 impact map includes HTML/CSS). Exits 1 on failure.

### `capture_screenshot.py <BKI-ID> [sprint-folder]`
Starts a static server (`npx serve src -p 3000`), captures a Playwright screenshot of `http://localhost:3000`, saves to `test-results/<sprint-folder>/<BKI-ID>_ui.png`, then kills the server. Required DoD artifact for UI stories in Phase 5.

### `script_logger.py`
Shared utility module. Not invoked directly. Imported by all other Python scripts via `sys.path.insert`. Provides `log_invocation(script, args)` and `log_result(script, status, detail)`. Writes to `logs/scripts-records.log` in append-only mode.
