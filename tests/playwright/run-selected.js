const { spawnSync } = require('node:child_process');

const selected = process.env.SELECTED_TESTS || '';
const selectedFiles = selected
  .split(',')
  .map((v) => v.trim())
  .filter(Boolean);

const baseArgs = ['playwright', 'test', '-c', 'tests/playwright/playwright.config.js'];
const args = selectedFiles.length > 0 ? [...baseArgs, ...selectedFiles] : baseArgs;

const result = spawnSync('npx', args, { stdio: 'inherit', shell: process.platform === 'win32' });
process.exit(result.status ?? 1);
