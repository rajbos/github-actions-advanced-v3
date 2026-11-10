# Publication validation status

**Status: blocked; do not publish runnable course material yet.** Checked 2026-11-10. This records current evidence and limitations; it is not a claim of tenant rehearsal or complete security validation.

## Inventory and permissions

- Runnable examples: 16 workflow files in `examples/workflows/`.
- Local action: `actions/hello/action.yml`; its JavaScript implementation, the `tools/` scripts, and application JavaScript are included in the CodeQL coverage below.
- No reusable workflow files or separate runnable solution workflow variants were found. Hidden solutions in the labs are references to the example workflows, not additional workflow files.
- All 16 workflow files now use file-level `permissions: {}`. Jobs that check out the repository request `contents: read` at job scope; jobs without that need retain no token permissions.

## zizmor

- Version: `1.32.0`.
- Command: `zizmor --strict-collection --format json` with every file under `examples/workflows/*.yml` and `actions/hello/action.yml` passed as an explicit input.
- Current result after upgrading all example action references to the latest full release tags: **31 `unpinned-uses` findings**, exit code 14, retained in `.validation/zizmor-latest-releases.json`. The earlier empty result applied to SHA-pinned examples, not current files. No suppressions were added. A generated/reviewed action lock remains a publication requirement; confirm scanner support for that lockfile before claiming these findings resolved.
- Limitation: zizmor emitted a warning that its support for native parallel steps in `04-parallel.yml` is experimental. It was not suppressed. Verify that syntax against the target GitHub host/runner and retain runtime evidence.

## CodeQL

- **Freshness warning:** subsequent trigger edits and version-tag changes across the example workflows are not covered by the historical scan described below. A later source snapshot does not cover edits made after it was created. Revalidate the final workflow contents before publication.
- CodeQL is available through the installed `gh codeql` extension: CLI `2.27.1`. No scanner installation or update was needed.
- Both security-extended analyses completed successfully with **zero findings** and no warning/error-level SARIF execution notifications. No suppressions were added.
- Actions query pack: `codeql/actions-queries@0.6.39`, 24 queries. Extraction confirms all 16 current workflows plus `actions/hello/action.yml`: 17 Actions files / 581 lines.
- JavaScript query pack: `codeql/javascript-queries@2.5.0`, 105 queries. Extraction confirms all 8 authored JavaScript files / 114 lines: both `actions/hello/src/` files, all three `tools/*.mjs` files, and the application's source, build script, and test.
- Source snapshot: `.validation/gh-codeql-20261110/source`. All workflow examples were materialized under `.github/workflows` so the Actions extractor would discover them. The local action, helpers, application source/tests/build script and package manifests were copied without generated output or `node_modules`. All 29 snapshot files were verified byte-for-byte against the current originals after scanning.
- Evidence retained under `.validation/gh-codeql-20261110/`: `actions.sarif`, `javascript.sarif`, and `databases/` containing extractor logs, query results and `baseline-info.json` coverage inventories. This ignored evidence is local; preserve it with the release evidence before publishing.
- The previous CodeQL `2.27.4` Actions-only snapshot is superseded by this current, broader scan; it is not the evidence for these results.

Commands run from the course root after materializing the snapshot:

```powershell
gh codeql database create .validation\gh-codeql-20261110\databases --db-cluster --language=actions,javascript --source-root=.validation\gh-codeql-20261110\source --build-mode=none --threads=2
gh codeql database analyze .validation\gh-codeql-20261110\databases\actions codeql/actions-queries@0.6.39:codeql-suites/actions-security-extended.qls --format=sarifv2.1.0 --output=.validation\gh-codeql-20261110\actions.sarif --threads=2 --sarif-category=course-actions
gh codeql database analyze .validation\gh-codeql-20261110\databases\javascript codeql/javascript-queries@2.5.0:codeql-suites/javascript-security-extended.qls --format=sarifv2.1.0 --output=.validation\gh-codeql-20261110\javascript.sarif --threads=2 --sarif-category=course-javascript
```

