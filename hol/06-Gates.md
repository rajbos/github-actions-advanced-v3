# 🔨 Lab 6: Which gate is blocking?

**Time:** 35 minutes. **Prerequisite:** [Lab 5](05-Stacks-and-queue.md), your own disposable organization-owned repository, and permission to create and manage organization rulesets. **ORG ADMIN OR EQUIVALENT REQUIRED:** use an organization owner account or an authorized organization role with equivalent ruleset-management permissions. Repository admin access alone is not enough to create an organization ruleset. **GHEC REQUIRED:** the centrally required-workflow rule needs an eligible GitHub Enterprise Cloud organization. There are **no administrator-prepared rulesets**: you create your own during this lab. **EMU SETUP / GHE.COM SETUP:** use your approved identity and actual enterprise host. If you lack the permissions or feature, use the instructor's recorded evidence for that part; do not request broader access or edit a shared rule to work around it. Real cloud resources are not part of this exercise.

## Objectives

Diagnose required checks, deployments and centrally required workflows independently without bypassing any gate.

> **Trainer note — demonstrate when participants lack permissions:** If participants do not have organization-owner or equivalent organization ruleset-management permissions, deliver the ruleset setup and enforcement steps as a trainer-led demo instead of asking them to obtain elevated access. The trainer must have the required permissions and use a disposable lab demo repository. Create a uniquely named demo ruleset, choose **Only selected repositories**, and select **exactly that lab demo repository**, with only its default branch targeted. Show the saved repository selection before activating the rule. Never target all repositories, a broad pattern or participants' repositories for the demo. Learners predict and explain the outcomes while the trainer operates the rule. Disable and remove only the demo ruleset during cleanup. If the trainer also lacks permissions or feature eligibility, use recorded evidence and state that live enforcement was not demonstrated.

## Create a ruleset for only your repository

1. Record your exact `OWNER/REPOSITORY`, its default branch and a unique ruleset name, such as `actions-lab6-<repository>-<your-handle>-<date>-<suffix>`. Replace the placeholders; add a short random suffix if needed. Do not reuse another participant's ruleset.
2. In your **organization's Settings**, open **Repository → Rulesets → New ruleset → New branch ruleset**. Enter your unique name and leave **Enforcement status: Disabled** while configuring it. This is an organization ruleset, not a rule created only in repository settings. [Create organization rulesets](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization)
3. Under **Target repositories → Repository targeting criteria**, choose **Only selected repositories**. Click **Select repositories**, search for your exact repository and select **only that one**. Verify the selected list contains exactly your repository. **Never choose All repositories, a name pattern, a property filter or another participant's repository.**
4. Under **Target branches**, include only your default branch (`main` in the examples). Do not select all branches. Leave the bypass list empty for this exercise. Record the ruleset URL or ID so you can find your own rule during cleanup.
5. Before enforcing anything, copy the reviewed Lab 6 workflow examples you need into `.github/workflows` in your repository's default branch. Confirm the actions/lockfile and host prerequisites from setup. Use `06-gates.yml` for the final required check, `06-staging.yml` for the local test deployment, and `06-central-required.yml` as the required-workflow source. If an example has a disabled-job guard, enable the relevant lab jobs without removing their existing safety conditions.
6. Configure the rule needed for each scenario below, one at a time: **Require status checks to pass** with the observed final `required` check and its expected GitHub Actions source; **Require deployments to succeed** with your course-only staging environment; or **Require workflows to pass before merging** with your selected source repository, default-branch ref and `.github/workflows/06-central-required.yml`. Create the staging environment only in your own repository if needed. The workflow source may be your own eligible organization repository; choosing a source workflow does **not** choose which repositories the ruleset protects.
7. Recheck the unique name, **one selected repository**, target branch and chosen rule before saving. Save it Disabled, reopen it and confirm the scope. Then set it to **Active** to test blocking behavior on a fresh disposable PR. **Evaluate** can preview violations but does not block merging, so it cannot prove the gate works. If any selection includes another repository, stop and correct it before activation. Never change an existing shared ruleset.

Existing organization or enterprise rules still apply. Your new rule cannot weaken them. If a separate rule blocks your PR, identify it; do not modify it or add a bypass.

## Tasks

1. Inspect `examples/workflows/06-gates.yml` and the [required check troubleshooting guide](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). With your own scoped ruleset active, identify your PR's latest commit, expected check source and exact blocker. Create failing and passing cases only in your disposable repository.
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

You can explain each blocker and a non-bypass resolution, and show that your ruleset targets exactly your repository and default branch. Cancel your course runs and close only your disposable PRs. Open the organization ruleset using the URL/ID you recorded; confirm its unique name and single-repository scope, disable it, then delete only that lab ruleset when its evidence is no longer needed. Remove only your course-only staging environment after checking that no deployment is active. Do not change other participants' rules or shared organization/enterprise policy; coordinate any shared queue cleanup with its owner. Next: [Lab 7](07-Debug.md).
