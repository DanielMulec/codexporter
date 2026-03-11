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
5. skill writes export file `-1`
6. skill writes checkpoint sidecar
7. skill informs user of success

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
6. skill renders next numbered markdown export
7. skill updates checkpoint sidecar
8. skill informs user of success

### Alternate flows

- sidecar is unreadable
- cursor validation fails
- there is no new content since the last export

### Postconditions

- new export file exists
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
4. skill stops without writing a false success artifact
5. skill informs user what failed, why, and next step if possible

### Alternate flows

- optional metadata is blocked but core export is still possible

### Postconditions

- no false success is reported
- checkpoint does not advance on failure
