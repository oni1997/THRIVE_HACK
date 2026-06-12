# Partner Onboarding Guide

Welcome to Menstrual Health Open. This guide walks new partners through joining
the ecosystem, contributing infrastructure, and preparing responsible data
workflows.

Contributors do not need formal partner status to contribute code,
documentation, synthetic datasets, validation tools, privacy-preserving
infrastructure, translations, examples, or design prototypes. Formal onboarding
is for organizations that want to contribute real data, access non-public data,
or participate in ongoing research operations.

Contributions are reviewed for usefulness and readiness, not only
safety. Good submissions define the problem, users, data flow, Menstrual Health Open fit,
evaluation approach, accessibility considerations, and limitations.

## Who Can Partner?

- **Research institutions** conducting menstrual health studies
- **Healthcare organizations** serving menstruating populations
- **Community organizations** with grassroots health programs
- **Schools and universities** with student health initiatives
- **Government agencies** responsible for public health
- **Technology organizations** building health tools
- **NGOs** focused on menstrual equity

## Partnership Levels

### Open-Source Contributor
**Who**: Individuals or teams building open-source prototypes, examples,
documentation, schemas, validation tools, or infrastructure

**Benefits**:
- Ability to contribute code, docs, schemas, examples, synthetic data, and
  privacy-preserving infrastructure
- Use of public docs, public schema, synthetic data, and validation tools
- Eligibility for standard open-source review

**Requirements**:
- Follow the Contribution Policy
- Follow the Builder Readiness Guide
- Use synthetic, local-only, ephemeral, aggregate, or properly de-identified data
  in public demos and repo contributions
- Do not submit real participant data, raw media, consent records, direct
  identifiers, or secrets
- Document data flow and privacy mode in the project README
- Document problem, intended users, evaluation approach, accessibility
  considerations, and known limitations

**Does not include**:
- Access to controlled research data
- Approval to collect real participant data
- Permission to publish diagnostic claims
- Permission to store raw participant health data

### Contributor
**Who**: Organizations submitting data or resources
**Benefits**:
- Access to synthetic data and development tools
- Data quality feedback on submissions
- Recognition in contributor acknowledgments
- Access to aggregate insights from the broader dataset

**Requirements**:
- Signed partnership agreement
- Compliance with data submission standards
- Completion of data ethics training

### Collaborator
**Who**: Organizations actively co-developing tools or research
**Benefits**:
- Everything in Contributor
- Access to controlled research data (after ethics approval)
- Co-authorship opportunities on publications
- Priority access to new platform features
- Direct engagement with the technical team

**Requirements**:
- Everything in Contributor
- Active contribution to platform development
- Regular participation in partner meetings
- Ethics approval for research activities

### Strategic Partner
**Who**: Organizations with significant resource or data contributions
**Benefits**:
- Everything in Collaborator
- Representation on the Community Advisory Council
- Input on platform roadmap and priorities
- Co-branding opportunities
- Dedicated technical support

**Requirements**:
- Everything in Collaborator
- Significant sustained contribution
- Alignment with Menstrual Health Open mission and values
- Commitment to open-source principles

## Getting Started

### Step 1: Complete Partner Registration
Fill out the partner registration form when the project publishes one. It should
collect:
- Organization name and type
- Contact information
- Intended contribution (data, tools, research, funding)
- Geographic focus area
- Institutional ethics approval status (if applicable)

### Step 2: Review Governance Documents
Read and acknowledge:
- Data Access Policy
- Ethics Checklist
- Consent Templates
- Contribution Guidelines

### Step 3: Complete Ethics Training
All partner staff who will handle real participant data must complete an
approved data ethics and protection training process before any non-public data
workflow begins.

### Step 4: Set Up Technical Access
- Request technical access through the approved partner onboarding channel
- Set up secure data transfer after governance approval
- Review data schema and validation requirements

### Step 5: Submit First Data Contribution
- Prepare data in the standard format (see schema documentation)
- Run validation scripts locally before submission
- Submit through the approved partner workflow when available
- Receive data quality feedback through the review process

## Data Submission Standards

### Required Format
- JSON or CSV format following the Menstrual Health Open schema
- UTF-8 encoding
- ISO 8601 dates
- ISO 3166-1 country codes

### Starter Fields
The public starter schema includes:
- Record ID
- Age band
- Country code
- Coarse region
- Setting
- Collection month
- Cycle length
- Period duration
- Flow heaviness
- Pain score
- Controlled symptom labels
- School/work impact
- Product access
- Healthcare access
- Collection method
- Source type

### Quality Requirements
- Completeness score should meet the project threshold in `validation/quality_rules.json`
- No duplicate participant IDs
- All categorical values from approved lists
- No obvious data entry errors (validated by scripts)

## Support

- **Technical Support**: [insert technical support contact]
- **Ethics Questions**: [insert ethics contact]
- **General Inquiries**: [insert partner contact]
- **Community Forum**: [to be added]

## Code of Conduct
All partners must:
- Prioritize participant welfare and dignity
- Maintain strict data confidentiality
- Report any data incidents immediately
- Respect community voices and agency
- Contribute openly and collaboratively
- Follow the guiding principle: Open the infrastructure. Protect the people.

---

*Part of the Menstrual Health Open governance framework*
