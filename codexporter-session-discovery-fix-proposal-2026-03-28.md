# Codexporter Session Discovery Fix Proposal

Date: 2026-03-28

Audience: maintainer Codex instance

Scope: restore reliable current-session export when the live session rollout exists on disk but `state_5.sqlite` no longer has the matching `threads` row.

Check date for upstream docs that affect this proposal: 2026-03-28.

## Executive Summary

The export skill is failing for the current Windows session, but the exporter pipeline itself is not broken.

The actual split is:

1. Codex's local SQLite-backed state runtime on this Windows `.codex` home appears to have stopped initializing cleanly after a migration mismatch on March 26, 2026.
2. The `export` skill currently assumes that `state_5.sqlite.threads` is the only authoritative way to find the current session.

That assumption is too brittle.

The exporter already uses the rollout JSONL file as the transcript source once it has a valid session target. The failure is in session discovery, not in parsing, rendering, or compact-mode compaction.

The recommended fix is to make current-session discovery use the current thread id plus the rollout file as the canonical path, and to treat SQLite as a secondary index instead of the sole authority.

This proposal does not recommend teaching the skill to repair or mutate Codex's SQLite state.

## What Happened

### Local evidence

- The current live session id is `019d367b-7d72-7331-995b-2b4177361274`.
- The live rollout file exists at:
  `C:\Users\DanielMulecDatenpol\.codex\sessions\2026\03\28\rollout-2026-03-28T23-05-55-019d367b-7d72-7331-995b-2b4177361274.jsonl`
- The first `session_meta` record in that rollout reports:
  - `id = 019d367b-7d72-7331-995b-2b4177361274`
  - `cwd = C:\projekte\AI\sonstiges\codexporter`
  - `cli_version = 0.115.0-alpha.27`
- The same session id is present in:
  `C:\Users\DanielMulecDatenpol\.codex\session_index.jsonl`
- The same session id is absent from:
  `C:\Users\DanielMulecDatenpol\.codex\state_5.sqlite`

### State runtime warning

The local Codex log contains this warning on March 26, 2026 and again on March 27, 2026:

`failed to initialize state runtime ... migration 2 was previously applied but is missing in the resolved migrations`

The local `_sqlx_migrations` table still reports migration `2` as applied, along with versions `1` through `20`.

That combination strongly suggests a runtime-side migration mismatch in Codex's SQLite state layer for this Windows `.codex` home.

## What The Exporter Does Today

Current discovery flow:

1. Read `--session-id` or `CODEX_THREAD_ID`.
2. Query `state_5.sqlite.threads`.
3. Read `rollout_path` from the selected row.
4. Parse the rollout file and render the export.

That means the skill already relies on the rollout file for the real transcript content.

`state_5.sqlite` is currently just the discovery mechanism.

This is why explicit export of older sessions still works: those older sessions still have `threads` rows, which still point at valid rollout files.

## Why The Current Design Fails

The current design has one brittle assumption:

- if the current session is real, it must also exist in `state_5.sqlite.threads`

That assumption is not safe enough.

On this machine, the live session clearly exists and is exportable from disk, but the state index that the skill depends on stopped registering newer sessions after the runtime migration warning started appearing.

The consequence is a false negative:

- the skill says the current session does not exist
- but the current session rollout and metadata are present on disk

## ELI5 Explanation Of The Runtime Failure

Think of Codex as keeping two different kinds of records:

- a diary file for each conversation
- a card catalog that helps it quickly look conversations up

The rollout JSONL is the diary.
It contains the actual conversation events.

The SQLite database is part of the card catalog.
It stores structured lookup information such as thread ids, workspace paths, and rollout locations.

### What does "initializing a DB-backed state subsystem" mean?

It means Codex is starting up the internal part of itself that depends on that SQLite database.

In plain terms:

- open the database
- check that its structure is what the current Codex build expects
- make sure the needed tables and columns are there
- only then start using it for thread lookup, logs, agent jobs, and related runtime state

If that startup check fails, Codex avoids trusting the database.

### What is a migration framework?

A migration framework is the part that tracks database structure changes over time.

Imagine versioned setup steps such as:

1. create the `threads` table
2. add the `logs` table
3. add a new column
4. add a new index

Each step has a version number and a known definition.

The framework keeps two things in sync:

- what the database says has already been applied
- what the current application build says the valid migration steps are

### What did the migration framework "refuse"?

It refused to continue using the database because the history stored inside the database did not match the migration list that the current runtime resolved.

In effect, it said:

- "This database says migration 2 already happened."
- "But in the migration list I was given today, migration 2 does not exist."
- "That mismatch is dangerous, so I will stop rather than guess."

That is the safe behavior.
Guessing here could corrupt the DB or make the runtime read the wrong schema.

### What does "mismatch between the existing DB and the migration inventory" mean?

The existing DB is the actual SQLite file on disk.

The migration inventory is the list of schema-change steps that the current Codex build believes are valid and available.

The mismatch means:

- the file on disk remembers one history
- the currently running Codex build believes in a different history

That usually points to one of these classes of problems:

- a build upgrade or downgrade where the bundled migration set changed unexpectedly
- a packaging bug where the runtime resolved the wrong migration bundle
- two different Codex variants sharing one `.codex` state DB but not agreeing on the exact migration set

This repo cannot prove which of those happened.
It can only observe the symptom and design the exporter to be less fragile when that symptom occurs.

