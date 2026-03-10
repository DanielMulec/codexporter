# Changelog

All notable changes to this repository will be documented in this file.

The format is based on Keep a Changelog, and this project intends to follow Semantic Versioning once versioned releases exist.

## [Unreleased]

## [v0.0.4] - 2026-03-10

### Added

- Added `docs/spec/03_product_definition.md` for the product problem statement, goals, and non-goals.
- Added `docs/spec/04_assumptions_and_constraints.md` for assumptions, platform constraints, and UX principles.
- Added `docs/spec/05_open_questions_and_next_steps.md` for open questions and the next spec steps.

### Changed

- Reduced `docs/spec/01_product_triage.md` to a pure must/should/could prioritization document.
- Updated `docs/spec/02_user_stories.md` to reflect the stricter separation between prioritization and the other spec artifacts.

## [v0.0.3] - 2026-03-10

### Changed

- Refined `AGENTS.md` authority wording to remove the equal-weight versus final-authority ambiguity.
- Consolidated overlapping `AGENTS.md` rules for decision flow, freshness research requirements, conflict handling, and semantic version changelog policy.

## [v0.0.2] - 2026-03-10

### Added

- Added the standalone user stories document at `docs/spec/02_user_stories.md`.

### Changed

- Moved the detailed user stories out of `docs/spec/01_product_triage.md` so the triage document stays focused on scope, assumptions, and open decisions.

## [v0.0.1] - 2026-03-10

### Added

- Added the initial product triage document at `docs/spec/01_product_triage.md`.

### Changed

- Updated `AGENTS.md` to remove the carried-over project-specific wording while keeping the rest of the document unchanged.
- Updated `AGENTS.md` to require semantic versioning release entries in `CHANGELOG.md`, starting at `v0.0.1`.
- Converted `CHANGELOG.md` from a generic unreleased list to semantic versioned release entries.
