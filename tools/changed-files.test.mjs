import { test } from 'node:test';
import assert from 'node:assert/strict';
import { needsChecks } from './changed-files.mjs';

test('docs alone can skip application checks', () => {
  assert.equal(needsChecks(['README.md', 'docs/overview.md']), false);
});
test('code, shared inputs, and workflow changes require validation', () => {
  for (const path of ['app/src/server.js', 'app/package-lock.json', '.github/workflows/check.yml',
    '.github/policy.md', 'tools/changed-files.mjs', 'app/test/removed.test.js']) {
    assert.equal(needsChecks([path]), true, path);
  }
});
