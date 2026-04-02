# Changelog

All notable changes to this repository will be documented in this file.

The format is based on Keep a Changelog, and this project intends to follow Semantic Versioning once versioned releases exist.

## [Unreleased]

## [v1.1.3] - 2026-04-02

### Added

- Added `skills/export/codexporter/json_utils.py` to contain the stdlib `json.loads(...)` `Any` escape hatch in one narrow helper with explicit JSON value aliases, so production modules can validate decoded shapes immediately instead of propagating dynamic values.

### Changed

- Updated `skills/export/codexporter/session_store.py` to replace raw `sqlite3.Row` propagation with a typed thread-row boundary, reducing dynamic SQLite values to one coercion point before the exporter builds `ThreadRecord`.
- Updated `skills/export/codexporter/cli.py`, `skills/export/codexporter/renderer.py`, `skills/export/codexporter/rollout_parser.py`, `skills/export/codexporter/compaction.py`, and `skills/export/codexporter/checkpoint.py` so Stage 2 of the approved no-`Any` rollout now lands in production code by narrowing `argparse` inputs and JSON checkpoint or rollout payloads at the module boundary instead of letting implicit `Any` flow deeper into the package.
- Updated `pyproject.toml`, `README.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/23_engineering_policy.md`, and `docs/spec/28_no_any_rollout.md` so the repository now states truthfully that production `codexporter` modules are checked with `disallow_any_expr = true` while the test-suite-wide expression stage still remains pending.

## [v1.1.2] - 2026-04-02

### Changed

- Updated `pyproject.toml` so the binding `mypy` configuration now enforces Stage 1 of the approved no-`Any` rollout by enabling `disallow_any_explicit` and `disallow_any_unimported` without changing the contributor command surface.
- Updated `README.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/23_engineering_policy.md`, and `docs/spec/28_no_any_rollout.md` so the repository now states truthfully that Stage 1 of the no-`Any` rollout is active while the later `disallow_any_expr` stages remain pending.

## [v1.1.1] - 2026-04-02

### Added

- Added `docs/spec/28_no_any_rollout.md` to record the approved staged no-`Any` hardening plan, including the current implicit-`Any` audit result, the rollout order for `mypy` `--disallow-any-*` enforcement, and the policy for using a Fedora Linux guest on Daniel's Mac as supplemental Linux CLI validation evidence once directly observed.

### Changed

- Updated `docs/spec/23_engineering_policy.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/22_platform_validation.md`, and `README.md` so the repository now distinguishes clearly between the current enforced `mypy strict` baseline and the newly approved staged no-`Any` rollout instead of implying that `strict` already bans all `Any`.

## [v1.1.0] - 2026-04-01

### Added

- Added the first implemented compact export profile on the existing `export` skill surface, so `$export --compact` now writes the same canonical markdown artifact type with deterministic omission markers for bulky raw tool payloads instead of introducing a second export identity.
- Added 4 new automated tests covering compact CLI invocation, deterministic compaction of file-read outputs, raw patch payloads, large diffs, oversized file listings, short-diff preservation, and shared checkpoint behavior between compact and full renders.
- Added `codexporter-session-discovery-fix-proposal-2026-03-28.md` to capture the March 28, 2026 investigation and the recommended fix for current-session discovery when live rollout files exist but `state_5.sqlite` session indexing is stale or missing.
- Added first-class compact-mode traceability across user stories, journeys, flows, acceptance criteria, test scenarios, and the coverage matrix so `$export --compact` is no longer documented only in the dedicated compact spec and README layers.
- Added a new automated compact-mode regression test for deterministic suppression of oversized machine-shaped JSON output.

### Changed

