# 🔨 Hands-on: End-of-class cleanup

**Objective:** leave no unintended training automation, access or paid capacity running. Coordinate with the instructor before touching shared resources. [Manage workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs) and [manage caches](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manage-caches).

## Tasks and verification

**Before cleanup, check back on Lab 3.** If the seeded image is Ready and time permits, finish the consumer comparison and record the actual job image version. If it is still generating or unavailable, use the recorded comparison and mark your live result pending. Do not let that wait delay cleanup or leave paid resources indefinitely: agree with the owner whether to clean them up now or retain them for an explicitly approved follow-up, with a named cleanup owner and deadline.

1. In each disposable course repository, inspect **Actions** for queued/in-progress runs. Cancel those no longer needed. Disable or remove only course-owned workflow files and verify they no longer respond to events. Check for schedules and automations; remove any created for training. Do not disable shared production workflows.
2. Close your course issues and PRs and delete only your temporary branches after coordinating queue state. Retain agreed evidence; remove only identifiable course-owned caches, artifacts, packages, releases and images. Confirm remaining entries belong to shared or intentionally retained work. Cache keys and retention are instructor-coordinated.
3. Stop only local processes/containers you started, and remove only course-owned fake credential files and modified artifact copies. Do not run broad deletion commands or remove shared configuration.
4. **PAID RUNNER / ADMIN REQUIRED:** ask the owner to deprovision dedicated paid runners, scale sets, custom-image generation resources, private networks/VNet integrations, and disposable deployment targets. Stopping compute alone can leave image, disk, registry and network charges. Verify capacity and retained storage separately; never remove a shared runner group or network.
5. **GHEC REQUIRED / EMU SETUP / GHE.COM SETUP:** find your Lab 5 and Lab 6 course-only repository and organization rulesets by their recorded IDs and names. Confirm their exact scope, restore only your temporary changes, and disable/delete only course-created rules when no longer needed. Remove required-check/workflow requirements before disabling the corresponding workflow. Remove only course-owned `lab-staging` and `lab-release` environments after checking deployment state. Restore any explicitly owner-approved temporary Actions sharing change; do not broaden access as part of cleanup. Coordinate shared queue settings, other environment protection and temporary access with their owner, on the correct host. Do not remove shared policy. Verify any course-only tokens, credentials or grants are revoked.

<details>
<summary>Instructor verification checklist</summary>

- [ ] No course runs remain queued/running and no course schedules or event automations remain enabled.
- [ ] Course-only issue/PR/branch and cache/artifact retention agreed and verified.
- [ ] Dedicated compute, image generation, network, image/storage and mock targets accounted for, including ongoing costs.
- [ ] Only temporary grants and course-owned policy removed; shared resources left intact.
- [ ] Local demos stopped and fake inputs removed.
</details>

## Success

You can name what was removed, what was intentionally retained, and who owns any outstanding cleanup. Return to the [course outline](../CLASS-OUTLINE.md).
