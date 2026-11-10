# 🔨 Lab 9: Verify, then promote

**Time:** 30 minutes. **Prerequisite:** instructor-prepared trusted release, identity expectations, artifacts and verification evidence. **GHEC REQUIRED:** private/internal artifact attestations require an eligible Enterprise Cloud plan; verify availability for your repository. **PAID RUNNER / ADMIN REQUIRED:** any staging target and environment protection are pre-provisioned. **EMU SETUP / GHE.COM SETUP:** use the authorized repository, actual host and supported attestation verifier. **DEMO / FALLBACK:** use recorded evidence for unavailable issuance, verification or staging.

## Objectives

Verify the subject bytes and expected signer, show tamper and wrong-identity rejection, then promote the same trusted bytes without deploying to a real cloud.

## Tasks

1. Inspect `examples/workflows/09-release.yml` as inert text. With instructor preflight, identify the trusted release ref, build command, exact artifact, provenance and SBOM evidence, subject digest, token permissions, selected expected signer workflow/repository and cache-disabled promotion. Do not copy or dispatch it until the instructor confirms its trigger, permissions, environment and safe local/mock target. [Attestation concepts](https://docs.github.com/en/actions/concepts/security/artifact-attestations), [generating attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
2. From the prepared trusted release run, obtain the artifact and its provenance/SBOM evidence. Compute and record its digest; inspect the attestation subject and predicate. Compare to the expected trusted repository and exact signer workflow, not merely a valid signature. [Verify attestations](https://cli.github.com/manual/gh_attestation_verify)
3. Verify with the instructor's host-appropriate `gh attestation verify` invocation and expected signer constraints, or inspect the recorded command and output. Record the artifact digest, identity constraint, exit status, and corresponding provenance and SBOM evidence. An absent, unverifiable or mismatched attestation blocks promotion.
4. Copy the artifact to a separate disposable file, change the copy, and repeat verification against the original evidence. Confirm failure. Repeat with the unmodified artifact and an intentionally **wrong expected signer**; confirm rejection. Do not replace or corrupt the original release artifact.
5. Promote only the original verified bytes to the instructor's safe local/mock staging target, or trace the prepared demonstration. Compare the archive's digest at the promotion boundary to step 2 before extraction; do not compare a directory hash to an archive hash. Never promote untrusted PR artifacts; no cloud resource modification is required. Explain why verifying and rebuilding later would not demonstrate promotion of the same bytes.

<details>
<summary>Hint</summary>

Bind three things: bytes, trusted identity, and the intended predicate. A successful signature from an unexpected builder is not enough.
</details>

<details>
<summary>Solution</summary>

See the [release checkpoint](../examples/workflows/09-release.yml) and the [verification flags](https://cli.github.com/manual/gh_attestation_verify), particularly signer workflow/repository and predicate constraints supported by the installed version. Successful verification must bind the downloaded artifact's digest to the expected signer and provenance; check the SBOM predicate separately. The altered copy and wrong signer must both return a nonzero result. The mock target must receive bytes with the original digest. Attestation establishes an authenticated claim about the subject and builder, not that dependencies are safe or the artifact is vulnerability-free.
</details>

## Success and cleanup

Record matching original/promoted digests, successful expected-signer verification and both negative results. Delete only your disposable altered copy and local/mock course output; do not delete shared artifacts, attestations or releases. Cancel course-only runs. Finish with [cleanup](10-Cleanup.md).
