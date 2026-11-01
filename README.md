# Heart rate from smartphone PPG

MPA-PRM · Application project: Biosignals · week 7

## Team

Team name (your start-up): 

Members: 

## The task

Develop the software of a medical device that estimates the heart rate from a 9.5 s smartphone
camera PPG record – the algorithm that a phone app would later run, not the app itself.
For every record it either **estimates the heart rate** or **requests a new measurement**.
Validate it honestly and write its technical documentation for the notified body.

The full assignment and the scoring are in the slides on e-learning.

## Getting started

1. On your GitHub create a new **private**, empty repository. Do not use *Fork*: a fork of a public
   repository cannot be private.
2. Copy this repository into it:

   ```
   git clone https://github.com/JakubicekRoman/MPA-PRM-biosignals.git
   cd MPA-PRM-biosignals
   git remote set-url origin <the URL of your repository>
   git push -u origin main
   ```

3. Add your team mate and **`JakubicekRoman`** as collaborators (*Settings → Collaborators*).
4. Fill in the team above.
5. Download `app1_data.zip` from e-learning and unzip it into `data/`:

   ```
   python -m zipfile -e app1_data.zip data/
   ```

   ```
   data/train/signals/T0001.csv ...   PPG, column "ppg", 40 Hz, 380 samples
   data/train/info.csv                record_id, spot, sex, age
   data/train/annotations.csv         record_id, subject_id, height_cm, weight_kg, hr
   ```

   The data are **for this course only**: do not commit or share them.
6. Commit often. The commit history is your design and development record.

## What must be in your repository at 17:00

- `predict.py`: keep its interface, put your algorithm in `estimate()`
- your trained model (larger than 100 MB: a download link below)
- `requirements.txt`: every package `predict.py` needs
- the code you used for training, as it is
- `report.html`: technical documentation, max. 4 A4 pages when printed, including figures

## How we run it

After 17:00 we take your last commit and run:

```
pip install -r requirements.txt
python predict.py --data <hidden test folder> --out predictions.csv
```

The hidden test folder has the same layout as `data/train` (`signals/` + `info.csv`), without
`annotations.csv`. The output has one row per record: `record_id,hr`, with an empty `hr` for a new
measurement.

**Try it before the final push**, on a few synthetic records in `smoke/`:

```
python predict.py --data smoke --out predictions.csv
```

## Model download (only for a model larger than 100 MB)

Link:

Save it as (path in the repository):

## Rules

- Use **only the provided data**. Any other data is cheating.
- AI tools and agents are recommended. Both members of the pair must be able to explain the
  solution.
- The last commit before **17:00** counts.
