# Menstrual Health Open Data Governance

## Principles

1. **Open the infrastructure. Protect the people.**
2. Build broadly; restrict only unsafe handling of real participant data
3. Participant welfare and dignity are paramount
4. Data minimization: collect only what is necessary
5. Privacy by default: prefer synthetic, local-only, no-storage, ephemeral,
   aggregate, or controlled-access patterns
6. Data quality by design: validate, normalize, document, and test data flows
7. Interoperability by design: use shared schemas, APIs, and export formats
8. Accessibility by design: account for language, literacy, disability,
   connectivity, and CHW workflows
9. Transparency in all data practices
10. Community benefit drives research priorities

## Contributor Position

Menstrual Health Open welcomes contributions in any useful direction: data
quality, diagnostic support, AI, voice, CHW workflows, sensors, consent, privacy
infrastructure, validation, interoperability, synthetic data, research tools,
education, localization, community materials, and governance.

The public repo should not contain real participant menstrual health data. Build
with one of these safe lanes:

- Synthetic-only data
- Local-only or no-storage processing
- Ephemeral server processing with no retained raw input
- Aggregate-only outputs
- Properly de-identified examples
- Controlled-access tooling with synthetic fixtures

See
[`governance/builder_readiness_guide.md`](../governance/builder_readiness_guide.md),
[`governance/contribution_policy.md`](../governance/contribution_policy.md)
and
[`governance/privacy_preserving_patterns.md`](../governance/privacy_preserving_patterns.md).

## Contribution Quality

Safety is one requirement, not the whole standard. Contributor projects should
also show:

- Clear problem and intended users
- Connection to Menstrual Health Open schemas, synthetic data, validation, docs,
  governance, or another reusable project layer
- Data quality checks or a plan for validation
- Accessibility and low-resource design considerations
- Interoperable inputs and outputs
- Evaluation approach, test cases, or known failure modes
- Responsible diagnostic-support language where applicable
- Setup instructions, dependency notes, and limitations

## Governance Structure

### Data Governance Board

Oversees data access decisions and policy compliance. Reviews all Tier 3-5 data
access requests.

### Ethics Review Committee

Reviews research proposals, consent processes, and data sharing agreements.
Ensures compliance with ethical standards and local regulations.

### Community Advisory Council

Ensures community voices inform data practices. Includes representatives from
partner organizations, community health workers, and research participants.

### Technical Security Team

Maintains data infrastructure, access controls, and security protocols.

## Policies

- [Contribution Policy](../governance/contribution_policy.md)
- [Builder Readiness Guide](../governance/builder_readiness_guide.md)
- [Privacy-Preserving Build Patterns](../governance/privacy_preserving_patterns.md)
- [Data Access Policy](../governance/data_access_policies/data_access_policy.md)
- [Ethics Checklist](../governance/ethics_checklist.md)
- [Consent Template](../governance/consent_templates/informed_consent.md)
- [Partner Onboarding](../governance/partner_onboarding.md)

## Data Classification

### Public (Tier 1)

Open documentation, schema, code, research methods, and contributor resources.

### Synthetic (Tier 2)

Fake or fixture datasets for development, such as `synthetic-data/sample_20.csv`.
No real participant data.

### Aggregate (Tier 3)

Regional summaries and broad statistics. Reviewed for small cells and
re-identification risk before release.

### Controlled (Tier 4)

De-identified individual-level data. Requires DUA, ethics approval, and
governance review. Public repo contributions for this layer must use synthetic
fixtures.

### Private (Tier 5)

Original participant records, raw media, identifiers, consent records, and
partner-submitted raw files. Accessible only to data subjects and authorized
stewards.

## No-Storage Standard

For contributor tools that invite users to enter menstrual health information:

- Process input on-device when possible
- If a server is needed, process in memory and delete raw input immediately
- Do not write raw inputs to disk, database, logs, telemetry, analytics, or crash
  reports by default
- Store only a non-identifying derived output when there is a clear purpose
- Use coarse categories instead of exact dates, precise locations, or direct
  identifiers
- Document data flow, retention, deletion, and third-party services

## Compliance

Real-world data activities must comply with:

- Applicable national and regional data protection laws
- Institutional ethics requirements
- Partner agreements
- Menstrual Health Open Data Access Policy
- This governance framework

Prototypes are not automatically approved for real participant data
collection or clinical deployment.

## Reporting

Data incidents, access requests, and governance decisions are logged and reported
to the Data Governance Board quarterly.

## Contact

- **Governance**: [insert governance contact]
- **Ethics**: [insert ethics contact]
- **Security**: [insert security contact]

---

*Part of the Menstrual Health Open governance framework*
