/**
 * Playwright Configuration
 * E2E Testing for Exovisions React Native Web App
 */

const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',

  // Maximum time one test can run for
  timeout: 60 * 1000,

  // Test execution settings
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 1,

  // Reporter to use
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list'],
  ],

  // Shared settings for all projects
  use: {
    // Base URL for tests
    baseURL: 'http://localhost:19006',

    // Collect trace when retrying the failed test
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on failure
    video: 'retain-on-failure',
  },

  // Configure projects for major browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Run your local dev server before starting the tests
  // NOTE: Start server manually with `npm run web` before running tests
  webServer: {
    command: 'npm run web',
    url: 'http://localhost:19006',
    reuseExistingServer: true, // Use existing server if already running
    timeout: 180 * 1000, // Increased timeout to 3 minutes
  },
});
