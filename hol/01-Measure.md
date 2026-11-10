# 🔨 Lab 1: Find the bottleneck

**Time:** 10 minutes. **Prerequisite:** [setup](00-Setup.md) and an instructor-prepared baseline run of `examples/workflows/01-baseline.yml`. **DEMO / FALLBACK:** use the prepared run if dispatch, queue, or metrics access is unavailable.

## Objectives

Separate queue delay, setup and execution time; propose an optimization supported by evidence rather than by a single total duration.

## Tasks

1. Open the prepared baseline run in **Actions**. If the instructor permits a fresh run, copy only `01-baseline.yml` to `.github/workflows`, commit it on the default branch and dispatch it. Do not wait for a queued run: use the prepared evidence instead. [Managing workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs)
2. Record runner type, queued and started times, job duration, checkout/setup/install and each check duration. Note failures, retries or cancellations, plus the workflow's end-to-end feedback time and the sum of job execution times. What can and cannot be inferred about billable usage?
3. If permitted, compare [performance and usage metrics](https://docs.github.com/en/actions/how-tos/administer/view-metrics); access/aggregation can differ, so use the run timeline if unavailable. Propose a first target and explain why it is material.

| Observation | Your evidence |
| --- | --- |
| Queue versus execution | |
| Setup versus test/lint/build | |
| Feedback latency versus job time | |
| Proposed optimization and uncertainty | |

<details>
<summary>Hint</summary>

Do not count waiting for a runner as test execution, and do not assume the longest visible step will remain the bottleneck after a change.
</details>

<details>
<summary>Solution / interpretation</summary>

The [baseline template](../examples/workflows/01-baseline.yml) is the checkpoint. A defensible answer identifies the measured largest repeatable contributor and a relevant intervention: cache downloads for repeated dependency setup, parallelize independent CPU work only after measuring it, or investigate runner capacity when queueing dominates. A single run and a metrics dashboard may have different populations; preserve failed and cancelled observations.
</details>

## Success and cleanup

You have a filled worksheet and a justified first experiment. Cancel an unneeded active run; keep the baseline workflow and evidence for comparison if the instructor requests it. Confirm no schedules were created. Next: [Lab 2](02-Cache.md).
