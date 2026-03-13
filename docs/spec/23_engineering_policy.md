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

This repository is currently specifying a Codex skill.

It is not yet a conventional backend-plus-frontend application with an approved web stack.

## Current Engineering Status

- the implementation stack is not fully decided yet
- the testing toolchain is not fully decided yet
- packaging and distribution details are not fully decided yet
- only already-approved spec decisions should be treated as binding engineering constraints

## Hard Rule On Undecided Stack Choices

Until a stack choice is explicitly approved in this document:

- do not assume a backend framework
- do not assume a frontend framework
- do not assume a database
- do not assume a browser automation framework
- do not assume a unit-test or integration-test runner
- do not treat carried-over tooling from another project as binding here

Examples of assumptions that are currently not allowed:

- `FastAPI`
- `React`
- `Vite`
- `Vitest`
- `Playwright`
- `SQLAlchemy`
- `Alembic`

These tools may still be proposed later, but they are not standards for this project unless and until this document says so.

## Current Binding Engineering Constraints

The following engineering constraints are already approved through the spec documents:

- the product is a Codex skill for exporting the current session
- the primary export artifact in v1 is one markdown file per successful export invocation
- repeated exports in the same session are incremental
- checkpoint state is stored in a JSON sidecar
- export artifacts are written into `codex_exports` under the current project root
- user-visible failures must be explicit and language-sensitive
- deferred post-v1 features must integrate additively rather than redefining v1 semantics

## Testing Policy Before Stack Selection

The project already defines required test layers conceptually:

- unit
- integration
- full-flow
- manual platform validation

Those layers are defined in:

- `docs/spec/20_test_taxonomy.md`
- `docs/spec/21_coverage_matrix.md`
- `docs/spec/22_platform_validation.md`

But the exact tools used to implement those layers are not fixed yet.

## Engineering Review Rule

Until the stack is fixed:

- reviews may challenge correctness, traceability, product behavior, validation gaps, and spec contradictions
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

Before stack selection, it should stay intentionally narrow and avoid fake certainty.

After stack selection, it should expand to capture the real engineering standards that are actually approved for this repository.
