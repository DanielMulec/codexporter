# Test Scenarios

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 test planning draft

## Purpose

This document lists the main v1 test scenarios implied by the current specification.

## Successful Export Scenarios

- successful export of the current live session
- successful export including git metadata
- successful export in a non-git workspace
- successful second export of the same session with incremental behavior
- successful export with a session name that requires filename sanitization
- successful export rendering with the agreed markdown section order
- successful export rendering with `## <Model Name> Assistant` and inline timestamps when available
- successful tool rendering using labeled subsections and fenced blocks

## Checkpoint Scenarios

- failed export does not advance checkpoint state
- corrupted checkpoint sidecar is handled safely
- unreadable checkpoint sidecar is handled safely
- sidecar JSON remains consistent after repeated successful exports
- composite cursor resumes from the correct next record without re-exporting prior content

## Degraded-Mode Scenarios

- inaccessible session history produces a natural-language failure
- unavailable optional metadata does not block the core export
- missing git context does not block the core export
- failure messaging follows the active conversation language
- omission messaging follows the active conversation language

## Cross-Platform Scenarios

- macOS Codex CLI export path behavior
- Linux Codex CLI export path behavior
- macOS Codex app export path behavior
- Windows Codex CLI export path behavior
- Windows Codex app export path behavior

## Validation Scenarios

- Daniel validates Windows behavior in real use
- trusted Windows users validate Windows behavior in real use
- validation findings are compared against the documented v1 environment targets

## Future Test Planning Rule

Negative-path tests are not limited to degraded-mode behavior alone.

They should also cover:

- checkpoint safety
- naming safety
- partial-data handling
- environment-specific behavior
