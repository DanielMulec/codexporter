# Test Taxonomy

## Purpose

This document defines the test layers for the `$export` skill.

## Unit Tests

Purpose:

- verify isolated logic with fast feedback

Scope examples:

- filename generation
- session name sanitization
- markdown section rendering
- message heading rendering
- tool rendering formatting
- cursor handling logic
- sidecar JSON serialization
- language-selection rules for failures

## Integration Tests

Purpose:

- verify subsystems working together against realistic local inputs

Scope examples:

- reading persisted session data
- extracting exportable records
- rendering markdown artifact
- writing markdown file
- writing sidecar JSON
- updating checkpoint after success
- preserving checkpoint on failure
- including visible git-related content when present in the session history
- omitting optional metadata safely

## End-To-End Or Full-Flow Tests

Purpose:

- verify the complete `$export` flow from invocation to produced artifacts

Scope examples:

- first export in a live-like session
- repeated export in the same session
- blocked export behavior
- long-running session with multiple exports
- final user-facing success or failure messaging

## Manual Validation

Purpose:

- verify behavior that depends on real Codex environments and real OS usage

Scope examples:

- macOS CLI
- Linux CLI
- macOS app
- Windows CLI
- Windows app
- real-user validation by Daniel
- trusted-user validation on Windows

## Negative-Path Coverage Rule

Negative-path coverage must exist across all relevant layers, not only degraded-mode tests.

This includes:

- unreadable session data
- corrupted sidecar
- cursor mismatch
- missing git repo
- unsafe session names
- missing optional metadata
- language-sensitive failure behavior

## Mapping Rule

Every important user-side acceptance criterion should map to at least one test scenario and one test layer.
