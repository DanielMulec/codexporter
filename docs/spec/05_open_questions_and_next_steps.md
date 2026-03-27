# Open Questions And Next Steps

## Status

- Phase: implementation and validation
- Date: March 27, 2026

## Key Open Questions

- Does a fresh Windows virtual environment now run `python -m pytest` cleanly with the shared fixture and timezone harness fixes that are already in the repo?
- What is the leanest validation sequence for re-checking the remaining Windows surfaces now that the macOS and Linux CLI checklists are closed and the known shared test-harness defects are covered by regression tests?
- How much additional installer metadata do we want beyond Daniel's retrospective March 22, 2026 install confirmations on macOS, Linux, and Windows devices?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, and Linux CLI runtime evidence as validated, and continue to treat both Windows surfaces as partial until their remaining manual checklist items are actually re-observed.
3. Treat the March 22, 2026 fixture-rendering and timezone cleanup as implemented repo state, not as an open design question.
4. Make the next QA pass about verification and evidence collection rather than more speculative harness work:
  - re-run the full automated gates in a fresh Windows virtual environment
  - preserve the March 27 Linux rerun as the recorded shared-harness confirmation on Linux
  - keep the maintained macOS-local baseline green while the remaining Windows reruns are collected
5. After the automated reruns, update only the validation docs that are justified by directly observed evidence.
6. Preserve the March 22, 2026 retrospective `skill-installer` confirmations in the platform validation notes and add richer installer metadata later only if it materially helps future release or support work.

## Current Repo State

- The shared test harness now renders rollout JSONL fixtures structurally, including nested JSON strings such as tool arguments and tool outputs.
- The shared baseline fixtures now use UTC so Windows test runs no longer depend on named timezone data for the common path.
- Named-timezone success-path behavior remains covered in the targeted renderer tests rather than in the shared fixture baseline.
- The runtime code was left unchanged during this harness cleanup.

## Acceptance Criteria

- In a fresh Windows virtual environment, `python -m pip install -e ".[dev]"` followed by `python -m pytest` passes without ad hoc fixes.
- The fixture-rendering regression test proves that a Windows-style path yields valid JSONL and valid nested JSON tool payloads.
- The maintained macOS-local baseline remains green for `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- Linux has at least one fresh rerun of the automated gates recorded after the shared harness cleanup, because this is shared cross-platform test infrastructure.
- Windows platform-validation docs are updated only with real runtime evidence, not merely because the shared automated suite becomes Windows-clean.

## Implementation Order

1. Re-run Windows gates in a fresh virtual environment.
2. Reconfirm the maintained macOS-local baseline if any follow-up change lands.
3. Record only the runtime evidence that is directly re-observed in `22_platform_validation.md` and the per-platform validation records.
4. Close the remaining manual Windows platform checklist items or document them explicitly as still open.
