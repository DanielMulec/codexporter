# Open Questions And Next Steps

## Status

- Phase: analysis and discussion
- Date: March 18, 2026

## Key Open Questions

- What is the smallest implementation change set that makes current-session targeting thread-accurate and fail-closed on ambiguity across all target platforms?
- Should the session-targeting fix and Windows runtime hardening land in one patch set or two tightly sequenced patch sets?
- What is the most efficient validation sequence for re-checking macOS, Linux, and Windows once non-happy-path current-thread targeting scenarios are included?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, and Linux CLI happy-path evidence, but do not treat that evidence as sufficient for current-thread targeting correctness or same-workspace ambiguity resistance.
3. Treat the current automated suite as the baseline rather than the finish line:
   - isolated unit tests for filename generation, session-name sanitization, renderer formatting, message-heading rendering, tool rendering, sidecar serialization, and language detection
   - public invocation tests that exercise `cli.main(...)` and the script entrypoint rather than only `export_current_session(...)`
   - degraded-mode and checkpoint edge-case tests for inaccessible session history, blocked-access guidance, language-sensitive omission or failure messaging, unsafe-project-root fail-fast behavior, unreadable checkpoint sidecars, raw sidecar-schema assertions, and failed-write checkpoint preservation
4. Add automated coverage for thread-ID-first session selection, same-workspace ambiguity handling, platform-specific path-representation mismatches, explicit-thread-versus-workspace conflicts, and UTC fallback when named timezone data is unavailable.
5. Implement the spec-aligned session-targeting and runtime-hardening changes.
6. Re-run macOS, Linux, and Windows validation against the expanded checklist and record the results in `22_platform_validation.md`.
