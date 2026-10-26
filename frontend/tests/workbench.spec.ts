import { test, expect } from '@playwright/test';
import { readFile } from 'node:fs/promises';

const ready = async (page: import('@playwright/test').Page, step = 8, ceiling = 20) => {
  await expect(page.getByText(`Replay step ${step} of ${ceiling}`, { exact: true })).toBeVisible();
  await expect(page.getByRole('img', { name: 'Posterior concentration map', exact: true })).toBeVisible();
};

test('documentary notebook: acquire, replay, policy, reveal, rotation, export and bounds', async ({ page }) => {
  await page.goto('http://127.0.0.1:8104');
  await expect(page.getByRole('heading', { name: 'A record of the unseen.' })).toBeVisible();
  await ready(page);
  await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(20, 14, 10)');
  await expect(page.locator('.reconstruction .field-map svg')).toHaveCSS('transform', 'none');
  await page.screenshot({ path: 'artifacts/notebook-desktop.png', fullPage: true, animations: 'disabled' });
  await page.screenshot({ path: 'artifacts/notebook-hero.png', fullPage: false, animations: 'disabled' });

  await page.getByRole('button', { name: 'Acquire sample +' }).click();
  await ready(page, 9);
  await expect(page.locator('#ledger tbody tr')).toHaveCount(9);
  await page.getByRole('slider', { name: 'Observation replay' }).fill('4');
  await ready(page, 4);
  await expect(page.locator('#ledger tbody tr')).toHaveCount(4);
  const changedPolicy = page.waitForResponse(r => r.url().includes('/api/survey?') && r.url().includes('policy=grid') && r.url().includes('budget=4'));
  await page.getByLabel('Sampling policy', { exact: true }).selectOption('grid');
  await changedPolicy;
  await ready(page, 4);
  await expect(page.locator('.survey-record')).toContainText('Regular grid');

  await page.getByRole('button', { name: 'Reveal evaluator map' }).click();
  await expect(page.getByRole('img', { name: 'Evaluator-only synthetic ground truth' })).toBeVisible();
  const mesh = page.locator('.surface polygon').first();
  const oldPoints = await mesh.getAttribute('points');
  await page.getByRole('slider', { name: 'Rotate 3D surface' }).fill('1.21');
  await expect(mesh).not.toHaveAttribute('points', oldPoints!);
  await expect(page.locator('.surface')).toHaveCSS('transform', 'none');
  const download = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export complete audit ↓' }).click();
  const downloaded = await download;
  expect(downloaded.suggestedFilename()).toBe('soilquest-audit.json');
  const audit = JSON.parse(await readFile((await downloaded.path())!, 'utf8'));
  expect(audit.synthetic).toBe(true);
  expect(audit.records).toHaveLength(4);
  expect(audit.policy).toBe('grid');

  await page.getByLabel('Sample ceiling', { exact: true }).fill('1');
  await page.getByLabel('Field family', { exact: true }).selectOption('smooth');
  await ready(page, 1, 1);
  await expect(page.locator('#ledger tbody tr')).toHaveCount(1);
  await expect(page.getByRole('button', { name: 'Acquire sample +' })).toBeDisabled();
  await page.getByLabel('Sample ceiling', { exact: true }).fill('100');
  await expect(page.getByLabel('Sample ceiling', { exact: true })).toHaveValue('40');
  await page.getByLabel('Field seed', { exact: true }).fill('-2');
  await expect(page.getByLabel('Field seed', { exact: true })).toHaveValue('0');
});

test('390px field notebook reflows without page overflow', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://127.0.0.1:8104');
  await ready(page);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
  await expect(page.getByLabel('Field family', { exact: true })).toBeVisible();
  await page.screenshot({ path: 'artifacts/notebook-mobile.png', fullPage: true, animations: 'disabled' });
  await page.getByRole('button', { name: 'Acquire sample +' }).click();
  await ready(page, 9);
  await page.getByRole('button', { name: 'Reveal evaluator map' }).click();
  await expect(page.getByRole('img', { name: 'Evaluator-only synthetic ground truth' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
});

test('reduced motion: no decorative animation, no autoplay, manual replay preserved', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('http://127.0.0.1:8104');
  await ready(page);
  await expect(page.locator('.notebook-heading')).toHaveCSS('animation-name', 'none');
  await expect(page.locator('.lower-third')).toHaveCSS('animation-name', 'none');
  await expect(page.locator('html')).toHaveCSS('scroll-behavior', 'auto');
  await expect(page.getByRole('button', { name: 'Manual replay' })).toBeDisabled();
  await page.getByRole('button', { name: 'Acquire sample +' }).click();
  await ready(page, 9);
  await page.getByRole('slider', { name: 'Observation replay' }).fill('3');
  await ready(page, 3);
  await expect(page.locator('#ledger tbody tr')).toHaveCount(3);
  await page.screenshot({ path: 'artifacts/notebook-reduced-motion.png', fullPage: true, animations: 'disabled' });
});
