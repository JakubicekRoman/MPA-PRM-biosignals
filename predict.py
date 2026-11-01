"""Heart rate from a 9.5 s PPG record – the entry point we run on the hidden test set.

    python predict.py --data <folder> --out predictions.csv

<folder> has the same layout as data/train:
    signals/<record_id>.csv   column "ppg", 40 Hz, 380 samples
    info.csv                  record_id, spot, sex, age

The output has one row per record of info.csv: record_id,hr – the heart rate in bpm,
or an empty hr to request a new measurement.

Keep this interface (the arguments and the output). Everything else is yours: load your
trained model from the repository, use any packages listed in requirements.txt.
No training here, and no internet access is needed while it runs.
"""

import argparse
import csv
from pathlib import Path


def estimate(ppg, info):
    """Return the heart rate in bpm for one record, or None to request a new measurement.

    ppg  – list of 380 floats (40 Hz)
    info – dict with record_id, spot, sex, age
    """
    return None  # TODO: your algorithm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="folder with signals/ and info.csv")
    ap.add_argument("--out", required=True, help="output CSV: record_id,hr")
    a = ap.parse_args()
    data = Path(a.data)

    with (data / "info.csv").open(newline="", encoding="utf-8") as f:
        records = list(csv.DictReader(f))

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "hr"])
        for info in records:
            with (data / "signals" / f"{info['record_id']}.csv").open(newline="", encoding="utf-8") as s:
                ppg = [float(row["ppg"]) for row in csv.DictReader(s)]
            hr = estimate(ppg, info)
            w.writerow([info["record_id"], "" if hr is None else f"{hr:.1f}"])


if __name__ == "__main__":
    main()
