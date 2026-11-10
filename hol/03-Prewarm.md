# 🔨 Lab 3: Remove repeated setup

**Time:** 15 minutes, plus image-generation time. **CUSTOM IMAGE / PAID RUNNER / ADMIN REQUIRED:** each participant builds a uniquely named custom image and uses a separate runner. **GHEC REQUIRED:** verify actual custom-image and larger-runner eligibility; do not assume every GHEC account qualifies. Do not purchase a plan or create paid capacity just for this lab. If you cannot create images and runners, use the instructor's comparable run evidence and complete the workflow-editing and analysis tasks.

> **Start now, check back later.** Image generation and replication can take several hours; a successful builder run does not mean the image is available. After launching it, record the run URL and image name/version, then continue with Lab 4 rather than waiting here. Check its status at a later break and again before end-of-class cleanup. Resume at setup step 5 only when the seeded version is **Ready**. If it is still unavailable, use recorded instructor evidence for the comparison and record your own result as pending; do not launch duplicate builds just to retry the wait. Agree with the owner on cleanup or an explicitly approved later comparison, since retained images can incur storage charges.

## Objectives

Change the custom-image snapshot configuration, pre-pull a Docker image, and distinguish image contents from runtime caches and artifacts.

## Setup when you have the required permissions

Custom image generation requires an authorized organization or enterprise, eligible plan/region, administrator permissions, and an approved budget. Follow GitHub's [custom image setup](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images) and current [larger-runner billing guidance](https://docs.github.com/en/actions/concepts/runners/larger-runners#billing). Use the instructor-provided restricted runner group if available; otherwise do not change organization policy or create paid capacity just for this exercise.

