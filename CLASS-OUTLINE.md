# Actions Advanced: Faster Feedback, Trusted Delivery

**Status:** proposed class outline, not yet implemented or approved.

An instructor-led follow-up to Actions Fundamentals. Four sections of **1 hour 45 minutes** provide seven hours of instruction and hands-on work. Two 15-minute breaks and a 30-minute lunch complete an eight-hour day.

## Audience and starting point

Developers and platform engineers who can already create workflows, use environments and containers, author actions, call reusable workflows, and apply the supply-chain protections from Actions Fundamentals.

The class applies those foundations to a new question:

> How do we get useful feedback and deliver changes faster without weakening the evidence required to merge or deploy?

Learners use one small application throughout, with independent checks, build output and a health-checkable target. Lab 2 adds a reviewed CodeQL bundle download to teach custom caching rather than duplicate setup-node's built-in npm cache.

## Day schedule

| Time | Activity |
| --- | --- |
| 09:00-10:45 | 1. Measure, cache, and prewarm safely |
| 10:45-11:00 | Break |
| 11:00-12:45 | 2. Avoid unnecessary work and parallelize what remains |
| 12:45-13:15 | Lunch |
| 13:15-15:00 | 3. Reduce runner churn and enforce the right merge gates |
| 15:00-15:15 | Break |
| 15:15-17:00 | 4. Debug efficiently and promote trusted artifacts |

Instruction and labs: **420 minutes**. Breaks and lunch: **60 minutes**. Total: **480 minutes**.

Open with [00-introduction](slides/00-introduction.md) for the trainer introduction, agenda and lab guidance within module 1's first ten minutes. Finish with [99-conclusion](slides/99-conclusion.md) for the recap, cleanup, Q&A, MTM feedback and Microsoft Learn completion within module 4's final ten minutes. Trainer details and QR-code destinations must be filled in before delivery.

## 1. Measure, cache, and prewarm safely

**Outcome:** distinguish queue, setup, and execution bottlenecks; implement safe dependency-cache reuse and explain when a prewarmed image removes repeated setup more effectively.

| Minutes | Format | Content |
| --- | --- | --- |
| 0-10 | Teaching | Scenario, desired feedback time, and fundamentals recap: immutable action dependencies, least privilege, environments, and deployment `cache-mode: none`. |
| 10-20 | Teaching/demo | Actions performance versus usage metrics; queue time versus execution time; workflow latency versus total runner-minutes and cost. |
| 20-30 | Lab 1 | Inspect the baseline run and identify the first optimization target. |
| 30-50 | Teaching | `actions/cache`, restore/save separation, scope, keys, partial matches, conditions, and `cache-mode`. |
| 50-75 | Lab 2 | Complete trusted cache and PR restore-only starters, then compare cold, exact and partial runs. |
| 75-85 | Teaching/demo | Hosted custom images and prefetching tools, packages, Docker images, and action archives; image trust and maintenance. |
| 85-100 | Guided lab/demo | Lab 3: customize and launch the image build, then continue without waiting; ask the trainer to demonstrate the comparison and check back at a later break or before cleanup for your own result. |
| 100-105 | Debrief | Choose between runtime caching and image prewarming; account for rebuild cost and freshness. |

### Content to teach

