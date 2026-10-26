import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', timeout: 30000,
  use: { viewport: { width: 1440, height: 1100 }, launchOptions: { args: ['--no-sandbox'], ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE } : {}) } },
  webServer: { command: `${process.env.SOILQUEST_PYTHON || '../.venv/bin/python'} -m uvicorn soilquest.api:app --app-dir .. --host 127.0.0.1 --port 8104`, url: 'http://127.0.0.1:8104/api/health', reuseExistingServer: !process.env.CI, timeout: 30000 },
});
