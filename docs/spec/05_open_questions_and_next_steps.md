# Open Questions And Next Steps

## Status

- Phase: validated v1 baseline with implemented initial compact mode and staged no-`Any` hardening plan
- Date: April 3, 2026

## Key Open Questions

- The April 3, 2026 Windows 11 ARM post-refactor audit re-opened blocking Windows validation work on the current repo state:
  - real Windows app-style compact exports still leak bulky raw `shell_command` file-read output
  - the globally installed Windows skill on this machine is stale relative to the repo, so installed-skill manual runs do not automatically validate the current revision
  - a long-path Windows project root still fails during export writing on the current repo entrypoint
- How should the repo resolve the separate March 28, 2026 stale-SQLite/live-rollout session-discovery proposal relative to the new April 3, 2026 Windows findings, given that the proposal remains partly unimplemented but was not the main blocker reproduced in this audit?
- How much tuning do we want on the compact profile's generic bulky-output thresholding beyond the initial deterministic implementation?
- How much additional installer metadata do we want beyond Daniel's retrospective March 22, 2026 install confirmations on macOS, Linux, and Windows devices?
- Do we want any of the lower-value extra mypy `Any` flags after the now-complete Stage 3 baseline, or is the current repo-wide `disallow_any_expr` posture sufficient?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, Linux CLI, and historical Windows CLI runtime evidence, but do not keep claiming that Windows app or broader Windows post-refactor sign-off is closed while the April 3, 2026 Windows findings remain open.
3. Treat the implemented March 27, 2026 compact-mode surface as current repo state, not as a pending design discussion.
4. Keep the maintained macOS-local baseline green and rerun Linux or Windows quality gates when future code changes touch shared exporter behavior.
5. Update validation docs only with directly observed runtime evidence.
6. Preserve the March 22, 2026 retrospective `skill-installer` confirmations in the platform validation notes and add richer installer metadata later only if it materially helps future release or support work.
7. Use future compact-mode work first to close the reopened Windows app blocker by covering real `shell_command` file-read and listing traffic before doing lower-priority threshold tuning or new profile work.
8. Use `28_no_any_rollout.md` as the source of truth for the staged no-`Any` hardening order; do not claim repo-wide no-`Any` enforcement until the corresponding mypy settings are actually enabled.
9. When the rollout reaches shared exporter refactors, use directly observed Linux reruns, including a Fedora guest on Daniel's Mac when available, as supplemental Linux evidence rather than as assumed coverage.

## Current Repo State

- The shared test harness now renders rollout JSONL fixtures structurally, including nested JSON strings such as tool arguments and tool outputs.
- The shared unit-test baseline now uses host-independent UTC construction, so Windows test runs do not depend on named timezone data for UTC cases.
- Markdown expectation templates now re-encode fenced JSON blocks structurally, so Windows path escaping matches the renderer output instead of depending on raw string substitution.
- Named-timezone success-path behavior remains covered in the targeted renderer tests rather than in the shared fixture baseline.
- On March 27, 2026, a fresh Windows `.venv` rerun passed `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .`.
- On March 27, 2026, controlled Windows CLI and Windows app close-out replays were recorded from isolated temporary Codex homes derived from copied real thread rows and copied rollout artifacts, closing the remaining Windows checklist items without mutating live Codex state.
- On March 27, 2026, the initial compact export profile landed on the same `export` skill surface via `$export --compact`, preserving chronology and checkpoint identity while deterministically compacting bulky raw tool payloads.
- The maintained macOS-local automated baseline is now 39 passing `pytest` cases, including compact CLI invocation, deterministic bulky-payload compaction, oversized JSON-output compaction, compact/full checkpoint-sharing behavior, malformed-rollout timestamp handling, tool-output instruction-payload omission, and boolean checkpoint-field rejection.
- On April 2-3, 2026, the staged no-`Any` hardening plan moved from audit to completed baseline: Stage 1 landed by enabling `disallow_any_explicit` and `disallow_any_unimported`, Stage 2 landed after narrowing the production JSON, SQLite, and CLI boundaries, and Stage 3 then landed after the test fixture and JSON assertion helpers were typed well enough for repo-wide `disallow_any_expr`.
- On April 2-3, 2026, Daniel revalidated the post-Stage-2 macOS happy path from live Codex surfaces more broadly than the retained local transcripts alone show: on both macOS app and macOS CLI he exercised full export, full incremental export, full compact export, and compact incremental export from the current repo state across multiple invocation orders. The retained transcripts document example slices of that broader retest. This reconfirmation was happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.
- On April 3, 2026, Daniel also revalidated the post-Stage-2 Linux happy path and confirmed that both full and compact exports still worked from the current repo state. That Linux reconfirmation was also happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.
- On April 3, 2026, Daniel also revalidated the post-Stage-2 Windows happy path more broadly than the earlier retained evidence alone showed: on both Windows app and Windows CLI he exercised full export, full incremental export, full compact export, and compact incremental export from the current repo state across multiple invocation orders. This Windows reconfirmation was also happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.
- On April 3, 2026, a deeper Windows 11 ARM audit of the current repo state then reran the Windows gates in a fresh temporary `.venv`, replayed copied Windows Codex homes derived from the current live app thread, and reproduced a blocking Windows app compact-mode regression on real `shell_command` traffic, a stale installed-skill/repo mismatch on this machine, and a long-path Windows write failure on the current repo entrypoint. That audit is recorded in `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md`.

## Acceptance Criteria

- A fresh Windows virtual environment now passes `python -m pip install -e ".[dev]"`, `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .` without ad hoc fixes.
- The fixture-rendering regression test proves that a Windows-style path yields valid JSONL and JSON-valid fenced markdown for tool arguments.
- The maintained macOS-local baseline remains green for `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- Linux and Windows each now have at least one fresh rerun of the automated gates recorded after the shared harness cleanup.
- Windows platform-validation docs are now updated from real runtime evidence rather than from assumptions.
- The initial compact profile is invokable through `$export --compact` without changing export numbering or checkpoint semantics.
- Compact exports omit full file-read bodies, raw `apply_patch` bodies, and large raw diff bodies deterministically while preserving short raw diffs and the visible session chronology.
- Real Windows app-style compact exports also omit bulky raw `shell_command` file-read bodies deterministically rather than preserving the full raw file contents.
- Installed-skill Windows validation on this machine proves parity with the current repo revision before it is used as evidence for the current repo state.
- The current repo entrypoint's Windows path-length behavior is either closed as a bug or explicitly documented as an unsupported boundary before Windows is treated as fully revalidated again.

## Implementation Order

1. Reconfirm the maintained macOS-local baseline if a future follow-up change lands.
2. Record only the runtime evidence that is directly re-observed in `22_platform_validation.md` and the per-platform validation records.
3. Fix the reopened Windows app compact-mode blocker on real `shell_command` traffic and add automated regression coverage for that exact surface.
4. Refresh the installed Windows skill before counting any installed-skill rerun as evidence for the current repo revision.
5. Decide and document the supported Windows path-length envelope, then rerun the repo entrypoint accordingly.
6. Keep future Windows validation additive rather than redefining the meaning of the v1 checklist.
7. Treat future compact-mode work after the blocker fix as threshold tuning or explicit new profile design, not as a rewrite of the implemented `--compact` contract.
8. Treat the repo-wide no-`Any` expression gate as the new baseline and revisit lower-value extra `Any` flags only if a demonstrated gap justifies them.
