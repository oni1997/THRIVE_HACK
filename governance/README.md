# governance/

Ethical governance framework for menstrual health data. Provides templates,
policies, and checklists for responsible data collection, access, and use.

This folder is designed to help contributors build usable
open-source infrastructure that can be accepted, reused, and contributed back to
Menstrual Health Open.

Governance is not only about safety. It also covers usefulness, data quality,
interoperability, accessibility, clinical responsibility, evaluation,
maintainability, and community value.

## Guiding Principle

**Open the infrastructure. Protect the people.**

For contributor work, this means:

- Build in any useful direction: data tools, AI, diagnostic support, CHW
  workflows, sensors, voice, dashboards, consent systems, privacy tooling, or
  infrastructure.
- Make the project usable by others: clear problem, clear users, synthetic demo,
  setup instructions, evaluation plan, and documented limitations.
- Use shared schemas, validation, and export formats where possible so tools can
  plug into the broader ecosystem.
- Use synthetic, local-only, ephemeral, aggregate, or properly de-identified data
  for public demos and repo contributions.
- Do not put real participant data, raw recordings, identifiers, consent forms,
  or secrets in the public repo.
- Treat privacy-preserving architecture as a design constraint, not a ban on
  data innovation.

## Contents

| File/Directory | Purpose |
|----------------|---------|
| `builder_readiness_guide.md` | Positive build standards for useful, reusable, interoperable, accessible contributions |
| `contribution_policy.md` | Builder-friendly rules for what can be contributed to the open-source ecosystem |
| `privacy_preserving_patterns.md` | No-storage, local-first, ephemeral, aggregate, federated, and controlled-access design patterns |
| `consent_templates/informed_consent.md` | Standard informed consent form template for menstrual health research, including audio/video recording consent |
| `data_access_policies/data_access_policy.md` | 5-tier data access model from public infrastructure to private participant data |
| `ethics_checklist.md` | Pre-collection, processing, sharing, and publication review checklist |
| `partner_onboarding.md` | Guide for new partners and organizations |

## Tiered Data Access Model

| Tier | Content | Access |
|------|---------|--------|
| 1 - Public | Docs, schema, code | Open to all |
| 2 - Synthetic | Fake datasets | Open to all |
| 3 - Aggregate | Regional summaries | After privacy review |
| 4 - Controlled | De-identified data | Approved researchers |
| 5 - Private | Raw participant data | Data subjects and authorized stewards only |

## Voice/Video Consent

The consent template includes an audio/video recording addendum for:

- Verbal consent recording before data collection
- Participant right to withdraw
- Confidentiality of recordings
- Use of recordings for research purposes

For public demos, do not upload real participant voice/video. Use
synthetic, volunteer test, or fictional demo media unless an approved research
protocol and consent process are already in place.

## Field Media And Transcription Ethics

Field audio, video, and transcripts should follow the same consent and
privacy-preserving standards before entering the Menstrual Health Open pipeline:

- Consent captured in participant languages
- Raw media kept in restricted storage, never the public repo
- Transcripts de-identified before consumer or researcher processing
- Local/offline collection protected with encryption and deletion procedures
- Third-party transcription or translation disclosed and approved

## Using These Documents

- **For contributors**: Start with
  `builder_readiness_guide.md`, `contribution_policy.md`, and
  `privacy_preserving_patterns.md`
- **For researchers**: Use `ethics_checklist.md` before starting any data
  collection
- **For partners**: Complete `partner_onboarding.md` to join the ecosystem
- **For data collection**: Adapt `informed_consent.md` to your local context
- **For voice/video recording**: Follow the consent template and
  `privacy_preserving_patterns.md`
- **For data sharing**: Follow `data_access_policy.md` tiered model

## Standards Alignment

The framework is aligned with common privacy and research governance practices:

- Open science and reusable research infrastructure principles
- Data quality and validation expectations for research datasets
- Interoperability expectations for health and research data exchange
- Accessibility expectations for inclusive digital tools
- Data minimization, purpose limitation, storage limitation, security, and
  accountability
- Privacy by design and by default
- De-identification review before releasing participant-level data
- Informed consent and ethics review for human-subjects research
- Clear data flows, retention limits, withdrawal paths, and access controls

This folder is not legal advice. Teams collecting real participant data must
obtain local legal, ethics, and community review.
