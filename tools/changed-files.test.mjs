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
    assert.ok(text.includes("if: needs.impact.result != 'success'"));
  }
});

test('completed required gate fails closed for missing or unsuccessful evidence', () => {
  const gate = workflows[1].split('  required:')[1];
  assert.match(gate, /^\s+if: always\(\)/);
  assert.match(gate, /needs: \[impact, application\]/);
  assert.doesNotMatch(gate, /continue-on-error/);

  const steps = gate.split(/^      - name: /m).slice(1);
  const conditions = steps
    .map(step => ({ condition: step.match(/^        if: (.+)$/m)?.[1], text: step }))
    .filter(step => step.condition);
  assert.equal(conditions.length, 4);
  for (const step of conditions) assert.match(step.text, /^          exit 1$/m);
  assert.match(steps.at(-1), /^All gate conditions are satisfied/m);

  const evaluate = (expression, values) => expression.split(/\s+\|\|\s+/).some(alternative =>
    alternative.split(/\s+&&\s+/).every(term => {
      const match = /^needs\.(impact\.result|impact\.outputs\.checks|application\.result)\s*(==|!=)\s*'([^']*)'$/.exec(term);
      assert.ok(match, `Unsupported gate condition: ${term}`);
      const equal = values[match[1]].toLowerCase() === match[3].toLowerCase();
      return match[2] === '==' ? equal : !equal;
    }));

  const cases = [
    ['success', 'false', 'skipped', true],
    ['success', 'true', 'success', true],
    ['success', '', 'skipped', false],
    ['success', 'unexpected', 'skipped', false],
    ...['failure', 'cancelled', 'skipped'].map(result => [result, 'false', 'skipped', false]),
    ...['failure', 'cancelled', 'skipped'].map(result => ['success', 'true', result, false]),
    ...['success', 'failure', 'cancelled'].map(result => ['success', 'false', result, false]),
  ];
  for (const [impact, checks, application, shouldPass] of cases) {
    const values = {
      'impact.result': impact,
      'impact.outputs.checks': checks,
      'application.result': application,
    };
    const passes = !conditions.some(step => evaluate(step.condition, values));
    assert.equal(passes, shouldPass, JSON.stringify(values));
  }
});