## Recommended Fix

### Recommendation

Make `CODEX_THREAD_ID` plus rollout discovery the canonical current-session path.

Do not keep "SQLite first, rollout second" as the current-session design.

That would keep the exporter dependent on a state index that is not the real transcript source and is outside this repo's control.

### Proposed current-session algorithm

If an explicit session id is available from `--session-id` or `CODEX_THREAD_ID`:

1. Search `CODEX_HOME/sessions/**/rollout-*-<session_id>.jsonl`.
2. If no matching rollout exists, fail clearly.
3. Parse only the first `session_meta` record.
4. Verify `payload.id == session_id`.
5. Verify normalized `payload.cwd == invocation_cwd`.
6. Build the `ThreadRecord` directly from `session_meta` plus the rollout path.
7. Continue with the existing parse and render pipeline.

That makes the authoritative current-session identity come from the authoritative current-session id and the authoritative transcript file.

### Proposed no-session-id behavior

If no explicit session id is available:

1. Scan recent rollout files.
2. Parse only `session_meta`.
3. Filter by normalized `cwd`.
4. Sort by session timestamp.
5. If exactly one candidate remains, use it.
6. If more than one remains, fail closed as ambiguous.

`session_index.jsonl` can be used as an accelerator if useful, but it should not be the sole trust anchor because it does not contain the full validation surface that the rollout header does.

### SQLite's new role

SQLite should become optional supporting metadata, not the only gatekeeper.

Reasonable uses:

- legacy/secondary metadata fill-in when present
- heuristic assistance when no explicit session id exists
- diagnostics when a rollout exists but the state index is stale

Unreasonable use:

- treating a missing `threads` row as proof that the current session does not exist

## Why This Is The Right Shape

This repo's hard-cut policy prefers one canonical current-state code path over compatibility glue.

That means the goal should not be:

- "support both the old SQLite world and the new rollout world forever"

The goal should be:

- "use the real current transcript source as the canonical session-discovery path"

That source is the rollout file once the current thread id is known.

This keeps the exporter aligned with the artifact it actually exports and avoids turning the skill into a repair tool for another system's database.

## What Not To Do

### Do not mutate Codex's SQLite DB from the skill

The exporter should not insert missing `threads` rows or try to heal `_sqlx_migrations`.

Why:

- it is outside the skill's ownership boundary
- it risks corrupting a runtime DB owned by Codex
- it hides a real upstream state-runtime problem

### Do not block the fix on solving the Codex runtime issue first

Even if the Windows `.codex` state DB is later repaired, the current exporter assumption will remain fragile.

The exporter should be robust against stale or unavailable state indexes because the transcript file is what it truly needs.

### Do not add a broad silent fallback maze

The skill should not try many opaque guesses and export whichever looks plausible.

It should:

- validate the requested thread id and workspace explicitly
- fail fast when validation does not line up
- explain what was missing or inconsistent

## Diagnostic Improvements

The current user-facing errors blame the user for not running from the active project session.

That is misleading in this incident.

Diagnostics should instead distinguish:

- no current thread id available
- thread id available but no rollout file found
- rollout file found but workspace does not match
- rollout file found and valid, but SQLite index is missing or stale

That last message would have exposed the real problem immediately.

## Test Plan

Add a regression fixture that models this exact incident:

- live rollout file exists
- `session_index.jsonl` contains the current session id
- `state_5.sqlite` is present but missing the thread row
- current `cwd` matches the rollout header

Then add tests for:

1. `$export` succeeds in that state.
2. `$export --compact` succeeds in that state.
3. explicit wrong-workspace targeting still fails.
4. ambiguous same-workspace selection without a thread id still fails closed.
5. diagnostics distinguish rollout-missing from index-stale conditions.

## Separate Track Outside This Repo

The Windows `.codex` home likely has a real Codex runtime-state issue that should be reported upstream with:

- the exact warning from `codex-tui.log`
- the local `_sqlx_migrations` contents
- the observation that rollout persistence continued while `threads` stopped updating

That is a Codex runtime investigation.
It should not block the exporter fix.

## Acceptance Criteria

This proposal should be considered implemented only when:

1. the active session exports successfully when `CODEX_THREAD_ID` is present and the rollout exists, even if `state_5.sqlite` is stale
2. full and compact export share the same corrected discovery path
3. workspace-mismatch protection still fails closed
4. ambiguity without a thread id still fails closed
5. user-facing errors identify stale session indexing accurately
6. the repo has automated regression coverage for the stale-SQLite/live-rollout case

## Sources

Official docs checked on 2026-03-28:

- OpenAI Codex config reference: `https://developers.openai.com/codex/config-reference/`
- OpenAI Codex Windows app docs: `https://developers.openai.com/codex/app/windows/`
- SQLx migration error source: `https://docs.rs/crate/sqlx-core/latest/source/src/migrate/error.rs`

Local evidence checked on 2026-03-28:

- `C:\Users\DanielMulecDatenpol\.codex\log\codex-tui.log`
- `C:\Users\DanielMulecDatenpol\.codex\state_5.sqlite`
- `C:\Users\DanielMulecDatenpol\.codex\session_index.jsonl`
- `C:\Users\DanielMulecDatenpol\.codex\sessions\2026\03\28\rollout-2026-03-28T23-05-55-019d367b-7d72-7331-995b-2b4177361274.jsonl`
