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

Use plain English on slides, including captions, diagrams and tables. Introduce a required technical term on the same slide or an earlier slide; speaker notes alone are not a learner-facing explanation. Give lab prompts a concrete action and object ("open the instructor's example run"), not unexplained shorthand ("begin from the checkpoint"). Keep exact YAML/API names in examples, explain what they do, and keep longer implementation caveats in instructor notes. The cache lab changes the lockfile and cache-version label separately so learners can distinguish a partial hit from a new-version miss.

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
2. Preflight individual workflow examples under `examples/workflows`; they are inert until copied. Verify event and ref semantics, file-level `permissions: {}`, least-privilege job-level permissions, safe input handling, caches, timeout/cancellation, and `workflow_dispatch` availability. Check that each action reference names a current supported version, then generate/update and review the repository lockfile with `gh actions-lock` rather than repeating SHAs in workflow files; verify lockfile support on the target host. **Never install all examples at once.** Issue examples must be metadata-only: no checkout/API writes, `permissions: {}`, and `cache-mode: none`. PR cache uses restore-only and `cache-mode: read`, never hidden setup writers; deployments use `cache-mode: none`. Trusted cache writers must not execute PR code/artifacts or untrusted lifecycle scripts.
3. **GHEC REQUIRED:** verify required-workflow eligibility, org ownership and configuration; separately check private/internal attestation, queue and each rule. **EMU SETUP:** assign managed identities to authorized org repositories rather than assuming personal/fork access. **GHE.COM SETUP:** confirm the enterprise's actual host, auth, API endpoints, runner/action availability, CLI and feature support. Record product, plan, visibility, date checked, and any preview/region restrictions. Research baseline is [2026-11-10](REFERENCES.md); it is not a tenant test.
4. **PAID RUNNER / ADMIN REQUIRED:** if used, authorize budgets, safe prebuilt image/version, runner group, networking, organization rulesets, queue and a disposable staging environment before class. Verify custom image, private networking/VNet integration and required workflows **independently**. Do not require purchases, live image generation, ARC installation or real cloud modifications from learners. Restricted environments and image builders need least privilege and reviewed inputs. Use recorded evidence when unavailable.
5. Prepare actual recordings/screenshots/logs (with confidential data removed): baseline; trusted cold/exact/partial cache and PR restore-only; image setup and archive-cache diagnostics; sequential/native-parallel/separate jobs, propagated failure and one-minute timeout; issue activity table; stack cancellation and merge-group combined SHA; check/detection-failure/deployment/central-workflow scenarios; path/output debugging; dependency graph before/after, unresolved mappings and graph/artifact SBOMs; signed release verification, tamper, wrong-signer and same-digest mock promotion. If a capability cannot be safely rehearsed, label it blocked and use accurate conceptual evidence rather than claiming success.
6. Prepare docs-only, app-code, shared-lockfile/config, workflow-change and failed-detection fixtures. Required aggregator tests must prove missing, failed, cancelled and timed-out evidence does not pass. Use actual merge-group base/head for combined revisions. Prepare safe fake-only local tool inputs; no real secrets or full-context dumps.

## Publication validation gate

### Exercise trigger scope

Only the trusted Lab 2 cache writer subscribes to `push`, limited to `main` and changes under `app/`, its own workflow (source or installed path), or `actions.lock`. The Lab 2 PR consumer uses the same relevant-input categories. These optional path-filtered cache examples must not be configured as required checks: unrelated changes intentionally produce no run. If a workflow is renamed when installed, update its self-path filter. Expand the input list if the application gains shared build/configuration inputs outside `app/`.

The Lab 5 stack/queue and Lab 6 required gate, staging deployment and central-policy examples deliberately remain unfiltered: required evidence must exist for every applicable revision, including docs-only changes. Lab 6 selects application work inside the run and always evaluates its final gate. `merge_group` and `issues` do not support trigger `paths`; do not add invalid filters or skip required deployments. Issue workflows retain their activity experiment; dispatch-only examples cannot run on pushes. Copy only the active lab's workflows, then disable/remove those course-owned copies at the end of the lab instead of leaving all exercises subscribed.

Inventory every runnable workflow, local action, reusable workflow, starter/solution and materialized embedded example. Run **zizmor** on all runnable workflow/action variants and **CodeQL GitHub Actions analysis** where supported plus applicable supported script/action languages. Record versions, exact commands/configuration, scope, findings and narrow justified dispositions. Do not use blanket suppressions. Confirm actual Actions analysis coverage, not just a green scan of unrelated app code. If a surface cannot be analyzed, explicitly mark it blocked or document the precise limitation; do not claim it was validated.

