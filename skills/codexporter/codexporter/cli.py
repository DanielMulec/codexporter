from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from codexporter.errors import ExporterError
from codexporter.service import export_current_session


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export the current Codex session to markdown.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Active project root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Codex home directory. Defaults to $CODEX_HOME or ~/.codex.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        result = export_current_session(project_root=args.project_root, codex_home=args.codex_home)
    except ExporterError as exc:
        print(exc.user_message)
        return 1

    print(result.message)
    return 0
