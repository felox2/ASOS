import { test, expect } from '@playwright/test';

test('test-search', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('link', { name: 'EShop' })).toBeVisible();
  await expect(page.getByRole('link', { name: 'Product photo Tablet Latest' })).toBeVisible();
  await page.getByPlaceholder('search').click();
  

  await page.getByPlaceholder('search').click();
  await page.getByPlaceholder('search').fill('Tab');
  await expect(page.locator('div').filter({ hasText: /^TabletLatest model tablet€499\.99$/ }).nth(3)).toBeVisible();
  await page.getByRole('link', { name: 'Tablet Latest model tablet €' }).click();
  await expect(page.getByRole('heading', { name: 'Tablet' })).toBeVisible();
});

