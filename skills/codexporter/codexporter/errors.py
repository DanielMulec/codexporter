from __future__ import annotations


class ExporterError(RuntimeError):
    """Base class for user-facing exporter failures."""

    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


class ProjectRootError(ExporterError):
    """Raised when the active project root is unsafe or unclear."""


class SessionDiscoveryError(ExporterError):
    """Raised when the current Codex session cannot be discovered."""


class RolloutAccessError(ExporterError):
    """Raised when the rollout history cannot be read safely."""


class CheckpointError(ExporterError):
    """Raised when checkpoint state is missing, corrupted, or mismatched."""
