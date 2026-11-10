# Publication validation status

**Status: blocked; do not publish runnable course material yet.** Checked 2026-11-10. The walkthrough sections below record partial live tenant rehearsal, corrections and limitations. They do not clear all historical publication gates or establish complete security validation.

## Inventory and permissions

### Introduction and conclusion decks (2026-11-11)

- Added `00-introduction` with trainer-detail placeholders, the day agenda and participant guidance. Added `99-conclusion` with recap, explicit lab/paid-resource cleanup, Q&A, MTM feedback and Microsoft Learn completion.
- QR slots are editable, labelled placeholders, not actual codes or invented destinations. The instructor guide explains how to prepare delivery copies with organizer-provided links, module names and real QR images.
- The six decks contain 83 slides. Opening and closing material fits the existing course time boxes; the outline and capstone notes identify the handoffs. Slide-source tests cover QR placeholder rendering and opening/closing content. No new hosted lab execution or publication clearance is claimed.

### Visible background synchronization examples (2026-11-11)

- Added three module 2 slides with YAML examples: `wait: build` before reading a generated artifact, empty-valued `wait-all:` before building after two checks, and `cancel: heartbeat` to stop an endless background loop after tests. Each shows `background: true`, matching step IDs and an explicit synchronization or cancellation point.
- Speaker notes explain prerequisites, failure behavior, the lack of `if` support, why waiting is not server readiness, and why an endless process needs cancellation rather than `wait-all`. The examples stay within the existing 45–53 minute teaching segment; they are not new participant tasks or claimed hosted executions.
- Verified syntax against the referenced GitHub workflow-syntax source. Module 2 now has 26 slides and the course has 73. Updated the instructor inventory and added a slide-source regression for all three visible examples.

### Lab 6 UI-first setup sequence (2026-11-10)

- Replaced participant ruleset-ID bookkeeping with recognizable ruleset names and UI navigation, including end-of-class cleanup. Historical API/run evidence remains unchanged.
- Moved creation of the temporary `lab-06-gates` PR before required-check selection. The lab now explains that a check must run before it appears in the selector, directs participants to its first successful result and reuses the same PR for subsequent experiments. Manual dispatch is explained as an alternative only for workflows that provide that trigger; no trigger was added to this workflow.

### Lab 6 staging as run-and-observe (2026-11-10)

- Made the participant-owned deployment rule the explicit task: create a separate repository branch ruleset, target the exact default branch, select **Require deployments to succeed → lab-staging**, verify saved scope and activate it for the experiment. Observe failed deployment blocking merging and successful deployment removing that specific blocker; do not substitute a similarly named status check, approval or bypass.
- Supplied the completed local staging implementation in the learner workflow. Participants toggle `LAB_STAGING_FAIL`, inspect failed/successful deployment records and observe the deployment rule's merge blocking; they no longer implement server startup, readiness checks or cleanup.
- Updated the lab, setup, example directory guide, instructor guidance, module 3 slide and starter/reference regression expectations. Gate aggregation and central title policy remain implementation exercises. No hosted deployment or policy changes were made.

### Lab 5 runnable stack/queue observation example (2026-11-10)

- Supplied the cancellation policy and `optional-top-layer` report in the learner workflow, matching the completed reference. The lab introduces the report as a message-only example of optional work selected by stack metadata. Participants create the dependent changes and native stack, inspect running/skipped jobs, observe cancellation and configure/use their merge queue rather than implement workflow policy.
- Updated setup, the example directory guide, instructor guidance, module 3 slide and starter/reference regression expectations. This is an intentional runnable observation exercise, like the baseline and event observer; other implementation starters still withhold their target logic.

### Lab 3 readable extension cleanup (2026-11-10)

- Removed the optional dispatch input. Participants either add the stretch steps or leave them out; the completed example includes them without input conditions. The starter provides guidance for adding them rather than an optional failing step.
- Replaced the completed builder's shell exit trap with separate install, download and uninstall steps, and updated the lab's collapsed example and starter guidance. Cleanup uses `always()` together with the installation step's successful outcome, so a failed download still triggers uninstall, while a skipped or failed installation does not remove an existing extension.
- Kept cleanup failure blocking: no `continue-on-error` on uninstall, because a successful image must not retain the extension. A successful cleanup cannot erase a preceding download failure. Hard runner termination can still prevent cleanup. This supersedes the earlier exit-trap implementation notes below, not their historical execution evidence.

### Artificial baseline workload (2026-11-10)

- Lab 1 now downloads the reviewed 559,484,083-byte CodeQL v2.27.4 bundle into a newly created job-temporary directory on every run. It verifies size/checksum, extracts outside the download directory and invokes the downloaded CLI's version command. Starter and reference remain identical observation scaffolds, with no cache and no extra action or permission. Lab 2 caches the same archive; compare matching download/verification/extraction steps, not total job times.
- Added explicitly logged 20-second waits to the app's HTTP test and build before their real checks/packaging. These waits apply to later labs too, remain identical across workflow variants and simulate latency rather than CPU work. No unused large npm dependencies were added. Updated setup, Labs 1–4, outline, instructor guidance and module 1 slides with timing, download-budget and comparison limits.
- Ran the app lint, real HTTP test and build locally: lint took 0.66 seconds; tests took 20.73 seconds and build 20.59 seconds including npm startup. Verified the staged source and runtime dependency. Twenty-two targeted workflow/downloader regressions pass, including fresh-directory downloads of the same manifest.
- Executed the baseline's exact embedded Node download script against the real public release on Windows: 559,484,083 bytes, expected SHA-256, 58,295 ms download and 584 ms verification. Native libarchive read all 40,477 tar entries, including `codeql/codeql`. Temporary archive/output files were removed. This is not a hosted Linux extraction/CLI execution or a classroom speed guarantee; those checks remain outstanding.
- Regenerated the 70 slides with current workload notes; six generator tests pass. No participant workflows were activated or pushed, and publication gates remain blocked.

### Participant-facing lab wording and spacing (2026-11-10)

