/**
 * E2E Tests for Prediction Form and Results
 */

const { test, expect } = require('@playwright/test');

test.describe('Prediction Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home and then to prediction form
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.getByRole('button', { name: /New Prediction/i }).click();
    await page.waitForLoadState('networkidle');
  });

  test('should display prediction form with all inputs', async ({ page }) => {
    // Check form title
    await expect(page.getByText('New Prediction')).toBeVisible();
    await expect(page.getByText('Features (10 Parameters)')).toBeVisible();

    // Check all 10 feature inputs are present
    const featureLabels = [
      'Orbital Period',
      'Transit Duration',
      'Transit Depth',
      'Planet Radius',
      'Equilibrium Temperature',
      'Insolation',
      'Signal to Noise',
      'Stellar Temperature',
      'Stellar Log(g)',
      'Stellar Radius',
    ];

    for (const label of featureLabels) {
      const input = page.locator(`text=${label}`).first();
      await expect(input).toBeVisible();
    }

    // Check predict button
    await expect(page.getByRole('button', { name: /Predict Exoplanet/i })).toBeVisible();
  });

  test('should display test sample buttons', async ({ page }) => {
    // Check for test samples section
    await expect(page.getByText('Quick Test Samples')).toBeVisible();

    // Check for sample buttons
    await expect(page.getByText('Typical Exoplanet')).toBeVisible();
    await expect(page.getByText('Hot Jupiter')).toBeVisible();
    await expect(page.getByText('Earth Analog')).toBeVisible();
    await expect(page.getByText('Clear False Positive')).toBeVisible();
  });

  test('should load test sample and make prediction', async ({ page }) => {
    // Load Typical Exoplanet sample
    await page.getByText('Typical Exoplanet').click();

    // Wait a moment for values to populate
    await page.waitForTimeout(500);

    // Click predict button
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();

    // Wait for prediction to complete (with longer timeout for API call)
    await page.waitForTimeout(5000);

    // Should navigate to results page
    await expect(page.getByText('Prediction Result')).toBeVisible();

    // Check for result indicators
    const exoplanetIndicator = page.locator('text=/Exoplanet/i').first();
    await expect(exoplanetIndicator).toBeVisible();
  });

  test('should display prediction results correctly', async ({ page }) => {
    // Load test sample and predict
    await page.getByText('Typical Exoplanet').click();
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
    await page.waitForTimeout(5000);

    // Check result sections are present
    await expect(page.getByText('Confidence')).toBeVisible();
    await expect(page.getByText('Probabilities')).toBeVisible();
    await expect(page.getByText('Input Features')).toBeVisible();

    // Check action buttons
    await expect(page.getByRole('button', { name: /New Prediction/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /Back to Home/i })).toBeVisible();
  });

  test('should navigate back to form from results', async ({ page }) => {
    // Make a prediction
    await page.getByText('Typical Exoplanet').click();
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
    await page.waitForTimeout(5000);

    // Click New Prediction button
    await page.getByRole('button', { name: /New Prediction/i }).click();
    await page.waitForLoadState('networkidle');

    // Should be back on form
    await expect(page.getByText('New Prediction')).toBeVisible();
    await expect(page.getByText('Features (10 Parameters)')).toBeVisible();
  });

  test('should navigate back to home from results', async ({ page }) => {
    // Make a prediction
    await page.getByText('Typical Exoplanet').click();
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
    await page.waitForTimeout(5000);

    // Click Back to Home button
    await page.getByRole('button', { name: /Back to Home/i }).click();
    await page.waitForLoadState('networkidle');

    // Should be on home page
    await expect(page.getByText('Exovisions')).toBeVisible();
    await expect(page.getByText('Model Information')).toBeVisible();
  });

  test('should test all 4 sample predictions', async ({ page }) => {
    const samples = [
      { name: 'Typical Exoplanet', expectExoplanet: true },
      { name: 'Hot Jupiter', expectExoplanet: false },
      { name: 'Earth Analog', expectExoplanet: false },
      { name: 'Clear False Positive', expectExoplanet: false },
    ];

    for (const sample of samples) {
      // Load sample
      await page.getByText(sample.name).click();
      await page.waitForTimeout(500);

      // Make prediction
      await page.getByRole('button', { name: /Predict Exoplanet/i }).click();
      await page.waitForTimeout(5000);

      // Verify we got results
      await expect(page.getByText('Prediction Result')).toBeVisible();

      // Go back to form for next sample
      if (sample !== samples[samples.length - 1]) {
        await page.getByRole('button', { name: /New Prediction/i }).click();
        await page.waitForLoadState('networkidle');
      }
    }
  });
});
