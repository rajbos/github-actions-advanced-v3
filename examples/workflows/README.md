# Learner workflow starters

Copy only the starter named by the current lab into `.github/workflows`. Complete its tasks and TODOs before expecting success; regenerate and review `actions.lock` after changing action references. Never bulk-install this directory.

`TODO` marks work for you to implement, not a command that GitHub Actions understands. Read the nearby comments and the linked lab for the required change and expected result. A placeholder that prints `TODO` and exits with an error is intentionally incomplete: replace the whole placeholder with your implementation, not just its error message or `exit` command. For the timeout exercise, the completed step still fails, but because its time limit is reached rather than because the placeholder exits immediately.

The completed reference implementations are in [`solutions/workflows`](../../solutions/workflows). Open them through a lab's collapsed solution section after attempting the exercise. They are not the files to copy at the start. Baselines, observers and the minimal local demo are intentionally runnable because their exercises focus on using and observing them.

| Files | Supplied starting point | Learner work |
| --- | --- | --- |
| `01-baseline.yml` | Unoptimized application pipeline | Run and measure; a baseline is intentionally runnable. |
| `02-cache-*.yml` | Safe boundaries and verified CodeQL archive preparation/smoke test | Design manifest-based keys; implement trusted save and PR restore-only reuse for a 559 MB download. |
| `03-build-prewarm.yml` | Snapshot fields and tool setup | Customize identity; implement npm download-cache seeding, Docker pre-pull and optional extension install/download/uninstall. |
| `03-prewarm.yml` | Read-only image assertions | Select/verify the actual image; add the stretch action and output inspection. |
| `04-issues-all.yml`, `04-issues-filtered.yml` | Identical broad event observers | Restrict the second observer before predicting and testing. |
| `04-parallel.yml` | Sequential baseline and job setup | Implement shared parallel checks, isolated checks and failure propagation. |
| `04-timeout.yml` | Job budget and explicit incomplete step | Implement a shorter step budget and bounded stall. |
| `05-stack-queue.yml` | Runnable validation, top-PR report and bounded delay; concurrency TODO | Write the PR-only `concurrency:` group, make the two dependent app/workflow changes; create a stack, observe jobs and cancellation, and configure/use the merge queue. |
| `06-gates.yml`, `06-central-required.yml` | Impact detector, app checks and policy inputs | Implement fail-closed aggregation and metadata policy before enforcing rules. |
| `06-staging.yml` | Runnable local deployment and health check | Configure Require deployments to succeed for lab-staging in a repository branch ruleset; toggle failure and observe the merge blocker. |
| `07-debug.yml` | Deliberately failing source check | Diagnose without a supplied listing, add narrow evidence and repair the revision. |
| `07-local-emulator.yml` | Minimal instructor demo workflow | Discuss what local execution cannot prove; no authored solution required. |
| `08-dependencies.yml` | Trusted-main checkout with read-only permission | Configure verified-lock submission and grant only its job the needed write access. |
| `09-release.yml` | Build/archive/artifact handoff and promotion scaffolding | Add SBOM, attestations, constrained verification, negative cases and same-byte local promotion. |

Unfinished evidence-producing steps deliberately return nonzero rather than report success. Do not remove these barriers until their implementation exists. Existing security boundaries are not TODOs to weaken. Preserve cleanup and paid-resource approval requirements.
