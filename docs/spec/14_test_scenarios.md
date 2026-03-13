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
- `T-08`: successful export writes artifacts into the `codex_exports` subfolder in the current project root
- `T-09`: successful first export clearly communicates that the export was created for the current session and provides the file location
- `T-32`: successful export includes the required compact session metadata header when the metadata is available
- `T-37`: globally installed skill exports successfully in more than one project context without reinstallation
- `T-38`: globally installed skill writes export artifacts to the active project root rather than the installed skill directory

## Checkpoint Scenarios

- `T-10`: failed export does not advance checkpoint state
- `T-11`: corrupted checkpoint sidecar is handled safely
- `T-12`: unreadable checkpoint sidecar is handled safely
- `T-13`: sidecar JSON remains consistent after repeated successful exports
- `T-14`: composite cursor resumes from the correct next record without re-exporting prior content
- `T-15`: when there is no new exportable content since the previous successful checkpoint, no new export file is created and the user is informed
- `T-16`: successful repeated export clearly communicates that the export was incremental
- `T-34`: successful export writes the checkpoint sidecar as JSON with the required v1 schema fields
- `T-35`: later exports do not rewrite earlier markdown export artifacts for the same session
- `T-36`: cursor validation metadata mismatch stops export and preserves the prior checkpoint state

## Degraded-Mode Scenarios

- `T-17`: inaccessible session history produces a natural-language failure
- `T-18`: unavailable optional metadata does not block the core export
- `T-19`: failure messaging follows the active conversation language
- `T-20`: omission messaging follows the active conversation language
- `T-21`: when blocked access can be resolved, the user is guided toward the recovery step
- `T-22`: restricted-environment behavior explains what could not be accessed without claiming a false success
- `T-33`: export output excludes hidden reasoning and raw internal instruction payloads
- `T-39`: when the active project root cannot be determined, the skill fails clearly without writing export artifacts into the installed skill directory

## Cross-Platform Scenarios

- `T-23`: macOS Codex CLI satisfies the platform validation checklist for first export, incremental export, and failure communication
- `T-24`: Linux Codex CLI satisfies the platform validation checklist for first export, incremental export, and failure communication
- `T-25`: macOS Codex app satisfies the platform validation checklist for first export, incremental export, and failure communication
- `T-26`: Windows Codex CLI satisfies the platform validation checklist for first export, incremental export, and failure communication
- `T-27`: Windows Codex app satisfies the platform validation checklist for first export, incremental export, and failure communication

## Validation Scenarios

- `T-28`: Daniel validates Windows behavior in real use
- `T-29`: trusted Windows users validate Windows behavior in real use
- `T-30`: validation findings are compared against the documented v1 environment targets
- `T-31`: export filenames increment clearly across repeated exports of the same session

## Future Test Planning Rule

Negative-path tests are not limited to degraded-mode behavior alone.

They should also cover:

- checkpoint safety
- naming safety
- partial-data handling
- environment-specific behavior
