# GH-500 Labs

Work through these in order. Each lab ends with **Exam notes**: the facts that tend to
show up as questions.

---

## Lab 1: Turn on the features

1. Go to **Settings → Code security**. Turn on everything that's available and note what
   isn't available (and why: user account, not an org; public, not private).
2. Go to **Insights → Dependency graph** and browse the pip and npm dependencies.
3. **Insights → Dependency graph → Export SBOM** downloads an SPDX SBOM.

**Exam notes**
- The dependency graph is generated from manifests and lock files, or submitted through the
  dependency submission API (for example, for Gradle or Maven builds).
- The SBOM export format is **SPDX**.
- Who can see security alerts: admins and maintainers by default. Admins can grant
  read access to people or teams.

---

## Lab 2: Secret scanning and push protection

1. Make sure secret scanning and push protection are on.
2. Create a **fine-grained PAT** with **no permissions** and a 1-day expiry
   (**Settings → Developer settings**).
3. Add it to a new file `labs/leak.txt`, commit, and push. **Push protection blocks it.**
   Read the message, which shows the secret type, file and line, and the bypass URL.
4. Look at the bypass reasons: *It's used in tests*, *It's a false positive*,
   *I'll fix it later*. Choose one, bypass, and push again.
5. Go to **Security → Secret scanning** and look at the alert. The reason you chose
   decides whether an alert is opened.
6. **Revoke the PAT**, then close the alert as *Revoked*.
7. Commit a token under `labs/fixtures/`. It's excluded by `.github/secret_scanning.yml`,
   so nothing happens. Revoke that one too.

**Exam notes**
- Push protection also covers the web editor and the REST API, not just `git push`.
- Bypass reasons: *used in tests* and *false positive* close the alert straight away.
  *Fix later* leaves it open.
- `secret_scanning.yml` `paths-ignore` lives in `.github/` on the default branch.
- Partner program: in public repos, GitHub notifies the provider (for example AWS or
  Slack), which may revoke the token automatically.
- Custom patterns can be defined at repo, org and enterprise level. They need Secret Protection.
- Alert close reasons: *revoked*, *false positive*, *used in tests*, *won't fix*.

---

## Lab 3: Dependabot

1. After the first push, check **Security → Dependabot**. You should see alerts for
   PyYAML, urllib3, lodash, minimist and others.
2. Open an alert and look at the CVE/GHSA, the vulnerable range, the patched version and
   the **CVSS / EPSS** information.
3. Dependabot **security updates** open PRs automatically. Review one.
4. Comment `@dependabot rebase`, `@dependabot ignore this major version` and others
   on a Dependabot PR and see what each does.
5. **Auto-triage rules** (Security → Dependabot → the gear icon): create a rule that
   dismisses low-severity alerts for dev dependencies.
6. Edit `.github/dependabot.yml` and add `ignore:` for one dependency. Watch the effect.

**Exam notes**
- `dependabot.yml` = **version** updates. Security updates are switched on in Settings and
  need no config file, but they do respect `dependabot.yml` options.
- Alerts need the dependency graph. Security updates need alerts.
- Dependabot PRs run Actions with a **read-only `GITHUB_TOKEN` and no secrets** (except
  Dependabot secrets).
- Dismiss reasons: *fix started*, *no bandwidth*, *tolerable risk*, *inaccurate*, *not used*.

---

## Lab 4: Code scanning with CodeQL

1. Push and watch `CodeQL` run as two jobs (python and javascript-typescript).
2. **Security → Code scanning:** match each alert to the `CWE-xxx` comment in the code.
3. Open an alert and look at the **data flow path** (source → sink).
4. Try **Copilot Autofix** on one alert and see what PR it suggests.
5. Dismiss one alert as *False positive*, one as *Won't fix* and one as *Used in tests*.
6. In `codeql-config.yml`, switch `security-extended` to `default`, re-run, and
   compare the alert counts. Then try `security-and-quality`.
7. **Default vs advanced:** enable default setup in Settings and see what GitHub says
   about the existing workflow. Turn it off again.
8. Run **Actions → Upload third-party SARIF** and filter the code scanning list by
   tool = `FakeScanner`.

**Exam notes**
- Workflow permission `security-events: write` is required to upload results.
- Query suites: `default` < `security-extended` < `security-and-quality`.
- Build modes: `none` (interpreted, plus Java/C# without a build), `autobuild`, `manual`.
- `category` separates multiple analyses of the same commit (matrix, monorepo, third-party).
- CodeQL CLI flow: `codeql database create` → `codeql database analyze` →
  `codeql github upload-results`.
- Severities: alert **severity** (error/warning/note) vs **security severity**
  (critical/high/medium/low, from CVSS).

---

## Lab 5: Pull request workflow

1. Create a branch, then add `"axios": "0.21.0"` to `web/package.json` and a new SQL
   injection to `app/app.py`.
2. Open a PR to `main`.
3. **Dependency review** fails the PR because of the vulnerable axios version, and
   **CodeQL** annotates the new SQLi inline.
4. In **Settings → Rules → Rulesets**, create a branch ruleset for `main` with
   *Require code scanning results* (CodeQL, high or higher) and required status checks.
5. Try to merge.

**Exam notes**
- Code scanning on PRs only shows alerts **introduced by the PR**.
- Code scanning merge protection is configured through **rulesets**.
- Dependency review compares the base and head dependency graphs.

---

## Lab 6: Advisories and reporting

1. **Security → Advisories → New draft security advisory.** Fill it in, request a CVE
   (just look at the option, don't submit), and create a temporary private fork.
2. From a second account or a browser in incognito mode, open **Report a vulnerability**
   to see the private vulnerability reporting flow.

**Exam notes**
- Repository security advisories: draft → private collaboration (temporary private fork)
  → publish → optional CVE from GitHub (GitHub is a CNA).
- Published advisories go into the **GitHub Advisory Database** after review.
