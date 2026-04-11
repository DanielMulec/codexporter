# Open Questions And Next Steps

## Status

- Phase: validated v1 baseline with compact `shell_command` closure and staged no-`Any` hardening complete
- Date: April 11, 2026

## Agreed Post-April-5 Queue

1. Compact-mode `shell_command` normalization and regression coverage: closed on current repo state.
2. Session discovery fix for stale-SQLite or missing-thread-row current sessions: implemented on current repo state on April 11, 2026; pending fresh cross-platform rerun evidence.
3. Windows long-path behavior: open follow-up.
4. Windows `\\?\` user-facing path normalization: open follow-up.

## Session Discovery Implementation Plan (Approved April 11, 2026)

### Scope

- Implement explicit-thread discovery as rollout-first when `--session-id` or `CODEX_THREAD_ID` is available.
- Keep no-thread-id ambiguity behavior fail-closed exactly as it is today.
- Treat SQLite thread rows as secondary metadata for explicit-thread discovery, not as the sole authority.

### Implementation Steps

1. Update `session_store.py` so explicit-thread discovery first resolves rollout files by session id under `CODEX_HOME/sessions/**/rollout-*-<session_id>.jsonl`, then validates session id and normalized workspace from `session_meta`.
2. Preserve the existing fail-closed workspace mismatch protection for explicit session targets.
3. Use SQLite thread-row fields as optional metadata enrichment when available and consistent with the validated rollout context.
4. Keep no-session-id discovery behavior fail-closed and unchanged for this track.
5. Update user-facing diagnostics to distinguish rollout-missing conditions from stale or missing SQLite indexing conditions.

### Regression Tests Required

1. Full export succeeds when explicit session id is available, the rollout exists, and `state_5.sqlite` is missing the matching thread row.
2. Compact export succeeds in the same stale-SQLite or missing-thread-row condition.
3. Explicit wrong-workspace targeting still fails closed.
4. Ambiguous same-workspace discovery without a thread id still fails closed.
5. Diagnostics for rollout-missing and stale-index conditions remain distinct and deterministic.

### Acceptance Criteria For This Track

1. Explicit current-session export succeeds from rollout history even when `state_5.sqlite.threads` is stale or missing the matching row.
2. Full and compact export both use the corrected explicit-thread discovery path.
3. Workspace mismatch and no-thread-id ambiguity protections remain fail-closed.
4. Automated regression coverage for stale-SQLite/live-rollout conditions is merged and green.
5. `22_platform_validation.md` and per-platform validation records are updated only with directly observed rerun evidence after code lands.

### Freshness Note

- Check date: April 11, 2026.
- Official Codex docs used for boundary confirmation: `https://developers.openai.com/codex/config-reference` and `https://developers.openai.com/codex/app/windows/`.
- Current public docs do not define `session_index.jsonl`, `state_5.sqlite`, or rollout filename schema as stable integration contracts, so this plan treats local-state discovery as best-effort and robustness-oriented.

### Implementation Status

- Completed on current repo state on April 11, 2026 in `session_store.py`, `messages.py`, and `tests/test_session_selection.py`.
- Explicit-thread discovery now resolves rollout metadata first and treats SQLite as secondary metadata.
- No-thread-id ambiguity behavior remains fail-closed.
- Added regression tests for stale-SQLite or missing-thread-row success paths in full and compact mode plus stale-index diagnostics.

## Key Open Questions

