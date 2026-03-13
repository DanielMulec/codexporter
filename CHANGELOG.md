# Changelog

All notable changes to this repository will be documented in this file.

The format is based on Keep a Changelog, and this project intends to follow Semantic Versioning once versioned releases exist.

## [Unreleased]

## [v0.1.8] - 2026-03-13

### Changed

- Updated `docs/spec/14_test_scenarios.md` so the v1 baseline now explicitly covers prior-artifact immutability, cursor-validation mismatch handling, and per-platform checklist scope for cross-platform validation.
- Updated `docs/spec/18_user_story_mapping.md` and `docs/spec/21_coverage_matrix.md` so repeated-export traceability includes prior-artifact immutability and checkpoint-safety traceability includes cursor-mismatch handling without overstating coverage.

## [v0.1.7] - 2026-03-13

### Added

- Added `docs/spec/23_engineering_policy.md` as the project-specific engineering source of truth until and after stack selection.

### Changed

- Expanded `docs/spec/21_coverage_matrix.md` with a second requirement-level traceability table and explicit design-constraint coverage.
- Updated `docs/spec/08_artifact_structure_and_naming.md`, `docs/spec/13_acceptance_criteria.md`, `docs/spec/14_test_scenarios.md`, `docs/spec/17_user_flows.md`, `docs/spec/19_user_side_acceptance_criteria.md`, and `docs/spec/22_platform_validation.md` to use `current project root` instead of `current project repository`.
- Updated `docs/spec/05_open_questions_and_next_steps.md` to include `23_engineering_policy.md` as a next-step review item.
- Updated `AGENTS.md` so project-specific engineering policy now lives in `docs/spec/23_engineering_policy.md` and stale stack assumptions are no longer treated as binding for this repository.

## [v0.1.6] - 2026-03-13

### Added

- Added `docs/spec/21_coverage_matrix.md` to provide explicit v1 traceability from stories to acceptance criteria to tests and test layers.
- Added `docs/spec/22_platform_validation.md` to define the platform validation checklist and evidence model for the primary v1 targets.

### Changed

- Updated `docs/spec/05_open_questions_and_next_steps.md` to point at coverage-matrix review and platform-validation review as the next spec steps.

## [v0.1.5] - 2026-03-13

### Changed

- Updated `docs/spec/02_user_stories.md` to mark the true v1 story groups versus the post-v1 story groups and to align repeated-export wording with the approved v1 contract.
- Expanded `docs/spec/18_user_story_mapping.md` so the explicit v1 mapping now reflects the full set of user-designated v1 stories.
- Expanded `docs/spec/19_user_side_acceptance_criteria.md` with cross-platform consistency and restricted-environment transparency criteria.
- Updated `docs/spec/14_test_scenarios.md` so the scenario IDs cover first-versus-incremental messaging and restricted-environment transparency.
- Updated `docs/spec/05_open_questions_and_next_steps.md` to remove the now-resolved v1-versus-post-v1 story-boundary question.

## [v0.1.4] - 2026-03-13

### Changed

- Updated `docs/spec/05_open_questions_and_next_steps.md` to reflect the actual remaining spec work after the Track B scaffolding was added.
- Expanded `docs/spec/17_user_flows.md` with fuller blocked-access behavior, explicit no-new-content behavior, and user-facing success communication details.
- Filled `docs/spec/18_user_story_mapping.md` with available acceptance mappings and added stable test scenario mappings.
- Expanded `docs/spec/19_user_side_acceptance_criteria.md` with file-location, no-new-content, incremental-communication, blocked-access-guidance, and default-export-destination criteria.
- Updated `docs/spec/08_artifact_structure_and_naming.md`, `docs/spec/13_acceptance_criteria.md`, and `docs/spec/14_test_scenarios.md` to define the `codex_exports` default destination and the approved no-new-content behavior.
- Updated `docs/spec/20_test_taxonomy.md` to align the integration-test language with the visible-session export model.

## [v0.1.3] - 2026-03-13

### Changed

- Rewrote `docs/spec/16_user_journeys.md` in the same formal product-spec language used by the rest of the documentation.
- Removed the post-v1 `$export --full` mention from `docs/spec/16_user_journeys.md` and aligned the blocked-access journey with the approved degraded-mode behavior.

