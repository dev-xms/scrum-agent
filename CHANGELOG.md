# CHANGELOG

## [Sprint 1] — 2026-04-20

### Added
- **BKI-001** Save a Recipe: form validates required fields, persists to LocalStorage, displays in list
- **BKI-002** View Recipe List: renders all saved recipes with title; shows empty-state message when none
- **BKI-003** Delete a Recipe: removes recipe by ID from LocalStorage; list updates immediately

### Technical Decisions
- ADR-001: Vanilla JS + static HTML/CSS (no framework); single `src/app.js` module (~23 lines)
- Storage: LocalStorage key `smart_plate_recipes`, JSON array

### Verification
- 11/11 tests passing (Jest)
- All Gherkin scenarios for BKI-001, BKI-002, BKI-003 covered
- No orphaned imports or ghost work
