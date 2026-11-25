#!/usr/bin/env python3
"""Write one Wi-Fi network name to /output/entry.txt.

The name is a single joke that implies a whole story in 28 characters:
a husband whose wife left him for the IT guy next door now broadcasts
that fact as his Wi-Fi network name -- a name the IT guy next door can
see every time he opens his phone's network list. The medium is part of
the punchline: the betrayal is announced on the very network the
neighbour's expertise runs on.

Deterministic, no network access, no arguments. The output directory
comes from the OUTPUT_DIR environment variable and defaults to /output
(the make.fun harness mount), so the program can be tested locally by
pointing OUTPUT_DIR at a scratch directory.

Gate contract (from the bounty rules): /output/entry.txt must be UTF-8
text of 1 to 32 characters, not only whitespace. This entry is 28
characters, no trailing newline, so it passes the gate as written.
"""

import os
import sys

# The entry: a Wi-Fi name that is a joke and a whole story at once.
# "She left me for the IT guy next door" -- told as one network name.
WIFI_NAME = "SheLeftMeForTheITGuyNextDoor"

MAX_CHARS = 32


def main() -> int:
    name = WIFI_NAME
    if not name or not name.strip():
        print("error: Wi-Fi name is empty", file=sys.stderr)
        return 1
    if len(name) > MAX_CHARS:
        print(
            "error: Wi-Fi name is %d characters, over the 32-character limit"
            % len(name),
            file=sys.stderr,
        )
        return 1
    # A Wi-Fi name strangers read on a phone list must be plain readable
    # text: printable characters only, no control characters or newlines.
    if not all(32 <= ord(ch) <= 126 for ch in name):
        print(
            "error: Wi-Fi name contains non-printable characters",
            file=sys.stderr,
        )
        return 1

    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")
    # Write exactly the name: no trailing newline, no extra whitespace.
    with open(entry_path, "w", encoding="utf-8", newline="") as f:
        f.write(name)

    # Round-trip check: what landed on disk must be byte-for-byte the
    # name we intended, still within the 32-character gate. If the disk
    # disagrees, fail loudly instead of shipping a corrupted entry.
    with open(entry_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != name:
        print(
            "error: entry.txt content %r does not match Wi-Fi name %r"
            % (written, name),
            file=sys.stderr,
        )
        return 1
    if not 1 <= len(written) <= MAX_CHARS:
        print(
            "error: written entry is %d characters, outside the 1-32 gate"
            % len(written),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
