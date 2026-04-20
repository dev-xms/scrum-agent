# BKI-001: The Smart Plate — Sprint 1 "Basic Digital Box"

## User Story
> **As a** busy parent or health enthusiast  
> **I want to** save, view, and delete recipes (Title, Ingredients, Instructions)  
> **So that** I can digitize and manage my personal cookbook without losing recipes

## Scope
Sprint 1 Goal: US.1 + US.2 + US.3

---

## Acceptance Criteria

### US.1 — Save Recipe
- **Given** I am on the main page
- **When** I fill in Title, Ingredients, and Instructions and click "Save"
- **Then** the recipe is persisted to LocalStorage and appears in the recipe list

- **Given** I submit the form with any required field empty
- **When** I click "Save"
- **Then** a validation error is shown and no recipe is saved

### US.2 — View Recipe List
- **Given** I have at least one saved recipe
- **When** I open or refresh the app
- **Then** all saved recipes are displayed in a list with their titles visible

- **Given** no recipes have been saved
- **When** I open the app
- **Then** an empty-state message is shown (e.g., "No recipes yet")

### US.3 — Delete Recipe
- **Given** I have at least one recipe in the list
- **When** I click "Delete" on a recipe
- **Then** the recipe is removed from LocalStorage and disappears from the list immediately

---

## Non-Functional Requirements
- [ ] Performance: UI interactions (save, delete, load) must complete within 300ms.
- [ ] Security: No external data transmission; all data stays in LocalStorage.
- [ ] Logging: Must write outcome to `log.md`.
- [ ] Responsiveness: Mobile-first layout; usable on tablet (min 768px viewport).
- [ ] Compatibility: No console errors on Chrome and Safari (desktop + mobile).

---

## Definition of Done
1. Code peer-reviewed (or demo double-checked).
2. UI matches basic layout requirements.
3. Feature works on both Desktop and Mobile browsers.
4. No console errors present.

---

## Technical Constraints
- **Test Framework**: pytest (not Jest/jsdom)
- Logic under test must be extractable to Python (backend validation layer or headless test via selenium/playwright if needed)

---

## Estimates
- US.1: 3 points | US.2: 2 points | US.3: 1 point | **Total: 6 points**
