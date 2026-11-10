# Instructor guide: Actions Advanced

This guide accompanies [the outline](CLASS-OUTLINE.md), [delivery requirements](DELIVERY-REQUIREMENTS.md) and [source register](REFERENCES.md). These labs are authored guidance, **not evidence of an executed rehearsal or completed security scan**. Do not publish runnable material until the validation gate below is complete.

See [current validation status](VALIDATION-STATUS.md) for completed scanner runs, exact coverage, retained evidence, and remaining publication blockers.

Use the dated [action version lookup](ACTION-VERSIONS.md) for live-queried stable releases, release-tag commits, versions currently used and refresh commands. It is not a dependency lockfile.

## Teaching decks and updates

The four decks use the supplied `Guidance_PPTX.pptx` Xebia master and layouts. Their Markdown sources are authoritative; speaker notes include the source timing, demonstrations, failure/recovery cases and references.

Supporting material accompanies 37 slides: nine editable flow diagrams, fourteen comparison/decision tables and fourteen code or worked-example panels. Examples cover cache keys and restore behavior, latency versus runner consumption, issue activity predictions, parallel steps, OS/runtime compatibility matrices and timeout, merge-queue revisions and gate decisions, targeted diagnostics, and artifact identity verification. Numerical timelines and predicted outcomes are labeled illustrative, not captured run evidence; code excerpts are identified as incomplete where applicable.

| Module | Markdown source | PowerPoint with speaker notes |
| --- | --- | --- |
| 1: measure and reuse | [Caching](slides/01-caching.md) | [16 slides](slides/powerpoint/01-caching.pptx) |
| 2: avoid and parallelize | [Execution](slides/02-execution.md) | [23 slides](slides/powerpoint/02-execution.pptx) |
| 3: stack and gates | [Policy](slides/03-policy.md) | [17 slides](slides/powerpoint/03-policy.pptx) |
| 4: diagnose and promote | [Debug and trust](slides/04-debug-trust.md) | [14 slides](slides/powerpoint/04-debug-trust.pptx) |

Edit the matching Markdown and its notes, not the generated PowerPoint. Keep the labs and references aligned.

**Starter versus solution:** learners copy from `examples/workflows` and implement the task-specific TODOs, not from `solutions/workflows`. Full references are linked in collapsed lab solutions. Baselines and minimal observers/demos intentionally remain runnable scaffolding. Other incomplete evidence steps fail explicitly; do not activate required rules or accept an image/release until implementations are reviewed. Rehearse both the incomplete failure and the learner-completed path. Prior walkthrough evidence covers the completed checkpoints, not the revised authoring exercises. The existing time boxes are targets pending a fresh timed rehearsal; use hints and labeled recorded evidence rather than silently replacing starters with solved copies.

Lab 3's archive-cache stretch uses `jessehouwing/gh-actions-archive-cache` pinned to `v0.0.2`: install, download the exact reviewed action commit, then uninstall via an exit trap before snapshotting. Preflight GitHub CLI, builder cache permissions and the job's step-only read token; do not save authentication in the image. Verify download/uninstall logs and later runner archive-copy diagnostics separately. The extension is build tooling, not a consumer dependency. Keep its explicit github.com host/token example separate from GHE.com credentials.

**Lab 3 is split across the day.** Launch the image build during module 1, record the run and image identity, then move on to Lab 4 without waiting for generation/replication. Use recorded comparison evidence in the scheduled slot. Remind learners to check back at a later break and before Lab 10 cleanup; resume the consumer only for the seeded Ready version and confirm the actual job version. If unavailable, record live verification as pending and agree owner-led cleanup or an explicitly approved later comparison with a cleanup deadline. Do not repeatedly rebuild or leave paid images indefinitely while waiting.

Use plain English on slides, including captions, diagrams and tables. Introduce required terms visibly; notes alone are not explanations. Lab prompts need a concrete action/object, not unexplained checkpoint shorthand. Keep exact YAML/API names in examples and longer caveats in notes. Lab 2 changes the CodeQL manifest note and cache epoch separately, distinguishing compatible partial reuse from a fresh miss without changing actual tool bytes.

**Lab 2 download budget:** the reviewed CodeQL v2.27.4 Linux x64 `.tar.zst` bundle is 559,484,083 bytes. Preflight Node 24, GNU tar/zstd, GitHub release access, disk space and cache quota on the hosted Linux runner. The helper supplies download/checksum safety, not Actions cache logic; learners implement the latter. Extract only verified bytes outside the cache and call the downloaded CLI directly, not a preinstalled CodeQL on PATH. No scan/database/upload setup is needed. Compare upstream/cache transfer, verification, extraction and save separately. New epochs can consume over a gigabyte per participant across snapshots; coordinate keys/retention. Historical npm-cache evidence is not evidence that this revised exercise ran; prepare new CodeQL recordings before delivery.

