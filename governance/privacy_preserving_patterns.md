# Privacy-Preserving Build Patterns

Use these patterns when designing menstrual health data tools for Menstrual Health Open. They
are meant to give builders options, not narrow the open-source ecosystem.

## Pattern 1: Synthetic-Only Demo

Use generated or fictional records for all examples, tests, screenshots, and
public demos.

Best for:

- Dashboards
- Model prototypes
- Data quality tools
- Schema mapping
- Research assistants

Contribution standard:

- Mark the dataset as synthetic
- Do not mix synthetic and real participant records
- Keep distributions realistic enough for testing but not copied from a small
  real cohort

## Pattern 2: Local-Only / No-Storage Tool

The user enters data, the tool computes a result on the same device, and nothing
is retained after the session.

Best for:

- Symptom education
- Risk explanations
- CHW decision-support aids
- Menstrual diary calculators
- Offline screening prototypes

Contribution standard:

- No server upload by default
- No local persistence unless the user explicitly opts in
- No hidden analytics or crash logs containing health inputs
- Clear reset/delete behavior

## Pattern 3: Ephemeral Processing API

The app sends data to an API for a single calculation, but the API does not save
the raw input.

Best for:

- Larger model inference
- Transcription or translation
- Temporary validation checks
- Format conversion

Contribution standard:

- Disable request-body logging
- Do not persist raw uploads
- Store only minimal operational telemetry
- Delete temporary files immediately
- Document any third-party processor

## Pattern 4: Edge Redaction Before Upload

Identifiers are removed before any data leaves the collection device.

Best for:

- Voice transcription
- Free-text symptom extraction
- CHW notes
- Image or video workflows

Contribution standard:

- Redact names, phone numbers, exact addresses, and other identifiers locally
- Avoid uploading raw audio/video unless separately approved
- Prefer text summaries, feature vectors, or aggregate counts over raw media
- Keep consent records separate from research data

## Pattern 5: Aggregate-Only Public Insights

The public output is a summary, not a participant-level dataset.

Best for:

- Public dashboards
- Regional summaries
- Missing-data reports
- Community trend reporting

Contribution standard:

- Suppress small cells
- Use broad age bands and coarse geography
- Avoid exact dates when month/quarter is enough
- Review combinations of fields for re-identification risk

## Pattern 6: Federated or Secure Aggregation

Analysis runs across local sites or devices, and only model updates or aggregate
statistics are shared.

Best for:

- Multi-partner research
- Low-trust data collaboration
- Cross-region model improvement
- Sensitive community datasets

Contribution standard:

- Explain what leaves each site
- Protect against leakage from model updates or rare categories
- Provide a fallback for low-connectivity settings
- Document governance assumptions

## Pattern 7: Controlled Research Enclave

Approved researchers use de-identified data inside a controlled environment.
The public repo contains only the tooling, schema, tests, and synthetic examples.

Best for:

- Research-grade analysis
- De-identified individual-level datasets
- Reproducible notebooks that cannot expose raw records

Contribution standard:

- No real dataset in the repo
- Synthetic fixture data for tests
- Role-based access assumptions documented
- Export rules for aggregate results

## Design Checklist

Before submitting, answer:

- What is the minimum data needed?
- Can the same tool work with synthetic data?
- Can computation happen locally?
- If a server is needed, can processing be ephemeral?
- What exact data is stored, and why?
- What data is transmitted to third parties?
- Could a person be identified through rare combinations of fields?
- How does a participant withdraw, delete, or avoid collection?
- What happens if the device, repo, database, or logs become public?

## Diagnostics and Safety

Contributor tools may support diagnostic workflows, triage, referral, education,
or research. They should not present themselves as clinically validated medical
diagnosis unless validation, clinical governance, and applicable regulatory
requirements are in place.

Use language such as:

- "decision support"
- "screening support"
- "risk flag"
- "education"
- "research prototype"

Avoid language such as:

- "diagnoses"
- "rules out"
- "clinically proven"
- "medical device ready"

Open the infrastructure. Protect the people.
