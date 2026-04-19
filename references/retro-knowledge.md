# Retro Knowledge & Lessons Learned

This document tracks historical process failures and successes to ensure continuous improvement of the Scrum Agent.

## ⚠️ Known Pitfalls (Conflict Detection)
*   **Assumption Trap**: In Sprint BKI-002, the agent assumed the database schema was SQL without checking. 
    *   *Rule*: Always run `ls -R` or `grep` to verify technology stack before drafting ACs.
*   **Over-Engineering**: In Sprint BKI-005, a simple utility was implemented as a class factory.
    *   *Rule*: Apply the "50-line test." If it can be done in 50 lines, reject 500-line abstractions.

## ✅ Process Best Practices
*   **Gherkin Clarity**: Acceptance Criteria (AC) written in Given/When/Then format reduced Phase 3 (TDD) generation errors by 40%.
*   **Log-Before-Act**: Writing the start of a phase to `log.md` prevented "ghost work" during session timeouts.

## 🔄 Active Improvement Actions
*   [ ] Improve the "Contradiction Check" in Phase 1 to specifically look for naming convention conflicts.
*   [ ] Ensure `tdd-spec-generator` (Phase 3) always includes edge-case testing for null inputs.