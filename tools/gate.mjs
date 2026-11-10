const { DETECTION_RESULT, CHECKS_REQUIRED, CHECK_RESULT } = process.env;
if (DETECTION_RESULT !== 'success') {
  throw new Error('Change detection did not succeed.');
}
if (!['true', 'false'].includes(CHECKS_REQUIRED)) {
  throw new Error('Missing or invalid impact decision.');
}
if (CHECKS_REQUIRED === 'true' && CHECK_RESULT !== 'success') {
  throw new Error('Required application checks did not succeed.');
}
if (CHECKS_REQUIRED === 'false' && CHECK_RESULT !== 'skipped') {
  throw new Error('Unexpected outcome for an explicitly unnecessary check.');
}
console.log('Applicable validation satisfied.');
