# Contribution Policy

This policy explains how contributors can build freely while keeping
menstrual health data safe enough for open-source contribution.

It is not only a safety policy. It is also a contribution policy: projects
should be useful, understandable, interoperable, accessible, testable, and easy
for others to extend.

## Core Position

Menstrual Health Open should not limit builders to one kind of idea. Participants may build
tools, infrastructure, models, workflows, sensors, dashboards, consent systems,
voice tools, validation tools, privacy systems, data pipelines, and diagnostic
support prototypes.

The policy limits only unsafe data handling, not the direction of the idea.

**Default rule for the public repository: build with synthetic, local-only,
ephemeral, aggregate, or properly de-identified data. Do not submit real
identifiable participant data, raw recordings, private health records, consent
forms, or secrets.**

**Contribution rule: make the idea usable. A submission should explain the
problem, intended users, data flow, Menstrual Health Open integration point, evaluation
approach, limitations, and next steps.**

## What Makes a Strong Contribution

Strong submissions usually include:

- A clear menstrual health problem or infrastructure gap
- A defined user: participant, CHW, researcher, clinician, partner, educator,
  policymaker, or developer
- A working prototype, schema, workflow, model, dashboard, API, or design that
  can be inspected
- Synthetic or fictional demo data
- A documented data flow
- Connection to Menstrual Health Open schema, validation, API, governance, examples, or docs
- Accessibility or low-resource design considerations
- Evaluation criteria, test cases, or known failure modes
- Responsible wording for diagnostic-support features
- Setup instructions and dependency notes

See `builder_readiness_guide.md` for the full readiness checklist.

## Contribution Lanes

| Lane | What participants can build | Public repo status | Review needed |
|------|-----------------------------|--------------------|---------------|
| 0 - Synthetic-only | Apps, models, dashboards, validation tools, demos, tests using fake data | Accepted | Standard code review |
| 1 - Local-only / no-storage | Tools where participant input stays on the user's device and is not retained | Accepted if clearly documented | Standard code review + privacy checklist |
| 2 - Ephemeral processing | Server or edge tools that process input in memory and delete it immediately | Accepted if logs/storage are disabled or scrubbed | Privacy checklist |
| 3 - Aggregate-only | Tools that output group summaries, trends, or public dashboards | Accepted after small-cell and re-identification review | Privacy review |
| 4 - Controlled de-identified research | Tools designed for approved researchers using de-identified individual records | Accepted as infrastructure; real data stays outside repo | Governance review before real use |
| 5 - Raw/private participant data | Consent records, names, direct identifiers, raw clinical files, raw participant media | Not accepted in public repository | Steward-only environment |

## What Is Encouraged

Participants are encouraged to explore any useful direction. Possible directions
include:

- No-storage menstrual health data collection where data never leaves the device
- Local-first analysis and offline-first community health worker workflows
- Ephemeral APIs that return results without retaining raw inputs
- Anonymization, de-identification, redaction, and privacy review tools
- Synthetic data generation and synthetic benchmark datasets
- Federated learning, secure aggregation, differential privacy, and edge AI
- Consent management, withdrawal workflows, and audit trails
- Data quality scoring, schema mapping, and interoperability tools
- Diagnostic-support prototypes for triage, referral, education, or research
- Hardware, sensor, wearable, image, voice, and low-connectivity workflows

## Hard Lines

These are the things that will block a contribution:

- Real participant data committed to the repo, issue tracker, demo dataset, logs,
  screenshots, or public deployment
- Participant names, phone numbers, email addresses, exact addresses, precise GPS,
  face images, raw voice/video, unredacted free text, or direct clinical records
- Re-identification attempts or tooling intended to identify participants
- Sharing data with third-party services, SDKs, analytics, ad networks, or LLMs
  without explicit disclosure, consent, and approval
- Diagnostic claims that imply clinical accuracy without validation, clinical
  oversight, and clear limitation language
- Storage of raw menstrual health inputs without a retention period, deletion
  path, access controls, and documented purpose
- Any use outside the stated purpose or consent scope

## Minimum Acceptance Checklist

Every contribution should include:

- Problem: what issue the project addresses
- Users: who it is for and in what setting
- Data lane: identify whether the project is Lane 0, 1, 2, 3, 4, or 5
- Data flow: describe what is collected, processed, stored, transmitted, and
  deleted
- Demo data: use synthetic data or clearly marked fictional examples
- Project fit: explain whether it extends schemas, synthetic data, validation,
  governance, documentation, infrastructure, or another reusable project layer
- Evaluation: include test cases, metrics, expected output, or success criteria
- Accessibility: note language, offline, low-literacy, disability, youth, CHW, or
  low-connectivity considerations
- Privacy mode: explain whether the tool is local-only, ephemeral, aggregate,
  de-identified, or controlled-access
- Retention: state whether data is stored; if yes, why, where, for how long, and
  how it can be deleted
- Consent: explain whether real users are involved; if yes, identify the consent
  and ethics approval path
- Safety: avoid clinical diagnosis language unless the tool has appropriate
  validation and oversight
- Maintainability: include setup instructions, dependency notes, and known
  limitations

## No-Storage Standard

For contributor tools that invite users to enter menstrual health information, the
preferred standard is:

1. Process input on-device when possible.
2. If a server is needed, process in memory and return the result immediately.
3. Do not write raw inputs to disk, database, analytics, error tracking, or logs.
4. Store only a non-identifying derived output when there is a clear purpose.
5. Use coarse categories instead of exact dates, locations, or identifiers.
6. Provide a clear delete/export path for anything retained.
7. Document the data flow in the README.

## Real Participant Data

Contributors should not collect or upload real participant menstrual
health data into public demos or this repository.

A project may be designed to support future real-world data collection, but real
collection requires:

- Institutional ethics review or documented exemption
- Local legal and cultural review
- Informed consent in participant languages
- Data steward approval
- Secure storage and access controls
- Retention and deletion procedures
- Incident response process

## How This Policy Avoids Limiting Builders

The policy does not say "do not build data tools." It says "choose a safe data
lane." A strong project can be ambitious while still using synthetic
data, no-storage architecture, de-identification, secure aggregation, or
controlled-access assumptions.

The policy also does not say "only work on safety." It asks teams to build
things that can actually be used: useful workflows, reliable data structures,
accessible interfaces, interoperable exports, meaningful evaluation, and clear
documentation.

Open the infrastructure. Protect the people. Build things others can use.
