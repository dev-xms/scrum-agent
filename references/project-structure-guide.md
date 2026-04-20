# Software Development Project Structure Guide

A well-organized project structure is a **game-changer** that prevents code duplication, enhances stability, and enables seamless scaling. While structures vary by language, modern development focuses on the **principle of separation of concerns** and **service-layered architecture**.

---

### 1. Java (Spring Boot / Maven Standard)
Java projects typically follow the **Apache Maven Standard Directory Layout**, which provides a common look-and-feel across the ecosystem.

*   **Standard Layout**:
    *   `src/main/java`: Application/Library sources (package hierarchy).
    *   `src/main/resources`: Configuration and static resources.
    *   `src/test/java`: Unit and integration test sources.
    *   `target/`: Build output and artifacts.
*   **Layered Architecture Recommendation**:
    *   `controller`: Handles incoming requests (keep these thin).
    *   `service`: Contains **core business logic** (often using the Interface + Implementation pattern).
    *   `repository`: Data access layer (e.g., `JpaRepository`).
    *   `entity`: Database table mappings.
    *   `dto`: Data Transfer Objects to avoid exposing internal entities.
    *   `exception`: Global error handling logic.
*   **Strategic Evolution**: For large projects, use a **feature-based structure** (e.g., `com.app.order`, `com.app.user`) to simplify future extraction into **microservices**.

### 2. Go (Modules and Commands)
Go projects are organized based on the type of artifact being built, often utilizing an `internal` directory to prevent external modules from depending on private logic.

*   **Server Project Structure**:
    *   `cmd/`: Contains the main application entry points (e.g., `cmd/server/main.go`).
    *   `internal/`: Houses the server's logic; these packages cannot be imported by other modules.
    *   `pkg/`: (Optional) Logic intended for use by other projects.
*   **Core Principles**: Keep simple packages in the root directory and use **hierarchical sub-packages** for complex projects.

### 3. Python (src Layout)
The **src/ layout** is strongly recommended as it ensures tests run against the installed version of the package rather than local files.

*   **Recommended Structure**:
    *   `src/package_name/`: Primary directory for source code and modules.
    *   `tests/`: Located at the root level, outside the `src/` folder.
    *   `docs/`: User-facing documentation.
    *   `pyproject.toml`: Build configuration and metadata.
*   **Avoid**: Do not include test datasets directly in the package; host them externally to keep distribution sizes small.

### 4. TypeScript / JavaScript (Node.js & React)
For Node.js, the community is moving toward **feature-based organization** to group related files by domain rather than type.

*   **Node.js Feature-Based Structure**:
    *   `src/features/`: Subdirectories for each domain (e.g., `auth/`, `users/`).
        *   `*.controller.ts`: Request handling.
        *   `*.service.ts`: **Brain of the feature** containing business logic.
        *   `*.model.ts`: Database schemas.
    *   `src/middleware/`: Shared custom Express middleware.
    *   `src/config/`: Centralized settings (secrets handled via `.env`).
*   **React Frontend Structure**:
    *   **Advanced Scale**: Use a `features/` folder where each feature exposes a **public API** via an `index.js` file.
    *   `layouts/`: Reusable layout components like navbars or sidebars.
    *   `lib/`: Facades for third-party libraries (e.g., axios) to simplify future updates.

---

### 5. Scrum-Agent Skeleton (Language-Neutral)

`scripts/init.sh` creates this skeleton before any implementation code exists. It is language-agnostic — Phase 2 (Architect) fills in the internal structure of `src/` and `tests/unit/` based on the chosen language (see Section 6).

```
project-root/
├── adr/                  # ADR-XXX_<slug>.md — Phase 2 outputs
├── backlog/              # BKI-XXX_story.md — Phase 1 outputs
├── requirements/         # Raw intake docs — human-authored, agent reads only
├── src/                  # Implementation code — language-specific (see Section 6)
├── tests/
│   ├── unit/             # Unit test files — Phase 3/4
│   ├── e2e/              # Playwright E2E specs — Phase 3 (UI stories only)
│   ├── scripts/          # Gate scripts: run_unit_tests.py, run_e2e_tests.py
│   └── results/          # Artifacts (gitignored): Sprint-N-BKI-XXX/
│       └── Sprint-N-BKI-XXX/
│           ├── BKI-XXX_unit.txt
│           ├── regression_unit.txt
│           ├── BKI-XXX_e2e.txt    # UI stories only
│           └── BKI-XXX_ui.png     # UI stories only
├── scripts/              # Workflow gates: scrum_guard.py, invest_validator.py
├── references/           # Static docs: retro-knowledge.md, workflow-guidance.md
├── logs/
│   ├── log.md            # Active append-only audit trail
│   ├── scripts-records.log
│   └── archive/          # Rotated per-sprint logs (Phase 6)
└── skills/               # Phase skill files — source of truth for /commands
```

