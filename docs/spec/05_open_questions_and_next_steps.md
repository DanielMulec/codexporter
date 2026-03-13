# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 13, 2026

## Key Open Questions

- Which initial implementation stack decisions should be approved first and recorded in `23_engineering_policy.md`?
- What fixture strategy should be used for persisted session samples before implementation begins?
- How should validation evidence be recorded so macOS-first testing is auditable before Windows follow-up begins?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, and `23_engineering_policy.md` as the working pre-stack engineering policy.
2. Approve the initial stack decisions in `23_engineering_policy.md` in this order:
   - runtime and language
   - test harness for unit, integration, and full-flow coverage
   - fixture strategy for persisted session samples
   - evidence storage format for platform validation
3. Define the first macOS fixture set from real persisted-session structures and map each fixture to the relevant v1 test scenarios.
4. Implement a macOS-first vertical slice that proves session discovery, event extraction, markdown rendering, artifact writing, and checkpoint behavior end to end.
5. Record real validation evidence for macOS Codex CLI first, then macOS Codex app, using the platform checklist and linked evidence artifacts.
6. After the macOS path is stable, follow with Windows validation and any Windows-specific implementation adjustments that are still required.
