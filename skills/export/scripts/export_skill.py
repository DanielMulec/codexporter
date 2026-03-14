from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def _run() -> int:
    if str(SKILL_ROOT) not in sys.path:
        sys.path.insert(0, str(SKILL_ROOT))
    from codexporter.cli import main

    return main()


if __name__ == "__main__":
    raise SystemExit(_run())
