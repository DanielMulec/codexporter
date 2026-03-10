# Artifact Structure And Naming

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 contract

## Purpose

This document defines the v1 export artifact shape and naming rules.

## V1 Artifact Structure

V1 produces:

- one markdown export file per export invocation
- one sidecar checkpoint file for incremental export state

The markdown file is the user-facing artifact.

The sidecar file is implementation support state and should not be treated as the primary record.

## V1 Markdown Artifact Rule

V1 must default to a single markdown file for the exported session content.

No second markdown report is part of the default v1 export.

The markdown reading format is defined in `docs/spec/15_markdown_rendering_rules.md`.

## Naming Rule

The markdown export filename should use this structure:

`YYYYMMDD-HHMMSS-SESSIONNAME-<number>.md`

If no session name is available, use:

`YYYYMMDD-HHMMSS-SESSIONID-<number>.md`

Examples:

- `20260310-214500-Export-Spec-1.md`
- `20260310-214500-019cd4a0-80b5-7431-a1aa-3389c373381e-1.md`

## Naming Semantics

- `YYYYMMDD-HHMMSS` is the export timestamp, not necessarily the session start time
- `SESSIONNAME` is the best available session title or thread name when available
- `SESSIONID` is the stable fallback when no usable session name exists
- `<number>` is the export sequence number for that same session

## Export Sequence Rule

- first export for a session: `-1`
- second export for the same session: `-2`
- third export for the same session: `-3`

The sequence number is per session, not global across the project.

## Sanitization Rule

When using a session name in the filename:

- remove or replace path-unsafe characters
- keep the name readable
- avoid changing the session meaning more than necessary

## Future Compatibility Rule

Later versions may add additional artifacts, but they must not break the v1 expectation that:

- one primary markdown export exists per invocation
- the base naming structure remains recognizable

Any later added artifacts should derive from the same export identity rather than inventing an unrelated naming model.

This follows the project anti-refactor rule: later capabilities should extend the artifact set additively instead of redefining what the primary artifact is.
