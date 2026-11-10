import { cp, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';
import { setTimeout } from 'node:timers/promises';

console.log('Teaching workload: waiting 20 seconds to simulate a slow build.');
await setTimeout(20_000);
const root = fileURLToPath(new URL('../', import.meta.url));
const output = join(root, 'dist');
await mkdir(join(output, 'src'), { recursive: true });
await cp(join(root, 'src', 'server.js'), join(output, 'src', 'server.js'));
await cp(join(root, 'node_modules', 'picocolors'), join(output, 'node_modules', 'picocolors'), {
  recursive: true,
});
await cp(join(root, 'package-lock.json'), join(output, 'package-lock.json'));
await cp(join(root, 'package.json'), join(output, 'package.json'));
await writeFile(join(output, 'BUILD.txt'), 'Actions Advanced teaching artifact; local staging only.\n');
