import { execFileSync } from 'node:child_process';
import { appendFileSync } from 'node:fs';

export function needsChecks(paths) {
  return paths.some((path) => !path.endsWith('.md') || path.startsWith('.github/'));
}

if (process.env.GITHUB_OUTPUT) {
  const { BASE_SHA, HEAD_SHA } = process.env;
  for (const sha of [BASE_SHA, HEAD_SHA]) {
    if (!/^[a-f0-9]{40,64}$/.test(sha ?? '')) {
      throw new Error('Expected event base and head commit SHAs; refusing an ambiguous diff.');
    }
  }
  const files = execFileSync('git', ['diff', '--name-only', '-z', BASE_SHA, HEAD_SHA], {
    encoding: 'utf8',
  }).split('\0').filter(Boolean);
  appendFileSync(process.env.GITHUB_OUTPUT, `checks=${needsChecks(files)}\n`);
}
