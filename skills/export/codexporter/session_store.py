from __future__ import annotations

import ntpath
import os
import posixpath
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from codexporter.errors import RolloutAccessError, SessionDiscoveryError
from codexporter.json_utils import load_json_object
from codexporter.messages import (
    ambiguous_session_message,
    missing_rollout_message,
    missing_session_message,
    missing_targeted_rollout_message,
    missing_targeted_session_message,
    session_workspace_mismatch_message,
    stale_session_index_message,
)
from codexporter.models import ThreadRecord


@dataclass(frozen=True)
class _ThreadRow:
    session_id: str
    rollout_path: str
    created_at: object
    updated_at: object
    source: str | None
    model_provider: str | None
    cwd: str
    title: str | None
    sandbox_policy: str | None
    approval_mode: str | None
    cli_version: str | None


@dataclass(frozen=True)
class _RolloutHeader:
    rollout_path: Path
    session_id: str | None
    cwd: str | None
    timestamp: datetime | None
    source: str | None
    model_provider: str | None
    cli_version: str | None


_THREAD_QUERY = """
    SELECT
        id,
        rollout_path,
        created_at,
        updated_at,
        source,
        model_provider,
        cwd,
        title,
        sandbox_policy,
        approval_mode,
        cli_version
    FROM threads
"""


def resolve_codex_home(explicit_codex_home: Path | None) -> Path:
    if explicit_codex_home is not None:
        return explicit_codex_home.expanduser().resolve()
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home).expanduser().resolve()
    return Path.home().joinpath(".codex")


def discover_current_thread(
    invocation_cwd: Path | str,
    codex_home: Path,
    session_id: str | None = None,
) -> ThreadRecord:
    normalized_invocation_cwd = normalize_cwd(invocation_cwd)
    if session_id is not None:
        return _discover_targeted_thread(
            invocation_cwd=invocation_cwd,
            codex_home=codex_home,
            normalized_invocation_cwd=normalized_invocation_cwd,
            session_id=session_id,
        )

    state_db = codex_home / "state_5.sqlite"
    if not state_db.is_file():
        raise SessionDiscoveryError(missing_session_message(invocation_cwd))

    connection = sqlite3.connect(state_db)
    try:
        row = _select_workspace_thread_row(
            connection=connection,
            invocation_cwd=invocation_cwd,
            normalized_invocation_cwd=normalized_invocation_cwd,
            codex_home=codex_home,
        )
    finally:
        connection.close()

    rollout_path = Path(row.rollout_path).expanduser()
    if not rollout_path.is_file():
        raise RolloutAccessError(missing_rollout_message(rollout_path))

    return ThreadRecord(
        session_id=row.session_id,
        rollout_path=rollout_path,
        created_at=_parse_epoch(row.created_at),
        updated_at=_parse_epoch(row.updated_at),
        cwd=Path(row.cwd).expanduser(),
        title=row.title,
        source=row.source,
        model_provider=row.model_provider,
        cli_version=row.cli_version,
        approval_mode=row.approval_mode,
        sandbox_policy=row.sandbox_policy,
    )


def _discover_targeted_thread(
    invocation_cwd: Path | str,
    codex_home: Path,
    normalized_invocation_cwd: str,
    session_id: str,
) -> ThreadRecord:
    row = _load_optional_thread_row(codex_home, session_id)
    rollout_header = _select_targeted_rollout_header(
        codex_home=codex_home,
        session_id=session_id,
        normalized_invocation_cwd=normalized_invocation_cwd,
        invocation_cwd=invocation_cwd,
        row=row,
    )

    metadata_row = (
        row if row is not None and normalize_cwd(row.cwd) == normalized_invocation_cwd else None
    )
    created_at = _parse_epoch(metadata_row.created_at) if metadata_row is not None else None
    updated_at = _parse_epoch(metadata_row.updated_at) if metadata_row is not None else None
    rollout_cwd = rollout_header.cwd or str(invocation_cwd)

    return ThreadRecord(
        session_id=session_id,
        rollout_path=rollout_header.rollout_path,
        created_at=created_at or rollout_header.timestamp,
        updated_at=updated_at or rollout_header.timestamp,
        cwd=Path(rollout_cwd).expanduser(),
        title=metadata_row.title if metadata_row is not None else None,
        source=rollout_header.source or (metadata_row.source if metadata_row is not None else None),
        model_provider=rollout_header.model_provider
        or (metadata_row.model_provider if metadata_row is not None else None),
        cli_version=rollout_header.cli_version
        or (metadata_row.cli_version if metadata_row is not None else None),
        approval_mode=metadata_row.approval_mode if metadata_row is not None else None,
        sandbox_policy=metadata_row.sandbox_policy if metadata_row is not None else None,
    )


