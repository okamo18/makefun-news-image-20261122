# main.py: copy the entry image to the output directory (stdlib only).
# The image sums up Sunday 22 November 2026: Ukraine's largest attack
# of the year (110 missiles, 400+ drones), Poland's airspace breach,
# Houthi strikes on Riyadh, the Sparta II fire in the Baltic, the UN
# killer-robot talks, Bitcoin's two-year low, and the COP31 deadlock.
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
src = os.path.join(here, "entry.png")
dst = os.path.join(out, "entry.png")
shutil.copyfile(src, dst)
# The gate takes a whole PNG: fail loudly if the copy is not a
# byte-complete one — signature first, then size against the source.
# (Explicit checks, not assert, so `python -O` cannot skip them.)
with open(dst, "rb") as f:
    signature = f.read(8)
if signature != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("copied entry.png is not a PNG (bad signature)")
src_size = os.path.getsize(src)
dst_size = os.path.getsize(dst)
if dst_size != src_size:
    raise SystemExit(
        f"copied entry.png is incomplete: {dst_size} of {src_size} bytes"
    )
print("wrote", dst, dst_size, "bytes")
