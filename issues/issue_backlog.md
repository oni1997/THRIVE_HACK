# Starter Issue Backlog

Concrete, scoped issues participants can pick up directly. Difficulty labels:
**good-first-issue** (a few hours), **intermediate** (a day), **advanced**
(multi-day or research-heavy). These are infrastructure improvements that
support work on any of the prompts in
[challenge_statements.md](challenge_statements.md).

Claim an issue by opening a GitHub issue referencing its ID.

---

## Validation & Data Quality

- **VAL-01** (good-first-issue) — Add a cross-field check to the validator:
  flag rows where `period_duration_days` is implausibly long relative to
  `cycle_length_days`.
- **VAL-02** (good-first-issue) — Add a `--format json|text` flag to
  `validate_dataset.py` so humans get a readable summary and CI gets JSON.
- **VAL-03** (intermediate) — Per-field missingness report: extend the
  validation report with per-field fill rates for both required and optional
  fields.
- **VAL-04** (intermediate) — Schema-driven validation: derive required
  fields, enums, and ranges from `schema/survey_schema.json` instead of the
  hard-coded copies in the script, so schema and validator cannot drift.
- **VAL-05** (advanced) — Multi-version schema support: validate datasets
  written against older schema versions and emit migration hints.
- **VAL-06** (intermediate) — Field-name normalizer: a tool that maps common
  variant column names (e.g. `cycle_len`, `CycleLength`) onto schema fields
  and reports unmapped columns.

## Synthetic Data

- **SYN-01** (intermediate) — Add realistic correlation options to the
  generator (e.g. age band influencing cycle regularity) behind explicit
  flags, with documentation that correlations are still artificial.
- **SYN-02** (intermediate) — Longitudinal mode: generate multiple cycle
  records per synthetic participant with a stable pseudonymous participant ID.
- **SYN-03** (good-first-issue) — Add a `--locale` flag that expands the
  country list and region label patterns.
- **SYN-04** (advanced) — Synthetic benchmark suite: parameterized datasets
  with known injected anomalies for testing quality tools.

## Dashboard

- **DASH-01** (good-first-issue) — Add a data quality tab that runs
  `validation/validate_dataset.py` on the loaded dataset and displays the
  report.
- **DASH-02** (intermediate) — Build small-cell suppression into every
  aggregate chart, with a visible "suppressed" indicator.
- **DASH-03** (intermediate) — Country/setting comparison view with
  synthetic-data caveat labels baked into the chart titles.
- **DASH-04** (advanced) — Port the dashboard template to a static stack
  (plain HTML + Chart.js) for low-bandwidth, no-server deployment.
- **DASH-05** (good-first-issue) — Accessibility pass: color contrast,
  colorblind-safe palettes, and chart alt-text.

## Privacy & Governance

- **GOV-01** (good-first-issue) — Plain-language one-pager: "What this project
  will never publish," derived from `docs/project_brief.md`.
- **GOV-02** (intermediate) — Reusable small-cell suppression helper module
  with tests, extracted from the notebook pattern.
- **GOV-03** (intermediate) — Privacy review checklist as a structured,
  fillable markdown template for proposed public outputs.
- **GOV-04** (advanced) — Differential privacy demonstration on the synthetic
  dataset, with a plain-language explanation of the tradeoffs.
- **GOV-05** (intermediate) — Consent withdrawal workflow design: how a
  participant's withdrawal propagates through a research dataset pipeline.

## Localization & Accessibility

- **LOC-01** (good-first-issue) — Translate the data dictionary field
  definitions into one additional language as a parallel JSON file.
- **LOC-02** (intermediate) — Multilingual label infrastructure: a format and
  loader for schema field labels in multiple languages.
- **LOC-03** (intermediate) — Low-literacy explanation cards for each schema
  field, designed for community health worker use.
- **LOC-04** (advanced) — Offline-first collection prototype that produces
  schema-conforming CSV/JSONL without a network connection.

## Research Enablement

- **RES-01** (good-first-issue) — Add a fourth notebook demonstrating cohort
  comparison with uncertainty intervals on synthetic data.
- **RES-02** (intermediate) — Research question library: a structured document
  mapping open menstrual health research questions to the schema fields that
  could address them.
- **RES-03** (intermediate) — Metadata explorer: a small tool that summarizes
  any schema-conforming dataset (fields, ranges, categories, missingness)
  into a shareable dataset card.

## Documentation & Community

- **DOC-01** (good-first-issue) — Glossary of project terms (synthetic,
  aggregate, controlled access, suppression…) in plain language.
- **DOC-02** (good-first-issue) — Improve the contributor quickstart with
  screenshots of the dashboard and a 10-minute first-contribution path.
- **DOC-03** (intermediate) — Partner data preparation guide: step-by-step
  from a spreadsheet to a validated, schema-conforming submission.
- **DOC-04** (intermediate) — Community briefing template explaining how data
  is protected, for use at partner onboarding sessions.

---

## Proposing New Issues

Open a GitHub issue using the **project idea** template. Good issues are
scoped (finishable in days, not months), grounded in synthetic data, and
state what "done" looks like.
