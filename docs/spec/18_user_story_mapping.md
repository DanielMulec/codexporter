# User Story Mapping

## Purpose

This document maps user stories to journeys, flows, acceptance criteria, and tests.

| Story ID | User Story | Priority | Version | Journey IDs | Flow IDs | Acceptance IDs | Test IDs | Notes |
|---|---|---|---|---|---|---|---|---|
| US-01 | As a Codex user, I want to invoke `$export` in the current session so that I can preserve the chat history in markdown. | Must | v1 | J-01 | F-01 |  |  |  |
| US-02 | As a Codex user, I want repeated exports in the same session to contain only new content so that I do not get duplicate exports. | Must | v1 | J-02, J-05 | F-02 |  |  |  |
| US-03 | As a Codex user, I want the export to reflect what I visibly experienced in chat so that the markdown is readable and useful. | Must | v1 | J-01, J-02 | F-01, F-02 |  |  |  |
| US-04 | As a Codex user, I want the export to fail clearly in my current conversation language when it cannot complete. | Must | v1 | J-04 | F-03 |  |  |  |
| US-05 | As a Codex user, I want git information included when available so that I can correlate the session with repo state. | Should | v1 | J-01, J-03 | F-01 |  |  |  |
| US-06 | As a Codex user, I want the export filename sequence to stay clear across multiple exports of the same session. | Must | v1 | J-02, J-05 | F-02 |  |  |  |
