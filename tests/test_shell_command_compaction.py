from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from codexporter.cli import main
from codexporter.compaction import prepare_entries_for_render
from codexporter.json_utils import JsonObject
from codexporter.models import ExportEntry
from conftest import SessionFixture, build_session_fixture, dump_json_value


def test_prepare_entries_for_render_compacts_shell_command_json_payloads() -> None:
    file_read_output = "[build-system]\nrequires = ['setuptools>=80']\nversion = '1.1.5'"
    listing_output = "\n".join(f"src/file_{index:03d}.py" for index in range(150))
    entries = (
        _tool_call(
            1,
            "call-read",
            "shell_command",
            dump_json_value({"command": "cat pyproject.toml"}),
        ),
        _tool_output(2, "call-read", "shell_command", file_read_output),
        _tool_call(
            3,
            "call-list",
            "shell_command",
            dump_json_value({"cmd": "rg --files"}),
        ),
        _tool_output(4, "call-list", "shell_command", listing_output),
    )

    compacted = prepare_entries_for_render(entries, "compact")

    assert compacted[1].output is not None
    assert "Raw file contents omitted in compact mode." in compacted[1].output
    assert "- pyproject.toml" in compacted[1].output
    assert "[build-system]" not in compacted[1].output

    assert compacted[3].output is not None
    assert "Large raw file listing omitted in compact mode." in compacted[3].output
    assert "src/file_149.py" not in compacted[3].output


def test_prepare_entries_for_render_compacts_shell_command_plain_string_payloads() -> None:
    file_read_output = "[build-system]\nrequires = ['setuptools>=80']\nversion = '1.1.5'"
    entries = (
        _tool_call(1, "call-read", "shell_command", "cat pyproject.toml"),
        _tool_output(2, "call-read", "shell_command", file_read_output),
    )

    compacted = prepare_entries_for_render(entries, "compact")

    assert compacted[1].output is not None
    assert "Raw file contents omitted in compact mode." in compacted[1].output
    assert "- pyproject.toml" in compacted[1].output
    assert "[build-system]" not in compacted[1].output


def test_cli_main_compact_compacts_windows_shell_command_rollout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    session_fixture = build_session_fixture(tmp_path)
    _write_windows_shell_rollout_fixture(session_fixture)

    exit_code = main(
        [
            "--project-root",
            str(session_fixture.project_root),
            "--codex-home",
            str(session_fixture.codex_home),
            "--compact",
        ]
    )

    captured = capsys.readouterr()
    export_paths = sorted(session_fixture.export_dir.glob("*.md"))

    assert exit_code == 0
    assert len(export_paths) == 1
    assert "compact mode" in captured.out.strip()

    rendered = export_paths[0].read_text(encoding="utf-8")
    assert "## Tool Call · shell_command" in rendered
    assert "## Tool Output · shell_command" in rendered
    assert "Raw file contents omitted in compact mode." in rendered
    assert "- pyproject.toml" in rendered
    assert "[build-system]" not in rendered


def _tool_call(
    source_index: int,
    call_id: str,
    tool_name: str,
    arguments: str,
) -> ExportEntry:
    return ExportEntry(
        source_index=source_index,
        kind="tool_call",
        timestamp=datetime(2026, 4, 3, 22, 43, source_index, tzinfo=UTC),
        turn_id="turn-1",
        tool_name=tool_name,
        arguments=arguments,
        call_id=call_id,
    )


def _tool_output(
    source_index: int,
    call_id: str,
    tool_name: str,
    output: str,
) -> ExportEntry:
    return ExportEntry(
        source_index=source_index,
        kind="tool_output",
        timestamp=datetime(2026, 4, 3, 22, 43, source_index, tzinfo=UTC),
        turn_id="turn-1",
        tool_name=tool_name,
        output=output,
        call_id=call_id,
    )


def _write_windows_shell_rollout_fixture(session_fixture: SessionFixture) -> None:
    records: list[JsonObject] = [
        {
            "timestamp": "2026-04-03T22:43:00Z",
            "type": "session_meta",
            "payload": {
                "id": session_fixture.session_id,
                "timestamp": "2026-04-03T22:43:00Z",
                "cwd": str(session_fixture.project_root),
                "originator": "Codex Desktop",
                "cli_version": "0.118.0-alpha.2",
                "source": "vscode",
                "model_provider": "openai",
            },
        },
        {
            "timestamp": "2026-04-03T22:43:05Z",
            "type": "event_msg",
            "payload": {"type": "task_started", "turn_id": "turn-1"},
        },
        {
            "timestamp": "2026-04-03T22:43:06Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Please export this Windows app session in compact mode.",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-04-03T22:43:06Z",
            "type": "turn_context",
            "payload": {
                "turn_id": "turn-1",
                "cwd": str(session_fixture.project_root),
                "current_date": "2026-04-03",
                "timezone": "UTC",
                "approval_policy": "never",
                "sandbox_policy": {"type": "danger-full-access"},
                "model": "gpt-5.4",
            },
        },
        {
            "timestamp": "2026-04-03T22:43:07Z",
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "status": "completed",
                "call_id": "call-read",
                "name": "shell_command",
                "input": "cat pyproject.toml",
            },
        },
        {
            "timestamp": "2026-04-03T22:43:08Z",
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "call_id": "call-read",
                "output": (
                    "[build-system]\n"
                    'requires = ["setuptools>=80"]\n'
                    'build-backend = "setuptools.build_meta"\n\n'
                    "[project]\n"
                    'name = "codexporter-skill"\n'
                    'version = "1.1.5"'
                ),
            },
        },
        {
            "timestamp": "2026-04-03T22:43:09Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": "The compact export kept the shell-command chronology.",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-04-03T22:43:10Z",
            "type": "event_msg",
            "payload": {"type": "task_complete", "turn_id": "turn-1"},
        },
    ]
    session_fixture.rollout_path.write_text(
        "\n".join(dump_json_value(record, separators=(",", ":")) for record in records) + "\n",
        encoding="utf-8",
    )
