# User Journeys

## Purpose

This document describes the main user journeys for the `$export` skill from the user's perspective.

## Journey J-01: First Export In Current Session

- Actor: Human, GPT Model, Codex CLI/Codex App
- Trigger: execution of the $export skill
- Context: User executes $export
- Goal: The entire chat history including the use of $export skill is being exported into a markdown file as per @08_artifact_structure_and_naming.md
- Happy path:
  1. User types in $export in Codex App / Codex CLI
  2. GPT executes the skill
  3. The markdown file with the content is created
  4. GPT confirms to the user that the file has been created, gives the user its name and the path to the file on the system
- Failure or edge path:
  1. Something goes wrong and the file isn't created or only in part created
  2. GPT analyzes the precise error
  3. GPT tells the user what the precise error is
  4. GPT makes suggestions on what to do next
- Outcome: The file is created or the user knows why it couldn't be created and gets ideas on what to do next
- Notes: ?

## Journey J-02: Repeated Export In Same Session

- Actor: Human, GPT Model, Codex CLI/Codex App
- Trigger: execution of the $export skill
- Context: User executes $export
- Goal: When the chat session has been exported once, the next execution of the $export skill will export from where the last export left off
- Happy path:
  1. User types $export in Codex App / Codex CLI after J-01 has already passed
  2. GPT executes the skill
  3. GPT figures out that this chat session already was exported once
  4. GPT checks what the last checkpoint was
  5. GPT looks in the jsonl file for where the point was and continues the export from there
  6. GPT confirms with the user that the file has been created, that it's been an incremental export and gives the user the name and the path to the file on the system. On top of that, GPT shows that the user can create a new full export of this chat session anytime, whenever the user uses $export --full
- Failure or edge path:
  1.
  2.
  3.
- Outcome:
- Notes:

## Journey J-03: Export When Access Is Blocked

- Actor:
- Trigger:
- Context:
- Goal:
- Happy path:
- Failure or edge path:
  1.
  2.
  3.
- Outcome:
- Notes:

## Journey J-04: Export In Long-Running Session

- Actor:
- Trigger:
- Context:
- Goal:
- Happy path:
  1.
  2.
  3.
  4.
- Failure or edge path:
  1.
  2.
- Outcome:
- Notes:
