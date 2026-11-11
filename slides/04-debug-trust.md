# Find failures and deploy verified files
- Inspect relevant logs without exposing secrets
- Record which packages and actions the project uses
- A digest is a file's fingerprint: it changes when the contents change
- Verify where the release came from, then deploy that exact file

<!-- notes: Timing 0-5 min. Open module 4 with the final pipeline question: how do we diagnose efficiently and deliver verified bytes? State that local tools are an instructor demo, not required learner installations. Expected evidence: learners distinguish debugging evidence from artifact integrity evidence. Failure/recovery: demonstrate with a supported trainer release workflow if the participant setup is unavailable. Otherwise explain provenance and verification without claiming a promotion occurred. Docs: [D18](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [W08](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/designing-resilient-ci-cd.md). -->

---

# Start with the failed step's logs
- Read the error and the few details needed to explain it
- `ACTIONS_STEP_DEBUG` enables more detailed step logs
- Runner debug logs help diagnose the runner itself
- Check whether work failed, reached a time limit or was cancelled
- Save useful logs before the job's time limit expires

<!-- notes: Timing 5-10 min. Explain step vs runner debug and the appropriate rerun/settings path. Repository/org permissions may be required to set debug flags; use prepared debug-enabled evidence if not available. Hard cancellation can prevent diagnostics and cleanup, so capture bounded evidence early. Expected evidence: learners select the smallest useful diagnostic level and classify the outcome. Failure/recovery: if detailed logs expose too much, stop sharing them, remove/redact the exposure, and use an allowlisted rerun. Docs: [D18](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [D24](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idtimeout-minutes), [D25](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepstimeout-minutes). -->

---

# Print only the details you need
- Context means the run's available data; do not print it all or expose secrets

## Diagnostic solution excerpt: choose only evidence you need
```yaml
- name: Selected diagnostics
  run: |
    echo '::group::Selected tool and path evidence'
    node --version
    npm --version
    find app/src app/test -maxdepth 2 -type f
    echo '::endgroup::'
```

<!-- notes: Timing 10-15 min. Demonstrate allowlisted event/ref/sha values and safe environment-variable handling. GitHub context includes sensitive and attacker-influenced fields. Do not interpolate issue/PR fields or filenames into shell source; pass structured values via environment and validate. Masking can fail for transformed/structured secrets. Expected evidence: one useful diagnostic that avoids secrets and uncontrolled event text. Failure/recovery: if sensitive data is printed, stop, restrict log access, rotate affected credentials where appropriate, and replace the example with fake values only. Docs: [D19](https://docs.github.com/en/actions/reference/security/secure-use), [D19C](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context), [D21](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands). -->

---

# Lab 7: Find the real failure
- Compare the failing path with the files actually present

## Fill in your diagnosis from the starter's failed run
```text
First failing command: _____________________

Smallest useful diagnostic: ________________
What did the diagnostic establish? _________

Cause: ___________________________________
Correction and new run revision: ___________
```

<!-- notes: Timing 15-25 min. Copy the deliberately failing starter, not the completed reference. Learners diagnose its check, add bounded grouped evidence and a debug-gated message, then dispatch and debug-rerun the same failing revision. Do not reveal the corrected path before they inspect evidence. The solution checks app/src/server.js instead of app/src/serve.js; the panel is a worksheet, not captured output. Commit the fix and dispatch a new revision; Rerunning old code retains the failure. Earlier test results in VALIDATION-STATUS.md used the older completed checkpoint, not a rehearsal of this revised starter. Never dump environment/context or secrets. Disable diagnostics after success. Docs: [D18](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [D19](https://docs.github.com/en/actions/reference/security/secure-use), [D21](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands). -->

---

# Check that the fix addresses the cause
- Was the cause a wrong path, missing file or time limit?
- Which log message supports that explanation?
- Dispatch the corrected revision; rerunning the old one retains its typo
- Could unreviewed PR text or a filename change a shell command?

<!-- notes: Timing 25-35 min. Finish Lab 7 with peer explanation and one verification run. Expected evidence: root cause, safe evidence, minimal correction, and outcome on the same relevant scenario. Failure/recovery: when a green run lacks the expected evidence, mark the diagnosis unverified and rerun with a narrow diagnostic; do not equate edited code with resolution. Docs: [D19](https://docs.github.com/en/actions/reference/security/secure-use), [D21](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands). -->

---

# What local tests cannot prove
- Local tools help you try changes; test GitHub's rules on GitHub

## A passing result proves only what the tool actually tested
| Tool or test | What it can show | What it does not prove |
| --- | --- | --- |
| github/local-action | Test action source code locally | Whole workflow or merge rules |
| act | Run selected jobs locally | All GitHub permissions and features |
| GitHub training run | Real event and runner | Other hosts or plans |
| Test a repository rule | This case is blocked or allowed | Cases not tested |

<!-- notes: Timing 35-45 min. Instructor demonstration only: show `github/local-action` on unbundled JS/TS action logic, then a selected workflow/job through `act` or its VS Code extension. Do not install tools during class. Local runs do not prove rulesets, real token permissions, OIDC, environments, merge queues, or new server syntax. Expected evidence: learners name what local feedback can accelerate and what still needs hosted verification. Failure/recovery: if a tool or runner mapping fails, show prepared local output and proceed to hosted evidence; don't present emulator success as platform validation. Docs: [L01](https://github.com/github/local-action), [L02](https://nektosact.com/usage/index.html), [L03](https://nektosact.com/not_supported.html), [L04](https://marketplace.visualstudio.com/items?itemName=SanjulaGanepola.github-local-actions). -->

---

# What software records can tell you
- A software bill of materials (SBOM) lists components
- An attestation is a signed statement about a file; its predicate is the content, such as an SBOM or provenance

## Four records; none alone proves the software is safe
| Record | What it tells you | Limit |
| --- | --- | --- |
| Dependency graph | Known packages and actions | Some may be missing |
| Dependency submission | Adds details to that graph | Only the submitted data |
| SBOM: software bill of materials | Components in a release | Must match the delivered file |
| Attestation | Who signed a claim about a file | Not a quality review |

<!-- notes: Timing 45-50 min. Start Lab 8 by distinguishing dependency graph, dependency submission, SBOM, and attestation. Submission enriches GitHub's dependency inventory; an SBOM describes a scoped inventory; provenance attestation binds claims to a subject digest and identity. Expected evidence: learners identify the question each evidence type answers and one limitation. Failure/recovery: if dependency graph indexing is delayed, use the prepared indexed snapshot and state the delay. Docs: [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [S05](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph), [S06](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph-data), [S07](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom). -->

---

# Lab 8: Improve the dependency inventory
- Requires: repository admin if the dependency graph needs to be enabled
- Pinning selects exact action code using its commit SHA
- Find that action in GitHub's dependency graph
- Compare its commit identifier with its release version
- Complete trusted submission, verified-lock inputs and job permissions
- Compare your graph exports with the staged app's npm SBOM
- Do not give a fork PR extra permissions to make submission work

<!-- notes: Timing 50-57 min, pending a fresh timed starter rehearsal. Export the participant graph before submission, then implement the starter's missing submission action, explicit relationship/verifier inputs and minimum job-only write permission using linked docs. Do not copy the completed reference initially. Lock/review/dispatch trusted main; inspect verified-lock and submission logs, then export after indexing. Reference solution uses actions-lock-version v0.4.1 and report-transitive-as-direct false; verification failure is not an acceptable warning. Existing detectors can make counts unchanged; entries repeat across manifests. Historical 15 -> 56 entries were not 56 unique shipped components. Never broaden a fork token. The trainer can demonstrate submission in a trusted trainer repository if participants cannot run it. Docs: [S08](https://jessehouwing.net/github-actions-improved-dependency-submission/), [S09](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md), [S10](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/action.yml), [S13](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/docs/dependency-review.md), [D20](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles). -->

---

# Record what the dependency list cannot tell you
- If the README and action input defaults differ, set the input explicitly
- Verify the lockfile; record unresolved versions and duplicate entries
- Docker image detection is experimental and may miss images
- Package inventories do not enumerate every shipped file or OS component

<!-- notes: Timing 57-65 min. Generate the staged app's npm SPDX inventory using the lab commands and save it outside dist. In a test run the inventory contained actions-advanced-lab and picocolors; repository graph also included workflow actions and course tooling. Neither lists every shipped file, OS library or potential advisory. report-transitive-as-direct defaults differ between README prose and metadata at the inspected revision; set explicitly and verify relationships. Unresolved version/upstream mappings and experimental Docker detection remain limitations. Disable the Lab 8 workflow after export, preserve unrelated graph automation and evidence, and never delete another detector's snapshots. Docs: [S09](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md), [S10](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/action.yml), [S11](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/fork-resolver.ts), [S12](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/dependency-submitter.ts), [S07](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom). -->

---

# Lab 9: Build once, verify, then deploy
- Requires: repo admin for the environment; GHEC for private or internal repositories

## A SHA-256 checksum is the file fingerprint; provenance records how that same file was built
```flow
Build once | Build application.tgz; record its SHA-256.
Attest | Sign provenance and an SBOM for this file.
Verify | Check the file, signer, source and statement.
Deploy | Use that same file; do not rebuild.
```

<!-- notes: Timing 65-73 min, pending a fresh timed starter rehearsal. Learners complete 09-release.yml evidence, verification and negative-test TODOs, retaining the supplied promotion step, build/archive handoff and empty root permissions. Consult the collapsed completed reference only after attempting implementation. Generate staged npm SBOM, attest both predicates for application.tgz and verify before any extraction. The build job needs id-token: write and attestations: write. Review minimum permissions, lock and create course-only lab-release before dispatching reviewed main. Incomplete barriers deliberately fail. Public attestations are supported on current plans; private/internal need GHEC. Verify actual host/tenant and separate EMU setup. If eligibility or indexing blocks the participant run, the trainer can demonstrate with an authorized workflow. Distinguish that demonstration from the participant's build; never substitute different bytes to claim their verification passed. No external staging target is required. Docs: [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [S02](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [F04](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/attestations.md), [S03](https://cli.github.com/manual/gh_attestation_verify). -->

---

# Verify the file and the signing workflow
- Subject means the file being verified; predicate type identifies the kind of statement

## Release solution excerpt: verify before unpacking
```bash
# PowerShell: (Get-FileHash -Algorithm SHA256 application.tgz).Hash
test "$(sha256sum application.tgz | cut -d ' ' -f 1)" = "$EXPECTED_DIGEST"
gh attestation verify application.tgz --repo "$REPOSITORY" \
  --signer-workflow "$REPOSITORY/.github/workflows/09-release.yml" \
  --source-ref refs/heads/main --source-digest "$EXPECTED_SHA" \
  --predicate-type https://slsa.dev/provenance/v1 --deny-self-hosted-runners
```

<!-- notes: Timing 73-81 min. The panel shows only provenance; the full workflow separately verifies the SPDX SBOM predicate. Bind each to application.tgz, the participant repository's exact signer workflow, source ref, source commit and hosted runner. Compare build_archive_sha256, promotion_archive_sha256 and the independently downloaded inner archive. The upload-artifact transport ZIP has a different digest and is not the attested subject. On PowerShell use (Get-FileHash -Algorithm SHA256 application.tgz).Hash.ToLower() rather than assuming sha256sum exists. Keep the workflow path unchanged unless signer constraints are reviewed together. A valid signature is not a vulnerability assessment. Stop on missing or mismatched evidence; never weaken constraints until green. Docs: [S03](https://cli.github.com/manual/gh_attestation_verify), [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [S04](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating). -->

---

# Test tampering without secrets
- Tampering means changing a file; test a copy and keep the original unchanged

## Expected results, not results from an actual test run
| File or record | Required signer | Expected result |
| --- | --- | --- |
| Original application.tgz | Approved release workflow | Accept only if every check passes |
| Copy with changed contents | Approved release workflow | Reject: file contents differ |
| Original application.tgz | not-the-signer.yml | Reject: wrong signing workflow |
| No usable attestation | Approved release workflow | Stop; do not deploy without verification |

<!-- notes: Timing 81-89 min. Use a downloaded copy and non-secret test input only. Expected evidence: tampered bytes fail digest/provenance verification while the original artifact remains unchanged. Failure/recovery: if the original was overwritten, delete the changed copy and recover from the immutable prepared artifact; do not upload modified content as the promoted release. Docs: [S02](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [S03](https://cli.github.com/manual/gh_attestation_verify), [D19](https://docs.github.com/en/actions/reference/security/secure-use). -->

---

# Deploy the exact file you verified
- Promotion means moving a verified release to the next environment
- Use only the artifact that passed verification; do not rebuild it
- Disable the Actions package cache in the deployment job
- Give that job only the permissions and target it needs
- Match the application.tgz digest, not the artifact-service ZIP digest

<!-- notes: Timing 89-95 min. The lab-release job verifies, extracts and starts the exact downloaded archive on its job runner, checks /health and stops that process via a trap. This is local promotion rehearsal, not proof of external cloud or production deployment. No rebuild or npm install occurs after verification; cache-mode is none and permissions are minimal. Compare archive digests across build, independent download and promotion; mismatch stops promotion. Preserve the evidence, remove tampered copies, disable Lab 09 attested release and remove only the idle course-owned environment. Docs: [S02](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [S03](https://cli.github.com/manual/gh_attestation_verify), [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [D19](https://docs.github.com/en/actions/reference/security/secure-use). -->

---

# Final exercise: Explain your workflow choices
- Compare time until results and total runner-minutes with the baseline
- Explain your cache settings, job design and merge rules
- Explain what dependency lists and signed build records do not prove
- State which results were observed and which remain untested
- Check back on Lab 3 before cleanup; account for pending paid resources

<!-- notes: Timing 95-98 min. Use the scheduled capstone discussion, then switch to 99-conclusion for minutes 98-105. Learners compare baseline and optimized run evidence, explain an optimization without weakening required gates, and distinguish dependency graph/SBOM/provenance claims. Expected evidence: a measured pipeline decision with known limitations and a verified artifact chain. Failure/recovery: if a live measure or signature check was unavailable, name it as unresolved and cite the prepared fallback; never claim runnable validation from these slides. The conclusion covers cleanup, paid-resource ownership, Q&A, MTM feedback and Microsoft Learn completion. Docs: [D09](https://docs.github.com/en/actions/concepts/metrics), [D10](https://docs.github.com/en/actions/how-tos/administer/view-metrics), [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [W08](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/designing-resilient-ci-cd.md). -->
