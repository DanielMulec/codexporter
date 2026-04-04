from __future__ import annotations

import json
import re
import shlex
from dataclasses import dataclass, replace
from typing import TypeGuard

from codexporter.json_utils import JsonObject, JsonValue, load_json_value
from codexporter.models import ExportEntry, RenderProfile

SHORT_DIFF_MAX_LINES = 60
SHORT_DIFF_MAX_FILES = 2
GENERIC_OUTPUT_MAX_LINES = 120
GENERIC_OUTPUT_MAX_CHARS = 8000
_COMMAND_TOOL_NAMES = frozenset({"exec_command", "shell_command"})
_CONTROL_TOKENS = frozenset({"&&", "||", "|", ";", ">", ">>", "<", "2>", "&>"})
_FILE_READ_COMMANDS = frozenset({"awk", "bat", "cat", "head", "less", "more", "nl", "sed", "tail"})
_LISTING_COMMANDS = frozenset({"find", "ls", "tree"})
_DIFF_HEADER_PATTERN = re.compile(r"^diff --git a/(.+?) b/(.+)$")
_PATCH_FILE_PREFIXES = (
    "*** Add File: ",
    "*** Delete File: ",
    "*** Update File: ",
)


@dataclass(frozen=True)
class _CommandDetails:
    raw_command: str
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class _DiffFileSummary:
    path: str
    additions: int | None
    deletions: int | None


def prepare_entries_for_render(
    entries: tuple[ExportEntry, ...],
    render_profile: RenderProfile,
) -> tuple[ExportEntry, ...]:
    if render_profile == "full":
        return entries

    calls_by_id = {
        entry.call_id: entry
        for entry in entries
        if entry.kind == "tool_call" and entry.call_id is not None
    }
    return tuple(_compact_entry(entry, calls_by_id) for entry in entries)


def _compact_entry(
    entry: ExportEntry,
    calls_by_id: dict[str, ExportEntry],
) -> ExportEntry:
    if entry.kind == "tool_call":
        return _compact_tool_call(entry)
    if entry.kind == "tool_output":
        return _compact_tool_output(entry, calls_by_id)
    return entry


def _compact_tool_call(entry: ExportEntry) -> ExportEntry:
    if entry.tool_name != "apply_patch" or not entry.arguments:
        return entry
    summary_lines = ["Raw patch omitted in compact mode."]
    patch_files = _extract_patch_files(entry.arguments)
    if patch_files:
        summary_lines.append("Patched files:")
        summary_lines.extend(f"- {path}" for path in patch_files)
    summary_lines.append(f"Suppressed lines: {_count_lines(entry.arguments)}")
    return replace(entry, arguments="\n".join(summary_lines))


def _compact_tool_output(
    entry: ExportEntry,
    calls_by_id: dict[str, ExportEntry],
) -> ExportEntry:
    if not entry.output:
        return entry

    call_entry = calls_by_id.get(entry.call_id or "")
    if _is_file_read_call(call_entry):
        return replace(entry, output=_build_file_read_summary(call_entry, entry.output))

    if _is_raw_diff_output(call_entry, entry.output):
        if _should_keep_diff_verbatim(entry.output):
            return entry
        return replace(entry, output=_build_diff_summary(entry.output))

    generic_summary = _build_generic_output_summary(call_entry, entry.output)
    if generic_summary is not None:
        return replace(entry, output=generic_summary)
    return entry


def _is_file_read_call(entry: ExportEntry | None) -> bool:
    command_details = _parse_command_invocation(entry)
    if command_details is None or not command_details.tokens:
        return False
    return command_details.tokens[0] in _FILE_READ_COMMANDS


def _is_raw_diff_output(entry: ExportEntry | None, output: str) -> bool:
    if "diff --git " in output:
        return True
    command_details = _parse_command_invocation(entry)
    if command_details is None or not command_details.tokens:
        return False
    command = command_details.tokens
    if len(command) < 2 or command[0] != "git":
        return False
    if command[1] not in {"diff", "show", "log"}:
        return False
    if any(flag in command for flag in ("--stat", "--name-only", "--name-status", "--shortstat")):
        return False
    return True


