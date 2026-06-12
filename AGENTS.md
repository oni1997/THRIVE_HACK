# Agent Instructions

Guidance for AI coding assistants (and their humans) working in this
repository.

## What This Project Is

Open-source infrastructure starter kit for ethical menstrual health research,
used as the shared foundation for the THRIVE hackathon. Participants build
tools, models, standards, and documentation against **synthetic data only**.
Core principle: **Open the infrastructure. Protect the people.**

## Hard Rules — Never Violate These

- **Never add real participant-level health data**, or anything that looks
  like it: names, phone numbers, addresses, GPS coordinates, exact cycle or
  collection dates, raw free-text survey responses, consent records, or
  identity-linked records.
- All row-level data committed to the repo must be synthetic and marked
  `source_type = synthetic`.
- Public aggregate outputs (charts, tables, dashboards) must use synthetic
  data, or apply small-cell suppression if ever derived from approved
  non-synthetic sources (see `governance/privacy_preserving_patterns.md`).
- Do not claim clinical validity for any tool or model built here. Use
  decision-support framing, not diagnosis.
- Do not commit secrets, credentials, or partner files.

When generating example data, always use the bundled generator rather than
inventing records by hand — it guarantees schema conformance and synthetic
marking.

## Repository Map

| Path | Purpose |
| --- | --- |
| `schema/` | Survey schema + data dictionary — the source of truth for fields |
| `synthetic-data/` | Generator (`generate.py`) and bundled datasets (`datasets/`) |
| `validation/` | Dataset validator (`validate_dataset.py`) + quality rules |
| `src/menstrual_health_open/` | Python package backing the generator/validator/CLI |
| `tests/` | Pytest suite for the package |
| `dashboard/` | Streamlit starter dashboard |
| `notebooks/` | Jupyter notebooks: exploration, data quality, analysis patterns |
| `governance/` | Ethics checklist, consent templates, data access policy |
| `docs/` | Project brief, data model, contributor workflow, licensing |
| `issues/` | Official hackathon prompts (A–D) and starter issue backlog |
| `inspirations/` | Open-ended project directions |

## Commands

Everything core needs only Python 3.11+ (stdlib). Run from the repo root.

```bash
# Generate synthetic data (deterministic per --seed)
python synthetic-data/generate.py --count 100 --output /tmp/sample.csv

# Validate a CSV or JSONL dataset (exit 0 = valid, prints JSON report)
python validation/validate_dataset.py /tmp/sample.csv

# Tests
pip install -e ".[dev]"
python -m pytest

# Dashboard (needs pip install -r dashboard/requirements.txt)
streamlit run dashboard/app.py
```

CI (`.github/workflows/ci.yml`) compiles the Python, validates the bundled
sample, generates and validates a smoke-test dataset, and runs pytest. Keep it
green.

## Conventions

- `synthetic-data/generate.py` and `validation/validate_dataset.py` are thin
  CLI wrappers over `src/menstrual_health_open/` — put logic in the package,
  keep the wrappers thin.
- The package is stdlib-only by design. Do not add runtime dependencies to it;
  heavier dependencies belong in `dashboard/` or `notebooks/` with their own
  `requirements.txt`.
- `schema/survey_schema.json` defines fields; the validator currently
  duplicates enums/ranges in code — if you change one, change both (or pick up
  backlog item VAL-04 and unify them).
- Schema changes must bump `schema_version` and update
  `schema/data_dictionary.json` and `validation/quality_rules.json` together.
- Notebooks must run on the bundled synthetic datasets and state the
  synthetic-data caveat prominently.
- Categorical fields use controlled vocabularies — never introduce free-text
  fields to public schemas.

## Contribution Flow

Work on a branch, open a pull request to `main` (see `CONTRIBUTING.md`).
External participants: fork the repo and PR from the fork. Every contribution
should document what it does, who it is for, how to run it, what data it uses,
and its privacy posture.

## Licensing

Code: Apache-2.0 (`LICENSE`). Docs and governance: CC BY 4.0
(`LICENSE-DOCS.md`). Synthetic data: CC0 (`synthetic-data/LICENSE`).
