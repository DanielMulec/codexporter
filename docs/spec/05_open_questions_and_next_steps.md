# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 14, 2026

## Key Open Questions

- Which missing automated suites should be implemented next so the documented unit, integration, and full-flow layers are no longer aspirational?
- How should remaining macOS gap evidence be captured for non-English failure or omission behavior and restricted-environment honesty?
- What is the most efficient validation sequence for Linux and Windows once the current macOS path is considered stable enough?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app evidence for the renamed globally installed `$export` boundary and active-project output behavior, while keeping the remaining macOS gaps explicit rather than rounding them up to full validation.
3. Add the missing automated test suites that the current docs already call for:
   - isolated unit tests for filename generation, session-name sanitization, renderer formatting, message-heading rendering, tool rendering, sidecar serialization, and language detection
   - full-flow automated tests that exercise the public invocation boundary rather than only `export_current_session(...)`
4. Add the missing degraded-mode and checkpoint edge-case tests:
   - inaccessible session history
   - language-sensitive failure and omission messaging
   - blocked-access recovery guidance
   - restricted-environment honesty
   - unsafe-project-root fail-fast behavior
   - unreadable checkpoint sidecar
   - raw sidecar-schema assertions
5. Record the remaining macOS validation evidence for non-English failure or omission messaging and restricted-environment honesty.
6. After the current macOS path is stable enough, validate Linux and Windows and record the results in `22_platform_validation.md`.
