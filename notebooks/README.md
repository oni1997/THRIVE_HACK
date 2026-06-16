# notebooks/

Research notebooks demonstrating how to work with the starter repository. All
notebooks use the bundled synthetic datasets — nothing here touches real
participant data.

## Notebooks

| Notebook | Purpose |
| --- | --- |
| `01_explore_synthetic_data.ipynb` | Tour of the synthetic dataset, schema fields, and distributions |
| `02_data_quality_walkthrough.ipynb` | Using the validator programmatically and building quality reports |
| `03_research_questions_starter.ipynb` | Example analysis patterns, including small-cell suppression |
| `04_risk_modeling.ipynb` | ML models predicting iron deficiency from self-reported data (Prompt B) |
| `05_triage_demo.ipynb` | End-to-end CHW triage pipeline from community data to referrals (Prompts B + C) |

## Setup

```bash
pip install -r notebooks/requirements.txt
jupyter lab
```

Open the notebooks from the `notebooks/` directory; paths resolve relative to
either the repository root or this folder.

## Rules

- Notebooks committed to this repository must run on synthetic data only.
- Clear outputs that contain large tables before committing.
- State the synthetic-data caveat prominently in any notebook that could be
  mistaken for real analysis.
