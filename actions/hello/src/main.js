import * as core from '@actions/core';

export async function run() {
  try {
    const name = core.getInput('name', { required: true });
    if (!/^[A-Za-z0-9 -]{1,40}$/.test(name)) {
      throw new Error('Use 1-40 letters, numbers, spaces, or hyphens.');
    }
    core.debug('Validated the fake learner identifier.');
    core.setOutput('greeting', `Hello, ${name}`);
    core.info('Greeting output created; no external calls were made.');
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : 'Unexpected action failure');
  }
}
