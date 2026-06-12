# governance/data_access_policies/

Data access policies defining who can access menstrual health data and under
what conditions.

For contributors, the goal is to enable broad building while keeping real
participant data out of public demos and repo contributions.

## Files

| File | Purpose |
|------|---------|
| `data_access_policy.md` | Complete data access policy with 5-tier model |

## 5-Tier Access Model

| Tier | Name | Content | Requirements |
|------|------|---------|--------------|
| 1 | Public | Docs, schema, code | None |
| 2 | Synthetic | Fake datasets | None |
| 3 | Aggregate | Regional summaries | Privacy review |
| 4 | Controlled | De-identified data | DUA + ethics approval + governance review |
| 5 | Private | Raw participant data | Data subject consent + steward authorization |

## Contribution-Safe Modes

Contributors can explore approaches using:

- Synthetic-only datasets
- Local-only or no-storage processing
- Ephemeral APIs that do not retain raw inputs
- Aggregate-only outputs after small-cell review
- De-identified examples with documented re-identification review
- Controlled-access tooling with synthetic fixtures in the public repo

Do not commit real participant data, raw media, consent records, direct
identifiers, secrets, or private health records.

## Key Principles

1. **Minimization** - Collect only what is necessary
2. **Purpose Limitation** - Data used only for approved purposes
3. **De-identification** - Remove identifiers early
4. **Access Control** - Least-privilege role-based access
5. **Audit Trail** - All access logged
6. **Community Benefit** - Research benefits the communities that provided data
7. **Transparency** - Practices documented and public

## Prohibited Uses

- Commercial exploitation without consent
- Re-identification of de-identified participants
- Sharing with unauthorized third parties
- Accessing data without authorization
- Hidden analytics, ad SDKs, telemetry, or LLM sharing of sensitive health input
- Unsupported clinical diagnostic claims