The module 2 compatibility-matrix example occupies minutes 56-60 within the existing teaching segment, not a new required lab. It repeats all tests on two operating systems and three illustrative Node versions (six jobs), limits active matrix jobs to three and keeps other combinations running after a failure. Verify runtime availability and project support before class. Contrast this with sharding, which splits one suite between runners; the proposed scatter/gather optional lab is not implemented.

To regenerate from the course root, supply the location of the original guidance deck:

```powershell
python -m pip install -r requirements.txt
python tools\build_slides.py --template 'C:\path\to\Guidance_PPTX.pptx'
python -m unittest discover -s tools -p test_build_slides.py
pwsh -NoProfile -File tools\validate_slides.ps1
```

The authoring environment uses Python **3.13.14**, recorded in `.python-version`. Root `requirements.txt` pins `python-pptx` **1.0.2**, Pillow **13.0.0** and zizmor **1.32.0**; `tools/requirements-pptx.txt` forwards to it for older commands. These are author/instructor prerequisites, not learner installations. A Python version manager can read `.python-version`; otherwise select that interpreter explicitly before installing. Use an isolated `.venv` rather than changing a shared Python environment.

Non-Python prerequisites are not installed by pip: GitHub CLI with `gh codeql` (recorded CodeQL CLI **2.27.1**) and `gh actions-lock` (installed extension **v0.4.1**), PowerShell, desktop Microsoft PowerPoint (**16.0** used for rendering), and Arial/Consolas fonts. The native slide renderer needs Windows and desktop PowerPoint. Confirm host support and availability before class; a Python requirements install alone cannot provide these tools or a target-tenant rehearsal.

The generator checks content/notes/example parity, template masters/layouts and slide bounds, and writes hashes and counts to `slides\powerpoint\manifest.json`. It uses Arial regular/bold and Consolas from Windows; `--font` and `--bold-font` accept alternate paths to the Arial files. The native validation script requires installed desktop PowerPoint; it opens the decks read-only, renders every slide, checks text bounds including table cells and footer clearance, and retains PNGs plus a hash-linked report under `.validation\powerpoint-render`. Estimated wrapping is not a substitute for native rendering. After changes, inspect the renders for branding, clarity and reading order, and run PowerPoint's Accessibility Checker before publication. Do not treat deck generation as completion of the runnable-material validation gate.

To edit supporting material, keep one short takeaway above a `##` example caption, then a Markdown table or one fenced block (`yaml`, `bash`, `text`, or `flow`). A `flow` block contains one `heading | explanation` card per line, rendered left to right with arrows. Keep code excerpts brief and preserve indentation; diagrams and tables remain editable PowerPoint objects. Keep the slide's existing notes block and timing; supporting material belongs to the same teaching segment, not an extra lecture.

## Before class: ownership and preflight

