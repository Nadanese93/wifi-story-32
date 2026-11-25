#!/usr/bin/env python3
"""Write the 32-character story entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Validation is split into separate checks, each raising its own error,
and the written file is read back and compared byte-for-byte before
the program reports success.
"""

import os
import sys

ENTRY = "ProposedOverHotspot_SheSaidYes"


class EntryLengthError(ValueError):
    """Entry is not between 1 and 32 characters."""


class EntryBlankError(ValueError):
    """Entry is only whitespace."""


class EntryMultilineError(ValueError):
    """Entry spans more than one line."""


class EntryMismatchError(ValueError):
    """Written file does not match the entry bytes."""


def check_length(entry: str) -> None:
    if not (1 <= len(entry) <= 32):
        raise EntryLengthError(
            f"entry must be 1-32 characters, got {len(entry)}"
        )


def check_not_blank(entry: str) -> None:
    if not entry.strip():
        raise EntryBlankError("entry must not be only whitespace")


def check_single_line(entry: str) -> None:
    if "\n" in entry or "\r" in entry:
        raise EntryMultilineError("entry must be a single line")


def validate(entry: str) -> None:
    check_length(entry)
    check_not_blank(entry)
    check_single_line(entry)


def write_entry(entry: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    return path


def verify_written(path: str, entry: str) -> None:
    with open(path, "rb") as f:
        written = f.read()
    if written != entry.encode("utf-8"):
        raise EntryMismatchError(
            f"read-back mismatch: wrote {len(entry.encode('utf-8'))} bytes, "
            f"read back {len(written)} bytes"
        )


def main() -> int:
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    path = write_entry(ENTRY, out_dir)
    try:
        verify_written(path, ENTRY)
    except (OSError, EntryMismatchError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
