# 🔨 Lab 4: Run only necessary work, within a budget

**Time:** 45 minutes across section 2. **Prerequisite:** instructor-prepared issue label and runs, and [setup](00-Setup.md). **DEMO / FALLBACK:** use prepared logs if issue permissions, runner capacity or native parallel syntax are unavailable. Use only a disposable training issue, with no confidential text.

## Objectives

Predict event activity selection, select checks using an impact map, and compare safe parallel execution with bounded failure.

## Opening demonstration: avoid unnecessary checkout

During the opening eight-minute teaching segment, first explain checkout as a lifecycle: workspace preparation/cleaning, repository/ref selection, Git trust/authentication, object/history fetching, file materialization, optional LFS/submodules and credential cleanup. It is not simply `git clone`. Then explain sparse checkout as a working tree containing only selected paths, not a different repository revision. Inspect the module's workflow-only zizmor example: `.github/workflows` selected with non-cone sparse patterns, `fetch-depth: 1`, `submodules: false`, and `lfs: false`. zizmor is preinstalled; job-scoped `contents: read` and reviewed action locking are preflight requirements. This is a teaching excerpt, not an additional workflow to install.

Compare full versus sparse checkout at the same revision and confirm identical intended scanner inputs before comparing checkout time or disk use. Include required scanner configuration and local action definitions when those are part of the scan; workflow-only coverage is not the full publication gate. No speedup is assumed without measurements. Discuss why diff-based detection may need additional history and why jobs that need submodules or LFS payloads must selectively fetch them. Depth 1, submodules off and LFS off are already checkout defaults. Use recorded evidence when a suitably large disposable repository is unavailable. [Checkout inputs and scenarios](https://github.com/actions/checkout), [zizmor collection](https://docs.zizmor.sh/usage/#input-collection)

Follow with the four-minute artifact comparison: prepare several files/archives and upload each with its own `archive: false` invocation, or use multiple upload steps to create distinct named bundles. The first accepts only one file per invocation; the filename becomes its artifact name. A dependent consumer downloads only required names/IDs or artifact-name matches, not members inside a ZIP. Show `skip-decompress: true` to keep a prepared ZIP intact and false (the default) to extract a detected ZIP; neither changes transfer scope. Required output must not disappear behind an overly narrow selection. This is a teaching comparison, not a change to Lab 9's signed release archive. [Artifact selection and direct files](https://github.com/actions/download-artifact#examples)

## Part A: Predict and observe events (20 minutes)

1. Inspect [issue events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues) and [issue-comment events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment). With instructor approval, copy only `04-issues-all.yml` and `04-issues-filtered.yml` from `examples/workflows` to `.github/workflows` on the default branch. Confirm both have `permissions: {}`, `cache-mode: none`, no checkout, no API writes, and report only allowlisted event/activity names. Do not insert issue text in scripts.
2. Before acting, predict which workflow runs for each activity. Create an issue, edit its title or body, apply the prepared label and add a comment. Compare each prediction to the Actions run list. Don't repeatedly edit while a run is pending.

| Activity | Broad issues prediction / observation | Filtered opened, edited prediction / observation |
| --- | --- | --- |
| Open | | |
| Edit | | |
| Label | | |
| Comment | | |

3. Transfer the reasoning to [PR events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request): list defaults, what a code push triggers, and why `edited` alone is not code CI. Discuss a base-branch change arriving as `edited`; use prepared payload evidence rather than executing issue/PR contents.

<details>
<summary>Solution: event table</summary>

Open and edit trigger both; label triggers only the broad `issues` workflow; comment triggers neither, because it uses `issue_comment`. Bare `issues` selects all supported issue activities, whereas bare `pull_request` defaults to `opened`, `synchronize`, `reopened`. Explicit `types` replaces that selection. If draft work is suppressed, include `ready_for_review` and keep later code pushes covered; base changes may require validation on `edited`.
</details>

## Part A continued: Select checks (discussion)

4. Examine the instructor's docs-only, app-code, shared-lockfile/configuration, workflow-change and detection-failure fixtures. Draw an impact map for lint, test and build. Include shared inputs and explain how a `merge_group` must compare the combined revision against its actual base. [Path filters](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore)
5. Explain why a path-filtered **workflow** may leave a required check pending and why a skipped **job** can appear successful. How does an always-run gate distinguish an explicitly unnecessary check from a detection error? [Required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)

<details>
<summary>Hint</summary>

Unknown is not the same as “no files changed”. Shared inputs can affect multiple components, even if a component's own source did not change.
</details>

<details>
<summary>Solution: impact model</summary>

Docs-only can skip checks only where the reviewed impact model explicitly says they are unnecessary. App source runs its affected lint/test/build; a shared lockfile, shared configuration or workflow change fans out to every affected check. Detection failure blocks the required aggregator or runs all relevant checks. Validate the merge-group combined revision, not the previous PR file list. Native diff limits vary by product/version; use the current documentation.
</details>

## Part B: Compare and bound work (25 minutes)

6. Inspect `04-parallel.yml` and the instructor's sequential, native parallel-step and separate-job runs. Copy that one example only after instructor preflight. Compare elapsed feedback time, sum of runner time, shared resources and failure propagation. Do not install dependencies concurrently into the same mutable checkout. [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
7. With the instructor's safe failure fixture, make one independent branch fail and verify the final result fails; observe the prepared intentionally stalled step with a one-minute step timeout and a larger job budget. The separate [timeout example](../examples/workflows/04-timeout.yml) is intentionally unsuccessful; copy it only if the instructor authorizes the bounded run. Use a recorded run if waiting is impractical. Compare the timeout with cancellation and fail-fast. [Job and step timeouts](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idtimeout-minutes)
8. Complete a decision: native steps share the job runner; jobs provide isolation/independent capacity and permissions; a larger runner may improve CPU-bound work but costs more and does not guarantee improvement for serial/network-bound work. Set budgets from measured cold/warm runs with headroom.

<details>
<summary>Solution / checkpoints</summary>

See [parallel example](../examples/workflows/04-parallel.yml) and prepared runs. Parallel work must synchronize before consuming outputs and propagate failures; bound server readiness and teardown. Step timeout is inside the job budget. A failure, timeout or cancellation is not a successful required gate. The default job timeout is 360 minutes subject to runner limits; do not rely on it for a stalled check.
</details>

## Success and cleanup

Your table matches observed runs; the impact map handles shared changes and detection failure; one failure remains visible and the stall ends within its budget. Close the disposable issue; remove its label only if course-owned. Cancel active course runs and disable the issue examples after the experiment to avoid future event-triggered usage; do not touch shared workflows. Next: [Lab 5](05-Stacks-and-queue.md).
