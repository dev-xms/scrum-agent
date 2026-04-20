// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  outputDir: './tests/results/playwright',
  use: {
    baseURL: 'http://localhost:8080',
  },
  // Server started externally via tests/scripts/run_e2e_tests.py
});