def _should_keep_diff_verbatim(output: str) -> bool:
    file_summaries = _parse_diff_file_summaries(output)
    return (
        _count_lines(output) <= SHORT_DIFF_MAX_LINES and len(file_summaries) <= SHORT_DIFF_MAX_FILES
    )


def _build_file_read_summary(call_entry: ExportEntry | None, output: str) -> str:
    summary_lines = ["Raw file contents omitted in compact mode."]
    read_files = _extract_read_files(call_entry)
    if read_files:
        summary_lines.append("Read files:")
        summary_lines.extend(f"- {path}" for path in read_files)
    summary_lines.append(f"Suppressed lines: {_count_lines(output)}")
    return "\n".join(summary_lines)


def _build_diff_summary(output: str) -> str:
    summary_lines = ["Raw diff omitted in compact mode."]
    file_summaries = _parse_diff_file_summaries(output)
    if file_summaries:
        summary_lines.append("Changed files:")
        summary_lines.extend(f"- {_format_diff_file_summary(item)}" for item in file_summaries)
    summary_lines.append(f"Suppressed lines: {_count_lines(output)}")
    return "\n".join(summary_lines)


def _build_generic_output_summary(
    call_entry: ExportEntry | None,
    output: str,
) -> str | None:
    if _count_lines(output) <= GENERIC_OUTPUT_MAX_LINES and len(output) <= GENERIC_OUTPUT_MAX_CHARS:
        return None

    command_details = _parse_command_invocation(call_entry)
    if _is_listing_command(command_details):
        heading = "Large raw file listing omitted in compact mode."
    elif _looks_like_json(output):
        heading = "Large raw JSON output omitted in compact mode."
    else:
        heading = "Large raw tool output omitted in compact mode."

    return f"{heading}\nSuppressed lines: {_count_lines(output)}"


def _parse_command_invocation(entry: ExportEntry | None) -> _CommandDetails | None:
    if entry is None or entry.tool_name not in _COMMAND_TOOL_NAMES or not entry.arguments:
        return None
    raw_command = _extract_raw_command(entry.arguments)
    if raw_command is None:
        return None
    try:
        tokens = tuple(_truncate_control_sequence(shlex.split(raw_command)))
    except ValueError:
        tokens = tuple(_truncate_control_sequence(raw_command.strip().split()))
    return _CommandDetails(raw_command=raw_command, tokens=tokens)


def _extract_raw_command(arguments: str) -> str | None:
    stripped_arguments = arguments.strip()
    if not stripped_arguments:
        return None
    try:
        payload = load_json_value(arguments)
    except json.JSONDecodeError:
        return stripped_arguments

    if isinstance(payload, dict):
        return _extract_command_from_payload(payload)
    if isinstance(payload, str) and payload.strip():
        return payload
    return None


