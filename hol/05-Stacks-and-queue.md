# 🔨 Lab 5: A small stack and fewer obsolete runs

**Time:** 25 minutes. **Prerequisite:** instructor-provided organization repository and prepared branches/runs. **PAID RUNNER / ADMIN REQUIRED:** merge queue and branch policy are preconfigured; eligibility depends on organization ownership, visibility and plan. **EMU SETUP / GHE.COM SETUP:** use the approved organization and actual host. **DEMO / FALLBACK:** review prepared stack and queue evidence if access or native stacks are unavailable. See [merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

## Objectives

Distinguish per-layer validation from combined-revision integration validation and identify genuinely avoided runs.

## Tasks

1. In the disposable instructor repository, create two small dependent changes using the prepared branches and open linked PRs as directed. Inspect each diff and native stack metadata; distinguish a native stack from manually changing PR bases. [Creating stacks](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests)
2. Inspect `examples/workflows/05-stack-queue.yml` and prepared run logs. Activate only after instructor preflight: queue event, actual target branch, stable required check names, isolated concurrency groups and permissions must fit the training repository. Identify optional expensive top-only work versus checks required on every relevant revision. [Stack CI optimization](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests)
3. Push one harmless update to a course branch. Identify which obsolete PR run is cancelled, whether unrelated runs or merge groups are protected, and count actual jobs avoided. Do not infer savings just because the stack has fewer PRs.
4. With instructor guidance, queue the prepared stack or inspect the recorded queue. Locate the `merge_group` `checks_requested` run, its combined tested commit and base. Explain why successful layer runs do not establish that the combination passed.

<details>
<summary>Hint</summary>

Concurrency cancellation is not the merge queue. A merge queue creates its own revision and requires workflows that respond to its event.
</details>

<details>
<summary>Solution</summary>

See [stack/queue checkpoint](../examples/workflows/05-stack-queue.yml). Compare check names, commit SHAs, run states and job counts. Required evidence remains required even if optional expensive work runs only at a meaningful stack position. Documented deployment inheritance does not imply arbitrary status-check inheritance. Queue merge limits do not guarantee batched CI builds.
</details>

## Success and cleanup

You can identify layer SHAs, the combined SHA and evidence of an actual saved run. Leave queued changes alone unless the instructor authorizes removal; close and delete only your disposable PRs/branches when done. Do not alter shared queue or rulesets. Next: [Lab 6](06-Gates.md).
