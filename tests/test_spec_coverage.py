from __future__ import annotations

import json

from codexporter.service import export_current_session
from conftest import SESSION_ID, SessionFixture


def test_export_excludes_internal_instructions_and_hidden_reasoning(
    session_fixture: SessionFixture,
) -> None:
    result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    assert result.export_path is not None
    markdown = result.export_path.read_text(encoding="utf-8")

    assert "# AGENTS.md instructions for" not in markdown
    assert "<INSTRUCTIONS>" not in markdown
    assert "encrypted_content" not in markdown
    assert "\nhidden\n" not in markdown


def test_export_succeeds_without_optional_rollout_metadata(
    session_fixture: SessionFixture,
) -> None:
    minimal_records = (
        {
            "timestamp": "2026-03-13T19:00:00Z",
            "type": "session_meta",
            "payload": {
                "id": SESSION_ID,
                "timestamp": "2026-03-13T19:00:00Z",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:05Z",
            "type": "event_msg",
            "payload": {
                "type": "task_started",
                "turn_id": "turn-1",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:06Z",
            "type": "turn_context",
            "payload": {
                "turn_id": "turn-1",
                "cwd": str(session_fixture.project_root),
            },
        },
        {
            "timestamp": "2026-03-13T19:00:06Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Please export this session without optional metadata.",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-03-13T19:00:07Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": "The exporter can still succeed without optional metadata.",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-03-13T19:00:08Z",
            "type": "event_msg",
            "payload": {
                "type": "task_complete",
                "turn_id": "turn-1",
            },
        },
    )
    session_fixture.rollout_path.write_text(
        "\n".join(json.dumps(record, separators=(",", ":")) for record in minimal_records) + "\n",
        encoding="utf-8",
    )

    result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
    )

    assert result.export_path is not None
    markdown = result.export_path.read_text(encoding="utf-8")
    assert "- Session id: 019aaa00-bbbb-7ccc-8ddd-eeeeffff0001" in markdown
    assert f"- Current working directory: {session_fixture.project_root}" in markdown
    assert "- Model:" not in markdown
    assert "## User · 2026-03-13 19:00:06 UTC" in markdown
