"""The One-Line AI Excuse for Breaking Production.

A tiny program with one job: hand the judge a single line, spoken by an
AI agent to its human, seconds after production went down. The line is
kept in one place, checked against the 180-character gate, and written
out as UTF-8 with no trailing newline so the file holds exactly the
line and nothing else.
"""

import os
import sys
from pathlib import Path

# The excuse itself: 105 characters, first person, machine voice.
EXCUSE = (
    "I ran the tests, they passed, and then I deployed the code "
    "I actually wrote instead of the code I tested."
)

GATE_LIMIT = 180


def excuse_text() -> str:
    """Return the entry line, exactly as it will be judged."""
    line = EXCUSE.strip()
    if not line or len(line) > GATE_LIMIT:
        raise ValueError("entry line fails the 1-180 character gate")
    return line


def destination() -> Path:
    """Resolve where entry.txt goes: the harness dir, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    folder = Path(out_dir)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def publish(text: str, path: Path) -> int:
    """Write the line as UTF-8 bytes, make the file world-readable,
    then read it back and refuse to report success unless the bytes
    on disk are exactly the line (deterministic, no trailing junk)."""
    payload = text.encode("utf-8")
    path.write_bytes(payload)
    os.chmod(path, 0o644)
    if path.read_bytes() != payload:
        raise ValueError("entry.txt on disk differs from the entry line")
    return len(payload)


def main() -> int:
    line = excuse_text()
    target = destination()
    written = publish(line, target)
    print(f"wrote {written} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
