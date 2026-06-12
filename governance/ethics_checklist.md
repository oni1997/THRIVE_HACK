# Ethics Review Checklist

Use this checklist before initiating any menstrual health data collection,
analysis, or sharing activity.

For open-source contribution, this checklist should help contributors build
more useful projects, not block creativity. Synthetic-only, local-only,
ephemeral, and aggregate-first projects can usually move quickly. Projects that
collect or store real participant health data need formal review before real
deployment.

## Contribution Review

- [ ] Problem statement is clear and connected to menstrual health research,
  care, diagnosis support, data infrastructure, education, or access
- [ ] Intended users and setting are identified
- [ ] Project explains how it uses or extends Menstrual Health Open schemas,
  synthetic data, validation, docs, governance, or another reusable project
  layer
- [ ] Demo can be run by reviewers using documented setup steps
- [ ] Project includes test cases, sample output, evaluation criteria, or known
  failure modes
- [ ] Accessibility, language, offline, low-literacy, youth, disability, or CHW
  considerations are documented where relevant
- [ ] Project identifies its data lane: synthetic-only, local-only/no-storage,
  ephemeral processing, aggregate-only, controlled research, or raw/private
- [ ] Public demo uses synthetic, fictional, volunteer test, or properly
  de-identified data
- [ ] No real participant data, consent records, raw recordings, private health
  records, secrets, or direct identifiers are committed to the repo
- [ ] Data flow is documented: collected, processed, stored, transmitted,
  retained, and deleted
- [ ] If the tool accepts menstrual health input, the default design is
  local-only or no-storage unless storage is justified
- [ ] Logs, analytics, crash reports, telemetry, and error traces do not capture
  sensitive health input
- [ ] Third-party services, SDKs, LLMs, or cloud processors are disclosed
- [ ] Diagnostic-support features include clear limitations and do not claim
  clinical validation unless evidence and oversight exist
- [ ] README explains how future real-world use would handle consent, ethics
  approval, data access, retention, and deletion

## Pre-Collection Review

- [ ] Research protocol reviewed by ethics board (IRB or equivalent)
- [ ] Informed consent process designed and documented
- [ ] Consent form translated into all participant languages
- [ ] Data minimization assessment completed (collecting only what is necessary)
- [ ] Risk assessment completed (physical, psychological, social risks)
- [ ] Vulnerable populations considerations addressed
- [ ] Data security plan documented and approved
- [ ] Participant recruitment materials reviewed for cultural sensitivity
- [ ] Compensation plan reviewed for ethical appropriateness
- [ ] Community engagement plan developed

## No-Storage / Local-First Review

- [ ] Data processing happens on device when feasible
- [ ] Raw inputs are not written to disk, database, telemetry, or logs by default
- [ ] Temporary files are deleted immediately after processing
- [ ] Any retained output is minimized, non-identifying, and justified
- [ ] Exact dates, precise location, contact details, and direct identifiers are
  avoided unless required and approved
- [ ] User can reset, delete, or avoid storing data

## Data Collection Review

- [ ] Consent process implemented as designed
- [ ] Data collection tools tested for usability and accessibility
- [ ] Field staff trained on ethics and data protection
- [ ] Participant right to withdraw clearly communicated
- [ ] Adverse event reporting process in place
- [ ] Data storage and backup procedures verified

## Data Processing Review

- [ ] De-identification process documented
- [ ] Re-identification risk assessment completed
- [ ] Synthetic data generation verified (no real data in public outputs)
- [ ] Free-text fields reviewed for accidental identifiers
- [ ] Audio/video/image-derived outputs reviewed before sharing
- [ ] Pseudonymous IDs are not reversible without a separate approved key
- [ ] Data quality validation completed
- [ ] Missing data handling approach documented
- [ ] Statistical methods appropriate for the data and questions

## Data Sharing Review

- [ ] Tiered access classification completed for all data products
- [ ] Data-use agreements in place for controlled access data
- [ ] Aggregate data reviewed for re-identification risk
- [ ] Small cells suppressed or generalized
- [ ] Geography, date, age, and rare-condition combinations reviewed for
  uniqueness risk
- [ ] Community benefit assessment completed
- [ ] Partner agreements reviewed for data sharing provisions
- [ ] International data transfer compliance verified (if applicable)

## Publication and Reporting Review

- [ ] Results reviewed for potential harm to communities
- [ ] Small cell suppression applied (no identifying aggregates)
- [ ] Community members consulted on findings presentation
- [ ] Limitations and caveats clearly stated
- [ ] Data access information included for reproducibility
- [ ] Authorship and contributor recognition documented

## Ongoing Compliance Review

- [ ] Data access logs reviewed regularly
- [ ] Participant withdrawal requests processed promptly
- [ ] Data retention schedule followed
- [ ] Security incidents reported and addressed
- [ ] Policy updates communicated to all stakeholders

## Red Flags: Stop and Consult

If any of the following occur, halt the activity and consult the Ethics Review
Committee:

- Potential for participant re-identification
- Data access by unauthorized individuals
- Use of data beyond approved purposes
- Discovery of sensitive information about identifiable individuals
- Community complaints about data practices
- Security breach or data loss
- Real participant data appears in a public PR, issue, screenshot, demo, log, or
  dataset
- A tool stores raw menstrual health input without consent, retention limits, or
  deletion behavior
- A prototype makes medical diagnostic claims without clinical validation

---

*Part of the Menstrual Health Open governance framework*
