// BKI-001: The Smart Plate — E2E Playwright Spec
// Covers: US.1 (save), US.2 (view list), US.3 (delete)

const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8080';

test.beforeEach(async ({ page }) => {
  await page.goto(BASE_URL);
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});

// --- US.1: Save Recipe ---

test('US1: valid form save persists recipe and shows in list', async ({ page }) => {
  await page.fill('[data-testid="input-title"]', 'Pasta');
  await page.fill('[data-testid="input-ingredients"]', 'Noodles, sauce');
  await page.fill('[data-testid="input-instructions"]', 'Boil and mix');
  await page.click('[data-testid="btn-save"]');

  const items = page.locator('[data-testid="recipe-item"]');
  await expect(items).toHaveCount(1);
  await expect(items.first()).toContainText('Pasta');
});

test('US1: empty title shows validation error and no recipe saved', async ({ page }) => {
  await page.fill('[data-testid="input-ingredients"]', 'Noodles');
  await page.fill('[data-testid="input-instructions"]', 'Boil');
  await page.click('[data-testid="btn-save"]');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="recipe-item"]')).toHaveCount(0);
});

test('US1: empty ingredients shows validation error', async ({ page }) => {
  await page.fill('[data-testid="input-title"]', 'Pasta');
  await page.fill('[data-testid="input-instructions"]', 'Boil');
  await page.click('[data-testid="btn-save"]');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
});

test('US1: empty instructions shows validation error', async ({ page }) => {
  await page.fill('[data-testid="input-title"]', 'Pasta');
  await page.fill('[data-testid="input-ingredients"]', 'Noodles');
  await page.click('[data-testid="btn-save"]');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
});

// --- US.2: View Recipe List ---

test('US2: saved recipes appear on reload', async ({ page }) => {
  await page.evaluate(() => {
    localStorage.setItem('smart_plate_recipes', JSON.stringify([
      { id: 1, title: 'Salad', ingredients: 'Lettuce', instructions: 'Toss' }
    ]));
  });
  await page.reload();

  const items = page.locator('[data-testid="recipe-item"]');
  await expect(items).toHaveCount(1);
  await expect(items.first()).toContainText('Salad');
});

test('US2: empty state shown when no recipes', async ({ page }) => {
  await expect(page.locator('[data-testid="empty-state"]')).toBeVisible();
});

// --- US.3: Delete Recipe ---

test('US3: delete removes recipe from list', async ({ page }) => {
  await page.evaluate(() => {
    localStorage.setItem('smart_plate_recipes', JSON.stringify([
      { id: 1, title: 'Soup', ingredients: 'Water', instructions: 'Boil' }
    ]));
  });
  await page.reload();

  await page.click('[data-testid="btn-delete"]');
  await expect(page.locator('[data-testid="recipe-item"]')).toHaveCount(0);
});

test('US3: delete only removes targeted recipe', async ({ page }) => {
  await page.evaluate(() => {
    localStorage.setItem('smart_plate_recipes', JSON.stringify([
      { id: 1, title: 'Soup', ingredients: 'Water', instructions: 'Boil' },
      { id: 2, title: 'Salad', ingredients: 'Lettuce', instructions: 'Toss' }
    ]));
  });
  await page.reload();

  await page.locator('[data-testid="btn-delete"]').first().click();
  const items = page.locator('[data-testid="recipe-item"]');
  await expect(items).toHaveCount(1);
  await expect(items.first()).toContainText('Salad');
});
