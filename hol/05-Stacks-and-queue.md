# 🔨 Lab 5: A small stack and fewer obsolete runs

**Time:** 25 minutes, plus repository policy setup. **Prerequisite:** your participant repository and permission to push branches and open PRs. **ADMIN REQUIRED:** you must configure merge queue policy for your own participant repository before the queue experiment; it is not assumed to be preconfigured by the instructor. Eligibility depends on organization ownership, visibility and plan. Without the required permissions or feature availability, complete the stack and cancellation tasks and explicitly report the queue portion as unverified, or use instructor-recorded queue evidence. Do not silently substitute an ordinary PR merge for a queue run. **EMU SETUP / GHE.COM SETUP:** use the approved organization and actual host.

## Objectives

Distinguish per-layer validation from combined-revision integration validation and identify genuinely avoided runs.

## Tasks

1. Copy the [`05-stack-queue.yml` starter](../examples/workflows/05-stack-queue.yml). Preserve the mandatory `validate` job, PR/queue events and bounded-delay fixture. Implement its TODOs: concurrency that cancels older runs only for the same PR without cancelling queue runs or another PR, and a non-required `optional-top-layer` report only for the last PR in native stack metadata. Keep validation on every PR and combined queue revision. Review the actual target branch and permissions, generate/review the lockfile, then commit/push to your default branch. [Stack CI](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests), [concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
2. In your participant repository, create branch `lab-05-first` from `main`, add `"check": "npm run lint && npm test"` to `app/package.json` scripts, and open the **first PR** targeting `main`. Create branch `lab-05-second` from `lab-05-first`, change the validation step in `.github/workflows/05-stack-queue.yml` from `npm test` to `npm run check`, and open the **second PR** targeting `lab-05-first`. The second PR depends on the first: `main ← first PR ← second PR`. Use **Create stack** or the recommendation banner to register a native stack; dependent bases alone do not register it. Inspect each PR's focused diff and native stack metadata. GitHub calls the first PR the bottom of this stack and the second PR the top; these instructions use first and second. [Creating stacks](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests)
3. Set repository Actions variable `LAB_STACK_DELAY_SECONDS` to `30` (the workflow permits only 0-60 seconds). Push a harmless workflow-comment update to `lab-05-second`, wait until its validation job starts the bounded sleep, then push another harmless comment update to `lab-05-second`. Identify which obsolete second-PR run is cancelled and check that the first PR's run is not cancelled. Remove the variable or set it to `0` afterward. Count actual cancelled/skipped jobs; do not infer savings just because the stack has fewer PRs. [Workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency)
4. Configure merge queue policy in **your participant repository** before queueing the stack, using the setup below. Queueing can automatically merge the disposable changes once required checks pass. Locate the `merge_group` `checks_requested` run, its combined tested commit and base. Explain why successful layer runs do not establish that the combination passed.

### Set up your repository's merge queue policy

Follow GitHub's [merge queue configuration guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) and [branch protection setup](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule#creating-a-branch-protection-rule).

1. Verify the browser is showing **your participant repository**, confirm eligibility and administrator access, and record any existing rules before changing policy. Do not edit organization-wide or shared course rules.
2. Confirm the installed Lab 5 workflow includes both `pull_request` and `merge_group: types: [checks_requested]`, and let its `validate` check complete on a PR so the check can be selected in repository settings.
3. In **Settings → Branches**, create or edit a branch protection rule targeting the exact base branch `main` (or your actual stack base). Do not use a wildcard branch pattern for merge queue. Require pull requests and successful status checks; select the Lab 5 `validate` check using its actual displayed name and GitHub Actions source. Do **not** require `optional-top-layer`, which intentionally skips some revisions.
4. Enable **Require merge queue**, choose an allowed merge method, and review its settings. For this disposable experiment, use build concurrency `1`, require non-failing PRs, and keep minimum/maximum PRs per merge at `1`. Choose a status-check timeout above the workflow's ten-minute job budget, with queue headroom. Merge limits control merges, not whether CI builds are batched.
5. Save the rule and confirm it is effective for your stack's base branch. If a repository ruleset already controls the branch, use its equivalent merge-queue and required-check rules instead of adding contradictory protection. Do not bypass existing requirements.
6. Wait for both PRs' checks to pass, then use the native stack's queue action from the second PR to queue both changes. Confirm a real `merge_group` run reports `validate` on the combined revision. If the check never starts, inspect the event trigger and required-check identity; do not remove the required check to force a merge.

<details>
<summary>Hint</summary>

Concurrency cancellation is not the merge queue. A merge queue creates its own revision and requires workflows that respond to its event.
</details>

<details>
<summary>Solution</summary>

Completed [stack/queue reference](../solutions/workflows/05-stack-queue.yml). The first PR adds the command; the second PR uses it. Compare check names, commit SHAs, run states and job counts. `stack.position == stack.size` selects the second PR in this two-PR stack; the reference job ID `optional-top-layer` uses GitHub's terminology for that position. Required evidence remains required for both PRs even when optional expensive work runs only for the second. Documented deployment inheritance does not imply arbitrary status-check inheritance. Queue merge limits do not guarantee batched CI builds.
</details>

## Success and cleanup

You can identify layer SHAs, the combined SHA (or explicitly report missing queue evidence) and evidence of an actual cancelled obsolete run. Leave queued changes alone unless the instructor authorizes removal; close and delete only your disposable PRs/branches when done. Reset `LAB_STACK_DELAY_SECONDS` to `0`. Once the queue experiment has finished and no queued PR needs the check, restore only the course-specific policy changes you made, using your recorded settings; never remove pre-existing protections. Remove the temporary Lab 5 required-check requirement before disabling `Lab 05 stack and queue`, otherwise future PRs can be left waiting for a disabled workflow. This workflow is not used in Lab 6. Do not alter shared queue or rulesets. Next: [Lab 6](06-Gates.md).
