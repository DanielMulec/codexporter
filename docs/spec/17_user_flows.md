# User Flows

## Purpose

This document defines the step-by-step flows for `$export`.

## Flow F-01: First Export

### Preconditions

- user is in an active Codex session
- current session history is accessible

### Main flow

1. user invokes `$export`
2. skill identifies the current session
3. skill reads exportable session records
4. skill renders the markdown export
5. skill writes export file `-1` into the `codex_exports` subfolder in the current project root
6. skill writes checkpoint sidecar into the `codex_exports` subfolder
7. skill informs user of success and provides the file name and file path

### Alternate flows

- optional metadata is unavailable
- session name is unavailable

### Postconditions

- one markdown export file exists
- one checkpoint sidecar exists
- user is informed of success

## Flow F-02: Repeated Incremental Export

### Preconditions

- user is in the same session
- at least one prior successful export exists
- checkpoint sidecar exists

### Main flow

1. user invokes `$export`
2. skill identifies current session
3. skill loads checkpoint sidecar
4. skill validates cursor state
5. skill reads only new records after the checkpoint
6. if there is no new exportable content, skill does not create a new export file and informs the user directly
7. if there is new exportable content, skill renders the next numbered markdown export
8. skill updates checkpoint sidecar only after a successful export
9. if a new export file was created, skill informs the user of success, that the export was incremental, and provides the file name and file path

### Alternate flows

- sidecar is unreadable
- cursor validation fails
- there is no new content since the last export

### Postconditions

- if new exportable content exists, a new export file exists
- if no new exportable content exists, no new export file is created
- prior export files remain unchanged
- checkpoint advances only on success

## Flow F-03: Blocked Export

### Preconditions

- user invokes `$export`
- required session access is not available

### Main flow

1. user invokes `$export`
2. skill attempts to resolve current session data
3. skill detects blocked or unavailable required data
4. skill determines whether the problem can be resolved through an available user action or environment change
5. if a recovery step is available, skill guides the user toward that recovery step
6. if required access becomes available, the skill continues through the first-export or repeated-export flow as appropriate
7. if required access does not become available, skill stops without writing a false success artifact
8. skill informs the user what failed, why, and what to do next if that can be stated responsibly

### Alternate flows

- optional metadata is blocked but core export is still possible
- required access remains unavailable after the guidance step

### Postconditions

- if required access remains unavailable, no false success is reported
- checkpoint does not advance on failure
- if required access is restored, the export continues under the appropriate normal flow

## Flow F-04: Global Install Across Projects

### Preconditions

- the skill is installed globally
- user is in an active Codex session

### Main flow

1. user invokes `$export`
2. skill resolves the active project root from the current session or workspace context
3. skill confirms that the installed skill directory is not the export target
4. skill continues through the first-export or repeated-export flow as appropriate
5. skill writes export artifacts into the active project's `codex_exports` subfolder

### Alternate flows

- user has moved to a different project context since the last export
- the active project root cannot be determined responsibly

### Postconditions

- the same installed skill can be used across project contexts without reinstallation
- export destination stays tied to the active project root
- if the active project root cannot be determined, no export artifact is written into the installed skill directory

## Flow F-05: Explicit Compact Export

### Preconditions

- user is in an active Codex session
- current session history is accessible
- user explicitly requests `$export --compact`

### Main flow

1. user invokes `$export --compact`
2. skill identifies the current session
3. skill reads exportable session records
4. skill applies the compact render profile to the exportable entry stream
5. skill preserves the visible chronological workflow while replacing qualifying bulky raw tool payloads with deterministic omission markers
6. skill writes the markdown export into the `codex_exports` subfolder in the current project root
7. skill writes the checkpoint sidecar into the same `codex_exports` subfolder
8. skill records `Render profile: compact` in the export metadata
9. skill informs user that the compact export succeeded and provides the file name and file path

### Alternate flows

- optional metadata is unavailable
- session name is unavailable
- a short qualifying raw diff remains verbatim because it is below the compact threshold

### Postconditions

- one markdown export file exists
- one checkpoint sidecar exists
- the export preserves visible chronology while compacting qualifying bulky raw payloads
- the export metadata identifies the compact render profile

## Flow F-06: Shared Compact And Full Checkpoint History

### Preconditions

- user is in the same session
- at least one prior successful export exists
- checkpoint sidecar exists
- the prior export may have used either the full or compact render profile

### Main flow

1. user invokes `$export --compact` or plain `$export`
2. skill identifies the current session
3. skill loads the existing checkpoint sidecar
4. skill validates the canonical cursor state
5. skill reads only new records after the checkpoint
6. if there is no new exportable content, skill does not create a new export file and informs the user directly
7. if there is new exportable content, skill renders the next numbered export using the requested render profile
8. skill updates the same checkpoint sidecar only after a successful export
9. if a new export file was created, skill informs the user of success, whether the export was incremental, and where the file was written

### Alternate flows

- sidecar is unreadable
- cursor validation fails
- there is no new content since the last export

### Postconditions

- compact and full exports share one per-session numbering model
- compact and full exports share one checkpoint history
- if no new exportable content exists, no new export file is created
- checkpoint advances only on success
