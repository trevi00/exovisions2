/**
 * E2E Tests for Home Screen
 */

const { test, expect } = require('@playwright/test');

test.describe('Home Screen', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home page
    await page.goto('/');
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should display app title and header', async ({ page }) => {
    // Check for main title
    await expect(page.getByText('Exovisions')).toBeVisible();
    await expect(page.getByText('NASA Space Apps Challenge')).toBeVisible();
    await expect(page.getByText('외계행성 탐지 머신러닝 시스템')).toBeVisible();
  });

  test('should show API status', async ({ page }) => {
    // Wait for API health check
    await page.waitForTimeout(2000);

    // Check for API status chip - it should be either Connected or Disconnected
    const apiStatus = page.getByText(/API:/);
    await expect(apiStatus).toBeVisible();
  });

  test('should display model information', async ({ page }) => {
    // Check model info card
    await expect(page.getByText('Model Information')).toBeVisible();
    await expect(page.getByText('3-Class Classification')).toBeVisible();
    await expect(page.getByText('CONFIRMED')).toBeVisible();
    await expect(page.getByText('CANDIDATE')).toBeVisible();
    await expect(page.getByText('FALSE POSITIVE')).toBeVisible();
    await expect(page.getByText('Kepler, K2, TESS (21,495 samples)')).toBeVisible();
  });

  test('should have navigation buttons', async ({ page }) => {
    // Check for all navigation buttons
    await expect(page.getByRole('button', { name: /New Prediction/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /Prediction History/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /About/i })).toBeVisible();
  });

  test('should navigate to Prediction Form', async ({ page }) => {
    // Click New Prediction button
    await page.getByRole('button', { name: /New Prediction/i }).click();

    // Wait for navigation
    await page.waitForLoadState('networkidle');

    // Check we're on prediction form page
    await expect(page.getByText('New Prediction')).toBeVisible();
    await expect(page.getByText('Features (10 Parameters)')).toBeVisible();
  });

  test('should navigate to History', async ({ page }) => {
    // Click Prediction History button
    await page.getByRole('button', { name: /Prediction History/i }).click();

    // Wait for navigation
    await page.waitForLoadState('networkidle');

    // Check we're on history page
    await expect(page.getByText('Prediction History')).toBeVisible();
  });

  test('should navigate to About', async ({ page }) => {
    // Click About button
    await page.getByRole('button', { name: /About/i }).click();

    // Wait for navigation
    await page.waitForLoadState('networkidle');

    // Check we're on about page
    await expect(page.getByText('Exovisions')).toBeVisible();
    await expect(page.getByText('Technology Stack')).toBeVisible();
  });
});
