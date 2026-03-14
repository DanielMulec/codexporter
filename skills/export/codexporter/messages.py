from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from codexporter.models import Language

GERMAN_MARKERS = (
    " bitte ",
    " danke",
    " und ",
    " nicht ",
    " jetzt ",
    " noch ",
    " soll ",
    " kann ",
    "wieso",
    "warum",
    "läuft",
    "für",
)


def detect_language(samples: Iterable[str]) -> Language:
    combined = " ".join(samples).strip().lower()
    if any(marker in combined for marker in GERMAN_MARKERS) or any(
        char in combined for char in ("ä", "ö", "ü", "ß")
    ):
        return "de"
    return "en"


def success_message(path: Path, incremental: bool, language: Language) -> str:
    if language == "de":
        if incremental:
            return f"Inkrementellen Export {path.name} unter {path} erstellt."
        return f"Aktuellen Sitzungsverlauf nach {path} exportiert. Datei: {path.name}."
    if incremental:
        return f"Created incremental export {path.name} at {path}."
    return f"Exported the current session to {path}. File: {path.name}."


def no_new_content_message(language: Language) -> str:
    if language == "de":
        return (
            "Es gibt seit dem letzten erfolgreichen Export noch keinen neuen Inhalt zu exportieren."
        )
    return "There is no new content to export since the last successful export."


def unsafe_project_root_message(project_root: Path) -> str:
    return (
        "I couldn't determine a safe active project root from this context, so I did not write any "
        f"export files. Current path: {project_root}."
    )


def missing_session_message(project_root: Path) -> str:
    return (
        f"I couldn't find a live Codex session for this workspace at {project_root}. "
        "Run $export from the active project session and retry."
    )


def missing_rollout_message(rollout_path: Path) -> str:
    return (
        f"I couldn't read the persisted session history at {rollout_path}. "
        "Make sure this Codex environment can access the live session data, then retry $export."
    )


def unreadable_checkpoint_message(sidecar_path: Path, language: Language) -> str:
    if language == "de":
        return (
            "Ich konnte den inkrementellen Export nicht fortsetzen, weil die Checkpoint-Datei "
            f"{sidecar_path} unlesbar oder unvollständig ist. Repariere oder entferne sie "
            "und versuche "
            "es dann erneut."
        )
    return (
        "I couldn't continue the incremental export because the checkpoint sidecar "
        f"{sidecar_path} is unreadable or incomplete. Repair or remove it, then retry $export."
    )


def checkpoint_mismatch_message(sidecar_path: Path, language: Language) -> str:
    if language == "de":
        return (
            "Ich habe den Export gestoppt, weil die Checkpoint-Datei "
            f"{sidecar_path} nicht mehr zur bisherigen Exporthistorie dieser Sitzung passt. "
            "Prüfe oder entferne sie und versuche es dann erneut."
        )
    return (
        "I stopped because the checkpoint sidecar "
        f"{sidecar_path} no longer matches this session's export history. Inspect or remove it, "
        "then retry $export."
    )


def no_exportable_content_message(language: Language) -> str:
    if language == "de":
        return "Ich konnte in dieser Sitzung noch keinen exportierbaren sichtbaren Verlauf finden."
    return "I couldn't find any exportable visible session content yet."


def write_failure_message(target_dir: Path, language: Language) -> str:
    if language == "de":
        return f"Ich konnte die Exportartefakte nicht zuverlässig nach {target_dir} schreiben."
    return f"I couldn't write the export artifacts safely into {target_dir}."
