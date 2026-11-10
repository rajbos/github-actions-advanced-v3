# Fewer repeated runs, the same safeguards
- A stack is a group of pull requests that build on one another
- Test the combined changes before merging them
- Keep the required checks and deployment results
- An unknown result must not count as a pass

<!-- notes: Timing 0-5 min. Introduce the module's distinction: reduce redundant or obsolete work, but retain required layer and integration evidence. Demo checkpoint: show a prepared two-change stack and an integration run. Expected evidence: learners can state what evidence must remain for every proposed optimization. Failure/recovery: if the organization demo repository is unavailable, use prepared run and ruleset screenshots; do not make enterprise provisioning a learner task. Docs: [D12](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests), [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue), [W05](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/governance/recommendations/managing-repositories-at-scale/rulesets-best-practices.md). -->

---

# Review each change, then test them together
- Each PR is a layer in the stack; review it separately and test the combination

## Example: PR B needs the changes from PR A
```flow
main | The branch that will receive the changes.
PR A: service | Changes the service; still needs its own required checks.
PR B: screen | Uses A's service; review only B's added changes.
Combined commit | Test both changes with the latest target branch.
```

<!-- notes: Timing 5-10 min. Explain native stacked PR relationships, stack position/size metadata, and the difference from manually targeting an unrelated feature branch. Native stack behavior has specific branch protection and merge semantics. Expected evidence: learners can identify base/head dependency for each layer. Failure/recovery: if stack metadata is unavailable in the tenant/repository, use prepared evidence and avoid assuming arbitrary branch chains receive native stack behavior. Docs: [D12](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests), [D14](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests). -->

---

# Avoid running the same checks twice
- Do not duplicate checks on both a branch push and its pull request
- Some optional checks may run only on the last PR in a stack
- Keep each PR's required checks
- Cancel an older PR run when a newer commit replaces it

<!-- notes: Timing 10-15 min. Discuss avoiding duplicate feature-branch push and PR workflows, stack-aware optional jobs, and cancellation groups that isolate a PR without cancelling merge-group runs. Deployment requirements documented for linear stacks do not imply arbitrary status-check inheritance. Expected evidence: a proposed reduction identifies exactly which redundant runs disappear and which required results remain. Failure/recovery: if cancellation groups overlap, separate PR and merge-group namespaces. Docs: [D13](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests), [D05](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency). -->

---

# The merge queue tests changes together
- A merge queue tests PRs with the latest target branch before merging

## Trigger excerpt: merge_group starts a run for the combined commit
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
  merge_group:
    types: [checks_requested]

