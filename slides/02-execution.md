# Avoid work before speeding it up
- Choose which events and changes need a workflow run
- Download only the files a job needs
- Run independent checks at the same time
- Set time limits so a stuck job cannot run forever
- Measure the problem before choosing a larger runner

<!-- notes: Timing 0-1 min. Introduce module 2's sequence: filter, select, parallelize, bound, then size. Include checkout and artifact downloads as work to avoid, not just checks. Checkout occupies minutes 1-8, artifact selection 8-12 and events 12-20, keeping the 20-minute teaching opening and 105-minute module intact. State Lab 4 has two parts: issue-activity experiment and prepared workflow comparisons. Expected evidence: learners can tell checkout scope, event filtering and path-based check selection apart. Failure/recovery: demonstrate with trainer workflows if participants cannot run them. If a demonstration is also unavailable, discuss predictions without claiming observations. Docs: [D26](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onevent_nametypes), [W02](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/effective-ci.md). -->

---

# Checkout does more than download code
- `actions/checkout` prepares repository files and Git access for later steps

## Some work depends on the options and files already on the runner
```flow
Prepare | Choose the repository and folder; clean old files if needed.
Set up access | Configure Git authentication and ownership settings.
Get files | Select a revision (commit), fetch data and create local files.
Finish | Get optional files; remove saved Git credentials after the job.
```

<!-- notes: Timing 1-3 min. Walk through the lifecycle rather than reading a list of inputs. actions/checkout runs after the runner has obtained the action itself; downloading the action archive is not the repository checkout. repository, github-server-url and path select source and destination under GITHUB_WORKSPACE; multiple checkout steps can target different repositories/paths. ref defaults to the triggering event ref/SHA for the current repository, not universally main or the PR head; PR runs commonly use a detached merge revision. Without a supplied ref/commit for another repository, it resolves that repository's default branch. The normal Git path inspects Git capability, prepares an existing directory or initializes a repository and origin, handles temporary safe.directory/global config, disables automatic Git garbage collection, configures token/SSH auth, fetches using a targeted refspec and depth/filter, resolves checkout info, applies sparse selection and checks out. LFS setup/fetch and submodule sync/update add work when enabled; exact ordering differs, so the diagram groups responsibilities rather than promising every operation runs in this order. The inspected v7 implementation checks fetched refs against the expected commit, logs commit information and exposes ref/commit outputs. A post-job action removes persisted auth; persist-credentials false removes action-configured auth after checkout instead of leaving it for later steps. Expected evidence: learners map a checkout log group to a responsibility and distinguish setup time from test execution. Failure/recovery: if a required revision/input cannot be obtained, fail and diagnose rather than changing refs or accepting missing files. Source inspected 2026-11-10: [checkout implementation](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/src/git-source-provider.ts), [checkout inputs](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/action.yml). -->

---

# Checkout settings also protect the job
- Submodules link repositories; Git LFS manages large-file downloads

## Keep cleanup and authentication safeguards, even when reducing downloads
| Work | What checkout does | What to consider |
| --- | --- | --- |
| Clean old files | Removes earlier changes | Keep jobs separate |
| Set up Git access | Sets credentials and ownership | Keep access only as long as needed |
| Get source files | Downloads a commit and history | Get the files the job needs |
| Finish and clean up | Gets extras; removes credentials | Skip unused extras, not cleanup |

<!-- notes: Timing 3-4 min. Give the less-obvious details in notes rather than crowding the slide. clean defaults true; on a reused repository it attempts git clean -ffdx and git reset --hard HEAD before fetch and may recreate an incompatible/unusable checkout. This explains why persistent runners do not automatically retain arbitrary build output. Never recommend clean false just to preserve untrusted state. set-safe-directory defaults true to accommodate ownership/container use; it is a Git ownership exception, not sandboxing or proof that code is trustworthy. token defaults to github.token; it is repository-scoped and does not automatically authorize a second private repository. SSH inputs include key, known hosts, strict checking and user; do not disable strict host verification as a speed optimization. persist-credentials defaults true; v6+ uses a separate credentials file under RUNNER_TEMP, with action-managed cleanup after the job. false avoids retaining those Git credentials for later steps but does not revoke the job's token or remove secrets independently exposed to it. fetch-tags defaults false with shallow history, show-progress affects logging rather than scope, and depth 0 fetches all branches/tags. LFS downloads payloads beyond ordinary Git pointers; submodules fetch additional repositories and recursive includes nested ones. Checkout can fall back to a REST archive download if a usable Git command manager is unavailable; that is not a normal local Git checkout, does not support SSH-key/submodule mode, and is not equivalent evidence for history/sparse behavior. LFS/sparse modes require suitable tooling; verify capabilities rather than relying on fallback. v7 also guards fork-code checkout in privileged pull_request_target/workflow_run contexts; do not enable allow-unsafe-pr-checkout as an optimization workaround. Runner Node/runtime compatibility, safe host/auth configuration and post-job cleanup remain preflight requirements. Expected evidence: explain why credentials, optional payloads and an existing workspace can appear in checkout duration. Failure/recovery: retain cleanliness and least privilege; narrow required data instead. Source: [input defaults](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/action.yml), [implementation and cleanup](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/src/git-source-provider.ts). -->

