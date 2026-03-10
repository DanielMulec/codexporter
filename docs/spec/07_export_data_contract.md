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

### Required git metadata when available

- repository URL
- branch name
- commit hash

If git metadata is unavailable, the export must still succeed and explain the omission only when user-facing clarification is useful.

### Required visible conversation and workflow content

- user messages
- assistant visible final answers
- assistant visible commentary or progress updates when available
- task started markers when available
- task complete markers when available
- tool invocations when available
- tool outputs when available

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

## Future Compatibility Rule

The export pipeline should be structured so that new optional sections can be added later without changing the meaning of existing v1 sections.

This means later additions should generally be:

- additive
- optional
- clearly labeled

Later features should not require rewriting the v1 source-record semantics.
