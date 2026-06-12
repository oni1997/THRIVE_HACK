# Contributing

Thank you for contributing to Menstrual Health Open.

## What You Can Contribute

- Code
- Documentation
- Governance resources
- Validation rules
- Synthetic datasets
- Project inspirations
- Research methods
- Translation and localization
- Accessibility improvements
- Research question sets
- Issue triage and review

## Contribution Rules

- Use synthetic, fictional, or approved aggregate data in public contributions.
- Do not add real participant-level health data.
- Do not add names, phone numbers, precise location, exact cycle dates, raw free
  text, consent records, partner files, secrets, or credentials.
- Document the problem, intended users, data flow, and limitations.
- Use careful diagnostic-support language. Do not claim clinical validation
  unless appropriate review and evidence exist.

## Before Submitting

- Run validation on any dataset you add.
- Make sure examples are clearly marked as synthetic, fictional, or aggregate.
- Update relevant docs.
- Add tests for Python utilities when practical.
- Check the relevant issue template if you are opening a new idea, bug report,
  or governance review.

## Pull Request Workflow

Work from a branch and open a pull request into `main`.

```powershell
git checkout -b contributor/short-description
# make changes
git add .
git commit -m "Describe contribution"
git push origin contributor/short-description
```

Do not push directly to `main`. Maintainers should enable GitHub branch
protection or rulesets so `main` requires pull requests, review, and passing CI.
See `docs/branch_protection.md`.

If you are not ready to open a pull request, open an issue first. Ideas are
welcome as broad directions, not as fixed assignments.

## Review Standard

Contributions are reviewed for:

- Usefulness
- Data quality
- Interoperability
- Accessibility
- Privacy and governance
- Maintainability
- Clear documentation

## Licensing of Contributions

Unless clearly stated otherwise, contributions are accepted under the license
that applies to the file or directory being changed. See `docs/licensing.md`.
