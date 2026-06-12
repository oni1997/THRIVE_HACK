# Builder Readiness Guide

This guide helps contributors build projects that can be reused,
reviewed, contributed, piloted, or extended after the event.

It is not only a safety checklist. A strong Menstrual Health Open contribution should be useful,
understandable, technically sound, respectful of communities, and easy for
others to build on.

## What Good Looks Like

A project is contribution-ready when it can answer:

- What menstrual health problem does it solve?
- Who is it for: participants, community health workers, researchers, clinicians,
  partners, policymakers, educators, or developers?
- What data does it need, and can it work with synthetic or no-storage data?
- How does it improve diagnosis support, data quality, access, education,
  infrastructure, or research?
- Can another team run, test, understand, and extend it?
- Does it fit the Menstrual Health Open schema, governance model, and open-source direction?

## Build Pillars

| Pillar | What it means | Example evidence |
|--------|---------------|------------------|
| Usefulness | Solves a real menstrual health workflow or infrastructure gap | Clear user, use case, and output |
| Data Quality | Improves collection, validation, normalization, completeness, or interpretation | Validation checks, quality scores, schema mapping |
| Interoperability | Can connect to Menstrual Health Open schemas, APIs, exports, or health data systems | JSON/CSV contract, documented fields, FHIR-ready mapping where relevant |
| Privacy & Governance | Protects people while enabling useful analysis | Safe data lane, consent path, retention/deletion behavior |
| Accessibility & Inclusion | Works for low-connectivity, low-literacy, multilingual, disability, youth, or CHW contexts | Offline mode, language support, accessible UI, plain-language outputs |
| Clinical Responsibility | Uses careful diagnostic-support language and clear escalation paths | Triage wording, limitations, referral guidance, validation plan |
| Evaluation | Shows how success will be measured | Test cases, metrics, sample outputs, known failure modes |
| Reusability | Other contributors can run and extend it | README, setup steps, examples, license-compatible dependencies |
| Maintainability | Code and docs are organized enough for future work | Small modules, tests, documented assumptions |
| Community Value | Benefits the people and communities represented in the data | Feedback loop, community-facing output, non-extractive design |

## Contribution Readiness Checklist

Every submission should include:

- [ ] Short problem statement
- [ ] Intended users and setting
- [ ] Data lane: synthetic, local-only/no-storage, ephemeral, aggregate,
  controlled, or private
- [ ] Data flow: inputs, processing, outputs, storage, transmission, deletion
- [ ] How it uses or extends Menstrual Health Open schema, validation, API, governance, or docs
- [ ] Demo instructions using synthetic or fictional data
- [ ] Known limitations and failure modes
- [ ] Evaluation approach or test cases
- [ ] Accessibility and language considerations
- [ ] Responsible diagnostic-support wording, if health recommendations are shown
- [ ] Setup/run instructions
- [ ] License and dependency notes

## Data and Diagnostics Projects

Data and diagnostic-support projects are encouraged. They should be framed so
they can mature responsibly:

- Use "screening support," "triage support," "risk flag," "education," or
  "research prototype" unless clinical validation exists
- Show what evidence would be needed before field use
- Include an escalation/referral path where relevant
- Separate data capture, inference, explanation, and action recommendations
- Make uncertainty visible rather than hiding it
- Avoid making the user feel diagnosed, blamed, or dismissed

## Interoperability Expectations

Prefer:

- Menstrual Health Open schema fields or documented extensions
- ISO-style dates when exact dates are appropriate; otherwise use coarse dates
- ISO 3166-1 country codes where country data is needed
- Documented categorical values instead of free-form labels
- JSON or CSV exports that can be validated
- Stable APIs with example requests and responses
- Clear mapping notes for health data standards such as HL7 FHIR when a tool is
  meant to connect to clinical systems

## Accessibility Expectations

For participant, CHW, or community-facing tools, consider:

- Offline or low-bandwidth use
- Plain-language text
- Translation and localization path
- Voice input/output where helpful
- Keyboard-accessible and screen-reader-friendly UI
- Large tap targets and readable contrast
- Low-literacy and youth-friendly workflows
- Clear consent and withdrawal flows

## Evaluation Expectations

Even a prototype should show how it would be judged:

- Input examples and expected outputs
- Synthetic test cases
- Validation rules
- Quality metrics
- Error states
- Bias or coverage risks
- Human review points
- What would need to be proven before real-world deployment

## README Template

Each project README should cover:

```markdown
# Project Name

## Problem

## Intended Users

## What It Does

## Data Lane

## Data Flow

## How It Uses Menstrual Health Open

## Demo With Synthetic Data

## Evaluation

## Accessibility and Inclusion

## Privacy and Governance

## Diagnostic-Support Limitations

## Setup

## Known Limitations

## Future Work
```

## Review Philosophy

Menstrual Health Open should help people build, not make them afraid to contribute. Reviewers
should ask:

- Is the idea useful?
- Is the data flow understandable?
- Can it be run and improved?
- Does it avoid avoidable harm?
- Does it move menstrual health research, care, infrastructure, or access
  forward?

Open the infrastructure. Protect the people. Build things others can use.
