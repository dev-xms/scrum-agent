// BKI-002: The Smart Plate — E2E Playwright Spec
// Covers: US.4 (search by name), US.6 (dark mode toggle + persistence)

const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8080';

const RECIPES = [
  { id: 1, title: 'Pasta Bolognese', ingredients: 'Noodles, beef', instructions: 'Boil and mix' },
  { id: 2, title: 'Chicken Soup', ingredients: 'Chicken, water', instructions: 'Simmer' },
  { id: 3, title: 'Pasta Carbonara', ingredients: 'Noodles, egg', instructions: 'Toss' },
];

test.beforeEach(async ({ page }) => {
  await page.goto(BASE_URL);
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});

// --- US.4: Search Recipes by Name ---

test('US4: partial name match shows only matching recipes', async ({ page }) => {
  await page.evaluate((recipes) => {
    localStorage.setItem('smart_plate_recipes', JSON.stringify(recipes));
  }, RECIPES);
  await page.reload();

  await page.fill('[data-testid="input-search"]', 'pasta');
  const items = page.locator('[data-testid="recipe-item"]');
  await expect(items).toHaveCount(2);
});

test('US4: no match shows empty-state message', async ({ page }) => {
  await page.evaluate((recipes) => {
    localStorage.setItem('smart_plate_recipes', JSON.stringify(recipes));
  }, RECIPES);
  await page.reload();

  await page.fill('[data-testid="input-search"]', 'pizza');
  await expect(page.locator('[data-testid="empty-state"]')).toBeVisible();
  await expect(page.locator('[data-testid="recipe-item"]')).toHaveCount(0);
});

test('US4: clearing search restores all recipes', async ({ page }) => {
  await page.evaluate((recipes) => {
    localStorage.setItem('smart_plate_recipes', JSON.stringify(recipes));
  }, RECIPES);
  await page.reload();

  await page.fill('[data-testid="input-search"]', 'pasta');
  await expect(page.locator('[data-testid="recipe-item"]')).toHaveCount(2);

  await page.fill('[data-testid="input-search"]', '');
  await expect(page.locator('[data-testid="recipe-item"]')).toHaveCount(3);
});

// --- US.6: Dark Mode Toggle ---

test('US6: clicking dark mode toggle adds dark class to body', async ({ page }) => {
  await page.click('[data-testid="btn-dark-mode"]');
  await expect(page.locator('body')).toHaveClass(/dark/);
});

test('US6: clicking dark mode toggle again removes dark class', async ({ page }) => {
  await page.click('[data-testid="btn-dark-mode"]');
  await page.click('[data-testid="btn-dark-mode"]');
  const cls = await page.locator('body').getAttribute('class');
  expect(cls ?? '').not.toMatch(/dark/);
});

test('US6: dark mode preference persists after reload', async ({ page }) => {
  await page.click('[data-testid="btn-dark-mode"]');
  await page.reload();
  await expect(page.locator('body')).toHaveClass(/dark/);
});