Also verify schema and runtime on the target tenant; manually review event/ref/token/cache/artifact/image boundaries and negative gate outcomes. Retain run evidence and revalidate on source or feature changes. Static scans are not proof of safety. No scanners are assumed installed or executed by this guide.

## Facilitation and timing

Use **predict → observe → change → explain back**. Show a prepared checkpoint when queueing or indexing threatens the schedule; never omit the failure, trust and gate cases.

| Section | Schedule inside 105 minutes | Evidence / recovery |
| --- | --- | --- |
| 1: measure and reuse | 0–10 recap; 10–20 metrics; 20–30 [Lab 1](hol/01-Measure.md); 30–50 cache teaching; 50–75 [Lab 2](hol/02-Cache.md); 75–85 image demo; 85–100 [Lab 3](hol/03-Prewarm.md); 100–105 debrief | Baseline worksheet, cold/exact/partial and restore-only logs, image comparison. Reuse prepared runs on a miss/queue delay. Explain why partial cache still needs `npm ci`. |
| 2: avoid and parallelize | 0–8 checkout lifecycle/sparse scan; 8–12 artifact packaging/selection/extraction; 12–20 events; 20–40 [Lab 4A](hol/04-Events-and-parallelism.md); 40–60 parallel/timeout teaching; 60–85 Lab 4B; 85–100 runner choices; 100–105 debrief | Issue prediction table; shared-impact/detection failure; parallel failure and one-minute timeout. Comment is a different event, PR defaults differ. Use recorded runs if native syntax is unavailable. |
| 3: stack and gates | 0–15 stack/queue; 15–40 [Lab 5](hol/05-Stacks-and-queue.md); 40–60 gates; 60–95 [Lab 6](hol/06-Gates.md); 95–105 debrief | Layer versus combined SHA, cancellation evidence, separate check/deployment/central workflow blockers. Fail detection closed. Never bypass a rule for the demo. |
| 4: diagnose and promote | 0–15 debugging; 15–35 [Lab 7](hol/07-Debug.md); 35–45 local-tool demo; 45–65 [Lab 8](hol/08-Dependencies.md); 65–95 [Lab 9](hol/09-Promotion.md); 95–105 capstone | Targeted failure/fix; graph versus artifact inventory; exact signer and digest, tamper/wrong signer rejection, same-byte mock promotion. A signature is not a vulnerability assessment. |

Breaks are 10:45–11:00 and 15:00–15:15; lunch 12:45–13:15. The timed sections total 420 minutes. Local-action targets unbundled JS/TS action logic; `act` does not reproduce GitHub's full security/control plane. Do not install tools on each learner workstation during the demo.

## Demonstration cards

| Checkpoint and prediction | Action / expected observation | Failure and recovery |
| --- | --- | --- |
| Baseline: setup versus execution | Open run timing and compare job time to feedback latency. | Queue delay: use recorded timeline; avoid treating a single run as representative. |
| Cache: exact, partial, miss | Inspect output strings and confirm `npm ci` each time. | Entry expired: use recorded logs; never enable a low-trust write override. |
| Checkout: what work is needed? | Explain lifecycle, show sparse working tree, compare the same revision and scanner inputs; inspect depth, submodules and LFS. | Missing config/local action/history invalidates the comparison. Expand inputs; retain clean workspace and auth safeguards. |
| Artifact transfer: what is selected? | Compare prepared archives (one file per archive:false invocation) with distinct named bundles. Show skip-decompress true/false and artifact-name selection. | ZIP-member selection is not supported. Extraction control does not save transfer; keep required evidence and integrity checks. |
| Issue events | Open/edit/label/comment the disposable issue; both/both/broad/neither. | Issue denied: instructor demo. No issue text in scripts. |
| Parallel/timeout | Show failed branch propagating and one-minute step termination. | Runner saturation: recorded variants; discuss shared resources and measured budgets. |
| Stack and policy | Identify combined SHA and each independent gate. | Missing access/queue: use prepared runs; never change shared rules. |
| Debug/inventory | Show bounded path evidence and trusted-branch graph snapshot. | Index lag: use snapshots; no full environment or secrets. |
| Release | Verify original expected identity, modified copy and wrong identity; compare promoted digest. | Verification unavailable/mismatch: stop promotion and show prepared negative evidence; never replace it with a green-looking result. |

## End-of-day and ownership

Run [the cleanup checklist](hol/10-Cleanup.md) with learners. Personally verify active/queued runs, event/scheduled automations, retention of course caches/artifacts/images, dedicated paid capacity, image build/storage/network charges and temporary access. Coordinate queue/ruleset/runner-group cleanup with their owners; do not remove shared resources. Stop local demos and remove fake credential files. Document any residual resource, cost owner and follow-up.
