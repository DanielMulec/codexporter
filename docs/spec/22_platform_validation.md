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
- Codex version: `0.115.x` live happy-path evidence, plus March 27 close-out on `0.116.0` and `0.80.0`
- Source surface: Codex CLI in Ghostty
- Model: `gpt-5.4` and `gpt-5.2-codex`
- Sandbox mode: March 18 live run not recorded; March 27 close-out observed `workspace-write` with network access
- Approval mode: March 18 live run not recorded; March 27 close-out observed `on-request`
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
- Notes: Daniel recorded direct real-user macOS CLI happy-path evidence on March 18, 2026. On March 27, 2026, the production entrypoint was rerun on macOS against isolated temporary Codex homes derived from copied real CLI thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, honest unreadable-rollout failure, same-workspace ambiguity fail-closed behavior, and targeted current-thread success without mutating live `~/.codex` state. Daniel also reported on March 22, 2026 that the global `skill-installer` flow had already succeeded on his macOS device for this skill. On April 2-3, 2026, Daniel then revalidated the post-Stage-2 live macOS CLI happy path more broadly than the retained transcripts alone show: he confirmed that full export, full incremental export, full compact export, and compact incremental export all succeeded from the current repo state across multiple invocation orders. Retained Codex CLI thread `019d5032-e209-7a70-ab8a-e5ebe9d0257b` preserves one concrete example slice of that broader retest, and he explicitly reported `Works great` after reviewing the normal and incremental artifacts. That April reconfirmation was happy-path-only, so the March 27 controlled close-out still carries the authoritative failure-path and ambiguity evidence.
  The compact checklist item for this platform is now backed by Daniel's broader April 2-3, 2026 live CLI retest across full and compact export orders, one retained April 3, 2026 live compact incremental CLI transcript, and the maintained macOS-host automated gate rerun, which includes the explicit compact full-flow and compaction tests.

### Linux Codex CLI

- Target status: primary v1 target
- Validated status: validated
- Evidence source: `docs/validation/linux_cli.md`
- Codex version: `0.115.x` live happy-path evidence, plus March 27 close-out on `0.117.0` and `0.77.0`
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
- Notes: Daniel recorded direct real-user Linux CLI happy-path evidence on March 18, 2026. On March 27, 2026, the production entrypoint was rerun on Linux against isolated temporary Codex homes derived from copied real CLI thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, honest unreadable-rollout failure, same-workspace ambiguity fail-closed behavior, and targeted current-thread success without mutating live `~/.codex` state. Daniel also reported on March 22, 2026 that the global `skill-installer` flow had already succeeded on his Linux device for this skill. On April 3, 2026, Daniel then revalidated the post-Stage-2 live Linux CLI happy path and confirmed that both full and compact exports still worked from the current repo state. That April reconfirmation was happy-path-only, so the March 27 controlled close-out remains the authoritative failure-path and ambiguity evidence for this platform.
  The compact checklist item for this platform is now backed by Daniel's April 3, 2026 live Linux full and compact happy-path retest plus the fresh Linux-host automated gate rerun, which includes the explicit compact full-flow and compaction tests.

### macOS Codex app

- Target status: primary v1 target
- Validated status: validated
- Evidence source: `docs/validation/macos_app.md`
- Codex version: `0.115.0-alpha.11`
- Source surface: Codex Desktop app context, rollout source field `vscode`
- Model: `gpt-5.4`
- Sandbox mode: `danger-full-access` in the March 13-14 live app-context run; `workspace-write` without network access in the March 27 close-out source row
- Approval mode: `never` in the March 13-14 live app-context run; `on-request` in the March 27 close-out source row
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
- Notes: March 13-14, 2026 captured direct macOS app happy-path evidence, including installed-skill invocation into the active project root. On March 27, 2026, the production entrypoint was rerun on macOS against isolated temporary Codex homes derived from copied real `vscode` thread data, which captured German checkpoint-failure messaging, honest unreadable-rollout failure, same-workspace ambiguity fail-closed behavior, and targeted current-thread success without mutating live app data. That closes the macOS app platform checklist while leaving GitHub-origin installation flow as a separate question. On April 2-3, 2026, Daniel then revalidated the post-Stage-2 live macOS app happy path more broadly than the retained transcripts alone show: he confirmed that full export, full incremental export, full compact export, and compact incremental export all succeeded from the current repo state across multiple invocation orders. Retained app-context thread `019d5012-678c-7223-867e-9ee9f25f4ab9` preserves one concrete example slice of that broader retest, where the installed `$export --compact` skill wrote a first-run compact artifact into the active project root after a dense synthetic payload. That April reconfirmation was happy-path-only, so the March 27 controlled close-out remains the authoritative failure-path evidence for this platform.
  The compact checklist item is now satisfied by Daniel's broader April 2-3, 2026 live app retest across full and compact export orders, one retained April 2, 2026 live app-context `$export --compact` transcript, and the same macOS-host automated gate rerun used as supplemental evidence for this repository.

### Windows Codex CLI

- Target status: primary v1 target
- Validated status: validated
- Evidence source: `docs/validation/windows_cli.md`
- Codex version: March 20 live happy-path metadata not recorded; March 27 controlled close-out on `0.116.0`
- Source surface: Codex CLI
- Model: `gpt-5.4`
- Sandbox mode: March 20 live run not recorded; March 27 controlled close-out observed `danger-full-access`
- Approval mode: March 20 live run not recorded; March 27 controlled close-out observed `never`
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
- Notes: Daniel recorded direct real-user Windows CLI happy-path evidence on March 20, 2026. On March 27, 2026, the production entrypoint was rerun on Windows against isolated temporary Codex homes derived from copied real CLI thread rows and copied rollout artifacts, which captured German checkpoint-failure messaging, explicit persisted-session-history failure under denied read access, first/incremental/no-new-content sequencing, visible-chat-first markdown inspection, same-workspace ambiguity fail-closed behavior, and targeted current-thread recovery while the temp state DB used Windows extended-length `\\?\` path spelling. The same day also produced a fresh green Windows `.venv` rerun of `pytest`, `mypy`, `ruff check`, and `ruff format --check`. On April 3, 2026, Daniel then revalidated the post-Stage-2 live Windows CLI happy path and confirmed that full export, full incremental export, full compact export, and compact incremental export all still worked from the current repo state across multiple invocation orders, including mixed full-to-compact and compact-to-full sequences. That April reconfirmation was happy-path-only, so the March 27 controlled close-out remains the authoritative failure-path and ambiguity evidence for this platform.
  The compact checklist item for this platform is now backed by Daniel's April 3, 2026 live Windows CLI retest across full and compact export orders plus that fresh Windows-host automated gate rerun, which includes the explicit compact full-flow and compaction tests.

### Windows Codex app

- Target status: primary v1 target
- Validated status: validated
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
  The compact checklist item is now satisfied by Daniel's April 3, 2026 live Windows app retest across full and compact export orders plus the same Windows-host automated gate rerun used as supplemental evidence for this repository.

## Validation Recording Rules

- A platform should not be marked validated based on assumption alone.
- Partial validation should be recorded explicitly rather than rounded up to full validation.
- Checklist results should use the shared result vocabulary rather than free-form status words.
- Notes should capture meaningful deviations, not generic comments.
- If a platform fails one checklist item but passes the rest, that should be recorded as a real gap rather than hidden.

## Future Compatibility Rule

If later versions introduce new user-visible core behavior, the checklist should grow additively.

It should not redefine the meaning of the existing v1 validation evidence.
