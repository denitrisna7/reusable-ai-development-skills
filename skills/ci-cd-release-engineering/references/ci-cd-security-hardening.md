# CI/CD Pipeline Security & Hardening Reference

> Primary Source:
> - **GitHub Actions Documentation**: https://docs.github.com/en/actions
> - **GitHub Actions Security Guides**: https://docs.github.com/en/actions/security-for-github-actions/security-guides

This reference details mandatory security hardening controls for CI/CD workflows. While examples use GitHub Actions syntax, the underlying security principles apply across GitLab CI, Jenkins, CircleCI, Azure Pipelines, and Bitbucket Pipelines.

---

## 1. Least-Privilege Token Permissions (`GITHUB_TOKEN` / CI Job Tokens)

Never rely on permissive default repository tokens. Explicitly declare top-level `permissions: read-all` or `permissions: { contents: read }` and elevate permissions only at the specific job level that requires write or OIDC access.

```yaml
permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

  release:
    needs: verify
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write # Required for keyless OIDC cloud authentication
```

- **Keyless OIDC Over Long-Lived Cloud Keys**: Prefer OpenID Connect (OIDC) federation with AWS IAM, Google Cloud Workload Identity Federation, or Azure AD over storing static long-lived cloud access keys in CI secrets.

---

## 2. Third-Party Action & Runner Supply Chain Pinning

Mutable version tags (`@v3`, `@main`) can be hijacked if an upstream action maintainer account is compromised.
- **Full Commit SHA Pinning**: Pin third-party actions to a full 40-character commit SHA accompanied by a human-readable version comment:
  - Good: `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2`
  - Bad: `uses: actions/checkout@main`
- **Container Image Digest Pinning**: In GitLab CI, CircleCI, or containerized jobs, pin base images to immutable SHA256 digests (`node:22-alpine@sha256:...`) or locked internal registry tags.
- **Self-Hosted Runner Isolation**: Never run untrusted public fork pull requests on persistent self-hosted runners with access to internal networks or cloud metadata endpoints (`169.254.169.254`). Use ephemeral, single-use VM/container runners.

---

## 3. Preventing Untrusted Script Injection in Workflows

Interpolating untrusted event context fields directly inside a `run:` shell script allows attackers to execute arbitrary shell commands via crafted PR titles, branch names, or commit messages.

- **Vulnerable Pattern (Never Do This)**:
  ```yaml
  - name: Unsafe PR title check
    run: echo "Checking PR: ${{ github.event.pull_request.title }}"
  ```
- **Remediation Pattern (Pass via Environment Variable)**:
  ```yaml
  - name: Safe PR title check
    env:
      PR_TITLE: ${{ github.event.pull_request.title }}
    run: |
      printf 'Checking PR: %s\n' "$PR_TITLE"
  ```
- **Dangerous Event Contexts**: Always treat `github.event.issue.title`, `github.event.issue.body`, `github.event.pull_request.title`, `github.event.pull_request.body`, `github.event.comment.body`, `github.event.commits[*].message`, and `github.head_ref` as untrusted user input.
- **Avoid `pull_request_target` Executing Untrusted Code**: Never checkout and execute PR head code (`ref: ${{ github.event.pull_request.head.sha }}`) inside a `pull_request_target` workflow, as it runs with write permissions and access to repository secrets.

---

## 4. Concurrency Controls & Protected Environments

1. **PR / Feature Branch Concurrency**: Cancel redundant intermediate runs on feature branches to save runner capacity while never canceling in-flight production deployments:
   ```yaml
   # For CI check workflows on PRs:
   concurrency:
     group: ci-${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true

   # For Production Release workflows (serialize, NEVER cancel in-progress):
   concurrency:
     group: deploy-production
     cancel-in-progress: false
   ```
2. **Protected Deployment Environments**:
   - Configure `environment: production` (or `resource_group: production` in GitLab CI) with required human reviewers, branch restrictions (`main` or signed release tags only), and environment-scoped secrets.
3. **Artifact Integrity & Provenance**:
   - Build the deployable artifact (Docker image, binary, or immutable bundle) **once** during the build stage, sign or record its SHA256 digest, and promote that exact artifact through staging and production rather than rebuilding from source at deploy time.
