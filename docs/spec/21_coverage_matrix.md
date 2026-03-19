# Coverage Matrix

## Purpose

This document provides traceability across the v1 specification.

It exists in two layers:

- story-level traceability for user-visible v1 behavior
- requirement-level traceability for the broader v1 contract

## How To Use This Document

- Use this matrix to check whether every important v1 user promise has acceptance coverage.
- Use this matrix to check whether every important acceptance criterion has test coverage.
- Use the requirement-level table to check coverage for v1 contract rules that are broader than user-side acceptance criteria alone.
- Use this matrix to identify which verification is expected to be automated versus manual.
- Use this matrix together with `22_platform_validation.md` when validating target environments.

## Test Layer Key

- `unit`: isolated logic validation
- `integration`: subsystem behavior against realistic local inputs
- `full-flow`: end-to-end or realistic invocation flow validation
- `manual`: real-user or real-environment validation

## Story-Level Coverage Matrix

| Story ID | Story Summary | Acceptance IDs | Test IDs | Test Layers | Platform Scope | Notes |
|---|---|---|---|---|---|---|
| US-01 | Invoke `$export` in the current session and preserve the chat history in markdown. | AC-01, AC-02, AC-08, AC-12 | T-01, T-08, T-09, T-40, T-41, T-42 | integration, full-flow | all primary v1 targets | covers current-session targeting, markdown artifact, file-location reporting, default destination, and no-guess session selection |
| US-02 | Include the meaningful workflow trail, not just the final answer. | AC-03 | T-05, T-06, T-07 | unit, integration, full-flow | all primary v1 targets | rendering-focused story |
| US-03 | Keep the export readable and well-structured. | AC-02, AC-03, AC-08 | T-05, T-06, T-07 | unit, integration, full-flow | all primary v1 targets | overlaps intentionally with rendering and file-location communication |
| US-04 | Repeated exports continue from the last export point without noisy duplication. | AC-04, AC-07, AC-09, AC-10 | T-03, T-14, T-15, T-16, T-31, T-35 | integration, full-flow | all primary v1 targets | covers incremental behavior, no-new-content behavior, sequencing clarity, and prior-artifact immutability |
| US-05 | It is clear whether an export is the first export or an incremental export. | AC-08, AC-10 | T-09, T-16 | full-flow | all primary v1 targets | user-facing communication story |
| US-06 | Export filenames stay clearly sequenced across repeated exports. | AC-07 | T-31 | unit, integration, full-flow | all primary v1 targets | naming and sequencing story |
| US-07 | The skill works consistently across the supported operating systems for Codex. | AC-13 | T-23, T-24, T-25, T-26, T-27, T-28, T-29, T-30 | full-flow, manual | macOS CLI, Linux CLI, macOS app, Windows CLI, Windows app | requires per-platform checklist evidence and real-environment validation |
| US-08 | In a restricted environment, the skill explains clearly what it can and cannot access. | AC-05, AC-06, AC-11, AC-14 | T-17, T-19, T-20, T-21, T-22 | integration, full-flow, manual | all primary v1 targets | degraded-mode and restricted-environment transparency story |
| US-09 | The skill installs once globally and can then be used across project contexts. | AC-15 | T-37, T-38, T-39 | integration, full-flow | all primary v1 targets | covers global install model, per-project export destination, and fail-fast handling when project root cannot be determined |

## Requirement-Level Coverage Matrix

