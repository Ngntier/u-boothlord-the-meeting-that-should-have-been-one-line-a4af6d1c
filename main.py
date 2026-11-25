"""Entry for make.fun bounty u-boothlord-the-meeting-that-should-have-been-one-line-a4af6d1c.

Writes the single sentence that could have replaced an entire pointless
meeting to entry.txt. Deterministic, stdlib only, no network, no randomness:
the same bytes on every run.
"""

import os

ENTRY = (
    "We have agreed to change nothing, assign it to no one, and meet again "
    "next Tuesday to confirm that nothing happened."
)


def validate(line):
    """Check the entry line against the competition gate.

    The gate requires /output/entry.txt to be UTF-8 text of 1 to 200
    characters, not only whitespace, and the task requires a single line.
    """
    if not line or line.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) < 1 or len(line) > 200:
        raise ValueError("entry must be 1 to 200 characters")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    for char in line:
        if ord(char) < 32 or ord(char) == 127:
            raise ValueError("entry must not contain control characters")
    line.encode("utf-8")
    return line


def main():
    line = validate(ENTRY)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


if __name__ == "__main__":
    main()
