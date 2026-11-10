# 🔨 Hands-on: Set up your lab repository

You will use one disposable repository and the same small Node application throughout this instructor-led course. The four sections are 105 minutes each; use prepared evidence when a queue, permission, or service delay would consume the lab.

## Objectives and prerequisites

- Identify your host, repository, default branch, and training resources.
- Confirm that Actions, issues, and the sample application are available without enabling every workflow.
- Bring fundamentals knowledge: workflows, environments, reusable workflows, immutable action dependencies and least privilege.

You need a browser, a GitHub account, and a course repository supplied by the instructor. A local Git client and Node.js are useful but optional. **Do not install tools or change enterprise settings as a prerequisite.** Work only with fictitious data; never enter real secrets into logs, images, caches, artifacts, or local emulator inputs.

## Choose your setup

1. **GitHub.com:** Create or receive a disposable repository using the course materials as instructed. Record the owner, repository and default branch; these labs use `main` as shorthand, so substitute your actual default branch.
2. **EMU SETUP:** An Enterprise Managed User uses the managed identity and an administrator-approved organization/repository. A personal repository or fork may not be available. Ask the instructor for the prepared organization repository and use the fallback if creation, issues or PRs are restricted.
3. **GHE.COM SETUP:** Use your enterprise's actual `https://SUBDOMAIN.ghe.com` host, its authentication, and its own API/CLI host configuration. Do not substitute `github.com` URLs in commands. Availability and action sources can differ; use prepared evidence when an example is unavailable. EMU and data-residency hosts are separate choices.
4. **GHEC REQUIRED:** Central required workflows need an eligible Enterprise Cloud organization/enterprise ruleset and admin preparation. Private/internal attestation availability also depends on the plan. Merge queue, ordinary rules, images and networking have their own eligibility; do not assume one license covers all. See [availability](../REFERENCES.md#product-and-version-gates-from-githubdocs).
5. **PAID RUNNER / ADMIN REQUIRED:** Custom images, larger runners, networking, organization rulesets, queue and staging resources are instructor-provisioned and cost-controlled. Learners do not provision or purchase them. **DEMO / FALLBACK:** use instructor-run evidence if unavailable.

## Prepare the workspace

The workflows and slide examples use the full release tags recorded in [the action version lookup](../ACTION-VERSIONS.md), including checkout `v7.0.1` and dependency submission `v2.0.2`. The instructor must verify Node 24 action-runtime support and host feature availability before activation. A tag is readable but mutable; the reviewed execution lockfile is still required.

1. Locate `app/package.json`, `app/package-lock.json`, `app/src/server.js`, and `app/test/server.test.js`. The application supports `npm ci`, `npm test`, `npm run lint`, and `npm run build` from `app`. Review the scripts before running them. [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/)
2. Locate `examples/workflows`. These files are **inert examples** until copied individually to `.github/workflows`. Copy only the specific example selected by a lab after instructor preflight. Preserve its filename unless the instructor explains why a change is safe; the release example's signer verification binds its exact workflow path. Several examples explicitly guard `main`; if your default branch differs, have the instructor review all relevant triggers, conditions and signer constraints before activation. Never bulk-copy the directory, and never enable an unsafe demonstration.
3. Identify how to open Actions runs, inspect job logs, cancel a run, and disable a workflow. Check that the instructor has prepared baseline and failure evidence. Confirm each runnable workflow has file-level `permissions: {}` and only least-privilege job permissions. Check current supported action versions and the repository's `actions.lock`, generated/reviewed with `gh actions-lock`; do not repeat SHA pins in every workflow or hand-edit the lockfile. Confirm the target host supports the lockfile feature rather than weakening organization policy. [Secure use](https://docs.github.com/en/actions/reference/security/secure-use), [lock workflow dependencies](https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies)
4. Record the default branch and access to issues, PRs and Actions. If you cannot create or edit the disposable training issue, follow the instructor's recorded observations.

<details>
<summary>Hint: how does a workflow become active?</summary>

GitHub recognizes workflow YAML in `.github/workflows` on the relevant branch. Event-specific requirements differ: the issue examples must exist on the default branch; manual dispatch also requires the workflow on the default branch.
</details>

## Success and cleanup

You can identify your host, repository, default branch and chosen fallback. No example was enabled merely by locating it. Leave the repository in place for later labs; remove nothing shared. Continue with [Lab 1](01-Measure.md). At the end of class use [Cleanup](10-Cleanup.md).
