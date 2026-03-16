# Engineering Policy

## Purpose

This document is the project-specific engineering source of truth for this repository.

It exists to prevent fresh chats, reviews, and implementation work from inheriting incorrect stack assumptions from older projects.

## Source Of Truth Rule

For this repository:

- `AGENTS.md` remains the source of truth for collaboration rules
- this document is the source of truth for project-specific engineering policy
- when engineering guidance in `AGENTS.md` conflicts with this document, this document wins for this repository

## Current Project Type

This repository is specifying and beginning to implement a Codex skill.

It is a local exporter and integration tool for Codex session data, not a conventional web application.

## Current Engineering Status

- the initial implementation stack is now approved for v1 development
- the global install boundary is now approved, but release and versioning details are still not fully decided yet
- CI wiring beyond the initial local quality gates is still not fully decided yet
- Windows-specific implementation adjustments remain subject to follow-up after macOS validation
- only already-approved spec decisions should be treated as binding engineering constraints

## Approved Initial Stack Decisions

Decision date: March 13, 2026.

### Runtime And Language

- Python 3.12+ is the approved implementation language for the v1 exporter and supporting utilities.
- This choice is approved because the current persisted-session surface is filesystem- and text-centric, with JSONL rollout data and SQLite metadata, and Python handles those sources with low toolchain overhead.

### Automated Test Harness

- `pytest` is the binding automated test runner for unit, integration, and full-flow coverage.
- Manual platform validation remains separate and is recorded through `docs/spec/22_platform_validation.md` and linked validation evidence.

### Static Analysis And Formatting

- `mypy` in `strict` mode is required for project code.
- `ruff check` is required.
- `ruff format --check` is required.
- `ruff` rule `C901` is required with `lint.mccabe.max-complexity = 10`.
- Do not add `flake8`, `pylint`, SonarQube, or another second general-purpose static-analysis layer unless a demonstrated gap justifies it.

### Modular File Size Rule

- no `.py` source file should exceed 400 lines without strong justification
- at 320+ lines, proactively evaluate split options
- if a file approaches 400 lines, split responsibilities before adding more logic

Preferred split strategies:

- separate transport from business logic
- separate parsing or normalization from rendering or formatting
- separate persistence access from export composition

### Fixtures And Validation Evidence

- automated tests must use sanitized repo-local fixtures derived from real persisted-session structures
- the first fixture set should be captured on macOS
- detailed platform-validation evidence lives under `docs/validation/`
- `docs/spec/22_platform_validation.md` remains the checklist and index, not the storage location for all raw validation evidence

### Install Boundary

- the installable skill artifact lives at `skills/export/`
- the skill is intended to be installed once globally through the skill installer and then reused across project contexts
- runtime output must always resolve from the active project root, never from the installed skill directory
- if the active project root cannot be determined responsibly, the skill must fail clearly rather than guess

### Ignore Rules And Local-Only Artifacts

- use `.gitignore` for ignore rules that should apply to every clone of this repository
- use `.git/info/exclude` for repo-local ignore rules that should stay on one machine and must not appear on GitHub
- use the global Git excludes file via `core.excludesFile` only for machine-wide noise that is not specific to this repository
- when choosing between `.gitignore` and `.git/info/exclude`, prefer the narrowest scope that matches the intent
- ignore rules do not stop tracking files that are already in Git; if a tracked file must remain on disk but leave version control, remove it from the index explicitly

### Security Scanning

- `Trivy` is approved as a CI security gate after dependency manifests and CI wiring exist.
- The initial Trivy scope should be filesystem vulnerability and secret scanning.
- Misconfiguration scanning may be added later when the repository has enough config surface to justify it.
- Container or image scanning is not in scope unless the project later introduces Docker or packaged runtime images.

## Hard Rule On Still-Undecided Choices

Beyond the approved stack decisions in this document:

- do not assume a separate service layer or HTTP API
- do not assume a separate user-interface framework
- do not assume an application-owned database
- do not assume a browser automation framework
- do not assume a packaging or distribution model
- do not treat carried-over tooling from another project as binding here

Unapproved tools from older projects are not standards for this repository unless and until this document says so.

## Current Binding Engineering Constraints

The following engineering constraints are already approved through the spec documents:

- the product is a Codex skill for exporting the current session
- the primary export artifact in v1 is one markdown file per successful export invocation
- repeated exports in the same session are incremental
- checkpoint state is stored in a JSON sidecar
- export artifacts are written into `codex_exports` under the current project root
- the globally installed skill boundary lives at `skills/export/`, and install location does not determine export destination
- user-visible failures must be explicit and language-sensitive
- deferred post-v1 features must integrate additively rather than redefining v1 semantics

## Binding Test Layers

The project already defines required test layers conceptually:

- unit
- integration
- full-flow
- manual platform validation

Those layers are defined in:

- `docs/spec/20_test_taxonomy.md`
- `docs/spec/21_coverage_matrix.md`
- `docs/spec/22_platform_validation.md`

The approved tool choice for automated unit, integration, and full-flow coverage is `pytest`.

## Binding Quality Gates

Before a change is considered done, the following quality gates are binding once the relevant tooling is configured in the repository:

- `pytest`
- `mypy`
- `ruff check`
- `ruff format --check`

When CI is introduced and dependency manifests exist, add:

- `trivy fs` for filesystem vulnerability and secret scanning

Tool-specific settings should be recorded in `pyproject.toml` or the relevant tool configuration files once those files are introduced.

## Engineering Review Rule

Until further stack decisions are approved:

- reviews may challenge correctness, traceability, product behavior, validation gaps, and spec contradictions
- reviews may treat the approved Python, pytest, mypy, ruff, file-size, and Trivy baseline as binding
- reviews must not treat an unapproved framework or tool as mandatory
- if a review recommendation depends on a specific tool or stack, that recommendation must be labeled as contingent rather than normative

## How To Record New Engineering Decisions

When a stack or tooling decision is approved, update this document with:

- decision date
- chosen tool or framework
- scope of use
- why it was chosen
- what alternatives were rejected if that matters
- what new quality gates become binding because of the choice

## Living-Document Rule

This document is intended to stay alive throughout the project.

After initial stack selection, it should expand only where a decision is actually approved.

It should still avoid fake certainty for packaging, distribution, CI shape, or platform-specific details that remain undecided.