- Revised setup, Labs 1–9 and end-of-class cleanup to address learners directly. Split timing, prerequisites, access requirements and alternatives into separate paragraphs; replaced uppercase planning markers and audit-style reporting language with readable guidance. Broke long tasks into action-sized paragraphs and added a change-category table to Lab 4.
- Rewrote the collapsed hints and solutions as explanations rather than compressed checklists. Lab 5 now explains the PR dependency, stack positions, optional reporting, cancellation and queue validation separately. Other solutions explain cache results, archive seeding, event selection, failure/timeout behavior, gate decisions, debugging, inventories and attestation claims with short paragraphs and comparison tables.
- Kept the technical exercises, starter/solution separation, participant-repository scope, permissions, policy approvals and workflow-disable/retention instructions. Lab 5 still asks participants to configure their own eligible merge queue and distinguishes it from an ordinary merge. Lab 3 still starts image generation early and resumes later. Lab 6 participant instructions now point to the trainer alternative without including directions for delivering that demonstration; trainer-only scope and approval checks remain in the instructor guide.
- Updated delivery requirements and instructor guidance to distinguish learner prose from author/instructor planning categories, including hints, solutions and cleanup. The separate Lab 5 fixture and slide changes are described below.
- Fifteen workflow/documentation regressions pass. Checked local link targets, balanced collapsed-solution/code blocks and whitespace across the revised Markdown documents. No new hosted runs, resource changes or publication clearance.

### Lab 5 terminology and cancellation window (2026-11-10)

- Standardized on GitHub's bottom/top PR terminology in the lab, starter comments, outline, slides and teaching notes. The bottom PR targets `main`; the top PR builds on it. New instructions use `lab-05-bottom` and `lab-05-top`; historical walkthrough SHAs and run evidence below are unchanged.
- Increased the allowed cancellation delay from 60 to 150 seconds in both starter and completed workflow, retaining the zero default and ten-minute job limit. The lab selects 150 seconds and prepares both local comment commits before either push. Its first push publishes only the earlier commit; the replacement is ready locally when the job reports `Waiting 150 seconds`. Reset/cleanup instructions remain.
- Executed 18 Bash input/boundary cases across both workflow variants, with sleep stubbed: 150 is accepted; larger, negative, empty and noninteger inputs fail. Verified the two exact push commands against a disposable local remote: the replacement stays local after the first push and appears remotely after the second. Temporary test repositories were removed. This is not a new hosted cancellation rehearsal.
- Regenerated the 70 teaching slides with matching notes. Six slide-generator tests and native PowerPoint text/table fit checks pass. Publication gates remain blocked.

### Managed-account lab repository requirement (2026-11-10)

- Setup now requires organization-owned repositories for Enterprise Managed Users and `ghe.com`, rather than treating personal repositories as a possible fallback. Personal repositories and user-owned forks cannot use the GitHub-hosted runners required by these labs. Updated instructor preflight, delivery requirements and a regression check.
- Rechecked GitHub's [managed-account restrictions](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/abilities-and-restrictions-of-managed-user-accounts#github-actions), which explicitly exclude repositories owned by managed user accounts from GitHub-hosted runners. No tenant settings or permissions were changed.

### Trainer demonstrations instead of assumed recordings (2026-11-10)

- Removed claims that recordings or recorded fallback runs are available from participant labs, the outline, instructor guidance and all four slide modules. Participants who cannot complete a step now ask the trainer to demonstrate it. If that is also unavailable, explain the expected behavior and identify what was not demonstrated.
- Trainer preflight now calls for rehearsed demonstrations rather than promised recordings. Lab 3 still starts image generation early; a timely trainer comparison requires an approved image prepared before class, not an assumption that participant images are ready.
- Regenerated the four decks and retained the distinction between participant results, trainer demonstrations and historical walkthrough evidence. Existing historical run IDs and validation records below do not promise classroom recordings.

### Lab 6 reusable change detector (2026-11-10)

- Replaced the custom `tools/changed-files.mjs` detector in both starter and completed gate workflows with reviewed `tj-actions/changed-files@v47.0.6`, reusing the action introduced in Lab 3. Removed the custom runtime script and converted its tests to workflow-contract regressions. The final gate remains learner work in the starter.
- Preserved explicit PR/merge-group base and tested combined SHAs, full checkout history, read-only job permissions and disabled checkout credential persistence. The action uses local Git with initial fetch skipped and diff failures treated as errors. Ordered patterns select all files, exclude Markdown, then re-include `.github/**`. The deletion/type-inclusive selected-file count drives the boolean job output; both sides of renames count, preventing code renamed to Markdown from hiding removed code. A missing count conservatively requests checks; unsuccessful detection still blocks the final gate.
- Updated the lab's shared-workflow and invalid-base/recovery fixtures, plain-English detector explanation, course outline, instructor guidance, delivery standards, action/source register and slide modules 2/3. The invalid-base experiment changes only `base_sha` to 40 zeros in the disposable PR; it does not weaken error handling or edit an action implementation. Historical custom-helper walkthrough evidence below describes the earlier revision, not this implementation.
- Executed the actual upstream bundled action at reviewed commit `9426d40962ed5378910ee2e21d5f8c6fcbf2dd96` on isolated local Git repositories with synthetic PR and merge-group events: 20 cases passed, covering docs, app, lockfile, `.github` Markdown, code/doc deletions, code-to-doc rename, file-type change, empty diff and invalid base failure. Evidence: `.validation/changed-files-v47.0.6/fixture-results.json`. This used local Node 26, not the hosted Node 24 action runtime; temporary repositories and isolated Git configuration were removed. No live tenant workflows or policies were activated.
- Nineteen Node regressions pass. Parsed 34 workflow YAML files, syntax-checked 94 embedded scripts and checked local targets in 23 Markdown files. The unchanged completed gate passed all 90 detection/decision/result combinations. Regenerated the 70 branded slides; six generator tests and native PowerPoint text/table fit checks pass. Fresh hosted-runner rehearsal, generated execution locks and full security/publication gates remain outstanding.

### Lab 2 CodeQL download cache and clearer learner TODOs (2026-11-10)

- Replaced the npm-download-cache exercise with the reviewed CodeQL v2.27.4 Linux x64 bundle, downloaded directly rather than through an installer with built-in caching. Reconfirmed release API metadata: `codeql-bundle-linux64.tar.zst`, 559,484,083 bytes, SHA-256 `da3e952c7fe978a0b6b93e75d9cbabbdf8535667ca0810bd4b2ae37bc840ffee`. Added a reviewed manifest and supplied downloader that validates metadata, verifies cached/downloaded size and digest, separates local filenames by version and cleans failed downloads. Corrupt cached bytes fail explicitly. Only archives are cached; verification, extraction into job-temporary storage and the exact downloaded CLI's version command always run.
- Both Lab 2 starters still withhold restore/save implementation. Completed references use OS/architecture/tool/epoch/manifest-hash keys; only trusted main saves after a successful smoke test and non-exact lookup. PR is restore-only. Trigger fixtures are now helper comments for exact repeats, manifest note-only edits for compatible partial reuse and consistent epoch changes for misses. Updated lab, directory guide, outline, instructor guidance, release reference and module 1 slides. No database, CodeQL scan/upload or additional analysis permissions are required.
- Expanded TODO comments across all 14 implementation starters into concrete learner actions, placement guidance, preserved boundaries and observable outcomes. The timeout starter and Lab 4 now explain a two-minute wait stopped by a one-minute step limit within the unchanged three-minute job budget, distinguishing a real timeout from the placeholder's immediate error. The directory guide explains replacing whole placeholders, and delivery requirements record the plain-English authoring standard. Completed workflow logic remains separate.
- Eighteen Node tests pass, including small-byte CodeQL download/reuse/version-change/corruption/failure fixtures and timeout explanation checks. Parsed all 34 workflow YAML files, syntax-checked 96 embedded scripts and checked local links in 23 Markdown documents. Regenerated the four branded decks (70 slides); six generator tests and native PowerPoint text/table fit checks pass.
- The new 559 MB bundle was not downloaded/executed in this update, and the revised cache exercise has not been run or timed on a hosted runner. Unit fixtures do not establish its extraction/runtime behavior, cache transfer performance or classroom timing. Historical npm run evidence below belongs to the previous design, not this CodeQL revision. No fresh full security scan, tenant workflow activation, paid image provisioning, commit or push was performed; publication gates remain blocked.

