# Post-V1 Deferrals

## Status

- Phase: analysis and discussion
- Date: March 10, 2026

## Purpose

This document records what is intentionally deferred beyond v1, why it is deferred, what the consequence of that deferral is, and how v1 should be designed so those features can be added later without major refactoring.

## Deferred Items

### AI-derived reporting

Deferred status:

- post-v1

What it is:

- an additional AI-written report derived from the raw export, such as a handoff summary, worklog, or retrospective

Why it is deferred:

- the core v1 requirement is the faithful raw export
- the raw export is easier to validate than an AI-written derivative
- shipping both at once increases scope and validation burden

Consequence of deferral:

- v1 users get the source record but not an automatic summary artifact

Integration rule for later:

- reporting must be layered on top of the raw export pipeline, not mixed into the source-record generation path
- later report generation should consume stable exported data rather than requiring a redesign of the core exporter

### AI classification

Deferred status:

- post-v1

What it is:

- structured labeling or interpretation of a session, such as workflow type, topic, outcome, or risk classification

Why it is deferred:

- it is less directly valuable than the raw export
- it depends on having a trustworthy raw export and artifact identity first
- it introduces extra model-behavior validation questions

Consequence of deferral:

- v1 exports do not include structured AI labels or classifier output

Integration rule for later:

- classification should be an additive post-processing step keyed to the same export identity
- it must not require changing the meaning of the v1 markdown source record

### Multi-file user-facing export bundles

Deferred status:

- post-v1

What it is:

- multiple user-facing export artifacts produced by default for one invocation

Why it is deferred:

- one markdown file is the narrowest clear v1 behavior
- multiple default artifacts introduce extra naming, packaging, and UX complexity

Consequence of deferral:

- v1 favors clarity over richer artifact sets

Integration rule for later:

- additional artifacts should derive from the same base export identity and sequence number
- later bundle additions must remain compatible with the existing v1 filename model

### Compact export modes

Deferred status:

- post-v1

What it is:

- optional export modes that reduce output size by omitting, collapsing, or summarizing selected content classes while preserving the main export identity

Why it is deferred:

- the v1 priority is a faithful source-record export
- compact-mode behavior introduces product and UX decisions that are not yet approved
- we do not yet know which compactness levels or content-reduction options should be offered

Consequence of deferral:

- v1 exports may become very large for long, tool-heavy sessions

Evidence note:

- this concern is documented in `docs/spec/25_export_length_analysis.md`, which records why a real first export reached `29,741` lines

Integration rule for later:

- compact modes must be additive export options rather than a redefinition of the default v1 export semantics
- compact modes must not break the base export identity, numbering model, or checkpoint behavior
- if multiple compactness levels are introduced later, they should be documented explicitly rather than inferred

### Richer internal metadata coverage

Deferred status:

- post-v1

What it is:

- broader export of optional or internal metadata beyond the current supported v1 contract

Why it is deferred:

- not all fields are clearly stable or useful enough for the first supported contract
- exporting too much too early increases coupling to internal platform details

Consequence of deferral:

- v1 intentionally excludes some data that may exist locally

Integration rule for later:

- new metadata should be added as optional labeled sections
- existing v1 sections should not need to be redefined or renamed

### Structured session-level git metadata

Deferred status:

- post-v1

What it is:

- dedicated structured session metadata such as `session_meta.git` containing repository URL, branch, or commit snapshot fields when present

Why it is deferred:

- it is not foundational to exporting the visible chat and workflow history
- it appears to be optional and session-level rather than the main event stream
- visible git-related tool output is already covered by the visible-session export model

Consequence of deferral:

- v1 does not surface structured session-level git metadata as a dedicated export section

Integration rule for later:

- if added later, it should appear as an optional labeled metadata section
- it must not redefine the core visible-history export model

### Hidden reasoning export

Deferred status:

- not planned for v1 and not assumed to be supported later

What it is:

- exporting non-visible model chain-of-thought or encrypted reasoning content

Why it is deferred:

- it is not part of the visible workflow record
- it is not a stable or appropriate v1 contract surface

Consequence of deferral:

- the export remains a visible-workflow source record, not a hidden-thought dump

Integration rule for later:

- the product should not be architected around the assumption that hidden reasoning will become available

## Architectural Constraint For All Deferred Items

V1 should be implemented as a pipeline with clear boundaries between:

- session data collection
- export normalization
- primary markdown rendering
- checkpoint state management
- optional future post-processing

This boundary design matters because it minimizes refactor pressure when post-v1 features are added.

## Anti-Refactor Rule

Deferred features should be integrated later by adding optional stages or optional artifacts, not by rewriting the core v1 export semantics.

If a future feature requires redefining:

- what a session export is
- what the primary artifact is
- how checkpoints work

then v1 was shaped incorrectly.