- Updated `skills/export/codexporter/cli.py`, `skills/export/codexporter/service.py`, `skills/export/codexporter/renderer.py`, `skills/export/codexporter/models.py`, `skills/export/codexporter/messages.py`, and the new `skills/export/codexporter/compaction.py` so the exporter now supports explicit `full` versus `compact` render profiles while keeping export numbering and checkpoint semantics canonical.
- Updated `skills/export/codexporter/rollout_parser.py` so tool-call and tool-output entries keep their call identifiers, allowing deterministic compaction decisions to match outputs back to the originating tool call.
- Updated `README.md`, `skills/export/SKILL.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/07_export_data_contract.md`, `docs/spec/11_post_v1_deferrals.md`, `docs/spec/15_markdown_rendering_rules.md`, `docs/spec/21_coverage_matrix.md`, `docs/spec/25_export_length_analysis.md`, `docs/spec/26_compact_mode_readiness.md`, and `docs/spec/27_compact_mode_definition.md` so the documentation reflects the implemented compact-mode surface instead of treating it as still pending.
- Updated `docs/spec/02_user_stories.md`, `docs/spec/13_acceptance_criteria.md`, `docs/spec/14_test_scenarios.md`, `docs/spec/16_user_journeys.md`, `docs/spec/17_user_flows.md`, `docs/spec/18_user_story_mapping.md`, `docs/spec/19_user_side_acceptance_criteria.md`, `docs/spec/21_coverage_matrix.md`, `docs/spec/22_platform_validation.md`, `docs/spec/05_open_questions_and_next_steps.md`, `README.md`, and the per-platform validation records so compact mode is now assimilated into the canonical product, QA, and validation stack instead of sitting partly outside it.
- Updated `AGENTS.md` and `docs/spec/23_engineering_policy.md` so advancing the repository release version now explicitly requires synchronized updates across the versioned `CHANGELOG.md` entry, `[project].version` in `pyproject.toml`, and the matching GitHub tag `vX.Y.Z`.
- Updated `skills/export/codexporter/__init__.py` so the internal package version string no longer lags the already-recorded `1.0.0` package baseline in `pyproject.toml`.

### Removed

- Removed `codexporter-windows-test-suite-bug-report-2026-03-19.md` and `codexporter-windows-test-suite-fix-proposal-2026-03-19.md` because those Windows test-suite investigation documents are no longer needed in the current repository state.

## [v1.0.0] - 2026-03-27

### Added

- Added 7 new automated tests covering CLI-level German no-new-content messaging, CLI-level German checkpoint-failure messaging, CLI fail-closed behavior under same-workspace ambiguity, CLI preference for runtime thread identifiers over same-workspace heuristics, Windows-path-safe fixture rendering, explicit hidden-reasoning/internal-instruction exclusion assertions, and export success when optional rollout metadata is absent.
- Added an explicit degraded-mode regression test that preserves English fallback for pre-rollout access failures even when the thread would otherwise have been German, so the narrowed v1 language rule is pinned in the automated suite.
- Added a repository-wide `.github/CODEOWNERS` file that makes `@DanielMulec` the sole code owner for all paths, so GitHub can enforce code-owner review on protected merges.

### Changed

