# User Story Mapping

## Purpose

This document maps user stories to journeys, flows, acceptance criteria, and tests.

| Story ID | User Story | Priority | Version | Journey IDs | Flow IDs | Acceptance IDs | Test IDs | Notes |
|---|---|---|---|---|---|---|---|---|
| US-01 | As a Codex user, I want to invoke `$export` in the current session so that I can preserve the chat history in markdown. | Must | v1 | J-01 | F-01 | AC-01, AC-02, AC-08, AC-12 | T-01, T-08 |  |
| US-02 | As a Codex user, I want repeated exports in the same session to contain only new content so that I do not get duplicate exports. | Must | v1 | J-02 | F-02 | AC-04, AC-07, AC-09, AC-10 | T-03, T-13, T-14 |  |
| US-03 | As a Codex user, I want the export to reflect what I visibly experienced in chat so that the markdown is readable and useful. | Must | v1 | J-01, J-02 | F-01, F-02 | AC-02, AC-03, AC-08 | T-05, T-06, T-07 |  |
| US-04 | As a Codex user, I want the export to fail clearly in my current conversation language when it cannot complete. | Must | v1 | J-03 | F-03 | AC-05, AC-06, AC-11 | T-15, T-17, T-18, T-19 |  |
| US-05 | As a Codex user, I want the export filename sequence to stay clear across multiple exports of the same session. | Must | v1 | J-02 | F-02 | AC-07 | T-03 |  |