1. Provide each learner an authorized disposable repository and the same `app` with lockfile, tests, lint and build. Check Actions and issue/PR permissions, training label, default branch, allowed actions/lockfiles, retention and runner budgets. Confirm all example paths used by the labs exist and match their described behavior.
2. Preflight both `examples/workflows` starters and `solutions/workflows` references, inert until copied. Check that each starter withholds its target logic and that the lab supplies enough taught concepts/linked docs to implement it; don't copy the solution for learners. Verify event/ref semantics, root empty and job-only least-privilege permissions, safe inputs, cache boundaries and budgets. Generate/review locks after learners add actions, using `gh actions-lock`, not per-file SHA pins. **Never install either whole directory.** Issue fixtures stay metadata-only; PR cache is restore-only/read and setup caching is disabled; deployments use no cache. Trusted writers never execute unreviewed PR inputs.
3. **GHEC REQUIRED:** verify required-workflow eligibility, org ownership and configuration; separately check private/internal attestation, queue and each rule. **EMU SETUP:** assign managed identities to authorized org repositories rather than assuming personal/fork access. **GHE.COM SETUP:** confirm the enterprise's actual host, auth, API endpoints, runner/action availability, CLI and feature support. Record product, plan, visibility, date checked, and any preview/region restrictions. Research baseline is [2026-11-10](REFERENCES.md); it is not a tenant test.
4. **PAID RUNNER / ADMIN REQUIRED:** authorize Lab 3 budgets and a repository-restricted runner group before class. Eligible participants customize and build their image, then select its exact Ready version on a separate consumer; allow configuration propagation and confirm the version in the job log. Use recorded evidence if generation exceeds class time; do not require purchases, ARC installation or real cloud modifications. Lab 5 participants configure their own repository's queue rule and record the prior settings. Lab 6 check/deployment gates use repository rulesets; its separate central-workflow rule requires organization ruleset-management permission and approved Actions sharing on the source. Never broaden that sharing without owner approval. For the organization rule select exactly the participant repository and default branch, verify saved scope and record its ID. Labs 6/9 staging servers are local to jobs. Verify each feature independently and use recorded evidence where access is unavailable.
5. Prepare actual recordings/screenshots/logs (with confidential data removed): baseline; trusted cold/exact/partial cache and PR restore-only; image setup and archive-cache diagnostics; sequential/native-parallel/separate jobs, propagated failure and one-minute timeout; issue activity table; stack cancellation and merge-group combined SHA; check/detection-failure/deployment/central-workflow scenarios; path/output debugging; dependency graph before/after, unresolved mappings and graph/artifact SBOMs; signed release verification, tamper, wrong-signer and same-digest mock promotion. If a capability cannot be safely rehearsed, label it blocked and use accurate conceptual evidence rather than claiming success.
6. Prepare docs-only, app-code, shared-lockfile/config, workflow-change and failed-detection fixtures. Lab 6 reuses reviewed `tj-actions/changed-files` rather than a custom script; full checkout history and explicit event base/tested SHAs keep PR and merge-group comparisons correct. Preserve fail-on-diff-error and ordered patterns, including `.github` Markdown, deleted/type-changed files and both rename paths. Temporarily use 40 zeros for `base_sha` only in the disposable PR to cause detection failure, then restore the expression. Required aggregator tests must prove missing, failed, cancelled and timed-out evidence does not pass. Prepare safe fake-only local tool inputs; no real secrets or full-context dumps.

## Publication validation gate

### Lab 6 permission fallback

Participants with repository-admin access can perform approved Lab 6 repository-local check and deployment scenarios even without organization ruleset permissions. Technical administrator access is not approval to change sharing or policy: require explicit repository-owner and policy-owner authorization. When participant changes are disallowed by organization policy or technical permissions, demonstrate only the central-enforcement portion in an authorized disposable trainer repository; do not ask learners to obtain elevated access or policy exceptions. Follow the lab's source-sharing steps, recording the original setting and explaining that organization sharing is broader than the ruleset's one selected target. The trainer creates a uniquely named organization demo rule targeting **Only selected repositories → exactly the disposable demo repository**, and only its default branch. Verify saved scope before activation. Do not select all repositories, patterns or participants' repositories. Remove the course rule before restoring exactly the original source-sharing setting. If a trainer demonstration is not authorized or technically available, label enforcement unverified and use recorded evidence.

### Exercise trigger scope

Only the trusted Lab 2 cache writer subscribes to `push`, limited to `main`, `examples/codeql-bundle.json`, `tools/prepare-codeql.mjs`, its own source/installed workflow and `.github/workflows/actions.lock`. The PR consumer selects the same categories. Unrelated app/docs edits deliberately do not trigger either; they must not be required checks. A harmless helper comment repeats an exact key; a manifest note edit changes the key without changing the requested archive. Update self-filters on rename; preserve required unfiltered workflows in later labs.

The Lab 5 stack/queue and Lab 6 required gate, staging deployment and central-policy examples deliberately remain unfiltered: required evidence must exist for every applicable revision, including docs-only changes. Lab 6 selects application work inside the run and always evaluates its final gate. `merge_group` and `issues` do not support trigger `paths`; do not add invalid filters or skip required deployments. Issue workflows retain their activity experiment; dispatch-only examples cannot run on pushes. Copy only the active lab's workflows, then disable/remove those course-owned copies at the end of the lab instead of leaving all exercises subscribed.

Inventory every runnable workflow, local action, reusable workflow, starter/solution and materialized embedded example. Run **zizmor** on all runnable workflow/action variants and **CodeQL GitHub Actions analysis** where supported plus applicable supported script/action languages. Record versions, exact commands/configuration, scope, findings and narrow justified dispositions. Do not use blanket suppressions. Confirm actual Actions analysis coverage, not just a green scan of unrelated app code. If a surface cannot be analyzed, explicitly mark it blocked or document the precise limitation; do not claim it was validated.

Also verify schema and runtime on the target tenant; manually review event/ref/token/cache/artifact/image boundaries and negative gate outcomes. Retain run evidence and revalidate on source or feature changes. Static scans are not proof of safety. No scanners are assumed installed or executed by this guide.

## Facilitation and timing

