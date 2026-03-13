from __future__ import annotations

import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from codexporter.errors import RolloutAccessError, SessionDiscoveryError
from codexporter.messages import missing_rollout_message, missing_session_message
from codexporter.models import ThreadRecord


def resolve_codex_home(explicit_codex_home: Path | None) -> Path:
    if explicit_codex_home is not None:
        return explicit_codex_home.expanduser().resolve()
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home).expanduser().resolve()
    return Path.home().joinpath(".codex")


def discover_current_thread(invocation_cwd: Path, codex_home: Path) -> ThreadRecord:
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
        WHERE cwd = ?
        ORDER BY updated_at DESC
        LIMIT 1
    """
    connection = sqlite3.connect(state_db)
    connection.row_factory = sqlite3.Row
    try:
        row = connection.execute(query, (str(invocation_cwd),)).fetchone()
    finally:
        connection.close()

    if row is None:
        raise SessionDiscoveryError(missing_session_message(invocation_cwd))

    rollout_path = Path(str(row["rollout_path"])).expanduser()
    if not rollout_path.is_file():
        raise RolloutAccessError(missing_rollout_message(rollout_path))

    return ThreadRecord(
        session_id=str(row["id"]),
        rollout_path=rollout_path,
        created_at=_parse_epoch(row["created_at"]),
        updated_at=_parse_epoch(row["updated_at"]),
        cwd=Path(str(row["cwd"])).expanduser().resolve(),
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
