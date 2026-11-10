# Actions Advanced - source register

**Last researched:** 2026-11-10.

Lab 2 large-download fixture: [CodeQL bundle v2.27.4](https://github.com/github/codeql-action/releases/tag/codeql-bundle-v2.27.4), queried through its release API on 2026-11-10. Linux x64 asset `codeql-bundle-linux64.tar.zst` is 559,484,083 bytes; published SHA-256 `da3e952c7fe978a0b6b93e75d9cbabbdf8535667ca0810bd4b2ae37bc840ffee`. `examples/codeql-bundle.json` is reviewed download metadata, not an execution `actions.lock`. The exercise directly downloads/verifies/extracts this bundle and runs its version command, not a CodeQL scan or the action's automatic installation.

This register preserves the documentation, blogs, implementation references, and supporting resources collected for the [proposed class](CLASS-OUTLINE.md). It is a maintenance aid, not a claim that every feature has been exercised on the training tenant.

Use GitHub Well-Architected for design trade-offs, GitHub Docs for implementation/availability, and source code to investigate mechanisms or discrepancies. The framework itself makes that source-of-truth distinction. Failed/obsolete discovery URLs are omitted in favor of their working canonical destinations.

## Research baseline

| Repository | Inspected revision | Purpose |
| --- | --- | --- |
| [github/github-well-architected](https://github.com/github/github-well-architected) | `d7ff7ab0b225e189c18dadca53196b0d8bc19764` | Design guidance and relevant recommendations. |
| [github/docs](https://github.com/github/docs) | `15f068380afe64f9d87ef55ec24d590eb9e055da` | Workflow syntax, feature/version gates, policy, and supply-chain docs. |
| [actions/runner](https://github.com/actions/runner) | `310a370bf3605f5b092f8af63b3126627de2a210` | Action archive cache implementation. |
| [actions/action-versions](https://github.com/actions/action-versions) | `e3c62146623237ce0e50fbb68f09fc0c4739446a` | First-party action archive cache builder. |
| [jessehouwing/gh-actions-archive-cache](https://github.com/jessehouwing/gh-actions-archive-cache) | `v0.0.2` | Lab 3 CLI for exact-commit downloads and reviewed-lockfile imports; [image provisioning and acceptance](https://github.com/jessehouwing/gh-actions-archive-cache/blob/v0.0.2/docs/custom-runner-images.md). Install/download/uninstall in the builder; preserve archive cache for the consumer. |
| [jessehouwing/actions-dependency-submission](https://github.com/jessehouwing/actions-dependency-submission) | `811981eec3c108f41783f194522fde91a34301a4` | Submission behavior, input defaults, resolver limits, and integration guidance. |
| [austenstone/github-actions-best-practices](https://github.com/austenstone/github-actions-best-practices) | `c069cad06a06b7fc7cf25d528f997a31d066a36b` | Community guidance on changed-file conditions, timeouts, and avoiding wasted work. |
| [dorny/paths-filter](https://github.com/dorny/paths-filter) | `f3360c560367c9daf72b88c0e6164162034c5721` | Job/step selection, event-specific comparisons, outputs, and filename handling. |
| [tj-actions/changed-files](https://github.com/tj-actions/changed-files) | `9426d40962ed5378910ee2e21d5f8c6fcbf2dd96` (`v47.0.6`) | Lab 3 archive seed and Lab 6 reusable detector: explicit SHAs, local-history comparison, ordered patterns, errors, deletions, type changes and both rename paths. |
| [actions/checkout](https://github.com/actions/checkout) | `f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a` | Inspected action metadata, README and source-provider implementation: workspace/auth/fetch/sparse/LFS/submodule lifecycle and cleanup; implementation reference, not a new approved action lock. |

Checkout teaching supplements: [Git sparse-checkout](https://git-scm.com/docs/git-sparse-checkout), [submodules](https://git-scm.com/docs/git-submodule), [Git LFS pull filters](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-pull.adoc), and [zizmor input collection](https://docs.zizmor.sh/usage/#input-collection). A workflow-only sparse scan is intentionally narrower than the course publication scan; compare equal inputs before claiming performance improvement.

Artifact-transfer supplements checked 2026-11-10: [download-artifact v8.0.2 inputs](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml) and [examples](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/README.md), plus [upload-artifact archive input](https://github.com/actions/upload-artifact#inputs). `pattern` selects artifact names, not ZIP members. With upload v7 `archive: false`, a single file becomes a directly downloadable artifact named after the file; `name` is ignored at upload. Avoid claiming arbitrary selective download within a monolithic archive.

Artifact packaging/extraction clarification: [upload validation](https://github.com/actions/upload-artifact/blob/main/src/upload/upload-artifact.ts) rejects multiple files in one `archive: false` invocation. Use separate steps/matrix jobs for prepared files, or distinct names with normal archive packaging. [Download inputs](https://github.com/actions/download-artifact/blob/9000827ccba6bdab643e8b6fd33ac0654aef8333/action.yml) expose `skip-decompress`: false extracts a detected ZIP by default, true preserves the downloaded archive. Neither extracts arbitrary nested formats recursively nor reduces selected-artifact transfer size.

The fundamentals comparison used `D:\actions-fundamentals`, particularly its README, hands-on lab layout, deployment `cache-mode` guidance, and pinning/lockfile lessons. Do not edit that course as part of this proposal.

## User-provided historical teaching materials

These are local, access-controlled teaching references. Do not upload or republish their contents, screenshots, speaker notes, or commercial information as part of the new class. The proposed adaptations are original explanations and teaching patterns, not copied slides.

### Intermediate class: Seismic 20260107

Source folder:

```text
C:\Users\JesseHouwing\Xebia\XMS - Xpirit Group\Training\GitHub\GitHub Actions Intermediate\Seismic 20260107
```

| ID | File or locator | Relevance and review boundary |
| --- | --- | --- |
| T01 | `GitHub Actions Intermediate ES offering (slidedeck-en).PPTX` | 55-slide topic inventory; selected text and speaker notes reviewed. Slides 11-17: matrix/concurrency/conditions and observable experiments; 29-31: local iteration; 45-49: debugging, runners, and monitoring. Visual design not inspected. |
| T02 | `GitHub Actions Intermediate ES offering (delivery guide-en).DOCX` | Sandbox rehearsal, prework, time checks, demo readiness, and end-of-session feedback. Reviewed as delivery guidance, not current product authority. |
| T03 | `GitHub Actions Intermediate ES offering (datasheet-en).DOCX`; `GitHub Actions Intermediate ES offering (seller one pager-en).DOCX` | Audience/prerequisite and practical-learning framing only. Commercial details are not part of the new course or this register. |

Useful patterns: predict the job graph, change one setting, observe the run, introduce an intentional failure, restore a working checkpoint, and explain the trade-off.

Do not inherit the 45-minute recap or broad API/custom-action authoring scope. Specific examples need correction: slide 11's `max-parallel` range; slide 16's deprecated environment/output commands and incorrect implication that command suspension hides sensitive output; slide 27's composite/reusable-workflow restrictions; and slides 29-30's overstatement of local runner fidelity. `stop-commands` disables command interpretation, not logging or secret disclosure. Current references D01, D19, D21, L01-L03, and W09 govern the replacement material.

### GH200: older official course

Source folder:

```text
C:\Users\JesseHouwing\Xebia\XMS - Xpirit Group\Training\Microsoft MOC\GH200
```

| ID | File or locator | Relevance and review boundary |
| --- | --- | --- |
| T04 | `GH-200T00-ENU-TrainerPrepGuide.pdf`; `GH-200T00-ENU-Change-Log.pdf` | Both dated June 2025. Reviewed objectives, preparation, timing, delivery choices, and refresh guidance. The guide contains inconsistent instructional/exercise allocation and unrelated certification wording; do not adopt its schedule or exam claims. |
| T05 | `GH-200T00-ENU-Powerpoint\GH-200T00-ENU-Powerpoint-01.pptx` through `-07.pptx`, plus `-Introduction.pptx` and `-Conclusion.pptx` | Topic/title inventory across nine decks. Selected content: module 2 slides 45-49 (cache/artifacts/logs), module 6 slides 30, 33, 38, 42 (diagnostic practices), module 7 slides 48-49, 66-67 (runner trade-offs and controls). Text/notes only; not a full factual audit or visual review. |

The matching `GH-200T00-ENU-Powerpoint.zip` is a packaged copy, not an additional independently reviewed source.

Useful patterns: objective-first modules, concept-to-example progression, comparison tables, instructor explanation beyond slide bullets, short knowledge checks, and rehearsed demonstrations. Keep the new course lab-led; do not import a mostly lecture-based certification syllabus or its eight-hour instruction total into an eight-hour day that must include breaks.

Refresh rather than reuse the sample `@v2` action references, unrestricted cache writer examples, secrets-only debugging instructions, runner capability/pricing claims, and broad logging advice. Retain the cache/artifact distinction and runner ownership trade-offs while adding restore-only PRs, modern `cache-mode`, hosted custom images, current diagnostics, and evidence-based verification.

### Related links discovered in historical speaker notes

Retained for future review; these repositories/pages were not independently fetched or their workflows executed during the historical-material review.

| Resource | Potential use |
| --- | --- |
| [enyil/matrix-demo](https://github.com/enyil/matrix-demo) | Small matrix experiments and intentional failure. |
| [enyil/concurrency-demo](https://github.com/enyil/concurrency-demo) | Observe superseded-run cancellation and dependency sequencing. |
| [enyil/act-demo](https://github.com/enyil/act-demo) | Minimal local workflow demonstration. |
| [enyil/reusable-workflows-demo](https://github.com/enyil/reusable-workflows-demo) | Historical background; outside the new class's core authoring scope. |
| [enyil/issue-automation-demo](https://github.com/enyil/issue-automation-demo) | Historical background; outside the new performance syllabus. |
| [ps-actions-sandbox/demo-workflow-syntax](https://github.com/ps-actions-sandbox/demo-workflow-syntax) | Guided observation of workflow execution and logs. |
| [Red Hat: testing GitHub Actions locally](https://www.redhat.com/en/blog/testing-github-actions-locally) | Historical local-tool discussion; revalidate tools and limitations. |
| [Microsoft Learn training](https://learn.microsoft.com/en-us/training/) | Locate current learning paths rather than treating local slides as current. |
| [GitHub certifications](https://resources.github.com/learn/certifications) | Check current certification information only if needed; this proposal is not an exam-coverage guarantee. |

## Well-Architected design guidance

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| W01 | [Framework overview][W01] | Source hierarchy, pillars, and design principles. |
| W02 | [Effective continuous integration][W02] | Main design backbone: feedback, caching, native parallel steps/jobs, custom environments, and metrics. |
| W03 | [Engineering System Metrics][W03] | Balance velocity, quality, developer experience, and business outcomes. |
| W04 | [Securing GitHub Actions Workflows][W04] | Least privilege, immutable inputs, untrusted triggers, runner trust, and OIDC. |
| W05 | [Rulesets Best Practices][W05] | Policy tiers, pilot/Evaluate rollout, bypasses, and Rule Insights. |
| W06 | [Deploying Actions Runner Controller][W06] | Self-hosted operational responsibility, images, tool/action archive caches, networking, and scaling. |
| W07 | [Private networks from runners][W07] | Hosted networking alternatives to self-hosting. |
| W08 | [Resilient CI/CD][W08] | Approved artifacts, portable deployment logic, verification material, and recovery. |
| W09 | [Scaling Actions Reusability][W09] | Shared patterns and ownership; distinguish reuse from enforcement. |

## Performance, caching, parallelism, and runners

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| D01 | [Workflow syntax][D01] | Authoritative `cache-mode`, native `parallel`/`background`/`wait`/`wait-all`/`cancel`, `needs`, permissions, and limits. |
| D01S | [Versioned native parallel-step source][D01S] | Research snapshot of newer syntax; compare with current Docs before publication. |
| D02 | [Dependency caching reference][D02] | Exact/prefix matching, branch scope, modes, reusable-call limits, defaults, storage, and eviction. |
| D03 | [actions/cache][D03] | Restore/save actions, string outputs, selected version/runtime requirements. |
| D04 | [Matrix strategies][D04] | Variations, failure behavior, and `max-parallel`. |
| D05 | [Concurrency controls][D05] | Cancellation, group isolation, pending queues, and `queue: max`; distinct from merge queue. |
| D06 | [Larger runners][D06] | Resource, platform, network, grouping, and autoscaling capabilities. |
| D07 | [Custom hosted images][D07] | Generation runners, `snapshot`, versions, availability, permissions, retention, and builder security. |
| D08 | [Larger-runner billing][D08] | Check current rates/plan terms rather than preserving price assumptions. |
| A01 | [First-party action archive tooling][A01] | Archive layout and builder behavior. |
| A02 | [Runner archive-cache implementation][A02] | `ACTIONS_RUNNER_ACTION_ARCHIVE_CACHE`, exact-SHA archive lookup, and download fallback. |
| A03 | [Ken Muse: action archive cache][A03] | Practical image integration, linked by WAF and first-party tooling. |
| A04 | [Ken Muse: tool cache][A04] | Tool prewarming, ownership, runtime version/architecture. |
| P01 | [npm ci][P01] | A download-cache hit does not replace project installation. |
| P02 | [NuGet packages/cache folders][P02] | Global packages, `NUGET_PACKAGES`, credential separation, and restore behavior. |
| D23 | [Native path filters][D23] | Workflow versus job selection, PR/push diff semantics, version-dependent file limits, and required-check interaction. |
| D24 | [Job timeouts][D24] | Default 360-minute budget, runner execution limits, and token lifetime constraints. |
| D25 | [Step timeouts][D25] | Positive whole-minute budget, maximum, and enclosing job limit. |
| D26 | [Event activity types][D26] | `on.<event>.types`, PR default activities, explicit replacement of defaults, and metadata versus code-validation triggers. |
| D27 | [Issue events][D27] and [issue-comment events][D28] | Low-friction activity-filtering experiment; issues accept all activities by default, comments are a separate event, and workflow files must exist on the default branch. |

## Community performance guidance

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| B01 | [Austen Stone: GitHub Actions best practices][B01] | Changed-file conditions, job/step timeouts, concurrency, and cost framing. Community guidance, not the official GitHub Well-Architected repository. |
| B02 | [dorny/paths-filter README][B02] | Reviewed candidate for component-aware job/step selection; PR API permissions, merge-group base/head, string outputs, and untrusted filenames. |
| B03 | [tj-actions/changed-files][B03] | Selected reusable detector for Lab 6 and archive-seeding fixture for Lab 3. Reviewed v47.0.6 metadata/source; preserve explicit base/tested SHAs, fail-on-diff-error, ordered patterns and deletion/type/rename coverage. |

Apply B01 selectively. Its `node_modules` caching example is unsuitable for the class's `npm ci` flow; cache package downloads instead. Its broad concurrency and versioning examples also need the class's event isolation and immutable-dependency protections. Do not copy its historical limits, pricing assumptions, or workstation-as-runner suggestion without current verification.

## Metrics

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| D09 | [Actions metrics concepts][D09] | Performance versus usage, access, and dimensions. |
| D10 | [Viewing Actions metrics][D10] | Dashboard location, CSV export, aggregation periods, excluded data, and count discrepancies. |
| X01 | [Xebia performance metrics](https://github.com/orgs/xebia/actions/metrics/performance) | User-supplied teaching entry point; access-controlled, not inspected for this research. |
| X02 | [Xebia usage metrics](https://github.com/orgs/xebia/actions/metrics/usage) | User-supplied teaching entry point; use anonymized/repository fallback if inaccessible. |

## Stacks, merge queue, and policy

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| D11 | [Managing merge queue][D11] | Combined revision, required events, concurrency, rebuilds, and merge limits versus build batching. |
| D12 | [Native stacked PR reference][D12] | Trunk protections, linear history, deployments, atomic merges, and queue support. |
| D13 | [Optimizing stacked-PR CI][D13] | Metadata and top/lowest-unmerged conditions; preserve mandatory evidence. |
| D14 | [Creating stacked PRs][D14] | Website and documented `gh stack` workflow. |
| D15 | [Available rules][D15] | Required checks versus deployments, expected sources, strict/loose requirements. |
| D16 | [Required workflows][D16] | Central enforcement, source visibility, supported events/filter behavior, and direct-push restrictions. |
| D17 | [Required-check troubleshooting][D17] | Latest SHA, skipped jobs versus skipped workflows, eligible events, and final-gate pitfalls. |

## Debugging and action-dependency protection

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| D18 | [Enable debug logging][D18] | Step/runner switches, settings, reruns, and diagnostic archives. |
| D19 | [Secure use reference][D19] | Masking limitations, injection, trigger risks, permissions, and dependency locks. |
| D19C | [GitHub context warning][D19C] | Whole-context logging includes sensitive and attacker-influenced fields. |
| D20 | [Workflow dependency lockfiles][D20] | `actions.lock`, covered/transitive action dependencies, reusable-workflow exclusions, and policy behavior. |
| D21 | [Workflow commands][D21] | Safe diagnostics, annotations, groups, summaries, outputs, masks, and command suspension. |
| D22 | [Workflow events / PRs][D22] | Fork token limitations, event revision semantics, and trigger security. |
| L01 | [github/local-action][L01] | JS/TS source debugging, supported Node/toolkit versions, command shape, and bundling limitations. |
| L02 | [act usage][L02] | Specific workflow/job selection, events, fake inputs, and local configuration. |
| L03 | [act unsupported functionality][L03] | Never treat emulator success as hosted permission/environment/concurrency enforcement. |
| L04 | [GitHub Local Actions VS Code extension][L04] | `act` UI integration, prerequisites, payloads, logs, runner mappings, and settings. |
| L05 | [nektos/act repository](https://github.com/nektos/act) | Version/release tracking and implementation changes. |

## Provenance, SBOM, and dependency submission

| ID | Resource | Use and update watchpoint |
| --- | --- | --- |
| S01 | [Attestation concepts][S01] | Meaning, limitations, when to sign, and need for verification. |
| S02 | [Generate provenance/SBOM attestations][S02] | Current `actions/attest` interface, permissions, subject digest/path, and SBOM predicates. |
| S03 | [gh attestation verify][S03] | Expected identity, signer workflow/repository, source constraints, predicates, and policy flags. |
| S04 | [Reusable workflows / SLSA][S04] | Trusted builder identity; do not claim compliance from signing alone. |
| S05 | [Dependency graph][S05] | Known repository dependencies versus artifact-specific inventory. |
| S06 | [Graph recognition and precedence][S06] | Static/automatic/manual submission, graph jobs, compute costs, and insight coverage. |
| S07 | [Export graph as SBOM][S07] | Current graph state, SPDX export, and asynchronous API behavior. |
| S08 | [Jesse Houwing: improved dependency submission][S08] | SHA/version and fork/upstream advisory-matching motivation. |
| S09 | [Submission action README][S09] | Features, lockfile integration, permissions, and experimental Docker detection. |
| S10 | [Submission action metadata][S10] | Executable inputs/defaults; takes precedence over conflicting prose for selected revision. |
| S10M | [Submission input interpretation][S10M] | Verify how strings/options become runtime configuration. |
| S11 | [SHA/fork resolver][S11] | Matching strategy, finite ref enumeration, unresolved SHAs, and upstream mapping. |
| S12 | [Dependency submitter][S12] | SHA plus version reporting, purls, graph relationships, snapshots, and detector identity. |
| S13 | [Submission/review integration][S13] | Base/head snapshots, sequencing, and permissions; adapt examples for forks safely. |
| S14 | [Dependabot alerts][S14] | Alert prerequisites and limits; detection is not a guarantee of automated repair. |
| S15 | [Dependency submission API guide][S15] | Build-time resolved dependencies and SBOM-to-snapshot submission. |
| S16 | [Supported graph ecosystems][S16] | Verify coverage and advisory matching; Docker references are not complete image scans. |
| S17 | [Dependency review action][S17] | Policy options, snapshot processing, versions, runtime requirements, and licensing. |

## Product and version gates from github/docs

These are pinned evidence of availability at research time, not promises for every later tenant/version.

| ID | Source | Check before each class |
| --- | --- | --- |
| F01 | [Cache-mode feature gate][F01] | Source marks GitHub.com/Cloud support, not GHES. |
| F02 | [Merge-queue availability][F02] | Organization ownership and public/private plan requirements. |
| F03 | [Required-workflow gate][F03] | Enterprise Cloud and supported GHES versions. |
| F04 | [Attestation availability][F04] | Public current plans; Enterprise Cloud for private/internal repositories. |
| F05 | [Ruleset availability][F05] | Repository visibility, plan, and rule-specific differences. |
| F06 | [Metrics feature gate][F06] | Cloud/Server differences in addition to view permissions. |

## Known issues and qualifications to preserve

1. `cache-mode` and native parallel-step syntax are current documented behavior; do not replace them with older assumptions when refreshing examples.
2. Cache outputs are strings. Package-download caching does not justify skipping `npm ci`.
3. Stack metadata and native stack rule evaluation differ from older manual branch-chain patterns.
4. Merge limits do not guarantee combined CI builds. Required checks must run on `merge_group`.
5. Action archive cache, tool cache, dependency cache, Docker store, and release artifact are different mechanisms.
6. `toJSON(secrets)` is not a safe diagnostic recommendation.
7. `act` does not reproduce GitHub's full security/control plane.
8. Graph-exported SBOMs are not necessarily the inventory of a particular shipped artifact.
9. Verify attested bytes and expected identity; a signature is not proof of vulnerability freedom.
10. At the inspected submission-action revision, the README table and `action.yml` disagree on the `report-transitive-as-direct` default. Set it explicitly and verify relationships.
11. The inspected resolver limits tag/branch enumeration; unresolved version mappings must remain visible.
12. Experimental Docker reference detection must not be presented as complete container inventory/advisory coverage.
13. Submission requires write access; the blog's combined PR example must not be copied as a universally fork-safe workflow.
14. Updated secure-use Docs prefers action dependency lockfiles for onboarded workflows; reusable-workflow references remain a separate pinning concern.
15. Changed-file selection is an impact model, not just a glob: include shared inputs, preserve mandatory checks, and fail closed or run full validation if detection fails. Re-evaluate the combined revision in merge queue.
16. Native path-filter diff limits vary by product/version; use current D23 rather than hard-coding an old file-count assumption.
17. Set explicit job and appropriate step budgets using observed timings with headroom. The default job timeout is 360 minutes, not a recommended budget; hard cancellation does not guarantee diagnostic uploads.
18. Bare `pull_request:` selects `opened`, `synchronize`, and `reopened`; `edited` is not a default and does not stand in for pushed commits. Metadata-only workflows and code CI need different activity sets. Account for base-branch edits and `ready_for_review` if their behavior affects validation.
19. Default-branch execution, cache restore visibility, and cache write scope are different. Current default-scope write-eligible events are `push`, `workflow_dispatch`, `repository_dispatch`, `delete`, `registry_package`, `page_build`, and `schedule`; low-trust default-context events are read-only unless explicitly overridden. Ordinary PR saves remain merge-ref scoped. Review D02 and D22 before teaching this boundary.

## Updating the class when GitHub evolves

Before each delivery, and after relevant announcements:

1. Start with the live implementation docs and record new source revisions/date. Keep older pinned links as historical evidence rather than silently rewriting the research baseline.
2. Recheck the product gates, selected tenant, runner version, action runtimes, local-tool versions, and schema validators.
3. Review the watchpoints above, especially cache defaults, native parallel semantics, native stacks, queue behavior, `snapshot`, lockfiles, attestations, and graph submission.
4. Review the current submission action's metadata and source when prose differs; confirm whether previously noted discrepancies were fixed.
5. Update starter/solution examples together, including dependency lockfiles, image seeds, tool caches, and exact action archives.
6. Rerun cold/warm, changed-file/shared-input/detection-failure, timeout/cancellation, PR/fork, stack/queue, required-gate, tamper, and wrong-signer cases. A documentation refresh is not runtime validation.
7. Remeasure comparable workloads and update screenshots/metrics without presenting selected best runs as representative.
8. Record changes in the log below and update the outline if the new behavior changes the learning objectives.

| Date | Scope | Result |
| --- | --- | --- |
| 2026-11-10 | Initial topic research, public source review, and fundamentals comparison | Source register and four-section outline proposed; live lab implementation/validation still pending. |
| 2026-11-10 | User-supplied community guidance | Reviewed changed-file conditions and timeouts against official docs; incorporated into section 2 and reinforced in sections 3-4 without extending the day. |
| 2026-11-10 | User-provided Intermediate and June 2025 GH200 materials | Preserved local source locators, selected slide/module anchors, delivery patterns, and freshness caveats; adapted original facilitation guidance without copying slides or expanding the schedule. |
| 2026-11-10 | User-directed regrouping and event filtering | Moved prewarming into section 1 with caching; section 2 now starts with event activity selection before file-impact filtering. Retained four 105-minute sections and distinguished `edited` from `synchronize`. |
| 2026-11-10 | Issue-based activity experiment | Replaced the hands-on PR activity experiment with opening/editing/labeling/commenting on issues; retained PR defaults as a brief transfer example. |

[W01]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/docs/framework-overview.md
[W02]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/effective-ci.md
[W03]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/productivity/recommendations/engineering-system-metrics.md
[W04]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/application-security/recommendations/actions-security.md
[W05]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/governance/recommendations/managing-repositories-at-scale/rulesets-best-practices.md
[W06]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/deploying-actions-runner-controller.md
[W07]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/hosted-runner-private-networking.md
[W08]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/designing-resilient-ci-cd.md
[W09]: https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/collaboration/recommendations/scaling-actions-reusability.md
[D01]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
[D01S]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/content/actions/reference/workflows-and-actions/workflow-syntax.md#L1078-L1235
[D02]: https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
[D03]: https://github.com/actions/cache#outputs
[D04]: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations
[D05]: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
[D06]: https://docs.github.com/en/actions/concepts/runners/larger-runners
[D07]: https://docs.github.com/en/actions/how-tos/manage-runners/larger-runners/use-custom-images
[D08]: https://docs.github.com/en/actions/concepts/runners/larger-runners#billing
[D09]: https://docs.github.com/en/actions/concepts/metrics
[D10]: https://docs.github.com/en/actions/how-tos/administer/view-metrics
[D11]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
[D12]: https://docs.github.com/en/pull-requests/reference/stacked-pull-requests
[D13]: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests
[D14]: https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests
[D15]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
[D16]: https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-workflows-to-pass-before-merging
[D17]: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
[D18]: https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging
[D19]: https://docs.github.com/en/actions/reference/security/secure-use
[D19C]: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context
[D20]: https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles
[D21]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands
[D22]: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request
[A01]: https://github.com/actions/action-versions/blob/e3c62146623237ce0e50fbb68f09fc0c4739446a/README.md
[A02]: https://github.com/actions/runner/blob/310a370bf3605f5b092f8af63b3126627de2a210/src/Runner.Worker/ActionManager.cs#L1232-L1305
[A03]: https://www.kenmuse.com/blog/building-github-actions-runner-images-with-an-action-archive-cache/
[A04]: https://www.kenmuse.com/blog/building-github-actions-runner-images-with-a-tool-cache/
[P01]: https://docs.npmjs.com/cli/v11/commands/npm-ci/
[P02]: https://learn.microsoft.com/en-us/nuget/consume-packages/managing-the-global-packages-and-cache-folders
[L01]: https://github.com/github/local-action
[L02]: https://nektosact.com/usage/index.html
[L03]: https://nektosact.com/not_supported.html
[L04]: https://marketplace.visualstudio.com/items?itemName=SanjulaGanepola.github-local-actions
[S01]: https://docs.github.com/en/actions/concepts/security/artifact-attestations
[S02]: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
[S03]: https://cli.github.com/manual/gh_attestation_verify
[S04]: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating
[S05]: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph
[S06]: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph-data
[S07]: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom
[S08]: https://jessehouwing.net/github-actions-improved-dependency-submission/
[S09]: https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md
[S10]: https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/action.yml
[S10M]: https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/main.ts
[S11]: https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/fork-resolver.ts
[S12]: https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/dependency-submitter.ts
[S13]: https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/docs/dependency-review.md
[S14]: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts
[S15]: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/use-dependency-submission-api
[S16]: https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems
[S17]: https://github.com/actions/dependency-review-action
[F01]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/features/actions-cache-mode.yml
[F02]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/merge-queue.md
[F03]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/features/repo-rules-required-workflows.yml
[F04]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/attestations.md
[F05]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/repo-rules.md
[F06]: https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/features/actions-metrics.yml
[D23]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onpushpull_requestpull_request_targetpathspaths-ignore
[D24]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idtimeout-minutes
[D25]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepstimeout-minutes
[B01]: https://github.com/austenstone/github-actions-best-practices/blob/c069cad06a06b7fc7cf25d528f997a31d066a36b/README.md
[B02]: https://github.com/dorny/paths-filter/blob/f3360c560367c9daf72b88c0e6164162034c5721/README.md
[B03]: https://github.com/tj-actions/changed-files/tree/9426d40962ed5378910ee2e21d5f8c6fcbf2dd96
[D26]: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onevent_nametypes
[D27]: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issues
[D28]: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment
