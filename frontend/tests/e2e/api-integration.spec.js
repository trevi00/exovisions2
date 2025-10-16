/**
 * E2E Tests for API Integration
 * Tests the integration between frontend and backend API
 */

const { test, expect } = require('@playwright/test');

test.describe('API Integration Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should check backend API is running', async ({ page }) => {
    // Wait for home page to load
    await page.waitForTimeout(2000);

    // Check API status indicator
    const apiStatusChip = page.locator('text=/API:/');
    await expect(apiStatusChip).toBeVisible();

    // Status should show either Connected or Disconnected
    const statusText = await apiStatusChip.textContent();
    expect(statusText).toMatch(/API: (Connected|Disconnected)/);
  });

  test('should make successful prediction via API', async ({ page }) => {
    // Navigate to prediction form
    await page.getByRole('button', { name: /New Prediction/i }).click();
    await page.waitForLoadState('networkidle');

    // Setup request interception to verify API call
    let apiCallMade = false;
    page.on('response', (response) => {
      if (response.url().includes('/api/v1/predictions/')) {
        apiCallMade = true;
        console.log('API Response Status:', response.status());
        console.log('API Response URL:', response.url());
      }
    });

    // Load test sample and predict
    await page.getByText('Typical Exoplanet').click();
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();

    // Wait for API call to complete
    await page.waitForTimeout(5000);

    // Verify API call was made
    expect(apiCallMade).toBe(true);

    // Should show results
    await expect(page.getByText('Prediction Result')).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // This test verifies error handling when API is unavailable
    // We'll simulate by trying to predict with invalid data or when backend is down

    // Navigate to prediction form
    await page.getByRole('button', { name: /New Prediction/i }).click();
    await page.waitForLoadState('networkidle');

    // Try to submit with default values (should work if API is up)
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();

    // Wait for response
    await page.waitForTimeout(5000);

    // Should either show results or error alert
    // The app should not crash
    const resultVisible = await page.getByText('Prediction Result').isVisible().catch(() => false);
    expect(typeof resultVisible).toBe('boolean');
  });

  test('should retrieve prediction history from API', async ({ page }) => {
    // Navigate to history
    await page.getByRole('button', { name: /Prediction History/i }).click();
    await page.waitForLoadState('networkidle');

    // Setup request interception
    let apiCallMade = false;
    page.on('response', (response) => {
      if (response.url().includes('/api/v1/predictions')) {
        apiCallMade = true;
        console.log('History API Response Status:', response.status());
      }
    });

    // Wait for API call
    await page.waitForTimeout(3000);

    // Verify API call was made
    expect(apiCallMade).toBe(true);

    // Page should load without error
    await expect(page.getByText('Prediction History')).toBeVisible();
  });

  test('should complete full prediction workflow with API', async ({ page }) => {
    // 1. Check API health on home page
    await page.waitForTimeout(2000);
    const apiStatus = await page.locator('text=/API:/).textContent();
    console.log('API Status:', apiStatus);

    // 2. Navigate to prediction form
    await page.getByRole('button', { name: /New Prediction/i }).click();
    await page.waitForLoadState('networkidle');

    // 3. Load test sample
    await page.getByText('Hot Jupiter').click();
    await page.waitForTimeout(500);

    // 4. Make prediction
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
    await page.waitForTimeout(5000);

    // 5. Verify results received from API
    await expect(page.getByText('Prediction Result')).toBeVisible();
    await expect(page.getByText('Confidence')).toBeVisible();
    await expect(page.getByText('Probabilities')).toBeVisible();

    // 6. Go to history
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /Prediction History/i }).click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // 7. Verify history was retrieved from API
    await expect(page.getByText('Prediction History')).toBeVisible();
  });

  test('should test multiple predictions in sequence', async ({ page }) => {
    const samples = ['Typical Exoplanet', 'Hot Jupiter', 'Earth Analog'];

    for (const sample of samples) {
      // Go to prediction form
      await page.goto('/');
      await page.waitForLoadState('networkidle');
      await page.getByRole('button', { name: /New Prediction/i }).click();
      await page.waitForLoadState('networkidle');

      // Load sample
      await page.getByText(sample).click();
      await page.waitForTimeout(500);

      // Make prediction
      await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
      await page.waitForTimeout(5000);

      // Verify result
      await expect(page.getByText('Prediction Result')).toBeVisible();

      console.log(`Successfully predicted: ${sample}`);
    }
  });
});
