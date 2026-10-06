# GH-500 Practice Lab

> ⚠️ **This repo is deliberately vulnerable.** The Python and Node apps contain planted
> flaws and outdated dependencies so that GitHub Advanced Security has something to find.
> Never run or deploy them.

This is a hands-on sandbox for the **GitHub Advanced Security (GH-500)** exam. Because it is a
**public** repository, most GHAS features are free here. The exercises are in
[`labs/README.md`](labs/README.md).

## What's in here

| Path | What it's for |
|---|---|
| `app/app.py` | Flask app with SQLi, command injection, path traversal, XSS, unsafe deserialization, weak hashing, open redirect, debug mode |
| `app/requirements.txt` | Old Flask, Jinja2, Werkzeug, requests, PyYAML and urllib3 versions → Dependabot alerts |
| `web/server.js` + `web/package.json` | Express app with command injection, path traversal, XSS, `eval`, and vulnerable lodash/minimist |
| `.github/workflows/codeql.yml` | CodeQL **advanced setup**, a python + javascript matrix, `security-extended` |
| `.github/codeql/codeql-config.yml` | CodeQL config file (query suites, `paths-ignore`) |
| `.github/workflows/dependency-review.yml` | Blocks PRs that add vulnerable dependencies |
| `.github/workflows/upload-sarif.yml` + `sarif/` | Uploads a third-party SARIF file to code scanning |
| `.github/dependabot.yml` | Version updates for pip, npm and GitHub Actions, with grouping |
| `.github/secret_scanning.yml` | Excludes paths from secret scanning |
| `SECURITY.md` | Security policy, used with private vulnerability reporting |

## What's free on a public repo

| Feature | Public repo (free) | Notes |
|---|---|---|
| Dependency graph | ✅ | On by default for public repos |
| Dependabot alerts / security updates / version updates | ✅ | Free on every repo type |
| Dependabot auto-triage rules | ✅ | |
| Dependency review (action and PR diff) | ✅ | Private repos need GHAS / Code Security |
| Code scanning with CodeQL (default + advanced setup) | ✅ | |
| Third-party SARIF upload | ✅ | |
| Copilot Autofix for code scanning alerts | ✅ | |
| Secret scanning alerts (partner/provider patterns) | ✅ | |
| Push protection | ✅ | |
| Private vulnerability reporting and repository security advisories | ✅ | |
| Custom secret scanning patterns | ❌ | Needs an organization with Secret Protection |
| Non-provider patterns, validity checks, Copilot secret scanning | ❌ | Secret Protection license |
| Security overview, security campaigns | ❌ | Organization-level features |
| Delegated bypass and delegated alert dismissal | ❌ | Organization-level features |
| Security configurations applied at scale | ❌ | Organization-level. A free org with public repos lets you explore part of it |

For the exam, you need to know **which features need a license on private repos**: Secret
Protection (secret scanning, push protection, custom patterns) and Code Security (code
scanning, dependency review, Copilot Autofix). Dependabot and the dependency graph are always free.

## Setup after cloning

1. **Settings → Code security** (or "Advanced Security"): enable the dependency graph,
   Dependabot alerts, Dependabot security updates, secret scanning, push protection and
   private vulnerability reporting.
2. **Code scanning:** keep the provided `codeql.yml`, which is advanced setup. Don't also
   enable default setup, because the two conflict (see Lab 4).
3. Push to `main`, then open **Actions** and watch the CodeQL runs.
4. Open **Security** to see the alerts start to appear.
