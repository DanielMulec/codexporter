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
8. Failure or omission messaging follows the language of the active conversation.
9. Restricted-environment behavior does not claim false success.
10. When multiple sessions share a workspace or platform-specific path spellings vary, export still targets the invoking current thread or fails clearly rather than exporting a different session.

## Validation Evidence Types

Acceptable evidence may include:

- direct real-user validation by Daniel
- direct real-user validation by trusted Windows users
- full-flow test results in the target environment
- captured artifact examples from the target environment
- concise validation notes recorded against the checklist below

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
- Validated status: partial
- Evidence source: `docs/validation/macos_cli.md`
- Codex version: `0.115.x` (exact patch not recorded)
- Source surface: Codex CLI in Ghostty
- Model: `gpt-5.4`
- Sandbox mode: not recorded
- Approval mode: not recorded
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `not run`
  - restricted-environment honesty: `not run`
  - current-thread targeting under shared-workspace ambiguity or path variation: `not run`
- Notes: direct real-user validation by Daniel recorded on March 18, 2026; validation included both more-restricted and less-restricted runtime configurations, but the exact Codex approval-mode and sandbox-mode labels were not captured; no failure, blocked-access case, or same-workspace ambiguity case occurred during the recorded runs.

### Linux Codex CLI

- Target status: primary v1 target
- Validated status: partial
- Evidence source: `docs/validation/linux_cli.md`
- Codex version: `0.115.x` (exact patch not recorded)
- Source surface: Codex CLI in Kitty
- Model: `gpt-5.4`
- Sandbox mode: not recorded
- Approval mode: not recorded
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `not run`
  - restricted-environment honesty: `not run`
  - current-thread targeting under shared-workspace ambiguity or path variation: `not run`
- Notes: direct real-user validation by Daniel recorded on March 18, 2026; the tested CLI was reported as the same `0.115` series as the corresponding macOS validation, but the exact patch/build was not retained; validation included both more-restricted and less-restricted runtime configurations, but the exact Codex approval-mode and sandbox-mode labels were not captured; no failure, blocked-access case, or same-workspace ambiguity case occurred during the recorded runs.

### macOS Codex app

- Target status: primary v1 target
- Validated status: partial
- Evidence source: `docs/validation/macos_app.md`
- Codex version: `0.115.0-alpha.11`
- Source surface: Codex Desktop app context, rollout source field `vscode`
- Model: `gpt-5.4`
- Sandbox mode: `danger-full-access`
- Approval mode: `never`
- Checklist results:
  - first export: `pass`
  - default export destination: `pass`
  - success message with file location: `pass`
  - incremental export: `pass`
  - no-new-content behavior: `pass`
  - filename sequencing: `pass`
  - markdown rendering: `pass`
  - language-sensitive failure messaging: `partial`
  - restricted-environment honesty: `not run`
  - current-thread targeting under shared-workspace ambiguity or path variation: `not run`
- Notes: no-new-content behavior was validated by running two exporter calls inside one shell process so no extra Codex session records landed between the two checks; on March 14, 2026, the renamed globally installed `$export` skill was also invoked successfully in the active macOS app thread and wrote the export into the active project's `codex_exports/` folder rather than into the installed skill directory; non-English messaging, restricted-environment honesty, and same-workspace wrong-session resistance still need real-use validation.

### Windows Codex CLI

- Target status: primary v1 target
- Validated status:
- Evidence source:
- Codex version:
- Source surface:
- Model:
- Sandbox mode:
- Approval mode:
- Checklist results:
  - first export:
  - default export destination:
  - success message with file location:
  - incremental export:
  - no-new-content behavior:
  - filename sequencing:
  - markdown rendering:
  - language-sensitive failure messaging:
  - restricted-environment honesty:
  - current-thread targeting under shared-workspace ambiguity or path variation:
- Notes:

### Windows Codex app

- Target status: primary v1 target
- Validated status:
- Evidence source:
- Codex version:
- Source surface:
- Model:
- Sandbox mode:
- Approval mode:
- Checklist results:
  - first export:
  - default export destination:
  - success message with file location:
  - incremental export:
  - no-new-content behavior:
  - filename sequencing:
  - markdown rendering:
  - language-sensitive failure messaging:
  - restricted-environment honesty:
  - current-thread targeting under shared-workspace ambiguity or path variation:
- Notes:

## Validation Recording Rules

- A platform should not be marked validated based on assumption alone.
- Partial validation should be recorded explicitly rather than rounded up to full validation.
- Checklist results should use the shared result vocabulary rather than free-form status words.
- Notes should capture meaningful deviations, not generic comments.
- If a platform fails one checklist item but passes the rest, that should be recorded as a real gap rather than hidden.

## Future Compatibility Rule

If later versions introduce new user-visible core behavior, the checklist should grow additively.

It should not redefine the meaning of the existing v1 validation evidence.
