# Platform Validation

## Purpose

This document defines what counts as validation evidence for each primary v1 target environment.

It exists so that platform support is not treated as a vague claim.

## Validation Principle

A platform should be treated as validated only when the agreed evidence has been observed for that platform.

Target support and validated support are not the same thing:

- target support means the platform is in scope for v1
- validated support means the agreed evidence has been collected

## Core Validation Checklist

The following checks define the baseline validation evidence for a target environment:

1. A first export of the current live session succeeds.
2. The export file is written into the `codex_exports` subfolder in the current project root.
3. The success message provides the file name and file path.
4. A repeated export in the same session behaves incrementally.
5. A repeated export with no new content creates no new file and informs the user directly.
6. Export filenames sequence correctly across repeated exports of the same session.
7. The rendered markdown follows the approved visible-chat-first format closely enough to satisfy the v1 rendering rules.
8. Failure or omission messaging follows the language of the active conversation when the exporter can determine that language from the available session data; pre-rollout access failures may fall back to English in v1.
9. Restricted-environment behavior does not claim false success.
10. When multiple sessions share a workspace or platform-specific path spellings vary, export still targets the invoking current thread or fails clearly rather than exporting a different session.
11. When the user invokes `$export --compact`, the export succeeds on the same canonical exporter surface, records the compact render profile, preserves visible chronology, and applies the approved deterministic compactness rules without forking checkpoint identity.

## Validation Evidence Types

Acceptable evidence may include:

- direct real-user validation by Daniel
- direct real-user validation by trusted Windows users
- full-flow test results in the target environment
- captured artifact examples from the target environment
- concise validation notes recorded against the checklist below

For Linux CLI validation, directly observed execution inside a Linux guest or VM may count as Linux evidence when the guest environment is recorded explicitly. It does not count as Windows evidence and does not replace Windows validation.

## Result Vocabulary

Use the following result labels in checklist records:

- `pass`
- `fail`
- `partial`
- `not run`

## Validation Scope Clarification

Happy-path success alone does not validate current-thread targeting correctness.

When practical, validation should include at least one condition that distinguishes the invoking thread from another same-workspace session or from an alternative path spelling of the same workspace.

## Per-Platform Validation Records

### macOS Codex CLI

- Target status: primary v1 target
- Validated status: validated
- Evidence source: `docs/validation/macos_cli.md`
- Codex version: `0.115.x` live happy-path evidence, plus March 27 close-out on `0.116.0` and `0.80.0`, plus April 5 and April 11 reruns on `0.118.0`
- Source surface: Codex CLI in Ghostty
- Model: `gpt-5.4` and `gpt-5.2-codex`
- Sandbox mode: March 18 live run not recorded; March 27 close-out and April 5 reruns observed `workspace-write` with network access
- Approval mode: March 18 live run not recorded; March 27 close-out and April 5 reruns observed `on-request`
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `pass`
  - restricted-environment honesty: `pass`
  - current-thread targeting under shared-workspace ambiguity or path variation: `pass`
  - compact export behavior: `pass`
