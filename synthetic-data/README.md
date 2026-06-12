# synthetic-data/

Synthetic menstrual health datasets for development, testing, dashboards, and
research workflow prototypes.

These files are fake. They do not contain real participant information.

## Generate Data

The generator accepts `--count`, so contributors can generate the amount of
synthetic data they need. The command-line path streams records to disk instead
of keeping the whole dataset in memory; practical limits are disk space and
runtime.

```powershell
python synthetic-data/generate.py --count 100 --output synthetic-data/generated_100.csv
```

Generate JSONL:

```powershell
python synthetic-data/generate.py --count 100 --format jsonl --output synthetic-data/generated_100.jsonl
```

Generate optional-field missingness for validation testing:

```powershell
python synthetic-data/generate.py --count 100 --missingness 0.15 --output synthetic-data/generated_missingness.csv
```

## Included Files

| File | Purpose |
| --- | --- |
| `generate.py` | CLI wrapper for generating synthetic records |
| `sample_20.csv` | Small fixture dataset for demos and validation |

## Rules

- Mark synthetic datasets clearly.
- Do not mix synthetic and real participant data.
- Do not infer that synthetic distributions represent real prevalence.
- Use `--missingness` only to test validation and reporting behavior; missingness
  is simulated and not based on real-world rates.
- Use synthetic data for public demos, tests, dashboards, notebooks, and issues.
