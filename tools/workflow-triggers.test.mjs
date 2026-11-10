import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';

const directory = new URL('../examples/workflows/', import.meta.url);
const workflow = name => readFileSync(new URL(name, directory), 'utf8');

test('workflows and teaching examples match the dated latest-release lookup', () => {
  const lookup = readFileSync(new URL('../ACTION-VERSIONS.md', import.meta.url), 'utf8');
  const versions = new Map(
    [...lookup.matchAll(/^\| `([^`]+)` \| `(v[^`]+)` \| \[(v[^\]]+)\]/gm)]
      .map(([, action, used, latest]) => {
        assert.equal(used, latest, action);
        return [action, latest];
      }),
  );
  assert.equal(versions.size, 8);
  const seen = new Set();
  for (const folder of ['examples/workflows/', 'slides/', 'hol/']) {
    const url = new URL(`../${folder}`, import.meta.url);
    for (const name of readdirSync(url).filter(name => /\.(?:yml|yaml|md)$/.test(name))) {
      const text = readFileSync(new URL(name, url), 'utf8');
      for (const [, action, version] of text.matchAll(/uses:\s+([\w.-]+\/[\w./-]+)@([^\s#]+)/g)) {
        assert.equal(version, versions.get(action), `${folder}${name}: ${action}`);
        seen.add(action);
      }
    }
  }
  assert.deepEqual([...seen].sort(), [...versions.keys()].sort());
});

test('example action references use readable version tags', () => {
  for (const name of readdirSync(directory).filter(name => name.endsWith('.yml'))) {
    const text = workflow(name);
    assert.doesNotMatch(text, /uses:\s+\S+@[0-9a-f]{40}\b/, name);
    for (const match of text.matchAll(/uses:\s+([^\s#]+)/g)) {
      if (match[1].startsWith('./')) continue;
      assert.match(match[1], /^[\w.-]+\/[\w./-]+@v\d+(?:\.\d+){0,2}$/, name);
    }
  }
});

const triggers = name => {
  const match = workflow(name).match(/^on:\r?\n([\s\S]*?)(?=^\S)/m);
  assert.ok(match, `${name}: missing event block`);
  return match[1];
};

test('optional cache workflows filter application, self, and lockfile inputs', () => {
  for (const [name, event] of [
    ['02-cache-main.yml', 'push'],
    ['02-cache-pr.yml', 'pull_request'],
  ]) {
    const block = triggers(name);
    assert.match(block, new RegExp(`^  ${event}:`, 'm'));
    const paths = [...block.matchAll(/^      - '([^']+)'$/gm)].map(match => match[1]);
    assert.deepEqual(paths, [
      'app/**',
      `.github/workflows/${name}`,
      `examples/workflows/${name}`,
      'actions.lock',
    ]);
  }
  assert.match(triggers('02-cache-main.yml'), /^    branches: \[main\]$/m);
});

test('required evidence is not removed by trigger path filters', () => {
  for (const name of [
    '05-stack-queue.yml', '06-gates.yml', '06-staging.yml', '06-central-required.yml',
  ]) {
    const block = triggers(name);
    assert.match(block, /^  pull_request:/m);
    assert.match(block, /^  merge_group:/m);
    assert.doesNotMatch(block, /\bpaths(?:-ignore)?:/);
  }
});

test('all other exercises are dispatch-only or issue-activity examples', () => {
  const scoped = new Set([
    '02-cache-main.yml', '02-cache-pr.yml', '05-stack-queue.yml',
    '06-gates.yml', '06-staging.yml', '06-central-required.yml',
  ]);
  const names = readdirSync(directory).filter(name => name.endsWith('.yml'));
  assert.equal(names.length, 16);
  for (const name of names.filter(name => !scoped.has(name))) {
    const block = triggers(name);
    assert.match(block, /^  (?:workflow_dispatch|issues):/m, name);
    assert.doesNotMatch(block, /^  (?:push|pull_request|merge_group):/m, name);
    assert.doesNotMatch(block, /\bpaths(?:-ignore)?:/, name);
  }
});