### Learner starter / completed solution split (2026-11-10)

- At the owner's request, preserved the 17 completed workflow references in `solutions/workflows` and converted implementation exercises under `examples/workflows` into learner starting points. Baseline, broad issue observer and minimal emulator fixture intentionally remain identical measurement/demo scaffolding; the other 14 differ. Directory guides identify supplied scaffolding and learner-owned work.
- Removed task-specific solved cache operations, Docker/archive seeding, filtered activities, parallel/matrix checks, step timeout, cancellation/stack selection, aggregator/policy/deployment logic, diagnostic solution, dependency submission and release evidence/verification/promotion from starters. Preserved security boundaries and bounded scaffolding. Fourteen incomplete implementation steps explicitly fail; the debug starter fails on its intentional path error. Normal application validation and read-only image assertions remain legitimate scaffolding, not claims that an unfinished extension task was completed.
- Updated setup and Labs 2-9 to name the implementation work and taught/linked references before activation; completed workflow links appear only inside collapsed lab solutions. Updated outline, delivery/instructor guidance, version inventory and all teaching decks; solution excerpts are labeled. Do not enforce rules against unfinished gates or publish an image/release by deleting failure placeholders. Prior live walkthrough evidence used completed checkpoints, not the revised starter exercises. Fresh learner/timed tenant rehearsal remains outstanding; existing time boxes are targets, not verified delivery durations.
- Eleven Node tests pass, covering starter/reference pairing, withheld target logic, root permissions, trigger boundaries, archive extension lifecycle reference and collapsed solution links, plus the impact helper. Six slide-generator tests pass. Parsed all 34 YAML variants, syntax-checked 94 embedded shell/Python steps and verified local Markdown file targets. Executed all 14 incomplete-step failures and the debug check; none reported success. Executed the completed aggregator against all 90 detection/decision/result combinations, accepting only explicit valid evidence.
- Regenerated all 70 slides from the original branded template and passed native PowerPoint text/table fit checks after correcting a crowded release slide. Current manifest/render hashes supersede earlier decks.
- Fresh `zizmor 1.32.0 --strict-collection --offline --format json` covered all 34 explicit workflow files; JSON retained at `.validation/zizmor-starters-solutions.json`. Exit 14 reports 69 `unpinned-uses` findings for readable release tags under the course's separate execution-lock policy. No findings were suppressed or per-file SHA pins substituted. This does not verify installed generated locks, online dependency behavior, all embedded examples/actions or CodeQL coverage; native parallel-step support is marked experimental by the scanner. Full publication validation remains blocked, and no new live workflows, paid capacity or policies were activated for this split.

### Course-source update and owner cleanup (2026-11-10)

- Transferred walkthrough findings, corrected labs, inert workflow examples, outline/instructor guidance, Markdown slides and related regression expectations into `D:\actions-advanced`. No participant-installed `.github/workflows`, execution lockfile, solved `app/package.json` changes or disposable PR fixtures were copied; learners still complete those steps themselves.
- Runtime evidence below belongs to [xebia/jessehouwing-actions-advanced-walkthrough](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough), not to executions in this course-source repository. Run IDs and resource IDs identify that rehearsal only; they are not values participants should reuse.
- The owner reported paid-runner cleanup. Inventory confirms runners `11` and `12` are absent. Observed image `6325` progress through `ImageDefinitionDeleting` from 150 GB to 75 GB, then disappear from the custom-image inventory. The empty restricted runner group `7` remains (zero runners); this is not active compute. No course runs are in progress.
- All walkthrough course workflows are disabled, and only unrelated GitHub-managed Dependency Graph remains active. Owner-selected organization Actions sharing remains enabled. Earlier checkpoints below that say sharing was disabled or cleanup was awaiting approval are historical and superseded by this update and the successful central-enforcement retry.

### Lab 6 central enforcement retry: verified (2026-11-10)

