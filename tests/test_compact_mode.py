from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from codexporter.cli import main
from codexporter.compaction import prepare_entries_for_render
from codexporter.json_utils import JsonObject, JsonValue
from codexporter.models import ExportEntry
from codexporter.service import export_current_session
from conftest import SessionFixture, build_session_fixture, dump_json_value


def test_prepare_entries_for_render_compacts_bulky_tool_payloads() -> None:
    file_read_output = "first line\nsecond line\nthird line\nfourth line"
    patch_payload = "\n".join(
        [
            "*** Begin Patch",
            "*** Update File: src/app.py",
            "@@",
            "-old line",
            "+new line",
            "*** End Patch",
        ]
    )
    listing_output = "\n".join(f"src/file_{index:03d}.py" for index in range(150))
    large_diff_output = _build_large_diff_output()
    entries = (
        _tool_call(1, "call-read", "exec_command", '{"cmd":"sed -n \'1,120p\' src/app.py"}'),
        _tool_output(2, "call-read", "exec_command", file_read_output),
        _tool_call(3, "call-patch", "apply_patch", patch_payload),
        _tool_output(
            4,
            "call-patch",
            "apply_patch",
            '{"output":"Success. Updated the following files:\\nM src/app.py\\n"}',
        ),
        _tool_call(5, "call-diff", "exec_command", '{"cmd":"git diff -- src/app.py"}'),
        _tool_output(6, "call-diff", "exec_command", large_diff_output),
        _tool_call(7, "call-list", "exec_command", '{"cmd":"rg --files"}'),
        _tool_output(8, "call-list", "exec_command", listing_output),
    )

    compacted = prepare_entries_for_render(entries, "compact")

    assert compacted[1].output is not None
    assert "Raw file contents omitted in compact mode." in compacted[1].output
    assert "- src/app.py" in compacted[1].output
    assert "first line" not in compacted[1].output

    assert compacted[2].arguments is not None
    assert "Raw patch omitted in compact mode." in compacted[2].arguments
    assert "- src/app.py" in compacted[2].arguments
    assert "*** Begin Patch" not in compacted[2].arguments

    assert compacted[5].output is not None
    assert "Raw diff omitted in compact mode." in compacted[5].output
    assert "- src/app.py +61 -1" in compacted[5].output
    assert "diff --git" not in compacted[5].output

    assert compacted[7].output is not None
    assert "Large raw file listing omitted in compact mode." in compacted[7].output
    assert "src/file_149.py" not in compacted[7].output


def test_export_current_session_compact_shares_checkpoint_with_full_mode(
    session_fixture: SessionFixture,
) -> None:
    compact_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
        render_profile="compact",
    )

    assert compact_result.export_path is not None
    assert compact_result.render_profile == "compact"
    assert "compact mode" in compact_result.message

    full_result = export_current_session(
        project_root=session_fixture.project_root,
        codex_home=session_fixture.codex_home,
        now=session_fixture.first_export_time,
        render_profile="full",
    )

    assert full_result.no_new_content is True
    assert full_result.export_sequence == 1
    assert full_result.render_profile == "full"
    assert len(list(session_fixture.export_dir.glob("*.md"))) == 1


def test_prepare_entries_for_render_compacts_oversized_json_output() -> None:
    large_report: JsonValue = [
        {"index": index, "value": f"item-{index:03d}"} for index in range(400)
    ]
    large_json_output = dump_json_value(large_report, indent=2, sort_keys=True)
    entries = (
        _tool_call(1, "call-json", "exec_command", '{"cmd":"jq \'.\' build/report.json"}'),
        _tool_output(2, "call-json", "exec_command", large_json_output),
    )

    compacted = prepare_entries_for_render(entries, "compact")

    assert compacted[1].output is not None
    assert "Large raw JSON output omitted in compact mode." in compacted[1].output
    assert '"index": 399' not in compacted[1].output


