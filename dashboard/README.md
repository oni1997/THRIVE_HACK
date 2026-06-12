# dashboard/

Starter dashboard template for exploring synthetic menstrual health data.

Built with [Streamlit](https://streamlit.io) and Altair. It loads the bundled
synthetic dataset by default and accepts any schema-conforming CSV via the
sidebar uploader.

## Run It

From the repository root:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

The app opens at `http://localhost:8501`.

## What It Shows

- Headline metrics: record count, median cycle length, median pain score,
  share of records reporting missed school or work
- Pain score by flow heaviness (box plot)
- Cycle length distribution
- Reported symptom frequency
- Product access by setting
- Records by collection month
- Filterable raw record browser

## Rules For Dashboards

- Public dashboards must use synthetic or reviewed aggregate data only.
- Never load real participant-level records into a public dashboard.
- Apply small-cell suppression before publishing aggregate views of any
  approved non-synthetic data (see `governance/privacy_preserving_patterns.md`).
- Label synthetic data clearly so charts are not mistaken for real prevalence.

## Contribution Ideas

- Add a data quality view powered by `validation/validate_dataset.py`
- Add comparison views across countries or settings with suppression built in
- Add localization / multilingual labels
- Add accessibility improvements (contrast, keyboard navigation, alt text)
- Port the template to another stack (Dash, Observable, plain HTML + Chart.js)
