# User Journeys

## Purpose

This document describes the main user journeys for the `$export` skill from the user's perspective.

## Journey J-01: First Export In Current Session

- Actor: Codex user, `$export` skill, Codex CLI or Codex app
- Trigger: user invokes `$export`
- Context: user is in the current active Codex session
- Goal: export the current session to a markdown file as defined in `08_artifact_structure_and_naming.md`
- Happy path:
  1. The user invokes `$export` in Codex CLI or the Codex app.
  2. The skill exports the current session's supported content.
  3. The markdown export file is created.
  4. Codex tells the user that the export succeeded and provides the file name and file path.
- Failure or edge path:
  1. The export cannot be completed successfully.
  2. Codex identifies the specific blocking problem.
  3. Codex tells the user what failed and why.
  4. Codex provides a next step when one is available.
- Outcome: the export file is created, or the user understands why the export did not succeed and what to do next

## Journey J-02: Repeated Export In Same Session

- Actor: Codex user, `$export` skill, Codex CLI or Codex app
- Trigger: user invokes `$export`
- Context: the current session has already been exported successfully at least once
- Goal: create a new export that continues from the last successful checkpoint without repeating previously exported content
- Happy path:
  1. The user invokes `$export` again in the same Codex session.
  2. The skill detects that the session has already been exported.
  3. The skill reads the last successful checkpoint.
  4. The skill resumes from that checkpoint in the session event stream.
  5. The next markdown export file is created with only the new supported content.
  6. Codex tells the user that the export succeeded, that it was incremental, and provides the file name and file path.
- Failure or edge path:
  1. The export cannot be completed successfully.
  2. Codex identifies the specific blocking problem.
  3. Codex tells the user what failed and why.
  4. Codex provides a next step when one is available.
- Outcome: the next incremental export file is created, or the user understands why the export did not succeed and what to do next

## Journey J-03: Export When Access Is Blocked

- Actor: Codex user, `$export` skill, Codex CLI or Codex app
- Trigger: user invokes `$export`
- Context: the user invokes `$export`, but required access to the current session data is not available
- Goal: guide the user toward either a successful export or a clear understanding of what must change before retrying `$export`
- Happy path: 
  1. The user invokes `$export` in Codex CLI or the Codex app.
  2. The skill detects that required access is blocked or unavailable.
  3. Codex explains the blocking issue.
  4. If a recovery step is available, Codex guides the user toward restoring access.
  5. If access becomes available, the export continues through the first-export or repeated-export journey as appropriate.
  6. If access does not become available, Codex tells the user what must be resolved before retrying `$export`.
- Outcome: the correct export file is created, or the user understands the blocking issue and what to do before retrying `$export`