---

### 6. Populating `src/` and `tests/unit/` by Language

The scrum-agent skeleton is language-neutral. Phase 2 (Architect) decides the internal layout of `src/` and `tests/unit/` based on the target language. Use these mappings as the starting point for the Surgical Impact Map.

#### Java (Spring Boot / Maven)
```
src/main/java/<package>/
  controller/    # Request handling — keep thin
  service/       # Core business logic (Interface + Impl pattern)
  repository/    # Data access (JpaRepository)
  entity/        # DB table mappings
  dto/           # Data Transfer Objects
  exception/     # Global error handling
src/main/resources/    # application.yml, static assets
```
Scrum-agent mapping:
- `src/` → `src/main/java/<package>/` + `src/main/resources/`
- `tests/unit/` → `src/test/java/<package>/` (mirrors main package structure)
- `tests/e2e/` → Playwright specs for Spring MVC UI endpoints

#### Go (Modules)
```
src/cmd/<appname>/main.go    # entry point(s)
src/internal/                # private business logic (cannot be imported externally)
src/pkg/                     # optional: shared library code
```
Scrum-agent mapping:
- `src/` → Go module root; `go.mod` at `src/` or project root
- `tests/unit/` → integration-style tests; unit tests (`*_test.go`) live beside source in `src/internal/` per Go convention
- `tests/e2e/` → httptest-based API tests or Playwright for web UI

#### Python (src layout)
```
src/<package_name>/
  __init__.py  models.py  services.py  repositories.py  ...
tests/unit/       # pytest discovers test_BKI_XXX_*.py here
pyproject.toml    # build config and metadata
```
Scrum-agent mapping:
- `src/` → `src/<package_name>/` — src layout prevents import confusion with installed package
- `tests/unit/` → pytest test files (`test_BKI_XXX_*.py`); discovered directly by `tests/scripts/run_unit_tests.py`
- `tests/e2e/` → Playwright specs for web UI, or pytest BDD for API scenarios

#### TypeScript / Node.js (feature-based)
```
src/features/<domain>/
  <domain>.controller.ts   # Request handling
  <domain>.service.ts      # Business logic
  <domain>.model.ts        # DB schema
src/middleware/             # Shared Express middleware
src/config/                 # Centralized settings (.env handled externally)
```
Scrum-agent mapping:
- `src/` → feature-based structure; `src/index.ts` as entry point
- `tests/unit/` → Jest test files (`*.test.ts`) mirroring `src/features/` structure
- `tests/e2e/` → Playwright specs (`BKI-XXX.spec.js`) using `data-testid` selectors

#### React Frontend
```
src/features/<feature>/
  index.js             # Public API for feature
  <Feature>Page.tsx    # Page component
  <feature>.service.ts # Feature-scoped business logic
src/layouts/           # Shared navbars, sidebars
src/lib/               # Facades for third-party libraries (e.g., axios)
```
Scrum-agent mapping:
- `src/` → CRA/Vite root; `src/index.tsx` entry point
- `tests/unit/` → Jest + React Testing Library (`*.test.tsx`)
- `tests/e2e/` → Playwright specs using `data-testid` selectors (enforced by Phase 3 skill)

---

### Architectural Philosophies
*   **3-Layer Architecture**: Decouple the **Routing/Controller** layer from the **Service (Business)** and **Data Access** layers to ensure code is testable and reusable.
*   **Hexagonal Architecture**: Also known as **Ports and Adapters**, this pattern creates loosely coupled components by isolating the application core from external environments like databases or UIs.
*   **Monolithic vs. Microservices**: Monoliths are easier to start with but become complex to scale. Microservices offer flexibility and independent deployment but require more upfront planning and infrastructure.