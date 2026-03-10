# Assumptions And Constraints

## Status

- Phase: analysis and discussion
- Date: March 10, 2026

## Product Assumptions

- Codex persists enough local session data to enable a useful export flow.
- The skill can rely on visible session artifacts more safely than on internal or hidden reasoning data.
- A raw export and a derived report are separate product concerns and should not be conflated.
- Repeated exports in the same session are common enough to justify checkpoint behavior.
- Markdown is the primary output format for v1.
- Users value transparency into tool activity, file work, and git state alongside the conversation itself.

## Platform Assumptions And Constraints

- Current platform support must be defined based on actual Codex product support, not aspirational support.
- Codex CLI and Codex app may expose different runtime capabilities and storage layouts.
- Sandboxing and approval behavior may limit file access, especially outside the workspace.
- A skill should not assume it can always self-upgrade its privileges without user interaction or platform support.
- Git context may or may not exist for a given session.
- Export behavior must remain useful even when some optional data sources are unavailable.

## Initial UX Principles

- The raw export is the source record.
- Optional AI summarization must never replace the source record.
- Repeated export behavior must be predictable.
- Degraded-mode behavior must be explicit, not silent.
- The user should not need to understand internal Codex storage details to use the skill successfully.

## Source Notes

This document is based on:

- the March 10, 2026 project discussion
- current Codex platform constraints checked on March 10, 2026
- local verification that Codex persists session data on disk in the current environment
