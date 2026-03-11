# User-Side Acceptance Criteria

## Purpose

This document defines the user-observable acceptance criteria for `$export`.

## AC-01: Current Session Export

- Related stories: US-01
- Criterion:
  - When the user invokes `$export`, the skill exports the current live session, not another session.
- Observable evidence:
  - The created export contains the current thread's visible content.

## AC-02: Markdown Artifact

- Related stories: US-01, US-03
- Criterion:
  - The export is created as a markdown file.
- Observable evidence:
  - The produced file is a `.md` file and is readable as markdown.

## AC-03: Visible-Chat-First Rendering

- Related stories: US-03
- Criterion:
  - The default export stays close to what the user visibly experienced in chat.
- Observable evidence:
  - The export shows visible user messages, assistant replies, commentary, and tool activity in chronological order.

## AC-04: Repeated Export Does Not Duplicate Prior Content

- Related stories: US-02
- Criterion:
  - A later export of the same session does not repeat content that was already exported successfully before.
- Observable evidence:
  - Previously exported content does not reappear in the next incremental export file.

## AC-05: Clear Failure Messaging

- Related stories: US-04
- Criterion:
  - If export fails, the user is informed directly what failed and why.
- Observable evidence:
  - No false success is shown, and the failure message explains the problem.

## AC-06: Language-Sensitive Failure Messaging

- Related stories: US-04
- Criterion:
  - Failure and omission messaging follows the language of the active conversation.
- Observable evidence:
  - English threads receive English failure messaging, German threads receive German failure messaging.

## AC-07: Stable Export Numbering

- Related stories: US-05
- Criterion:
  - Exports of the same session use clear incrementing numbering.
- Observable evidence:
  - The first export ends in `-1`, the second in `-2`, and so on.
