# 🔨 Lab 7: Find the failure without dumping secrets

**Time:** 20 minutes. **Prerequisite:** instructor's prepared failing run and [setup](00-Setup.md). **DEMO / FALLBACK:** inspect recorded logs if reruns or debug settings are unavailable.

## Objectives

Use narrowly scoped diagnostics to identify and fix a path/configuration or missing-output failure without exposing sensitive or untrusted data.

## Tasks

1. Inspect `examples/workflows/07-debug.yml` and the instructor's prepared failure. Activate only this example after preflight. Identify the first meaningful failure, expected path/output, and job/step timeout. Differentiate a hard timeout, cancellation and an ordinary failed test.
2. Predict which small allowlist of tool versions, selected paths or bounded tree output would resolve the uncertainty. Add only those diagnostics in the disposable checkpoint, with log groups or annotations as useful. Never dump all environment variables, secrets, or `toJSON(github)`; masking is not a guarantee. Never interpolate untrusted issue/PR fields into shell.
3. Use a debug-enabled rerun if permitted, choosing step or runner diagnostics as appropriate. Record the evidence and fix the root cause in the prepared course branch. Verify the corrected run. [Debug logging](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands)
4. Observe the instructor's optional `github/local-action` and `act` demo using fake-only inputs. Explain what local success does **not** establish about token permissions, OIDC, rulesets, queue behavior, hosted environment or new server syntax. [Local action](https://github.com/github/local-action), [act limitations](https://nektosact.com/not_supported.html)

<details>
<summary>Hint</summary>

Compare the configured working directory to the path the failing command expects. Capture evidence before the timeout, as hard cancellation cannot guarantee an upload.
</details>

<details>
<summary>Solution</summary>

Use the [debug checkpoint](../examples/workflows/07-debug.yml) and the instructor's corresponding failure fixture. The exact fix depends on that fixture; explain it with one specific path/output and a successful rerun, not a general “enable debug” answer. Step debug and runner debug serve different layers; neither justifies logging secrets or entire contexts.
</details>

## Success and cleanup

You can cite the failure, targeted observation and fix. Cancel course-only reruns, remove your diagnostic changes if no longer needed, and stop any local demo process or container the instructor started for you. Remove only course-owned fake credential files, never broad local configuration. Next: [Lab 8](08-Dependencies.md).
