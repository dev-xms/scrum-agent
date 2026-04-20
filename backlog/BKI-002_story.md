# BKI-002: The Smart Plate — Sprint 2 "The Smart Searcher"

## User Story
> **As a** busy parent or health enthusiast
> **I want to** search recipes by name and toggle dark mode
> **So that** I can find recipes quickly and read them comfortably at night

## Scope
Sprint 2 Goal: US.4 + US.6

---

## Acceptance Criteria

### US.4 — Search Recipes by Name
- **Given** I have multiple saved recipes
- **When** I type a name (or partial name) into the search field
- **Then** only recipes whose titles match the input are displayed

- **Given** I have typed a search query that matches no recipes
- **When** the search input is non-empty
- **Then** an empty-state message is shown (e.g., "No recipes match your search")

- **Given** I have an active search filter
- **When** I clear the search field
- **Then** all saved recipes are displayed again

### US.6 — Dark Mode Toggle
- **Given** I am viewing the app in light mode (default)
- **When** I click the dark mode toggle
- **Then** the UI switches to a dark color scheme

- **Given** I am viewing the app in dark mode
- **When** I click the dark mode toggle again
- **Then** the UI reverts to light mode

- **Given** I have previously enabled dark mode
- **When** I refresh the page
- **Then** dark mode preference is preserved (persisted to LocalStorage)

---

## Non-Functional Requirements
- [ ] Performance: Search filtering must complete within 100ms for up to 100 recipes.
- [ ] Security: No external data transmission; all data stays in LocalStorage.
- [ ] Logging: Must write outcome to `log.md`.
- [ ] Responsiveness: Mobile-first layout; usable on tablet (min 768px viewport).
- [ ] Compatibility: No console errors on Chrome and Safari (desktop + mobile).

---

## Technical Constraints
- **Test Framework**: pytest (unit logic) + Playwright E2E (UI behavior)
- **Environment**: Playwright must be installed (`npm install playwright && npx playwright install`) before Phase 3 E2E spec generation — verify upfront (retro lesson BKI-001)
- Search logic must be extractable to Python for pytest coverage

---

## Definition of Done
1. Code peer-reviewed (or demo double-checked).
2. UI matches basic layout requirements.
3. Feature works on both Desktop and Mobile browsers.
4. No console errors present.

---

## Estimates
- US.4: 3 points | US.6: 2 points | **Total: 5 points**
