# 🔨 Lab 9: Verify, then promote

**Time:** 30 minutes. **Prerequisite:** your participant repository, trusted default branch and Actions/artifact-attestation availability. **GHEC REQUIRED:** private/internal artifact attestations require an eligible Enterprise Cloud plan; verify availability for your repository. **ADMIN REQUIRED:** permission to create the course-only `lab-release` environment if needed. No paid custom runner or cloud target is required: staging is an ephemeral local server in a GitHub-hosted job. **EMU SETUP / GHE.COM SETUP:** use the authorized repository, actual host and supported attestation verifier. **DEMO / FALLBACK:** use recorded evidence for unavailable issuance, verification or staging and state what remains unverified.

## Objectives

Verify the subject bytes and expected signer, show tamper and wrong-identity rejection, then promote the same trusted bytes without deploying to a real cloud.

## Tasks

1. Copy the `09-release.yml` starter into `.github/workflows`, retaining its trusted branch guard, archive/digest handoff and cache-disabled promotion. Complete the build TODOs: generate the staged npm SBOM outside `dist`, attest both provenance and that SBOM for the same `application.tgz`, and include the SBOM in the artifact. Use the taught attestation action/version and documentation to add only required build-job OIDC/attestation permissions. Complete verification and promotion in tasks 3-5 before expecting a passing run; explicit incomplete-step failures must not simply be deleted. Create only course-owned `lab-release`, review/lock and dispatch reviewed default-branch code. No cloud credentials/target are required. [Issuance and permission requirements](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [action versions](../ACTION-VERSIONS.md), [Lab 8 staged inventory](08-Dependencies.md)
2. From that run, download the `release` artifact to a new disposable directory. Record `build_archive_sha256` from the build log and independently compute the downloaded `application.tgz` digest (`sha256sum application.tgz` on Linux, `Get-FileHash application.tgz -Algorithm SHA256` on PowerShell). Inspect the attestation subject and predicate. Expected identity is **your** `OWNER/REPOSITORY/.github/workflows/09-release.yml`, source ref `refs/heads/main` (or your adjusted branch), and the exact run commit. [Verify attestations](https://cli.github.com/manual/gh_attestation_verify)
3. Implement **Verify bytes and expected identity**: independently compute the downloaded archive digest, log/compare it with `EXPECTED_DIGEST`, and use `gh attestation verify` for provenance and SBOM separately. Require your exact signer repository/workflow, source ref, run commit and hosted runner; use the approved host/account and the supplied environment values, not hardcoded walkthrough identities. Consult the verifier documentation for flags/predicate identifiers. Verify before extraction or execution; absent/mismatched/unverifiable evidence must block promotion. Independently repeat verification on the downloaded artifact and record constraints and exit status. [Verifier flags and predicates](https://cli.github.com/manual/gh_attestation_verify)
4. Implement copy-only tamper and wrong-signer negative tests after valid verification succeeds. Reject any unexpected acceptance. Test the same cases independently on your downloaded artifact. Confirm failure reasons are digest/identity, not auth/network outage. Never corrupt the original.
5. Implement **Promote the verified archive**: only after successful verification, extract the downloaded bytes without rebuilding/installing, start their server, bound `/health` polling and validate its JSON, and always stop the server on normal exit. Use the Lab 6 pattern you implemented or linked Bash trap documentation; retain the job timeout. Compare `promotion_archive_sha256`/`expected_sha256` with build/download digests before extraction, never a directory hash. Explain why rebuilding breaks same-byte promotion. [Bash traps](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html#index-trap)

<details>
<summary>Hint</summary>

Bind three things: bytes, trusted identity, and the intended predicate. A successful signature from an unexpected builder is not enough.
</details>

<details>
<summary>Solution</summary>

See the [completed release reference](../solutions/workflows/09-release.yml) and [verification flags](https://cli.github.com/manual/gh_attestation_verify). The reference uses `actions/attest@v4.2.2`, build-job `id-token: write`/`attestations: write`/`contents: read`, and separate SLSA (`https://slsa.dev/provenance/v1`) and SPDX (`https://spdx.dev/Document`) verification. It binds the downloaded digest to signer workflow, source ref/commit and hosted runner, then checks negative cases before local promotion. Both altered copy and wrong signer must fail for the intended reason. The local target receives original bytes without rebuild. These claims are not a vulnerability assessment.
</details>

## Success and cleanup

Record matching original/promoted digests, successful expected-signer verification and both negative results. Check that negative tests failed for the expected digest/identity reason, not an unrelated authentication or network failure. Delete only your disposable altered copy and local/mock course output; do not delete shared artifacts, attestations or releases. Cancel course-only runs and disable **Lab 09 verified promotion**; it is not needed afterward. Remove only the course-owned `lab-release` environment once no job is using it. Finish with [cleanup](10-Cleanup.md).
