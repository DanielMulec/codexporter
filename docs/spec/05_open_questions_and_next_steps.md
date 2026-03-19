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

## Agreed Implementation Direction

- Scope the next change as a shared test-infrastructure cleanup, not as a Windows runtime refactor.
- Keep runtime code unchanged unless the repaired test harness exposes a real runtime defect.
- Keep `skills/export/codexporter/session_store.py` unchanged unless repaired cross-platform tests reveal a real path-normalization defect.

## Concrete Change Scope

- In `tests/conftest.py`, split plain-text expected-markdown rendering from rollout-JSONL fixture rendering.
- Keep `tests/fixtures/session_alpha/rollout_initial.jsonl` and `tests/fixtures/session_alpha/rollout_incremental.jsonl` as JSONL fixtures, but render each line structurally by parsing JSON first, replacing placeholder text inside string values, then serializing back with `json.dumps(...)`.
- Keep `tests/fixtures/session_alpha/expected/initial_export.md` and `tests/fixtures/session_alpha/expected/incremental_export.md` on plain-text replacement only.
- In `tests/test_unit_contracts.py`, remove implicit named-zone dependence from UTC-only test data and prefer `datetime.UTC` where a named zone is not the behavior under test.
- Add one focused fixture-rendering regression test, likely in `tests/test_fixture_rendering.py`, that proves a Windows-style `C:\...` project root yields valid JSONL and the intended plain-text markdown output.

## Timezone Default

- Do not add `tzdata` as the first move.
- Prefer removing named-zone dependence from shared fixtures and UTC-only tests.
- Keep named-zone success-path behavior covered only in targeted renderer tests.
- If a positive named-zone success-path test still needs deterministic zone data, mock that dependency or add explicit test-local support rather than making the whole shared test harness depend on IANA zone data by default.

## Acceptance Criteria

- In a fresh Windows virtual environment, `python -m pip install -e ".[dev]"` followed by `python -m pytest` passes without ad hoc fixes.
- The fixture-rendering regression test proves that a Windows-style path yields valid JSONL.
- The maintained macOS-local baseline remains green for `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- Linux gets at least one rerun of the automated gates, because this is shared cross-platform test infrastructure.
- No runtime behavior change is introduced intentionally unless repaired tests reveal a real defect that must be fixed.
- Windows platform-validation docs are updated only with real runtime evidence, not merely because the shared automated suite becomes Windows-clean.

## Implementation Order

1. Refactor fixture rendering in `tests/conftest.py`.
2. Add the direct Windows-path fixture regression test.
3. Remove implicit named-zone dependence from shared tests.
4. Re-run macOS automated gates locally.
5. Re-run Windows gates in a fresh virtual environment.
6. Re-run Linux automated gates or collect equivalent Linux verification.
7. Update `CHANGELOG.md` and only the docs justified by the newly observed evidence.
