# Project Coding Standards & Karpathy Principles

All code modifications must adhere to these standards to ensure project maintainability and surgical precision.

## 1. The Karpathy Principles [7]
*   **Think Before Coding**: State assumptions explicitly in `log.md`. If a requirement is ambiguous, stop and ask for clarification [8].
*   **Simplicity First**: Implement the minimum code that solves the problem. No speculative "flexibility" or unrequested features [9].
*   **Surgical Changes**: Touch only what you must. Match existing styles and clean up ONLY the "mess" created by the current task [10].
*   **Goal-Driven Execution**: Define success via failing tests first. Loop execution until tests pass [11].

## 2. Surgical Modification Rules
*   **No Drive-by Refactoring**: Do not "improve" adjacent code, comments, or formatting that is orthogonal to the task [10].
*   **Orphan Management**: If your changes make an import or function unused, you MUST remove it [10].
*   **Style Match**: Adhere to the current file's indentation, naming, and documentation style even if it contradicts global preferences.

## 3. Implementation Patterns [12, 13]
*   **Sequential Orchestration**: Multi-step tasks must be broken down into explicit steps with validation gates in between.
*   **Error Handling**: Do not write error handling for "impossible" scenarios; keep the logic path lean and focused on the core requirement [9].
