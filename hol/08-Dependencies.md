# 🔨 Lab 8: Make the dependency inventory useful

**Time:** 20 minutes, plus graph indexing. **Prerequisite:** your participant repository, dependency graph enabled, and a trusted default branch. **ADMIN REQUIRED:** graph/submission configuration may require repository administration; only the trusted submission job receives `contents: write`. **EMU SETUP / GHE.COM SETUP:** use the approved organization and host; graph/feature availability can differ. **DEMO / FALLBACK:** use recorded snapshots if permissions or indexing are unavailable, and state what was not verified live.

## Objectives

Distinguish pinned execution identity, dependency inventory, advisory metadata and the contents of a shipped artifact.

## Tasks

1. In **your participant repository's Insights → Dependency graph**, inspect an action and its matching entry in `.github/workflows/actions.lock`. Record its source, SHA and visible version/upstream information. What can be determined from the SHA alone? Export the graph's SPDX SBOM as your **before** snapshot; record the time and commit. If the graph is empty, record that rather than substituting another repository. [Dependency graph](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph), [export a graph SBOM](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom)
2. Copy the `08-dependencies.yml` starter. Replace its incomplete step with the reviewed dependency-submission action from the version lookup, supplying the job token, explicit direct/transitive relationship handling and required lock verification. Determine the action's required write permission from its documentation and grant it only to `submit`; keep root permissions empty and the trusted-default-branch guard. Use the reviewed verifier version in the course lookup/lab solution if needed. Lock/review, commit/push and dispatch. Require a verified-lock log, not an unverified warning. Export an **after** snapshot, compare relationships and unresolved entries, and account for indexing delay/existing detectors; unchanged counts do not prove failure. Never broaden a fork token or remove another detector's snapshots. [Submission action inputs and permissions](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md), [submission API](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/use-dependency-submission-api)
3. Generate an inventory of this course app's staged npm components. From your repository's `app` directory, run `npm ci --ignore-scripts`, `npm run build`, then from `app/dist` run `npm sbom --sbom-format spdx --omit=dev` and save its JSON output **outside `dist`**. Compare it with the repository-graph SPDX export. Expect staged `picocolors` in both inventories, but workflow actions only in the repository graph. This npm inventory does not enumerate every source file or OS component. List one item each inventory may include or omit, and what evidence would establish its coverage. Do not commit generated output. [npm sbom](https://docs.npmjs.com/cli/v11/commands/npm-sbom)
4. Explain how an immutable execution SHA and version/upstream metadata solve different problems. An advisory example must be an inert fixture; do not execute a vulnerable action. Discuss configured upstream mappings and why unresolved SHAs or experimental Docker-reference detection remain gaps.

<details>
<summary>Hint</summary>

Inventory is a statement about what a detector knows, not a guarantee of all shipped bytes or all advisories.
</details>

<details>
<summary>Solution</summary>

The [completed submission reference](../solutions/workflows/08-dependencies.yml) uses `jessehouwing/actions-dependency-submission@v2.0.2`. Generate/review the lock before activation. Version 2 reads `.github/workflows/actions.lock`; explicit `actions-lock-version: v0.4.1` requires verification instead of a warning. The action installs that extension when needed; `gh` must be available. Grant `contents: write` only to `submit`; explicitly set `report-transitive-as-direct: 'false'` because README and metadata defaults differ. Review relationships and unresolved entries, not only success. Neither repository nor artifact inventory proves absence of vulnerabilities.
</details>

## Success and cleanup

You can state the coverage and unknowns of both inventories and cite your submission run. Retain the before/after and staged-component snapshots as evidence; do not delete shared graph data. Cancel unneeded course runs and disable **Lab 08 trusted dependency submission**; it is not used in Lab 9. Leave unrelated dependency-graph automation unchanged and remove temporary access only with its owner. Next: [Lab 9](09-Promotion.md).
