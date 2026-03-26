# Compact Mode Definition

## Status

- Phase: implementation planning
- Date: March 26, 2026
- Scope: approved initial compact-mode contract, not yet implemented

## Purpose

This document defines the first approved compact-mode behavior for the exporter.

It exists so compact mode is no longer just a general post-v1 idea.

## Product Position

Compact mode is an additive export option.

It is not:

- AI summarization
- AI classification
- an inferred narrative
- a second export identity

It is a deterministic, raw compaction of bulky visible workflow content.

## Invocation Rule

The intended user-facing compact-mode invocation is:

- `$export --compact`

That means:

- the same `export` skill remains the entry point
- plain `$export` keeps the current full-fidelity default behavior
- compact mode is selected explicitly through `--compact`

Source basis note:

- checked on March 26, 2026 against the official Codex skills and CLI docs
- those docs explicitly document `$skill` invocation
- they do not currently define a general skill-argument grammar in the same detail
- this repository still adopts `$export --compact` as its intended compact-mode contract based on observed Codex behavior and current product fit

## Core Compactness Rule

Compact mode must preserve the visible chronological workflow while removing raw bulk that is not necessary for quick human review.

Compact mode must keep:

- visible user messages
- visible assistant replies
- visible commentary or progress updates
- visible event markers
- tool chronology
- tool names
- concise command metadata that helps identify what ran
- short informative outputs such as concise errors, test summaries, `git status`, and `git diff --stat`

Compact mode must not preserve raw bulky payloads just because they were visible.

## Determinism Rule

Compact mode must remain raw and deterministic.

It must not:

- add inferred intent
- add a new explanation of why a tool was run
- use AI classification or AI summarization to reinterpret the session

Compact-mode summaries may use only facts directly derivable from:

- the visible chat history
- the visible tool-call payload
- the visible tool output payload

If a reason or intent statement already exists in the visible conversation, that visible text stays because it is part of the raw session record.

Compact mode still must not add a new explanatory layer on top of it.

## Required Compaction Rules

### Full file-read output

When a tool output contains full file contents or equivalent large readback content, compact mode must omit the raw body.

It should replace that body with a deterministic omission marker that preserves factual context such as:

- file path or file paths when derivable
- file count when derivable
- suppressed line count when derivable

### Raw patch payloads

Raw `apply_patch` bodies must always be omitted in compact mode.

Compact mode should preserve:

- that a patch was applied
- which files were touched when derivable from the patch header

### Raw diff bodies

Raw diff bodies may stay verbatim only when they are genuinely short.

The approved initial threshold is:

- keep verbatim only if the raw diff body is `<= 60` lines and touches `<= 2` files

If either threshold is exceeded, compact mode must omit the raw diff body and replace it with a deterministic summary.

That summary should prefer:

- changed file paths
- `+/-` counts when derivable safely

Examples:

- `src/thisisawesome.py +60 -5`
- `docs/spec/15_markdown_rendering_rules.md +3 -2`

If counts cannot be derived safely, compact mode should fall back to file paths only.

### Other bulky raw outputs

Large raw outputs outside the file-read, patch, or diff cases may also be compacted when they are obviously bulk-heavy and low-signal.

This includes examples such as:

- very large directory listings
- very large machine-shaped JSON blobs
- very large repeated command output dumps

The generic thresholding for those cases may be implementation-tuned later, but it must remain deterministic and must not conflict with the rules above.

## Compact-Mode Replacement Shape

Compact-mode omission markers should be factual and minimal.

Recommended examples:

- `Raw file contents omitted in compact mode.`
- `Raw patch omitted in compact mode.`
- `Raw diff omitted in compact mode.`

When additional deterministic detail is available, compact mode should append it in a compact list rather than re-expand the raw payload.

## Checkpoint And Identity Rule

Compact mode must not fork session identity, export numbering, or checkpoint semantics away from the canonical exporter flow.

The approved initial compact-mode design keeps:

- the same per-session export identity
- the same per-session numbering model
- the same checkpoint model

Compact mode changes rendering and content density, not the meaning of a successful export checkpoint.

## Constraint Reminder

Compact mode exists because the current full-fidelity exports can become extremely large in tool-heavy sessions.

It must still preserve enough factual workflow detail that the reader can understand:

- what happened
- which files were read or changed
- which commands ran
- which outputs were kept versus compacted

without preserving every raw payload verbatim.
