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

- Related stories: US-02, US-03
- Criterion:
  - The default export stays close to what the user visibly experienced in chat.
- Observable evidence:
  - The export shows visible user messages, assistant replies, commentary, and tool activity in chronological order.

## AC-04: Repeated Export Does Not Duplicate Prior Content

- Related stories: US-04
- Criterion:
  - A later export of the same session does not repeat content that was already exported successfully before.
- Observable evidence:
  - Previously exported content does not reappear in the next incremental export file.

## AC-05: Clear Failure Messaging

- Related stories: US-08
- Criterion:
  - If export fails, the user is informed directly what failed and why.
- Observable evidence:
  - No false success is shown, and the failure message explains the problem.

## AC-06: Language-Sensitive Failure Messaging

- Related stories: US-08
- Criterion:
  - Failure and omission messaging follows the language of the active conversation.
- Observable evidence:
  - English threads receive English failure messaging, German threads receive German failure messaging.

## AC-07: Stable Export Numbering

- Related stories: US-04, US-06
- Criterion:
  - Exports of the same session use clear incrementing numbering.
- Observable evidence:
  - The first export ends in `-1`, the second in `-2`, and so on.

## AC-08: Success Response Includes File Location

- Related stories: US-01, US-03
- Criterion:
  - On successful export, Codex tells the user the created file name and file path.
- Observable evidence:
  - The success message identifies the export file and where it was written.

## AC-09: No-New-Content Behavior

- Related stories: US-04
- Criterion:
  - If there is no new exportable content since the previous successful checkpoint, no new export file is created.
- Observable evidence:
  - The user is informed that there is no new content to export, and no additional export file appears.

## AC-10: Incremental Export Is Communicated Clearly

- Related stories: US-04, US-05
- Criterion:
  - On successful repeated export, Codex tells the user that the export was incremental.
- Observable evidence:
  - The success message states that the export contains only new content since the previous successful export.

## AC-11: Blocked-Access Guidance

- Related stories: US-08
- Criterion:
  - When required access is blocked and a recovery step is available, Codex guides the user toward that recovery step.
- Observable evidence:
  - The failure message explains the blocking issue and tells the user what to change before retrying `$export`.

## AC-12: Default Export Destination

- Related stories: US-01
- Criterion:
  - Export artifacts are written into the `codex_exports` subfolder in the current project root.
- Observable evidence:
  - The created export file appears in `codex_exports`, and the reported file path points there.

## AC-13: Cross-Platform Consistency

- Related stories: US-07
- Criterion:
  - Across the supported target environments, the skill preserves the same core user-facing behavior for export creation, incremental export, and failure communication.
- Observable evidence:
  - Users on the supported target environments receive the same basic export outcome and the same class of success or failure messaging, even if the underlying paths or environment details differ.

## AC-14: Restricted-Environment Transparency

- Related stories: US-08
- Criterion:
  - In a restricted environment, Codex tells the user clearly what required or optional data could not be accessed.
- Observable evidence:
  - The user is told what data was unavailable and whether the export still succeeded, partially succeeded, or failed.