- After the owner changed source Actions sharing to `organization`, GitHub accepted organization ruleset `26981869`. Verified its exact single-repository selection (`1453025124`), branch `refs/heads/main`, empty bypass list and source `.github/workflows/06-central-required.yml` at `refs/heads/main` before activation.
- Disposable PR [xebia/jessehouwing-actions-advanced-walkthrough#8](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough/pull/8) used an intentionally overlong title. Centrally required run `42902966932` failed at head `29af7e1c16665d3150c1d0f4e68a24a81572b99a` with `Use a nonempty PR title of at most 120 characters`; the PR was `blocked`. The effective branch rule identified organization ruleset `26981869`, not a repository-local required status check.
- Shortened the title and deleted the PR-local workflow copy only in the disposable branch, regenerating its lockfile. Required run `42903119973` still executed the selected source from main and passed at head `d8cdb2d6bade23112605c16b8abe500d9dbe142e`; PR merge state became `clean`. This distinguishes enforced source-workflow execution from optional local workflow reuse. The local workflow ID was `413769425`, while the centrally required run used workflow ID `413827609`.
- `gh run watch/view` could not resolve the central run's workflow ID (HTTP 404). Direct REST run/jobs/logs endpoints provided successful evidence; this CLI lookup limitation did not prevent policy enforcement. Logs for both results are retained in session artifacts.
- Closed that PR without merging the workflow deletion, disabled and removed only the test ruleset, then disabled the local course workflow again. Effective branch rules are empty. The owner's new `organization` sharing setting was preserved, not silently reverted. This supersedes the earlier blocked central-enforcement state; a permanently missing-result fixture was not exercised.

### Walkthrough acceptance assessment (2026-11-10)

| Requested verification | Result and remaining limit |
| --- | --- |
| Lab correctness | Labs 0-9 exercised live, including deliberate failures and recovery. Lab 6 central enforcement passed its owner-enabled retry above, including failure blocking and source execution without a PR-local workflow. A permanent missing-result fixture was not exercised. Lab 10 cleanup verified: owner-removed paid runners and custom image are absent; all course workflows are disabled. |
| Enough information at that point | Replaced unspecified failure/lockfile/deployment/release fixtures with concrete steps using the supplied application and taught workflow concepts; linked image internals, required workflow eligibility, dependency submission and attestation verification references. Optional local emulator demonstrations remain demonstrations, not prerequisites. |
| Clear instructions | Added first/second PR names, explicit queue-policy setup, bounded cancellation, independent gate fixtures, exact corrected-revision debugging, real before/after inventories, exact signer/digest constraints, image-version propagation and diagnostic cache-hit proof. |
| Participant repository scope | All live mutations and runs used `xebia/jessehouwing-actions-advanced-walkthrough`. Dedicated runner group selected only that repository. Organization rule selected only repository ID `1453025124` and `main`. Setup, outline and instructor/slide guidance now distinguish participant exercises from labeled fallback demonstrations. No source sharing or shared policy was broadened. |
| Per-lab workflow cleanup | Each execution lab names disabling its workflows or explains retention for the next comparison. Lab 1 is retained through Labs 2/3, then disabled. Required rules are restored/removed before disabling their workflows. All course workflows are currently disabled; unrelated Dependency Graph is retained. |

Corrections from the walkthrough have now been applied to this course source at the owner's request. The presentation review and renewed deck checks below supersede the earlier stale-deck warning; historical scanner evidence does not establish current security validation.

### Presentation review against the walkthrough (2026-11-10)

- Reviewed all four Markdown modules against the participant instructions and recorded walkthrough evidence. Replaced instructor-owned baseline/cache/release prompts with participant setup, concrete compatible cache fixtures and the reproducible debugging typo. Debug reruns retain the failing revision; recovery requires a new run at the corrected revision.
- Clarified custom-image readiness versus runner propagation, offline seed assertions and diagnostic archive-hit evidence. Neither the differing image/baseline workloads nor tiny parallel checks establish a general speedup or billing saving. Clarified the bounded Lab 5 cancellation fixture and actual base/combined-SHA evidence.
- Separated the Lab 4 impact-selection discussion from the live Lab 6 detector. Distinguished repository deployment rules from organization central-workflow enforcement, explicit owner/policy authorization from technical roles, and trainer alternatives when policy prevents participant changes. Lab 6 revisits Lab 5 queue evidence; it does not claim an additional queue merge with all Lab 6 gates installed. Missing-result predictions remain conceptual, not claimed walkthrough observations.
- Added graph-versus-staged-npm inventory limitations, duplicate-entry caveats and explicit verified-lock guidance. Distinguished the signed inner archive from the transport ZIP and local health-checked promotion from external deployment. Updated per-lab disable/retention and policy-first cleanup notes.
- Made Lab 3 explicitly non-blocking at the owner's request: launch the builder, continue to Lab 4, then check back at a later break and before cleanup. The lab, outline, instructor guide and slide prompts identify the resume point, recorded-evidence fallback and owner-approved cleanup/follow-up deadline when images remain unavailable.
- Regenerated all four decks (16/23/17/14 slides, 70 total) from the original `Guidance_PPTX.pptx`, found in the owner's downloaded template directory. Its SHA-256 remains `518640c93e437c317222471d3b8af77fb1dc49bee872e83779e8b10ab674a791`. `slides/powerpoint/manifest.json` records current source/deck/template hashes. Generator checks confirm matching titles, bullets, supporting material and notes with template layouts preserved.
- Native PowerPoint rendering and text/table bounds checks pass for all 70 slides after shortening a crowded policy slide; refreshed render evidence is under `.validation/powerpoint-render`. Six slide-generator tests and five workflow regression tests pass. No fresh full security/static scan, accessibility audit or timed classroom delivery rehearsal was performed; those publication gates remain open. Changes remain local and uncommitted.

### Lab 3 archive-cache extension update (2026-11-10)

- Replaced manual `curl`/archive-path construction with `jessehouwing/gh-actions-archive-cache`, pinned to published `v0.0.2` (release commit `e5811f9a420c3cef4d0c5d7de2723d8d2488ddcb`). The builder installs the extension, downloads the exact reviewed changed-files commit in Linux `tar.gz` format, then uninstalls via an exit trap before snapshotting. Download failure is preserved; uninstall failure also fails the step. The archives remain for the consumer, which does not need the extension.
- Kept root permissions empty, added job `contents: read` and step-only `GH_TOKEN`; no saved authentication or new persistent environment configuration is required. Documented cache access, existing-extension ownership, reviewed-lockfile import, host-specific credentials and hard-cancellation limitations. Updated the lab, builder, outline, instructor guidance, release/source registers and presentation prompt.
- Windows CLI verification with a temporary configuration and dedicated cache installed `v0.0.2`, downloaded the exact `9426d40962ed5378910ee2e21d5f8c6fcbf2dd96` archive using explicit `tar.gz`, repeated with one cached result and zero downloads, uninstalled, and verified the archive remained. Temporary configuration did not isolate Windows extension storage; restored and verified the user's pre-existing `v0.0.2` installation afterward. JSON evidence is in session artifacts. Executed the builder's Bash body with stubbed commands for success, download failure and uninstall failure; all invoked uninstall and returned the expected exit status.
- Six workflow regression tests and six slide-generator tests pass. Regenerated all four decks and passed native PowerPoint text/table fit checks. This update did not provision another paid runner or rebuild a live custom image; prior image/runner evidence above used the manual downloader. Linux hosted snapshot integration with the extension still needs a fresh authorized rehearsal, and existing publication gates remain open.

### Walkthrough execution: setup and Labs 1-2 (2026-11-10)

- Setup used the disposable organization-owned walkthrough repository, default branch `main`, with Actions, issues and administrator access available. Installed only each selected workflow; no blanket example activation or source-repository execution was used.
- Baseline [run 42875072607](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough/actions/runs/42875072607) passed at `48be2e04f583d3d9ec4284f5448d762b7fece78a`; its checks job took seven seconds. This tiny app does not establish a general performance or billing claim.
- Lab 2 passed cold miss `42875628733`, exact hit `42875879254`, compatible partial hit `42876237924`, new-epoch miss `42876461474`, and PR restore-only hit `42876703236`. Each still ran `npm ci --ignore-scripts`; the PR workflow had no save action or setup-node cache writer.
- Corrected optional trigger filters to `.github/workflows/actions.lock`, not root `actions.lock`. A harmless app change triggers a repeat run without changing its key; an unrelated docs-only change or empty push does not match these filters. Instructions now provide a whitespace-only lockfile fixture and fresh epoch values instead of an unspecified instructor checkpoint.
- Clarified that compatible default-branch caches can be restored by other branches, but a branch-scoped save cannot overwrite the default branch's cache. Merely switching branches does not guarantee a cache miss. The trusted writer remains restricted to main; no live poisoning or unsafe write override was exercised.
- Closed disposable PRs and disabled both cache workflows after evidence collection; retained the baseline only through the Lab 3 comparison, then disabled it too.

### Walkthrough execution: Lab 3 final comparison (2026-11-10)

- Builder run `42889687562` created seeded image `6325`, version `1.1.0`, at 19:53:47 UTC. It became Ready at approximately 20:43:21 UTC with size 75 GB, roughly 50 minutes later; workflow success was not image readiness.
- Consumer `latest` initially ran older `1.0.0` and correctly failed its offline Docker assertion in `42898082107`. Explicitly pinned course runner `12` to `1.1.0`; immediate runs `42898254516` and `42898370261` still reported `1.0.0` despite the control plane reporting the selected version/Ready. After a bounded propagation wait, run `42898843719` actually reported `1.1.0` and passed. Instructions now require selecting and verifying the actual job image version, without papering over a miss by downloading in the consumer.
- Successful consumer found `picocolors-1.1.1.tgz` in the npm download cache; host Node was `v24.22.2`. Docker image digest `sha256:438603bbb5cda404b9416f0b5c8026f61501ab911760d861ec28c36b5d675725` matched the builder, and `docker run --pull=never` returned container Node `v26.13.0`. No Docker pull fallback was allowed.
- Debug attempt 2 of `42898843719` passed and explicitly logged copying `/opt/actionarchivecache/tj-actions_changed-files/9426d40962ed5378910ee2e21d5f8c6fcbf2dd96.tar.gz`, plus the pre-existing checkout archive. This proves exact seeded archive reuse, not merely an environment-variable presence. Ordinary setup still prints `Download action repository` on these hits; instructions now explain this distinction and remaining ref-resolution service calls.
- Original Lab 1 checks job took 7 seconds; this consumer's inspection job took 26 seconds on attempt 1 and 13 seconds on debug attempt 2, excluding provisioning waits. They do different work, so no end-to-end speedup is claimed. Verified benefits are avoiding the Docker pull/action archive transfer and retaining the npm seed; image generation, propagation, storage, updates and drift remain costs.
- Disabled Lab 1 baseline and both Lab 3 workflows after comparison. All installed course workflows are now disabled; unrelated GitHub-managed Dependency Graph remains active. No queued/in-progress runs remain.
- At comparison completion, paid-resource deprovisioning remained owner-controlled: runners `11`/`12`, image `6325` (versions `1.0.0`/`1.1.0`) and group `7` were retained. The owner cleanup update above supersedes that state.

### Walkthrough execution: Lab 10 cleanup checkpoint (2026-11-10)

This was the pre-readiness checkpoint; the Lab 3 final comparison and owner cleanup update above supersede its pending-image, enabled-workflow and paid-resource retention state.

- No course workflow runs, issues or PRs remain open/running at this checkpoint. Temporary Lab 6 rulesets and both Lab 6/9 environments have been removed. The course-only Lab 5 queue ruleset `26977275` is disabled and retained for inspection; no active rules remain on `main`. Organization Actions sharing remains `none`.
- Labs 2 and 4-9 workflows are disabled. The Lab 1 baseline and Lab 3 builder/consumer remain enabled only until the outstanding image comparison completes. Unrelated GitHub-managed `Dependency Graph` automation was preserved.
- Deliberately retained three disposable remote branches, three identified Lab 2 npm cache entries (about 15 KiB total), and short-retention release artifacts as evidence; no blanket repository/cache/artifact deletion was performed. No persistent local server or tampered artifact copy remains.
- **Outstanding Lab 3 / paid cleanup:** dedicated runner IDs `11` (image generation) and `12` (consumer), image ID `6325` and restricted runner group `7` remain. Image `1.0.0` is Ready (75 GB); `1.1.0`, containing the Docker/action seeds, is still replicating. Group `7` selects exactly this participant repository and disallows public repositories. Do not dispatch the comparison against the older image.
- Owner approval is still needed for deprovisioning dedicated paid runners and image/storage after the comparison. Disabling workflows alone does not remove retained-image storage charges. No paid resource has been deleted or shared policy changed.

### Walkthrough execution: Lab 9 (2026-11-10)

- Run `42896111051` at `ec030556bacb81aa0efea0c540f5f9cf42640c30` passed both build (15 seconds) and local promotion (23 seconds), including lint, tests, build, staged npm inventory, provenance/SBOM issuance and verification.
- Original archive, downloaded archive and promotion-boundary SHA-256 all match: `684cfee348fbbd28e2039c79f773114c4f3f72e06898cfefa8bf139fdffb1d96`. This is the inner `application.tgz` subject, not the upload-artifact transport ZIP digest (`6f256caf4f40cb55a48a6eaa01e0a97fafda9e51a4311479cb101ab3d06248ee`).
- Verified both in-job and independently with local `gh 2.102.1`, constraining signer to `xebia/jessehouwing-actions-advanced-walkthrough/.github/workflows/09-release.yml`, source ref `refs/heads/main`, exact run commit and hosted runners. Saved successful verification JSON for SLSA provenance and SPDX SBOM; actual statement types are `https://slsa.dev/provenance/v1` and `https://spdx.dev/Document/v2.3`, with the same subject digest.
- Both in-job negative tests and independent downloaded-copy tests returned nonzero: altered bytes produced a lookup for their different digest (HTTP 404), while unchanged original bytes with `not-the-signer.yml` failed verification. The immediately preceding correctly constrained original verifications succeeded, so these were not authentication/network outages. Removed the local altered copy; retained original archive/SBOM and verification evidence.
- Promotion extracted the downloaded archive without rebuilding, started its app, validated `/health` and stopped the process via the job trap. No external cloud target, production environment or persistent local service was used.
- Instructions now supply the exact participant setup, default-branch guard, identity expectations, matching digest evidence and explicit workflow-disabling cleanup instead of unspecified instructor-prepared assets.
- Disabled `Lab 09 verified promotion` and removed only the course-owned `lab-release` environment after completion. Uploaded artifacts have one-day retention; no shared attestations, releases or other artifacts were removed.

### Walkthrough execution: Lab 8 (2026-11-10)

- Exported the participant repository's before graph: 15 SPDX package entries, including `picocolors` and workflow action version metadata.
- Installed the trusted-branch-only submission example with `contents: write` limited to its job and explicit `report-transitive-as-direct=false`, `actions-lock-version=v0.4.1`. Run `42895821255` at `faecb5a7f516a4bbbabc644f2722a6ffa277cd7f` passed, logging `Using verified .github/workflows/actions.lock to resolve dependencies`, 32 action dependencies found and 46 dependencies successfully submitted.
- Immediate after export contained 56 package entries, including both checkout `7.0.1` and locked SHA `3d3c42e5aac5ba805825da76410c181273ba90b1`, as well as submission action tag/SHA. Entries can repeat across detector manifests; counts are not counts of unique shipped components. No custom fork/upstream mapping was configured or claimed verified.
- Built the app locally after restoring its missing dependency with `npm ci --ignore-scripts`. The staged npm SPDX inventory contains only `actions-advanced-lab@1.0.0` and `picocolors@1.1.1`, not checkout/setup-node/Python tooling. It inventories staged npm packages, not every file, runtime or OS dependency.
- Saved before/after graph JSON and staged SPDX JSON in session artifacts. Replaced unspecified instructor snapshots with participant export/build instructions and documented graph indexing and duplicate-entry caveats. No vulnerable action was executed.
- Disabled `Lab 08 trusted dependency submission` afterward; preserved unrelated `Dependency Graph` automation and submitted graph data.

### Walkthrough execution: Lab 7 (2026-11-10)

- The original checkpoint always passed and referred to an unspecified instructor failure. Instructions now supply an exact participant-owned path typo, bounded observations, debug rerun command and correction; no new tool or privileged access is needed.
- Installed the workflow with intentional `app/src/serve.js` typo at `2f2e4730ed7e5b62ecdcdf25ba7cd926d2fedfc0`. Run `42895431160`, attempt 1 failed with exit 1 while the bounded listing showed actual path `app/src/server.js`.
- Reran the same revision with `gh run rerun 42895431160 --debug`. Attempt 2 emitted `Expected source directory is app/src` and failed at the same typo; enabling diagnostics did not fix the code.
- Corrected only the checked path at `57a90af35188a9b1197bcd377389f27ca9424b72`. New run `42895568323` succeeded. No timeout, cancellation, broad environment dump or real secret input was involved.
- Disabled `Lab 07 targeted diagnostics` after the corrected run. Optional instructor demonstrations of `act`/`github/local-action` were not performed; no local service was started for this lab.

### Walkthrough execution: Lab 6 (2026-11-10)

- Used only participant repository PR [xebia/jessehouwing-actions-advanced-walkthrough#7](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough/pull/7); closed it without merging any fixture. Organization ruleset `26977841` explicitly selected repository ID `1453025124` and `refs/heads/main`, with no bypass actors. The `required` check used GitHub Actions source `15368`.
- Docs-only run `42894121656`: impact success, application skipped, required success. Application-change run `42894243643` and shared-input-only run `42894394399`: all three success. The application fixture was restored before the shared-input experiment so the PR's full diff isolated shared inputs.
- Failed detector run `42894544346`: impact failure, application skipped, required failure; PR merge state `BLOCKED`. Repair run `42894748744` passed all three jobs. No missing output or failed detector was treated as a successful docs-only decision.
- Found a setup error: adding `required_deployments` for `lab-staging` to the organization ruleset returned HTTP 422, `Invalid deployment environments`. The identical environment requirement was accepted in repository ruleset `26978044`. Instructions now distinguish repository-local checks/deployments from organization-required workflows.
- With only the repository deployment rule active, staging run `42894748582` attempt 1 failed intentionally while application and final checks passed. Deployment `7693308986` at head `b3b0af19b15586e457aa0820ea14d0174268e11b` recorded failure. Resetting `LAB_STAGING_FAIL=false` and rerunning the same workflow succeeded: deployment `7693329915` recorded success after building, starting and health-checking the local server. PR merge state changed from `UNSTABLE` to `CLEAN`; no merge attempt or bypass was performed.
- **Central enforcement remains unverified:** the organization is Enterprise, but saving the workflow rule returned HTTP 422 because this source repository has Actions sharing disabled (`access_level=none`). Owner approval to temporarily broaden organization access was requested but unavailable; access was not changed. The successful local `central-policy` runs do not establish organization-required workflow enforcement.
- Replaced unspecified instructor fixtures with reproducible docs/application/shared/detection/staging cases, documented source-sharing eligibility, and reused actual Lab 5 combined-revision queue evidence instead of claiming another prepared run exists.
- Cleanup: closed that PR, disabled and removed only the two recorded course rulesets, reset the staging failure variable, removed the course-only environment after all jobs completed, and disabled all three Lab 6 workflows. Effective `main` rules are empty; source Actions sharing remained disabled at this earlier checkpoint.

### Walkthrough execution: Lab 5 (2026-11-10)

- Created native stack 6 in the participant repository, ordered PRs [xebia/jessehouwing-actions-advanced-walkthrough#4](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough/pull/4) and [xebia/jessehouwing-actions-advanced-walkthrough#5](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough/pull/5), rather than treating dependent PR bases as native stack registration. Both initial layer validations passed.
- Repository ruleset `26977275` targeted only `refs/heads/main`, required PRs and `validate` from GitHub Actions app `15368`, and required an ALLGREEN merge queue with build/merge limits 1 and a 20-minute check timeout. No bypass actors or pre-existing protections were changed.
- Cancellation run `42892808720` was observed inside its bounded delay before a replacement push cancelled it. Replacement `42892884357` passed both validation and the top-only optional job; the bottom PR's successful run remained intact. The delay variable was reset to `0`.
- Enqueued the native stack through the second PR's asynchronous merge API with the exact head `4a2968506ce2e18fcba5d8e01d73a0c711bd68d4`, explicitly selecting `merge_queue`, not direct merge.
- Queue run `42893339859` passed at `45dab6c22cec28651bf969409bff8b29ea592ccc`, based on `e0a947cc1e9e7379dd7b8382b17beda641324ca6`. Queue run `42893434675` passed at combined top revision `08e9140edab2b55511f5a00ec25c3819b0de5f08`, based on the first queue revision. Both PRs were confirmed merged at 20:15:44 UTC; `main` resolved to the combined top revision.
- The lab now teaches participant-owned merge queue setup, stable required-check selection, concrete layer changes, and a bounded cancellation fixture. Queue size 1 did not prevent separate merge-group CI builds.
- After verifying the stack was fully merged, disabled only the course-created ruleset (retained for inspection), confirmed no active rules remained on `main`, and disabled `Lab 05 stack and queue`. This avoids leaving an impossible required check behind a disabled workflow.

### Walkthrough execution: Lab 4 (2026-11-10)

Executed in `xebia/jessehouwing-actions-advanced-walkthrough`, not the course source repository:

- Issue [xebia/jessehouwing-actions-advanced-walkthrough#3](https://github.com/xebia/jessehouwing-actions-advanced-walkthrough/issues/3): opening triggered both workflows (runs `42890381020`, `42890381228`); editing triggered both (`42890429320`, `42890429493`); labeling triggered only broad issues (`42890468422`); commenting created no issues run. Logs contain only event/activity metadata. The disposable issue is closed.
- Run `42890556627`: sequential, native parallel steps, and separate-job lint/test/build all passed. Sequential and shared-runner jobs each took 10 seconds; separate lint/test/build used 7 + 9 + 8 = 24 runner-seconds and a longer critical path. No speedup is claimed for this small application.
- Run `42890667861`: deliberate test failures failed both parallel implementations and the workflow. The shared-runner build step and dependent separate build job were skipped; an unrelated sequential job remained successful.
- Run `42890764476`: the one-minute step timeout fired within the three-minute job budget, failed the workflow, and emitted the explicit timeout annotation. Teardown overhead meant the whole job took 75 seconds.
- Fixed missing sequential/failure fixtures, supplied concrete impact-map discussion inputs, corrected the timeout budget, and made cleanup name all four workflows. All four live Lab 4 workflows are `disabled_manually`.
- The existing publication/security gates below are separate and are not cleared by these runtime experiments.

### Historical pre-walkthrough publication inventory

The scanner and deck results below describe their recorded earlier snapshots, not the current walkthrough. The walkthrough now has 17 example workflows, 16 installed/locked course workflows, and a generated lockfile verified successfully. Historical statements about 16 examples, missing locks or outstanding tenant runs are retained as dated evidence, not current-state assertions. Source changes require fresh publication validation.

- Runnable examples in the historical snapshot: 16 workflow files in `examples/workflows/`.
- Local action: `actions/hello/action.yml`; its JavaScript implementation, the `tools/` scripts, and application JavaScript are included in the CodeQL coverage below.
- No reusable workflow files or separate runnable solution workflow variants were found. Hidden solutions in the labs are references to the example workflows, not additional workflow files.
- All 16 workflow files now use file-level `permissions: {}`. Jobs that check out the repository request `contents: read` at job scope; jobs without that need retain no token permissions.

## zizmor

- Version: `1.32.0`.
- Command: `zizmor --strict-collection --format json` with every file under `examples/workflows/*.yml` and `actions/hello/action.yml` passed as an explicit input.
- Current result after upgrading all example action references to the latest full release tags: **31 `unpinned-uses` findings**, exit code 14, retained in `.validation/zizmor-latest-releases.json`. The earlier empty result applied to SHA-pinned examples, not current files. No suppressions were added. A generated/reviewed action lock remains a publication requirement; confirm scanner support for that lockfile before claiming these findings resolved.
- Limitation: zizmor emitted a warning that its support for native parallel steps in `04-parallel.yml` is experimental. It was not suppressed. Verify that syntax against the target GitHub host/runner and retain runtime evidence.

## CodeQL

- **Freshness warning:** subsequent trigger edits and version-tag changes across the example workflows are not covered by the historical scan described below. A later source snapshot does not cover edits made after it was created. Revalidate the final workflow contents before publication.
- CodeQL is available through the installed `gh codeql` extension: CLI `2.27.1`. No scanner installation or update was needed.
- Both security-extended analyses completed successfully with **zero findings** and no warning/error-level SARIF execution notifications. No suppressions were added.
- Actions query pack: `codeql/actions-queries@0.6.39`, 24 queries. Extraction confirms all 16 current workflows plus `actions/hello/action.yml`: 17 Actions files / 581 lines.
- JavaScript query pack: `codeql/javascript-queries@2.5.0`, 105 queries. Extraction confirms all 8 authored JavaScript files / 114 lines: both `actions/hello/src/` files, all three `tools/*.mjs` files, and the application's source, build script, and test.
- Source snapshot: `.validation/gh-codeql-20261110/source`. All workflow examples were materialized under `.github/workflows` so the Actions extractor would discover them. The local action, helpers, application source/tests/build script and package manifests were copied without generated output or `node_modules`. All 29 snapshot files were verified byte-for-byte against the current originals after scanning.
- Evidence retained under `.validation/gh-codeql-20261110/`: `actions.sarif`, `javascript.sarif`, and `databases/` containing extractor logs, query results and `baseline-info.json` coverage inventories. This ignored evidence is local; preserve it with the release evidence before publishing.
- The previous CodeQL `2.27.4` Actions-only snapshot is superseded by this current, broader scan; it is not the evidence for these results.

Commands run from the course root after materializing the snapshot:

```powershell
gh codeql database create .validation\gh-codeql-20261110\databases --db-cluster --language=actions,javascript --source-root=.validation\gh-codeql-20261110\source --build-mode=none --threads=2
gh codeql database analyze .validation\gh-codeql-20261110\databases\actions codeql/actions-queries@0.6.39:codeql-suites/actions-security-extended.qls --format=sarifv2.1.0 --output=.validation\gh-codeql-20261110\actions.sarif --threads=2 --sarif-category=course-actions
gh codeql database analyze .validation\gh-codeql-20261110\databases\javascript codeql/javascript-queries@2.5.0:codeql-suites/javascript-security-extended.qls --format=sarifv2.1.0 --output=.validation\gh-codeql-20261110\javascript.sarif --threads=2 --sarif-category=course-javascript
```

Static results do not establish target-tenant runtime behavior or complete manual trust-boundary review. Those separate release gates remain outstanding.

## Action versions and lockfile

The live-refreshed [action version lookup](ACTION-VERSIONS.md) includes all eight used entry points from seven repositories, release publication times and resolved release-tag commits. Queried 2026-11-10 at 17:55 UTC. All workflow and slide action references have been upgraded to these full release tags.

Latest release pages were checked on 2026-11-10:

| Action | Latest stable release checked | Example's current version tag |
|---|---|---|
| `actions/checkout` | `v7.0.1` | `v7.0.1` |
| `actions/setup-node` | `v7.1.0` | `v7.1.0` |
| `actions/cache` | `v6.1.0` | `v6.1.0` |
| `actions/attest` | `v4.2.2` | `v4.2.2` |
| `actions/upload-artifact` | `v7.0.2` | `v7.0.2` |
| `actions/download-artifact` | `v8.0.2` | `v8.0.2` |
| `jessehouwing/actions-dependency-submission` | `v2.0.2` | `v2.0.2` |

Sources: [checkout](https://github.com/actions/checkout/releases/latest), [setup-node](https://github.com/actions/setup-node/releases/latest), [cache](https://github.com/actions/cache/releases/latest), [attest](https://github.com/actions/attest/releases/latest), [upload-artifact](https://github.com/actions/upload-artifact/releases/latest), [download-artifact](https://github.com/actions/download-artifact/releases/latest).

All external action references now use the full latest release tags recorded above, including the checkout v7 and dependency-submission v2 major upgrades. Reviewed their action metadata and relevant release/README guidance: both use Node 24, checkout's new privileged fork-code safeguard needs no opt-out for these examples, and submission retains explicit input values. The dependency lab and stable research links now reference v2.0.2. Target-runner/tenant execution is still required. Tags are mutable and do not by themselves provide immutable dependencies. **Blocked:** there is no generated `actions.lock`, and the current scanner reports unpinned references. Before publication, verify the newest host-supported action references and generate/review the repository lockfile with `gh actions-lock`; do not hand-edit it. Lockfile support is a preview and must be checked for the target host.

## PowerPoint delivery

- The user supplied `Guidance_PPTX.pptx` as the accessible branding source, replacing the previously inaccessible Downloads template. Inspected its actual 51 guidance/sample slides, one slide master, 58 layouts, widescreen dimensions, theme colors, Arial typography and notes master before generation.
- Generated one deck per module under `slides/powerpoint/`: `01-caching.pptx` (16 slides), `02-execution.pptx` (23), `03-policy.pptx` (17), and `04-debug-trust.pptx` (14). All 70 slides have speaker notes copied from their Markdown source. Sample teaching slides were removed; the original master/layout XML, logo, separators and copyright footer were retained. Content uses the actual `Title Content/White` and `Title Content/Dark` layouts.
- Reproducible generator: `tools/build_slides.py`; authoring/scanner dependencies: root `requirements.txt`, with Python 3.13.14 in `.python-version` and a forwarding compatibility file at `tools/requirements-pptx.txt`. See the [instructor guide](INSTRUCTOR-GUIDE.md#teaching-decks-and-updates) for regeneration. `slides/powerpoint/manifest.json` retains template, source and output SHA-256 hashes, slide/notes counts and layout measurements.
- Supporting material accompanies 37 slides: nine editable flow diagrams, fourteen comparison/decision tables and fourteen YAML/shell/worked-example panels. Actual workflow excerpts are identified and intentionally incomplete where labeled; numerical examples and predicted outcomes are explicitly illustrative, not fabricated runtime evidence. Module 2 now includes checkout lifecycle/scope at minutes 1-8 and two artifact packaging/selection/extraction patterns at 8-12, with event teaching at 12-20. Its nine added slides preserve all labs, the 105-minute module and 420-minute teaching day. Checkout implementation and artifact inputs/examples were inspected against the references recorded in REFERENCES.md. New snippets have preflight prerequisites; they are not installed runnable workflows, measured speedups, or new scanner-run evidence.
- Structural checks reopened every output and confirmed exact title/bullet/notes/example parity with Markdown (display formatting removed and visual line breaks normalized), unchanged masters/layouts/dimensions, inherited title margins and no off-slide shapes. Six focused generator tests cover parsing, code indentation, notes preservation, malformed material rejection, editable flow rendering and oversized-code rejection.
- Reviewed all 70 slides for plain English across titles, teaching points, captions, tables, diagrams and code comments. Replaced unexplained lab shorthand with concrete actions. Added visible first-use explanations for runner, PR, baseline, runner-minutes, cache key/lockfile/hash, exact/partial/miss, prewarming, sparse checkout, submodules/LFS, artifacts, event activities, matrix, stack, merge queue, ruleset, SHA, digest, SBOM, attestation, provenance and promotion. Lab 2 now separates the prepared lockfile change from the cache-version change and explains cold runs. Technical instructor notes and references remain available; the Lab 2 notes were expanded to support the clearer steps. This is an editorial review, not evidence of comprehension testing with learners.
- Native PowerPoint `16.0` opened and rendered all 70 slides at 1600 x 900. `tools/validate_slides.ps1` checks native bounding width/height within a 2-point tolerance, including table cells, and checks example shapes against the footer region and slide bounds. Its report records each deck's SHA-256. Corrected bold-font wrapping, code height and native table expansion before retaining final renders.
- The OS/runtime matrix slide illustrates six compatibility jobs with `max-parallel: 3` and `fail-fast: false`, within the existing minutes 53-60 teaching segment. Runtime versions require preflight; this is not a recorded six-platform run or an installed workflow. The proposed scatter/gather optional lab remains unimplemented.
- Evidence: `.validation/powerpoint-render/native-validation.json`, current module PNG render folders, and exported template guidance slides. Earlier contact sheets predate the latest wording/matrix slide; use the current PNGs and hash-linked report for this revision. This ignored evidence is local; preserve it with release evidence.
- Accessibility essentials checked: semantic title and notes placeholders, title/takeaway/example/module-label reading order, English run language, high-contrast dark/light theme colors, 54-point cover titles, 36-point teaching titles, 22-point takeaways, 18-20-point table/code content and editable diagram text. This is **not** a PowerPoint Accessibility Checker or assistive-technology certification; those checks and actual presentation-room readability remain outstanding.
- Deck generation does not clear the action-lock, target-tenant runtime or full-course rehearsal gates. The added Python deck-generation tool is outside the earlier Actions/JavaScript CodeQL scan scope.

## Other release gates

- Run PowerPoint's Accessibility Checker and confirm assistive-technology and presentation-room usability; deck generation and native rendering are complete, but these checks are not.
- Target-tenant schema/runtime checks and manual event/ref/token/cache/artifact trust-boundary rehearsals remain outstanding. Use prepared evidence only when it is clearly labeled as such.
- `node --test tools/changed-files.test.mjs tools/workflow-triggers.test.mjs`: passed, 7 tests, including exact action-release lookup parity across workflows and teaching examples.
- Python 3.13.14 matches `.python-version`. Both requirements entry points resolve to the installed direct tool versions: python-pptx 1.0.2, Pillow 13.0.0 and zizmor 1.32.0. The earlier Pillow `<13` constraint did not match the installed rendering environment and has been replaced with the verified exact version.
- `.gitignore` covers dependency/build directories, scanner reports/databases, native render output, virtual environments, Python caches, release-lab outputs and local credential/temporary files. The previously staged `.zizmor-initial.json` was removed from the index without deleting its local copy. Course PowerPoint deliverables, manifests and source fixtures remain trackable.
- `npm --prefix app test`: passed, 1 test.
