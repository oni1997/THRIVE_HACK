# Menstrual Health Open Data Access Policy

## Purpose
This policy defines how menstrual health data within the Menstrual Health Open ecosystem is accessed, used, and governed. It establishes a tiered access model that balances open science with participant protection.

## Guiding Principle
**Open the infrastructure. Protect the people.**

All code, standards, documentation, synthetic datasets, and research methods are open for contribution. Sensitive participant-level health data remains protected and is not used during public development, public demos, or unapproved contribution workflows.

## Contributor Builder Scope

This policy is not a restriction on what participants can imagine or prototype.
It is a restriction on unsafe handling of real menstrual health data.

Contributors may build in any direction, including diagnostic-support
tools, AI systems, community health worker workflows, sensors, voice/video
tools, privacy infrastructure, consent systems, data pipelines, validation
tools, dashboards, and research infrastructure.

Public contributions should use one of these safe modes:

- Synthetic-only data
- Local-only or no-storage processing
- Ephemeral server processing with no retained raw input
- Aggregate-only outputs
- Properly de-identified examples
- Controlled-access assumptions with synthetic fixtures in the repo

Real participant data, raw media, consent forms, and direct identifiers must not
be committed to the public repo or used in public demos.

## Tiered Data Access Model

### Tier 1: Public Layer
**Access**: Open to everyone
**Content**:
- Open documentation, schema, data dictionary
- Research methods and contributor guides
- Public metadata and corpus statistics
- Code, validation scripts, and tools
- Contributor resources and challenge briefs

**Requirements**: None

### Tier 2: Synthetic Data Layer
**Access**: Open to everyone
**Content**:
- Fake datasets that mimic real data structure
- No real participant information
- Suitable for development, testing, and education
- Generated as fixtures or examples, such as `synthetic-data/sample_20.csv`

**Requirements**: None
**Purpose**: Enable developers and researchers to build tools safely

**Contributor default**: Most prototypes should start here.

### Tier 3: Aggregate Data Layer
**Access**: Open after privacy review
**Content**:
- Regional summaries and broad age-band statistics
- Missing-data reports and general trends
- Access-to-care indicators
- Data quality reports

**Requirements**:
- Data request submitted through official channel
- Privacy review completed
- No individual participants can be re-identified
- Small cells suppressed or generalized
- Exact dates and precise locations removed unless specifically approved

### Tier 4: Controlled Research Layer
**Access**: Restricted to approved researchers
**Content**:
- De-identified individual-level datasets
- Detailed demographic breakdowns
- Symptom and outcome data

**Requirements**:
- Formal data-use agreement (DUA) signed
- Ethics review approval (IRB or equivalent)
- Institutional affiliation verified
- Research proposal reviewed and approved
- Data security plan submitted
- Annual reporting on data use

**Repo rule**: Tools for this layer may be contributed openly, but real datasets
must remain outside the public repository. Use synthetic fixtures for tests and
examples.

### Tier 5: Private Raw Data Layer
**Access**: Data subjects and authorized data stewards only
**Content**:
- Original participant-level records
- Identifiable information
- Consent records
- Partner-submitted raw files

**Requirements**:
- Data subject consent
- Data steward authorization
- Encrypted storage
- Audit trail maintained
- Retention and deletion schedule documented
- No public contributor use unless separately approved by the relevant ethics and
  data governance bodies

## Data Use Principles

1. **Minimization**: Collect only what is necessary for the research purpose
2. **Purpose Limitation**: Data used only for stated and approved purposes
3. **De-identification**: Remove identifiers as early as possible in the data pipeline
4. **Access Control**: Role-based access with least-privilege principle
5. **Audit Trail**: All data access and use logged and reviewable
6. **Community Benefit**: Research outcomes should benefit the communities that provided data
7. **Transparency**: Data practices documented and publicly available
8. **Privacy by Default**: Prefer local-only, no-storage, ephemeral, aggregate,
   or synthetic workflows before retaining sensitive data

## No-Storage and Ephemeral Processing

For contributor tools that accept menstrual health inputs, the preferred design is
no-storage:

- Process data on-device whenever possible
- If a server is needed, process in memory and delete raw input immediately
- Disable request-body logging for sensitive routes
- Do not store raw uploads, exact dates, precise location, names, contact
  details, or raw free text unless approved
- Store only minimal derived outputs when there is a clear purpose
- Document retention, deletion, and third-party processing in the project README

## Prohibited Uses
- Commercial exploitation of participant data without explicit consent
- Re-identification of de-identified participants
- Sharing data with unauthorized third parties
- Using data for purposes not specified in the data-use agreement
- Accessing data without proper authorization
- Publishing data that could identify individuals or small communities
- Sending sensitive menstrual health inputs to analytics, advertising,
  telemetry, or LLM services without explicit disclosure, consent, and approval
- Presenting diagnostic-support prototypes as clinically validated diagnostic
  tools without evidence, review, and appropriate oversight

## Contribution Acceptance Requirements

Any contribution that touches data should include:

- Problem statement and intended users
- Data tier or contribution lane
- Data flow summary: collected, processed, stored, transmitted, deleted
- Demo dataset source and confirmation that it is synthetic or fictional
- Schema, validation, API, or export format used
- Data quality checks or known data quality limitations
- Accessibility and low-resource considerations where relevant
- Evaluation approach, test cases, or success criteria
- Retention period and deletion behavior for anything stored
- Third-party services used, if any
- Safety language for diagnostic-support features
- Privacy checklist completion for local-only, ephemeral, aggregate, or
  controlled-access workflows

For non-data projects, use `../builder_readiness_guide.md` as the main review
standard.

## Governance Structure
- **Data Governance Board**: Oversees data access decisions and policy compliance
- **Ethics Review Committee**: Reviews research proposals and consent processes
- **Community Advisory Council**: Ensures community voices inform data practices
- **Technical Security Team**: Maintains data infrastructure and access controls

## Contact
For data access requests or questions about this policy:
- **Email**: [insert governance contact]
- **Data Access Request Form**: [to be added]

---

*Version 0.1.0 - Last updated: January 2024*
