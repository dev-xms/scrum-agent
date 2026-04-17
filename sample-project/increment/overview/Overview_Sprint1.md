---
type: overview
sprint_id: BKI-001
tags: [sprint-1, recipe-box, crud]
summary: "Sprint 1 delivered core CRUD — save, view, delete recipes via LocalStorage with mobile-first UI."
sources: ["requirements/smart_plate_requirements.md"]
updated: 2026-04-17
---

# Overview: Sprint 1 — The Basic Digital Box

## Goal
Deliver a working in-browser recipe box: save, view, and delete recipes with no backend.

## Scope
- US.1: Save recipe (Title, Ingredients, Instructions)
- US.2: View recipe list
- US.3: Delete recipe with confirmation

## Key Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| CSS framework | Tailwind CDN | No build step — open index.html directly |
| Storage | LocalStorage (`smartplate_recipes`) | Demo constraint, no Firebase needed |
| Data shape | `{id, title, ingredients, instructions}` | Minimal fields from US.1 |
| XSS prevention | `textContent` only, never `innerHTML` | User content rendered safely |
| Delete confirm | `window.confirm()` | No extra dependency, satisfies AC-6 |

## AC Coverage

| AC | File |
|----|------|
| AC-1 (save happy path) | app.js `saveRecipe()` |
| AC-2 (save validation) | app.js `validateForm()` |
| AC-3 (list render) | app.js `renderList()` |
| AC-4 (empty state) | app.js `renderList()` |
| AC-5 (delete + persist) | app.js `deleteRecipe()` |
| AC-6 (delete confirm) | app.js `deleteRecipe()` |
| AC-N1 (mobile-first) | style.css |
| AC-N2 (no console errors) | verified manually |
| AC-N3 (Chrome + Safari) | verified manually |

## Source
- [[sources/Source_SmartPlateRequirements]]