# PR run: test the commit selected by the PR event.
# Queue run: test the combined commit, not just the PR.
# github.sha identifies the commit tested by this run.
```

<!-- notes: Timing 15-20 min. Start Lab 5 introduction within the scheduled 15-40 lab segment after showing the combined revision concept. Merge-queue availability depends on repository ownership, visibility/plan, and current product terms; verify F02 for the training tenant. GHEC REQUIRED only where the selected org plan/feature requires it; otherwise use the eligible prepared org repository. DEMO / FALLBACK: recorded queue run with tested commit evidence. Expected evidence: learner identifies the exact combined commit tested. Failure/recovery: if no merge-group run appears, check workflow trigger, queue eligibility, and required checks; do not infer integration validation from PR-head green checks. Docs: [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue), [F02](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/merge-queue.md). -->

---

# Lab 5: Build a small stack
- Use the instructor's branches to create two linked PRs
- Read each PR's diff: the lines that it adds or removes
- Compare checks on every PR with optional checks on the last PR
- List the checks that must still pass for each PR

<!-- notes: Timing 20-28 min. Learners create or inspect two dependent changes using prepared branches in the organization demo repository. Keep changes small and use a top-only condition only for optional expensive work. Expected evidence: stack graph, focused diffs, and explicit list of mandatory results. Failure/recovery: if native stack creation or permissions fail, switch to instructor-prepared linked PRs; do not spend lab time granting broad access. Docs: [D12](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests), [D13](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests), [D14](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests). -->

---

# See which old runs can be cancelled
- Push the instructor's example update to one PR
- Observe which runs restart and which older runs are cancelled
- Confirm PR cancellation does not stop merge-queue checks
- Measure the runner-minutes saved

<!-- notes: Timing 28-35 min. Demonstrate a prepared push/update and inspect superseded runs. Expected evidence: learners identify obsolete PR-run cancellation and distinguish it from validation on a combined queue revision. Failure/recovery: if run concurrency obscures the comparison, use prepared runs and report queue time separately. Docs: [D05](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency), [D13](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests), [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue). -->

---

# Lab 5: Check the combined changes
- Add the example stack to the merge queue
- Find the combined commit and its required check results
- Compare each PR's checks with checks of the combined changes
- Explain which repeated work was avoided

<!-- notes: Timing 35-40 min. Finish Lab 5 in the prepared organization repository and identify the tested combined commit. Expected evidence: learners distinguish layer validation from integration validation and quantify any meaningful reduction in redundant work. Failure/recovery: if queue capacity or access is unavailable, inspect the instructor's captured merge-group run and clearly label it as demonstration evidence. Docs: [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue), [D12](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests). -->

---

# Three independent merge controls
- A ruleset is a set of repository rules; these rules can block merging

## Passing one rule does not satisfy the others
| Rule requires | What must exist | What is not enough |
| --- | --- | --- |
| A status check | Passing check from the expected source and commit | Passing result on an older commit |
| A deployment | Successful deployment to the chosen environment | Approval, or a job named deploy |
| A required workflow | Passing workflow selected by the ruleset | Calling an optional shared workflow |

<!-- notes: Timing 40-45 min. Begin the 40-60 teaching segment. Contrast the three rules by evidence type and enforcement source. Check eligibility for each rule separately; do not claim every ruleset capability is Enterprise-only. Expected evidence: learners classify a prepared merge blocker by its actual rule. Failure/recovery: if UI wording differs by plan or host, use current ruleset docs and tenant verification, not a stale screenshot. Docs: [D15](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [D16](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-workflows-to-pass-before-merging), [W09](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/collaboration/recommendations/scaling-actions-reusability.md). -->

---

# Make required checks easy to identify
- Use a consistent check name and select its expected source
- Check whether the rule requires an up-to-date branch
- Filtering out a whole workflow can leave its required check pending
- A skipped job can appear successful without doing any work

<!-- notes: Timing 45-50 min. Explain required check names, source selection, and strict/loose branch update behavior. A workflow filtered out at trigger level can leave a required check pending; skipped jobs can have successful-looking conclusions. Expected evidence: learners can diagnose a check that is absent versus failed. Failure/recovery: use an always-running aggregator instead of weakening policy or selecting an unstable matrix-generated name. Docs: [D15](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). -->

---

# Required deployments need real evidence
- Require a successful deployment before allowing a merge
- An environment is a named deployment target, such as staging
- Approving a deployment does not mean it ran successfully
- A job named deploy is not proof that deployment occurred
- Select the required environment and expected source

<!-- notes: Timing 50-55 min. Show the prepared staging gate and distinguish successful deployment from approval or a job label. Check repository visibility/plan and selected environment eligibility separately. Do not have learners provision a production target. Expected evidence: an actual successful deployment record tied to the expected revision. Failure/recovery: if staging is unavailable, use the prepared run and identify its tested revision; never mark an approval-only scenario as success. Docs: [D15](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [F05](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/repo-rules.md). -->

---

# An organization can require a workflow
- This rule needs GitHub Enterprise Cloud (GHEC) and an eligible source repository

## An organization rule requires results, not just reuse of workflow code
```flow
Organization rule | An administrator selects a workflow and target branches.
Workflow source | A reviewed workflow in an accessible, eligible repository.
Commit to test | Run the workflow for the commit the rule requires.
Merge decision | Missing or failed results keep merging blocked.
```

<!-- notes: Timing 55-60 min. Required workflows need Enterprise Cloud and supported host/version eligibility per current feature gate; confirm organization ownership and repository source visibility before class. GHEC REQUIRED: this specific centrally enforced required-workflow feature, not every ruleset or required check. EMU SETUP: if using Enterprise Managed Users, confirm its separate identity and repository setup; do not treat EMU as a substitute for every GHEC account. GHE.COM SETUP: use the enterprise's actual host, auth, API endpoints, and feature availability. DEMO / FALLBACK: instructor's eligible org or prepared evidence. Expected evidence: learner identifies the central enforcement rule and source, not merely a workflow call. Failure/recovery: if unsupported, run the instructor demo and use an eligible fallback; never ask learners to change enterprise policy. Docs: [D16](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-workflows-to-pass-before-merging), [F03](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/features/repo-rules-required-workflows.yml), [F05](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/repo-rules.md). -->

---

# Lab 6: Find why merging is blocked
- Open the instructor's example PR and repository rules
- Name the rule that is not yet satisfied
- Change one relevant setting or input at a time
- Do not bypass the rule to make the example pass

<!-- notes: Timing 60-65 min. Launch Lab 6 with prepared scenarios: failing check, deployment gate, central workflow, and queue. Learners should report the rule name, expected evidence, and observed state before changing anything. Expected evidence: intended cause, not guesswork. Failure/recovery: if the scenario state drifted, restore the prepared ruleset/run checkpoint with the instructor; do not edit shared policy. Docs: [D15](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). -->

---

# Lab 6: Choose checks from changed files
- Try changes to documentation, application code and shared files
- Shared files include workflows, lockfiles and shared libraries
- Recheck changed files for the merge queue's combined commit
- If file detection fails, run all checks or block merging

<!-- notes: Timing 65-72 min. Inspect prepared docs-only, application-code, shared-lockfile/configuration, and detection-failure fixtures. Use a reviewed impact map. Re-evaluate the combined revision for `merge_group`; do not reuse a PR-only changed-file list. Expected evidence: correct applicable-check table for every fixture and no success-shaped detection failure. Failure/recovery: when path detection fails or exceeds limits, run the full relevant checks or fail the gate. Docs: [D23](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore), [B02](https://github.com/dorny/paths-filter/blob/f3360c560367c9daf72b88c0e6164162034c5721/README.md), [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue). -->

---

# Lab 6: Make the final check verify results
- DETECTION: file detection passed; REQUIRED: checks needed; RESULT: check outcome

## 06-gates.yml: impact decision means whether the changed files require checks
```bash
test "$DETECTION" = success
case "$REQUIRED" in
  true) test "$RESULT" = success ;;
  false) test "$RESULT" = skipped ;;
  *) echo 'Invalid or missing impact decision' >&2; exit 1 ;;
