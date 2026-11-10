# 🔨 Lab 2: Cache a large, versioned tool download

**Time:** 25 minutes, plus transfers. **Prerequisite:** [Lab 1](01-Measure.md), trusted default-branch access in your participant repository, and hosted Linux x64 capacity with Node 24, GNU tar and zstd. The helper is supplied; implementing cache restore/save is your work. **DEMO / FALLBACK:** use labeled recorded evidence if download access, cache quotas, runner time or `cache-mode` support is unavailable. Do not download the bundle to every learner workstation.

## Objectives

Cache a substantial download without a setup action's built-in caching. Populate only from reviewed main, restore read-only from PRs, and distinguish miss, exact and compatible partial reuse while verifying the requested bytes on every path.

## What you are caching

The [CodeQL bundle v2.27.4 release](https://github.com/github/codeql-action/releases/tag/codeql-bundle-v2.27.4) supplies `codeql-bundle-linux64.tar.zst`: **559,484,083 bytes (about 559 MB / 534 MiB)**, with published SHA-256. This is a CLI/query bundle, not a single query pack. We download it directly, not through `codeql-action/init` or another caching installer. No CodeQL database, scan, upload, license purchase or security permission setup is part of this lab.

[`examples/codeql-bundle.json`](../examples/codeql-bundle.json) records the reviewed release, platform-specific asset, byte size, checksum and a descriptive `note`. It is not `actions.lock`: that separate lock controls workflow action execution. The supplied [`tools/prepare-codeql.mjs`](../tools/prepare-codeql.mjs) downloads a missing versioned archive into `.cache/codeql-downloads`, verifies size and SHA-256 on every run, and exposes the verified path. Corrupt cached bytes fail explicitly rather than silently redownload. Extraction and `codeql version` run from a fresh job-temporary directory, never a preinstalled CodeQL found on PATH. The helper does not implement Actions caching.

## Tasks

1. Inspect [cache matching/access restrictions](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [cache usage and outputs](https://github.com/actions/cache#usage), and the manifest/helper. Design a key containing OS, architecture, tool identity, a participant-owned cache epoch and the manifest hash. Design a restore prefix that stays within that platform/tool/schema boundary. Cache **only** `.cache/codeql-downloads`, not the extracted CLI, workspace, credentials or analysis databases. [Release assets and checksums](https://github.com/github/codeql-action/releases/tag/codeql-bundle-v2.27.4)
2. Copy the two `02-cache-*.yml` starters into `.github/workflows`. Implement restore before the supplied preparation step in both. Add save only in the trusted main job, after verification/extraction/smoke test succeeds and only on a non-exact hit. Implement PR lookup reporting without any save. Replace the incomplete-step failures only once that logic exists. Keep the helper and extraction on **all** cache-hit paths; cache success is not integrity evidence. Preserve empty root permissions, job-only `contents: read`, main-only writer and PR `cache-mode: read`. Node is just the helper runtime; leave setup-node's package caching disabled. Generate/review `actions.lock` after adding actions.
3. Use the same fresh course-owned epoch in both keys/prefixes, such as `lab-yourhandle-20261110-a`. Commit/push the reviewed implementations and unchanged manifest to trusted main for a **cold miss**. Wait and record the actual lookup result, bundle download/verification, extraction and smoke test. The first run also saves roughly 559 MB; coordinate cache capacity/runner budgets with the instructor.
4. For an **exact hit**, add a harmless comment to `tools/prepare-codeql.mjs`, then commit/push without changing the manifest or cache epoch. This helper path is included in the trigger; an empty push or unrelated app/docs change is not. Expect cache transfer plus checksum verification/extraction, but no upstream bundle download. Report actual results if eviction or a failed save prevents reuse.
5. For a **compatible partial hit**, change only the manifest's `note`, commit/push and wait. Its file hash changes but the requested version, asset, size and digest stay identical. Expect a prefix restore, local bundle reuse and a new exact-key save. This note-only change is a controlled teaching fixture, not a production reason to invalidate downloads. For a new **miss**, change the epoch consistently in primary keys and prefixes in both workflows. Do not broaden the prefix, alter the checksum or upgrade the real bundle just to manufacture a hit.
6. Open a PR changing only the manifest's `note` again. Confirm PR restore-only reuse and no cache save, including no setup-action cache writer. Inspect a docs-only change separately: these optional workflows must not run or be configured as required checks. Keep release/deployment examples cache-disabled. If a workflow is renamed, update its self-path filter. Real bundle upgrades require reviewing release metadata/checksum together and downloading the newly requested version; an older restored bundle cannot substitute for it.
7. Explain branch scope and trust for `pull_request`, `pull_request_target`, `issues`, `workflow_run`, `workflow_dispatch` and `repository_dispatch`. [Events and refs](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) A different branch can restore default-branch caches but cannot overwrite them with its branch-scoped save; changing branches alone does not guarantee a miss. Never remove the writer's main guard or add unsafe write overrides to experiment.

| Checkpoint | cache-hit / matched key | Upstream download? | Verify / extract / version passed? | Restore / download / verify / extract / save time |
| --- | --- | --- | --- | --- |
| Cold/miss | | | | |
| Exact | | | | |
| Compatible partial | | | | |
| New epoch/miss | | | | |
| PR restore only | | | | |

A restored cache still transfers hundreds of megabytes. Compare restore/save transfer time, upstream download time, verification, extraction, queue time and total job time separately. An already compressed archive may compress little further. Avoided upstream downloads do not guarantee lower latency or cost.

<details>
<summary>Hint: match identity, then verify contents</summary>

The manifest hash belongs in the primary key, not the broad restore prefix. The helper's versioned local filename lets a prefix restore contain old versions without selecting them by accident. Always invoke it; it verifies the requested archive even after an exact hit. `setup-node` has npm caching, but that is unrelated to this directly downloaded CodeQL bundle.
</details>

<details>
<summary>Solution and trust boundary</summary>

Completed references: [trusted writer](../solutions/workflows/02-cache-main.yml) and [PR restore](../solutions/workflows/02-cache-pr.yml). They use OS/architecture + `codeql` + epoch + `hashFiles('examples/codeql-bundle.json')`, and cache only `.cache/codeql-downloads`. `cache-hit` is `'true'` on an exact hit, `'false'` on a partial hit and empty on a miss. Save uses the primary key only after a successful verified smoke test, when the lookup was not exact. The PR contains no save.

The helper constructs a fixed GitHub release URL from validated manifest values. It checks size and SHA-256 before publishing a downloaded archive or returning a cached one; it never trusts the key as authentication. Workflows then extract outside the cache and invoke that specific CLI. The digest is reviewed course input, not a value accepted from the restored cache itself. A reviewed checksum is not a vulnerability assessment.

Ordinary PR cache saves, when permitted by the platform, are merge-ref scoped and cannot replace main's cache. This course forbids PR saves entirely. Low-trust base/default-context events have separate platform safeguards; do not override them or execute untrusted PR artifacts in a privileged writer. A default-branch workflow file does not make all consumed data trusted. Teach the poisoning chain as an inert diagram, never a live exploit.
</details>

## Success and cleanup

Your table distinguishes cache lookup from verified local reuse and records avoided upstream transfers without inventing a speedup. Close course PRs, cancel unneeded runs and disable **Lab 02 trusted cache writer** and **Lab 02 PR restore only**. Neither is used in Lab 3. Keep **Lab 01 baseline** for the image comparison. Agree which exact participant-owned cache keys to retain temporarily; multiple epochs consume substantial storage. At class end remove only those recorded course caches, not shared entries. Do not commit downloaded bundles or extracted tools; the cache directory is ignored. Continue with [Lab 3](03-Prewarm.md) and follow [end-of-class cleanup](10-Cleanup.md).
