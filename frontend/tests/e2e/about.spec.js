/**
 * E2E Tests for About Screen
 */

const { test, expect } = require('@playwright/test');

test.describe('About Screen', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home and then to about
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /About/i }).click();
    await page.waitForLoadState('networkidle');
  });

  test('should display app information', async ({ page }) => {
    // Check page title
    await expect(page.getByText('About')).toBeVisible();

    // Check app info
    await expect(page.getByText('Exovisions')).toBeVisible();
    await expect(page.getByText('Version 1.0.0')).toBeVisible();
    await expect(page.getByText('NASA Space Apps Challenge 2024')).toBeVisible();
  });

  test('should display technology stack', async ({ page }) => {
    // Check technology stack section
    await expect(page.getByText('Technology Stack')).toBeVisible();

    // Check for key technologies
    await expect(page.getByText(/React Native/)).toBeVisible();
    await expect(page.getByText(/FastAPI/)).toBeVisible();
    await expect(page.getByText(/LightGBM/)).toBeVisible();
    await expect(page.getByText(/MySQL/)).toBeVisible();
  });

  test('should display training datasets information', async ({ page }) => {
    // Check datasets section
    await expect(page.getByText('Training Datasets')).toBeVisible();

    // Check for all three missions
    await expect(page.getByText('Kepler Mission')).toBeVisible();
    await expect(page.getByText('9,618 samples')).toBeVisible();

    await expect(page.getByText('K2 Mission')).toBeVisible();
    await expect(page.getByText('4,104 samples')).toBeVisible();

    await expect(page.getByText('TESS Mission')).toBeVisible();
    await expect(page.getByText('7,773 samples')).toBeVisible();

    await expect(page.getByText('21,495 samples')).toBeVisible();
  });

  test('should display model information', async ({ page }) => {
    // Check model info section
    await expect(page.getByText('Model Information')).toBeVisible();

    // Check for model details
    await expect(page.getByText('3-Class Classification')).toBeVisible();
    await expect(page.getByText(/CONFIRMED, CANDIDATE, FALSE_POSITIVE/)).toBeVisible();
    await expect(page.getByText(/10 parameters/)).toBeVisible();
    await expect(page.getByText(/Stacking Ensemble/)).toBeVisible();
  });

  test('should display resource links', async ({ page }) => {
    // Check resources section
    await expect(page.getByText('Resources')).toBeVisible();

    // Check for link buttons
    await expect(page.getByRole('button', { name: /NASA Space Apps Challenge/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /NASA Exoplanet Archive/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /API Documentation/i })).toBeVisible();
  });

  test('should display copyright information', async ({ page }) => {
    // Check footer
    await expect(page.getByText('© 2024 Exovisions Team')).toBeVisible();
    await expect(page.getByText('NASA Space Apps Challenge')).toBeVisible();
  });

  test('should have clickable external links', async ({ page }) => {
    // Test that link buttons are clickable (without actually following)
    const nasaButton = page.getByRole('button', { name: /NASA Space Apps Challenge/i });
    await expect(nasaButton).toBeEnabled();

    const archiveButton = page.getByRole('button', { name: /NASA Exoplanet Archive/i });
    await expect(archiveButton).toBeEnabled();

    const apiButton = page.getByRole('button', { name: /API Documentation/i });
    await expect(apiButton).toBeEnabled();
  });
});
