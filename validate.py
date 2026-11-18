"""Validate the entry: run main.ts twice and check the outputs are
byte-identical, and that entry.png is a whole PNG within the gate limits.
"""
import hashlib
import os
import struct
import subprocess

REPO = os.path.dirname(os.path.abspath(__file__))

for out in ("/tmp/out1", "/tmp/out2"):
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out)
    subprocess.run(["node", "main.ts"], cwd=REPO, env=env, check=True)

src = open(os.path.join(REPO, "entry.png"), "rb").read()
o1 = open("/tmp/out1/entry.png", "rb").read()
o2 = open("/tmp/out2/entry.png", "rb").read()
assert src == o1 == o2, "runs differ!"
print("deterministic: both runs byte-identical to entry.png")

assert src[:8] == b"\x89PNG\r\n\x1a\n", "bad PNG magic"
w, h = struct.unpack(">II", src[16:24])
assert w <= 1024 and h <= 1024, "too large in pixels"
assert len(src) <= 1048576, "too large in bytes"
assert src[-12:] == b"\x00\x00\x00\x00IEND\xaeB`\x82", "missing IEND"
print(f"PNG ok: {w}x{h}, {len(src)} bytes, sha256 {hashlib.sha256(src).hexdigest()[:16]}...")
print("ALL CHECKS PASSED")
