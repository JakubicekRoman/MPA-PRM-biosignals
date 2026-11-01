"""Download a model file that is too large for the repository (only if model.json exists).

    python download_model.py

model.json (commit it before 17:00):
    {"url": "https://...direct download link...", "sha256": "<checksum>", "path": "models/model.pt"}

The checksum freezes the model: if the file behind the link changes, the download fails.
Get the checksum with:  python download_model.py --sha256 models/model.pt
"""

import hashlib
import json
import sys
import urllib.request
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


if len(sys.argv) == 3 and sys.argv[1] == "--sha256":
    print(sha256(sys.argv[2]))
    sys.exit(0)

cfg = Path("model.json")
if not cfg.exists():
    print("no model.json - nothing to download")
    sys.exit(0)

m = json.loads(cfg.read_text(encoding="utf-8"))
target = Path(m["path"])
target.parent.mkdir(parents=True, exist_ok=True)
print(f"downloading {m['url']} -> {target}")
urllib.request.urlretrieve(m["url"], target)
if sha256(target) != m["sha256"].lower():
    target.unlink()
    sys.exit("checksum does not match model.json - the file behind the link has changed")
print("OK - checksum matches")