Use **predict → observe → change → explain back**. Show a prepared checkpoint when queueing or indexing threatens the schedule; never omit the failure, trust and gate cases.

| Section | Schedule inside 105 minutes | Evidence / recovery |
| --- | --- | --- |
| 1: measure and reuse | 0–10 recap; 10–20 metrics; 20–30 [Lab 1](hol/01-Measure.md); 30–50 cache teaching; 50–75 [Lab 2](hol/02-Cache.md); 75–85 image demo and launch of learner image builds; 85–100 [Lab 3](hol/03-Prewarm.md); 100–105 debrief | Baseline worksheet, CodeQL cold/exact/partial/restore-only logs and image comparison. Use recorded evidence when transfers, queues or image generation exceed the slot. Verify/check/extract on every cache path; don't count old npm evidence as CodeQL rehearsal. |
| 2: avoid and parallelize | 0–8 checkout lifecycle/sparse scan; 8–12 artifact packaging/selection/extraction; 12–20 events; 20–40 [Lab 4A](hol/04-Events-and-parallelism.md); 40–60 parallel/timeout teaching; 60–85 Lab 4B; 85–100 runner choices; 100–105 debrief | Issue prediction table; shared-impact/detection failure; parallel failure and one-minute timeout. Comment is a different event, PR defaults differ. Use recorded runs if native syntax is unavailable. |
| 3: stack and gates | 0–15 stack/queue; 15–40 [Lab 5](hol/05-Stacks-and-queue.md); 40–60 gates; 60–95 [Lab 6](hol/06-Gates.md); 95–105 debrief | Layer versus combined SHA, cancellation evidence, separate check/deployment/central workflow blockers. Fail detection closed. Never bypass a rule for the demo. |
| 4: diagnose and promote | 0–15 debugging; 15–35 [Lab 7](hol/07-Debug.md); 35–45 local-tool demo; 45–65 [Lab 8](hol/08-Dependencies.md); 65–95 [Lab 9](hol/09-Promotion.md); 95–105 capstone | Targeted failure/fix; graph versus artifact inventory; exact signer and digest, tamper/wrong signer rejection, same-byte mock promotion. A signature is not a vulnerability assessment. |

Breaks are 10:45–11:00 and 15:00–15:15; lunch 12:45–13:15. The timed sections total 420 minutes. Local-action targets unbundled JS/TS action logic; `act` does not reproduce GitHub's full security/control plane. Do not install tools on each learner workstation during the demo.

## Demonstration cards

| Checkpoint and prediction | Action / expected observation | Failure and recovery |
| --- | --- | --- |
| Baseline: setup versus execution | Open run timing and compare job time to feedback latency. | Queue delay: use recorded timeline; avoid treating a single run as representative. |
| Cache: exact, partial, miss | Inspect lookup outputs, upstream-download/reuse log, checksum and extracted CodeQL version each time. | Corrupt archive must fail; expiry can cause download. Use labeled recorded evidence, never a low-trust write override. |
| Checkout: what work is needed? | Explain lifecycle, show sparse working tree, compare the same revision and scanner inputs; inspect depth, submodules and LFS. | Missing config/local action/history invalidates the comparison. Expand inputs; retain clean workspace and auth safeguards. |
| Artifact transfer: what is selected? | Compare prepared archives (one file per archive:false invocation) with distinct named bundles. Show skip-decompress true/false and artifact-name selection. | ZIP-member selection is not supported. Extraction control does not save transfer; keep required evidence and integrity checks. |
| Issue events | Open/edit/label/comment the disposable issue; both/both/broad/neither. | Issue denied: instructor demo. No issue text in scripts. |
| Parallel/timeout | Show failed branch propagating and one-minute step termination. | Runner saturation: recorded variants; discuss shared resources and measured budgets. |
| Stack and policy | Identify combined SHA and each independent gate. | Missing access/queue: use prepared runs; never change shared rules. |
| Debug/inventory | Show bounded path evidence and trusted-branch graph snapshot. | Index lag: use snapshots; no full environment or secrets. |
| Release | Verify original expected identity, modified copy and wrong identity; compare promoted digest. | Verification unavailable/mismatch: stop promotion and show prepared negative evidence; never replace it with a green-looking result. |

## End-of-day and ownership

Run [the cleanup checklist](hol/10-Cleanup.md) with learners. Personally verify active/queued runs, event/scheduled automations, retention of course caches/artifacts/images, dedicated paid capacity, image build/storage/network charges and temporary access. Coordinate queue/ruleset/runner-group cleanup with their owners; do not remove shared resources. Stop local demos and remove fake credential files. Document any residual resource, cost owner and follow-up.
