# schema/

Shared schema resources for synthetic menstrual health datasets and future data
collection tools.

The schema is intentionally conservative for public contribution. It avoids
direct identifiers, exact cycle dates, precise location, and raw free text.

## Files

| File | Purpose |
| --- | --- |
| `survey_schema.json` | Machine-readable starter schema |
| `data_dictionary.json` | Human-readable field definitions and governance notes |

## Design Principles

- Include `schema_version` so tools can detect schema changes.
- Prefer coarse categories over directly identifying detail.
- Use `collection_month` instead of exact collection dates in public examples.
- Use broad age bands instead of exact ages.
- Use coarse region labels instead of precise location.
- Keep consent records separate from research records.
- Use synthetic data for public examples, demos, tests, and dashboards.
