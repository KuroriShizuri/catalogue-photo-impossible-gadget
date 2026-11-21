"""
TOAST²: A toaster that toasts other toasters.
This program writes a studio catalogue photograph of the impossible gadget
to /output/entry.png.
"""

import shutil
import os
import sys
import struct

# Create /output if it doesn't exist
output_dir = "/output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Copy entry.png to /output/entry.png
src = "/home/hatch/workspace/makefun/work/the-catalogue-photo-of-an-2-20261121-0341/entry.png"
dst = "/output/entry.png"

try:
    shutil.copy2(src, dst)
except Exception as e:
    print(f"Error copying file: {e}", file=sys.stderr)
    sys.exit(1)

# Verify it's a PNG
try:
    with open(dst, "rb") as f:
        header = f.read(8)
        # PNG signature: 0x89 0x50 0x4E 0x47 0x0D 0x0A 0x1A 0x0A
        expected_signature = b"\x89PNG\r\n\x1a\n"
        if header != expected_signature:
            print("Error: file is not a valid PNG", file=sys.stderr)
            sys.exit(1)
except Exception as e:
    print(f"Error verifying PNG signature: {e}", file=sys.stderr)
    sys.exit(1)

# Check file size
try:
    file_size = os.path.getsize(dst)
    if file_size > 1048576:
        print(f"Error: file size {file_size} exceeds 1048576 bytes", file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print(f"Error checking file size: {e}", file=sys.stderr)
    sys.exit(1)

# Read PNG IHDR chunk to get width and height
try:
    with open(dst, "rb") as f:
        # Skip PNG signature (8 bytes)
        f.seek(8)
        # Read IHDR chunk length (4 bytes, big-endian)
        chunk_len = struct.unpack(">I", f.read(4))[0]
        # Read chunk type (4 bytes, should be "IHDR")
        chunk_type = f.read(4)
        if chunk_type != b"IHDR":
            print("Error: IHDR chunk not found", file=sys.stderr)
            sys.exit(1)
        # Read width and height (4 bytes each, big-endian)
        width = struct.unpack(">I", f.read(4))[0]
        height = struct.unpack(">I", f.read(4))[0]
        
        # Check dimensions don't exceed 1024
        if width > 1024 or height > 1024:
            print(f"Error: dimensions {width}x{height} exceed 1024x1024", file=sys.stderr)
            sys.exit(1)
except struct.error as e:
    print(f"Error parsing PNG IHDR: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error reading PNG dimensions: {e}", file=sys.stderr)
    sys.exit(1)

# Print success with dimensions
print(f"wrote /output/entry.png ({file_size} bytes), dimensions: {width}x{height}")
