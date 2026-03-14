from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from codexporter.messages import detect_language
from codexporter.models import ExportEntry, SessionInfo
from codexporter.renderer import render_markdown
from codexporter.service import _build_export_filename


def test_build_export_filename_sanitizes_and_truncates_session_name() -> None:
    exported_at = datetime(2026, 3, 14, 12, 34, 56, tzinfo=ZoneInfo("UTC"))

    filename = _build_export_filename(
        exported_at=exported_at,
        session_name="Release planning / review!!! " + ("segment-" * 20),
        session_id="session-123",
        sequence=7,
    )

    assert re.fullmatch(r"20260314-123456-[A-Za-z0-9-]+-7\.md", filename)
    slug = filename.removeprefix("20260314-123456-").removesuffix("-7.md")
    assert len(slug) <= 60
    assert "--" not in slug


def test_detect_language_flags_german_markers() -> None:
    assert detect_language(["Kannst du das bitte jetzt exportieren, danke?"]) == "de"
    assert (
        detect_language(["Please export the current session and keep the new content only."])
        == "en"
    )


def test_render_markdown_formats_visible_chat_and_tool_blocks() -> None:
    session = SessionInfo(
        session_id="session-123",
        session_name="Renderer Check",
        session_started_at=datetime(2026, 3, 14, 12, 0, 0, tzinfo=ZoneInfo("UTC")),
        cwd=Path("/tmp/project-alpha"),
        source="vscode",
        originator="Codex Desktop",
        model="gpt-5.4",
        model_provider="openai",
        cli_version="0.115.0-alpha.11",
        timezone_name="Europe/Vienna",
        approval_policy="never",
        sandbox_policy='{"type":"danger-full-access"}',
        language="en",
    )
    entries = (
        ExportEntry(
            source_index=1,
            kind="user",
            timestamp=datetime(2026, 3, 14, 12, 0, 1, tzinfo=ZoneInfo("UTC")),
            turn_id="turn-1",
            text="Please export the current session.",
        ),
        ExportEntry(
            source_index=2,
            kind="commentary",
            timestamp=datetime(2026, 3, 14, 12, 0, 2, tzinfo=ZoneInfo("UTC")),
            turn_id="turn-1",
            text="Inspecting the current export surface first.",
        ),
        ExportEntry(
            source_index=3,
            kind="tool_call",
            timestamp=datetime(2026, 3, 14, 12, 0, 3, tzinfo=ZoneInfo("UTC")),
            turn_id="turn-1",
            tool_name="exec_command",
            arguments='{"cmd":"pwd"}',
        ),
        ExportEntry(
            source_index=4,
            kind="tool_output",
            timestamp=datetime(2026, 3, 14, 12, 0, 4, tzinfo=ZoneInfo("UTC")),
            turn_id="turn-1",
            tool_name="exec_command",
            output="/tmp/project-alpha",
        ),
        ExportEntry(
            source_index=5,
            kind="assistant",
            timestamp=datetime(2026, 3, 14, 12, 0, 5, tzinfo=ZoneInfo("UTC")),
            turn_id="turn-1",
            text="The export surface looks consistent.",
        ),
    )

    rendered = render_markdown(
        session=session,
        entries=entries,
        export_sequence=1,
        export_mode="full",
        exported_at=datetime(2026, 3, 14, 12, 5, 0, tzinfo=ZoneInfo("UTC")),
        sidecar_path=Path("/tmp/project-alpha/codex_exports/session-123-checkpoint.json"),
    )

    assert rendered.startswith("# Session Export\n\n- Session name: Renderer Check")
    assert "## Conversation" in rendered
    assert "## User · 2026-03-14 13:00:01 CET" in rendered
    assert "## gpt-5.4 Commentary · 2026-03-14 13:00:02 CET" in rendered
    assert "## Tool Call · exec_command · 2026-03-14 13:00:03 CET" in rendered
    assert '**Arguments**\n```json\n{\n  "cmd": "pwd"\n}\n```' in rendered
    assert "## Tool Output · exec_command · 2026-03-14 13:00:04 CET" in rendered
    assert "```text\n/tmp/project-alpha\n```" in rendered
    assert "## gpt-5.4 Assistant · 2026-03-14 13:00:05 CET" in rendered
    assert "## Export Metadata" in rendered
    assert rendered.index("## User") < rendered.index("## gpt-5.4 Commentary")
    assert rendered.index("## gpt-5.4 Commentary") < rendered.index("## Tool Call")
    assert rendered.index("## Tool Call") < rendered.index("## Tool Output")
    assert rendered.index("## Tool Output") < rendered.index("## gpt-5.4 Assistant")
