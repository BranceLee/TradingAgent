import type { PlaywrightTestConfig } from '@playwright/test';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

/**
 * See https://playwright.dev/docs/test-configuration.
 */
const config: PlaywrightTestConfig = {
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    headless: false,
    /* Maximum time each action such as `click()` can take. Defaults to 0 (no limit). */
    actionTimeout: 15000,
    navigationTimeout: 30000,
    /* Base URL to use in actions like `await page.goto('/')`. */
    // baseURL: 'http://localhost:8501/',
    browserName: 'chromium',
    ignoreHTTPSErrors: true,

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
    viewport: {
      width: 1920,
      height: 1080,
    },
  },
  testDir: './',
  /* Maximum time one test can run for. */
  timeout: 30 * 1000,
  expect: {
    /**
     * Maximum time expect() should wait for the condition to be met.
     * For example in `await expect(locator).toHaveText();`
     */
    timeout: 30000
  },
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: 1,
  reporter: [['list']],
};

export default config;
