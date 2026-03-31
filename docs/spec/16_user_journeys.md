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

## Journey J-04: Use One Installed Skill Across Projects

- Actor: Codex user, globally installed `$export` skill, Codex CLI or Codex app
- Trigger: user invokes `$export` from a different project context after the skill was already installed
- Context: the skill is already installed globally, and the user is now working in a project that is different from the one used during a prior export
- Goal: reuse the same installed skill without reinstallation while still writing export artifacts into the active project's `codex_exports` folder
- Happy path:
  1. The user installs the skill once through the skill installer.
  2. The user opens a Codex session in a project context.
  3. The user invokes `$export`.
  4. The skill resolves the active project root from the current session context.
  5. The skill writes export artifacts into that project's `codex_exports` subfolder.
  6. Later, the user invokes `$export` from a different project context without reinstalling the skill.
  7. The same installed skill writes export artifacts into the new active project's `codex_exports` subfolder.
- Failure or edge path:
  1. The skill cannot determine the active project root responsibly.
  2. The skill does not guess and does not write into the installed skill directory.
  3. Codex tells the user what failed and why.
- Outcome: one globally installed skill can be reused across projects, or the user is told clearly why export could not proceed

## Journey J-05: First Compact Export In Current Session

- Actor: Codex user, `$export` skill, Codex CLI or Codex app
- Trigger: user invokes `$export --compact`
- Context: user is in the current active Codex session and wants a denser export for quick review
- Goal: export the current session to a markdown file that preserves the visible chronology while omitting bulky raw tool payloads deterministically
- Happy path:
  1. The user invokes `$export --compact` in Codex CLI or the Codex app.
  2. The skill exports the current session's supported content using the compact render profile.
  3. The markdown export file is created with the same canonical artifact identity as any other export for that session.
  4. The compact export preserves the visible chronological workflow while replacing qualifying bulky raw tool payloads with deterministic omission markers.
  5. Codex tells the user that the compact export succeeded and provides the file name and file path.
- Failure or edge path:
  1. The export cannot be completed successfully.
  2. Codex identifies the specific blocking problem.
  3. Codex tells the user what failed and why.
  4. Codex provides a next step when one is available.
- Outcome: the compact export file is created, or the user understands why the compact export did not succeed and what to do next

## Journey J-06: Compact Export Within Existing Export History

- Actor: Codex user, `$export` skill, Codex CLI or Codex app
- Trigger: user invokes `$export --compact` or `$export` after the same session has already been exported successfully with either profile
- Context: the current session already has canonical export history and checkpoint state
- Goal: continue the same per-session export history without duplicating content or forking checkpoint identity when switching between full and compact renders
- Happy path:
  1. The user invokes `$export --compact` or plain `$export` again in the same Codex session.
  2. The skill detects the existing export history and reads the shared checkpoint.
  3. The skill validates that checkpoint against the current session event stream.
  4. The skill exports only new supported content after the last successful checkpoint, if any exists.
  5. If no new exportable content exists, Codex tells the user directly and creates no new markdown file.
  6. If new exportable content exists, the next numbered markdown export file is created with the requested render profile.
  7. Codex tells the user that the export succeeded, whether it was incremental, and where the file was written.
- Failure or edge path:
  1. The export cannot be completed successfully.
  2. Codex identifies the specific blocking problem.
  3. Codex tells the user what failed and why.
  4. Codex provides a next step when one is available.
- Outcome: compact and full exports remain part of one canonical export history for the session, or the user understands why export could not continue safely
