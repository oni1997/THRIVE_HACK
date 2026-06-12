# Contributor Workflow

## 1. Understand The Project

Read:

- `README.md`
- `docs/project_brief.md`
- `inspirations/project_inspirations.md`
- `governance/contribution_policy.md`
- `governance/builder_readiness_guide.md`

## 2. Explore The Starter Resources

Review:

- `schema/`
- `synthetic-data/sample_20.csv`
- `validation/`
- `governance/`
- `inspirations/`

## 3. Pick A Contribution Area

Choose an inspiration, combine multiple ideas, or define your own contribution
direction.

Possible first contributions include:

- Improve field definitions
- Add validation checks
- Translate a survey field
- Write a governance checklist
- Improve accessibility guidance
- Improve synthetic data generation
- Add examples of aggregate-only reporting

## 4. Build With Synthetic Data

Generate data:

```powershell
python synthetic-data/generate.py --count 100 --output synthetic-data/generated_100.csv
```

Validate data:

```powershell
python validation/validate_dataset.py synthetic-data/generated_100.csv
```

## 5. Document Your Work

Every contribution should explain:

- What it does
- Who it is for
- How to run it
- What data it uses
- How it handles privacy and governance
- Known limitations
- Future work

## 6. Submit

Submissions can be:

- Code
- Documentation
- Governance resources
- Schemas
- Validation rules
- Translation files
- Research question sets
- Design prototypes

Use synthetic data or clearly marked fictional examples in all public
submissions.