- Closed the remaining Windows v1 gaps: a fresh Windows `.venv` now passes `pytest`, `mypy`, `ruff check`, and `ruff format --check`; controlled Windows CLI and Windows app close-out replays now record German checkpoint-failure messaging, explicit persisted-session-history failures under denied read access, same-workspace ambiguity fail-closed behavior, targeted current-thread recovery, and Windows CLI sequencing/no-new-content evidence.
- Updated the shared test harness so UTC-only unit tests are host-independent across Windows, Linux, and macOS, and markdown expectation templates now re-encode fenced JSON blocks structurally so Windows path escaping matches the renderer output.
- Updated `.gitignore` to ignore `pytest-cache-files-*` temp directories so repo-root `ruff` traversals stay focused on real project files on Windows too.
- Updated `pyproject.toml` so the package version now records the validated v1 release as `1.0.0`.
- Updated `docs/validation/linux_cli.md`, `docs/spec/22_platform_validation.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/21_coverage_matrix.md`, and `README.md` to record the March 27, 2026 Linux-host controlled close-out evidence that forced the previously missing Linux CLI failure-path and same-workspace ambiguity cases, closing the Linux CLI platform checklist as validated.
- Updated `README.md` and `docs/spec/21_coverage_matrix.md` so the repository status now records the fresh March 27, 2026 Linux `.venv` rerun where `pytest`, `mypy`, `ruff check`, and `ruff format --check` all passed.
- Updated `docs/validation/macos_cli.md`, `docs/validation/macos_app.md`, `docs/spec/22_platform_validation.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/21_coverage_matrix.md`, and `README.md` to record the March 27, 2026 macOS-host controlled close-out evidence that forced the previously rare macOS failure-path and same-workspace ambiguity cases, closing the macOS CLI and macOS app platform checklists as validated.
- Added `docs/spec/27_compact_mode_definition.md` to define the first approved compact-mode contract: same `export` skill, explicit `--compact` invocation, deterministic non-AI compaction, always-compacted raw patch bodies, compacted full file reads, and threshold-based raw diff retention with file-level summaries for larger diffs.
- Updated `docs/spec/11_post_v1_deferrals.md`, `docs/spec/25_export_length_analysis.md`, and `docs/spec/26_compact_mode_readiness.md` so compact mode is no longer described as entirely undefined; the docs now point to the approved initial compact-mode contract while still treating implementation as pending.
- Updated `README.md` so the automated validation snapshot now reflects the actual current macOS-local baseline of 31 passing `pytest` cases and names the added hidden-reasoning/internal-instruction exclusion coverage.
- Updated `docs/spec/06_supported_environments.md` with a March 27, 2026 official-source refresh that records the current upstream documentation inconsistency around native Windows CLI support while aligning the repo-facing status with this repository's now-validated Windows evidence.
- Updated `docs/spec/15_markdown_rendering_rules.md` so the v1 rendering spec now matches the implementation: there is no separate `## Git Context` section, and visible git-related content stays in the chronological conversation stream.
- Updated `AGENTS.md` so unverified work must always be treated as absent until the repository proves otherwise, and branch audits are required when branch history may affect that judgment.
- Updated `AGENTS.md` so every Git commit must carry traceability footers and every pull request must repeat the same links and state whether older branches were merged, superseded, or selectively salvaged.
- Logged a local-only internal investigation event in repository history without publishing the underlying working notes.
- Expanded `docs/spec/05_open_questions_and_next_steps.md` so the agreed Windows follow-up is now documented as an explicit shared test-harness cleanup plan with concrete change scope, timezone stance, acceptance criteria, and validation order, and linked that plan from `README.md`.
- Updated `docs/spec/22_platform_validation.md`, `docs/validation/windows_app.md`, `docs/validation/windows_cli.md`, and `README.md` to record the March 20, 2026 Windows validation evidence that confirmed the current happy path in both Windows Codex Desktop app and Windows Codex CLI, while keeping the Windows surfaces partial because failure-path and deeper edge-case coverage still remain open.
- Refactored the shared test fixture harness so rollout JSONL fixtures are rendered structurally and keep nested JSON payloads valid for Windows-style paths, and removed the baseline named-timezone dependency from shared fixtures by standardizing them on UTC while keeping named-zone rendering covered in targeted renderer tests.
- Updated `README.md`, `docs/spec/05_open_questions_and_next_steps.md`, and `docs/spec/21_coverage_matrix.md` to replace the stale “known Windows fixture/timezone harness bug still exists” wording with the current state: the harness cleanup is in the repo, the macOS-local automated baseline is now 30 tests, and a fresh Windows rerun is still required before the Windows validation status can change.
- Narrowed the v1 language-sensitivity spec so pre-rollout access failures may fall back to English when the exporter has no authoritative way to determine the active thread language yet, and aligned the degraded-mode test suite with that rule.
- Updated the validation docs to record Daniel's retrospective March 22, 2026 `skill-installer` confirmations on macOS, Linux, and Windows devices, and clarified that the new macOS-host automated coverage is supplemental evidence rather than a substitute for direct macOS CLI or app runtime validation.

## [v0.2.12] - 2026-03-19

### Added

- Added the dated Windows repo-quality bug report and fix-proposal notes at the repository root: `codexporter-windows-test-suite-bug-report-2026-03-19.md` and `codexporter-windows-test-suite-fix-proposal-2026-03-19.md`.

### Changed