| Requirement ID | Source | Requirement Summary | Test IDs | Test Layers | Automation Expectation | Platform Scope | Notes |
|---|---|---|---|---|---|---|---|
| REQ-01 | `13_acceptance_criteria.md`, `19_user_side_acceptance_criteria.md` | Export the current live session into a markdown artifact and do not substitute a different same-workspace session. | T-01, T-09, T-40, T-41, T-42 | integration, full-flow | automated preferred plus manual platform confirmation | all primary v1 targets | base export behavior plus current-thread targeting safety |
| REQ-02 | `07_export_data_contract.md`, `15_markdown_rendering_rules.md`, `19_user_side_acceptance_criteria.md` | Render a visible-chat-first export with readable chronology, model-labeled assistant headings, and tool rendering. | T-05, T-06, T-07 | unit, integration, full-flow | automated preferred | all primary v1 targets | user-visible rendering contract |
| REQ-03 | `07_export_data_contract.md`, `13_acceptance_criteria.md` | Include the compact session metadata header with required fields when available. | T-32 | integration, full-flow | automated preferred | all primary v1 targets | covers model name and other required metadata when available |
| REQ-04 | `07_export_data_contract.md`, `13_acceptance_criteria.md` | Exclude hidden reasoning, encrypted reasoning payloads, and raw internal instruction payloads from v1 export output. | T-33 | integration, full-flow | automated preferred | all primary v1 targets | exclusion contract |
| REQ-05 | `08_artifact_structure_and_naming.md`, `13_acceptance_criteria.md` | Create one primary markdown artifact per successful export and write it into `codex_exports` under the current project root. | T-01, T-08 | integration, full-flow | automated preferred plus manual platform confirmation | all primary v1 targets | export location wording intentionally uses project root, not repository |
| REQ-06 | `08_artifact_structure_and_naming.md`, `13_acceptance_criteria.md` | Sanitize session-name-based filenames and keep repeated-export numbering clear. | T-04, T-31 | unit, integration, full-flow | automated preferred | all primary v1 targets | naming and sequencing contract |
| REQ-07 | `09_checkpoint_behavior.md`, `13_acceptance_criteria.md`, `19_user_side_acceptance_criteria.md` | First export is full so far; later exports are incremental; no-new-content creates no new export file and informs the user directly. | T-03, T-15, T-16, T-35 | integration, full-flow | automated preferred | all primary v1 targets | incremental export behavior, including prior-artifact immutability |
| REQ-08 | `09_checkpoint_behavior.md`, `12_checkpoint_sidecar_schema.md`, `13_acceptance_criteria.md` | Checkpoint state uses a JSON sidecar with the required v1 schema fields and composite cursor model. | T-13, T-34 | integration, full-flow | automated preferred | all primary v1 targets | sidecar format and cursor contract |
| REQ-09 | `09_checkpoint_behavior.md`, `10_degraded_mode_behavior.md`, `13_acceptance_criteria.md` | Failed exports, corrupted sidecar state, unreadable sidecar state, and cursor mismatch conditions do not advance the checkpoint and do not guess. | T-10, T-11, T-12, T-17, T-36 | integration, full-flow | automated preferred plus manual spot-check | all primary v1 targets | checkpoint safety and fail-safe behavior, including cursor-validation mismatch |
| REQ-10 | `07_export_data_contract.md`, `10_degraded_mode_behavior.md`, `13_acceptance_criteria.md` | Missing optional metadata, unavailable timezone data for display formatting, or non-git context does not block a successful core export. | T-02, T-18, T-43 | integration, full-flow | automated preferred | all primary v1 targets | resolves the non-git seam and timezone-formatting seam explicitly |
| REQ-11 | `10_degraded_mode_behavior.md`, `13_acceptance_criteria.md`, `19_user_side_acceptance_criteria.md` | Failure and omission messaging explains what failed, why, and what to do next in the language of the active conversation. | T-17, T-19, T-20, T-21, T-22 | integration, full-flow, manual | automated where practical plus manual language/platform validation | all primary v1 targets | degraded-mode communication contract |
| REQ-12 | `06_supported_environments.md`, `13_acceptance_criteria.md`, `22_platform_validation.md` | Preserve the same core export behavior across the supported target environments, including current-thread targeting correctness, and collect validation evidence per platform. | T-23, T-24, T-25, T-26, T-27, T-28, T-29, T-30, T-40, T-41, T-42 | full-flow, manual | manual validation required, automation supplemental | macOS CLI, Linux CLI, macOS app, Windows CLI, Windows app | cross-platform support contract scoped to the checklist in `22_platform_validation.md` |
| REQ-13 | `08_artifact_structure_and_naming.md`, `13_acceptance_criteria.md`, `19_user_side_acceptance_criteria.md`, `24_installation_and_distribution.md` | The skill is installed once globally, reused across project contexts, and never uses the installed skill directory as the export destination; if the active project root cannot be determined, the skill fails clearly. | T-37, T-38, T-39 | integration, full-flow | automated preferred plus manual platform confirmation | all primary v1 targets | install-boundary and project-context contract |

## Design-Constraint Coverage

| Constraint ID | Source | Constraint Summary | Verification Method | Notes |
|---|---|---|---|---|
| DC-01 | `03_product_definition.md`, `11_post_v1_deferrals.md` | Deferred features must integrate additively without redefining the meaning of the session export, the primary artifact, or checkpoint behavior. | design and spec review, not runtime testing | this is a governance and architecture constraint rather than a runtime test target |

## Coverage Review Rules

- Every v1 story must map to at least one acceptance criterion.
- Every acceptance criterion must map to at least one test scenario.
- Every user-facing communication promise should have at least one full-flow test.
- Every cross-platform promise should have platform-specific validation evidence.
- Manual validation should not replace unit, integration, or full-flow coverage where those are practical.

## Current Gaps To Watch

- The matrix identifies traceability, not implementation completeness.
- As of March 19, 2026, the repo has automated coverage for thread-accurate session targeting across same-workspace ambiguity, platform-specific path-shape differences, and timezone-data fallback, but a fresh Windows `pytest` run is still not clean because the shared test harness is not yet fully cross-platform.
- The current Windows automated gap is specific and known: baseline test setup still assumes named timezone data in Windows environments, and the rollout fixture templating still injects raw Windows paths into JSON fixture content without backslash-safe serialization.
- macOS app, macOS CLI, and Linux CLI have direct manual happy-path evidence, but each remains partial until non-English failure or omission messaging, restricted-environment honesty, and current-thread targeting robustness beyond the happy path are validated.
- Windows app now has direct partial runtime evidence in `22_platform_validation.md`, but Windows CLI still lacks its own validation record, and fresh-Windows automated-suite portability remains an explicit gap.
- GitHub skill installation flow end to end and the remaining manual restricted-environment checks still need explicit validation beyond the current automated suite.
