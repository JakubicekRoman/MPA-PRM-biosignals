"""Smoke test: will your predict.py run on our side?

    python check_submission.py            # fresh environment, like our evaluation
    python check_submission.py --reuse    # reuse the environment from the last run (faster)

It does what we do with the hidden test set, on a few synthetic records in smoke/:
1. creates a clean virtual environment (.smoke_env/) and installs requirements.txt,
2. runs download_model.py,
3. runs predict.py --data smoke --out .smoke_predictions.csv,
4. checks the output format.

The synthetic signals only test that the code runs - the heart rates it gives say nothing
about your method. Only the standard library is needed to run this script.
"""

import csv
import json
import math
import os
import shutil
import subprocess
import sys
import time
import venv
from pathlib import Path

ENV, OUT, SMOKE = Path(".smoke_env"), Path(".smoke_predictions.csv"), Path("smoke")

team = json.loads(Path("team.json").read_text(encoding="utf-8"))
if not team["team"].strip() or not all(m["name"].strip() for m in team["members"]):
    sys.exit("FAILED: fill in team.json (the team name and the name of every member)")


def step(title, cmd):
    print(f"\n== {title}\n   {' '.join(map(str, cmd))}")
    t = time.time()
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit(f"\nFAILED: {title} (exit code {r.returncode})")
    return time.time() - t


if "--reuse" not in sys.argv or not ENV.exists():
    shutil.rmtree(ENV, ignore_errors=True)
    print(f"== creating a clean environment in {ENV}/")
    venv.create(ENV, with_pip=True)
py = ENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

step("installing requirements.txt", [py, "-m", "pip", "install", "--quiet", "-r", "requirements.txt"])
step("downloading the model (if model.json exists)", [py, "download_model.py"])
OUT.unlink(missing_ok=True)
seconds = step("running predict.py on the synthetic records",
               [py, "predict.py", "--data", str(SMOKE), "--out", str(OUT)])

with (SMOKE / "info.csv").open(newline="", encoding="utf-8") as f:
    expected = [r["record_id"] for r in csv.DictReader(f)]
if not OUT.exists():
    sys.exit(f"\nFAILED: predict.py did not write {OUT}")
with OUT.open(newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    if [c.strip() for c in (reader.fieldnames or [])] != ["record_id", "hr"]:
        sys.exit(f"\nFAILED: the header must be exactly record_id,hr (found {reader.fieldnames})")
    rows = list(reader)

errors, estimated = [], 0
ids = [r["record_id"].strip() for r in rows]
if sorted(ids) != sorted(expected):
    errors.append("the output must have exactly one row for every record of info.csv")
for r in rows:
    hr = (r["hr"] or "").strip()
    if not hr:
        continue
    try:
        v = float(hr)
    except ValueError:
        errors.append(f"{r['record_id']}: hr '{hr}' is not a number (leave it empty to request a new measurement)")
        continue
    if not math.isfinite(v) or not 20 <= v <= 250:
        errors.append(f"{r['record_id']}: hr {hr} is outside 20-250 bpm")
    estimated += 1

if errors:
    print("\nFAILED:")
    print("\n".join(f"  - {e}" for e in errors[:20]))
    sys.exit(1)
per_record = seconds / len(rows)
print(f"\nOK: {len(rows)} records, heart rate estimated for {estimated}, new measurement requested for "
      f"{len(rows) - estimated}; {per_record:.2f} s per record.")
if per_record * 800 > 600:
    print("WARNING: about 800 hidden test records would take over 10 minutes - make predict.py faster.")