esac
```

<!-- notes: Timing 72-79 min. Review a prepared always-running aggregator that validates change-detection success and every applicable check. Ensure skipped jobs do not bypass the final gate; failed dependencies and missing outputs remain failures. Expected evidence: docs-only change safely skips only irrelevant checks; shared inputs fan out; failed detection blocks or runs all. Failure/recovery: if the aggregator can't distinguish skipped from failed, fix its result logic before considering the policy satisfied. Docs: [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks), [D23](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore). -->

---

# Lab 6: Tests are only one merge rule
- A SHA identifies a commit; results must be for the required commit

## Predict the decision for these examples
| Checks | Deployment | Central workflow | Decision |
| --- | --- | --- | --- |
| Pass | Failed | Pass | Block: failed deployment |
| Pass | Success | Missing | Block: missing workflow |
| Pass on old commit | Success | Pass | Block: old check results |
| Pass, required commit | Success | Pass | All three rules satisfied |

<!-- notes: Timing 79-86 min. Use the prepared deployment-failed and required-workflow-missing scenarios. Learners should satisfy each gate independently, then inspect the queue case. Bypass is not the lab recovery path; emergency bypass must be controlled and auditable by the organization's policy owners. Expected evidence: each scenario blocks for the intended reason and clears only with its required evidence. Failure/recovery: when a check is green on the wrong SHA, rerun or validate the current required revision; do not accept stale evidence. Docs: [D15](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [D16](https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-workflows-to-pass-before-merging), [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). -->

---

# Lab 6: Check the merge-queue run
- Find required checks for the combined commit
- Confirm the run was started by `merge_group`
- Check that no required workflow is missing because of a filter
- Record the results that allow merging

<!-- notes: Timing 86-95 min. Finish Lab 6 with the queue scenario. Learners confirm required workflow/check coverage on the combined revision and explain how a filtered workflow or skipped required job could deadlock or weaken the gate. Expected evidence: intended gate blocks until the exact evidence is successful, and the tested combined commit is known. Failure/recovery: if queue access is unavailable, use a prepared instructor run and make the limitation explicit. At cleanup, remove only course-owned temporary branches/runs and coordinate shared ruleset/queue changes with administrators; never delete shared policy. Docs: [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue), [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). -->

---

# Review: Fewer runs, but still enough checks
- Which repeated runs did we avoid?
- What tests each PR and the combined changes?
- When can a documentation-only change safely skip tests?
- What happens if we cannot identify the changed files?
- Which rule changes need an administrator?

<!-- notes: Timing 95-105 min. Use the full ten-minute debrief. Ask learners to explain stack-level evidence, queue combined revision, a safe docs-only path, detection failure behavior, and the difference between required status checks, deployments, and central workflows. GHEC REQUIRED recap applies to the specific required-workflow rule; eligibility for other rules is independently checked. Cleanup: do not leave temporary branches or active runs; coordinate rule/queue changes with admin and retain shared policy. Expected evidence: a design that reduces redundant work while every merge gate has explicit evidence. Failure/recovery: if a policy demo was unavailable, state that tenant validation remains pending rather than claiming success. Docs: [D12](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests), [D11](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue), [D15](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [W05](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/governance/recommendations/managing-repositories-at-scale/rulesets-best-practices.md). -->
