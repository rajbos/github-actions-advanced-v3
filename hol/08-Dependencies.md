# 🔨 Lab 8: Make the dependency inventory useful

**Time:** 20 minutes. **Prerequisite:** instructor-provided graph and submission snapshots for the sample repository. **PAID RUNNER / ADMIN REQUIRED:** graph/submission configuration may require repository administration and a trusted branch with limited write permissions. **EMU SETUP / GHE.COM SETUP:** use the approved organization and host; graph/feature availability can differ. **DEMO / FALLBACK:** use prepared snapshots if permissions or indexing are unavailable.

## Objectives

Distinguish pinned execution identity, dependency inventory, advisory metadata and the contents of a shipped artifact.

## Tasks

1. Inspect a pinned action dependency in the repository [dependency graph](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph). Record its source, SHA and any version/upstream information visible. What can be determined from the SHA alone?
2. Inspect `examples/workflows/08-dependencies.yml` and the instructor's trusted-branch submission run. Before any activation the instructor verifies exact token permissions, branch, pinned action revision, explicit inputs and snapshot ordering. Never grant a fork PR a broad write token. Compare the earlier and later snapshots and note unresolved mappings; index timing can delay the graph. [Submission API](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/use-dependency-submission-api), [submission action](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md)
3. Compare the prepared repository-graph SPDX export and an artifact-specific SBOM. List one item each may include or omit, and what evidence you would need to know their coverage. [Export a graph SBOM](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom)
4. Explain how an immutable execution SHA and version/upstream metadata solve different problems. An advisory example must be an inert fixture; do not execute a vulnerable action. Discuss configured upstream mappings and why unresolved SHAs or experimental Docker-reference detection remain gaps.

<details>
<summary>Hint</summary>

Inventory is a statement about what a detector knows, not a guarantee of all shipped bytes or all advisories.
</details>

<details>
<summary>Solution</summary>

The [submission checkpoint](../examples/workflows/08-dependencies.yml) uses `jessehouwing/actions-dependency-submission@v2.0.2`. Version tags alone are not immutable: generate/review the execution lockfile before activation. Version 2 reads and verifies `.github/workflows/actions.lock` when present; preflight `gh` and its lock extension, and investigate any warning that the lock was used without verification. Set `report-transitive-as-direct` explicitly: the v2.0.2 README and metadata still differ on the default. Review graph relationships, upstream mappings and unresolved entries, not just a successful submission. Graph snapshots represent repository dependencies; an artifact SBOM describes an identified built artifact and is only as complete as its generator and inputs. Neither alone proves absence of vulnerabilities.
</details>

## Success and cleanup

You can state the coverage and unknowns of both inventories. Keep prepared snapshots for the instructor; do not delete shared graph data. Cancel unneeded course runs and remove any temporary access only with the administrator. Next: [Lab 9](09-Promotion.md).
