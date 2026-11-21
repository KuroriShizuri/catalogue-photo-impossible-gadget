"""Entry program for make.fun: The Catalogue Photo of an Impossible Gadget.

Writes the catalogue photograph to /output/entry.png.

The image is a studio catalogue photograph of the TOAST^2, a toaster
whose absurd job is toasting other toasters: a miniature chrome toaster
pops out of the glowing slot, steaming, while one untouched slice of
bread waits on a small plate beside it.

Runs offline with the standard library only. Deterministic: the same
bytes are written on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    size = os.path.getsize(DEST)
    # Self-check: the output must be a whole PNG within the 1 MiB cap.
    with open(DEST, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            print("output is not a PNG", file=sys.stderr)
            return 1
    if size > 1_048_576:
        print(f"output too large: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote {DEST} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
