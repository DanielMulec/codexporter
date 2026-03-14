# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 14, 2026

## Key Open Questions

- How should remaining macOS gap evidence be captured for non-English failure or omission behavior and restricted-environment honesty?
- What is the most efficient validation sequence for Linux and Windows once the current macOS path is considered stable enough?
- Should the next automated additions focus on optional-metadata omission behavior and GitHub installation flow, or should the priority stay on manual platform validation first?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app evidence for the renamed globally installed `$export` boundary and active-project output behavior, while keeping the remaining macOS gaps explicit rather than rounding them up to full validation.
3. Treat the current automated suite as the new baseline:
   - isolated unit tests for filename generation, session-name sanitization, renderer formatting, message-heading rendering, tool rendering, sidecar serialization, and language detection
   - public invocation tests that exercise `cli.main(...)` and the script entrypoint rather than only `export_current_session(...)`
   - degraded-mode and checkpoint edge-case tests for inaccessible session history, blocked-access guidance, language-sensitive omission or failure messaging, unsafe-project-root fail-fast behavior, unreadable checkpoint sidecars, raw sidecar-schema assertions, and failed-write checkpoint preservation
4. Record the remaining macOS validation evidence for non-English failure or omission messaging and restricted-environment honesty.
5. Validate macOS Codex CLI against the checklist and record the result in `22_platform_validation.md`.
6. After the current macOS path is stable enough, validate Linux and Windows and record the results in `22_platform_validation.md`.
