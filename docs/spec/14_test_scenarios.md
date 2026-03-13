# Test Scenarios

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 test planning draft

## Purpose

This document lists the main v1 test scenarios implied by the current specification.

## Successful Export Scenarios

- `T-01`: successful export of the current live session
- `T-02`: successful export in a non-git workspace
- `T-03`: successful second export of the same session with incremental behavior
- `T-04`: successful export with a session name that requires filename sanitization
- `T-05`: successful export rendering with the agreed markdown section order
- `T-06`: successful export rendering with `## <Model Name> Assistant` and inline timestamps when available
- `T-07`: successful tool rendering using labeled subsections and fenced blocks
- `T-08`: successful export writes artifacts into the `codex_exports` subfolder in the current project repository

## Checkpoint Scenarios

- `T-09`: failed export does not advance checkpoint state
- `T-10`: corrupted checkpoint sidecar is handled safely
- `T-11`: unreadable checkpoint sidecar is handled safely
- `T-12`: sidecar JSON remains consistent after repeated successful exports
- `T-13`: composite cursor resumes from the correct next record without re-exporting prior content
- `T-14`: when there is no new exportable content since the previous successful checkpoint, no new export file is created and the user is informed

## Degraded-Mode Scenarios

- `T-15`: inaccessible session history produces a natural-language failure
- `T-16`: unavailable optional metadata does not block the core export
- `T-17`: failure messaging follows the active conversation language
- `T-18`: omission messaging follows the active conversation language
- `T-19`: when blocked access can be resolved, the user is guided toward the recovery step

## Cross-Platform Scenarios

- `T-20`: macOS Codex CLI export path behavior
- `T-21`: Linux Codex CLI export path behavior
- `T-22`: macOS Codex app export path behavior
- `T-23`: Windows Codex CLI export path behavior
- `T-24`: Windows Codex app export path behavior

## Validation Scenarios

- `T-25`: Daniel validates Windows behavior in real use
- `T-26`: trusted Windows users validate Windows behavior in real use
- `T-27`: validation findings are compared against the documented v1 environment targets

## Future Test Planning Rule

Negative-path tests are not limited to degraded-mode behavior alone.

They should also cover:

- checkpoint safety
- naming safety
- partial-data handling
- environment-specific behavior