1. Confirm that custom images are enabled for the organization or enterprise, and that you are an owner, CI/CD Admin, or have the required custom-image and runner-group permissions. Confirm supported platform/region, runner-group policy, billing owner, and image-storage retention before creating resources.
2. Create a larger runner for image generation on Linux x64, enable **Enable this runner to generate custom images**, and put it in a dedicated runner group restricted to this repository. Do not grant public repositories access to an image-generation runner.
3. Copy the [`03-build-prewarm.yml` starter](../examples/workflows/03-build-prewarm.yml) to `.github/workflows/03-build-prewarm.yml`. Customize `runs-on` and `snapshot.image-name` for your repository and keep `version: 1.*`. Implement the Docker TODO: pre-pull `node:latest` and log its image identity before snapshotting. The npm seed is supplied scaffolding. For the stretch, implement the separate `seed-action` TODO before selecting that input; see task 3 for requirements. Replace incomplete-step failures only with their implementations. Generate/review `actions.lock`. Do not put credentials or secrets in a snapshot. [Docker pull](https://docs.docker.com/reference/cli/docker/image/pull/)
4. Dispatch the builder on `main`. It installs Node.js 24, seeds the `picocolors` npm download cache, and pulls `node:latest`. Record the run URL, custom image name, platform and version from the custom-images page, plus the Docker image digest printed by the workflow. **Pause this lab and continue with Lab 4 while image generation runs.** Return to step 5 at a later break when the version is Ready; do not spend the lab slot waiting.
5. Create a separate larger runner from your image, on the same platform and with sufficient storage. Select the **exact Ready version containing your seeds**, not an older version; for this comparison prefer an explicit version over `latest`. Restrict its runner group to this repository. Wait for runner configuration to become Ready too. Set repository Actions variable `LAB_PREWARM_RUNNER` to that consumer runner's label, copy `03-prewarm.yml` to `.github/workflows/03-prewarm.yml`, update its lockfile with `gh actions-lock`, then dispatch it on `main`. In **Set up job → VM Image**, verify the actual version before accepting results. If the run still reports the older version, retain the failure evidence and allow configuration propagation; do not pull missing dependencies in the consumer to make the experiment appear successful.
6. If any policy, permission, budget, or runner prerequisite is missing, do not bypass the restriction. Use instructor run evidence and complete the analysis tasks instead.

## Tasks

1. Compare your baseline run with your custom-image run. Record runner and image versions, Node/npm versions, whether `picocolors` and `node:latest` were already present, what still downloaded, and the relevant setup timings. Do not claim a speedup unless the logs support it.
2. Explain the difference between the npm download cache, tool cache, Docker image store, Actions dependency cache, action archive cache, and build artifacts. Identify whether the job or service container uses the same Docker daemon as the host.
3. **Stretch goal:** implement the builder's archive-cache TODO using [`gh actions-archive-cache` v0.0.2](https://github.com/jessehouwing/gh-actions-archive-cache/blob/v0.0.2/README.md): install the pinned extension, download the supplied reviewed `ACTION_SHA` to the existing runner cache as `tar.gz`, then uninstall on success or failure before snapshotting. Use a step-only token; never persist authentication. The supplied token example is for github.com, not a GHE.com tenant token. Preserve download/uninstall failures. Add the reviewed `tj-actions/changed-files@v47.0.6` action to the consumer, inspect its output via a quoted environment variable, and review the generated lock entry against the seed SHA. Attempt this before opening the solution. For proof, use debug logs showing `Copied action archive` for the seeded exact SHA; `Download action repository` appears even on hits. The runner still resolves refs through GitHub. See [runner lookup](https://github.com/actions/runner/blob/310a370bf3605f5b092f8af63b3126627de2a210/src/Runner.Worker/ActionManager.cs#L1232-L1305) and [extension image guidance](https://github.com/jessehouwing/gh-actions-archive-cache/blob/v0.0.2/docs/custom-runner-images.md).
4. Propose who can build and use the image, how inputs are reviewed and pinned, patch/rebuild cadence, credential removal, version selection, and rollback. Compare saved per-run setup against build/retention costs and staleness.

<details>
<summary>Hint</summary>

The image can seed several independent stores. A download disappearing from logs does not prove every kind of cache was used. `node:latest` is mutable; production images should use a reviewed immutable digest and have an update plan.
</details>

<details>
<summary>Solution</summary>

Completed references: [builder](../solutions/workflows/03-build-prewarm.yml) and [consumer](../solutions/workflows/03-prewarm.yml). Change the runner label and `snapshot.image-name` for your own image. The Docker step is `docker pull node:latest`; the consumer verifies it with `docker image inspect` and `docker run --pull=never --rm node:latest node --version`. Docker documents [`docker image pull`](https://docs.docker.com/reference/cli/docker/image/pull/).

For the stretch goal, the action archive cache is separate from `_work/_actions` and the Actions dependency cache. GitHub's Ubuntu images use `/opt/actionarchivecache` and persist `ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE` in `/etc/environment`; see the [runner-images setup script](https://github.com/actions/runner-images/blob/d9a55a1954ef976392dce427271026deee8f1302/images/ubuntu/scripts/build/install-actions-cache.sh). The first-party [action-versions tooling](https://github.com/actions/action-versions/blob/e3c62146623237ce0e50fbb68f09fc0c4739446a/README.md) builds the per-action archive layout. Review the [changed-files action](https://github.com/tj-actions/changed-files) and pin it to the same full commit SHA used by the consumer workflow. `cache-mode: none` disables the Actions dependency cache; it does not disable preinstalled tools, Docker images, or action archive lookup. A job/service container or a different Docker daemon may not see host Docker images.

### Solution: builder snapshot fields and Docker seed

Change the builder workflow's `runs-on` label and snapshot fields for your own runner and image:

```yaml
runs-on: your-image-generation-runner-label
snapshot:
  image-name: actions-advanced-lab3-your-github-handle
  version: 1.*
```

Keep the Node/npm seed and add this step to the builder job:

```yaml
- name: Pre-pull a Docker image
  run: |
    docker pull node:latest
    docker image inspect node:latest --format '{{.Id}}'
```

The consumer workflow verifies the image with:

```yaml
- name: Verify the pre-pulled Docker image
  run: |
    docker image inspect node:latest --format '{{.Id}}'
    docker run --pull=never --rm node:latest node --version
```

### Stretch solution: seed the changed-files action archive

Implement this builder step before the `snapshot` job finishes, then select `seed-action` when dispatching. Only the completed reference implements it already. GitHub CLI must already be installed; the released extension binary needs no Go toolchain. GitHub's Ubuntu base image already configures the cache directory and runner environment. Preserve that configuration and ensure the trusted builder can write there; do not make a shared cache world-writable. Add just the reviewed exact commit, rather than every version or a moving latest tag.

Keep workflow-level `permissions: {}` and add job-level `permissions: { contents: read }`, as in the supplied builder. Pass the built-in token only through the step environment; do not run `gh auth login`, persist credentials or print tokens. This example explicitly targets public actions on `github.com`; a tenant-hosted job token must not be sent there. For GHE.com, follow the extension's [host-specific authentication guidance](https://github.com/jessehouwing/gh-actions-archive-cache/blob/v0.0.2/README.md#authentication-and-environment-tokens) and use separately authorized credentials or labeled instructor evidence.

```yaml
- name: Seed the changed-files action archive
  shell: bash
  env:
    GH_TOKEN: ${{ github.token }}
    ACTION_SHA: 9426d40962ed5378910ee2e21d5f8c6fcbf2dd96
  run: |
    cache="${ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE:?The base image must configure the action archive cache}"
    gh extension install jessehouwing/gh-actions-archive-cache --pin v0.0.2
    trap 'status=$?; gh extension remove actions-archive-cache || exit 1; exit "$status"' EXIT
    gh actions-archive-cache download "tj-actions/changed-files@$ACTION_SHA" \
      --hostname github.com --cache-dir "$cache" --format tar.gz
```

The exit trap uninstalls the extension on success or download failure; uninstalling it leaves the downloaded archives intact for the snapshot. It preserves download failures and fails the step if uninstall fails. Start with a builder that does not already have this extension installed; do not remove someone else's installation. Hard job cancellation can prevent traps, so do not publish an image from a failed/cancelled build. Inspect the download and uninstall messages before accepting the snapshot. The consumer does not need the extension installed.

For a larger reviewed workflow set, the extension also supports `gh actions-archive-cache from-lockfile .github/workflows/actions.lock --hostname github.com --cache-dir "$cache" --format tar.gz`. This requires checking out the reviewed lockfile in the builder first; importing is not independent verification of that lockfile. Keep the same install/download/uninstall lifecycle. Windows images use `--format zip`; this lab's Linux image uses `tar.gz`. Downloads in a consumer step are too late to accelerate that same job's action preparation.

The consumer workflow must request the same exact commit that is present in the archive. Use the readable release tag below, generate the installed workflow's lockfile with `gh actions-lock`, and verify that its changed-files entry resolves to `9426d40962ed5378910ee2e21d5f8c6fcbf2dd96` before dispatch. The archive is keyed by that resolved commit, not the tag:

```yaml
- uses: actions/checkout@v7.0.1
  with:
    fetch-depth: 0
- uses: tj-actions/changed-files@v47.0.6
  id: changed-files
  with:
    since_last_remote_commit: true
- name: Show changed files
  env:
    CHANGED_FILES: ${{ steps.changed-files.outputs.all_changed_files }}
  run: |
    printf 'Changed files: %s\n' "$CHANGED_FILES"
```

Rebuild the snapshot, wait for the new version to be ready, and select that version on the consumer runner before dispatching the consumer again. Check action-download logs to verify a cache hit; merely setting the variable or copying files is not proof. For a minimal base image without this environment variable, follow the linked Ubuntu setup script to configure the persistent runner environment before action preparation; setting `GITHUB_ENV` in a consumer step is too late.
</details>

## Success and cleanup

Your comparison names avoided and remaining work and an image-maintenance trade-off. After image generation and comparison finish, disable `Lab 03 build prewarmed image`, `Lab 03 consume prewarmed image`, and the retained `Lab 01 baseline`; none is used in Lab 4. Do not delete shared images or runner groups. Cancel course-only runs; the instructor deprovisions dedicated paid compute **and** image/storage/network resources at end of day, and verifies that image versions and storage are handled under the organization's retention policy. Next: [Lab 4](04-Events-and-parallelism.md).
