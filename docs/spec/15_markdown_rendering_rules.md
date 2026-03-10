# Markdown Rendering Rules

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 contract

## Purpose

This document defines the exact reading format for the primary markdown export artifact.

## Rendering Principle

The markdown export should read like the current Codex chat in chronological order.

It should prioritize what the user visibly experienced in the session.

## Section Order

The primary markdown artifact should use this order:

1. `# Session Export`
2. session metadata block
3. `## Conversation`
4. chronological event stream
5. `## Git Context` when available
6. `## Export Metadata`

## Message Heading Rules

- user messages should use `## User`
- assistant messages should use `## <Model Name> Assistant`
- commentary or progress updates should use `## <Model Name> Commentary`
- timestamps should appear inline in the heading when available

Example:

`## gpt-5.4 Assistant · 2026-03-10 22:14:31 CET`

## Chronological Rule

The conversation and workflow stream should be rendered in chronological order.

Tool-related content should appear where it happened in the flow, not in a separate detached appendix.

## Tool Call Rendering Rule

Tool calls should be rendered as labeled subsections with fenced blocks.

Recommended structure:

- heading with tool name and timestamp
- arguments block
- output block when available

Example shape:

- `## Tool Call · exec_command · 2026-03-10 22:14:40 CET`
- `**Arguments**`
- fenced JSON block
- `## Tool Output · exec_command · 2026-03-10 22:14:41 CET`
- fenced text block

## Formatting Rule

- use headings and fenced blocks rather than dense raw dumps
- keep the artifact readable in plain markdown
- prefer clarity over compactness when the two conflict

## Future Compatibility Rule

Later versions may add optional sections or optional artifacts, but they should preserve the v1 reading model:

- chronological
- user-visible-first
- clearly labeled

This follows the project anti-refactor rule.
