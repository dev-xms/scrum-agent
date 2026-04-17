# The Smart Plate

A lightweight, mobile-first web app for organizing home recipes. Built as a Scrum demo project to showcase incremental delivery — no backend, no build step, runs in any modern browser.

---

## Features

| Feature | Status | Sprint |
|---------|--------|--------|
| Save recipe (Title, Ingredients, Instructions) | ✅ Done | BKI-001 |
| View all saved recipes | ✅ Done | BKI-001 |
| Delete a recipe (with confirmation) | ✅ Done | BKI-001 |
| Search recipes by name | ✅ Done | BKI-002 |
| Dark mode toggle (persists across sessions) | ✅ Done | BKI-002 |
| Upload a photo of a dish | 🔲 Backlog | BKI-003 |
| Collapsible form layout | 🔲 Backlog | BKI-004 |
| Richer recipe cards (ingredient summary) | 🔲 Backlog | BKI-004 |

---

## Getting Started

1. Clone or download this repo
2. Open `src/index.html` in Chrome or Safari
3. No install, no build — that's it

> **Internet required on first load** — Tailwind CSS loads from CDN.

---

## How It Works

- **Storage:** All recipes saved to `localStorage` under key `smartplate_recipes`
- **Dark mode:** Preference saved to `localStorage` under key `smartplate_dark`
- **Search:** Live client-side filter on recipe title (case-insensitive)
- **Delete:** Requires `window.confirm()` before removal

---

## Project Structure

```
sample-project/
├── requirements/          # Source of truth (read-only)
│   └── smart_plate_requirements.md
├── sprints/               # One BKI file per backlog item
│   ├── BKI-001.md         ✅ done
│   ├── BKI-002.md         ✅ done
│   ├── BKI-003.md         🔲 backlog — photo upload
│   └── BKI-004.md         🔲 backlog — UX improvements
├── increment/             # Wiki: decisions, overviews, cross-refs
│   ├── index.md
│   ├── sources/
│   └── overview/
├── src/                   # App source
│   ├── index.html
│   ├── app.js
│   └── style.css
├── tests/                 # Test results + screenshots
│   ├── BKI-001_test_results.md
│   ├── BKI-001_mobile-375px.png
│   ├── BKI-002_test_results.md
│   ├── BKI-002_mobile-375px.png
│   └── BKI-002_dark-mode.png
└── log.md                 # Append-only sprint audit log
```

---

## Tech Stack

| Layer | Choice |
|-------|--------|
| HTML | HTML5 |
| CSS | Tailwind CSS 2.2 (CDN) + custom dark mode |
| JS | Vanilla JavaScript (ES6+) |
| Storage | Browser `localStorage` |
| Testing | Playwright (browser automation) |

---

## Scrum Process

This project follows the [Scrum-Agent framework](../SCRUM-AGENT.md). Each feature goes through 5 phases:

```
PLANNING → REFINEMENT → EXECUTION → INCREMENT → DONE
```

All phase transitions are logged in `log.md` before work begins. No sprint closes without a passing DoD check and test artifacts in `tests/`.
