# Action version lookup

**Queried live on 2026-11-10, 17:55 UTC**, using the GitHub REST API through `gh`.

Scope: every external `uses:` reference in `examples/workflows`, `solutions/workflows`, `actions`, `slides` and `hol`. Nine action entry points come from eight repositories; cache restore/save share a release. Starters intentionally omit actions learners must add; the completed references retain the full inventory. Local actions have no upstream release. Instructor tools such as `act` are not workflow action dependencies. The added Lab 3 `tj-actions/changed-files` entry was queried separately on 2026-11-10 during the walkthrough; its latest release and exact commit matched the reviewed archive seed.

The latest version below is GitHub's designated latest non-draft, non-prerelease release from `GET /repos/{owner}/{repo}/releases/latest`, not a guessed major tag or a recommendation to upgrade without review. Commit SHAs were resolved from the full release tag using `GET /repos/{owner}/{repo}/commits/{tag}`.

| Action entry point | Currently used tags | Latest stable release | Published (UTC) |
| --- | --- | --- | --- |
| `actions/checkout` | `v7.0.1` | [v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) | 2026-07-20 15:10:05 |
| `actions/setup-node` | `v7.1.0` | [v7.1.0](https://github.com/actions/setup-node/releases/tag/v7.1.0) | 2026-10-08 02:52:34 |
| `actions/cache/restore` | `v6.1.0` | [v6.1.0](https://github.com/actions/cache/releases/tag/v6.1.0) | 2026-06-26 19:17:06 |
| `actions/cache/save` | `v6.1.0` | [v6.1.0](https://github.com/actions/cache/releases/tag/v6.1.0) | 2026-06-26 19:17:06 |
| `tj-actions/changed-files` | `v47.0.6` | [v47.0.6](https://github.com/tj-actions/changed-files/releases/tag/v47.0.6) | 2026-04-18 11:20:20 |
| `actions/attest` | `v4.2.2` | [v4.2.2](https://github.com/actions/attest/releases/tag/v4.2.2) | 2026-08-04 20:36:29 |
| `actions/upload-artifact` | `v7.0.2` | [v7.0.2](https://github.com/actions/upload-artifact/releases/tag/v7.0.2) | 2026-10-07 10:08:14 |
| `actions/download-artifact` | `v8.0.2` | [v8.0.2](https://github.com/actions/download-artifact/releases/tag/v8.0.2) | 2026-10-07 10:09:51 |
| `jessehouwing/actions-dependency-submission` | `v2.0.2` | [v2.0.2](https://github.com/jessehouwing/actions-dependency-submission/releases/tag/v2.0.2) | 2026-10-16 13:07:14 |

## Release tag commits

Lab 3 build tooling (not an external `uses:` entry): `jessehouwing/gh-actions-archive-cache` is pinned to [v0.0.2](https://github.com/jessehouwing/gh-actions-archive-cache/releases/tag/v0.0.2), queried 2026-11-10. Precompiled Windows/Linux/macOS amd64/arm64 assets are available. Install with `gh extension install jessehouwing/gh-actions-archive-cache --pin v0.0.2`, seed the reviewed commit, then uninstall before snapshotting. This extension release is separate from the action commits in `actions.lock`.

These are lookup evidence from the query time, not an `actions.lock` or proof that a moving major tag resolves to the same commit.

| Repository | Release tag | Resolved commit SHA |
| --- | --- | --- |
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/setup-node` | `v7.1.0` | `949feb2413d6458794dcd2491c4babbbce0c15c1` |
| `actions/cache` | `v6.1.0` | `55cc8345863c7cc4c66a329aec7e433d2d1c52a9` |
| `tj-actions/changed-files` | `v47.0.6` | `9426d40962ed5378910ee2e21d5f8c6fcbf2dd96` |
| `actions/attest` | `v4.2.2` | `1e69f48acb82d1966a394da916b4c1698aa569d6` |
| `actions/upload-artifact` | `v7.0.2` | `cf430e030ddbb5b0abf93d22962f4752f3646cd9` |
| `actions/download-artifact` | `v8.0.2` | `9000827ccba6bdab643e8b6fd33ac0654aef8333` |
| `jessehouwing/actions-dependency-submission` | `v2.0.2` | `811981eec3c108f41783f194522fde91a34301a4` |

## Refresh the lookup

Reinventory action references when examples change. For each distinct repository, run the following PowerShell commands, replacing the example repository name:

```powershell
$repo = 'actions/checkout'
$release = gh api "repos/$repo/releases/latest" | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw "Release lookup failed: $repo" }
$commit = gh api "repos/$repo/commits/$($release.tag_name)" --jq .sha
if ($LASTEXITCODE -ne 0) { throw "Release commit lookup failed: $repo" }
$release | Select-Object tag_name, published_at, html_url
$commit
```

Update the query date, release details, resolved commits and used tags together. If the API returns no latest release, record that limitation rather than treating an arbitrary tag as a stable release.

**Applied to course samples:** workflows and teaching excerpts now use the full release tags above, including the checkout v6-to-v7 and dependency-submission v1-to-v2 upgrades. Both actions use the Node 24 action runtime; verify target runner support before class. Checkout v7's guard for privileged fork-code checkouts does not require an opt-out in these `pull_request`, `merge_group` and reviewed-main examples. Keep `persist-credentials: false`. Submission v2 retains the explicit `report-transitive-as-direct: 'false'` input; its README/input-default discrepancy still requires an explicit value. With an `actions.lock`, v2 also verifies and reads the lock; preflight `gh` and the lock extension and do not accept warning-only unverified lock usage as release evidence.

Release tags remain mutable. Generate/review `actions.lock` with `gh actions-lock` and validate host/runtime support. Updating references does not clear the course's publication blockers.

Lab 6 also reuses `tj-actions/changed-files@v47.0.6` for the supplied impact detector. Its explicit base/tested SHAs, local-history comparison, fail-on-diff-error setting and deletion/rename-inclusive count replace the custom Node detector. Include this reference in the installed execution lock; the starter still leaves final-gate implementation to the learner.