- Notes: Daniel recorded direct real-user macOS CLI happy-path evidence on March 18, 2026. On March 27, 2026, the production entrypoint was rerun on macOS against isolated temporary Codex homes derived from copied real CLI thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, honest unreadable-rollout failure, same-workspace ambiguity fail-closed behavior, and targeted current-thread success without mutating live `~/.codex` state. Daniel also reported on March 22, 2026 that the global `skill-installer` flow had already succeeded on his macOS device for this skill. On April 2-3, 2026, Daniel then revalidated the post-Stage-2 live macOS CLI happy path more broadly than the retained transcripts alone show: he confirmed that full export, full incremental export, full compact export, and compact incremental export all succeeded from the current repo state across multiple invocation orders. Retained Codex CLI thread `019d5032-e209-7a70-ab8a-e5ebe9d0257b` preserves one concrete example slice of that broader retest, and he explicitly reported `Works great` after reviewing the normal and incremental artifacts. On April 5, 2026, the installed global skill under `~/.codex/skills/export/` was then rechecked against the repo copy, a live installed-skill rerun on retained CLI thread `019d5032-e209-7a70-ab8a-e5ebe9d0257b` created incremental export `20260405-170904-Hi-GPT-We-started-to-refactor-the-skill-to-get-implicit-any--4.md`, the immediate follow-up returned the explicit no-new-content message, and isolated CLI-style replays under `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-cli-validation-socbnfp_` re-confirmed compact-first/full-second checkpoint sharing, German checkpoint-failure localization, same-workspace ambiguity fail-closed behavior plus targeted recovery, restricted-rollout honesty, workspace-mismatch rejection, and unsafe installed-skill-directory rejection without mutating live `~/.codex` state.
  On April 11, 2026, macOS CLI was rerun again after the session-discovery implementation: retained live CLI thread invocation returned explicit no-new-content in both full and compact mode, and a fresh normalized-path isolated replay matrix under `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-matrix-final-cuj7jx5t` re-confirmed all checklist rows plus stale-index diagnostics and explicit stale-SQLite-thread-row targeted recovery (report: `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-matrix-final-cuj7jx5t/validation_report.json`).
  The compact checklist item for this platform is now backed by Daniel's broader April 2-3, 2026 live CLI retest across full and compact export orders, one retained April 3, 2026 live compact incremental CLI transcript, the April 5 live installed-skill rerun, the April 5 isolated compact-first/full-second replay matrix, and the maintained macOS-host automated gate rerun, which includes the explicit compact full-flow and compaction tests.

### Linux Codex CLI

- Target status: primary v1 target
- Validated status: validated
- Evidence source: `docs/validation/linux_cli.md`
- Codex version: `0.115.x` live happy-path evidence, plus March 27 close-out on `0.117.0` and `0.77.0`, plus April 3 and April 5 post-refactor reruns on `0.118.0`
- Source surface: Codex CLI in Kitty
- Model: `gpt-5.4` and `gpt-5.2`
- Sandbox mode: March 18 live run not recorded; March 27 controlled close-out observed `workspace-write` with network access and `danger-full-access`
- Approval mode: March 18 live run not recorded; March 27 controlled close-out observed `on-request` and `never`
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `pass`
  - restricted-environment honesty: `pass`
  - current-thread targeting under shared-workspace ambiguity or path variation: `pass`
  - compact export behavior: `pass`
- Notes: Daniel recorded direct real-user Linux CLI happy-path evidence on March 18, 2026. On March 27, 2026, the production entrypoint was rerun on Linux against isolated temporary Codex homes derived from copied real CLI thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, honest unreadable-rollout failure, same-workspace ambiguity fail-closed behavior, and targeted current-thread success without mutating live `~/.codex` state. Daniel also reported on March 22, 2026 that the global `skill-installer` flow had already succeeded on his Linux device for this skill. On April 3, 2026, a fresh Linux-host post-refactor rerun recreated `.venv`, passed `pytest`, `mypy`, `ruff check`, and `ruff format --check`, then captured live targeted export, live ambiguity fail-closed behavior under three same-workspace thread rows, and live compact incremental export on Codex CLI `0.118.0`. The same day, isolated temporary Codex homes derived from the current live Linux CLI thread row and copied rollout history recaptured compact-first/full-second checkpoint sharing, explicit no-new-content behavior, German checkpoint-failure localization, denied rollout access, same-workspace ambiguity recovery, explicit workspace-mismatch fail-closed behavior, and safe-project-root rejection without mutating live `~/.codex` state. On April 5, 2026, a second Linux-host rerun verified that the installed skill under `~/.codex/skills/export` matched the repo copy, then re-observed a live installed-skill first export plus compact incremental export on live Linux CLI thread `019d5d8e-d3c2-7d70-ade4-f66f5dc126cc`, refreshed the same copied-state edge-case matrix under `/tmp/codexporter-linux-manual-validate-gee_dyuf`, and manually replayed a sanitized app-style `shell_command` compact export on Linux to confirm the shared command-normalization fix no longer leaks the raw `pyproject.toml` body.
  The compact checklist item for this platform is now backed by the April 3, 2026 live compact incremental rerun, the April 3 and April 5 compact-first/full-second replays in isolated Linux temp homes, the April 5 installed-skill compact incremental rerun on the active Linux CLI thread, the Linux-host automated gate reruns, and the April 5 sanitized `shell_command` replay as supplemental shared-behavior evidence.

