# Class delivery requirements

These are acceptance criteria for implementing the proposed class, not claims that slides, PowerPoint decks, runnable labs, or security checks already exist.

## Deliverables

- Guided Markdown labs following the fundamentals class's approach: objectives, prerequisites, tasks, documentation links, hints, observable success criteria, and cleanup.
- Describe what learners must accomplish without immediately supplying complete commands or YAML. Put progressively stronger hints and full solutions in collapsed `<details>` sections or clearly linked solution files. Collapsed content is a teaching convenience, not access control.
- `examples/workflows` contains learner starting points, not completed implementations of the target skill. Keep solved references in `solutions/workflows` and link them from collapsed lab solutions. Preserve safe scaffolding; explicitly fail unfinished evidence-producing steps. Runnable baselines/observers/minimal demos are allowed when measurement or observation is the task. Validate both starter and solved variants.
- Write starter TODO comments in plain English for participants with average technical skills who may not be native English speakers. Explain what to add or replace, where it belongs, what existing behavior to keep and what result to expect. Define unfamiliar terms instead of relying on shorthand such as "bounded stall" or "propagate failure". Leave implementation work for the learner. Explain that error-returning placeholders must be replaced with real checks, not merely deleted; distinguish placeholder errors from deliberate failure/timeout experiments.
- Write every part of a lab, including hints, solutions and cleanup, as guidance for people, not instructions to an agent or a delivery audit. Separate timing, prerequisites, access requirements and alternatives into short paragraphs. Use concrete actions and questions, explain unfamiliar terms and add paragraph breaks within long steps. Solutions should explain what the workflow does and why, with concrete examples rather than compressed lists of claims. Keep trainer-only directions in the instructor guide rather than asking participants to deliver a demonstration or report compliance.
- When participants cannot complete a step, ask the trainer to demonstrate it; do not claim recordings are available. If a trainer demonstration is also unavailable, explain the expected behavior and clearly state that it was not demonstrated.
- Use visible UI names and navigation for participant setup and cleanup, not numeric resource IDs. Introduce prerequisites before they are needed: run a new check before asking learners to select it in a ruleset, and explicitly explain how to trigger that first run.
- Link relevant documentation at the task that needs it, not just in a course-wide bibliography.
- Prefer reviewed reusable actions over custom scripts when an action already provides the required behavior. Lab 6 reuses the Lab 3 changed-files action; learner work remains the gate policy, not implementing Git-diff plumbing.
- Markdown slides per module with instructor notes, demonstration checkpoints, expected observations, failure cases, timing, recovery guidance, and source references.
- One PowerPoint per module, derived from the same teaching content and including speaker notes. Use the user-provided Xebia template at `C:\Users\JesseHouwing\Downloads\Template_PPTX.pptx`; inspect its actual masters/layouts before generating decks. Template accessibility and branding fidelity must be confirmed, not assumed.
- Keep Markdown, PowerPoint content, notes, labs, solutions, and source references consistent when updating a module.

## Platform and account markers

At course setup and in each affected lab, explain required access and what to do if it is unavailable. Use readable labels such as **Before you start**, **Paid resources** and **If you cannot run this part**, with separate paragraphs rather than a chain of uppercase markers.

The following categories are planning shorthand for the course author, not required wording in participant instructions:

| Marker | Meaning |
| --- | --- |
| `GHEC REQUIRED` | Requires an Enterprise Cloud capability; state the specific feature/plan and organization ownership requirements. |
| `EMU SETUP` | Requires a managed identity and an organization-owned lab repository. Personal repositories and user-owned forks cannot use the GitHub-hosted runners required by these labs. Not interchangeable with all GHEC accounts. |
| `GHE.COM SETUP` | Requires an organization-owned lab repository on the enterprise's actual `ghe.com` host, with its authentication, API endpoints and supported features. Personal repositories cannot be used for these hosted-runner labs. |
| `PAID RUNNER / ADMIN REQUIRED` | Needs a provisioned runner/image/network resource, billing authorization, or organization administrator action. |
| `DEMO / FALLBACK` | Prepared instructor run or evidence when the learner account cannot perform the task. |

Verify eligibility separately for required workflows/rulesets, custom hosted images, and Azure private networking/VNet integration. Do not blanket-label every rule or runner feature Enterprise-only. Record preview status, tenant/region/runner restrictions, and date checked. Never require learners to purchase a plan or change enterprise policy during the lab.