## [v0.1.2] - 2026-03-13

### Changed

- Expanded `docs/spec/16_user_journeys.md` with the blocked-access journey, filled the repeated-export failure path, and removed the unused notes placeholders.
- Updated `docs/spec/18_user_story_mapping.md` to remove references to the deleted long-running-session journey.

## [v0.1.1] - 2026-03-12

### Changed

- Updated `docs/spec/16_user_journeys.md` with drafted content for the first-export and repeated-export user journeys.

## [v0.1.0] - 2026-03-11

### Changed

- Removed dedicated structured session-level git metadata from the v1 export contract and deferred it to post-v1.
- Clarified that visible git-related tool output remains part of v1 when it appeared in the chat history.
- Updated the Track B starter docs so they no longer treat structured git metadata as a core v1 user-facing concern.

## [v0.0.9] - 2026-03-11

### Added

- Added Track B starter template documents for user journeys, user flows, user story mapping, user-side acceptance criteria, and test taxonomy under `docs/spec/16_` through `docs/spec/20_`.

## [v0.0.8] - 2026-03-10

### Added

- Added `docs/spec/15_markdown_rendering_rules.md` to define the exact v1 markdown reading format, section order, and tool rendering style.

### Changed

- Updated `docs/spec/09_checkpoint_behavior.md` and `docs/spec/10_degraded_mode_behavior.md` to define fail-safe behavior explicitly as stopping, not guessing, not advancing the checkpoint, and informing the user directly.
- Updated `docs/spec/12_checkpoint_sidecar_schema.md` to lock the composite cursor model with `last_exported_record_index` as the primary resume marker.
- Updated `docs/spec/13_acceptance_criteria.md` and `docs/spec/14_test_scenarios.md` to reflect the approved Track A decisions.
- Updated `docs/spec/05_open_questions_and_next_steps.md` so the next spec focus moves to the missing product-spec pack after Track A.

## [v0.0.7] - 2026-03-10

### Added

- Added `docs/spec/12_checkpoint_sidecar_schema.md` to define the v1 JSON sidecar schema.
- Added `docs/spec/13_acceptance_criteria.md` to turn the current v1 decisions into acceptance criteria.
- Added `docs/spec/14_test_scenarios.md` to document the current v1 test scenarios, including Windows validation by Daniel and trusted users.

### Changed

- Updated `docs/spec/06_supported_environments.md` so Windows Codex CLI is a required v1 target while still distinguishing target support from validated support.
- Updated `docs/spec/07_export_data_contract.md` to lock the default export view close to what the user visibly experienced in chat.
- Updated `docs/spec/09_checkpoint_behavior.md` to point to the approved JSON sidecar schema.
- Updated `docs/spec/10_degraded_mode_behavior.md` to require failure and omission messages in the language of the active conversation.
- Updated `docs/spec/05_open_questions_and_next_steps.md` to remove the now-resolved questions and reflect the remaining design work.

## [v0.0.6] - 2026-03-10

### Changed

- Propagated the anti-refactor rule through the relevant spec documents so v1 design, later extensibility, and deferred post-v1 work all point to the same additive integration model.

## [v0.0.5] - 2026-03-10

### Added

- Added `docs/spec/06_supported_environments.md` to define the current-session meaning and the v1 environment targets.
- Added `docs/spec/07_export_data_contract.md` to define the supported v1 export contract, including model name and excluded hidden reasoning.
- Added `docs/spec/08_artifact_structure_and_naming.md` to define the v1 artifact shape, filename rules, and export sequence behavior.
- Added `docs/spec/09_checkpoint_behavior.md` to define incremental export and sidecar checkpoint behavior.
- Added `docs/spec/10_degraded_mode_behavior.md` to define natural-language failure and partial-availability behavior.
- Added `docs/spec/11_post_v1_deferrals.md` to document deferred features, the reason for deferral, the consequence, and the anti-refactor integration rule.

### Changed

- Updated `docs/spec/05_open_questions_and_next_steps.md` to remove decisions that are now resolved and focus on the remaining open design work.

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
