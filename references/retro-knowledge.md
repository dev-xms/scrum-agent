# Retro Knowledge Base

## Known Pitfalls
<!-- Recurring mistakes to avoid -->

## Process Best Practices
<!-- Validated workflow patterns -->

## Active Improvement Actions
<!-- In-flight process changes -->

---

## 🏁 Sprint 1 Retrospective (BKI-001) — 2026-04-20

### Lessons Learned

* **Read tool docs before applying**: Playwright CLI has an `--output` flag that controls where test artifacts land (default: `test-results/` in cwd). Assuming defaults without checking caused a stray directory in repo root. Rule: run `--help` or check docs for any new CLI tool before wiring it into scripts.

* **Don't make redundant infra calls**: Phase 5 manually called `make_dir.py` to pre-create the sprint results folder — the test scripts already do this internally via `Path.mkdir(exist_ok=True)`. Check if a script self-provisions before adding external setup steps.

* **Proceed step by step, don't rush or skip**: Mid-sprint test framework switch (Jest→pytest) required backtracking. Slow down during Phase 1/2 to validate all constraints (tooling, environment) before committing to a design.

* **Verify environment before Red Phase**: Playwright was referenced in Phase 2 design but not installed. E2E Red Phase confirmation was partial. Environment dependencies (npm packages, browser drivers) must be confirmed present before spec generation.

(User-noted during retro: "Tests look smooth finally. Need to go extra step to understand the tool before applying (e.g. output args for Playwright — real case). Relax, proceed step by step, don't skip/rush.")

---

## 🏁 Sprint 2 Retrospective (BKI-002) — 2026-04-20

### Lessons Learned

* **`tests/scripts/` must not hardcode project-specific paths**: Scripts like `run_e2e_tests.py` used hardcoded dir conventions (`playwright/` subdir) and project-specific server commands (`python3 -m http.server --directory src`). These should be configurable (env vars, args, or config file) so scripts are genuinely reusable across projects and for regression reruns.

* **Reusable script requirement is project-wide**: Every phase (1–6) must invoke test/env/setup operations via `tests/scripts/` or `scripts/`. No raw CLI commands anywhere — not just in Phase 3. This applies to Phase 5 (capture_screenshot), Phase 4 verification loops, and any ad-hoc reruns.

* **Playwright `--output` wipes its target dir**: The `--output` flag causes Playwright to clean the directory before writing. Never point it at the sprint artifact folder directly — always use a subdir (e.g., `Sprint-N/playwright/`). Learned via artifact loss in Phase 5.

* **Phase 3 E2E speed**: `webServer` in `playwright.config.js` caused long startup waits. Managing server lifecycle inside `run_e2e_tests.py` is faster and more controllable.

(User-noted during retro: "Phase 1–4 smooth now. tests/scripts should not hardcode — (a) project-specific, (b) need reuse for regression reruns. Reminder: reusable script requirement for entire project.")
