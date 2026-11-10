# 🔨 Lab 9: Verify, then promote

**Time:** About 30 minutes.

**Before you start:** Check that Actions and artifact attestations are available in your lab repository. You will run reviewed code from the default branch. Private/internal attestations need an eligible Enterprise Cloud plan.

You also need permission to create the `lab-release` environment. Staging is a temporary local server inside a GitHub-hosted job; no paid custom runner or real cloud target is needed.

**If attestation or staging is unavailable:** Ask the trainer to demonstrate that part. On an enterprise host, use its supported verifier and the account selected during setup.

## Objectives

Verify the subject bytes and expected signer, show tamper and wrong-identity rejection, then promote the same trusted bytes without deploying to a real cloud.

## Tasks

1. Copy the `09-release.yml` starter into `.github/workflows`. Keep its default-branch restriction, archive/digest handoff and cache-disabled promotion.

   Complete the build TODOs: generate an npm SBOM for `app/dist`, save it outside that directory, and attest both build provenance and the SBOM for the same `application.tgz`. Include the SBOM in the uploaded artifact.

   Add only the build-job permissions required by the attestation action. Create the course `lab-release` environment, generate and review the lockfile, then commit and push to your default branch. [Attestation permissions and inputs](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations), [action versions](../ACTION-VERSIONS.md), [Lab 8 inventory](08-Dependencies.md)

   Tasks 3–5 explain the remaining TODOs. Your first run will fail at a placeholder until you implement them; replace the placeholders with checks rather than simply removing the errors.

2. Once your build uploads the `release` artifact, download it into a new temporary directory. Note `build_archive_sha256` from the log and calculate the downloaded `application.tgz` digest yourself: use `sha256sum application.tgz` on Linux or `Get-FileHash application.tgz -Algorithm SHA256` in PowerShell.

   Inspect what the attestation identifies and what it claims. The expected workflow is **your** `OWNER/REPOSITORY/.github/workflows/09-release.yml`, using source ref `refs/heads/main` (or your adjusted branch) and the exact run commit. [Verify attestations](https://cli.github.com/manual/gh_attestation_verify)

3. Complete **Verify bytes and expected identity**. Calculate the downloaded archive's digest, print it and compare it with `EXPECTED_DIGEST`. Use `gh attestation verify` separately for provenance and the SBOM.

   Restrict verification to your expected repository, signer workflow, source ref, run commit and hosted runner. Use the supplied environment values and your own host/account, not names from the walkthrough. The [verifier documentation](https://cli.github.com/manual/gh_attestation_verify) lists the flags and predicate identifiers.

   Verification must finish before extraction or execution. Missing or mismatched evidence should stop promotion. Repeat verification on your local download and note the constraints and result.

4. After valid verification works, add two tests that should be rejected: change bytes in a **copy** of the archive, and verify an unchanged copy while requiring the wrong signer.

   Keep the original untouched. Make the job fail if either invalid case is accepted. Repeat the tests on your local download and check that the rejection is due to the digest or identity, not a network or authentication problem.

5. Complete **Promote the verified archive**. After verification, extract the original downloaded archive without rebuilding or installing anything. Start its server, wait a limited time for `/health`, check the JSON response and always stop the server when the script exits. Keep the job timeout too.

   Reuse your Lab 6 approach or consult [Bash traps](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html#index-trap). Before extraction, compare `promotion_archive_sha256` and `expected_sha256` with the build and download digests. Hash the archive, not the extracted directory.

   Why would rebuilding the app break the claim that you promoted the same bytes?

<details>
<summary>Hint</summary>

Ask three questions: Is this the file I built? Did the expected workflow sign the statement? Does the statement contain the claim I want to verify?

An attestation from a different builder can have a valid signature and still be the wrong evidence for your release.
</details>

<details>
<summary>Solution</summary>

The [completed workflow](../solutions/workflows/09-release.yml) builds `application.tgz` once and uses `actions/attest@v4.2.2` to record two statements about it: how it was built and which npm components it contains.

The build job has `contents: read`, `id-token: write` and `attestations: write`. Those permissions let it read the code, obtain an identity token and create attestations. They are not granted to every job.

The promotion job calculates the downloaded archive's SHA-256 and compares it with the build job's value. It then verifies the two attestation types separately:

| Statement | Predicate type used by the verifier |
| --- | --- |
| Build provenance: where and how the archive was built | `https://slsa.dev/provenance/v1` |
| Component inventory in SPDX format | `https://spdx.dev/Document` |

A **predicate type** tells the verifier which kind of claim to check. The [verification flags](https://cli.github.com/manual/gh_attestation_verify) also restrict the expected repository, signer workflow, source branch, commit and hosted runner.

The altered-copy test should fail because its digest no longer matches. The wrong-signer test should fail because the trusted identity does not match. An authentication or network error would not demonstrate either protection.

After verification and both rejection tests, promotion extracts the original archive and starts the app without rebuilding it. Matching archive digests show that the build and promotion used the same bytes. This establishes identity and integrity, not the absence of vulnerabilities.
</details>

## Success and cleanup

Keep the matching build/download/promotion digests, successful signer verification and both rejected test cases. Check why each invalid case failed.

Remove your altered archive copy and temporary local output. Leave shared artifacts, attestations and releases alone.

Cancel unneeded course runs and disable **Lab 09 verified promotion**; it is not used again. Remove your `lab-release` environment once no job is using it.

Finish with [cleanup](10-Cleanup.md).