---

# Sparse checkout: get only selected files
- The working tree is your local copy; sparse checkout limits which files appear

## Example: zizmor checks workflow YAML for security problems
```flow
Repository | Contains workflows, application code, docs and large files.
Select folders | Choose the workflow folder for this example.
Local files | Workflow YAML is present; app files are not.
Run zizmor | Scan those workflows, not the whole repository.
```

<!-- notes: Timing 4-5 min. Explain the concept before syntax: Git stores a revision; checkout creates the working tree, the files tools can read on disk. A sparse checkout selects which paths are populated in that working tree without deleting them from the repository or changing the tested commit. Contrast a huge application/assets tree with the handful of workflow files a workflow-only zizmor job reads. This can substantially reduce checkout work and disk I/O on large repositories; savings are workload-dependent, not a measured course speedup. Sparse working-tree selection, shallow history and partial-clone object filtering are different controls. The inspected checkout implementation automatically uses a blob:none fetch filter for sparse checkout when no explicit filter is given, deferring blob content; required blobs are obtained for checkout. This can also reduce transfer, but is implementation/server/tooling-dependent, not a claim that sparse patterns alone universally prevent every unrelated object transfer. Expected evidence: learner explains which files exist on disk and which revision is analyzed. Failure/recovery: if a required config, local action or script is missing, expand the selected paths; do not declare a smaller scan equivalent to full coverage. Docs: [actions/checkout scenarios](https://github.com/actions/checkout#scenarios), [fetch filter implementation](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/src/git-source-provider.ts), [Git sparse-checkout](https://git-scm.com/docs/git-sparse-checkout). -->

---

# Checkout only what the scanner needs
- `fetch-depth: 1` gets one commit; keep the revision selected by the event

## Excerpt: the job needs contents: read, and zizmor must be installed first
```yaml
- uses: actions/checkout@v7.0.1
  with:
    persist-credentials: false
    sparse-checkout: /.github/workflows/
    sparse-checkout-cone-mode: false
    fetch-depth: 1
    submodules: false
    lfs: false
- run: zizmor --strict-collection .github/workflows
```

<!-- notes: Timing 5-7 min. Walk through the example only after the working-tree explanation. This is a steps excerpt, not an installed runnable workflow: root permissions stay empty, the scanner job requests contents: read, cache-mode is none, zizmor is preinstalled at a reviewed version, and checkout@v7.0.1 must be host-supported and locked with the course's generated actions.lock process before use. Do not copy the snippet as a privileged pull_request_target scanner or run PR code. The anchored directory pattern and non-cone mode intentionally exclude root/ancestor files; cone mode can include root and ancestor-level files. fetch-depth: 1 is already checkout's default and suffices for file-only analysis of the event revision. submodules and lfs also default to false; spelling them out teaches intentional avoidance rather than claiming new savings from default values. Demonstrate the visible file tree and zizmor's collected-input inventory; compare checkout duration and disk use with the same revision and scanner scope on a full checkout. .github/workflows is the actual active location in a hosted repo; this course's examples/workflows directory must first be copied there in your lab repository. Include any required zizmor configuration and local action.yml/action.yaml paths in sparse selection AND explicit scanner inputs when broadening the scan; strict-collection rejects parse failures but cannot detect files excluded by sparse checkout. Workflow-only scope does not replace the full course scan. Failure/recovery: missing inputs/configuration or different coverage invalidate the comparison; expand checkout and rerun. Do not claim massive or numerical gains without comparable runs. Docs: [checkout inputs](https://github.com/actions/checkout/blob/main/action.yml), [zizmor input collection](https://docs.zizmor.sh/usage/#input-collection), [workflow dependency lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles). -->

---

# Files, history and optional downloads
- Files, commit history, linked repositories and large files are separate choices

## Choose each setting separately; do not leave required files out
| Setting | What it does | When to download more |
| --- | --- | --- |
| sparse-checkout | Creates selected local files | Add needed settings and actions |
| fetch-depth: 1 | Gets one commit of history | Get more to compare commits |
| submodules: false | Skips linked repositories | Get only those the job uses |
| lfs: false | Skips large-file contents | Get full files, not just LFS links |

<!-- notes: Timing 7-8 min. Separate breadth (files), depth (history), submodule repositories and large-file payloads. Checkout defaults to depth 1 with no submodules or LFS downloads; avoid a shared checkout recipe that turns on fetch-depth: 0, recursive submodules and lfs: true for every job. Fetch the necessary comparison commits/tags or use sufficient history for impact detection/versioning; depth 0 fetches all history for all branches and tags and is justified only where needed. Keep full history in the existing 06-gates.yml change-detection example unless its diff algorithm has been adapted and tested; do not shallow it indiscriminately. With lfs false, checked-out LFS-managed files can remain pointer files, not usable payloads. Jobs that actually need them must fetch the required paths; Git LFS supports include/exclude filters. Submodule true initializes submodules, recursive includes nested ones; selective initialization of reviewed required paths avoids unnecessary repositories. Handle credentials and authorized hosts deliberately. Partial clone filter is a separate advanced input: checkout documents that filter overrides sparse-checkout if set, so do not simply combine them and promise both effects. Expected evidence: learner can explain why a workflow-only scan needs neither full history nor application submodules/LFS, while an integration build may. Failure/recovery: missing merge base, tag, submodule or LFS payload is a correctness failure; restore required inputs, not a success-shaped skip. Docs: [checkout inputs](https://github.com/actions/checkout/blob/main/action.yml), [Git submodule](https://git-scm.com/docs/git-submodule), [Git LFS pull filters](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-pull.adoc). -->

---

# Save outputs as separate artifacts
- An artifact is a job's saved output; split it so later jobs download only what they need

## Downloads select whole artifacts, not individual files inside one ZIP
| Approach | Job that uploads | Job that downloads |
| --- | --- | --- |
| Prepare ZIP files yourself | archive: false; one file per upload | Select the artifact by name (the filename), ID or pattern |
| Let the action package files | Separate uploads with different names | Select the artifact by name, ID or pattern |

<!-- notes: Timing 8-9 min. Present the two patterns explicitly before syntax. Pattern 1: prepare multiple output files or archives such as linux.tgz, windows.zip and test-report.json; publish each via its own archive:false invocation or one invocation per matrix job. Current upload-artifact v7 source rejects a multi-file match when archive is false, so a single wildcard upload is not a supported way to publish those separately. The source filename becomes the artifact name and the name input is ignored. Pattern 2: call upload-artifact multiple times with distinct names and selected file/directory inputs, normally using its default ZIP packaging. Both produce independent artifacts; download-artifact can select a name, immutable artifact ID or artifact-name pattern. The difference is who prepares packaging and the artifact name, not whether arbitrary ZIP members can be fetched. Choose unique filenames/names across matrix jobs; publish only required, secret-free content. Expected evidence: learner identifies which artifacts the consumer will transfer and which large outputs remain untouched. Failure/recovery: if outputs are trapped inside one monolithic artifact, split the producer packaging or accept the full transfer; do not claim a pattern matches internal paths. Sources: [upload single-file validation](https://github.com/actions/upload-artifact/blob/main/src/upload/upload-artifact.ts), [download input selection](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml). -->

---

# Option 1: Upload a ZIP you already created
- `archive: false` uploads one file; `skip-decompress: true` leaves it zipped

## Upload in one job; download in a later job that depends on it
```yaml
- uses: actions/upload-artifact@v7.0.2
  with:
    path: packages/linux.zip
    archive: false
    if-no-files-found: error
- uses: actions/download-artifact@v8.0.2
  with:
    name: linux.zip
    skip-decompress: true
```

<!-- notes: Timing 9-10 min. Prepare linux.zip and other platform files before upload; publish each with its own archive:false invocation or matrix job. This pair selects only linux.zip and intentionally leaves windows.zip untouched. archive:false accepts one file per invocation, ignores name and uses the filename as the artifact name. A wildcard matching multiple files is rejected, not split into uploads. The consumer uses skip-decompress:true so the prepared ZIP remains intact for verification or forwarding; false is the default and extracts a detected ZIP. This extraction switch is independent of whether the producer asked the upload action to create a ZIP. It is not recursive arbitrary-archive extraction; a tar/tgz needs an appropriate explicit unpack command. With path omitted, download goes to GITHUB_WORKSPACE. The snippets belong in separate producer and dependent consumer jobs, with needs ensuring the prepared file was uploaded. Avoid wrapping already-compressed archives in another ZIP without a reason. name and artifact-ids select whole artifacts; pattern matches artifact names, not ZIP members; path is only the destination. skip-decompress avoids extraction work but still transfers the complete selected artifact. Keep digest checking, trusted run/repository selection and required evidence intact; verify signed subject bytes before extraction/execution. This packaging example does not replace Lab 9's exact signed archive. Reviewed action locks are a prerequisite. Expected evidence: only linux.zip is downloaded, remains an archive, and matches its expected digest; compare equal required outputs rather than asserting speedup. Failure/recovery: missing output, wrong digest or a multi-file archive:false match fails; split producer invocations or correct the selection rather than accepting missing evidence. Docs: [download extraction input](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml), [upload archive behavior](https://github.com/actions/upload-artifact#inputs). -->

---

# Option 2: Give each upload a different name
- `skip-decompress: false` extracts the selected ZIP into files

## Save reports separately from the build; the next job downloads only reports
```yaml
- uses: actions/upload-artifact@v7.0.2
  with:
    name: test-reports
    path: reports/
    if-no-files-found: error
- uses: actions/download-artifact@v8.0.2
  with:
    name: test-reports
    skip-decompress: false
```

<!-- notes: Timing 10-12 min. Show the default archive:true approach as the second pattern, not an instruction to put every output into one artifact. Explicit skip-decompress:false shows the default download behavior: extract a detected ZIP into the destination, defaulting to GITHUB_WORKSPACE here. Set it true instead to keep the selected artifact as downloaded for later verification or unpacking; this changes processing, not transfer scope. Auto-extraction is not a recursive unpack of nested archives, and artifact-service digest validation is not a substitute for expected signer/subject verification. A producer uses separate upload-artifact invocations: name test-reports with path reports/, and another named application-build with the large build outputs. The consumer example selects only test-reports, leaving application-build untouched. Each named artifact may contain several files. The shown steps belong to separate producer and dependent consumer jobs and require preflighted versions/locks; the producer must create reports first. For report artifacts from several shards, give uploads distinct names such as test-reports-linux and test-reports-windows; download with pattern: test-reports-* and omit name. pattern filters artifact names, and name takes precedence if both are supplied. Keep merge-multiple false unless intentionally merging output directories; collisions can overwrite filenames. name/ID selects whole artifacts; no internal-file selector exists in the inspected v8 inputs. For outputs that must be required, verify that the expected artifacts/files exist and do not silently treat an empty pattern match as successful evidence. Same-run transfers use the action's run-scoped service; cross-run/repository transfers require reviewed run/repository identity and suitable minimal actions:read access. Keep digest checking and release verification; these examples do not change Lab 9's signed archive. Expected evidence: consumer receives reports but not the large build artifact. Failure/recovery: missing report is a failure, not a reason to download untrusted replacement output or weaken identity checks. Sources: [multiple named uploads](https://github.com/actions/upload-artifact#not-uploading-to-the-same-artifact), [download patterns](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/README.md#download-multiple-filtered-artifacts-to-the-same-directory). -->

---

# Choose an event, then its activity types
- `issues` is an event; opening or editing an issue is an activity

## Trigger examples only; types selects which activities start the workflow
```yaml
# File A: all issue activities
on:
  issues:
# File B: only opening and editing
on:
  issues:
    types: [opened, edited]
# Comments use issue_comment, a different event.
```

<!-- notes: Timing 12-16 min. Teach event family before activity type. `issues: types: [opened, edited]` includes opening and editing; labeling is excluded. A comment belongs to `issue_comment`, not `issues: types: [edited]`. Workflow files for these events must be on the default branch. Demo checkpoint: inspect the two prepared workflow declarations before changing an issue. Expected evidence: learners correctly predict which workflow runs for opened, edited, labeled, and commented events. Failure/recovery: if an event did not appear, verify workflow exists on default branch and inspect the actual activity type. Docs: [D27](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues), [D28](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment), [D26](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onevent_nametypes). -->

---

# Pull requests have different defaults
- Without `types`, runs start on opened, synchronize and reopened
- `synchronize` means the PR branch received new commits
- Setting `types` replaces that default list
- Checking a PR title is different from testing changed code
- If changed files are unknown, run all checks or block merging

<!-- notes: Timing 16-20 min. Finish the teaching/demo segment by transferring issue filtering to PR defaults and path-based selection. Separate metadata checks from code CI; include relevant base-branch edits and ready-for-review behavior. Changed-file selection is an impact model: include shared libraries, lockfiles, build config, and workflows. A required workflow filtered away can remain pending; unknown/failed detection must not become “nothing changed.” Expected evidence: learners classify PR activity and state the safe fallback for failed detection. Failure/recovery: restore an always-running aggregator or run full validation; do not green-light on missing impact data. Docs: [D22](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request), [D23](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore), [D26](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onevent_nametypes), [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). -->

---

# Lab 4A: Predict which workflows will run
- Make a prediction, change an issue, then compare the runs with your prediction
- First restrict the second starter to issue creation and edits

## Expected results, not results from an actual run
| Your action | issues without types | issues: opened, edited |
| --- | --- | --- |
| Open issue | Runs | Runs |
| Edit title | Runs | Runs |
| Add label | Runs | Does not run |
| Add comment | Does not run | Does not run |

<!-- notes: Timing 20-30 min. Start Lab 4 part A and run the issue experiment. The workflows should only report allowlisted event/activity names; no checkout, no API writes, `permissions: {}`, and `cache-mode: none`. Learners' own issue edits, labels and comments are the only interaction. Expected evidence: completed predicted/observed table; comment triggers neither issues workflow. Failure/recovery: if a learner cannot label, use instructor demonstration or a prepared issue; do not broaden permissions or ask for an org policy change. Docs: [D27](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues), [D28](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment), [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). -->

---

# Plan which files need checks
- A required gate is a final check that decides whether merging is allowed

## Impact detection: choose checks from changed files; the final gate always runs
| What changed? | Application checks | Final required gate |
| --- | --- | --- |
| Only course documentation | Skip only if it cannot affect the app | Confirm the skip was allowed |
| app/src/server.js | Run | Require checks to pass |
| Lockfile, workflow or shared settings | Run the checks these files affect | Require checks to pass |
| Cannot identify changed files | Run all checks or block merging | Never treat unknown as safe |

<!-- notes: Timing 30-40 min. Prediction/discussion only: Lab 4's live experiment is the issue-activity table, not a prepared path-detector example. Map docs, application and shared inputs to checks and identify why a final gate must always report. Lab 6 supplies its own pinned tj-actions/changed-files detector with explicit event base/tested SHAs, local history and fail-on-diff-error; it does not depend on Lab 3's optional archive-cache stretch. Learners implement the final aggregator in Lab 6. Do not activate those workflows early. Expected evidence here is a justified selection table, not a claimed live run. Unknown detection must run full checks or block, never imply no impact. Docs: [D23](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore), [B03](https://github.com/tj-actions/changed-files/tree/9426d40962ed5378910ee2e21d5f8c6fcbf2dd96), [D17](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks). -->

---

# Run independent steps at the same time
- `parallel` waits for both checks to finish before the build starts

## Shorthand for background steps plus one wait
```yaml
- run: npm ci --ignore-scripts
  working-directory: app
- parallel:
    - run: npm run lint
      working-directory: app
    - run: npm test
      working-directory: app
- run: npm run build
  working-directory: app
```

<!-- notes: Timing 40-45 min. Start the 40-60 teaching/demo segment. Correctly distinguish the syntax: `parallel` takes a list of steps and has an implicit join before continuing; the docs describe it as shorthand for marking each step `background: true` followed by a `wait`. Use `parallel` for a self-contained group; use `background` when a step must keep running across later steps or be referenced by `wait` or `cancel`. `background: true` marks an asynchronous run/uses step. `wait` accepts an ID or array; `wait-all:` waits for active work; `cancel: step-id` terminates background work. Expected evidence: learners can describe where synchronization occurs. Docs: [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [D01S](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/content/actions/reference/workflows-and-actions/workflow-syntax.md#L1078-L1235). -->

---

# Wait for background work before using it
- `background: true` lets later steps start before that step finishes
- Use `wait` or `wait-all` before using its results; failures are reported there
- At most ten background steps run at the same time
- The runner waits for background work before final cleanup
- `wait`, `wait-all` and `cancel` cannot use an `if` condition

<!-- notes: Timing 45-46 min. Introduce the next three examples within the existing 45-53 minute segment. Explain that background outputs/environment changes become available after an appropriate wait. Failures surface at synchronization unless the background step is allowed to fail. More than ten background steps queue. `wait`, `wait-all`, and `cancel` do not support `if`; native `parallel` and internal background declarations are unsupported inside composite actions, though a composite can be invoked as a background step. The final cleanup wait is a safety net, not a substitute for waiting before consuming results. On an unsupported participant host, the trainer can demonstrate on a supported host or explain the examples without claiming they ran. Docs: [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [D01S](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/content/actions/reference/workflows-and-actions/workflow-syntax.md#L1078-L1235). -->

---

# wait: finish a named step before continuing
- Lint runs while the build runs; inspect the artifact only after the wait

## Step excerpt: checkout, Node and npm installation already completed
```yaml
- id: build
  run: npm run build
  working-directory: app
  background: true
- run: npm run lint
  working-directory: app
- wait: build
- run: cat app/dist/BUILD.txt
```

<!-- notes: Timing 46-48 min. This is a steps excerpt in a Linux job, not a standalone workflow. Assume reviewed checkout, Node 24, npm ci --ignore-scripts in app, empty root permissions, job contents read, timeout and execution lock are already configured. The build has the app's labelled 20-second teaching delay; lint can finish while it is still running. Ask which step makes BUILD.txt safe to read. wait: build blocks until the build finishes and exposes its result; a failed build fails the wait, so the final ordinary run step does not run. wait can also accept a list, for example wait: [frontend, backend], when those background IDs exist. Do not put an if condition on wait. This is a worked example, not another required lab or a measured speedup. If demonstrating, use a supported trainer host and inspect both build and wait results. Docs: [wait](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepswait). -->

---

# wait-all: finish every active background step
- Build starts only after both checks finish successfully

## Step excerpt: two checks, one synchronization point
```yaml
- id: lint
  run: cd app && npm run lint
  background: true
- id: tests
  run: cd app && npm test
  background: true
- wait-all:
- run: cd app && npm run build
```

<!-- notes: Timing 48-50 min. Same Linux job prerequisites as the wait example: reviewed checkout, Node 24, npm ci --ignore-scripts in app, least privilege, timeout and execution lock. wait-all takes no value: leave the YAML value empty, not true or a list of IDs. It waits for all active background steps, not just the one declared immediately before it. In this example both checks must finish successfully before the ordinary build step runs. If either check fails, the synchronization reports failure and the build skips; do not set continue-on-error on these checks. Do not put if on wait-all. Prefer parallel for this self-contained group in ordinary code; this expanded version teaches what the explicit synchronization does. These checks do not share generated files, but other workloads may need isolation. Docs: [wait-all](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepswait-all). -->

---

# cancel: stop a background process by its ID
- Stop the heartbeat after testing; do not wait for an endless loop to finish

## Step excerpt: a visible heartbeat while tests run
```yaml
- id: heartbeat
  background: true
  run: |
    while true; do
      echo "Tests are still running"
      sleep 5
    done
- run: cd app && npm test
- cancel: heartbeat
```

<!-- notes: Timing 50-53 min. Same Linux job prerequisites as the other excerpts. The shell loop prints a heartbeat every five seconds and has no natural end. cancel targets one background step by its id; the runner sends SIGTERM and then SIGKILL if it does not exit within the grace period. Unlike wait, cancel requests termination rather than waiting for normal completion. Do not use wait-all to stop an endless process: it would keep waiting until the process exits or a timeout intervenes. The cancel construct always runs, including after a failed test, and does not accept if. It does not turn failed tests into a successful job. For a real server, starting in the background does not prove readiness; check health before sending requests. The heartbeat avoids introducing that separate readiness problem. Keep the enclosing job timeout as a final bound and confirm host support before a demonstration. Docs: [cancel](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepscancel). -->

---

# Choose steps, jobs or a matrix
- A matrix repeats a job with different settings, such as Node versions

## Compare ways to run the same code-style checks and tests
| Approach | Where checks run | Cost or risk |
| --- | --- | --- |
| Steps one after another | One runner and folder | Wait for each check |
| Parallel steps | Share processor, files and ports | Can change the same files |
| Separate jobs | Separate runners and credentials | Setup runs again for each job |
| Matrix | One job per settings combination | Too many jobs waste capacity |

<!-- notes: Timing 53-56 min. Contrast sequential steps, native parallel steps, background steps, separate jobs, and matrices. Parallel steps share CPU/RAM/disk, workspace, ports, credentials, and mutable package directories; do not install dependencies concurrently into one workspace. Separate jobs repeat setup but can use different permissions or capacity. Matrix `max-parallel` and `fail-fast` are not workflow concurrency controls. Expected evidence: learners select a design and defend resource/setup trade-offs. Failure/recovery: if a supposedly independent task shares files or ports, serialize it or isolate its workspace. Docs: [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [D04](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations), [D05](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency). -->

---

# Test each OS and Node version
- 2 operating systems × 3 Node versions = 6 jobs; at most 3 run at a time

## Scatter/gather: six matrix jobs, at most three at once, then one required decision
```scatter
Ubuntu · Node 24 | Test
Ubuntu · Node 25 | Test
Ubuntu · Node 26 | Test
Windows · Node 24 | Test
Windows · Node 25 | Test
Windows · Node 26 | Test
Results | Collect all six.
Required gate | Pass only if all pass.
```

<!-- notes: Timing 56-60 min. Worked example only, not another required lab. This editable scatter/gather diagram replaces the YAML panel; point out that `max-parallel: 3` allows at most three combinations to run at once. As a job finishes, another can start; a separate required gate evaluates the collected outcomes. A compatibility matrix repeats the same complete test suite for each OS/version combination; it does not split the suite into smaller groups. Contrast with test sharding: divide a large suite into groups, run each group on a separate runner, then collect results. Enumerate Ubuntu/24, Ubuntu/25, Ubuntu/26, Windows/24, Windows/25 and Windows/26. Each matrix job gets its own runner and repeats setup. max-parallel: 3 allows at most three matrix jobs at once; available capacity can reduce that number. fail-fast: false lets the other combinations finish when one fails, providing compatibility information. The default true cancels queued and running matrix jobs when a non-continue-on-error job fails; useful for saving work, but some combinations may remain untested. Neither setting allows failed, cancelled or missing required results to count as a pass. These controls are not workflow-level concurrency or cancellation of older PR runs. Node 24/25/26 is an example version set, not a claim that each version is available, maintained or supported on every host at class time. Preflight actual versions and the project's support policy; do not silently substitute a version when setup fails. A .NET course could instead pair OS values with eligible .NET SDK versions such as 10.x and 11.x, after checking project target frameworks and SDK availability; changing setup alone is not a valid .NET test example. The equivalent YAML uses `strategy.matrix` for OS/node, `max-parallel: 3`, `fail-fast: false`, then an explicit required gate. Before runnable use, add reviewed checkout with persist-credentials false, root permissions {}, job contents: read, a timeout and the course's reviewed action lock. Use cache-mode: none and package-manager-cache: false for a no-cache comparison; do not introduce an implicit setup-node cache writer. The selected npm scripts must work on both operating systems. Check runner label architecture and runtime support. Expected evidence: learner predicts six jobs, at most three at once, and explains why full-suite repetition tests compatibility rather than making one suite cheaper. Failure/recovery: correct unsupported SDK/runner or demonstrate on a supported trainer host. If neither is possible, explain the limitation without reporting skipped checks as successful. Docs: [D04](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations), [setup-node](https://github.com/actions/setup-node). -->

---

# Lab 4B: Implement and compare checks
- Complete shared-parallel and separate-job checks from the starter
- Predict time until results and total runner-minutes
- Compare runs that use the same checks and inputs
- Set fail-test; confirm failure and both dependent builds are skipped

<!-- notes: Timing 60-70 min, pending a fresh timed starter rehearsal. Learners copy 04-parallel.yml from examples/workflows, retain its sequential baseline, and implement both concurrency TODOs and fail-test propagation before lock/review/dispatch. The completed solution is linked only in the collapsed lab answer; do not install it for learners. With fail-test false, all equivalent checks should pass. With true, both test branches fail and both dependent builds skip; sequential can still pass but the workflow fails. Historical completed-checkpoint observations were 10 seconds for sequential/shared versus 24 summed seconds for separate jobs, not a general speedup. Report queues separately; disable all four Lab 4 workflows afterward. Docs: [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [D04](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations), [W02](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/effective-ci.md). -->

---

# Start, check and stop background services
- A successful start command does not prove that the server is ready for tests

## Example sequence, not runnable YAML
```flow
Start | Start the test service with a time limit.
Check readiness | Request /health until ready or the time limit expires.
Test | Run tests only after the service responds correctly.
Stop | Stop the service and save relevant logs before time runs out.
```

<!-- notes: Timing 70-78 min. Demonstrate a prepared server/test pattern. Readiness is an observed health condition, not “the start command returned.” If server logs or outputs are required, wait for that step; cancel it after the dependent checks. Expected evidence: correct readiness signal and bounded teardown. Failure/recovery: if health never becomes ready, timeout and inspect bounded logs; never leave an indefinite wait or assume cleanup will succeed after hard cancellation. Docs: [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [D25](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepstimeout-minutes). -->

---

# A timeout stops work, not the underlying bug
- A timeout is a time limit; this step should stop and the job should not pass

## Timeout solution excerpt; this example is designed to fail
```yaml
intentional-timeout:
  runs-on: ubuntu-latest
  timeout-minutes: 3
  steps:
    - name: Wait two minutes; expect the one-minute limit to stop it
      timeout-minutes: 1
      run: sleep 120
```

<!-- notes: Timing 78-85 min. Show a short deliberately stalled step with a one-minute step timeout and a larger job budget. Explain fail-fast, timeouts, and obsolete-run cancellation as different controls. Capture needed diagnostics before timeout because hard cancellation may prevent artifact upload. Expected evidence: bounded stalled check terminates and the job remains failed; budget has headroom from observed timings. Failure/recovery: when timeout is too aggressive, restore a measured budget; do not turn timeout/cancellation into a green required gate. Docs: [D24](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idtimeout-minutes), [D25](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepstimeout-minutes), [D05](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency). -->

---

# Choose runner size from measurements
- Requires: larger runners (Team or Enterprise Cloud), organization owner, paid minutes
- Find what limits speed: processor, memory, disk or network
- More processor cores do not fix a slow external service
- Compare time until results with the cost of the runner
- Include time waiting for an available runner

<!-- notes: Timing 85-93 min. Begin the 85-100 runner demo. Use prepared standard/larger-runner evidence. Explain that larger runners may address CPU, memory, disk, specialized hardware, or selected networking; they do not remove unnecessary work or improve a slow external API automatically. Check current availability and billing, not stale price assumptions. Expected evidence: a measured bottleneck tied to the proposed size. Failure/recovery: if resource telemetry is absent, mark the sizing choice as provisional and gather evidence rather than claiming more cores will help. Docs: [D06](https://docs.github.com/en/actions/concepts/runners/larger-runners), [D08](https://docs.github.com/en/actions/concepts/runners/larger-runners#billing), [W03](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/engineering-system-metrics.md). -->

---

# Decide who manages the runners
- Requires: organization owner for shared runners; larger runners also need paid minutes
- GitHub-hosted: GitHub maintains the runner machines
- Larger GitHub-hosted: more capacity and additional features
- Self-hosted: you maintain the machines, network and security
- Actions Runner Controller (ARC) manages runners on Kubernetes
- Do not run unreviewed public PR code on shared private runners

<!-- notes: Timing 93-100 min. Compare management responsibility, isolation, warmup, scaling, and operating costs. PAID RUNNER / ADMIN REQUIRED: larger-runner capacity/image/network features may require org setup, billing authorization, and administrator action; confirm plan, region, runner group, and feature eligibility separately. DEMO / FALLBACK: use prepared runs if learner access is unavailable. Do not make paid provisioning a learner task. Avoid public untrusted PR execution on organizational self-hosted runners; ephemeral does not remove in-job network/credential risk. Cleanup: stop lab workflows and deprovision only course-owned paid capacity; coordinate shared runner groups with admins. Docs: [D06](https://docs.github.com/en/actions/concepts/runners/larger-runners), [D07](https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images), [W06](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/deploying-actions-runner-controller.md), [W04](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/application-security/recommendations/actions-security.md). -->

---

# Review: What should run, and how?
- Which issue changes started each workflow?
- Why did adding a comment start neither workflow?
- Which checks can safely run at the same time?
- Which measurements justify the time limit?
- Did faster results also reduce total runner-minutes?

<!-- notes: Timing 100-105 min. Use explain-back questions, not a new activity. Expected evidence: issue activity predictions match observations; learners distinguish bare issues from bare PR defaults; parallelism preserves failure; timeout is bounded; runner choice follows a measured bottleneck. If a live run failed, explain why and demonstrate the intended behavior if possible. State what remains unobserved. Close exactly at 12:45 for lunch. Docs: [D27](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues), [D22](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request), [D01](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). -->
