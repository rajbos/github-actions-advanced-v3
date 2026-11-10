import { createHash } from 'node:crypto';
import { createReadStream, createWriteStream } from 'node:fs';
import { appendFile, lstat, mkdir, mkdtemp, readFile, rename, rm } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { pathToFileURL } from 'node:url';

export function validateManifest(manifest) {
  if (!/^\d+\.\d+\.\d+$/.test(manifest.version ?? '') ||
      manifest.asset !== 'codeql-bundle-linux64.tar.zst' ||
      !/^[a-f0-9]{64}$/.test(manifest.sha256 ?? '') ||
      !Number.isSafeInteger(manifest.size) || manifest.size <= 0 ||
      typeof manifest.note !== 'string') {
    throw new Error('Invalid CodeQL manifest: expected a release version, Linux x64 asset, SHA-256, byte size and note.');
  }
}

async function verifyArchive(path, manifest) {
  const info = await lstat(path);
  if (!info.isFile() || info.size !== manifest.size) {
    throw new Error('CodeQL archive is not a regular file of the reviewed size; refusing reuse.');
  }
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(path)) hash.update(chunk);
  if (hash.digest('hex') !== manifest.sha256) {
    throw new Error('CodeQL archive SHA-256 mismatch; refusing extraction or execution.');
  }
}

export async function prepareArchive(manifest, cacheDirectory, fetchArchive = fetch) {
  validateManifest(manifest);
  await mkdir(cacheDirectory, { recursive: true });
  const archive = join(resolve(cacheDirectory), `codeql-${manifest.version}-${manifest.asset}`);
  const existing = await lstat(archive).catch(error => {
    if (error.code === 'ENOENT') return null;
    throw error;
  });
  let downloadMilliseconds = 0;
  let verifyMilliseconds = 0;
  let downloaded = false;
  if (!existing) {
    const temporary = await mkdtemp(join(resolve(cacheDirectory), '.download-'));
    try {
      const url = `https://github.com/github/codeql-action/releases/download/codeql-bundle-v${manifest.version}/${manifest.asset}`;
      const downloadStart = performance.now();
      const response = await fetchArchive(url, { signal: AbortSignal.timeout(300_000) });
      if (!response.ok || !response.body) {
        throw new Error(`CodeQL bundle download failed: HTTP ${response.status}`);
      }
      const candidate = join(temporary, 'archive');
      await pipeline(Readable.fromWeb(response.body), createWriteStream(candidate, { flags: 'wx' }));
      downloadMilliseconds = performance.now() - downloadStart;
      const verifyStart = performance.now();
      await verifyArchive(candidate, manifest);
      verifyMilliseconds = performance.now() - verifyStart;
      await rename(candidate, archive);
      downloaded = true;
    } finally {
      await rm(temporary, { recursive: true, force: true });
    }
  } else {
    const verifyStart = performance.now();
    await verifyArchive(archive, manifest);
    verifyMilliseconds = performance.now() - verifyStart;
  }
  console.log(`CodeQL ${manifest.version}: ${downloaded ? 'downloaded and verified' : 'reused and verified'}; bytes=${manifest.size}; sha256=${manifest.sha256}; download_ms=${Math.round(downloadMilliseconds)}; verify_ms=${Math.round(verifyMilliseconds)}`);
  return { archive, downloaded };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const manifest = JSON.parse(await readFile('examples/codeql-bundle.json', 'utf8'));
  const { archive } = await prepareArchive(manifest, '.cache/codeql-downloads');
  if (process.env.GITHUB_OUTPUT) {
    await appendFile(process.env.GITHUB_OUTPUT, `archive=${archive}\n`);
  }
}
