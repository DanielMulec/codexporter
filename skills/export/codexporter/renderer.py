from __future__ import annotations

import json
from datetime import UTC, datetime, tzinfo
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from codexporter.json_utils import load_json_value
from codexporter.models import ExportEntry, ExportMode, RenderProfile, SessionInfo


def render_markdown(
    session: SessionInfo,
    entries: tuple[ExportEntry, ...],
    export_sequence: int,
    export_mode: ExportMode,
    render_profile: RenderProfile,
    exported_at: datetime,
    sidecar_path: Path,
) -> str:
    lines: list[str] = ["# Session Export", ""]
    lines.extend(_render_session_metadata(session))
    lines.extend(["", "## Conversation", ""])

    for entry in entries:
        lines.extend(_render_entry(session, entry))
        lines.append("")

    lines.extend(
        [
            "## Export Metadata",
            "",
            f"- Exported at: {_format_timestamp(exported_at, session.timezone_name)}",
            f"- Export sequence: {export_sequence}",
            f"- Export mode: {export_mode}",
            f"- Render profile: {render_profile}",
            f"- Checkpoint sidecar: {sidecar_path.name}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_session_metadata(session: SessionInfo) -> list[str]:
    lines: list[str] = []
    if session.session_name:
        lines.append(f"- Session name: {session.session_name}")
    lines.append(f"- Session id: {session.session_id}")
    if session.session_started_at is not None:
        started_at = _format_timestamp(session.session_started_at, session.timezone_name)
        lines.append(f"- Session started: {started_at}")
    lines.append(f"- Current working directory: {session.cwd}")
    if session.source:
        lines.append(f"- Source: {session.source}")
    if session.model:
        lines.append(f"- Model: {session.model}")
    return lines


def _render_entry(session: SessionInfo, entry: ExportEntry) -> list[str]:
    if entry.kind == "event":
        return [
            _heading(_event_label(entry.event_type), entry.timestamp, session.timezone_name),
            "",
            _event_body(entry.event_type),
        ]
    if entry.kind == "user":
        return [_heading("User", entry.timestamp, session.timezone_name), "", entry.text or ""]
    if entry.kind == "assistant":
        label = f"{session.model or 'Assistant'} Assistant"
        return [_heading(label, entry.timestamp, session.timezone_name), "", entry.text or ""]
    if entry.kind == "commentary":
        label = f"{session.model or 'Assistant'} Commentary"
        return [_heading(label, entry.timestamp, session.timezone_name), "", entry.text or ""]
    if entry.kind == "tool_call":
        tool_label = f"Tool Call · {entry.tool_name or 'unknown'}"
        lines = [_heading(tool_label, entry.timestamp, session.timezone_name)]
        if entry.arguments:
            lines.extend(["", "**Arguments**", _fence_block(entry.arguments)])
        return lines
    output_label = f"Tool Output · {entry.tool_name or 'unknown'}"
    lines = [_heading(output_label, entry.timestamp, session.timezone_name)]
    if entry.output:
        lines.extend(["", _fence_block(entry.output)])
    return lines


def _heading(label: str, timestamp: datetime | None, timezone_name: str | None) -> str:
    formatted_timestamp = _format_timestamp(timestamp, timezone_name)
    if formatted_timestamp is None:
        return f"## {label}"
    return f"## {label} · {formatted_timestamp}"


def _event_label(event_type: str | None) -> str:
    if event_type == "task_started":
        return "Task Started"
    if event_type == "task_complete":
        return "Task Complete"
    return "Event"


def _event_body(event_type: str | None) -> str:
    if event_type == "task_started":
        return "Started work on a new response."
    if event_type == "task_complete":
        return "Completed the response."
    return "Observed a session event."


def _fence_block(raw_text: str) -> str:
    block_language = "text"
    block_body = raw_text.rstrip()
    try:
        parsed = load_json_value(raw_text)
    except json.JSONDecodeError:
        try:
            parsed = load_json_value(raw_text.strip())
        except json.JSONDecodeError:
            parsed = None

    if parsed is not None:
        block_language = "json"
        block_body = json.dumps(parsed, indent=2, sort_keys=True)
    return f"```{block_language}\n{block_body}\n```"


def _format_timestamp(timestamp: datetime | None, timezone_name: str | None) -> str | None:
    if timestamp is None:
        return None
    timezone = _resolve_timezone(timezone_name)
    return timestamp.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S %Z")


def _resolve_timezone(timezone_name: str | None) -> tzinfo:
    if timezone_name is not None:
        try:
            return ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            pass
    return UTC
