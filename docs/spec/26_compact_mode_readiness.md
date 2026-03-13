# Compact Mode Readiness

## Status

- Phase: analysis and discussion
- Date: March 13, 2026
- Scope: implementation-readiness assessment for post-v1 compact export modes

## Purpose

This document records how close the current implementation is to supporting compact export modes as an additive post-v1 feature.

It exists to answer a specific design-health question:

- did v1 actually preserve the anti-refactor goal for later compact-mode work

## Headline Assessment

Current assessment:

- approximately `75%` to `85%` of the way to the anti-refactor goal for compact export modes

Interpretation:

- the current implementation already has the right major boundaries
- compact mode does not currently look like a rewrite
- compact mode does still require deliberate extension work before it becomes a clean first-class option

## Why The Current Implementation Is In Good Shape

The current code already separates the main responsibilities in a way that supports additive extension:

- session discovery in `skills/codexporter/codexporter/session_store.py`
- rollout parsing in `skills/codexporter/codexporter/rollout_parser.py`
- checkpoint logic in `skills/codexporter/codexporter/checkpoint.py`
- export orchestration in `skills/codexporter/codexporter/service.py`
- markdown rendering in `skills/codexporter/codexporter/renderer.py`

This matches the intended v1 pipeline shape:

- session data collection
- export normalization
- primary markdown rendering
- checkpoint state management
- optional future post-processing

That separation is the main reason compact mode still looks additive.

## What This Means For Compact Mode

The current architecture suggests that compact mode can probably be added by introducing:

- a new export or render option at the public surface
- a filtering, collapsing, or summarization step between parsed entries and markdown rendering
- renderer behavior that changes based on the selected output mode

That means compact mode should be able to evolve without changing:

- session discovery
- export identity
- export numbering
- sidecar semantics
- checkpoint semantics

This is the strongest sign that the anti-refactor rule is mostly holding.

## Strong Areas

### 1. Service orchestration is already clean enough

`skills/codexporter/codexporter/service.py` already does the high-level pipeline work in a clear order:

- resolve the current session
- parse the rollout
- determine incremental scope
- render the export
- write the markdown and sidecar

Compact mode can likely be inserted as a new option in this pipeline without redesigning the pipeline itself.

### 2. Checkpointing is already isolated

`skills/codexporter/codexporter/checkpoint.py` is already responsible for:

- sidecar loading
- sidecar validation
- sidecar building
- sidecar serialization

Compact mode should not need to alter that logic, which is exactly what the spec intended.

### 3. Parsed export entries already form a stable intermediate layer

`skills/codexporter/codexporter/models.py` and `skills/codexporter/codexporter/rollout_parser.py` already produce structured `ExportEntry` values.

That means later compact-mode logic can act on a normalized entry stream instead of having to parse raw JSONL again.

## Main Weakness

The main weakness is that markdown rendering is still a single fixed path.

`skills/codexporter/codexporter/renderer.py` currently has:

- one render function
- one fixed formatting policy
- one fixed verbosity level
- no explicit render profile or compactness model

This is not a design failure, but it does mean that:

- adding one simple compact mode should be straightforward
- adding multiple compactness levels cleanly will require a new options or profile abstraction

## What Is Still Missing Before Compact Mode Becomes Truly First-Class

The following additions are still likely needed later:

### 1. A compactness option model

Examples of future directions:

- `full`
- `compact`
- later possibly `minimal`, `audit`, or other explicit modes

These are only examples, not approved product decisions.

### 2. A transformation layer between parsed entries and rendering

That future layer would likely handle actions such as:

- excluding selected entry kinds
- truncating long tool payloads
- collapsing repeated workflow details
- replacing raw detail with a compact summary line

### 3. Renderer options

`renderer.py` will likely need an explicit render-options object or profile model so rendering policy is no longer hardcoded as one shape only.

### 4. Public invocation surface for mode selection

`skills/codexporter/codexporter/cli.py` currently exposes the v1 public surface.

Later compact mode will likely need:

- an explicit flag
- or another approved user-facing invocation mechanism

without changing the default v1 export behavior.

## Confidence Level

High confidence:

- compact mode can be added without redefining session export identity
- compact mode can be added without changing checkpoint behavior
- compact mode can be added without changing export numbering

Moderate caution:

- multiple compactness levels will need a better rendering-policy abstraction
- semantic compactness, such as summary-style tool condensation, may require one additional intermediate processing layer

## Bottom Line

Compact mode currently looks like:

- a localized extension

not like:

- a major rewrite

So the anti-refactor goal is mostly being achieved in the current implementation.

The main future work is not architectural rescue.

The main future work is to turn rendering and content-selection policy into explicit, configurable abstractions.