### macOS Codex app

- Target status: primary v1 target
- Validated status: validated
- Evidence source: `docs/validation/macos_app.md`
- Codex version: `0.115.0-alpha.11`, `0.118.0-alpha.2`, and `0.119.0-alpha.28`
- Source surface: Codex Desktop app context, rollout source field `vscode`
- Model: `gpt-5.4` and `gpt-5.3-codex`
- Sandbox mode: `danger-full-access` in the March 13-14 and April 5 live app-context runs; `workspace-write` without network access in the March 27 close-out source row
- Approval mode: `never` in the March 13-14 and April 5 live app-context runs; `on-request` in the March 27 close-out source row
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `pass`
  - restricted-environment honesty: `pass`
  - current-thread targeting under shared-workspace ambiguity or path variation: `pass`
  - compact export behavior: `pass`
- Notes: March 13-14, 2026 captured direct macOS app happy-path evidence, including installed-skill invocation into the active project root. On March 27, 2026, the production entrypoint was rerun on macOS against isolated temporary Codex homes derived from copied real `vscode` thread data, which captured German checkpoint-failure messaging, honest unreadable-rollout failure, same-workspace ambiguity fail-closed behavior, and targeted current-thread success without mutating live app data. That closes the macOS app platform checklist while leaving GitHub-origin installation flow as a separate question. On April 2-3, 2026, Daniel then revalidated the post-Stage-2 live macOS app happy path more broadly than the retained transcripts alone show: he confirmed that full export, full incremental export, full compact export, and compact incremental export all succeeded from the current repo state across multiple invocation orders. Retained app-context thread `019d5012-678c-7223-867e-9ee9f25f4ab9` preserves one concrete example slice of that broader retest, where the installed `$export --compact` skill wrote a first-run compact artifact into the active project root after a dense synthetic payload. That April reconfirmation was happy-path-only, so March 27 remained the authoritative failure-path source until the April 11, 2026 rerun refreshed those rows again on current repo state.
  On April 5, 2026, the current repo state was revalidated again on macOS app in two layers: a live installed-skill compact export on the active `vscode` app thread under Codex `0.118.0-alpha.2`, and isolated app-style replays derived from copied thread rows and copied rollout artifacts that re-confirmed `shell_command` compact behavior, shared compact/full checkpoint identity, no-new-content behavior, German checkpoint-failure localization, same-workspace ambiguity fail-closed behavior, targeted recovery, restricted-rollout honesty, workspace-mismatch rejection, and unsafe installed-skill-directory rejection. Those April 5 replays also confirmed `argv`-shaped `shell_command` compaction on the current repo state.
  On April 11, 2026, the live macOS app surface was rerun again on thread `019d7db4-d5fb-7d10-998b-06872ff57b7f` (Codex `0.119.0-alpha.28`) and produced first full plus compact incremental exports from the active project root; the same-day normalized-path isolated replay matrix under `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-matrix-final-cuj7jx5t` re-confirmed all checklist rows plus stale-index diagnostics and explicit stale-SQLite-thread-row targeted recovery (report: `/private/var/folders/z7/vnklz78n3954_0ljxwny2p0m0000gn/T/codexporter-macos-matrix-final-cuj7jx5t/validation_report.json`).
  One lower-priority macOS path-alias seam surfaced during those isolated replays: `/var/...` and `/private/var/...` were not treated as equivalent until the disposable validation homes were normalized to the same resolved path spelling. That does not currently overturn the validated macOS app checklist, but it remains a deferred cleanup rather than a closed path-variation guarantee.
  The compact checklist item is now satisfied by Daniel's broader April 2-3, 2026 live app retest across full and compact export orders, one retained April 2, 2026 live app-context `$export --compact` transcript, the April 5, 2026 live installed-skill compact rerun, the April 5 controlled app-style replay matrix, and the maintained macOS-host automated gate rerun used as supplemental evidence for this repository.