- Updated `README.md`, `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/21_coverage_matrix.md`, and `docs/spec/23_engineering_policy.md` so the documentation now reflects the pulled Windows app validation evidence, the current 23-test automated macOS-local baseline, and the remaining shared cross-platform test-harness gap that still keeps fresh-Windows `pytest` from being green.

## [v0.2.11] - 2026-03-18

### Changed

- Updated the affected spec documents so their status blocks no longer claim the repository is still in the analysis-and-discussion phase, and clarified the remaining support-target wording in `docs/spec/06_supported_environments.md`.

## [v0.2.10] - 2026-03-18

### Added

- Added 5 new `pytest` cases covering thread-ID-first session targeting, fail-closed same-workspace ambiguity, workspace-mismatch protection, Windows-style path-spelling equivalence during targeted lookup, and UTC fallback when named timezone data is unavailable.

### Changed

- Updated the exporter runtime to prefer the invoking Codex thread identifier when available, stop rather than guess when more than one session matches the same workspace, and reject explicit session targets that point at a different project root.
- Updated the renderer to fall back to UTC formatting without requiring external timezone data, and updated the Windows launcher guidance in `SKILL.md` and `README.md` to prefer `py -3` for non-venv invocation.

## [v0.2.9] - 2026-03-18

### Added

- Added `docs/validation/macos_cli.md` and `docs/validation/linux_cli.md` as concise manual validation records for the now-confirmed macOS Codex CLI and Linux Codex CLI happy-path runs.

### Changed

- Updated `docs/spec/22_platform_validation.md` to record partial validation status for macOS Codex CLI and Linux Codex CLI, including the observed pass results and the still-unrun degraded-mode checks.
- Updated `README.md`, `docs/spec/05_open_questions_and_next_steps.md`, and `docs/spec/21_coverage_matrix.md` so the repository status no longer claims that macOS CLI and Linux CLI evidence is missing.

## [v0.2.8] - 2026-03-16

### Changed

- Updated `.gitignore` to ignore a neutral `.local/` workspace folder for local-only artifacts that must stay off GitHub.
- Updated `docs/spec/23_engineering_policy.md` with a concise binding rule for when to use `.gitignore`, `.git/info/exclude`, and the global Git excludes file, plus the reminder that ignore rules do not untrack files already in Git.
- Updated the spec baseline to make current-session targeting fail-safe, treat same-workspace wrong-session export as a cross-platform validation concern, and require UTC fallback when named timezone data is unavailable.

## [v0.2.7] - 2026-03-16

### Changed

- Updated `README.md` so local development instructions are platform-neutral for contributors, with separate macOS/Linux and Windows virtual-environment setup paths and `python -m ...` command patterns instead of POSIX-only `.venv/bin/...` examples.

## [v0.2.6] - 2026-03-15

### Added

- Added a root `README.md` that documents the current `export` skill boundary, the `$export` invocation, local development commands, repository layout, and the current automated and manual validation status.

## [v0.2.5] - 2026-03-14

### Added

- Added 13 new `pytest` cases covering isolated unit behavior, public invocation flow through `cli.main(...)` and the skill script entrypoint, localized degraded-mode behavior, multi-project script reuse, unreadable or incomplete sidecars, raw sidecar schema assertions, and failed-write checkpoint preservation.

### Changed

- Extended `tests/conftest.py` with reusable fixture-building and rollout-replacement helpers so multiple project contexts and localized rollout variants can be exercised hermetically.
- Updated `docs/spec/21_coverage_matrix.md` and `docs/spec/05_open_questions_and_next_steps.md` so they reflect the new automated baseline and shift the remaining QA focus toward manual platform validation and the narrower remaining edge cases.

## [v0.2.4] - 2026-03-14

### Changed

- Updated `docs/validation/macos_app.md`, `docs/spec/22_platform_validation.md`, `docs/spec/21_coverage_matrix.md`, and `docs/spec/05_open_questions_and_next_steps.md` to record the March 14 macOS app evidence for the renamed globally installed `$export` skill boundary, to note that active-project output was observed from the installed skill path, and to clarify the still-open automated and manual validation gaps.

## [v0.2.3] - 2026-03-14

