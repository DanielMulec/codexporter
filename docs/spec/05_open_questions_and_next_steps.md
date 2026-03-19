# Open Questions And Next Steps

## Status

- Phase: implementation and validation
- Date: March 19, 2026

## Key Open Questions

- What is the smallest shared test-harness change set that makes rollout fixtures JSON-safe for Windows paths without hiding the real persisted-session structure?
- Should the remaining Windows timezone portability gap be solved by removing baseline named-zone assumptions from shared tests, by adding explicit dev-only timezone data, or by a narrow combination of both?
- What is the leanest validation sequence for re-checking macOS, Linux, and Windows once the shared test harness is fresh-Windows-clean?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, Linux CLI, and Windows app runtime evidence, but do not treat the partial records as sufficient for full Windows support or for Windows CLI validation.
3. Treat the March 19, 2026 Windows repo-quality findings as a separate cross-platform test-harness problem, not as proof that the Windows runtime happy path regressed.
4. Preserve the current session-targeting and runtime-hardening behavior as the baseline and make the next engineering change set about shared test-harness portability:
   - keep expected markdown fixtures as plain-text templates
   - render rollout JSONL fixtures structurally so Windows path strings are serialized safely inside JSON
   - remove or explicitly satisfy named timezone-data assumptions in shared tests rather than letting them fail implicitly on Windows
5. Add one tight regression test that proves a Windows-style project root still produces valid JSONL rollout fixtures and the intended plain-text expected markdown.
6. Re-run macOS, Linux, and Windows automated gates after the shared fixture and timezone cleanup, then record only the runtime evidence that is actually re-observed in `22_platform_validation.md` and the per-platform validation records.
