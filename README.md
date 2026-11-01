# Heart rate from smartphone PPG

MPA-PRM · Application project: Biosignals · week 7

## The task

Develop the software of a medical device that estimates the heart rate from a 9.5 s smartphone
camera PPG record – the algorithm that a phone app would later run, not the app itself.
For every record it either **estimates the heart rate** or **requests a new measurement**.
Validate it honestly and write its technical documentation for the notified body.

The full assignment and the scoring are in the slides on e-learning.

## Getting started

1. Choose a **team name** – the name of your start-up, short and original (e.g. *Pulse Pirates*,
   *Beat Busters*).
2. On your GitHub create a new **private**, empty repository named `mpa-prm-biosignals-<team>`
   (e.g. `mpa-prm-biosignals-pulse-pirates`). The name must start like this, otherwise we do not
   find it. Do not use *Fork*: a fork of a public repository cannot be private.
3. Copy this repository into it:

   ```
   git clone https://github.com/JakubicekRoman/MPA-PRM-biosignals.git mpa-prm-biosignals-<team>
   cd mpa-prm-biosignals-<team>
   git remote set-url origin https://github.com/<your account>/mpa-prm-biosignals-<team>.git
   git push -u origin main
   ```

4. Add your team mate and **`JakubicekRoman`** as collaborators (*Settings → Collaborators*).
5. Fill in `team.json` (team name, both of you) and push it **in the first 30 minutes**.
6. Download `app1_data.zip` from e-learning, save it into `data/` and unzip it:

   ```
   python -m zipfile -e data/app1_data.zip data/
   ```

   This gives:

   ```
   data/train/signals/T0001.csv ...   PPG, column "ppg", 40 Hz, 380 samples
   data/train/info.csv                record_id, spot, sex, age
   data/train/annotations.csv         record_id, subject_id, height_cm, weight_kg, hr
   ```

   The data are **for this course only**: keep your repository private. `data/` is in
   `.gitignore` – do not commit it.
7. Commit often. The commit history is your design and development record.

## How we evaluate your software

After 17:00 we take the last commit and run, in a clean Python 3.12 environment:

```
pip install -r requirements.txt
python download_model.py
python predict.py --data <hidden test folder> --out predictions.csv
```

The hidden test folder has the same layout as `data/train` (`signals/` + `info.csv`), without
`annotations.csv`. You never see the hidden test set; it is evaluated **only once**.

So your repository must contain:

| File | Contents |
|---|---|
| `predict.py` | keep its interface; put your algorithm in `estimate()` (or call your own modules) |
| your trained model | in the repository (files up to 100 MB), or via `model.json` – see below |
| `requirements.txt` | every package `predict.py` needs, with versions; CPU only |
| your training code | everything needed to train the model from `data/train` |
| `report.html` | technical documentation with the team name and the authors, **max. 4 A4 pages when printed**, including figures |
| `team.json` | the team name and its members |
| this `README.md` | *How to reproduce the training* below |

`predict.py` must not train, must run on a CPU and should take less than 10 minutes for
about 800 records.

**Model larger than 100 MB:** upload it to a direct-download link (no login) and commit
`model.json` with the link and the checksum before 17:00:

```
{"url": "https://...", "sha256": "...", "path": "models/model.pt"}
```

Get the checksum with `python download_model.py --sha256 models/model.pt`. If the file behind
the link changes after 17:00, the download fails and the test result is 0.

## Smoke test – run it before the final push

```
python check_submission.py
```

It does exactly what we do, on a few **synthetic** records in `smoke/`: a clean environment,
`requirements.txt`, `download_model.py`, `predict.py`, and a check of the output. If it passes
on your computer, your software will run on ours. If our run fails, the test result is 0.

## How to reproduce the training

*Write the exact commands (and the environment) that train your model from `data/train`.*

```
...
```

## Rules

- Use **only the provided data**. Any other data is cheating.
- AI tools and agents are recommended. Both members of the pair must be able to explain the
  solution.
- The last commit before **17:00** counts.
