# Compact Mode Readiness

## Status

- Phase: implementation and validation
- Date: March 27, 2026
- Scope: readiness assessment plus implementation outcome for the first compact export profile

## Purpose

This document records how the v1 architecture held up when the first compact export profile was actually implemented.

It exists to answer a specific design-health question:

- did v1 actually preserve the anti-refactor goal for later compact-mode work

## Headline Assessment

Current assessment:

- the anti-refactor goal held for the first compact profile

Interpretation:

- the compact profile landed as a localized extension rather than a rewrite
- the existing boundaries were strong enough to absorb the new render profile cleanly
- future expansion still needs deliberate abstraction work, but the initial mode is now first-class

## Why The Current Implementation Is In Good Shape

The current code already separates the main responsibilities in a way that supports additive extension:

- session discovery in `skills/export/codexporter/session_store.py`
- rollout parsing in `skills/export/codexporter/rollout_parser.py`
- checkpoint logic in `skills/export/codexporter/checkpoint.py`
- export orchestration in `skills/export/codexporter/service.py`
- markdown rendering in `skills/export/codexporter/renderer.py`

This matches the intended v1 pipeline shape:

- session data collection
- export normalization
- primary markdown rendering
- checkpoint state management
- optional future post-processing

That separation is the main reason compact mode still looks additive.

## What This Means For Compact Mode

The readiness assessment proved accurate.

The implemented compact profile now uses:

- a new explicit render-profile option at the public surface
- a deterministic compaction step between parsed entries and markdown rendering
- renderer metadata that records which render profile produced the artifact

The approved initial compact-mode contract now lives in `docs/spec/27_compact_mode_definition.md`.

The implemented first profile did not require changing:

- session discovery
- export identity
- export numbering
- sidecar semantics
- checkpoint semantics

This is the strongest sign that the anti-refactor rule held for the first expansion.

## Strong Areas

### 1. Service orchestration is already clean enough

`skills/export/codexporter/service.py` already does the high-level pipeline work in a clear order:

- resolve the current session
- parse the rollout
- determine incremental scope
- render the export
- write the markdown and sidecar

Compact mode landed in this pipeline without redesigning the pipeline itself.

### 2. Checkpointing is already isolated

`skills/export/codexporter/checkpoint.py` is already responsible for:

- sidecar loading
- sidecar validation
- sidecar building
- sidecar serialization

Compact mode did not alter that logic, which is exactly what the spec intended.

### 3. Parsed export entries already form a stable intermediate layer

`skills/export/codexporter/models.py` and `skills/export/codexporter/rollout_parser.py` already produce structured `ExportEntry` values.

That meant compact-mode logic could act on a normalized entry stream instead of having to parse raw JSONL again.

## What Landed

The first implementation added:

- an explicit render-profile split between `full` and `compact`
- a deterministic compaction module between parsed entries and rendering
- CLI-level `--compact` support on the same `export` skill surface
- renderer metadata that records the render profile
- automated coverage for compact CLI invocation, compaction rules, short-diff preservation, and compact/full checkpoint sharing

## What Still Remains For Future Expansion

The current implemented public mode split is:

- `full`
- `compact`

Later modes such as `minimal`, `audit`, or other explicit levels remain undecided.

The current compaction layer already handles:

- always omit raw `apply_patch` bodies
- omit full file-read bodies and replace them with deterministic omission markers
- keep raw diff bodies only when they are `<= 60` lines and touch `<= 2` files
- summarize larger diffs with changed file paths and `+/-` counts when derivable
- compact very large directory listings and large machine-shaped JSON outputs when they cross the generic threshold
- preserve raw chronology without AI classification or inferred explanation

Future expansion may still need:

- a more explicit render-options object if more than two profiles are added
- richer deterministic compaction heuristics if new bulk classes prove important
- direct real-session compact-mode validation notes in `docs/validation/` when future shared exporter changes warrant that evidence

## Confidence Level

High confidence:

- compact mode was added without redefining session export identity
- compact mode was added without changing checkpoint behavior
- compact mode was added without changing export numbering

Moderate caution:

- multiple compactness levels will need a better rendering-policy abstraction
- semantic compactness, such as summary-style tool condensation, may require one additional intermediate processing layer

## Bottom Line

Compact mode now looks like:

- a localized extension

not like:

- a major rewrite

So the anti-refactor goal was achieved for the first compact-mode implementation.

The main future work is not architectural rescue.

The main future work is threshold tuning or explicit new render-profile design, not rescuing the current architecture.