### Windows Codex CLI

- Target status: primary v1 target
- Validated status: validated on the current repo state, with residual Windows runtime caveats outside the core checklist
- Evidence source: `docs/validation/windows_cli.md`
- Codex version: March 20 live happy-path metadata not recorded; March 27 controlled close-out on `0.116.0`; April 5 live rerun on `0.118.0`
- Source surface: Codex CLI
- Model: `gpt-5.4`
- Sandbox mode: March 20 live run not recorded; March 27 controlled close-out observed `danger-full-access`; April 5 live and copied-state reruns observed `danger-full-access`
- Approval mode: March 20 live run not recorded; March 27 controlled close-out observed `never`; April 5 live and copied-state reruns observed `never`
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `pass`
  - restricted-environment honesty: `pass`
  - current-thread targeting under shared-workspace ambiguity or path variation: `pass`
  - compact export behavior: `pass`
- Notes: Daniel recorded direct real-user Windows CLI happy-path evidence on March 20, 2026. On March 27, 2026, the production entrypoint was rerun on Windows against isolated temporary Codex homes derived from copied real CLI thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, explicit persisted-session-history failure under denied read access, first/incremental/no-new-content sequencing, visible-chat-first markdown inspection, same-workspace ambiguity fail-closed behavior, and targeted current-thread recovery while the temp state DB used Windows extended-length `\\?\` path spelling. The same day also produced a fresh green Windows `.venv` rerun of `pytest`, `mypy`, `ruff check`, and `ruff format --check`. On April 3, 2026, Daniel then revalidated the post-Stage-2 live Windows CLI happy path and confirmed that full export, full incremental export, full compact export, and compact incremental export all still worked from the current repo state across multiple invocation orders, including mixed full-to-compact and compact-to-full sequences. That April reconfirmation was happy-path-only, so the March 27 controlled close-out remained the authoritative failure-path and ambiguity evidence until the fresh April 5 CLI rerun.
  On April 5, 2026, the current repo state was revalidated again on the real Windows Codex CLI surface: the installed skill under `C:\Users\Daniel\.codex\skills\export` matched the repo content after line-ending normalization, the active CLI thread `019d5e4b-2ed0-7423-83e8-c2341bc8d751` produced fresh first, incremental, and compact incremental installed-skill exports on Codex `0.118.0`, and isolated copied-state CLI replays under `C:\Users\Daniel\AppData\Local\Temp\codexporter-win-cli-manual-validate-_yhx2ky7` re-confirmed compact-first/full-second checkpoint sharing, explicit no-new-content behavior, denied rollout access handling, ambiguity fail-closed behavior, targeted recovery, workspace-mismatch rejection, German checkpoint-failure localization, and unsafe installed-skill-directory rejection.
  That same April 5 rerun also added a sanitized copied-state CLI `shell_command` compact replay, which used `Raw file contents omitted in compact mode.`, listed `pyproject.toml`, and did not leak the raw file body. One Windows path-length nuance also narrowed materially on this rerun: a copied CLI-style thread row whose persisted cwd used the extended-length `\\?\` spelling succeeded at project-root length `221`, while an otherwise parallel plain-path control still failed at length `222` with `LongPathsEnabled = 0`. The remaining Windows CLI caveats now observed directly on this host are therefore the raw `\\?\` success-message and checkpoint-path display rough edge plus the still-open plain-path long-path envelope, not an unresolved gap in the current live CLI checklist evidence.
  The compact checklist item for this platform is now backed by Daniel's April 3, 2026 live Windows CLI retest across full and compact export orders, the April 5, 2026 live installed-skill compact incremental rerun on the active CLI thread, the April 5 compact-first/full-second copied-state sequence replay, the April 5 copied CLI `shell_command` compact replay, and the fresh Windows-host automated full-flow and compaction tests.

### Windows Codex app

- Target status: primary v1 target
- Validated status: validated on the current repo state, with residual Windows runtime caveats outside the core checklist
- Evidence source: `docs/validation/windows_app.md`
- Codex version: `0.115.0-alpha.27` and `0.112.0-alpha.3`
- Source surface: Codex Desktop app context, rollout source field `vscode`
- Model: `gpt-5.4`
- Sandbox mode: `danger-full-access` and `workspace-write` without network access
- Approval mode: `never` and `on-request`
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `pass`
  - restricted-environment honesty: `pass`
  - current-thread targeting under shared-workspace ambiguity or path variation: `pass`
  - compact export behavior: `pass`
- Notes: direct real-user validation by Daniel recorded on March 18-20, 2026 in Windows Codex Desktop app context; validation covered the previously broken current-thread targeting case where the persisted thread row used a `\\?\` Windows path spelling while the invoking workspace used the plain drive-letter form, plus installed-skill happy-path, incremental behavior, and no-new-content behavior. On March 27, 2026, the production entrypoint was rerun on Windows against isolated temporary Codex homes derived from copied real app thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, explicit persisted-session-history failure under denied read access, same-workspace ambiguity fail-closed behavior, and targeted current-thread recovery without mutating live app data. The same day also produced a fresh green Windows `.venv` rerun of `pytest`, `mypy`, `ruff check`, and `ruff format --check`. On April 3, 2026, Daniel then revalidated the post-Stage-2 live Windows app happy path and confirmed that full export, full incremental export, full compact export, and compact incremental export all still worked from the current repo state across multiple invocation orders, including mixed full-to-compact and compact-to-full sequences. That April reconfirmation was happy-path-only, so the March 27 controlled close-out remains the authoritative failure-path and ambiguity evidence for this platform.
  On April 5, 2026, a fresh Windows-host rerun then revalidated the current repo state directly: the installed skill matched the repo content on disk after line-ending normalization, the current Windows app thread produced fresh installed-skill first, incremental, and compact incremental exports, and isolated copied-state replays re-confirmed no-new-content behavior, compact/full checkpoint sharing, same-workspace ambiguity fail-closed behavior, targeted `\\?\` current-thread recovery, workspace-mismatch rejection, denied rollout access handling, German checkpoint-failure localization, and unsafe installed-skill-directory rejection.
  That same April 5 rerun also closed the earlier compact checklist failure on the real Windows app-style surface: the copied `shell_command` compact replay now used `Raw file contents omitted in compact mode.`, listed `pyproject.toml`, and did not leak the raw file body. The remaining Windows runtime caveats now observed on this host are the long-path write failure and the raw `\\?\` success-message display rough edge. Those remain real Windows issues, but they sit outside the current v1 checklist rather than reopening Windows app validated status. See `codexporter-windows-post-refactor-validation-bug-report-2026-04-03.md` for the historical April 3 audit.

## Validation Recording Rules

- A platform should not be marked validated based on assumption alone.
- Partial validation should be recorded explicitly rather than rounded up to full validation.
- Checklist results should use the shared result vocabulary rather than free-form status words.
- Notes should capture meaningful deviations, not generic comments.
- If a platform fails one checklist item but passes the rest, that should be recorded as a real gap rather than hidden.

## Future Compatibility Rule

If later versions introduce new user-visible core behavior, the checklist should grow additively.

It should not redefine the meaning of the existing v1 validation evidence.
