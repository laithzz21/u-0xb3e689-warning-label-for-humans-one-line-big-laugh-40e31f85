#!/usr/bin/env python3
"""Entry generator for the make.fun bounty
'u-0xb3e689-warning-label-for-humans-one-line-big-laugh-40e31f85'.

Writes the one-line safety-warning-label entry to the output file.
Deterministic, stdlib only, no network, no clock, no randomness.
"""

import os
import sys

ENTRY_TEXT = (
    "WARNING: Contains one (1) human. Leaks feelings at inconvenient "
    "times. Do not shake, feed after midnight, or ask 'what are we?'"
)


def validate(text: str) -> None:
    """Enforce the competition rules: one line, 1-160 characters."""
    if not 1 <= len(text) <= 160:
        raise ValueError(f"Entry must be 1-160 chars, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("Entry must be a single line")


def output_path() -> str:
    """Resolve the output file path.

    Uses $MAKEFUN_OUTPUT when set, otherwise /output; if /output is not
    writable, falls back to ./output relative to this script's directory.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.access("/output", os.W_OK) or not os.path.exists("/output"):
        try:
            os.makedirs("/output", exist_ok=True)
            if os.access("/output", os.W_OK):
                return "/output/entry.txt"
        except OSError:
            pass
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def main() -> int:
    validate(ENTRY_TEXT)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY_TEXT + "\n")
    # Verify the written file by reading it back.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY_TEXT + "\n":
        raise RuntimeError(f"Read-back mismatch in {path}")
    print(f"Wrote entry to {path} ({len(ENTRY_TEXT)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
