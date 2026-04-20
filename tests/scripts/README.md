# tests/scripts — Test Runner Reference

Scripts for executing tests and capturing artifacts. Called by Phase 3 (Red Phase), Phase 4 (Green Phase), and Phase 5 (Auditor).

## Script Reference

| Script | Phase(s) | Args |
| :--- | :--- | :--- |
| `run_unit_tests.py` | 3, 4, 5 | `<BKI-ID\|regression> [sprint-folder]` |
| `run_e2e_tests.py` | 3, 4, 5 | `<BKI-ID\|regression> [sprint-folder]` |
| `capture_screenshot.py` | 5 | `<BKI-ID> <sprint-folder>` |
| `check_env.py` | 3 (pre-flight) | none |
| `check_playwright_pkg.py` | 3 (pre-flight) | none |
| `setup_playwright.py` | 3 (one-time setup) | none |

## Artifact Saving

Pass `sprint-folder` (e.g. `Sprint-1-BKI-001`) to activate artifact mode:
- Output written to `tests/results/{sprint-folder}/`
- Unit: `{BKI-ID}_unit.txt` or `regression_unit.txt`
- E2E: `{BKI-ID}_e2e.txt` or `regression_e2e.txt`
- Screenshot: `{BKI-ID}_ui.png`

Without `sprint-folder`: runs tests live, no artifact saved (Phase 3/4 usage).

## Script Descriptions

### `check_env.py`
Pre-flight check for Phase 3. Verifies `node`, `npx`, and `playwright` CLI are available. Run before writing E2E specs.

### `check_playwright_pkg.py`
Verifies `@playwright/test` npm package is locally installed (resolvable by `node`). Run after `check_env.py`. Prints fix instructions if missing.

### `setup_playwright.py`
One-time setup: runs `npm init -y`, `npm install @playwright/test`, and `npx playwright install`. Run once per project when `check_playwright_pkg.py` reports MISSING.

## Notes
- `run_e2e_tests.py` pre-starts HTTP server on port 8080, passes `--output {artifact-dir}` to Playwright, kills server after run.
- `capture_screenshot.py` uses macOS `qlmanage` — requires macOS environment.
