# Open Questions And Next Steps

## Status

- Phase: validated v1 baseline
- Date: March 27, 2026

## Key Open Questions

- No blocking v1 Windows validation questions remain after the March 27, 2026 close-out.
- How much additional installer metadata do we want beyond Daniel's retrospective March 22, 2026 install confirmations on macOS, Linux, and Windows devices?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, Linux CLI, Windows CLI, and Windows app runtime evidence as validated.
3. Treat the March 27, 2026 Windows close-out as implemented repo state, not as an open design question.
4. Keep the maintained macOS-local baseline green and rerun Linux or Windows quality gates when future code changes touch shared exporter behavior.
5. Update validation docs only with directly observed runtime evidence.
6. Preserve the March 22, 2026 retrospective `skill-installer` confirmations in the platform validation notes and add richer installer metadata later only if it materially helps future release or support work.

## Current Repo State

- The shared test harness now renders rollout JSONL fixtures structurally, including nested JSON strings such as tool arguments and tool outputs.
- The shared unit-test baseline now uses host-independent UTC construction, so Windows test runs do not depend on named timezone data for UTC cases.
- Markdown expectation templates now re-encode fenced JSON blocks structurally, so Windows path escaping matches the renderer output instead of depending on raw string substitution.
- Named-timezone success-path behavior remains covered in the targeted renderer tests rather than in the shared fixture baseline.
- On March 27, 2026, a fresh Windows `.venv` rerun passed `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .`.
- On March 27, 2026, controlled Windows CLI and Windows app close-out replays were recorded from isolated temporary Codex homes derived from copied real thread rows and copied rollout artifacts, closing the remaining Windows checklist items without mutating live Codex state.

## Acceptance Criteria

- A fresh Windows virtual environment now passes `python -m pip install -e ".[dev]"`, `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .` without ad hoc fixes.
- The fixture-rendering regression test proves that a Windows-style path yields valid JSONL and JSON-valid fenced markdown for tool arguments.
- The maintained macOS-local baseline remains green for `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- Linux and Windows each now have at least one fresh rerun of the automated gates recorded after the shared harness cleanup.
- Windows platform-validation docs are now updated from real runtime evidence rather than from assumptions.

## Implementation Order

1. Reconfirm the maintained macOS-local baseline if a future follow-up change lands.
2. Record only the runtime evidence that is directly re-observed in `22_platform_validation.md` and the per-platform validation records.
3. Keep future Windows validation additive rather than redefining the meaning of the v1 checklist.
