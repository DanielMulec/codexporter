# Export Data Contract

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 contract

## Purpose

This document defines what the v1 export must include, may include, and must exclude.

The goal is to create a stable export contract for v1 without tying the product to internal-only or high-volatility data.

## V1 Export Contract

### Required session metadata

- session identifier
- session start timestamp when available
- current working directory when available
- originator or source when available
- model name when available

### Required visible conversation and workflow content

- user messages
- assistant visible final answers
- assistant visible commentary or progress updates when available
- task started markers when available
- task complete markers when available
- tool invocations when available
- tool outputs when available

Visible git-related content that appeared in the chat, such as tool output, remains part of the export because it is part of the visible session history.

## Optional v1 fields

- model provider
- CLI version or app version when available
- timezone
- current date
- approval policy
- sandbox policy
- token counts

These fields may be included if they are reliably accessible and can be presented without cluttering the markdown output.

## Excluded from v1

- hidden chain-of-thought
- encrypted reasoning payloads
- dedicated structured session-level git metadata such as `session_meta.git`
- raw internal instruction payloads such as full base, developer, or user instruction dumps
- rate-limit internals
- internal-only event details that are not clearly useful to end users
- unstable internal fields that cannot yet be treated as a supported contract

## Contract Selection Criteria

A field is a valid part of the supported v1 export contract only if it is:

- human-meaningful
- useful in the exported markdown
- reasonably stable across supported environments
- not obviously internal-only
- not hidden reasoning

## V1 Output Principle

The v1 export contract should prefer visible workflow truth over maximal raw data collection.

That means:

- include what the user can meaningfully review
- exclude what is internal, hidden, noisy, or unstable

## Default Output Rule

The default markdown export should stay close to what the user visibly experienced in the chat.

That means the default output should prioritize:

- visible user messages
- visible assistant replies
- visible commentary or progress updates
- visible tool calls and outputs
- a compact session header metadata block

Optional environment metadata should stay minimal in the default export view.

## Timestamp Resilience Rule

If source timestamps are available but the environment cannot resolve the preferred named timezone, the export may render those timestamps in UTC.

Missing timezone database support must not by itself block an otherwise valid core export.

## Future Compatibility Rule

The export pipeline should be structured so that new optional sections can be added later without changing the meaning of existing v1 sections.

This means later additions should generally be:

- additive
- optional
- clearly labeled

Later features should not require rewriting the v1 source-record semantics.

This follows the project anti-refactor rule: post-v1 capabilities should be added as optional stages or optional artifacts, not by redefining the core v1 export contract.