def test_cli_main_compact_creates_compact_export_and_reports_it(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    session_fixture = build_session_fixture(tmp_path)
    _write_compact_rollout_fixture(session_fixture)

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
    assert "- Render profile: compact" in rendered
    assert "Raw file contents omitted in compact mode." in rendered
    assert "Raw patch omitted in compact mode." in rendered
    assert "Raw diff omitted in compact mode." in rendered
    assert "Large raw file listing omitted in compact mode." in rendered
    assert "class Example:" not in rendered
    assert "diff --git a/src/app.py b/src/app.py" not in rendered


def _tool_call(
    source_index: int,
    call_id: str,
    tool_name: str,
    arguments: str,
) -> ExportEntry:
    return ExportEntry(
        source_index=source_index,
        kind="tool_call",
        timestamp=datetime(2026, 3, 14, 12, 0, source_index, tzinfo=UTC),
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
        timestamp=datetime(2026, 3, 14, 12, 0, source_index, tzinfo=UTC),
        turn_id="turn-1",
        tool_name=tool_name,
        output=output,
        call_id=call_id,
    )


def _write_compact_rollout_fixture(session_fixture: SessionFixture) -> None:
    records: list[JsonObject] = [
        {
            "timestamp": "2026-03-13T19:00:00Z",
            "type": "session_meta",
            "payload": {
                "id": session_fixture.session_id,
                "timestamp": "2026-03-13T19:00:00Z",
                "cwd": str(session_fixture.project_root),
                "originator": "Codex Desktop",
                "cli_version": "0.115.0-alpha.11",
                "source": "vscode",
                "model_provider": "openai",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:05Z",
            "type": "event_msg",
            "payload": {"type": "task_started", "turn_id": "turn-1"},
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
                        "text": "Please export this session compactly.",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-03-13T19:00:06Z",
            "type": "turn_context",
            "payload": {
                "turn_id": "turn-1",
                "cwd": str(session_fixture.project_root),
                "current_date": "2026-03-13",
                "timezone": "UTC",
                "approval_policy": "never",
                "sandbox_policy": {"type": "danger-full-access"},
                "model": "gpt-5.4",
                "personality": "pragmatic",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:07Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "phase": "commentary",
                "content": [
                    {
                        "type": "output_text",
                        "text": "Checking the large tool payloads before writing the export.",
                    }
                ],
            },
        },
        {
            "timestamp": "2026-03-13T19:00:08Z",
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "name": "exec_command",
                "arguments": dump_json_value({"cmd": "sed -n '1,120p' src/app.py"}),
                "call_id": "call-read",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:08Z",
            "type": "response_item",
            "payload": {
                "type": "function_call_output",
                "call_id": "call-read",
                "output": (
                    "class Example:\n"
                    "    pass\n"
                    "    # still visible in full mode\n"
                    "    # but not in compact mode"
                ),
            },
        },
        {
            "timestamp": "2026-03-13T19:00:09Z",
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "status": "completed",
                "call_id": "call-patch",
                "name": "apply_patch",
                "input": "\n".join(
                    [
                        "*** Begin Patch",
                        "*** Update File: src/app.py",
                        "@@",
                        "-old line",
                        "+new line",
                        "*** End Patch",
                    ]
                ),
            },
        },
        {
            "timestamp": "2026-03-13T19:00:09Z",
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "call_id": "call-patch",
                "output": {
                    "output": "Success. Updated the following files:\nM src/app.py\n",
                    "metadata": {"exit_code": 0, "duration_seconds": 0.0},
                },
            },
        },
        {
            "timestamp": "2026-03-13T19:00:10Z",
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "name": "exec_command",
                "arguments": dump_json_value({"cmd": "git diff -- src/app.py"}),
                "call_id": "call-diff",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:10Z",
            "type": "response_item",
            "payload": {
                "type": "function_call_output",
                "call_id": "call-diff",
                "output": _build_large_diff_output(),
            },
        },
        {
            "timestamp": "2026-03-13T19:00:11Z",
            "type": "response_item",
            "payload": {
                "type": "function_call",
                "name": "exec_command",
                "arguments": dump_json_value({"cmd": "rg --files"}),
                "call_id": "call-list",
            },
        },
        {
            "timestamp": "2026-03-13T19:00:11Z",
            "type": "response_item",
            "payload": {
                "type": "function_call_output",
                "call_id": "call-list",
                "output": "\n".join(f"src/file_{index:03d}.py" for index in range(150)),
            },
        },
        {
            "timestamp": "2026-03-13T19:00:12Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": (
                            "The compact export kept the workflow but dropped the bulky raw "
                            "payloads."
                        ),
                    }
                ],
            },
        },
        {
            "timestamp": "2026-03-13T19:00:13Z",
            "type": "event_msg",
            "payload": {"type": "task_complete", "turn_id": "turn-1"},
        },
    ]
    session_fixture.rollout_path.write_text(
        "\n".join(dump_json_value(record, separators=(",", ":")) for record in records) + "\n",
        encoding="utf-8",
    )


def _build_large_diff_output() -> str:
    diff_lines = [
        "diff --git a/src/app.py b/src/app.py",
        "index 1111111..2222222 100644",
        "--- a/src/app.py",
        "+++ b/src/app.py",
        "@@ -1 +1,61 @@",
        "-old line",
    ]
    diff_lines.extend(f"+new line {index}" for index in range(1, 62))
    return "\n".join(diff_lines)
