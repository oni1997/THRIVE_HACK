# Maintainer Launch Checklist

Use this checklist before making the repository public for hackathon
participants.

## Repository Settings

- Confirm the repository description is: `Open-source infrastructure for ethical menstrual health research`.
- Add topics such as `menstrual-health`, `open-source`, `synthetic-data`,
  `data-governance`, `public-health`, `hackathon`, and `privacy`.
- Enable GitHub Actions.
- Enable branch protection or a repository ruleset for `main`.
- Require pull requests, at least one approval, code owner review, and passing
  CI before merge.
- Disable force pushes and branch deletion on `main`.

## Public Contribution Readiness

- Confirm no real participant-level data is present.
- Confirm no secrets, API keys, private partner files, or credentials are
  present.
- Confirm the sample data is synthetic and clearly labeled.
- Confirm issue templates and pull request template are visible.
- Confirm `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, and licensing files are
  visible from the repository root.

## Suggested First Issues

Create broad issues that invite exploration without limiting participants:

- Improve synthetic menstrual health data realism.
- Propose additional schema fields and explain their governance implications.
- Build a privacy-preserving validation or analytics pattern.
- Improve accessibility and localization guidance.
- Create examples for partner onboarding workflows.
- Review consent language for clarity and cultural adaptability.
- Explore data quality scoring approaches.

## Launch Principle

Open the infrastructure. Protect the people.
