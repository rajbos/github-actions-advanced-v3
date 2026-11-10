# 🔨 Lab 7: Find the failure without dumping secrets

**Time:** 20 minutes. **Prerequisite:** your participant repository and [setup](00-Setup.md). The path fixture below needs no instructor-prepared branch or run. **DEMO / FALLBACK:** inspect recorded logs if reruns or debug settings are unavailable.

## Objectives

Use narrowly scoped diagnostics to identify and fix a path/configuration or missing-output failure without exposing sensitive or untrusted data.

## Tasks

1. Copy the `examples/workflows/07-debug.yml` starter to `.github/workflows/07-debug.yml` in **your participant repository**. It already contains one deliberately incorrect source check, without the diagnostic listing or corrected path. Do not open the solution yet. Lock, commit/push and dispatch **Lab 07 targeted diagnostics**. Identify the first meaningful failure and distinguish an ordinary nonzero exit from your timeout/cancellation evidence.
2. Predict which small allowlist of tool versions, selected paths or bounded tree output would resolve the uncertainty. Add only those diagnostics in the disposable checkpoint, with log groups or annotations as useful. Never dump all environment variables, secrets, or `toJSON(github)`; masking is not a guarantee. Never interpolate untrusted issue/PR fields into shell.
3. Implement an additional bounded diagnostic gated on `runner.debug`, commit/push and dispatch that still-failing revision. Then use **Re-run jobs → Enable debug logging** on that failed run if permitted (or the linked CLI), observing the additional evidence at the same revision. Debugging does not repair the failure. Use the evidence to fix the path, commit/push and dispatch a **new run on the corrected revision**. Rerunning an old revision retains its old check. Verify the new run succeeds. [Debug logging](https://docs.github.com/en/actions/how-tos/monitor-workflows/enable-debug-logging), [CLI rerun](https://cli.github.com/manual/gh_run_rerun), [workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands)
4. Observe the instructor's optional `github/local-action` and `act` demo using fake-only inputs. Explain what local success does **not** establish about token permissions, OIDC, rulesets, queue behavior, hosted environment or new server syntax. [Local action](https://github.com/github/local-action), [act limitations](https://nektosact.com/not_supported.html)

<details>
<summary>Hint</summary>

Compare the configured working directory to the path the failing command expects. Capture evidence before the timeout, as hard cancellation cannot guarantee an upload.
</details>

<details>
<summary>Solution</summary>

The [completed debug reference](../solutions/workflows/07-debug.yml) contains narrow grouped diagnostics, a debug-gated message and the corrected source check. A listing shows `app/src/server.js`; the starter checks the nonexistent `app/src/serve.js`. Fix the exact path and dispatch the corrected revision. Explain the fix using observed evidence, not a general “enable debug” answer. Neither debug layer justifies logging secrets or entire contexts.
</details>

## Success and cleanup

You can cite the failure, targeted observation, corrected revision and successful run. Cancel course-only reruns and disable **Lab 07 targeted diagnostics**; it is not used in Lab 8. Remove your diagnostic changes if no longer needed, and stop any local demo process or container the instructor started for you. Remove only course-owned fake credential files, never broad local configuration. Next: [Lab 8](08-Dependencies.md).
