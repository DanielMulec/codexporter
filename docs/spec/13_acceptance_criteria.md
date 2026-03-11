# Acceptance Criteria

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 acceptance criteria draft

## Purpose

This document turns the current v1 decisions into acceptance criteria.

## Core Export

- The skill must export the current live Codex session when the user invokes `$export`.
- The output must be a markdown file.
- The export must reflect the current session, not a different session or a project-wide history.

## Default Output Content

- The default export must stay close to what the user visibly experienced in chat.
- The export must include visible user messages.
- The export must include visible assistant replies.
- The export must include visible assistant commentary or progress updates when available.
- The export must include visible tool invocations and outputs when available.
- The export must include a compact session metadata header.

## Metadata

- The export must include model name when available.
- The export must include session id when available.
- The export must include session start timestamp when available.
- The export must include current working directory when available.
- The default export must not be cluttered with excessive optional environment metadata.

## Exclusions

- The export must not include hidden chain-of-thought.
- The export must not include encrypted reasoning payloads.
- The export must not dump raw internal instruction payloads by default.
- The export must not require dedicated structured session-level git metadata in v1.

## Artifact And Naming

- Each export invocation must create one primary markdown artifact.
- The filename must follow the agreed export naming structure.
- Repeated exports for the same session must increment the per-session export number.
- The primary markdown artifact must follow the agreed rendering rules and section order.

## Incremental Export

- The first export for a session must export the session so far.
- Later exports for the same session must export only what appeared after the previous successful checkpoint.
- Prior markdown export artifacts must not be rewritten in v1.

## Checkpoint Sidecar

- V1 must use a sidecar checkpoint file.
- The sidecar file must use JSON.
- The sidecar must use `last_exported_record_index` as the primary resume cursor.
- The sidecar must store validation metadata alongside the primary cursor.
- The checkpoint must advance only after a successful export.
- A failed export must not advance the checkpoint.

## Degraded-Mode Behavior

- The skill must never fail silently.
- The skill must never imply success when export did not actually succeed.
- If checkpoint or validation metadata does not match expectations, the skill must stop rather than guess.
- User-facing failure messages must explain what failed and why.
- User-facing failure or omission messages should include a next-step hint when one is responsibly available.
- User-facing failure or omission messages must follow the language of the active conversation.

## Environment Targets

- V1 must target macOS Codex CLI.
- V1 must target Linux Codex CLI.
- V1 must target macOS Codex app.
- V1 must target Windows Codex CLI.
- V1 must target Windows Codex app.

## Extensibility Constraint

- The v1 design must allow deferred features to be added later as optional stages or optional artifacts.
- Adding deferred features later must not require redefining the meaning of a session export, the primary artifact, or checkpoint behavior.
