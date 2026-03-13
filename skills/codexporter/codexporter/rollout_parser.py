from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from codexporter.errors import RolloutAccessError
from codexporter.messages import detect_language, missing_rollout_message
from codexporter.models import ExportEntry, ParsedRollout, SessionInfo, ThreadRecord


@dataclass
class _ParserState:
    session_meta: dict[str, object]
    latest_turn_context: dict[str, object]
    active_turn_id: str | None
    tool_names_by_call_id: dict[str, str]
    entries: list[ExportEntry]
    visible_user_messages: list[str]


def parse_rollout(thread: ThreadRecord) -> ParsedRollout:
    state = _ParserState(
        session_meta={},
        latest_turn_context={},
        active_turn_id=None,
        tool_names_by_call_id={},
        entries=[],
        visible_user_messages=[],
    )

    for source_index, line in enumerate(_read_rollout_lines(thread.rollout_path)):
        _process_record(source_index, line, state, thread.rollout_path)

    session_started_at = _parse_timestamp(state.session_meta.get("timestamp")) or thread.created_at
    approval_policy = _as_str(state.latest_turn_context.get("approval_policy"))
    sandbox_policy = _stringify_optional(state.latest_turn_context.get("sandbox_policy"))
    session = SessionInfo(
        session_id=_as_str(state.session_meta.get("id")) or thread.session_id,
        session_name=_normalize_session_name(thread.title),
        session_started_at=session_started_at,
        cwd=Path(
            _as_str(state.latest_turn_context.get("cwd"))
            or _as_str(state.session_meta.get("cwd"))
            or str(thread.cwd)
        ),
        source=_as_str(state.session_meta.get("source")) or thread.source,
        originator=_as_str(state.session_meta.get("originator")),
        model=_as_str(state.latest_turn_context.get("model")),
        model_provider=_as_str(state.session_meta.get("model_provider")) or thread.model_provider,
        cli_version=_as_str(state.session_meta.get("cli_version")) or thread.cli_version,
        timezone_name=_as_str(state.latest_turn_context.get("timezone")),
        approval_policy=approval_policy or thread.approval_mode,
        sandbox_policy=sandbox_policy or thread.sandbox_policy,
        language=detect_language(state.visible_user_messages),
    )
    entry_index = {entry.source_index: entry for entry in state.entries}
    return ParsedRollout(session=session, entries=tuple(state.entries), entry_index=entry_index)


def _read_rollout_lines(rollout_path: Path) -> list[str]:
    try:
        lines = rollout_path.read_text(encoding="utf-8").splitlines()
        return [line for line in lines if line.strip()]
    except OSError as exc:
        raise RolloutAccessError(missing_rollout_message(rollout_path)) from exc


def _process_record(
    source_index: int,
    line: str,
    state: _ParserState,
    rollout_path: Path,
) -> None:
    try:
        record = json.loads(line)
    except json.JSONDecodeError as exc:
        raise RolloutAccessError(missing_rollout_message(rollout_path)) from exc

    timestamp = _parse_timestamp(record.get("timestamp"))
    record_type = _as_str(record.get("type"))
    payload = _as_dict(record.get("payload"))

    if record_type == "session_meta":
        state.session_meta = payload
        return

    if record_type == "turn_context":
        state.latest_turn_context = payload
        state.active_turn_id = _as_str(payload.get("turn_id"))
        return

    if record_type == "event_msg":
        _append_event_entry(source_index, timestamp, payload, state)
        return

    if record_type == "response_item":
        _append_response_entry(source_index, timestamp, payload, state)


def _append_event_entry(
    source_index: int,
    timestamp: datetime | None,
    payload: dict[str, object],
    state: _ParserState,
) -> None:
    event_type = _as_str(payload.get("type"))
    if event_type not in {"task_started", "task_complete"}:
        return
    state.entries.append(
        ExportEntry(
            source_index=source_index,
            kind="event",
            timestamp=timestamp,
            turn_id=_as_str(payload.get("turn_id")) or state.active_turn_id,
            event_type=event_type,
        )
    )


def _append_response_entry(
    source_index: int,
    timestamp: datetime | None,
    payload: dict[str, object],
    state: _ParserState,
) -> None:
    payload_type = _as_str(payload.get("type"))
    if payload_type == "message":
        _append_message_entry(source_index, timestamp, payload, state)
        return
    if payload_type == "reasoning":
        return
    if payload_type in {"custom_tool_call", "function_call", "web_search_call"}:
        _append_tool_call_entry(source_index, timestamp, payload, state)
        return
    if payload_type in {"custom_tool_call_output", "function_call_output"}:
        _append_tool_output_entry(source_index, timestamp, payload, state)


