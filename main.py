# The One-Line Developer Excuse for Breaking Production
# make.fun bounty: u-motasimfuad-make-the-ai-judge-laugh-developer-49386be3
# Writes a single-line excuse (1-200 chars, no trailing newline) to
# $MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt in the sandbox,
# or ./output/entry.txt as a local fallback).
# No network, no dependencies, Python 3.13, exits 0, never throws
# on the happy path.

import os
import sys

EXCUSE = "It worked in staging because staging has never met a real user."


def candidate_dirs() -> list:
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("MAKEFUN_BOT_DIR")
    if env_dir and env_dir.strip():
        dirs.append(env_dir)
    # The kit says the program writes to /output/entry.txt in the sandbox.
    dirs.append("/output")
    dirs.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    return dirs


def main() -> int:
    # Safety: the line must stay within the 1-200 character gate (code points)
    # and be exactly one line, or the sealed scorer marks the entry invalid.
    length = len(EXCUSE)
    if length < 1 or length > 200:
        print(f"excuse length {length} is outside the 1-200 gate", file=sys.stderr)
        return 1
    if "\n" in EXCUSE or "\r" in EXCUSE:
        print("excuse must be exactly one line", file=sys.stderr)
        return 1
    # No trailing newline: the gate counts the whole file, so the file
    # content is exactly the line itself. Try each candidate dir in order
    # and keep the first one that actually accepts the write.
    last_error = None
    for out_dir in candidate_dirs():
        try:
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="") as f:
                f.write(EXCUSE)
            break
        except OSError as exc:
            last_error = exc
    else:
        print(f"could not write entry.txt: {last_error}", file=sys.stderr)
        return 1
    print(EXCUSE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
