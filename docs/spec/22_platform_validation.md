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
2. The export file is written into the `codex_exports` subfolder in the current project repository.
3. The success message provides the file name and file path.
4. A repeated export in the same session behaves incrementally.
5. A repeated export with no new content creates no new file and informs the user directly.
6. Export filenames sequence correctly across repeated exports of the same session.
7. The rendered markdown follows the approved visible-chat-first format closely enough to satisfy the v1 rendering rules.
8. Failure or omission messaging follows the language of the active conversation.
9. Restricted-environment behavior does not claim false success.

## Validation Evidence Types

Acceptable evidence may include:

- direct real-user validation by Daniel
- direct real-user validation by trusted Windows users
- full-flow test results in the target environment
- captured artifact examples from the target environment
- concise validation notes recorded against the checklist below

## Per-Platform Validation Records

### macOS Codex CLI

- Target status: primary v1 target
- Validated status:
- Evidence source:
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
- Notes:

### Linux Codex CLI

- Target status: primary v1 target
- Validated status:
- Evidence source:
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
- Notes:

### macOS Codex app

- Target status: primary v1 target
- Validated status:
- Evidence source:
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
- Notes:

### Windows Codex CLI

- Target status: primary v1 target
- Validated status:
- Evidence source:
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
- Notes:

### Windows Codex app

- Target status: primary v1 target
- Validated status:
- Evidence source:
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
- Notes:

## Validation Recording Rules

- A platform should not be marked validated based on assumption alone.
- Partial validation should be recorded explicitly rather than rounded up to full validation.
- Notes should capture meaningful deviations, not generic comments.
- If a platform fails one checklist item but passes the rest, that should be recorded as a real gap rather than hidden.

## Future Compatibility Rule

If later versions introduce new user-visible core behavior, the checklist should grow additively.

It should not redefine the meaning of the existing v1 validation evidence.
