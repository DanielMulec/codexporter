# Degraded Mode Behavior

## Status

- Phase: analysis and discussion
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

## Future Compatibility Rule

Later versions may introduce richer recovery suggestions or platform-specific diagnostics, but they should extend the degraded-mode behavior rather than replace the core rule set above.