Static results do not establish target-tenant runtime behavior or complete manual trust-boundary review. Those separate release gates remain outstanding.

## Action versions and lockfile

The live-refreshed [action version lookup](ACTION-VERSIONS.md) includes all eight used entry points from seven repositories, release publication times and resolved release-tag commits. Queried 2026-11-10 at 17:55 UTC. All workflow and slide action references have been upgraded to these full release tags.

Latest release pages were checked on 2026-11-10:

| Action | Latest stable release checked | Example's current version tag |
|---|---|---|
| `actions/checkout` | `v7.0.1` | `v7.0.1` |
| `actions/setup-node` | `v7.1.0` | `v7.1.0` |
| `actions/cache` | `v6.1.0` | `v6.1.0` |
| `actions/attest` | `v4.2.2` | `v4.2.2` |
| `actions/upload-artifact` | `v7.0.2` | `v7.0.2` |
| `actions/download-artifact` | `v8.0.2` | `v8.0.2` |
| `jessehouwing/actions-dependency-submission` | `v2.0.2` | `v2.0.2` |

Sources: [checkout](https://github.com/actions/checkout/releases/latest), [setup-node](https://github.com/actions/setup-node/releases/latest), [cache](https://github.com/actions/cache/releases/latest), [attest](https://github.com/actions/attest/releases/latest), [upload-artifact](https://github.com/actions/upload-artifact/releases/latest), [download-artifact](https://github.com/actions/download-artifact/releases/latest).

All external action references now use the full latest release tags recorded above, including the checkout v7 and dependency-submission v2 major upgrades. Reviewed their action metadata and relevant release/README guidance: both use Node 24, checkout's new privileged fork-code safeguard needs no opt-out for these examples, and submission retains explicit input values. The dependency lab and stable research links now reference v2.0.2. Target-runner/tenant execution is still required. Tags are mutable and do not by themselves provide immutable dependencies. **Blocked:** there is no generated `actions.lock`, and the current scanner reports unpinned references. Before publication, verify the newest host-supported action references and generate/review the repository lockfile with `gh actions-lock`; do not hand-edit it. Lockfile support is a preview and must be checked for the target host.

## PowerPoint delivery

- The user supplied `Guidance_PPTX.pptx` as the accessible branding source, replacing the previously inaccessible Downloads template. Inspected its actual 51 guidance/sample slides, one slide master, 58 layouts, widescreen dimensions, theme colors, Arial typography and notes master before generation.
- Generated one deck per module under `slides/powerpoint/`: `01-caching.pptx` (16 slides), `02-execution.pptx` (23), `03-policy.pptx` (17), and `04-debug-trust.pptx` (14). All 70 slides have speaker notes copied from their Markdown source. Sample teaching slides were removed; the original master/layout XML, logo, separators and copyright footer were retained. Content uses the actual `Title Content/White` and `Title Content/Dark` layouts.
- Reproducible generator: `tools/build_slides.py`; authoring/scanner dependencies: root `requirements.txt`, with Python 3.13.14 in `.python-version` and a forwarding compatibility file at `tools/requirements-pptx.txt`. See the [instructor guide](INSTRUCTOR-GUIDE.md#teaching-decks-and-updates) for regeneration. `slides/powerpoint/manifest.json` retains template, source and output SHA-256 hashes, slide/notes counts and layout measurements.
- Supporting material accompanies 37 slides: nine editable flow diagrams, fourteen comparison/decision tables and fourteen YAML/shell/worked-example panels. Actual workflow excerpts are identified and intentionally incomplete where labeled; numerical examples and predicted outcomes are explicitly illustrative, not fabricated runtime evidence. Module 2 now includes checkout lifecycle/scope at minutes 1-8 and two artifact packaging/selection/extraction patterns at 8-12, with event teaching at 12-20. Its nine added slides preserve all labs, the 105-minute module and 420-minute teaching day. Checkout implementation and artifact inputs/examples were inspected against the references recorded in REFERENCES.md. New snippets have preflight prerequisites; they are not installed runnable workflows, measured speedups, or new scanner-run evidence.
- Structural checks reopened every output and confirmed exact title/bullet/notes/example parity with Markdown (display formatting removed and visual line breaks normalized), unchanged masters/layouts/dimensions, inherited title margins and no off-slide shapes. Six focused generator tests cover parsing, code indentation, notes preservation, malformed material rejection, editable flow rendering and oversized-code rejection.
- Reviewed all 70 slides for plain English across titles, teaching points, captions, tables, diagrams and code comments. Replaced unexplained lab shorthand with concrete actions. Added visible first-use explanations for runner, PR, baseline, runner-minutes, cache key/lockfile/hash, exact/partial/miss, prewarming, sparse checkout, submodules/LFS, artifacts, event activities, matrix, stack, merge queue, ruleset, SHA, digest, SBOM, attestation, provenance and promotion. Lab 2 now separates the prepared lockfile change from the cache-version change and explains cold runs. Technical instructor notes and references remain available; the Lab 2 notes were expanded to support the clearer steps. This is an editorial review, not evidence of comprehension testing with learners.
- Native PowerPoint `16.0` opened and rendered all 70 slides at 1600 x 900. `tools/validate_slides.ps1` checks native bounding width/height within a 2-point tolerance, including table cells, and checks example shapes against the footer region and slide bounds. Its report records each deck's SHA-256. Corrected bold-font wrapping, code height and native table expansion before retaining final renders.
- The OS/runtime matrix slide illustrates six compatibility jobs with `max-parallel: 3` and `fail-fast: false`, within the existing minutes 53-60 teaching segment. Runtime versions require preflight; this is not a recorded six-platform run or an installed workflow. The proposed scatter/gather optional lab remains unimplemented.
- Evidence: `.validation/powerpoint-render/native-validation.json`, current module PNG render folders, and exported template guidance slides. Earlier contact sheets predate the latest wording/matrix slide; use the current PNGs and hash-linked report for this revision. This ignored evidence is local; preserve it with release evidence.
- Accessibility essentials checked: semantic title and notes placeholders, title/takeaway/example/module-label reading order, English run language, high-contrast dark/light theme colors, 54-point cover titles, 36-point teaching titles, 22-point takeaways, 18-20-point table/code content and editable diagram text. This is **not** a PowerPoint Accessibility Checker or assistive-technology certification; those checks and actual presentation-room readability remain outstanding.
- Deck generation does not clear the action-lock, target-tenant runtime or full-course rehearsal gates. The added Python deck-generation tool is outside the earlier Actions/JavaScript CodeQL scan scope.

## Other release gates

- Run PowerPoint's Accessibility Checker and confirm assistive-technology and presentation-room usability; deck generation and native rendering are complete, but these checks are not.
- Target-tenant schema/runtime checks and manual event/ref/token/cache/artifact trust-boundary rehearsals remain outstanding. Use prepared evidence only when it is clearly labeled as such.
- `node --test tools/changed-files.test.mjs tools/workflow-triggers.test.mjs`: passed, 7 tests, including exact action-release lookup parity across workflows and teaching examples.
- Python 3.13.14 matches `.python-version`. Both requirements entry points resolve to the installed direct tool versions: python-pptx 1.0.2, Pillow 13.0.0 and zizmor 1.32.0. The earlier Pillow `<13` constraint did not match the installed rendering environment and has been replaced with the verified exact version.
- `.gitignore` covers dependency/build directories, scanner reports/databases, native render output, virtual environments, Python caches, release-lab outputs and local credential/temporary files. The previously staged `.zizmor-initial.json` was removed from the index without deleting its local copy. Course PowerPoint deliverables, manifests and source fixtures remain trackable.
- `npm --prefix app test`: passed, 1 test.
