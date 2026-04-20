# Project Requirements: "The Smart Plate" (Scrum Demo)

## 1. Project Overview
**The Smart Plate** is a lightweight, web-based MVP (Minimum Viable Product) designed to help users organize their home recipes. The goal of this project is to demonstrate how Scrum allows a team to deliver a functional product incrementally, handle changing requirements, and maintain high quality through a defined 'Definition of Done'.

---

## 2. Target Personas
* **The Busy Parent (Primary User):** Needs a quick way to store recipes found online so they don't lose them. Values speed and simplicity.
* **The Health Enthusiast:** Wants to track what goes into their meals but is easily overwhelmed by complex apps.

---

## 3. Product Backlog (User Stories)

| ID | User Story | Priority | Est. Points |
|:---|:---|:---|:---:|
| **US.1** | As a user, I want to **save a recipe** (Title, Ingredients, Instructions) so I can digitize my cookbook. | High (Must) | 3 |
| **US.2** | As a user, I want to **view a list** of all my saved recipes so I can decide what to cook. | High (Must) | 2 |
| **US.3** | As a user, I want to **delete a recipe** I no longer like to keep my list clean. | Medium (Should) | 1 |
| **US.4** | As a user, I want to **search for recipes** by name so I can find them quickly. | Medium (Should) | 3 |
| **US.5** | As a user, I want to **upload a photo** of the dish to make the list look appetizing. | Low (Could) | 5 |
| **US.6** | As a user, I want a **"Dark Mode"** toggle so I can read recipes comfortably at night. | Low (Could) | 2 |

---

## 4. Technical Requirements
To keep the demo agile and focused on the process rather than infrastructure:

### Front-End
* **Framework:** HTML5, CSS3 (using a framework like Tailwind or Bootstrap for speed).
* **Interactivity:** Vanilla JavaScript or React (Standard CRUD operations).
* **Responsiveness:** Must be "Mobile-First" (usable on a tablet in the kitchen).

### Back-End & Storage
* **Storage:** LocalStorage (for the demo) or a simple Firebase instance to show real-time updates.
* **Logic:** Simple filtering for the search functionality.

---

## 5. Definition of Done (DoD)
A story is only "Done" when:
1.  Code is peer-reviewed (or double-checked during the demo).
2.  UI matches the basic layout requirements.
3.  The feature works on both Desktop and Mobile browsers.
4.  No console errors are present.

---

## 6. Demo Sprint Plan
* **Sprint 1 Goal:** "The Basic Digital Box" - Implement US.1, US.2, and US.3.
* **Sprint 2 Goal:** "The Smart Searcher" - Implement US.4 and pivot based on Review feedback (e.g., US.6).
