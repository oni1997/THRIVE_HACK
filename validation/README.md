# validation/

Starter validation tools for synthetic or contribution-ready menstrual health
datasets.

## Run Validation

```powershell
python validation/validate_dataset.py synthetic-data/sample_20.csv
```

The validator checks:

- Required fields
- Duplicate `record_id` values
- Categorical values
- Basic numeric ranges
- ISO-style country codes
- `YYYY-MM` collection month

## Included Files

| File | Purpose |
| --- | --- |
| `validate_dataset.py` | CLI wrapper for dataset validation |
| `quality_rules.json` | Human-readable validation and quality rule summary |

## Contribution Ideas

- Add richer missingness reports
- Add cross-field consistency checks
- Add small-cell suppression helpers
- Add schema versioning
- Add data quality dashboards
