from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from codexporter.errors import CheckpointError
from codexporter.json_utils import JsonObject, load_json_object
from codexporter.messages import checkpoint_mismatch_message, unreadable_checkpoint_message
from codexporter.models import CheckpointState, ExportEntry, Language, ParsedRollout, SessionInfo

SCHEMA_VERSION = 1
REQUIRED_FIELDS = {
    "schema_version",
    "session_id",
    "session_name",
    "export_sequence",
    "last_exported_record_index",
    "last_exported_event_timestamp",
    "last_exported_turn_id",
    "exported_artifacts",
    "created_at",
    "updated_at",
}


def sidecar_path_for_session(export_dir: Path, session_id: str) -> Path:
    return export_dir / f"{session_id}-checkpoint.json"


def load_checkpoint(path: Path, language: Language) -> CheckpointState | None:
    if not path.exists():
        return None

    try:
        payload: JsonObject = load_json_object(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise CheckpointError(unreadable_checkpoint_message(path, language)) from exc

    if not REQUIRED_FIELDS.issubset(payload):
        raise CheckpointError(unreadable_checkpoint_message(path, language))

    exported_artifacts = payload.get("exported_artifacts")
    if not isinstance(exported_artifacts, list) or not all(
        isinstance(item, str) for item in exported_artifacts
    ):
        raise CheckpointError(unreadable_checkpoint_message(path, language))
    exported_artifact_paths = [item for item in exported_artifacts if isinstance(item, str)]

    try:
        return CheckpointState(
            schema_version=_required_int(payload["schema_version"]),
            session_id=_required_text(payload["session_id"]),
            session_name=(
                _optional_text(payload["session_name"])
                if payload["session_name"] is not None
                else None
            ),
            export_sequence=_required_int(payload["export_sequence"]),
            last_exported_record_index=_required_int(payload["last_exported_record_index"]),
            last_exported_event_timestamp=(
                _optional_text(payload["last_exported_event_timestamp"])
                if payload["last_exported_event_timestamp"] is not None
                else None
            ),
            last_exported_turn_id=(
                _optional_text(payload["last_exported_turn_id"])
                if payload["last_exported_turn_id"] is not None
                else None
            ),
            exported_artifacts=exported_artifact_paths,
            created_at=_required_text(payload["created_at"]),
            updated_at=_required_text(payload["updated_at"]),
        )
    except ValueError as exc:
        raise CheckpointError(unreadable_checkpoint_message(path, language)) from exc


def validate_checkpoint(state: CheckpointState, parsed: ParsedRollout, path: Path) -> None:
    if state.session_id != parsed.session.session_id:
        raise CheckpointError(checkpoint_mismatch_message(path, parsed.session.language))

    entry = parsed.entry_index.get(state.last_exported_record_index)
    if entry is None:
        raise CheckpointError(checkpoint_mismatch_message(path, parsed.session.language))

    if state.last_exported_event_timestamp != _timestamp_to_string(entry.timestamp):
        raise CheckpointError(checkpoint_mismatch_message(path, parsed.session.language))

    if state.last_exported_turn_id != entry.turn_id:
        raise CheckpointError(checkpoint_mismatch_message(path, parsed.session.language))


def build_checkpoint(
    previous: CheckpointState | None,
    session: SessionInfo,
    last_entry: ExportEntry,
    export_path: Path,
    exported_at: datetime,
) -> CheckpointState:
    exported_at_text = _required_timestamp(exported_at)
    created_at = previous.created_at if previous is not None else exported_at_text
    exported_artifacts = list(previous.exported_artifacts) if previous is not None else []
    exported_artifacts.append(str(export_path))
    return CheckpointState(
        schema_version=SCHEMA_VERSION,
        session_id=session.session_id,
        session_name=session.session_name,
        export_sequence=(previous.export_sequence + 1) if previous is not None else 1,
        last_exported_record_index=last_entry.source_index,
        last_exported_event_timestamp=_timestamp_to_string(last_entry.timestamp),
        last_exported_turn_id=last_entry.turn_id,
        exported_artifacts=exported_artifacts,
        created_at=created_at,
        updated_at=exported_at_text,
    )


def checkpoint_to_json(state: CheckpointState) -> str:
    return json.dumps(state.to_dict(), indent=2, sort_keys=True) + "\n"


def _timestamp_to_string(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _required_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _required_int(value: object) -> int:
    if isinstance(value, bool):
        raise ValueError("Checkpoint payload used a boolean where an integer is required.")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        return int(value)
    raise ValueError("Checkpoint payload used an unsupported numeric shape.")


def _required_text(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("Checkpoint payload used an unsupported text shape.")
    return value


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    return _required_text(value)
