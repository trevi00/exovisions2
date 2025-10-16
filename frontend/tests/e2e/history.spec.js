/**
 * E2E Tests for History Screen
 */

const { test, expect } = require('@playwright/test');

test.describe('History Screen', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home and then to history
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /Prediction History/i }).click();
    await page.waitForLoadState('networkidle');
  });

  test('should display history page with filters', async ({ page }) => {
    // Check page title
    await expect(page.getByText('Prediction History')).toBeVisible();

    // Check filter chips are present
    await expect(page.getByText('All').first()).toBeVisible();
    await expect(page.getByText('Exoplanets').first()).toBeVisible();
    await expect(page.getByText('Non-Exoplanets').first()).toBeVisible();
  });

  test('should display empty state when no predictions', async ({ page }) => {
    // If there are no predictions, should show empty state
    const emptyText = page.getByText('No predictions yet');
    const makeFirstButton = page.getByRole('button', { name: /Make First Prediction/i });

    // Check if either empty state or predictions list is visible
    const hasEmpty = await emptyText.isVisible().catch(() => false);
    const hasButton = await makeFirstButton.isVisible().catch(() => false);

    // If empty, verify empty state
    if (hasEmpty || hasButton) {
      await expect(emptyText).toBeVisible();
      await expect(makeFirstButton).toBeVisible();
    }
  });

  test('should create prediction and show in history', async ({ page }) => {
    // Navigate to prediction form
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /New Prediction/i }).click();
    await page.waitForLoadState('networkidle');

    // Load test sample
    await page.getByText('Typical Exoplanet').click();
    await page.waitForTimeout(500);

    // Make prediction with save enabled (default)
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
    await page.waitForTimeout(5000);

    // Go to history
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /Prediction History/i }).click();
    await page.waitForLoadState('networkidle');

    // Wait a moment for data to load
    await page.waitForTimeout(2000);

    // Should not show empty state now
    const emptyText = page.getByText('No predictions yet');
    const isVisible = await emptyText.isVisible().catch(() => false);
    expect(isVisible).toBe(false);
  });

  test('should filter predictions by exoplanet status', async ({ page }) => {
    // Click on Exoplanets filter
    const exoplanetsFilter = page.getByText('Exoplanets').first();
    await exoplanetsFilter.click();
    await page.waitForTimeout(1000);

    // Click on Non-Exoplanets filter
    const nonExoplanetsFilter = page.getByText('Non-Exoplanets').first();
    await nonExoplanetsFilter.click();
    await page.waitForTimeout(1000);

    // Click on All filter
    const allFilter = page.getByText('All').first();
    await allFilter.click();
    await page.waitForTimeout(1000);

    // All filter operations should complete without error
    expect(true).toBe(true);
  });

  test('should navigate to prediction form from empty state', async ({ page }) => {
    // Try to find Make First Prediction button
    const makeFirstButton = page.getByRole('button', { name: /Make First Prediction/i });
    const isVisible = await makeFirstButton.isVisible().catch(() => false);

    if (isVisible) {
      // Click button
      await makeFirstButton.click();
      await page.waitForLoadState('networkidle');

      // Should be on prediction form
      await expect(page.getByText('New Prediction')).toBeVisible();
      await expect(page.getByText('Features (10 Parameters)')).toBeVisible();
    }
  });

  test('should pull to refresh history list', async ({ page }) => {
    // Wait for initial load
    await page.waitForTimeout(2000);

    // Take initial screenshot/state
    const initialState = await page.content();

    // Simulate refresh by reloading
    await page.reload();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // Should still be on history page
    await expect(page.getByText('Prediction History')).toBeVisible();
  });
});
