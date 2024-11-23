import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('/');
  await page.locator('div').filter({ hasText: /^€499\.99toCart$/ }).getByRole('button').click();
  await expect(page.getByRole('button', { name: '1' })).toBeVisible();

  await page.locator('div').filter({ hasText: /^€199\.99toCart$/ }).getByRole('button').click();
  await expect(page.getByRole('button', { name: '2' })).toBeVisible();
  await page.getByRole('button', { name: '2' }).click();
  await expect(page.getByText('€699.98')).toBeVisible();
  await page.getByRole('link', { name: 'viewCart' }).click();
});