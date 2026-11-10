# 🔨 Lab 4: Run only necessary work, within a budget

**Time:** 45 minutes across section 2. **Prerequisite:** [setup](00-Setup.md), permission to create/edit issues, and a disposable label in your participant repository (create `lab-04-events` if it does not exist). **DEMO / FALLBACK:** use prepared logs if issue permissions, runner capacity or native parallel syntax are unavailable. Use only a disposable training issue, with no confidential text. Perform every activity in your participant repository, not the course source repository.

## Objectives

Predict event activity selection, select checks using an impact map, and compare safe parallel execution with bounded failure.

## Opening demonstration: avoid unnecessary checkout

During the opening eight-minute teaching segment, first explain checkout as a lifecycle: workspace preparation/cleaning, repository/ref selection, Git trust/authentication, object/history fetching, file materialization, optional LFS/submodules and credential cleanup. It is not simply `git clone`. Then explain sparse checkout as a working tree containing only selected paths, not a different repository revision. Inspect the module's workflow-only zizmor example: `.github/workflows` selected with non-cone sparse patterns, `fetch-depth: 1`, `submodules: false`, and `lfs: false`. zizmor is preinstalled; job-scoped `contents: read` and reviewed action locking are preflight requirements. This is a teaching excerpt, not an additional workflow to install.

Compare full versus sparse checkout at the same revision and confirm identical intended scanner inputs before comparing checkout time or disk use. Include required scanner configuration and local action definitions when those are part of the scan; workflow-only coverage is not the full publication gate. No speedup is assumed without measurements. Discuss why diff-based detection may need additional history and why jobs that need submodules or LFS payloads must selectively fetch them. Depth 1, submodules off and LFS off are already checkout defaults. Use recorded evidence when a suitably large disposable repository is unavailable. [Checkout inputs and scenarios](https://github.com/actions/checkout), [zizmor collection](https://docs.zizmor.sh/usage/#input-collection)

Follow with the four-minute artifact comparison: prepare several files/archives and upload each with its own `archive: false` invocation, or use multiple upload steps to create distinct named bundles. The first accepts only one file per invocation; the filename becomes its artifact name. A dependent consumer downloads only required names/IDs or artifact-name matches, not members inside a ZIP. Show `skip-decompress: true` to keep a prepared ZIP intact and false (the default) to extract a detected ZIP; neither changes transfer scope. Required output must not disappear behind an overly narrow selection. This is a teaching comparison, not a change to Lab 9's signed release archive. [Artifact selection and direct files](https://github.com/actions/download-artifact#examples)

## Part A: Predict and observe events (20 minutes)

1. Inspect [issue events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues) and [issue-comment events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment). Copy only the two issue starters to `.github/workflows`. Both initially observe all issue activities: implement the second workflow's TODO so it selects only creation and edits, leaving the broad observer unchanged. Review/lock before pushing to the default branch. Keep `permissions: {}`, `cache-mode: none`, no checkout/API writes and only allowlisted event/activity reporting. Never insert issue text in scripts.
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

Completed references: [broad observer](../solutions/workflows/04-issues-all.yml) and [filtered observer](../solutions/workflows/04-issues-filtered.yml).
</details>

## Part A continued: Select checks (discussion)

4. Draw an impact map for lint, test and build using these fixture change lists: `hol/01-Measure.md` (docs-only), `app/src/server.js` (app code), `app/package-lock.json` or `app/package.json` (shared inputs), and `.github/workflows/04-parallel.yml` (workflow change). Also classify a failed file-list API request or a Git diff whose base revision is unavailable (detection failure). These are discussion fixtures, not additional files to edit. Include shared inputs and explain how a `merge_group` must compare the combined revision against its actual base. [Path filters](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore)
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

6. Copy the [`04-parallel.yml` starter](../examples/workflows/04-parallel.yml). Keep its sequential baseline. Implement the shared-runner TODO with concurrent lint/test steps joined before build; implement the separate-runner TODO with isolated lint/test jobs or a matrix and the existing dependent build. In each test branch implement the `fail-test` boolean fixture after real tests. Replace incomplete steps only with completed checks. Do not install dependencies concurrently into one workspace. Lock, commit/push and dispatch with the fixture off. Compare feedback time, summed runner time and setup overhead; the tiny app may not be faster. [Parallel syntax and synchronization](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
7. Dispatch again with `fail-test` checked: the workflow must fail and both dependent builds must skip. Copy the [timeout starter](../examples/workflows/04-timeout.yml), implement a two-minute stall with a one-minute step limit while preserving the three-minute job budget, then lock/push/dispatch it. Confirm the failure is a timeout, not the starter's incomplete-step error. Use recorded evidence when waiting is impractical; compare timeout, cancellation and matrix fail-fast. [Timeouts](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepstimeout-minutes)

   Here, a **stall** means a command that waits without doing useful work. Replace the starter's error-printing commands with a command that waits for two minutes. Add the step's `timeout-minutes` setting at the same YAML level as `run` and limit it to one minute; leave the job's three-minute setting unchanged. This demonstrates that a step can have a shorter limit than its job. After about one minute, GitHub Actions should stop the waiting step and report a timeout. An immediate `TODO` error means you are still running the incomplete starter, not the timeout experiment.
8. Complete a decision: native steps share the job runner; jobs provide isolation/independent capacity and permissions; a larger runner may improve CPU-bound work but costs more and does not guarantee improvement for serial/network-bound work. Set budgets from measured cold/warm runs with headroom.

<details>
<summary>Solution / checkpoints</summary>

Completed references: [parallel comparison](../solutions/workflows/04-parallel.yml) and [timeout](../solutions/workflows/04-timeout.yml). Parallel work must synchronize before consuming outputs and propagate failures; bound server readiness and teardown. Step timeout is inside the job budget. A failure, timeout or cancellation is not a successful required gate. The default job timeout is 360 minutes subject to runner limits; do not rely on it for a stalled check.
</details>

## Success and cleanup

Your table matches observed runs; the impact map handles shared changes and detection failure; one failure remains visible and the stall ends within its budget. Close the disposable issue; remove its label only if course-owned. Cancel active course runs and disable all four Lab 4 workflows: `Lab 04 all issue activities`, `Lab 04 selected issue activities`, `Lab 04 parallel checks`, and `Lab 04 bounded timeout`. None is needed in Lab 5. Do not touch shared workflows. Next: [Lab 5](05-Stacks-and-queue.md).
