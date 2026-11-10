# Find failures and deploy verified files
- Inspect relevant logs without exposing secrets
- Record which packages and actions the project uses
- A digest is a file's fingerprint: it changes when the contents change
- Verify where the release came from, then deploy that exact file

<!-- notes: Timing 0-5 min. Open module 4 with the final pipeline question: how do we diagnose efficiently and deliver verified bytes? State that local tools are an instructor demo, not required learner installations. Expected evidence: learners distinguish debugging evidence from artifact integrity evidence. Failure/recovery: if the prepared release target is unavailable, inspect recorded provenance and verification evidence; do not claim a live promotion occurred. Docs: [D18](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [W08](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/designing-resilient-ci-cd.md). -->

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

## From 07-debug.yml: tool versions and files in two known folders
```yaml
- name: Selected diagnostics
  run: |
    echo '::group::Selected tool and path evidence'
    node --version
    npm --version
    find app/src app/test -maxdepth 2 -type f
    echo '::endgroup::'
```

<!-- notes: Timing 10-15 min. Demonstrate allowlisted event/ref/sha values and safe environment-variable handling. GitHub context includes sensitive and attacker-influenced fields. Do not interpolate issue/PR fields or filenames into shell source; pass structured values via environment and validate. Masking can fail for transformed/structured secrets. Expected evidence: one useful diagnostic that avoids secrets and uncontrolled event text. Failure/recovery: if sensitive data is printed, stop, restrict log access, rotate affected credentials where appropriate, and replace the example with a fake-only fixture. Docs: [D19](https://docs.github.com/en/actions/reference/security/secure-use), [D19C](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context), [D21](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands). -->

---

# Lab 7: Find the real failure
- Check whether the file is in a different folder or was never created

## Example diagnosis, not output captured from a runner
```text
Failure: test -f app/source/server.js -> exit 1

Files found in the selected folders:
  app/src/server.js
  app/test/server.test.js

Cause: the folder is src, not source.
Correction: test -f app/src/server.js
Verify: rerun the same example and inspect the check result.
```

<!-- notes: Timing 15-25 min. Launch Lab 7. The prepared failure is an incorrect path/configuration or missing output, never a secret leak. Learners add targeted version/path/tree evidence, inspect grouped logs, and enable the appropriate debug flag if permitted. Demo checkpoint: compare initial failure with the fixed run. Expected evidence: root cause explained using safe logs; no environment dump, full event payload, or secret output. Failure/recovery: restore the starter checkpoint if edits obscure the root cause; use instructor debug logs if repo settings are inaccessible. Docs: [D18](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [D19](https://docs.github.com/en/actions/reference/security/secure-use), [D21](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands). -->

---

# Check that the fix addresses the cause
- Was the cause a wrong path, missing file or time limit?
- Which log message supports that explanation?
- Does the fix preserve what the check is meant to do?
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
- An SBOM lists components; an attestation is a signed statement

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
- Pinning selects exact action code using its commit SHA
- Find that action in GitHub's dependency graph
- Compare its commit identifier with its release version
- Add dependency details only from a reviewed workflow
- Do not give a fork PR extra permissions to make submission work

<!-- notes: Timing 50-57 min. Use the trusted-branch dependency submission demonstration. Immutable SHA pinning protects what executes; version enrichment helps advisory matching. Submission needs write access, so do not grant a fork PR a broad token. Confirm base/head snapshot sequencing. Expected evidence: learners explain the pinned action and its version visibility, with any unresolved mapping recorded. Failure/recovery: if indexing is delayed or no write permission is available, use prepared graph evidence; never widen fork permissions to make the lab work. Docs: [S08](https://jessehouwing.net/github-actions-improved-dependency-submission/), [S09](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md), [S10](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/action.yml), [S13](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/docs/dependency-review.md), [D20](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles). -->

---

# Record what the dependency list cannot tell you
- If the README and action input defaults differ, set the input explicitly
- Record action commits that cannot be matched to a release version
- Docker image detection is experimental and may miss images
- A repository SBOM may not describe the files in the release

<!-- notes: Timing 57-65 min. Note the inspected action revision has a README/action.yml default discrepancy for `report-transitive-as-direct`; set it explicitly and verify relationships. Resolver ref enumeration is finite, so unresolved versions must remain visible. Experimental Docker reference detection is not complete image inventory or advisory coverage. Compare repository graph SBOM with an artifact-specific inventory. Expected evidence: learners can state what remains unknown rather than overclaim coverage. Failure/recovery: if submission output does not match README prose, trust the inspected action metadata/source and record revision. Docs: [S09](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/README.md), [S10](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/action.yml), [S11](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/fork-resolver.ts), [S12](https://github.com/jessehouwing/actions-dependency-submission/blob/811981eec3c108f41783f194522fde91a34301a4/src/dependency-submitter.ts), [S07](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/export-dependencies-as-sbom). -->

---

# Lab 9: Build once, verify, then deploy
- Private/internal attestations need GitHub Enterprise Cloud; use a test deployment

## Provenance records where and how a file was built; d is its example digest
```flow
Build once | Reviewed main creates application.tgz with digest d.
Sign records | Provenance and SBOM statements both refer to digest d.
Verify | Check the digest, signing workflow, source and statement type.
Deploy | Send that same file to the test target; do not rebuild it.
```

<!-- notes: Timing 65-73 min. Launch Lab 9 using the prepared release workflow and disposable staging target. Attestation availability: public repositories on current plans; private/internal repos require Enterprise Cloud per the current feature gate. GHEC REQUIRED for private/internal repository attestation in this lab; verify actual tenant, host, and region. EMU SETUP / GHE.COM SETUP where those identity/host configurations apply. DEMO / FALLBACK: instructor uses eligible repo and presents verification results. Deployment uses `cache-mode: none`; do not promote untrusted PR artifacts. Expected evidence: one artifact digest flows from build through verification to staging. Failure/recovery: if attestation generation or indexing is delayed, use a prepared artifact and captured evidence; do not substitute a different build. Docs: [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [S02](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [F04](https://github.com/github/docs/blob/15f068380afe64f9d87ef55ec24d590eb9e055da/data/reusables/gated-features/attestations.md), [S03](https://cli.github.com/manual/gh_attestation_verify). -->

---

# Verify the file and the signing workflow
- Subject means the file being verified; predicate type identifies the kind of statement

## From 09-release.yml: verify before unpacking; workflow supplies expected values
```bash
test "$(sha256sum application.tgz | cut -d ' ' -f 1)" = "$EXPECTED_DIGEST"
gh attestation verify application.tgz --repo "$REPOSITORY" \
  --signer-workflow "$REPOSITORY/.github/workflows/09-release.yml" \
  --source-ref refs/heads/main --source-digest "$EXPECTED_SHA" \
  --predicate-type https://slsa.dev/provenance/v1 --deny-self-hosted-runners
```

<!-- notes: Timing 73-81 min. Demonstrate verification against the exact artifact and expected signer identity. A valid signature does not establish that the artifact is vulnerability-free or that the workflow was appropriately reviewed. Expected evidence: verifier accepts the expected identity and digest, rejects an unexpected signing identity, and learner explains what remains unproven. Failure/recovery: if expected identity fields are ambiguous, stop promotion and consult verifier guidance; do not weaken identity constraints until it passes. Docs: [S03](https://cli.github.com/manual/gh_attestation_verify), [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [S04](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating). -->

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

<!-- notes: Timing 81-89 min. Use a disposable downloaded copy and non-secret fixture only. Expected evidence: tampered bytes fail digest/provenance verification while the original artifact remains unchanged. Failure/recovery: if the original was overwritten, discard the disposable fixture and recover from the immutable prepared artifact; do not upload modified content as the promoted release. Docs: [S02](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [S03](https://cli.github.com/manual/gh_attestation_verify), [D19](https://docs.github.com/en/actions/reference/security/secure-use). -->

---

# Deploy the exact file you verified
- Promotion means moving a verified release to the next environment
- Use only the artifact that passed verification; do not rebuild it
- Disable the Actions package cache in the deployment job
- Give that job only the permissions and target it needs
- Confirm the deployed file has the expected digest or fixed release ID

<!-- notes: Timing 89-95 min. Finish Lab 9 by confirming staging received the same artifact digest or immutable release reference. Deployment job uses `cache-mode: none`, least privilege, and the intended environment. Never rebuild after verification and call it the same artifact. Expected evidence: digest continuity from build to verify to deploy. Failure/recovery: if the deployed digest is missing or differs, stop promotion, preserve evidence, and redeploy the verified artifact after correction; do not treat deployment approval alone as proof. Docs: [S02](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [S03](https://cli.github.com/manual/gh_attestation_verify), [D02](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [D19](https://docs.github.com/en/actions/reference/security/secure-use). -->

---

# Final exercise: Explain your workflow choices
- Compare time until results and total runner-minutes with the baseline
- Explain your cache settings, job design and merge rules
- Explain what dependency lists and signed build records do not prove
- State which results were observed and which remain untested

<!-- notes: Timing 95-105 min. Use the scheduled capstone/debrief. Learners compare baseline and optimized run evidence, explain an optimization without weakening required gates, and distinguish dependency graph/SBOM/provenance claims. Expected evidence: a measured pipeline decision with known limitations and a verified artifact chain. Failure/recovery: if a live measure or signature check was unavailable, name it as unresolved and cite the prepared fallback; never claim runnable validation from these slides. End-of-day cleanup: stop active runs, disable training schedules/workflows, remove course-owned artifacts/branches/environments, revoke temporary access, confirm paid runner/image/storage/network resources are deprovisioned, and coordinate shared policy cleanup with admins. Docs: [D09](https://docs.github.com/en/actions/concepts/metrics), [D10](https://docs.github.com/en/actions/how-tos/administer/view-metrics), [S01](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [W08](https://github.com/github/github-well-architected/blob/d7ff7ab0b225e189c18dadca53196b0d8bc19764/content/library/architecture/recommendations/designing-resilient-ci-cd.md). -->
