# Menstrual Health Open

Open-source infrastructure for ethical menstrual health research.

This repository is built for a global menstrual health research infrastructure
hackathon and for ongoing open-source contribution after the event. It provides
schemas, synthetic datasets, a basic validation baseline, documentation,
governance resources, and open-ended project inspirations that contributors can
pull, run, improve, and adapt.

This is not an open raw-data project. Real participant-level menstrual health
data is sensitive and is not included in this repository. Contributors use
synthetic datasets and open project resources to build reusable infrastructure.

## Guiding Principle

**Open the infrastructure. Protect the people.**

All code, standards, documentation, synthetic datasets, research methods, and
governance resources are open for contribution. Sensitive participant-level
health data remains protected and is not used during the hackathon.

## Main Prompt

How might we build the tools, standards, and systems needed to make menstrual
health data more accessible, reliable, ethical, and useful for research
worldwide?

Four official sub-prompts (A-D) focus this question on measurement at the
margins, signal from community data, closing the diagnosis gap, and
engineering the built environment. See
[issues/challenge_statements.md](issues/challenge_statements.md).

## What Contributors Can Explore

The repository does not prescribe what participants must build. It provides a
shared foundation and a set of inspirations. Contributors can follow those
directions, remix them, or define something different.

Possible areas include data quality, synthetic data, interoperability,
accessibility, localization, privacy-preserving analytics, partner workflows,
public communication, education, governance, research methods, and community
engagement.

## Repository Map

| Path | Purpose |
| --- | --- |
| `schema/` | Data dictionary, survey schema, and field definitions. |
| `synthetic-data/` | Synthetic dataset generator and sample fake data. |
| `validation/` | Dataset validation script and quality rules. |
| `docs/` | Project brief, challenge tracks, contributor workflow, and data model docs. |
| `governance/` | Consent templates, access policy, ethics checklist, and builder readiness guide. |
| `dashboard/` | Starter Streamlit dashboard template. |
| `notebooks/` | Research notebooks for exploration, data quality, and analysis patterns. |
| `issues/` | Challenge statements and starter issue backlog. |
| `inspirations/` | Open-ended project inspirations, not assignments or limits. |
| `src/menstrual_health_open/` | Lightweight Python utilities used by starter scripts. |
| `tests/` | Tests for synthetic data and validation helpers. |
| `.github/` | CI, pull request template, issue templates, and code owner routing. |

## Quick Start

Generate a synthetic dataset:

```powershell
python synthetic-data/generate.py --count 100 --output synthetic-data/generated_100.csv
```

The generator accepts any non-negative `--count` and writes records as a stream,
so contributors can generate larger synthetic datasets as needed. Practical
limits are disk space and runtime.

Generate a dataset with optional-field missingness for testing:

```powershell
python synthetic-data/generate.py --count 100 --missingness 0.15 --output synthetic-data/generated_missingness.csv
```

Validate a dataset:

```powershell
python validation/validate_dataset.py synthetic-data/sample_20.csv
```

Run the package CLI:

```powershell
$env:PYTHONPATH = "src"
python -m menstrual_health_open.cli generate --count 100 --output synthetic-data/generated_100.csv
python -m menstrual_health_open.cli validate synthetic-data/generated_100.csv
```

## Contributor Workflow

1. Read [docs/project_brief.md](docs/project_brief.md).
2. Review [inspirations/project_inspirations.md](inspirations/project_inspirations.md).
3. Explore the schema and synthetic data.
4. Define a contribution direction.
5. Develop or document your contribution using synthetic data or documented
   aggregate assumptions.
6. Submit code, docs, governance, design, translation, or research contributions.
7. Explain how your work improves menstrual health research infrastructure.

## Governance

Start with:

- [Builder Readiness Guide](governance/builder_readiness_guide.md)
- [Contribution Policy](governance/contribution_policy.md)
- [Privacy-Preserving Build Patterns](governance/privacy_preserving_patterns.md)
- [Data Governance Overview](docs/data_governance.md)
- [Data Access Policy](governance/data_access_policies/data_access_policy.md)
- [Ethics Checklist](governance/ethics_checklist.md)
- [Informed Consent Template](governance/consent_templates/informed_consent.md)

## Data Access Model

| Layer | Content | Access |
| --- | --- | --- |
| Public | Docs, schema, code, methods | Open |
| Synthetic | Fake datasets and fixtures | Open |
| Aggregate | Reviewed summaries | Public after privacy review |
| Controlled | De-identified research datasets | Approved researchers only |
| Private | Raw participant records and consent records | Never public |

## Current Status

This is a starter scaffold. It is intentionally small, readable, and safe to run
locally. The goal is to make contribution easy without exposing sensitive data.

## Repository Protection

Contributors should work on branches and submit pull requests. Direct pushes to
`main` should be blocked using GitHub branch protection or rulesets. See
[docs/branch_protection.md](docs/branch_protection.md).

Maintainers preparing a public launch can also use
[docs/maintainer_launch_checklist.md](docs/maintainer_launch_checklist.md).

## License

Code is licensed under Apache License 2.0. Documentation and governance
materials are licensed under CC BY 4.0. Synthetic datasets and generated
fixtures in `synthetic-data/` are released under CC0 1.0. See
[docs/licensing.md](docs/licensing.md).
