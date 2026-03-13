# User Story Mapping

## Purpose

This document maps user stories to journeys, flows, acceptance criteria, and tests.

| Story ID | User Story | Priority | Version | Journey IDs | Flow IDs | Acceptance IDs | Test IDs | Notes |
|---|---|---|---|---|---|---|---|---|
| US-01 | As a Codex user, I want to invoke `$export` in the current session so that I can preserve the chat history in markdown. | Must | v1 | J-01 | F-01 | AC-01, AC-02, AC-08, AC-12 | T-01, T-08, T-09 |  |
| US-02 | As a Codex user, I want the export to include the meaningful workflow trail so that I can see what the agent actually did, not just the final answer. | Must | v1 | J-01, J-02 | F-01, F-02 | AC-03 | T-05, T-06, T-07 |  |
| US-03 | As a Codex user, I want the export to be readable and well-structured so that I can use it for documentation, handoff, or review. | Must | v1 | J-01, J-02 | F-01, F-02 | AC-02, AC-03, AC-08 | T-05, T-06, T-07 |  |
| US-04 | As a Codex user, I want repeated exports in the same session to continue from the last export point so that I do not get noisy duplication. | Must | v1 | J-02 | F-02 | AC-04, AC-07, AC-09, AC-10 | T-03, T-14, T-15, T-16, T-31, T-35 |  |
| US-05 | As a Codex user, I want it to be clear whether an export is the first export for a session or an incremental export so that I understand what changed since the previous checkpoint. | Must | v1 | J-01, J-02 | F-01, F-02 | AC-08, AC-10 | T-09, T-16 |  |
| US-06 | As a Codex user, I want export filenames to stay clearly sequenced across repeated exports of the same session so that I can tell the artifacts apart. | Must | v1 | J-02 | F-02 | AC-07 | T-31 |  |
| US-07 | As a Codex user, I want the skill to work consistently across the supported operating systems for Codex so that I can rely on it in different environments. | Must | v1 | J-01, J-02, J-03 | F-01, F-02, F-03 | AC-13 | T-23, T-24, T-25, T-26, T-27, T-28, T-29, T-30 |  |
| US-08 | As a Codex user in a restricted environment, I want the skill to tell me clearly what it can and cannot access so that I understand the result and the limitations. | Must | v1 | J-03 | F-03 | AC-05, AC-06, AC-11, AC-14 | T-17, T-19, T-20, T-21, T-22 |  |
