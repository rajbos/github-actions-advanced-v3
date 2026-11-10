import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';

const workflows = ['examples', 'solutions'].map(folder =>
  readFileSync(new URL(`../${folder}/workflows/06-gates.yml`, import.meta.url), 'utf8'));

test('gate variants reuse the reviewed changed-files action instead of a custom detector', () => {
  for (const text of workflows) {
    const impact = text.split('  impact:')[1].split('  application:')[0];
    assert.match(impact, /uses: tj-actions\/changed-files@v47\.0\.6/);
    assert.doesNotMatch(impact, /uses: actions\/setup-node@|run: node/);
    assert.match(impact, /fetch-depth: 0/);
    assert.match(impact, /persist-credentials: false/);
    assert.match(impact, /skip_initial_fetch: 'true'/);
    assert.match(impact, /fail_on_initial_diff_error: 'true'/);
    assert.doesNotMatch(impact, /continue-on-error|use_rest_api: 'true'|pull-requests: write/);
  }
  assert.equal(existsSync(new URL('./changed-files.mjs', import.meta.url)), false);
});

test('change detection compares the explicit event base with the tested combined revision', () => {
  for (const text of workflows) {
    assert.ok(text.includes('base_sha: ${{ github.event.merge_group.base_sha || github.event.pull_request.base.sha }}'));
    assert.ok(text.includes('sha: ${{ github.sha }}'));
    assert.doesNotMatch(text, /pull_request\.head\.sha|since_last_remote_commit/);
  }
});

test('selection includes deletions, type changes, both rename paths and all GitHub policy files', () => {
  for (const text of workflows) {
    assert.match(text, /output_renamed_files_as_deleted_and_added: 'true'/);
    assert.match(text, /files: \|\r?\n            \*\*\r?\n            !\*\*\/\*\.md\r?\n            \.github\/\*\*/);
    assert.ok(text.includes("checks: ${{ steps.impact.outputs.all_changed_and_modified_files_count != '0' }}"));
    assert.ok(text.includes("if: needs.impact.outputs.checks == 'true'"));
    assert.match(text, /DETECTION: \$\{\{ needs\.impact\.result \}\}/);
  }
});
