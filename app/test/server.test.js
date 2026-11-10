import assert from 'node:assert/strict';
import { once } from 'node:events';
import { test } from 'node:test';
import { setTimeout } from 'node:timers/promises';
import { createApp } from '../src/server.js';

test('health endpoint and unknown route', async () => {
  console.log('Teaching workload: waiting 20 seconds to simulate a slow integration test.');
  await setTimeout(20_000);
  const server = createApp();
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  try {
    const url = `http://127.0.0.1:${server.address().port}`;
    const health = await fetch(`${url}/health`);
    assert.equal(health.status, 200);
    assert.deepEqual(await health.json(), { status: 'ok' });
    const missing = await fetch(`${url}/unknown`);
    assert.equal(missing.status, 404);
    assert.deepEqual(await missing.json(), { error: 'not found' });
  } finally {
    server.closeAllConnections();
    server.close();
    await once(server, 'close');
  }
});
