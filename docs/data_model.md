# Data Model

The starter data model is intentionally small. It gives contributors a shared
foundation without pretending to be a complete clinical dataset.

Current schema version: `0.1.0`.

## Goals

- Support validation, synthetic data generation, and future contribution ideas
- Avoid direct identifiers
- Avoid exact cycle dates in public examples
- Support multilingual and low-resource workflows later
- Leave room for regional extensions

## Public Starter Fields

| Field | Purpose |
| --- | --- |
| `schema_version` | Schema version used by the record |
| `record_id` | Synthetic or contribution-specific row ID |
| `age_band` | Broad age category |
| `country_code` | ISO-style country code |
| `region` | Coarse fictional or approved region label |
| `setting` | Urban, peri-urban, or rural |
| `collection_month` | Month-level collection period |
| `cycle_length_days` | Synthetic or reported cycle length |
| `period_duration_days` | Synthetic or reported period duration |
| `flow_heaviness` | Self-reported flow category |
| `pain_score` | 0-10 pain score |
| `reported_symptoms` | Controlled symptom labels |
| `missed_school_or_work` | Attendance impact |
| `product_access` | Menstrual product access |
| `healthcare_access` | Care access or care-seeking status |
| `collection_method` | Collection or simulation method |
| `source_type` | Synthetic, example, or aggregate |

## Extension Ideas

Contributors may propose extensions for:

- Nutrition and anemia risk indicators
- School or workplace impact
- Product availability and affordability
- Referral and care access
- Survey localization
- Aggregate reporting
- Metadata and provenance
- Consent and withdrawal status

Extensions should document privacy implications and validation rules.