def _parse_epoch(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, int | float):
        return datetime.fromtimestamp(float(value), tz=UTC)
    return None


def _parse_iso_timestamp(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_cwd(path: Path | str) -> str:
    raw = str(path).strip()
    if not raw:
        return raw

    # Codex on Windows may persist extended-length paths that still refer to the
    # same workspace as the plain drive-letter form used by the invoking shell.
    if raw.startswith("\\\\?\\UNC\\"):
        raw = "\\\\" + raw.removeprefix("\\\\?\\UNC\\")
    elif raw.startswith("\\\\?\\"):
        raw = raw.removeprefix("\\\\?\\")

    if _looks_like_windows_path(raw):
        normalized = ntpath.normcase(ntpath.normpath(raw))
        return normalized.rstrip("\\/") or normalized

    normalized = posixpath.normpath(raw)
    return normalized if normalized == "/" else normalized.rstrip("/")


def _looks_like_windows_path(path: str) -> bool:
    return path.startswith("\\\\") or (len(path) >= 3 and path[1] == ":" and path[2] in ("\\", "/"))


def _select_workspace_thread_row(
    connection: sqlite3.Connection,
    invocation_cwd: Path | str,
    normalized_invocation_cwd: str,
    codex_home: Path,
) -> _ThreadRow:
    rows = _fetch_all_thread_rows(connection, f"{_THREAD_QUERY} ORDER BY updated_at DESC")
    matches = [row for row in rows if normalize_cwd(row.cwd) == normalized_invocation_cwd]
    if not matches:
        if _workspace_rollout_exists(codex_home, normalized_invocation_cwd):
            raise SessionDiscoveryError(stale_session_index_message(invocation_cwd))
        raise SessionDiscoveryError(missing_session_message(invocation_cwd))
    if len(matches) > 1:
        raise SessionDiscoveryError(ambiguous_session_message(invocation_cwd))
    return matches[0]


def _select_targeted_rollout_header(
    codex_home: Path,
    session_id: str,
    normalized_invocation_cwd: str,
    invocation_cwd: Path | str,
    row: _ThreadRow | None,
) -> _RolloutHeader:
    candidates = _targeted_rollout_candidates(codex_home, session_id, row)
    matching_headers = _matching_targeted_headers(candidates, session_id)
    if not matching_headers:
        _raise_missing_targeted_rollout(
            row=row,
            session_id=session_id,
            invocation_cwd=invocation_cwd,
            normalized_invocation_cwd=normalized_invocation_cwd,
        )

    matching_workspace = _matching_workspace_headers(
        matching_headers=matching_headers,
        normalized_invocation_cwd=normalized_invocation_cwd,
    )
    if not matching_workspace:
        raise SessionDiscoveryError(
            session_workspace_mismatch_message(
                session_id=session_id,
                project_root=invocation_cwd,
                session_root=matching_headers[0].cwd or "<unknown>",
            )
        )
    matching_workspace.sort(
        key=lambda header: (
            _timestamp_sort_value(header.timestamp),
            _safe_mtime(header.rollout_path),
        ),
        reverse=True,
    )
    return matching_workspace[0]


def _matching_targeted_headers(
    candidates: list[Path],
    session_id: str,
) -> list[_RolloutHeader]:
    matching_headers: list[_RolloutHeader] = []
    for candidate in candidates:
        header = _read_rollout_header(candidate)
        if header is None:
            continue
        if header.session_id != session_id or header.cwd is None:
            continue
        matching_headers.append(header)
    return matching_headers


def _matching_workspace_headers(
    matching_headers: list[_RolloutHeader],
    normalized_invocation_cwd: str,
) -> list[_RolloutHeader]:
    matching_workspace: list[_RolloutHeader] = []
    for header in matching_headers:
        session_root = header.cwd
        if session_root is None:
            continue
        if normalize_cwd(session_root) == normalized_invocation_cwd:
            matching_workspace.append(header)
    return matching_workspace


def _raise_missing_targeted_rollout(
    row: _ThreadRow | None,
    session_id: str,
    invocation_cwd: Path | str,
    normalized_invocation_cwd: str,
) -> None:
    if row is not None:
        if normalize_cwd(row.cwd) != normalized_invocation_cwd:
            raise SessionDiscoveryError(
                session_workspace_mismatch_message(
                    session_id=session_id,
                    project_root=invocation_cwd,
                    session_root=row.cwd,
                )
            )
        rollout_path = Path(row.rollout_path).expanduser()
        if rollout_path.is_file():
            raise SessionDiscoveryError(
                missing_targeted_session_message(session_id, invocation_cwd)
            )
    raise SessionDiscoveryError(missing_targeted_rollout_message(session_id, invocation_cwd))


def _targeted_rollout_candidates(
    codex_home: Path,
    session_id: str,
    row: _ThreadRow | None,
) -> list[Path]:
    sessions_root = codex_home / "sessions"
    candidates: dict[str, Path] = {}
    if sessions_root.is_dir():
        for path in sessions_root.rglob(f"rollout-*-{session_id}.jsonl"):
            candidates[str(path)] = path

    if row is not None:
        row_rollout_path = Path(row.rollout_path).expanduser()
        if row_rollout_path.is_file():
            candidates[str(row_rollout_path)] = row_rollout_path

    if not candidates and sessions_root.is_dir():
        for path in sessions_root.rglob("rollout*.jsonl"):
            candidates[str(path)] = path

    return list(candidates.values())


def _workspace_rollout_exists(codex_home: Path, normalized_invocation_cwd: str) -> bool:
    sessions_root = codex_home / "sessions"
    if not sessions_root.is_dir():
        return False
    for rollout_path in sessions_root.rglob("rollout*.jsonl"):
        header = _read_rollout_header(rollout_path)
        if header is None or header.cwd is None:
            continue
        if normalize_cwd(header.cwd) == normalized_invocation_cwd:
            return True
    return False


def _read_rollout_header(rollout_path: Path) -> _RolloutHeader | None:
    try:
        with rollout_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped:
                    continue
                record = load_json_object(stripped)
                if _as_str(record.get("type")) != "session_meta":
                    continue
                payload = _as_json_object(record.get("payload"))
                return _RolloutHeader(
                    rollout_path=rollout_path,
                    session_id=_as_str(payload.get("id")),
                    cwd=_as_str(payload.get("cwd")),
                    timestamp=_parse_iso_timestamp(_as_str(record.get("timestamp"))),
                    source=_as_str(payload.get("source")),
                    model_provider=_as_str(payload.get("model_provider")),
                    cli_version=_as_str(payload.get("cli_version")),
                )
    except (OSError, ValueError):
        return None
    return None


def _as_json_object(value: object) -> dict[str, object]:
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    return {}


def _timestamp_sort_value(value: datetime | None) -> float:
    if value is None:
        return float("-inf")
    return value.timestamp()


def _safe_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return float("-inf")


def _load_optional_thread_row(codex_home: Path, session_id: str) -> _ThreadRow | None:
    state_db = codex_home / "state_5.sqlite"
    if not state_db.is_file():
        return None
    connection = sqlite3.connect(state_db)
    try:
        return _fetch_one_thread_row(connection, f"{_THREAD_QUERY} WHERE id = ?", (session_id,))
    except sqlite3.Error:
        return None
    finally:
        connection.close()


def _fetch_one_thread_row(
    connection: sqlite3.Connection,
    query: str,
    parameters: tuple[str, ...],
) -> _ThreadRow | None:
    cursor = connection.execute(query, parameters)
    raw_row: object | None = cursor.fetchone()
    if raw_row is None:
        return None
    return _coerce_thread_row(raw_row)


def _fetch_all_thread_rows(
    connection: sqlite3.Connection,
    query: str,
) -> list[_ThreadRow]:
    cursor = connection.execute(query)
    raw_rows: list[object] = cursor.fetchall()
    return [_coerce_thread_row(raw_row) for raw_row in raw_rows]


def _coerce_thread_row(raw_row: object) -> _ThreadRow:
    row = _as_row_tuple(raw_row)
    if len(row) != 11:
        raise ValueError("Unexpected thread row shape.")

    return _ThreadRow(
        session_id=str(row[0]),
        rollout_path=str(row[1]),
        created_at=row[2],
        updated_at=row[3],
        source=_optional_text(row[4]),
        model_provider=_optional_text(row[5]),
        cwd=str(row[6]),
        title=_optional_text(row[7]),
        sandbox_policy=_optional_text(row[8]),
        approval_mode=_optional_text(row[9]),
        cli_version=_optional_text(row[10]),
    )


def _as_row_tuple(value: object) -> tuple[object, ...]:
    if not isinstance(value, tuple):
        raise ValueError("Unexpected sqlite row type.")
    return value


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _as_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    return None