- The April 5, 2026 Windows host reruns closed the earlier compact `shell_command` regression and stale installed-skill-parity findings, but two Windows follow-up questions still remain on the current repo state:
  - what is the supported Windows path-length envelope, given that the copied current Windows CLI-style `\\?\` row now succeeds at project-root length `221` while a parallel plain-path control still fails at `222` and `LongPathsEnabled = 0`
  - should successful targeted recovery paths be normalized for user-facing display instead of surfacing raw `\\?\` path spellings in success messages and checkpoint artifact paths
- Which minimal rerun matrix should be executed next to close validation evidence for the April 11, 2026 session-discovery implementation across macOS, Linux, Windows CLI, and Windows app?
- How much tuning do we want on the compact profile's generic bulky-output thresholding beyond the initial deterministic implementation?
- How much additional installer metadata do we want beyond Daniel's retrospective March 22, 2026 install confirmations on macOS, Linux, and Windows devices?
- Do we want any of the lower-value extra mypy `Any` flags after the now-complete Stage 3 baseline, or is the current repo-wide `disallow_any_expr` posture sufficient?
- A lower-priority macOS path-alias seam surfaced during the April 5, 2026 isolated app-style replay: `/var/...` and `/private/var/...` are not yet treated as equivalent during same-workspace session matching unless the paths are normalized to the same resolved spelling first.

## Recommended Next Spec Steps

1. Treat `21_coverage_matrix.md` as the working QA baseline, `22_platform_validation.md` as the working platform evidence model, `23_engineering_policy.md` as the working project-specific engineering policy, and `24_installation_and_distribution.md` as the working distribution-boundary spec.
2. Preserve the recorded macOS app, macOS CLI, Linux CLI, Windows app, and historical Windows CLI runtime evidence, and keep distinguishing checklist-validated surfaces from residual platform-specific caveats that still sit outside the checklist.
3. Treat the implemented March 27, 2026 compact-mode surface as current repo state, not as a pending design discussion.
4. Keep the maintained macOS-local baseline green and rerun Linux or Windows quality gates when future code changes touch shared exporter behavior.
5. Update validation docs only with directly observed runtime evidence.
6. Preserve the March 22, 2026 retrospective `skill-installer` confirmations in the platform validation notes and add richer installer metadata later only if it materially helps future release or support work.
7. Use future Windows follow-up work first on the supported path-length envelope and user-facing path normalization before doing lower-priority compact-threshold tuning or new profile work.
8. Use `28_no_any_rollout.md` as the source of truth for the staged no-`Any` hardening order; do not claim repo-wide no-`Any` enforcement until the corresponding mypy settings are actually enabled.
9. When the rollout reaches shared exporter refactors, use directly observed Linux reruns, including a Fedora guest on Daniel's Mac when available, as supplemental Linux evidence rather than as assumed coverage.
10. Keep the lower-priority macOS `/var` versus `/private/var` path-alias seam deferred until the higher-priority Windows follow-up is closed first; if it is later closed, the intended shape is a small `session_store.py` normalization fix plus regression coverage.

## Current Repo State

- The shared test harness now renders rollout JSONL fixtures structurally, including nested JSON strings such as tool arguments and tool outputs.
- The shared unit-test baseline now uses host-independent UTC construction, so Windows test runs do not depend on named timezone data for UTC cases.
- Markdown expectation templates now re-encode fenced JSON blocks structurally, so Windows path escaping matches the renderer output instead of depending on raw string substitution.
- Named-timezone success-path behavior remains covered in the targeted renderer tests rather than in the shared fixture baseline.
- On March 27, 2026, a fresh Windows `.venv` rerun passed `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .`.
- On March 27, 2026, controlled Windows CLI and Windows app close-out replays were recorded from isolated temporary Codex homes derived from copied real thread rows and copied rollout artifacts, closing the remaining Windows checklist items without mutating live Codex state.
- On March 27, 2026, the initial compact export profile landed on the same `export` skill surface via `$export --compact`, preserving chronology and checkpoint identity while deterministically compacting bulky raw tool payloads.
- The maintained macOS-local automated baseline is now 45 passing `pytest` cases, including compact CLI invocation, deterministic bulky-payload compaction, oversized JSON-output compaction, compact/full checkpoint-sharing behavior, malformed-rollout timestamp handling, tool-output instruction-payload omission, boolean checkpoint-field rejection, `shell_command` compaction coverage for JSON-backed, plain-string, and sanitized app-style rollout payloads, and explicit stale-SQLite/missing-thread-row session-discovery coverage in both full and compact modes.
- On April 2-3, 2026, the staged no-`Any` hardening plan moved from audit to completed baseline: Stage 1 landed by enabling `disallow_any_explicit` and `disallow_any_unimported`, Stage 2 landed after narrowing the production JSON, SQLite, and CLI boundaries, and Stage 3 then landed after the test fixture and JSON assertion helpers were typed well enough for repo-wide `disallow_any_expr`.
- On April 2-3, 2026, Daniel revalidated the post-Stage-2 macOS happy path from live Codex surfaces more broadly than the retained local transcripts alone show: on both macOS app and macOS CLI he exercised full export, full incremental export, full compact export, and compact incremental export from the current repo state across multiple invocation orders. The retained transcripts document example slices of that broader retest. This reconfirmation was happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.
- On April 3, 2026, Daniel also revalidated the post-Stage-2 Linux happy path and confirmed that both full and compact exports still worked from the current repo state. That Linux reconfirmation was also happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.
- On April 3, 2026, Daniel also revalidated the post-Stage-2 Windows happy path more broadly than the earlier retained evidence alone showed: on both Windows app and Windows CLI he exercised full export, full incremental export, full compact export, and compact incremental export from the current repo state across multiple invocation orders. This Windows reconfirmation was also happy-path-only and does not replace the March 27 controlled failure-path close-out evidence.
- On April 3, 2026, a deeper Windows 11 ARM audit of the current repo state then reran the Windows gates in a fresh temporary `.venv`, replayed copied Windows Codex homes derived from the current live app thread, and reproduced a blocking Windows app compact-mode regression on real `shell_command` traffic, a stale installed-skill/repo mismatch on this machine, and a long-path Windows write failure on the current repo entrypoint. That historical audit is recorded in `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md`.
- On April 5, 2026, fresh Windows-host reruns on the current repo state closed the earlier compact `shell_command` and stale-install findings: the installed skill again matched the repo content after line-ending normalization, a fresh Windows `.venv` passed `pytest` with `42` tests plus the binding `mypy` and `ruff` gates, live installed-skill app exports succeeded on the active thread, live installed-skill CLI exports then succeeded again on the active CLI thread, and copied-state Windows app-style and CLI-style replays re-confirmed no-new-content behavior, compact/full checkpoint sharing, compact `shell_command` omission, ambiguity fail-closed behavior, targeted recovery, German checkpoint-failure localization, denied rollout access handling, and unsafe installed-skill-directory rejection.
- That same April 5 Windows validation narrowed the remaining path-length question instead of closing it outright: the copied current CLI-style row with extended-length `\\?\` cwd succeeded at project-root length `221`, while a parallel plain-path control still failed at `222` with `LongPathsEnabled = 0`. The raw `\\?\` path-display rough edge on targeted recovery also remains current, so those two path-oriented seams are now the active Windows follow-up rather than the older compact-shell or stale-install blockers.
- On April 5, 2026, the current repo state was revalidated again on macOS app with both a live installed-skill compact export on the active `vscode` thread and isolated app-style replays that re-confirmed `shell_command` compact behavior, no-new-content handling, compact/full checkpoint sharing, German checkpoint-failure localization, same-workspace ambiguity recovery, restricted-rollout honesty, workspace-mismatch rejection, and unsafe installed-skill-directory rejection.
- That April 5 macOS rerun also surfaced one lower-priority path-alias seam in the validation harness itself: same-workspace session matching did not treat `/var/...` and `/private/var/...` as equivalent until the disposable validation homes were normalized to the same resolved path spelling. That seam is explicitly deferred behind the higher-priority Windows work and is not currently treated as a blocker for the macOS validation baseline.

## Acceptance Criteria

- A fresh Windows virtual environment now passes `python -m pip install -e ".[dev]"`, `python -m pytest`, `python -m mypy skills/export tests`, `python -m ruff check .`, and `python -m ruff format --check .` without ad hoc fixes.
- The fixture-rendering regression test proves that a Windows-style path yields valid JSONL and JSON-valid fenced markdown for tool arguments.
- The maintained macOS-local baseline remains green for `pytest`, `mypy`, `ruff check`, and `ruff format --check`.
- Linux and Windows each now have at least one fresh rerun of the automated gates recorded after the shared harness cleanup.
- Windows platform-validation docs are now updated from real runtime evidence rather than from assumptions.
- The initial compact profile is invokable through `$export --compact` without changing export numbering or checkpoint semantics.
- Compact exports omit full file-read bodies, raw `apply_patch` bodies, and large raw diff bodies deterministically while preserving short raw diffs and the visible session chronology.
- The current repo entrypoint's Windows path-length behavior is either closed as a bug or explicitly documented as an unsupported boundary before the remaining Windows follow-up is considered closed.
- Successful Windows targeted recovery either normalizes `\\?\` path spellings for user-facing success output and newly written checkpoint paths or documents the raw spelling as an intentional boundary.

## Implementation Order

1. Reconfirm the maintained macOS-local baseline and rerun at least one Linux or Windows gate after the April 11, 2026 session-discovery change.
2. Record only the runtime evidence that is directly re-observed in `22_platform_validation.md` and the per-platform validation records.
3. Decide and document the supported Windows path-length envelope, then rerun the repo entrypoint accordingly.
4. Normalize Windows success-message and checkpoint artifact paths for targeted `\\?\` recovery, or document that raw path spelling explicitly as an intentional boundary.
5. Keep future Windows validation additive rather than redefining the meaning of the v1 checklist.
6. Treat future compact-mode work as threshold tuning or explicit new profile design, not as a rewrite of the implemented `--compact` contract.
7. Treat the repo-wide no-`Any` expression gate as the new baseline and revisit lower-value extra `Any` flags only if a demonstrated gap justifies them.
8. Defer the macOS `/var` versus `/private/var` path-alias cleanup until after the higher-priority Windows items are addressed; if we choose to close it later, the intended shape is a small `session_store.py` normalization fix plus regression coverage.
