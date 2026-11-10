import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { prepareArchive, validateManifest } from './prepare-codeql.mjs';

const bytes = Buffer.from('small CodeQL archive fixture');
const manifest = {
  version: '2.27.4',
  asset: 'codeql-bundle-linux64.tar.zst',
  sha256: createHash('sha256').update(bytes).digest('hex'),
  size: bytes.length,
  note: 'test',
};

async function withCache(run) {
  const cache = await mkdtemp(join(tmpdir(), 'lab-codeql-'));
  try {
    await run(cache);
  } finally {
    await rm(cache, { recursive: true, force: true });
  }
}

test('download verifies bytes; exact and note-only partial reuse avoid network', async () => {
  await withCache(async cache => {
    let calls = 0;
    const download = async url => {
      calls++;
      assert.equal(url, 'https://github.com/github/codeql-action/releases/download/codeql-bundle-v2.27.4/codeql-bundle-linux64.tar.zst');
      return new Response(bytes);
    };
    const first = await prepareArchive(manifest, cache, download);
    assert.equal(first.downloaded, true);
    assert.deepEqual(await readFile(first.archive), bytes);
    assert.equal((await prepareArchive(manifest, cache, download)).downloaded, false);
    assert.equal((await prepareArchive({ ...manifest, note: 'changed key, same bundle' }, cache, download)).downloaded, false);
    assert.equal(calls, 1);
  });
});

test('a different requested version downloads separately instead of using old bytes', async () => {
  await withCache(async cache => {
    const first = await prepareArchive(manifest, cache, async () => new Response(bytes));
    const next = await prepareArchive({ ...manifest, version: '2.27.5' }, cache, async () => new Response(bytes));
    assert.notEqual(first.archive, next.archive);
    assert.equal(next.downloaded, true);
    assert.deepEqual(await readFile(first.archive), bytes);
  });
});

test('fresh baseline directories download again even with an unchanged manifest', async () => {
  let calls = 0;
  const download = async () => {
    calls++;
    return new Response(bytes);
  };
  await withCache(async firstDirectory => {
    await withCache(async secondDirectory => {
      const first = await prepareArchive(manifest, firstDirectory, download);
      const second = await prepareArchive(manifest, secondDirectory, download);
      assert.equal(first.downloaded, true);
      assert.equal(second.downloaded, true);
      assert.notEqual(first.archive, second.archive);
      assert.equal(calls, 2);
    });
  });
});

test('corrupt cached archive fails without silently downloading replacement bytes', async () => {
  await withCache(async cache => {
    const first = await prepareArchive(manifest, cache, async () => new Response(bytes));
    await writeFile(first.archive, Buffer.alloc(bytes.length));
    await assert.rejects(prepareArchive(manifest, cache, async () => assert.fail('must not fetch')), /SHA-256 mismatch/);
  });
});

test('bad download size, digest and HTTP failures leave no published archive', async () => {
  for (const response of [
    () => new Response('short'),
    () => new Response(Buffer.alloc(bytes.length)),
    () => new Response('unavailable', { status: 503 }),
  ]) {
    await withCache(async cache => {
      await assert.rejects(prepareArchive(manifest, cache, async () => response()), /reviewed size|SHA-256 mismatch|HTTP 503/);
      assert.deepEqual(await readdir(cache), []);
    });
  }
});

test('manifest rejects unsupported platforms, invalid versions and invalid digest metadata', () => {
  for (const patch of [
    { version: '../../main' }, { asset: 'codeql-bundle-win64.tar.zst' },
    { sha256: 'not-a-digest' }, { size: 0 }, { note: null },
  ]) assert.throws(() => validateManifest({ ...manifest, ...patch }), /Invalid CodeQL manifest/);
});
