# 🔨 Lab 3: Remove repeated setup

**Time:** 15 minutes. **PAID RUNNER / ADMIN REQUIRED:** consume only an instructor-provisioned custom hosted image and runner group; building it is not part of this lab. **GHEC REQUIRED:** verify the actual custom-image/runner eligibility separately; do not equate this with all GHEC accounts. **EMU SETUP / GHE.COM SETUP:** use the authorized group and actual host or the fallback. **DEMO / FALLBACK:** inspect comparable recorded baseline and image runs.

## Objectives

Identify setup avoided by prewarming and distinguish image contents from runtime caches and artifacts.

## Tasks

1. Compare the prepared baseline to the instructor's prebuilt-image run. Inspect `examples/workflows/03-prewarm.yml` as text; activate it only after the instructor confirms its runner label, policy and budget. Record image version, runner label, tool versions, setup/download timings and what still downloaded. [Custom hosted images](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images)
2. Identify the npm download cache, preinstalled tool cache, Docker image store, `ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE`, and build artifact. Explain which component owns each and whether it is shared with a job/service container or a different Docker daemon. Review [action archive cache implementation](https://github.com/actions/runner/blob/310a370bf3605f5b092f8af63b3126627de2a210/src/Runner.Worker/ActionManager.cs#L1232-L1305).
3. Propose who can build and use the image, its reviewed immutable inputs, patch/rebuild cadence, credential removal, version selection and rollback. Compare saved per-run setup against build/retention costs and staleness.

<details>
<summary>Hint</summary>

An image can seed several independent stores. A download disappearing from logs does not prove that every kind of cache was used.
</details>

<details>
<summary>Solution</summary>

Use the [prewarm example](../examples/workflows/03-prewarm.yml) and instructor evidence. Record actual observed savings, not a promised speedup. `cache-mode: none` disables the Actions dependency cache, not preinstalled tools, Docker stores or action-archive seeds. Archive cache is separate from `_work/_actions`; Docker-in-Docker or another daemon may not see host images.
</details>

## Success and cleanup

Your comparison names avoided and remaining work and an image-maintenance trade-off. Do not delete shared images or runner groups. Cancel course-only runs; the instructor deprovisions dedicated paid compute **and** image/storage/network resources at end of day. Next: [Lab 4](04-Events-and-parallelism.md).