## Security requirements

- PR dependency caches: only `actions/cache/restore` and explicit `cache-mode: read`; deployments use `cache-mode: none`.
- Explain default/base-branch execution context, cache read/write scope, low-trust default restrictions, and explicit write-mode overrides. A default-branch workflow file does not make its input trusted.
- Cache writers consume only reviewed trusted revisions/dependencies. Do not execute PR code, untrusted lifecycle scripts, or downloaded PR artifacts in privileged follow-up workflows.
- No live cache-poisoning exploit, malicious action execution, or intentionally vulnerable workflow enabled in a learner repository. Teach unsafe examples as inert text/diagrams.
- Metadata-only issue exercises use no checkout, no API writes, `permissions: {}`, and `cache-mode: none`.
- Never interpolate attacker-controlled issue/PR fields or filenames into shell scripts. Prefer allowlisted event metadata; handle necessary external data through structured inputs/environment variables with correct quoting and validation.
- Use fundamentals' immutable action dependencies/lockfile policy; disable implicit setup-action cache writers where explicit restore-only behavior is required.
- No real secrets in fixtures, screenshots, logs, caches, prewarmed images, or local emulator inputs. No broad PAT workaround for fork permissions.
- Restrict privileged environments, image builders, runner groups, network access, and reusable workflow callers. Treat artifacts and image/package seeds as trust boundaries.
- Failure, cancellation, missing evidence, detection errors, and timeouts must not produce a success-shaped required gate.

## Validation gate

Run **both CodeQL and zizmor** before publishing runnable course material:

1. Inventory workflow files, local actions, reusable workflows, starter/solution variants, and embedded examples. Materialized examples intended to run must be included in the validation scope.
2. Run zizmor against all runnable workflow/action variants, including hidden solutions, with no unexplained or blanket suppressions.
3. Configure and run CodeQL's GitHub Actions analysis where supported, plus applicable supported languages for scripts/custom actions. Confirm actual coverage rather than counting a passing scan of unrelated application code.
4. If the selected host/tool versions cannot analyze a required surface, mark validation blocked or document the precise limitation; do not claim that surface is validated.
5. Address findings with minimal changes and keep narrow, justified suppressions reviewable. Do not hide unsafe patterns merely to make a scanner pass.
6. Also verify schema/runtime behavior on the target GitHub tenant and manually review event/ref/token/cache/artifact trust boundaries. Static scanning alone is not proof of safety.
7. Retain tool versions, commands/configuration, scope, findings/disposition, and successful results as release evidence.

Do not install scanners or create recurring scan workflows until implementation requires them. No executable course workflows currently exist to validate.

## Cleanup and cost control

- Every lab ends with cleanup instructions and verification of what remains.
- Prefer bounded manual/event triggers and explicit job/step timeouts. Avoid recurring schedules, issue-comment loops, self-triggering automation, and auto-updating dependencies left enabled after training.
- Explain how to cancel active runs, disable training workflows, and remove schedules/automations created for the exercise.
- Remove only course-owned caches, artifacts, packages, images, temporary branches/environments, and credentials as appropriate; clearly identify what is shared and must not be deleted.
- Deprovision dedicated paid runners, scale sets, custom-image generation resources, private networking/VNet resources, and disposable deployment targets. Distinguish stopping compute from removing ongoing storage/network charges.
- Coordinate cleanup of organization rulesets, queue settings, and runner groups with the administrator; never remove shared policy.
- Local demos stop servers/containers and remove fake credential files without broad destructive cleanup commands.
- Provide an instructor end-of-day checklist that checks active runs, scheduled workflows, paid capacity, image/storage retention, and revocation of any temporary access.
- Add to the delivery guidelines: do not pin actions to their sha in every workflow file, but use `gh actions-lock` instead. Do check that you're using the latest versions.
- Add to the delivery guidelines: always request `permissions: {}` at the file level and only request explicit permissions at the job level

## Source maintenance

Use [REFERENCES.md](REFERENCES.md) for source locators, revisions, availability checks, and update watchpoints. Use [CLASS-OUTLINE.md](CLASS-OUTLINE.md) for the agreed teaching structure.
