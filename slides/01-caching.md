# Faster checks without weaker safeguards
- A workflow runs jobs; each runner is a machine that runs a job
- A pull request (PR) proposes code changes for review
- Measure waiting time before changing how jobs run
- Reuse downloaded packages, but still install and test them

<!-- notes: Timing 0-3 min. Welcome learners to module 1 of the 105-minute section. Frame the class question: reduce time to useful feedback without weakening merge or deployment evidence. Demo checkpoint: show the small application pipeline and its baseline run, not a prepared “fast” result. Expected evidence: learners can name the workflow and one wait they want to understand. Failure/recovery: if the live run is unavailable, use an anonymized recorded run and say it is prepared evidence. Docs: [W02](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/effective-ci.md), [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). -->

---

# Remove unnecessary work first
- Make checks faster without removing tests or security controls

## Try these changes in order
```flow
Avoid | Skip a check only when the change cannot affect it.
Run together | Run independent checks at the same time.
Reuse | Reuse downloads and tools from a reviewed source.
Choose capacity | Use a larger runner only if measurements justify it.
```

<!-- notes: Timing 3-7 min. Explain this ordering and ask learners which tempting optimization they would postpone. Demo checkpoint: compare a workflow run's elapsed duration with aggregate runner time. Expected evidence: learners distinguish faster feedback from lower consumption. Failure/recovery: if metrics are inaccessible, use repository-level metrics or an anonymized instructor export. Docs: [W02](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/effective-ci.md), [D09](https://docs.github.com/en/actions/concepts/metrics), [D10](https://docs.github.com/en/actions/how-tos/administer/view-metrics). -->

---

# Measure a run before making changes
- This first measurement is the baseline for later comparisons

## Example times, not measurements from this course
```flow
Waiting: 2 min | The job waits in a queue for a runner.
Setup: 3 min | Download code, prepare tools and install packages.
Checks: 5 min | Check code style (lint), run tests and build.
Result: 10 min | The runner worked for 8 minutes; waiting took 2.
```

