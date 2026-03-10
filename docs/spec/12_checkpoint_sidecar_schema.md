# Checkpoint Sidecar Schema

## Status

- Phase: analysis and discussion
- Date: March 10, 2026
- Scope: v1 contract

## Purpose

This document defines the v1 sidecar checkpoint format.

The sidecar exists to support incremental export behavior without mutating prior markdown artifacts.

## Format Rule

The v1 checkpoint sidecar should be a JSON file.

It should not be:

- a database file
- a binary format
- a hidden opaque implementation-specific state store

## Why JSON Is Preferred

- easy to inspect
- easy to debug
- easy to keep cross-platform
- low refactor pressure
- additive evolution is straightforward through versioned keys

## Required v1 fields

- `schema_version`
- `session_id`
- `session_name` when available
- `export_sequence`
- `last_exported_record_index`
- `last_exported_event_timestamp`
- `last_exported_turn_id` when available and useful
- `exported_artifacts`
- `created_at`
- `updated_at`

## Field Intent

- `schema_version`: supports additive evolution without redefining prior sidecar semantics
- `session_id`: ties the checkpoint state to one session
- `session_name`: human-friendly metadata when available
- `export_sequence`: tracks `-1`, `-2`, `-3` style export numbering
- `last_exported_record_index`: the primary resume cursor for v1
- `last_exported_event_timestamp`: validation metadata for the primary cursor
- `last_exported_turn_id`: optional extra validation anchor when session structure exposes it reliably
- `exported_artifacts`: records the produced file identities
- `created_at` and `updated_at`: support debugging and recovery

## Cursor Rule

The v1 sidecar should use a composite cursor.

That means:

- `last_exported_record_index` is the primary resume marker
- `last_exported_event_timestamp` is validation metadata
- `last_exported_turn_id` is optional extra validation metadata

This choice is intended to reduce the risk of duplicate or missed exports in long-running sessions with multiple incremental exports.

## Schema Evolution Rule

Future versions may add optional fields, but they should do so additively.

They should not require redefining:

- the meaning of `session_id`
- the meaning of `export_sequence`
- the meaning of a successful checkpoint cursor

This follows the project anti-refactor rule.
