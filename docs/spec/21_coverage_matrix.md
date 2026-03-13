# Coverage Matrix

## Purpose

This document provides traceability across the v1 specification.

It exists to make these relationships explicit:

- user story to user-side acceptance criteria
- acceptance criteria to test scenarios
- test scenarios to test layers
- v1 scope to platform coverage expectations

## How To Use This Document

- Use this matrix to check whether every important v1 user promise has acceptance coverage.
- Use this matrix to check whether every important acceptance criterion has test coverage.
- Use this matrix to identify which verification is expected to be automated versus manual.
- Use this matrix together with `22_platform_validation.md` when validating target environments.

## Test Layer Key

- `unit`: isolated logic validation
- `integration`: subsystem behavior against realistic local inputs
- `full-flow`: end-to-end or realistic invocation flow validation
- `manual`: real-user or real-environment validation

## V1 Coverage Matrix

| Story ID | Story Summary | Acceptance IDs | Test IDs | Test Layers | Platform Scope | Notes |
|---|---|---|---|---|---|---|
| US-01 | Invoke `$export` in the current session and preserve the chat history in markdown. | AC-01, AC-02, AC-08, AC-12 | T-01, T-08, T-09 | integration, full-flow | all primary v1 targets | covers current-session targeting, markdown artifact, file-location reporting, and default destination |
| US-02 | Include the meaningful workflow trail, not just the final answer. | AC-03 | T-05, T-06, T-07 | unit, integration, full-flow | all primary v1 targets | rendering-focused story |
| US-03 | Keep the export readable and well-structured. | AC-02, AC-03, AC-08 | T-05, T-06, T-07 | unit, integration, full-flow | all primary v1 targets | overlaps intentionally with rendering and file-location communication |
| US-04 | Repeated exports continue from the last export point without noisy duplication. | AC-04, AC-07, AC-09, AC-10 | T-03, T-14, T-15, T-16, T-31 | integration, full-flow | all primary v1 targets | covers incremental behavior, no-new-content behavior, and sequencing clarity |
| US-05 | It is clear whether an export is the first export or an incremental export. | AC-08, AC-10 | T-09, T-16 | full-flow | all primary v1 targets | user-facing communication story |
| US-06 | Export filenames stay clearly sequenced across repeated exports. | AC-07 | T-31 | unit, integration, full-flow | all primary v1 targets | naming and sequencing story |
| US-07 | The skill works consistently across the supported operating systems for Codex. | AC-13 | T-23, T-24, T-25, T-26, T-27, T-28, T-29, T-30 | full-flow, manual | macOS CLI, Linux CLI, macOS app, Windows CLI, Windows app | requires real-environment validation evidence |
| US-08 | In a restricted environment, the skill explains clearly what it can and cannot access. | AC-05, AC-06, AC-11, AC-14 | T-17, T-19, T-20, T-21, T-22 | integration, full-flow, manual | all primary v1 targets | degraded-mode and restricted-environment transparency story |

## Coverage Review Rules

- Every v1 story must map to at least one acceptance criterion.
- Every acceptance criterion must map to at least one test scenario.
- Every user-facing communication promise should have at least one full-flow test.
- Every cross-platform promise should have platform-specific validation evidence.
- Manual validation should not replace unit, integration, or full-flow coverage where those are practical.

## Current Gaps To Watch

- The matrix identifies traceability, not implementation completeness.
- Platform validation still depends on actual evidence being recorded in `22_platform_validation.md`.
- Automation-versus-manual decisions may still need to be refined once the implementation stack is chosen.
