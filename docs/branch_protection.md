# Branch Protection

Contributors should not push directly to `main`. They should work on branches
and submit pull requests for review.

This cannot be fully enforced by a GitHub Actions workflow alone. Enforcement
must be enabled in the repository settings using branch protection rules or a
repository ruleset.

## Recommended Settings

For `main`, enable:

- Require a pull request before merging
- Require at least 1 approval
- Dismiss stale approvals when new commits are pushed
- Require review from Code Owners, if maintainers use `CODEOWNERS`
- Require status checks to pass before merging
- Require the `Validate starter repo` status check from `.github/workflows/ci.yml`
- Require branches to be up to date before merging
- Block force pushes
- Block deletions
- Restrict who can push directly to `main`, if available on the repository plan

## Contributor Flow

```powershell
git checkout -b contributor/short-description
# make changes
git add .
git commit -m "Describe contribution"
git push origin contributor/short-description
```

Then open a pull request into `main`.

## Maintainer Note

If the GitHub CLI is authenticated with admin access, maintainers may configure
branch protection through GitHub settings or API. Otherwise, use the web UI:

1. Open the repository on GitHub.
2. Go to Settings.
3. Open Branches or Rulesets.
4. Add protection for `main`.
5. Require pull requests and the CI check before merge.