<!-- notes: Timing 7-10 min. Distinguish time-to-feedback from summed runner execution and avoid treating one lucky run as representative. Demo checkpoint: open the run timeline and one comparable recent run. Expected evidence: learners can point to queue, setup, and critical-path work separately. Failure/recovery: queue delay can hide execution improvements; record it separately. Docs: [D09](https://docs.github.com/en/actions/concepts/metrics), [D10](https://docs.github.com/en/actions/how-tos/administer/view-metrics), [W03](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/engineering-system-metrics.md). -->

---

# A faster result can use more runner time
- Runner-minutes add up time used by all runners, not time spent waiting

## Example: same checks, no waiting; actual billing may round time
| Design | Time until result | Total runner time |
| --- | --- | --- |
| One job: setup 2 min, two 4 min checks | 10 minutes | 10 runner-minutes |
| Two jobs together: each 2 + 4 min | 6 minutes | 12 runner-minutes |
| Difference | Result arrives 40% sooner | Uses 20% more runner time |

<!-- notes: Timing 10-20 min. Teach Actions performance versus usage metrics; distinguish queue time from execution time, workflow latency from aggregate runner-minutes, and elapsed duration from cost. Use anonymized/repository-level metrics if organization dashboards are inaccessible. Demo checkpoint: compare an apparently faster run with total runner execution and current runner rates. Expected evidence: learners can describe a useful before/after measure and its caveats. Failure/recovery: if p50/p95 are not exposed, do not imply the dashboard provides them; use a consistent sample and label the statistic. Docs: [D09](https://docs.github.com/en/actions/concepts/metrics), [D10](https://docs.github.com/en/actions/how-tos/administer/view-metrics), [X01](https://github.com/orgs/xebia/actions/metrics/performance), [X02](https://github.com/orgs/xebia/actions/metrics/usage), [W03](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/engineering-system-metrics.md). -->

---

# Lab 1: Find where time is spent
- Open the example run provided by the instructor
- Record time spent waiting, preparing tools and running checks
- Record total runner-minutes as a separate measurement
- Choose one change and explain why it should help

<!-- notes: Timing 20-30 min. Let learners inspect independently for the first half, then pair-check observations. Demo checkpoint: compare the timeline with Actions performance/usage metrics where available. Expected evidence: queue/setup/check measurements and a justified first optimization. Failure/recovery: if organization metrics are unavailable, fall back to repository-level views or anonymized CSV; do not make a fresh run or privileged dashboard access a prerequisite. Docs: [D09](https://docs.github.com/en/actions/concepts/metrics), [D10](https://docs.github.com/en/actions/how-tos/administer/view-metrics). -->

---

# Choose what to save and reuse
- Caches save reusable downloads; artifacts save a job's output

## These stores serve different purposes
| Store | What it holds | How it is used |
| --- | --- | --- |
| Package cache | Packages in ~/.npm | npm ci installs these packages |
| Artifact | Build: application.tgz | Next job downloads and verifies it |
| Tool / action archive | Saved tools or action code | Set up exact versions |
| Container / runner image | Saved software and files | Start with tools already installed |

<!-- notes: Timing 30-36 min. Explain that these stores have different lifetimes, boundaries, and consumers. `cache-mode: none` disables the Actions dependency cache; it does not remove tools or Docker layers from an image. Demo checkpoint: point to one example of a package cache and one artifact handoff. Expected evidence: learners choose the mechanism that matches the material and trust boundary. Failure/recovery: if learners call every reusable store “the cache,” ask who writes it, where it lives, and what consumes it. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [A02](https://github.com/actions/runner/blob/310a370bf3605f5b092f8af63b3126627de2a210/src/Runner.Worker/ActionManager.cs#L1232-L1305), [W06](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/deploying-actions-runner-controller.md). -->

---

# A cache key identifies reusable downloads
- The lockfile lists exact package versions; its hash identifies its contents

## Example key: a label used to find a saved cache
```text
Linux-X64-npm-node24-lab-v1-8c31...
  OS  CPU  tool Node version cache version lockfile hash

Exact key:      Linux-X64-npm-node24-lab-v1-8c31...
Restore prefix: Linux-X64-npm-node24-lab-v1-
Cache version: change lab-v1 to lab-v2 to stop reusing v1

A prefix matches the start of a key, not the package hash.
Matching a key does not prove that the contents are safe.
```

<!-- notes: Timing 36-43 min. Walk through a package-download key conceptually: platform, package manager/runtime, schema epoch, lockfile hash. A key is a matching contract, not authentication. Broad restore keys may cross incompatible toolchains if designed carelessly. Demo checkpoint: compare exact key, restore-key prefix, and changed epoch in prepared checkpoints. Expected evidence: learners can explain why a cache matched and what compatibility assumptions it makes. Failure/recovery: if a key is too broad, tighten its prefix and use a new epoch rather than deleting shared caches. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [D03](https://github.com/actions/cache#outputs). -->

---

# Finding a cache does not install packages
- `npm ci` installs the lockfile's package versions, even when downloads are cached

## A cache hit means a saved cache was found
| Cache lookup | cache-hit output | Still required |
| --- | --- | --- |
| Exact hit: full key matches | 'true' | Install with npm ci |
| Partial hit: only prefix matches | 'false' | Install with npm ci |
| Miss: no saved cache matches | '' (empty string) | Install with npm ci |

<!-- notes: Timing 43-47 min within the caching lesson. Stress that `cache-hit` is a string and that an empty string is not the same as `'false'`. `npm ci` reconciles the lockfile and installs the project even on an exact npm download-cache hit. Demo checkpoint: show the prepared exact/partial/miss outputs. Expected evidence: learners correctly explain the three states and why installation remains mandatory. Failure/recovery: if a condition checks only `'false'`, change it to handle every non-exact hit, for example `!= 'true'`. Docs: [D03](https://github.com/actions/cache#outputs), [P01](https://docs.npmjs.com/cli/v11/commands/npm-ci/). -->

---

# Let reviewed code save the cache
- PR jobs may download caches, not save them; deployment jobs use no cache

## PR example from 02-cache-pr.yml; incomplete, not runnable on its own
```yaml
permissions: {}
cache-mode: read
steps:
  - uses: actions/cache/restore@v6.1.0
    with:
      path: ~/.npm
      # key and restore-keys omitted; see full workflow
  - run: npm ci --ignore-scripts
    working-directory: app
```

<!-- notes: Timing 47-50 min concludes the 30-50 teaching/demo segment. Distinguish course policy from platform defaults: this class requires PR restore-only plus `cache-mode: read`, while current low-trust default-context protections and cache scopes are separate platform behavior. A default-branch workflow file does not make its input trusted. Ordinary pull_request caches use PR merge-ref scope; privileged/default-context events have different scope and write restrictions. Explicit write/write-only can override safeguards and is not a recovery fix. `cache-mode` is currently a GitHub.com/Enterprise Cloud feature, not universal GHES syntax. Demo checkpoint: show a PR restore step and a deployment with no Actions cache access. Expected evidence: no PR save operation; deployment uses none. Failure/recovery: if a setup action hides an implicit writer, disable its package-manager cache and keep explicit restore behavior. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [D03](https://github.com/actions/cache#outputs), [F01](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/features/actions-cache-mode.yml), [D19](https://docs.github.com/en/actions/reference/security/secure-use). -->

---

# Lab 2: Compare cache results
- Open the instructor's example: code on the reviewed default branch, main, saves a cache
- Open a pull request; its job downloads the cache but cannot save it
- Compare no saved cache (a cold run) with an exact cache hit
- Use the prepared lockfile change to observe a partial hit
- Change lab-v1 to lab-v2 in the key and restore prefix for a miss

<!-- notes: Timing 50-58 min. Launch Lab 2 using the instructor's prepared branch and run, not the unexplained shorthand "trusted-writer checkpoint." Point to the reviewed main job that saves downloaded packages and the pull-request job that can only download them. Cold means no matching cache exists; exact and partial hits were defined on the earlier lookup slide. Demonstrate the lockfile change and cache-version change separately: keep lab-v1 for the prepared lockfile change so its restore prefix can find compatible downloads, then change lab-v1 to lab-v2 in both the exact key and restore prefix for a miss. "Schema epoch" in technical cache discussions means this manually chosen cache-format/version label; learners do not need that term to do the exercise. Do not invent a broader prefix or change real dependencies just to manufacture a hit. Expected evidence: cold, exact, partial and new-version miss observations; no PR save. Failure/recovery: if the cache cannot be populated, use the instructor's recorded main run without granting write permission to the PR. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [D03](https://github.com/actions/cache#outputs). -->

---

# Check the logs, not just the green result
- An exact or partial hit still requires package installation
- A miss means packages must be downloaded without a saved cache
- Read the cache step's outputs and download/save messages
- A job can pass even when saving the cache was not allowed

<!-- notes: Timing 58-67 min. Have learners record hit state, restore/install/save times, and total job duration. Inspect `ACTIONS_CACHE_MODE` and cache logs; disallowed operations can log and continue, so job success alone is not evidence of a write. Demonstrate that `npm ci` remains on all paths. Expected evidence: run comparison table plus proof of read-only PR behavior. Failure/recovery: if logs are ambiguous, inspect the step outputs and action logs; do not “fix” a failed save by granting PR write mode. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [D03](https://github.com/actions/cache#outputs), [P01](https://docs.npmjs.com/cli/v11/commands/npm-ci/). -->

---

# Review what the cache-saving job runs
- A workflow on main can still be unsafe if it runs unreviewed code

## Who can save, download or use the cache?
```flow
Reviewed main | Only reviewed code and packages may save the cache.
Saved packages | Store package downloads, never passwords or tokens.
PR job | Download only; install packages with npm ci.
Deployment | Use no package cache; verify the release artifact.
```

<!-- notes: Timing 67-75 min, closing Lab 2. Draw an inert trust chain: untrusted input -> write-capable job -> shared cache -> privileged consumer. Do not demonstrate poisoning or enable an unsafe writer. Ask learners to inspect workflow definition, run ref, consumed code/data, and cache scope separately. Expected evidence: PR has restore-only access; trusted writer consumes reviewed inputs; deployment has no dependency-cache access. Failure/recovery: if an event/ref example is uncertain, consult event semantics and cache low-trust docs; do not assume default-branch YAML equals trusted execution. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#cache-access-for-low-trust-workflow-triggers), [D22](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [D19](https://docs.github.com/en/actions/reference/security/secure-use), [D20](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles). -->

---

# Prepare runner software in advance
- Prewarming means installing tools before the job starts
- A custom runner image saves this prepared environment
- Reusing it can avoid repeated downloads and installations
- Someone must pay for, update and rebuild the image
- On supported hosted runners, `snapshot` creates the image

<!-- notes: Timing 75-85 min. Explain Lab 3 uses an instructor-prebuilt image; image creation is not a timed learner prerequisite. GitHub-hosted larger runners support custom-image generation with `snapshot` on supported configurations; check tenant, runner, plan, region, retention, and billing eligibility before class. PAID RUNNER / ADMIN REQUIRED: generation may need provisioned larger-runner capacity, billing authorization, and organization admin setup. DEMO / FALLBACK: consume an instructor-prebuilt image or compare prepared run evidence; no learner purchases or policy changes. Prefetching SDKs, package downloads, Docker content, and action archives are separate mechanisms. Demo checkpoint: show image identity/version and a comparable baseline. Expected evidence: learners identify repeated work an image avoided and what still ran. Failure/recovery: if learner access or paid capacity is unavailable, use a prepared instructor run and equivalent logs. Docs: [D07](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images), [D08](https://docs.github.com/en/actions/concepts/runners/larger-runners#billing), [A01](https://github.com/actions/action-versions/blob/e3c62146623237ce0e50fbb68f09fc0c4739446a/README.md), [A02](https://github.com/actions/runner/blob/310a370bf3605f5b092f8af63b3126627de2a210/src/Runner.Worker/ActionManager.cs#L1232-L1305). -->

---

# Lab 3: Inspect a prepared image
- Find the runner image name and version in the example run
- Compare its setup steps with the baseline run
- Check which Docker service runs the containers
- Check logs: was saved action code reused for the exact commit?

<!-- notes: Timing 85-90 min. Launch Lab 3 at 85 minutes. Let learners inspect an image consumer run and record setup steps avoided. Action archive cache is not `_work/_actions`; the runner resolves exact action commits, and the archive cache must be configured before action preparation. For Docker, determine whether the consumer uses host, DinD, or another daemon. Expected evidence: learners name both avoided and remaining setup. Failure/recovery: when image cache data is absent or not used, use the baseline and prepared image logs; do not claim a cache hit without evidence. Docs: [D07](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images), [A01](https://github.com/actions/action-versions/blob/e3c62146623237ce0e50fbb68f09fc0c4739446a/README.md), [A02](https://github.com/actions/runner/blob/310a370bf3605f5b092f8af63b3126627de2a210/src/Runner.Worker/ActionManager.cs#L1232-L1305). -->

---

# Include the work of maintaining an image
- Measure which setup steps were avoided and which still ran
- Compare total runner time and cost
- Include the cost of creating and storing images
- Plan updates and a way to return to a previous image
- During cleanup, remove only resources created for this course

<!-- notes: Timing 90-100 min. Review image comparison and whether the same workload, runner capacity, and comparable queue conditions were used. Discuss image freshness, reviewed seeds, protected builders, rebuild cadence, retention/storage charges, and deprovisioning paid runner/image resources. Cleanup means stop training workflows and remove course-owned images/runners only; preserve shared infrastructure and coordinate admin-owned policy. Expected evidence: a decision to cache, prewarm, or do neither, defended by observed savings and ownership cost. Failure/recovery: if billing data is not available, call out the missing cost evidence and use current documented rates only as an estimate. Docs: [D07](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images), [D08](https://docs.github.com/en/actions/concepts/runners/larger-runners#billing), [W06](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/deploying-actions-runner-controller.md). -->

---

# Review: When is reuse worthwhile?
- Why is a partial package-cache hit still useful?
- Why must `npm ci` still install packages?
- Which job is allowed to save the cache, and why?
- When would a prepared image help more than a package cache?
- What still costs money or needs updating?

<!-- notes: Timing 100-105 min. Use the existing five-minute debrief only; ask for concise explain-backs. Expected evidence: learners connect partial download reuse to lockfile reconciliation, identify the restore-only PR rule and deployment none mode, and include freshness/cost in the prewarm choice. Failure/recovery: if time is short, use prepared run evidence rather than dropping the security or cost question. Close on time for the 10:45 break. Docs: [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [P01](https://docs.npmjs.com/cli/v11/commands/npm-ci/), [D07](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images). -->
