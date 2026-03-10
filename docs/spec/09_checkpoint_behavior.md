# Checkpoint Behavior

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 contract

## Purpose

This document defines how repeated exports of the same live session should behave in v1.

## V1 Checkpoint Rule

Repeated exports of the same session should be incremental.

That means each later export should include only the session content that appeared after the previous successful export checkpoint for that same session.

## Checkpoint Storage Rule

V1 should store checkpoint state in a sidecar file next to the export artifacts.

This is preferred over:

- embedding mutable checkpoint state into the markdown file itself
- hiding the checkpoint state in a global opaque storage location

## Why Sidecar Storage Is Preferred

- easier to inspect
- easier to debug
- easier to back up with the export artifacts
- easier to keep cross-platform
- lower refactor pressure when later features are added

## Incremental Export Behavior

- export `-1` for a session is the full export so far
- export `-2` and later contain only content after the previous successful checkpoint
- each export invocation produces a new markdown file
- earlier export files are not rewritten in v1

## Checkpoint Advancement Rule

Checkpoint state should advance only after a successful export.

If an export fails, the checkpoint must not move forward.

## Failure Safety Rule

The system must avoid checkpoint corruption or partial advancement if:

- the export fails midway
- the process stops unexpectedly
- the session data cannot be read consistently

## Future Compatibility Rule

The checkpoint model should be designed so that later features can be added without forcing a redesign of the v1 export identity.

This means later phases should be able to add:

- optional report artifacts
- optional classification artifacts
- optional richer metadata

without changing:

- the per-session sequence concept
- the meaning of a successful checkpoint

This follows the project anti-refactor rule: later features should attach to the existing checkpoint semantics rather than replace them.
