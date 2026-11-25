"""The Meeting That Should Have Been One Line — make.fun entry.

Writes one line to entry.txt in the output directory: the single sentence
that could have replaced an entire pointless meeting. Pure stdlib,
deterministic: the same bytes on every run.
"""

import os

# The line, written against the judge's brief (kill the meeting first, then
# relatable, then funny, then self-contained):
#   * It kills the meeting outright: the decision already exists, in an
#     email — so there is nothing left for the meeting to do.
#   * It is drawn from real office life: the unread email, the decision
#     re-made out loud, the slides nobody asked for.
#   * The sting lands at the end: an hour spent re-making a decision that
#     was already made, out loud, with slides.
LINE = (
    "This meeting exists because nobody read the email where we already "
    "made the decision, so now we spend an hour making it again out loud, "
    "with slides."
)


def main() -> None:
    line = LINE
    # Gate validation, mirroring the sealed scorer: /output/entry.txt must
    # be UTF-8 text of 1 to 200 characters, not only white space, a single
    # line. The gate counts characters, so validate the decoded string and
    # its exact UTF-8 byte round-trip.
    if not (1 <= len(line) <= 200):
        raise ValueError(f"line is {len(line)} characters, must be 1-200")
    if line.strip() == "":
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain control characters")
    encoded = line.encode("utf-8")
    if encoded.decode("utf-8") != line:
        raise ValueError("line is not clean UTF-8")
    # The brief wants one sentence, not two stitched together: no
    # sentence terminator may appear mid-line.
    if ". " in line or "! " in line or "? " in line:
        raise ValueError("line must be a single sentence")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the line, no trailing newline, UTF-8.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Verify what landed on disk is byte-identical to what we intended.
    with open(path, "rb") as f:
        if f.read() != encoded:
            raise RuntimeError("entry.txt on disk does not match the line")


if __name__ == "__main__":
    main()