def _extract_command_from_payload(payload: JsonObject) -> str | None:
    for key in ("cmd", "command"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    argv_value = payload.get("argv")
    if _is_string_sequence(argv_value):
        return " ".join(argv_value)
    return None


def _is_string_sequence(value: JsonValue) -> TypeGuard[list[str]]:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _truncate_control_sequence(tokens: list[str]) -> list[str]:
    truncated: list[str] = []
    for token in tokens:
        if token in _CONTROL_TOKENS:
            break
        truncated.append(token)
    return truncated


def _extract_read_files(entry: ExportEntry | None) -> tuple[str, ...]:
    command_details = _parse_command_invocation(entry)
    if command_details is None or not command_details.tokens:
        return ()
    command = command_details.tokens[0]
    arguments = list(command_details.tokens[1:])

    if command == "cat":
        return _unique_paths(_non_option_tokens(arguments))
    if command == "sed":
        return _unique_paths(_sed_file_tokens(arguments))
    if command == "awk":
        return _unique_paths(_script_then_paths(arguments))
    if command in {"head", "tail"}:
        return _unique_paths(_head_tail_paths(arguments))
    if command in {"nl", "bat", "less", "more"}:
        return _unique_paths(_non_option_tokens(arguments))
    return ()


def _non_option_tokens(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token and not token.startswith("-")]


def _sed_file_tokens(tokens: list[str]) -> list[str]:
    remaining = list(tokens)
    while remaining and remaining[0].startswith("-"):
        option = remaining.pop(0)
        if option in {"-e", "-f"} and remaining:
            remaining.pop(0)
    if remaining:
        remaining.pop(0)
    return [token for token in remaining if token and not token.startswith("-")]


def _script_then_paths(tokens: list[str]) -> list[str]:
    remaining = list(tokens)
    while remaining and remaining[0].startswith("-"):
        option = remaining.pop(0)
        if option in {"-f", "-v"} and remaining:
            remaining.pop(0)
    if remaining:
        remaining.pop(0)
    return [token for token in remaining if token and not token.startswith("-")]


def _head_tail_paths(tokens: list[str]) -> list[str]:
    remaining = list(tokens)
    paths: list[str] = []
    index = 0
    while index < len(remaining):
        token = remaining[index]
        if token in {"-n", "-c"}:
            index += 2
            continue
        if token.startswith(("-n", "-c", "-")):
            index += 1
            continue
        paths.append(token)
        index += 1
    return paths


def _unique_paths(values: list[str]) -> tuple[str, ...]:
    unique: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return tuple(unique)


def _extract_patch_files(raw_patch: str) -> tuple[str, ...]:
    files: list[str] = []
    for line in raw_patch.splitlines():
        if line.startswith(_PATCH_FILE_PREFIXES):
            files.append(line.split(": ", maxsplit=1)[1].strip())
            continue
        if line.startswith("*** Move to: "):
            files.append(line.removeprefix("*** Move to: ").strip())
    return _unique_paths(files)


def _parse_diff_file_summaries(output: str) -> tuple[_DiffFileSummary, ...]:
    stats_by_path: dict[str, list[int | None]] = {}
    order: list[str] = []
    current_path: str | None = None

    for line in output.splitlines():
        match = _DIFF_HEADER_PATTERN.match(line)
        if match is not None:
            current_path = match.group(2)
            if current_path not in stats_by_path:
                stats_by_path[current_path] = [0, 0]
                order.append(current_path)
            continue
        if current_path is None:
            continue
        if line.startswith("Binary files "):
            stats_by_path[current_path] = [None, None]
            continue
        if line.startswith(("+++", "---")):
            continue
        if line.startswith("+") and stats_by_path[current_path][0] is not None:
            stats_by_path[current_path][0] = int(stats_by_path[current_path][0] or 0) + 1
            continue
        if line.startswith("-") and stats_by_path[current_path][1] is not None:
            stats_by_path[current_path][1] = int(stats_by_path[current_path][1] or 0) + 1

    return tuple(
        _DiffFileSummary(
            path=path,
            additions=_as_optional_int(stats_by_path[path][0]),
            deletions=_as_optional_int(stats_by_path[path][1]),
        )
        for path in order
    )


def _as_optional_int(value: int | None) -> int | None:
    if value is None:
        return None
    return int(value)


def _format_diff_file_summary(summary: _DiffFileSummary) -> str:
    if summary.additions is None or summary.deletions is None:
        return summary.path
    return f"{summary.path} +{summary.additions} -{summary.deletions}"


def _is_listing_command(command_details: _CommandDetails | None) -> bool:
    if command_details is None or not command_details.tokens:
        return False
    command = command_details.tokens
    if command[0] in _LISTING_COMMANDS:
        return True
    return command[0] == "rg" and len(command) > 1 and command[1] == "--files"


def _looks_like_json(output: str) -> bool:
    stripped = output.strip()
    if not stripped.startswith(("{", "[")):
        return False
    try:
        json.loads(stripped)
    except json.JSONDecodeError:
        return False
    return True


def _count_lines(text: str) -> int:
    return len(text.splitlines()) or 1
