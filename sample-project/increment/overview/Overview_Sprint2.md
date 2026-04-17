---
type: overview
sprint_id: BKI-002
tags: [sprint-2, search, dark-mode]
summary: "Sprint 2 added client-side recipe search and persistent dark mode toggle."
sources: ["requirements/smart_plate_requirements.md"]
updated: 2026-04-17
---

# Overview: Sprint 2 — The Smart Searcher

## Goal
Deliver recipe search by name and a dark mode toggle, building on Sprint 1's CRUD foundation.

## Scope
- US.4: Search recipes by name (client-side filter)
- US.6: Dark Mode toggle (CSS class + LocalStorage persistence)

## Sprint Review Feedback Carried Forward (from Sprint 1)
- Form layout too long — collapsible/modal (future backlog)
- Recipe cards need more visible detail e.g. ingredient count (future backlog)

## Key Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Search trigger | `input` event (live filter) | No submit needed — instant UX |
| Search scope | Title only | Requirements say "by name" — no overreach |
| Search XSS safety | Term used in JS `.includes()` only, never rendered as HTML | Prevents injection |
| Dark mode mechanism | `.dark` class on `<body>` + CSS overrides | No framework needed, Tailwind-compatible |
| Dark persistence | `smartplate_dark` key in LocalStorage | Consistent with recipe storage pattern |
| Toggle label | Swaps "Dark Mode" ↔ "Light Mode" | Clear feedback to user |

## AC Coverage

| AC | Description | File |
|----|-------------|------|
| AC-1 | Search filters by title (case-insensitive) | app.js `filterRecipes()` |
| AC-2 | Clear search restores full list | app.js `renderList('')` on empty input |
| AC-3 | No match → "No recipes match your search." | app.js `renderList()` |
| AC-4 | Dark mode toggles on | app.js `toggleDark()` + style.css `.dark` |
| AC-5 | Dark pref persists after reload | app.js `loadDarkPref()` on init |
| AC-6 | Second toggle restores light mode | app.js `classList.toggle('dark')` |
| AC-N1 | Search usable on 375px | index.html full-width input |
| AC-N2 | Dark mode readable contrast | style.css color overrides |
| AC-N3 | No console errors | verified via Playwright |

## Related
- [[sources/Source_SmartPlateRequirements]]
- [[overview/Overview_Sprint1]]