- [Actions performance metrics](https://github.com/orgs/xebia/actions/metrics/performance) and [usage metrics](https://github.com/orgs/xebia/actions/metrics/usage), with a repository-level fallback.
- Measure before changing the pipeline; retain failures, retries, and cancellations in comparisons.
- Dependency caches versus artifacts, tool caches, Docker layers, and action archive caches.
- Keys that capture OS, architecture, tool/cache schema and a reviewed manifest hash; distinguish tool manifests from execution action lockfiles.
- Most-specific-to-least-specific restore keys and the compatibility boundaries they preserve.
- `cache-hit == 'true'` versus partial `'false'` and empty-string miss.
- Skip upstream download only when the requested archive exists; verify size/checksum, extract and smoke-test even on an exact cache hit.
- `cache-mode: read`, `write`, `write-only`, and `none`; workflow/job scopes and reusable-workflow limits.
- **PR workflows only use `actions/cache/restore` and `cache-mode: read`.**
- Trusted-main writers, hidden caching in setup actions, poisoning risks, no secrets in caches, and cache eviction/thrashing.
- Explain execution ref and cache scope separately using the trust table below; a workflow that can read main's cache cannot necessarily write back to main's scope.
- Reiterate why deployment workflows use `cache-mode: none`.
- Hosted custom-image generation with `snapshot`, as distinct from self-hosted VM/container image building.
- Prefetch SDKs/tool caches, npm package downloads, NuGet packages, and Docker images.
- Docker daemon topology: host, DinD, and job/service initialization determine whether prefetched images are usable.
- Prefetch exact action archives with `gh actions-archive-cache`: install the pinned extension, download, then uninstall before snapshotting. Preserve `ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE`; distinguish it from `_work/_actions` and the dependency cache.
- Protected image builders, reviewed immutable inputs, credential removal, rebuild/patch cadence, version selection, and rollback.
- `cache-mode: none` disables the Actions dependency cache, not preinstalled tools, Docker content, or action archive seeds.

### Lab 1: Find the bottleneck

Install and run the supplied unoptimized baseline, then record queue/setup/check durations, time to feedback, runner type and total job time. Every run downloads and verifies the 559 MB CodeQL bundle in fresh temporary storage, extracts it and checks its version. The app's tests and build each add a labelled 20-second artificial wait before their real work; these same waits apply in later labs. They simulate latency, not CPU load. If queue/capacity prevents completion, ask the trainer to demonstrate and distinguish their measurements from your own. Inspect organizational metrics if access and aggregation allow.

**Evidence:** a baseline worksheet and a justified first optimization, not simply “the workflow is slow.”

### Lab 2: Cold, exact, partial, and read-only

Implement cache restore/save around a supplied downloader for the 559 MB Linux x64 CodeQL v2.27.4 bundle. Key by OS/architecture, tool, participant epoch and `examples/codeql-bundle.json` hash. Trusted main saves; PRs only restore. A helper comment repeats the exact key; a manifest note-only change gives compatible partial reuse; a new epoch gives a miss. Review real version/size/digest updates together; never substitute a restored older version.

Control save using lookup outputs, while always verifying the requested archive, extracting outside the cache and invoking that exact CLI's version command. Measure large upstream versus cache transfers, verification, extraction and save separately; no speedup is assumed.

**Evidence:** the three cache states, changed timings, no PR save operation, and no dependency-cache access in the deployment workflow.

### Cache trust: which branch is the workflow really using?

Distinguish three questions: where the workflow definition comes from, which ref/revision the run represents, and which code/data the job actually consumes. Checking out a different ref does not turn a privileged run into an isolated PR run.

| Trigger/context | Cache scope and poisoning consideration |
| --- | --- |
| `pull_request` | Normal run uses the PR merge ref. It can restore default-branch/base-branch caches; any permitted saves are scoped to `refs/pull/.../merge`, not main. Main and other PRs cannot restore that PR-scoped cache. Course policy still requires restore-only plus `cache-mode: read`. |
| `pull_request_target` | Runs in the PR base-branch context, commonly main, not the untrusted head/merge context. Default-branch cache access is read-only under current low-trust protections unless explicitly overridden. Never check out/execute PR head code here to populate a trusted cache. |
| `issues`, `issue_comment` | Run in default-branch context despite externally influenced metadata. Default-scope cache writes are restricted by default. Keep the issue experiment cache-disabled; issue text must never become executable code. PR review/diff-comment events are different event families with different ref semantics. |
| `workflow_run` | Follow-up workflow runs in default-branch context even if the upstream workflow ran on a PR. Default-scope caches are read-only by default. Explicit write access combined with executing upstream PR artifacts/code can cross the trust boundary. |
| `workflow_dispatch` | Runs on the selected branch/tag, not necessarily the default branch. A default-branch run is write-eligible by default. Authorized dispatch does not make input strings, fetched refs, or external content safe to execute/cache. |
| `repository_dispatch` | Runs on the default branch and is write-eligible by default. Authenticate/restrict dispatch callers, validate `client_payload`, and never let a payload select untrusted code for a trusted cache writer. |
| `push`, `delete`, `registry_package`, `page_build`, `schedule` | Other current default-branch write-eligible triggers. Some operate on selected/event refs; eligibility does not mean every run is on main or every payload is trusted. Inspect the event ref and sources consumed. Main-branch runs can populate caches other branches/PRs restore. |

Under current GitHub.com cache protections, other events resolving to the default branch receive read-only default-scope access unless an explicit `cache-mode: write` or `write-only` opts out. These overrides are not required for the labs and must not be added to make an untrusted-trigger cache save succeed.
Teach the poisoning chain as an inert diagram: attacker-influenced code/data -> write-capable default/base-context job -> cache entry -> later privileged consumer. The risk needs both influence over cached content and a reachable trusted consumer; merely running from a default-branch workflow file is not proof of exploitability. Cache keys and lockfile hashes help matching but are not authentication or a substitute for trusted writers.

As a lab task, ask learners to classify prepared event/ref examples and identify which unsafe write override or untrusted checkout must be removed. Do not enable a vulnerable writer or poison a live cache. Inspect `ACTIONS_CACHE_MODE` and cache logs; a green run does not prove a save occurred.

**Documentation:** [cache scope and low-trust triggers](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching#cache-access-for-low-trust-workflow-triggers), [event ref semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), and [secure use](https://docs.github.com/en/actions/reference/security/secure-use).

### Lab 3: Remove repeated setup

Eligible learners customize the snapshot configuration, build a uniquely named image, pre-pull a Docker image, and inspect it on a separate runner. The stretch goal installs pinned `gh actions-archive-cache`, downloads the exact `tj-actions/changed-files` commit, then uninstalls the extension before snapshotting; the consumer uses the archive without the extension. This optional archive-cache exercise is not a prerequisite for Lab 6, which supplies its own pinned changed-files detector. Others ask the trainer to demonstrate and still complete workflow-editing and analysis.

**Evidence:** identify exactly which downloads/setup were avoided and which still occurred.

**Delivery boundary:** building the image is hands-on for learners with existing permission and approved capacity; no one should buy a plan, change organization policy, or provision paid infrastructure just for class. Image generation may take several hours: launch it during the teaching/demo segment, record its identity, then continue with Lab 4. Check back at a later break and before final cleanup; resume the consumer comparison only when the seeded version is Ready. The trainer can demonstrate using an approved image prepared before class. If still unavailable at cleanup, record the result as pending and agree owner-led cleanup or an explicitly approved follow-up with a deadline. This section does not assume live generation finishes during the 15-minute lab.

**Sources:** [D01-D03, D07, D09-D10, D20, W06, A01-A04, P01-P02](REFERENCES.md).

## 2. Avoid unnecessary work and parallelize what remains

**Outcome:** select the right events and affected components, bound runaway jobs, and choose between parallel steps, separate jobs, and a larger runner using evidence rather than adding runners indiscriminately.

| Minutes | Format | Content |
| --- | --- | --- |
| 0-20 | Teaching/demo | Checkout lifecycle/sparse zizmor (0-8); two artifact packaging/selection patterns and extraction control (8-12); event activities, PR defaults and check-selection pitfalls (12-20). |
| 20-40 | Lab 4, part A | Experiment with issue activities, then inspect prepared docs-only, code, and shared-input changes. |
| 40-60 | Teaching/demo | Native parallel/background steps versus jobs/matrices; synchronization, failure propagation, job/step timeouts, and shared resources. |
| 60-85 | Lab 4, part B | Compare parallel steps/jobs and observe a deliberately bounded stalled check. |
| 85-100 | Teaching/demo | Default/larger hosted versus self-hosted runners; CPU/RAM/disk/network bottlenecks, operational ownership, and cost. |
| 100-105 | Debrief | Select an execution design and defend latency, consumption, cost, and operational trade-offs. |

### Content to teach

- Optimize in this order: avoid unnecessary work, parallelize necessary work, reuse setup, then size the runner.
- Explain what checkout does before tuning it: select repository/path/ref, prepare or clean an existing workspace, configure Git ownership/authentication, fetch objects/history, populate files, optionally fetch LFS/submodules, expose the checked-out revision, and clean up credentials. Distinguish normal Git behavior from REST archive fallback; do not remove isolation or host/auth safeguards for speed.
- Explain sparse checkout before syntax: populate only selected paths in the working tree, retaining the event revision. Show a workflow-only zizmor scan of `.github/workflows` rather than checking out a large application's assets; compare equal scan scope and actual checkout time, not an assumed speedup.
- Distinguish sparse paths from `fetch-depth`: one commit is enough for file-only scanning, but diff/version/tag consumers need their required history. Keep scanner configuration and local actions in scope where relevant; a smaller checkout must not silently reduce validation coverage.
- Leave submodules and LFS downloads off in jobs that do not need them; enable or fetch only required modules/payloads. These and depth 1 are checkout defaults, not automatic new speedups. Note LFS pointers are not payloads, and checkout's `filter` input overrides `sparse-checkout`.
- Artifact downloads: `name`/`artifact-ids` and `pattern` select artifacts, not individual members of a ZIP; `path` is the destination. Show a single-file `archive: false` upload and filename-selected download, or split outputs into scoped artifacts. Avoid transferring unrelated large outputs without dropping required evidence or identity/digest checks.
- Contrast two producer patterns: prepared files/archives, each uploaded with `archive: false` (one file per invocation), versus multiple upload steps creating distinct named bundles with default ZIP packaging. Consumers select required artifacts by filename/name, ID or name pattern. `skip-decompress: true` preserves a downloaded ZIP; false defaults to extraction. Extraction control does not reduce bytes transferred or recursively unpack arbitrary nested archives.
- Event selection is the first filter: use `on.<event>.types: [...]` for supported activity types, not an `event: [types]` key.
- Start with issues: bare `issues:` accepts all supported issue activities; `issues: types: [opened, edited]` selects only those activities. Opening, editing, labeling, and commenting require no branches or code changes.
- Issue comments use the separate `issue_comment` event, not `issues: types: [edited]`. Contrast event families with activity types before introducing PR-specific behavior.
- Bare `pull_request:` runs on `opened`, `synchronize`, and `reopened` by default, not every PR activity. Explicit `types` replaces that default selection; `synchronize` covers new commits pushed to the PR.
- Separate title/body policy checks (`opened`, `edited`, and any other relevant metadata events) from build/test CI (`opened`, `synchronize`, `reopened`). Adding `edited` to code CI normally increases work rather than reducing it.
- Metadata that actually affects validation is an exception: a base-branch change can arrive as `edited`; inspect `github.event.changes` and revalidate the changed target where required.
- Optional draft suppression needs both a condition and `ready_for_review` to start validation when a draft becomes ready. Do not silently skip required validation or forget later code pushes.
- Native workflow `paths`/`paths-ignore` versus changed-file detection followed by job/step `if` conditions.
- Reuse reviewed `tj-actions/changed-files` for impact detection instead of writing a custom Git-diff script. Compare explicit event base/tested SHAs, count deletions and renames, and include shared libraries, lockfiles, build configuration and workflow changes. Keep detection errors blocking.
- PR, push, and merge-group comparisons need the correct event-specific base/head. Explain native diff limits; do not assume one diff recipe covers every event.
- Unknown/failed change detection must not become "nothing changed": block the required gate or explicitly run the full relevant checks.
- Explicit job `timeout-minutes` and narrower step timeouts bound stalled tests, network calls, and readiness checks. The job default is 360 minutes, subject to runner execution limits; a step budget does not extend its job budget.
- Choose timeouts from measured cold/warm durations with headroom, not arbitrary aggressive caps. Distinguish timeout, fail-fast, and obsolete-run cancellation.
- Native `parallel`, `background`, `wait`, `wait-all`, and `cancel`.
- Shared checkout, dependencies, CPU, memory, filesystem, ports, credentials, and output synchronization.
- No concurrent dependency installation into the same mutable workspace.
- Server readiness checks and bounded teardown, not “start it and hope.”
- Separate jobs for independent capacity, platform/toolchain differences, or distinct job permissions.
- Matrices, sharding, `max-parallel`, fail-fast, and meaningful `needs` edges.
- Why more cores help some workloads but not serial/network-bound work.
- Larger hosted runners: resources, selected networking capabilities, runner groups, and autoscaling.

### Lab 4: Run only the necessary work, within a budget

Start with two small broad issue observers; learners restrict the second to creation/edits before installing and predicting results. Open/edit/label/comment a test issue in your lab repository: both/both/broad/neither. Full filtered YAML is a solution, not the starter. Neither observer checks out code or uses issue contents as shell source.

The workflows only report allowlisted event/activity names; they do not execute issue text or post comments. Keep their definitions on the default branch and use `permissions: {}` because this demonstration needs no repository API access or checkout.

Transfer the lesson to a short PR trigger comparison: bare `pull_request:` has restricted defaults, unlike bare `issues:`. Explain `synchronize` for code pushes and why `edited` alone is not code CI. No PR creation is needed for this part; discuss target-branch changes with a prepared payload/run.

Use prepared docs-only, application-code, and shared-lockfile changes to select the relevant checks. Show why a change to shared inputs must fan out to all affected checks.

Compare the same independent checks in prepared sequential, native parallel-step, and separate-job variants. Inspect elapsed time and total runner execution rather than writing each workflow from scratch.

Make one branch fail and confirm the final result still fails. Use a short intentionally stalled step with a one-minute step timeout and a larger job budget; observe termination without waiting for the default job timeout. Discuss a CPU-heavy variant without assuming that more same-runner parallelism is faster.

**Evidence:** a predicted/observed issue-activity run table, correct docs/code/shared-input selection, a decision table for the application, propagated failure, and a bounded stalled check. Reuse prepared runs when runner queuing would consume the lab.

**Sources:** [D01, D04-D06, D08, D17, D22-D25, D26, W02, W06-W07, B01-B02](REFERENCES.md).

## 3. Reduce runner churn and enforce the right merge gates

**Outcome:** reduce obsolete/redundant validation without skipping mandatory evidence; understand which policy blocks a merge and why.

| Minutes | Format | Content |
| --- | --- | --- |
| 0-15 | Teaching/demo | Native stacked PRs, stack metadata, redundant CI, merge queue, and combined-revision validation. |
| 15-40 | Lab 5 | Create bottom and top PRs in the participant repository, configure its queue policy, and compare PR versus combined-revision checks. |
| 40-60 | Teaching | Required status checks, required deployments, and required workflows; scope, trust, skip traps, Evaluate/Active rollout, and bypasses. |
| 60-95 | Lab 6 | Diagnose and satisfy each merge gate independently, then validate the queue revision. |
| 95-105 | Debrief | Review runner churn and policy trade-offs; explain why fewer checks must not mean weaker validation. |

### Content to teach

- Native stacks versus manually targeting one feature branch at another. Create the bottom and top PRs, then use **Create stack** or GitHub's recommendation banner to make them a native stack; stack metadata follows that action.
- Small focused diffs, trunk-based protection, linear history, stack position/size metadata, and current stack merging behavior.
- Run expensive optional work at meaningful stack positions, not automatically on every layer.
- Do not confuse documented deployment inheritance with arbitrary status-check inheritance.
- Avoid duplicate feature-branch push and PR workflows.
- Cancel superseded PR runs without cancelling unrelated merge groups.
- `merge_group: checks_requested`, checkout of the combined revision, queue concurrency/timeouts, and why merge limits do not guarantee batched CI builds.
- **Require status checks to pass:** stable names, expected source, strict/loose updates, and explicit aggregation.
- **Require deployments to succeed:** real successful pre-merge preview/staging evidence, not merely an approval or a job named “deploy.”
- **Require workflows to pass before merging:** centrally selected enforcement, not merely a reusable-workflow call.
- Required-check pitfalls: filtered-out workflows stay pending, skipped jobs may count as successful, and failed dependencies must not bypass the final gate.
- Use an always-running required aggregator that validates change-detection success and the results of every applicable check. Permit a skip only when the impact map explicitly says that check is unnecessary.
- Revisit changed-file selection for `merge_group`: validate the combined revision against its actual base rather than reusing a PR-only changed-file list.
- Central ruleset workflow event/filter behavior, appropriate branch targeting, source visibility, and least privilege.
- Rollout through a pilot and Evaluate where available; controlled, auditable emergency bypass.

### Lab 5: A small stack and fewer obsolete runs

In the participant repository, the bottom PR targets the default branch (`main` in the lab) and adds `npm run check`; the top PR builds on it and uses that command in validation. Use **Create stack** or GitHub's recommendation banner to make the two PRs a native stack, then inspect focused diffs, metadata, required checks on both PRs and optional work only on the top PR.

For cancellation, set the delay to 150 seconds and push a harmless comment on `lab-05-top`. Once validation is waiting, add and push a second comment. Inspect obsolete-run cancellation and reset the delay to zero.

Configure participant-owned merge queue policy for the exact base branch, then queue from the top PR and identify the tested combined commit. Queue policy is a lab setup task, not assumed preconfigured; record and restore only course-specific changes before disabling the workflow.

**Evidence:** distinguish layer validation from integration validation and identify the actual reduction in redundant work.

### Lab 6: Which gate is blocking?

Work through the concrete examples in the participant lab instructions:

1. A failing required check and a skip/aggregation mistake; verify docs-only, shared-input, and failed-change-detection cases.
2. Configure a repository branch ruleset with **Require deployments to succeed → lab-staging**. Use the supplied staging workflow to observe a failed deployment blocking merging, then a successful deployment removing that blocker.
3. A central title policy fails, then passes; a centrally selected workflow remains required if the PR removes its local copy.
4. Compare the Lab 5 queue's combined commit with Lab 6's final-gate evidence.

**Evidence:** each gate blocks for the intended reason and can be satisfied without bypassing or deadlocking it.

**Delivery boundary:** check and deployment gates use repository-local rulesets and the participant's course-only environment. Only central workflow enforcement requires organization ruleset-management permission, Enterprise eligibility and approved Actions sharing on the source repository. Verify that its organization rule selects exactly the participant repository and default branch before activation. Do not broaden source access without owner approval. If any prerequisite is unavailable, the trainer can demonstrate in an authorized trainer repository. If that is also unavailable, explain the behavior without claiming that enforcement was demonstrated. Remove only course-owned rules before disabling their workflows. The staging target is a local job server, not real cloud infrastructure.

**Sources:** [D05, D11-D17, W05, F02-F03, F05](REFERENCES.md).

## 4. Debug efficiently and promote trusted artifacts

**Outcome:** shorten the investigation loop, understand dependency inventory, and verify an artifact before promoting the same bytes.

| Minutes | Format | Content |
| --- | --- | --- |
| 0-15 | Teaching/demo | Step versus runner diagnostics; safe context inspection, bounded tree output, log groups, annotations, and summaries. |
| 15-35 | Lab 7 | Diagnose a prepared workflow failure using safe logs and a debug-enabled rerun. |
| 35-45 | Instructor demo | Debug JS/TS action source with `github/local-action`; run a selected workflow/job through `act` and the VS Code extension; explain fidelity limits. |
| 45-65 | Teaching/guided lab | Lab 8: dependency graph, SHA-to-version enrichment, Jesse Houwing's submission action, and repository versus artifact SBOMs. |
| 65-95 | Lab 9 | Build once, generate provenance/SBOM evidence, verify the artifact and expected signer, then promote unchanged bytes; test tampering. |
| 95-98 | Capstone/debrief | Compare the optimized pipeline with the baseline and defend its performance, policy, and trust decisions. |
| 98-105 | Wrap-up | Recap, complete the cleanup checklist, address Q&A, collect MTM feedback and open Microsoft Learn module-completion links. |

### Content to teach

- `ACTIONS_STEP_DEBUG`, `ACTIONS_RUNNER_DEBUG`, debug-enabled reruns, and `runner.debug`.
- Diagnose timed-out jobs separately from failed/cancelled tests; collect useful diagnostics before the budget expires, since hard cancellation cannot guarantee cleanup or artifact upload.
- `toJSON(github)` can expose sensitive and untrusted fields: prefer selected fields and safe environment-variable handling.
- `toJSON(secrets)` is an anti-pattern, not a recommended trick; masking is not guaranteed.
- Useful diagnostics: selected tool versions/paths, bounded `tree`, groups, annotations, outputs, and summaries.
- `github/local-action` targets unbundled JS/TS action logic, not an entire workflow.
- `act` and GitHub Local Actions for local feedback, not verification of rulesets, real token permissions, OIDC, merge queues, or new server syntax.
- Dependency graph versus dependency submission versus SBOM versus attestation.
- Why SHA pinning and advisory-version matching solve different problems.
- [Improved Dependency Submission for GitHub Actions](https://jessehouwing.net/github-actions-improved-dependency-submission/): retain immutable execution while enriching inventory, including configured upstream mappings.
- Submission permission boundaries, correct base/head snapshot sequencing, unresolved mappings, and experimental Docker-reference detection.
- Graph-exported SBOM versus inventory of the shipped artifact/container.
- Provenance and SBOM attestations, digest binding, expected builder identity, and verification.
- Build-once/promote-many with `cache-mode: none` in deployment; do not promote untrusted PR artifacts.
- A valid attestation does not prove that the artifact is vulnerability-free.

### Lab 7: Find the failure without dumping secrets

Introduce the lab's exact source-path typo in the participant workflow. Use bounded diagnostics and a debug-enabled rerun to identify it, then dispatch a new run at the corrected revision. Rerunning the old revision still tests its typo.

**Evidence:** explain the failure using targeted logs without printing secrets, full environment dumps, or uncontrolled event content.

### Lab 8: Make the dependency inventory useful

Export the participant repository graph before and after trusted dependency submission, compare SHA/version entries, and generate the staged app's npm SBOM. Compare actual coverage, duplicate manifest entries and indexing uncertainty; do not assume either inventory represents every shipped byte.

**Evidence:** explain what each inventory covers, why advisory matching needs version/upstream metadata, and what remains unknown.

**Delivery boundary:** a trusted-branch submission demonstration is the default. Do not grant a fork PR a broad write token to make the exercise work. Any advisory example uses sample data that is never run. If indexing is delayed, the trainer can demonstrate with an already indexed trainer repository; otherwise explain what remains pending.

### Lab 9: Verify, then promote

Install the reviewed release example in the participant repository. Produce an artifact plus provenance/SBOM attestations, verify its digest and exact participant workflow identity, reject altered bytes and the wrong signer, and promote the same archive to a local job server without rebuilding.

Modify a downloaded copy and show verification failure. Show that verification rejects an unexpected signing identity.

**Evidence:** the promoted artifact matches the verified digest, tampering is rejected, and learners can distinguish integrity/provenance from vulnerability assurance.

**Sources:** [D18-D22, L01-L04, S01-S17, W08](REFERENCES.md).

## Scope and pacing

The complete requested scope fits only if environments, test inputs, and workflow variants are prepared. Session 4 deliberately uses an instructor demo for the local tools rather than attempting three separate workstation installations.

### Presentation and facilitation approach

Use the older Intermediate and GH200 materials as teaching references, not as implementation authority. Retain the Intermediate class's small, observable workflow experiments and the GH200 pattern of objectives, worked examples, short checks, and summaries. Write original explanations and examples for this class rather than copying the older slides.

For each substantial concept, use this loop within the allocated times:

1. **Predict:** ask what will execute, what will be reused, or what will block merging.
2. **Explain:** show the relevant execution graph, decision table, or small YAML fragment.
3. **Observe:** run a prepared example and point learners to the specific timeline, output, or policy evidence.
4. **Change:** let learners make a targeted modification, including one intentional failure.
5. **Explain back:** ask why the result changed and what trade-off the optimization introduced.

Keep slides focused on a decision and its visual evidence. Put commands, expected observations, common mistakes, recovery checkpoints, and source links in instructor notes. Include time checks at the end of each scheduled segment and allow learners to reach the same observation before advancing.

Use three original comparison aids:

- **Reuse the right thing:** package-download cache versus build artifact versus tool/action content prebaked into an image.
- **Control the right concurrency:** parallel steps versus jobs/matrices versus concurrency groups; execution capacity is different from stale-run cancellation.
- **Choose the right environment:** default hosted versus larger hosted versus self-hosted, with custom-image preparation treated as a separate decision.

Use these original checks in the existing debrief time, not as extra agenda items:

| Section | Explain-back question |
| --- | --- |
| 1 | Why can a partial tool-download cache match be useful, and why must checksum verification and extraction still run? |
| 2 | Why does adding an issue comment not trigger an `issues` workflow filtered to `edited`, how do PR defaults differ, and what bounds a stalled check? |
| 3 | Can a docs-only change merge safely, and what happens if changed-file detection itself fails? |
| 4 | What does a valid attestation establish, and what does it leave unproven? |

Keep the fundamentals recap to the existing ten minutes. Do not expand this into the older courses' general custom-action authoring, API automation, Azure provisioning, or certification-preparation syllabus.

**Historical-source caution:** GH200's local change log and trainer guide are dated June 2025. Its published timing assumptions do not establish that the new hands-on agenda fits; the new labs need their own rehearsal. Older action versions, workflow commands, local-emulation claims, runner capability tables, and debugging guidance must be refreshed against current sources.

**Sources:** historical material T01-T05 in [REFERENCES.md](REFERENCES.md). Text and speaker notes were reviewed; slide visuals/layouts were not inspected.

Core activities are the numbered labs above. Optional follow-up work, not part of the 420 minutes:

- Build a hosted custom image from scratch or implement a self-hosted/ARC image pipeline.
- Create a larger native stack or use the `gh stack` extension in depth.
- Debug a custom JS/TS action interactively on every learner workstation.
- Configure enterprise fork/mirror submission and private-registry inventory.
- Explore SBOM standards, offline attestation verification, or SLSA builder design in depth.

If a section overruns, use prepared runs for provisioning/indexing waits and shorten demonstrations before dropping the mandatory failure/security cases.

## Instructor preparation

- Supply the small application, lockfile, independent checks, and numbered starter/solution checkpoints.
- Prepare docs-only, component, shared-lockfile/configuration, and detection-failure test cases; include merge-group diff coverage and the one-minute timeout example.
- Install the broad and activity-filtered issue workflows on the default branch; prepare an issue label and confirm learner issue permissions. Keep the exercise read-only apart from learners' own issue edits/labels/comments.
- Run the baseline and all failure cases on the target GitHub tenant.
- Prepare an organization repository with native stacks, merge queue, and appropriate permissions.
- Prepare required-workflow enforcement in an eligible enterprise, or provide an instructor demonstration.
- Prebuild the custom image and set explicit budgets for paid runner resources.
- Prepare a real staging target used only for this course and a non-circular pre-merge deployment policy.
- Check current supported action versions, then generate/review the `actions.lock` file with `gh actions-lock` (not inline SHA pins in every workflow); check the target host's lockfile support and review tool/image versions.
- Verify new syntax against the target service/runner and selected tools.
- Provide public-repository or appropriately licensed attestation/dependency-review examples.
- Keep fake-only local inputs, safe diagnostic examples, and anonymized metrics/run exports.
- Preconfigure trusted dependency submission and retain correctly indexed snapshots.
- Make Docker/local tooling optional unless learner prerequisites were confirmed beforehand.
- Prepare an instructor-note card for each demo: starting checkpoint, prediction, action, expected evidence, failure case, recovery checkpoint, elapsed-time target, and current source.

## What learners leave with

A measured pipeline design, safe cache-key/restore patterns, an informed step/job/runner choice, stack/queue-aware validation, clear policy gates, targeted debugging techniques, and a verified artifact-promotion pattern.

All collected documentation, implementation sources, blogs, version baselines, and product-change watchpoints are maintained in [REFERENCES.md](REFERENCES.md).

Implementation must also satisfy [DELIVERY-REQUIREMENTS.md](DELIVERY-REQUIREMENTS.md): guided labs with hidden solutions/task-level documentation, Markdown slides and notes, Xebia-template PowerPoint decks per module, account/host markers, cleanup, and CodeQL/zizmor validation.
