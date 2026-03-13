# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 13, 2026

## Key Open Questions

- What fixture strategy should be used for persisted session samples before implementation begins?
- How should validation evidence be recorded so macOS-first testing is auditable before Windows follow-up begins?
- Which packaging and distribution decision should follow once the macOS implementation path is proven?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, and `23_engineering_policy.md` as the working project-specific engineering policy.
2. Define the first macOS fixture set from real persisted-session structures and map each fixture to the relevant v1 test scenarios.
3. Implement a macOS-first vertical slice that proves session discovery, event extraction, markdown rendering, artifact writing, and checkpoint behavior end to end.
4. Configure the approved local quality gates from `23_engineering_policy.md`: `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
5. Record real validation evidence for macOS Codex CLI first, then macOS Codex app, using the platform checklist and linked evidence artifacts.
6. After the macOS path is stable, follow with Windows validation and any Windows-specific implementation adjustments that are still required.
