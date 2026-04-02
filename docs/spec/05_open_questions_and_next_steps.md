# Open Questions And Next Steps

## Status

- Phase: validated v1 baseline with implemented initial compact mode and staged no-`Any` hardening plan
- Date: April 3, 2026

## Key Open Questions

- No blocking v1 Windows validation questions remain after the March 27, 2026 close-out.
- How much tuning do we want on the compact profile's generic bulky-output thresholding beyond the initial deterministic implementation?
- How much additional installer metadata do we want beyond Daniel's retrospective March 22, 2026 install confirmations on macOS, Linux, and Windows devices?
- How quickly do we want to move from production-only no-`Any` enforcement into test-suite-wide no-`Any` enforcement after the production pass is green?

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, Linux CLI, Windows CLI, and Windows app runtime evidence as validated.
3. Treat the implemented March 27, 2026 compact-mode surface as current repo state, not as a pending design discussion.
4. Keep the maintained macOS-local baseline green and rerun Linux or Windows quality gates when future code changes touch shared exporter behavior.
5. Update validation docs only with directly observed runtime evidence.
6. Preserve the March 22, 2026 retrospective `skill-installer` confirmations in the platform validation notes and add richer installer metadata later only if it materially helps future release or support work.
7. Use future compact-mode work only for threshold tuning, additional deterministic compaction rules, or explicitly documented new render profiles rather than reopening the first compact-mode contract.
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
- The maintained macOS-local automated baseline is now 36 passing `pytest` cases, including compact CLI invocation, deterministic bulky-payload compaction, oversized JSON-output compaction, and compact/full checkpoint-sharing behavior.
- On April 2, 2026, a stricter one-off mypy audit confirmed that the repo currently has no explicit `Any` annotations but still contains implicit `Any` propagation at dynamic boundaries, the staged remediation plan was recorded in `28_no_any_rollout.md`, Stage 1 was landed in `pyproject.toml` by enabling `disallow_any_explicit` and `disallow_any_unimported`, and Stage 2 then landed by enabling `disallow_any_expr` for `codexporter` production modules after the JSON, SQLite, and CLI boundaries were narrowed.
- On April 2-3, 2026, Daniel revalidated the post-Stage-2 macOS happy path from live Codex surfaces more broadly than the retained local transcripts alone show: on both macOS app and macOS CLI he exercised full export, full incremental export, full compact export, and compact incremental export from the current repo state across multiple invocation orders. The retained transcripts document example slices of that broader retest. This reconfirmation was happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.

## Acceptance Criteria

- A fresh Windows virtual environment now passes `python -m pip install -e ".[dev]"`, `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .` without ad hoc fixes.
- The fixture-rendering regression test proves that a Windows-style path yields valid JSONL and JSON-valid fenced markdown for tool arguments.
- The maintained macOS-local baseline remains green for `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- Linux and Windows each now have at least one fresh rerun of the automated gates recorded after the shared harness cleanup.
- Windows platform-validation docs are now updated from real runtime evidence rather than from assumptions.
- The initial compact profile is invokable through `$export --compact` without changing export numbering or checkpoint semantics.
- Compact exports omit full file-read bodies, raw `apply_patch` bodies, and large raw diff bodies deterministically while preserving short raw diffs and the visible session chronology.

## Implementation Order

1. Reconfirm the maintained macOS-local baseline if a future follow-up change lands.
2. Record only the runtime evidence that is directly re-observed in `22_platform_validation.md` and the per-platform validation records.
3. Keep future Windows validation additive rather than redefining the meaning of the v1 checklist.
4. Treat future compact-mode work as threshold tuning or explicit new profile design, not as a rewrite of the implemented `--compact` contract.
5. Continue no-`Any` hardening from the now-landed Stage 2 baseline by extending `disallow_any_expr` to the tests only after the test fixture and JSON assertion boundaries are cleaned up.