### Changed

- Renamed the installable skill boundary from `skills/codexporter/` to `skills/export/` and changed the skill frontmatter name from `codexporter` to `export` so the registered invocation token matches the required `$export` command.
- Updated the approved install-boundary references in `pyproject.toml`, engineering/spec docs, validation evidence, and packaged source metadata to reflect the renamed `skills/export/` install surface while keeping the internal Python package name `codexporter`.

## [v0.2.2] - 2026-03-13

### Added

- Added `docs/spec/26_compact_mode_readiness.md` to assess how close the current implementation is to supporting compact export modes as an additive post-v1 feature.

### Changed

- Updated `docs/spec/11_post_v1_deferrals.md` and `docs/spec/25_export_length_analysis.md` to reference the new compact-mode implementation-readiness assessment alongside the export-length evidence.

## [v0.2.1] - 2026-03-13

### Added

- Added `docs/spec/25_export_length_analysis.md` to record why a real first export became extremely large and to preserve that evidence for later compact-mode design.

### Changed

- Updated `docs/spec/11_post_v1_deferrals.md` to add compact export modes as an explicit post-v1 deferral and to reference the new export-length analysis report as evidence.

## [v0.2.0] - 2026-03-13

### Added

- Added the installable `skills/codexporter/` skill runtime, including `SKILL.md`, a Python entry script, and modular exporter code for session discovery, rollout parsing, markdown rendering, artifact writing, and checkpoint sidecars.
- Added `pyproject.toml` and `.gitignore` for the approved Python toolchain and local development exclusions.
- Added sanitized macOS-derived rollout fixtures and `pytest` coverage for first export, incremental export, no-new-content behavior, prior-artifact immutability, and checkpoint corruption or mismatch handling.
- Added `docs/validation/macos_app.md` with the first real macOS Codex app validation record.

### Changed

- Updated `docs/spec/22_platform_validation.md` to add shared validation result vocabulary, runtime-environment evidence fields, and the first partial macOS Codex app validation status.

## [v0.1.12] - 2026-03-13

### Added

- Added `docs/spec/24_installation_and_distribution.md` to define the global-install model, the installable repo boundary at `skills/codexporter/`, and the rule that install location must never determine export destination.

### Changed

- Updated `docs/spec/01_product_triage.md`, `docs/spec/02_user_stories.md`, `docs/spec/03_product_definition.md`, `docs/spec/13_acceptance_criteria.md`, `docs/spec/19_user_side_acceptance_criteria.md`, `docs/spec/16_user_journeys.md`, `docs/spec/17_user_flows.md`, `docs/spec/18_user_story_mapping.md`, and `docs/spec/21_coverage_matrix.md` to make global install and per-project export destination an explicit v1 product promise with traceability.
- Updated `docs/spec/05_open_questions_and_next_steps.md`, `docs/spec/08_artifact_structure_and_naming.md`, and `docs/spec/23_engineering_policy.md` to align the next steps, export-location contract, and engineering policy with the approved global install boundary.

## [v0.1.11] - 2026-03-13

### Changed

- Updated `docs/spec/23_engineering_policy.md` to remove stale web-stack, frontend, and backend framing so the engineering policy now describes the project in Codex-skill terms only.

## [v0.1.10] - 2026-03-13

### Changed

- Updated `docs/spec/23_engineering_policy.md` to approve the initial Python stack, binding quality gates, fixture strategy, modular file-size rule, and later Trivy CI posture for the repository.
- Updated `AGENTS.md` so project-specific implementation standards must be read from `docs/spec/23_engineering_policy.md`, and moved the 400-line source-file rule out of `AGENTS.md`.
- Updated `docs/spec/05_open_questions_and_next_steps.md` to reflect that the initial stack decision is now made and that the next work is macOS-first fixture definition, implementation, and validation.

## [v0.1.9] - 2026-03-13

### Changed

- Updated `docs/spec/05_open_questions_and_next_steps.md` to reflect the accepted QA baseline, platform validation model, and pre-stack engineering policy, and to shift the plan toward stack selection, macOS-first implementation, and later Windows follow-up.

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
