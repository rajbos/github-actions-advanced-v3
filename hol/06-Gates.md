# 🔨 Lab 6: Which gate is blocking?

**Time:** 35 minutes. **Prerequisite:** instructor-prepared policy scenarios and [Lab 5](05-Stacks-and-queue.md). **GHEC REQUIRED:** centrally required workflows require eligible Enterprise Cloud organization/enterprise ruleset setup. **PAID RUNNER / ADMIN REQUIRED:** queue, rulesets and any real staging environment are prepared by an administrator; do not create or alter them. **EMU SETUP / GHE.COM SETUP:** use the approved repository and real host; availability is separately verified. **DEMO / FALLBACK:** diagnose prepared policy and deployment evidence when a gate cannot be exercised.

## Objectives

Diagnose required checks, deployments and centrally required workflows independently without bypassing any gate.

## Tasks

1. Inspect `examples/workflows/06-gates.yml` and the [required check troubleshooting guide](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). Do not copy it into a protected/shared repository without instructor preflight. Use the prepared scenarios to identify the latest commit, expected check source and exact blocker.
2. For docs-only, code, shared-input and failed-detection scenarios, fill in: detection outcome; applicable checks; each result (`success`, `failure`, `cancelled`, `skipped`, or missing); expected final gate. Distinguish an intentional skip supported by a successful impact decision from an unknown or failed detector. [Available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
3. Diagnose passing tests with an unsuccessful required staging deployment. What actual evidence is required? Is an approval or a job called “deploy” enough? Inspect the inert [local staging example](../examples/workflows/06-staging.yml) and the instructor's safe prepared deployment record; do not modify cloud resources.
4. Diagnose passing repository-local checks but a missing centrally required workflow. Inspect the inert [central policy example](../examples/workflows/06-central-required.yml). Explain why merely calling a reusable workflow does not enforce it. Review [required workflows](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-workflows-to-pass-before-merging).
5. Trace the corrected queue scenario through the actual combined revision and stable required check. If access allows, inspect the instructor's prepared run; otherwise use recorded evidence. Discuss Evaluate/pilot and auditable emergency bypass without performing a bypass.

<details>
<summary>Hint</summary>

Look at the rule and exact SHA before looking for a green badge. Skipped jobs and a workflow that never ran have different outcomes.
</details>

<details>
<summary>Solution</summary>

The [gate checkpoint](../examples/workflows/06-gates.yml) illustrates an always-running aggregator. It must explicitly validate detection success and every applicable result; failure, cancellation, timeout, missing evidence or an unjustified skip fails it. A docs-only skip is acceptable only if a successful reviewed impact decision permits it. Required deployments need actual successful pre-merge deployment evidence to the required environment, not just approval. A centrally enforced workflow is a separate policy requirement. The queue checks the combined revision, not only the PR head.
</details>

## Success and cleanup

You can explain each blocker and a non-bypass resolution. Do not merge or modify policies unless instructed. Cancel your course runs and close only your disposable PRs; coordinate ruleset/queue cleanup with the administrator. Next: [Lab 7](07-Debug.md).
