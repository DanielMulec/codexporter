# Degraded Mode Behavior

## Status

- Phase: implementation and validation
- Date: March 10, 2026
- Scope: v1 contract

## Purpose

This document defines how the export skill must behave when the environment blocks access to all or part of the required data.

## Core Rule

The skill must never fail silently.

The skill must never imply success when the export did not actually succeed.

## User-Facing Failure Rule

When export fails, Codex must inform the user in natural language:

- that the export failed
- the specific reason it failed
- a next-step hint when one can be given responsibly

## Language Rule

User-facing degraded-mode and omission messages should be generated in the language of the active conversation.

They should not be hardcoded to English when the user is actively using another language in that thread.

For v1, one narrow exception is allowed:

- if the failure happens before the exporter can read enough session history to determine the active conversation language at all, an English fallback message is acceptable
- this exception applies to pre-rollout access failures such as missing or unreadable persisted session history, not to ordinary post-parse failures where language detection is available

## Examples

- "I couldn't export this session because the current environment cannot access the persisted session history from here."
- "I couldn't include git information because this session is not in a git repository."

## Partial Availability Rule

If optional data is unavailable but the core export can still succeed:

- complete the export with the available data
- omit the unavailable optional section
- explain the omission when that explanation is useful to the user

## Restricted Environment Rule

The skill must be useful in restricted environments when possible, but it must not pretend that inaccessible data was exported.

If sandboxing or platform restrictions block required session access:

- do not fake an export
- explain the actual access limitation

## Current Session Resolution Rule

If a precise current-thread identifier is available at invocation time, the skill must prefer that identifier over workspace-path heuristics.

If the current session cannot be identified unambiguously, or if an explicit thread target conflicts with the invoking project context, the skill must stop rather than export a different session.

## Fail Safely Rule

If validation metadata or checkpoint state does not match expectations:

- stop the export rather than guessing
- do not advance the checkpoint
- inform the user directly what failed and why

If optional timezone lookup fails but the underlying timestamp data is available:

- continue the export
- render timestamps in UTC
- avoid failing the export for formatting-only reasons

## Future Compatibility Rule

Later versions may introduce richer recovery suggestions or platform-specific diagnostics, but they should extend the degraded-mode behavior rather than replace the core rule set above.

This follows the project anti-refactor rule: degraded-mode improvements should be additive and should not require redefining what counts as a successful export versus a failed export.