def _append_message_entry(
    source_index: int,
    timestamp: datetime | None,
    payload: dict[str, object],
    state: _ParserState,
) -> None:
    role = _as_str(payload.get("role"))
    text = _extract_message_text(payload.get("content"))
    if role == "user":
        if text and not _is_internal_user_message(text):
            state.entries.append(
                ExportEntry(
                    source_index=source_index,
                    kind="user",
                    timestamp=timestamp,
                    turn_id=state.active_turn_id,
                    text=text,
                )
            )
            state.visible_user_messages.append(text)
        return
    if role == "assistant" and text:
        if _as_str(payload.get("phase")) == "commentary":
            state.entries.append(
                ExportEntry(
                    source_index=source_index,
                    kind="commentary",
                    timestamp=timestamp,
                    turn_id=state.active_turn_id,
                    text=text,
                )
            )
        else:
            state.entries.append(
                ExportEntry(
                    source_index=source_index,
                    kind="assistant",
                    timestamp=timestamp,
                    turn_id=state.active_turn_id,
                    text=text,
                )
            )


def _append_tool_call_entry(
    source_index: int,
    timestamp: datetime | None,
    payload: dict[str, object],
    state: _ParserState,
) -> None:
    tool_name, arguments, call_id = _parse_tool_call(payload)
    if call_id is not None:
        state.tool_names_by_call_id[call_id] = tool_name
    state.entries.append(
        ExportEntry(
            source_index=source_index,
            kind="tool_call",
            timestamp=timestamp,
            turn_id=state.active_turn_id,
            tool_name=tool_name,
            arguments=arguments,
        )
    )


def _append_tool_output_entry(
    source_index: int,
    timestamp: datetime | None,
    payload: dict[str, object],
    state: _ParserState,
) -> None:
    call_id = _as_str(payload.get("call_id"))
    state.entries.append(
        ExportEntry(
            source_index=source_index,
            kind="tool_output",
            timestamp=timestamp,
            turn_id=state.active_turn_id,
            tool_name=state.tool_names_by_call_id.get(call_id or "", "unknown"),
            output=_extract_tool_output(payload.get("output")),
        )
    )


def _parse_tool_call(payload: dict[str, object]) -> tuple[str, str | None, str | None]:
    payload_type = _as_str(payload.get("type"))
    if payload_type == "function_call":
        return (
            _as_str(payload.get("name")) or "function_call",
            _as_str(payload.get("arguments")),
            _as_str(payload.get("call_id")),
        )
    if payload_type == "custom_tool_call":
        return (
            _as_str(payload.get("name")) or "custom_tool_call",
            _as_str(payload.get("input")),
            _as_str(payload.get("call_id")),
        )
    web_search_payload = dict(payload)
    web_search_payload.pop("status", None)
    return (
        "web_search",
        json.dumps(web_search_payload, indent=2, sort_keys=True),
        _as_str(payload.get("call_id")),
    )


def _extract_message_text(content: object) -> str | None:
    if not isinstance(content, list):
        return None
    chunks: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = _as_str(item.get("type"))
        if item_type not in {"input_text", "output_text"}:
            continue
        text = _as_str(item.get("text"))
        if text:
            chunks.append(text.rstrip())
    combined = "\n\n".join(chunk for chunk in chunks if chunk)
    return combined or None


def _extract_tool_output(output: object) -> str | None:
    if isinstance(output, str):
        return output.rstrip()
    if isinstance(output, dict | list):
        return json.dumps(output, indent=2, sort_keys=True)
    return None


def _is_internal_user_message(text: str) -> bool:
    stripped = text.strip()
    if stripped.startswith("# AGENTS.md instructions for "):
        return True
    return "<INSTRUCTIONS>" in stripped and "Collaboration Charter" in stripped


def _normalize_session_name(title: str | None) -> str | None:
    if title is None:
        return None
    first_line = title.splitlines()[0].strip()
    return first_line or None


def _parse_timestamp(value: object) -> datetime | None:
    timestamp = _as_str(value)
    if timestamp is None:
        return None
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def _as_dict(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    return {}


def _as_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    return None


def _stringify_optional(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)
