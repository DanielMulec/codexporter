from __future__ import annotations

import ntpath
import os
import posixpath
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from codexporter.errors import RolloutAccessError, SessionDiscoveryError
from codexporter.messages import (
    ambiguous_session_message,
    missing_rollout_message,
    missing_session_message,
    missing_targeted_session_message,
    session_workspace_mismatch_message,
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
    state_db = codex_home / "state_5.sqlite"
    if not state_db.is_file():
        raise SessionDiscoveryError(missing_session_message(invocation_cwd))

    query = """
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
    normalized_invocation_cwd = normalize_cwd(invocation_cwd)
    connection = sqlite3.connect(state_db)
    try:
        row = _select_thread_row(
            connection=connection,
            query=query,
            invocation_cwd=invocation_cwd,
            normalized_invocation_cwd=normalized_invocation_cwd,
            session_id=session_id,
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


def _parse_epoch(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, int | float):
        return datetime.fromtimestamp(float(value), tz=UTC)
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


def _select_thread_row(
    connection: sqlite3.Connection,
    query: str,
    invocation_cwd: Path | str,
    normalized_invocation_cwd: str,
    session_id: str | None,
) -> _ThreadRow:
    if session_id is not None:
        row = _fetch_one_thread_row(connection, f"{query} WHERE id = ?", (session_id,))
        if row is None:
            raise SessionDiscoveryError(
                missing_targeted_session_message(session_id, invocation_cwd)
            )
        if normalize_cwd(row.cwd) != normalized_invocation_cwd:
            raise SessionDiscoveryError(
                session_workspace_mismatch_message(
                    session_id=session_id,
                    project_root=invocation_cwd,
                    session_root=row.cwd,
                )
            )
        return row

    rows = _fetch_all_thread_rows(connection, f"{query} ORDER BY updated_at DESC")
    matches = [row for row in rows if normalize_cwd(row.cwd) == normalized_invocation_cwd]
    if not matches:
        raise SessionDiscoveryError(missing_session_message(invocation_cwd))
    if len(matches) > 1:
        raise SessionDiscoveryError(ambiguous_session_message(invocation_cwd))
    return matches[0]


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
