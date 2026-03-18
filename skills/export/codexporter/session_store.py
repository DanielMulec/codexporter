from __future__ import annotations

import ntpath
import os
import posixpath
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from codexporter.errors import RolloutAccessError, SessionDiscoveryError
from codexporter.messages import (
    ambiguous_session_message,
    missing_rollout_message,
    missing_session_message,
    missing_targeted_session_message,
    session_workspace_mismatch_message,
)
from codexporter.models import ThreadRecord


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
    connection.row_factory = sqlite3.Row
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

    rollout_path = Path(str(row["rollout_path"])).expanduser()
    if not rollout_path.is_file():
        raise RolloutAccessError(missing_rollout_message(rollout_path))

    return ThreadRecord(
        session_id=str(row["id"]),
        rollout_path=rollout_path,
        created_at=_parse_epoch(row["created_at"]),
        updated_at=_parse_epoch(row["updated_at"]),
        cwd=Path(str(row["cwd"])).expanduser(),
        title=str(row["title"]) if row["title"] is not None else None,
        source=str(row["source"]) if row["source"] is not None else None,
        model_provider=str(row["model_provider"]) if row["model_provider"] is not None else None,
        cli_version=str(row["cli_version"]) if row["cli_version"] is not None else None,
        approval_mode=str(row["approval_mode"]) if row["approval_mode"] is not None else None,
        sandbox_policy=str(row["sandbox_policy"]) if row["sandbox_policy"] is not None else None,
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
    return path.startswith("\\\\") or (
        len(path) >= 3 and path[1] == ":" and path[2] in ("\\", "/")
    )


def _select_thread_row(
    connection: sqlite3.Connection,
    query: str,
    invocation_cwd: Path | str,
    normalized_invocation_cwd: str,
    session_id: str | None,
) -> sqlite3.Row:
    if session_id is not None:
        row = cast(
            sqlite3.Row | None,
            connection.execute(f"{query} WHERE id = ?", (session_id,)).fetchone(),
        )
        if row is None:
            raise SessionDiscoveryError(
                missing_targeted_session_message(session_id, invocation_cwd)
            )
        if normalize_cwd(str(row["cwd"])) != normalized_invocation_cwd:
            raise SessionDiscoveryError(
                session_workspace_mismatch_message(
                    session_id=session_id,
                    project_root=invocation_cwd,
                    session_root=str(row["cwd"]),
                )
            )
        return row

    rows = cast(
        list[sqlite3.Row],
        connection.execute(f"{query} ORDER BY updated_at DESC").fetchall(),
    )
    matches = [row for row in rows if normalize_cwd(str(row["cwd"])) == normalized_invocation_cwd]
    if not matches:
        raise SessionDiscoveryError(missing_session_message(invocation_cwd))
    if len(matches) > 1:
        raise SessionDiscoveryError(ambiguous_session_message(invocation_cwd))
    return matches[0]
