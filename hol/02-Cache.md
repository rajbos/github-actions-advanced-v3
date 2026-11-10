# 🔨 Lab 2: Cold, exact, partial, and read-only

**Time:** 25 minutes. **Prerequisite:** [Lab 1](01-Measure.md), trusted default-branch access and instructor-provided cache checkpoints. **DEMO / FALLBACK:** compare prepared logs if cache state, branch permissions or newer `cache-mode` syntax is unavailable.

## Objectives

Populate a package-download cache only from trusted main, restore it read-only from a PR, and distinguish miss, exact and partial results.

## Tasks

1. Inspect [cache matching and access restrictions](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) and [cache action outputs](https://github.com/actions/cache#outputs). Design a key with OS, architecture/toolchain or compatible cache schema, and lockfile hash. A less-specific restore prefix must preserve the intended compatibility boundary. Do not cache `node_modules` or secrets.
2. With instructor approval, copy only `02-cache-main.yml` and `02-cache-pr.yml` from `examples/workflows` to `.github/workflows`. Inspect event filters, explicit permissions, selected cache paths, version-tagged actions and their reviewed lockfile entries, and any setup-action implicit cache. The main writer must consume reviewed trusted revisions/dependencies; the PR must use only `actions/cache/restore` and `cache-mode: read`, with no implicit or explicit save. Commit reviewed files to the appropriate branch as directed.
3. Observe a cold trusted-main run with a fresh course-owned epoch, then another trusted run with the same key for an exact hit. To trigger that second run, use an instructor-approved harmless change under `app/` without changing the lockfile; an empty push or unrelated documentation edit does not match the path filters. Use the instructor's compatible lockfile-change checkpoint for a partial hit: its lockfile hash changes but its restore prefix does not. A different epoch with no matching prefix demonstrates a miss. Do not modify real dependencies simply to fabricate a partial hit. Record the actual restore key, `cache-hit` output, installation and setup duration. A matching cache may have expired or been evicted; use prepared logs if so.
4. Open a PR containing a harmless course change under `app/`. Inspect its run: confirm restore-only behavior and the continued `npm ci`. Verify no save step or hidden setup-action writer exists. Compare an unrelated docs-only PR: neither cache workflow should run. These optional examples must not be required checks; path-filtered required workflows can leave checks pending. If you rename an installed workflow, update its self-path filter. Inspect the release/deployment example as inert text and locate `cache-mode: none`.
5. Classify the event, workflow-definition ref, code consumed, cache scope and writer eligibility for `pull_request`, `pull_request_target`, `issues`, `workflow_run`, `workflow_dispatch`, and `repository_dispatch`. [Events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

| Checkpoint | Output | npm ci ran? | Evidence |
| --- | --- | --- | --- |
| Cold/miss | | | |
| Exact | | | |
| Partial | | | |
| PR restore only | | | |

<details>
<summary>Hint: a restore key is not a trust decision</summary>

Look at which event/ref writes the entry, not only the lockfile hash. A package-download cache is not an installed dependency tree.
</details>

<details>
<summary>Solution and trust boundary</summary>

See [trusted writer](../examples/workflows/02-cache-main.yml) and [PR restore](../examples/workflows/02-cache-pr.yml). `cache-hit` is the string `'true'` on an exact primary-key hit, `'false'` on a partial hit, and empty on a miss. Always run `npm ci`; it reconciles the checkout's lockfile even with a hit.

An ordinary PR normally uses a merge ref: it can restore base/default caches; any permitted save is PR-ref scoped and is not visible to main or other PRs. Course PRs never save. `pull_request_target`, issue events and `workflow_run` execute in a base/default context; current low-trust default-scope protection is read-only unless explicitly overridden. Never add write overrides or execute PR code/artifacts in a trusted cache writer. `workflow_dispatch` uses the selected ref; `repository_dispatch` uses the default branch and is write-eligible by default, but caller/input data is not thereby trusted. A default workflow file or cache key does not authenticate inputs. Protections vary by product/version.

An inert risk model is: attacker-influenced input → write-capable default-context writer → shared entry → privileged consumer. No live poisoning is needed.
</details>

## Success and cleanup

The table distinguishes three states and demonstrates read-only PR reuse. Cancel pending runs; close the course PR when no longer needed. Keep only instructor-approved caches for later comparison. At class end remove only identifiable course-owned cache keys, not shared entries; see [cleanup](10-Cleanup.md). Next: [Lab 3](03-Prewarm.md).
