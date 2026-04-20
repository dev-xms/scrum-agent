# CHANGELOG

## [BKI-002] — 2026-04-20 — The Smart Plate: Sprint 2 "The Smart Searcher"

### Summary
Delivered Sprint 2 of The Smart Plate. Added live recipe search by name (partial, case-insensitive, client-side filtering) and a dark mode toggle with LocalStorage persistence. Search logic extracted to `RecipeStore.filter_recipes()` for pytest coverage; UI wired via `input` event for live filtering.

### Changes
- **Modified** `src/recipe_store.py` — added `filter_recipes(query)` method
- **Modified** `src/app.js` — added `filterRecipes()`, `initDarkMode()`, `DARK_MODE_KEY`; updated `renderList(query)` to accept filter param; wired search `input` event
- **Modified** `src/index.html` — added `input-search`, `btn-dark-mode`, `.header-row` layout
- **Modified** `src/style.css` — added `body.dark` overrides, search input style, dark mode button style
- **Created** `tests/test_BKI_002.py` — 8 pytest unit tests for `filter_recipes()`
- **Created** `tests/e2e/BKI-002.spec.js` — 6 Playwright E2E specs (US.4 + US.6)
- **Modified** `tests/scripts/run_e2e_tests.py` — fixed Playwright `--output` dir wipe bug; added HTTP server lifecycle management
- **Created** `playwright.config.js` — Playwright config with `outputDir: tests/results/playwright`
- **Modified** `skills/tdd-spec-generator.md` — added Section 1c Script Execution Policy hard rule
- **Modified** `tests/scripts/README.md` — documented `check_env.py`, `check_playwright_pkg.py`, `setup_playwright.py`

### Requirements Traceability
- US.4 AC-1 (partial match): `test_us4_search_partial_match`, E2E `US4: partial name match` — PASS
- US.4 AC-2 (no match empty-state): `test_us4_search_no_match_returns_empty`, E2E `US4: no match shows empty-state` — PASS
- US.4 AC-3 (clear restores all): `test_us4_search_empty_query_returns_all`, E2E `US4: clearing search restores all recipes` — PASS
- US.6 AC-1 (toggle on): E2E `US6: clicking dark mode toggle adds dark class` — PASS
- US.6 AC-2 (toggle off): E2E `US6: clicking dark mode toggle again removes dark class` — PASS
- US.6 AC-3 (persist on reload): E2E `US6: dark mode preference persists after reload` — PASS

### Test Artifacts
- `tests/results/Sprint-2-BKI-002/BKI-002_unit.txt` — 8 passed
- `tests/results/Sprint-2-BKI-002/BKI-002_e2e.txt` — 6 passed
- `tests/results/Sprint-2-BKI-002/regression_unit.txt` — 21 passed (BKI-001 + BKI-002)
- `tests/results/Sprint-2-BKI-002/regression_e2e.txt` — 14 passed (all sprints)
- `tests/results/Sprint-2-BKI-002/BKI-002_ui.png` — UI screenshot

### Retro Addendum (Post-Sprint 2 — 2026-04-20)
- **Sprint closure**: BKI-002 officially closed by Phase 6 retro.
- **Post-sprint fixes**: Fixed Playwright `--output` dir wipe — now routes to `Sprint-N/playwright/` subdir. Removed `webServer` from `playwright.config.js` — server managed by runner script.
- **BKI Seeds registered**: None. (Future BKI: refactor `tests/scripts/` to eliminate hardcoded project paths — make server port, directory, and output conventions configurable.)
- **Retro-knowledge rotation**: No rotation — 26 lines before Sprint 2 block, within token budget.

---

## [BKI-001] — 2026-04-20 — The Smart Plate: Sprint 1 "Basic Digital Box"

### Summary
Delivered Sprint 1 MVP of The Smart Plate — a mobile-first, LocalStorage-backed recipe manager. Users can save recipes (Title, Ingredients, Instructions) with validation, view the full list with an empty-state fallback, and delete individual recipes. Logic is implemented as a Python `RecipeStore` class (pytest-testable) plus a Vanilla JS SPA for the browser UI.

### Changes
- **Created** `src/recipe_store.py` — Python RecipeStore class: add/get/delete with validation; pytest target
- **Created** `src/index.html` — App shell with form, recipe list, empty-state, error display; all `data-testid` attributes present
- **Created** `src/style.css` — Mobile-first styles; `@media (min-width: 768px)` breakpoint
- **Created** `src/app.js` — DOM wiring, LocalStorage CRUD, XSS-safe `escapeHtml()` render
- **Created** `tests/test_BKI_001.py` — 13 pytest unit tests covering all AC scenarios
- **Created** `tests/e2e/BKI-001.spec.js` — 9 Playwright E2E specs (pending Playwright install)
- **Created** `tests/scripts/run_unit_tests.py` — pytest runner with optional sprint-folder artifact save
- **Created** `tests/scripts/run_e2e_tests.py` — Playwright runner with `--output` flag; prevents stray `test-results/` dir
- **Created** `tests/scripts/capture_screenshot.py` — qlmanage-based screenshot capture
- **Modified** `backlog/BKI-001_story.md` — refined mid-sprint: added pytest constraint, Technical Constraints section

### Requirements Traceability
- US.1 AC-1 (save persists): `test_us1_save_recipe_persists` — PASS
- US.1 AC-2 (validation error): `test_us1_empty_title_raises`, `test_us1_whitespace_title_raises`, `test_us1_empty_ingredients_raises`, `test_us1_empty_instructions_raises`, `test_us1_invalid_save_does_not_persist` — PASS
- US.2 AC-1 (list on load): `test_us2_get_recipes_returns_all`, `test_us2_recipe_titles_visible` — PASS
- US.2 AC-2 (empty state): `test_us2_empty_store_returns_empty_list` — PASS
- US.3 AC-1 (delete removes): `test_us3_delete_removes_recipe`, `test_us3_delete_only_removes_target` — PASS
- US.3 AC-2 (delete nonexistent): `test_us3_delete_nonexistent_raises` — PASS

### Test Artifacts
- `tests/results/Sprint-1-BKI-001/BKI-001_unit.txt` — 13 passed
- `tests/results/Sprint-1-BKI-001/regression_unit.txt` — 13 passed
- `tests/results/Sprint-1-BKI-001/BKI-001_ui.png` — UI screenshot (qlmanage)
- E2E: spec ready at `tests/e2e/BKI-001.spec.js` — Playwright runtime not installed

### Retro Addendum (Post-Sprint 1 — 2026-04-20)
- **Sprint closure**: BKI-001 officially closed by Phase 6 retro.
- **Post-sprint fixes**: Fixed Playwright stray `test-results/` dir via `--output` flag in `run_e2e_tests.py`.
- **BKI Seeds registered**: None.
- **Retro-knowledge rotation**: No rotation — within token budget (first sprint).
