# E2E Testing Guide

Playwright를 사용한 Exovisions 프론트엔드 E2E 테스트입니다.

## 📋 Test Coverage

### Test Suites

1. **home.spec.js** - Home Screen Tests
   - App title and header display
   - API status check
   - Model information display
   - Navigation buttons
   - Navigation to other screens

2. **prediction.spec.js** - Prediction Flow Tests
   - Form display with 10 inputs
   - Test sample buttons
   - Load sample and make prediction
   - Display results correctly
   - Navigation between screens
   - All 4 sample predictions

3. **history.spec.js** - History Screen Tests
   - Page display with filters
   - Empty state
   - Create and show prediction in history
   - Filter by exoplanet status
   - Navigate to prediction form
   - Pull to refresh

4. **about.spec.js** - About Screen Tests
   - App information display
   - Technology stack
   - Training datasets
   - Model information
   - Resource links
   - Copyright information

5. **api-integration.spec.js** - API Integration Tests
   - Backend API health check
   - Successful prediction via API
   - Error handling
   - Retrieve prediction history
   - Full prediction workflow
   - Multiple predictions in sequence

## 🚀 Prerequisites

### Backend API Must Be Running
```bash
cd ../backend
python -m uvicorn app.presentation.main:app --host 127.0.0.1 --port 8000
```

Verify API is running:
```bash
curl http://127.0.0.1:8000/api/v1/health
```

## 📦 Installation

Playwright is already installed as a dev dependency:
```bash
npm install
```

Install browser (if not already installed):
```bash
npx playwright install chromium
```

## 🧪 Running Tests

### Run All Tests
```bash
npm run test:e2e
```

### Run Tests with UI Mode (Recommended)
```bash
npm run test:e2e:ui
```

### Run Tests in Headed Mode (See Browser)
```bash
npm run test:e2e:headed
```

### Run Tests in Debug Mode
```bash
npm run test:e2e:debug
```

### Run Specific Test File
```bash
npx playwright test tests/e2e/home.spec.js
```

### Run Tests by Name Pattern
```bash
npx playwright test --grep "should display"
```

### View Test Report
```bash
npm run test:report
```

## 📊 Test Configuration

Configuration is in `playwright.config.js`:

- **Base URL**: http://localhost:19006 (Expo web server)
- **Timeout**: 60 seconds per test
- **Browser**: Chromium
- **Web Server**: Auto-starts with `npm run web`
- **Reports**: HTML report in `test-results/html`

## 🎯 Test Execution Flow

1. Playwright starts Expo web server automatically (`npm run web`)
2. Waits for server to be ready at http://localhost:19006
3. Runs all test files in `tests/e2e/`
4. Generates HTML report
5. Takes screenshots on failure
6. Records video on failure

## 📝 Writing New Tests

### Basic Test Structure
```javascript
const { test, expect } = require('@playwright/test');

test.describe('My Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should do something', async ({ page }) => {
    // Your test code
    await expect(page.getByText('Something')).toBeVisible();
  });
});
```

### Common Patterns

#### Navigation
```javascript
await page.getByRole('button', { name: /Button Name/i }).click();
await page.waitForLoadState('networkidle');
```

#### Form Input
```javascript
await page.getByLabel('Input Label').fill('value');
```

#### Assertions
```javascript
await expect(page.getByText('Expected Text')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
```

#### Wait for API
```javascript
await page.waitForTimeout(2000); // Wait 2 seconds for API
```

## 🐛 Troubleshooting

### Frontend Not Starting
```bash
# Manually start frontend
cd frontend
npm run web
```

### Backend Not Running
```bash
# Start backend
cd backend
python -m uvicorn app.presentation.main:app --host 127.0.0.1 --port 8000
```

### Port Already in Use
```bash
# Kill process on port 19006 (Windows)
netstat -ano | findstr :19006
taskkill /F /PID <pid>

# Kill process on port 19006 (Linux/Mac)
lsof -ti:19006 | xargs kill -9
```

### Tests Timing Out
- Increase timeout in `playwright.config.js`
- Add more `waitForTimeout` calls
- Check network speed and API response time

### Browser Not Installed
```bash
npx playwright install chromium
```

## 📈 Test Metrics

### Current Coverage
- ✅ 5 test suites
- ✅ 35+ test cases
- ✅ All major user flows
- ✅ API integration tests
- ✅ Error handling tests

### Test Areas
- Home page functionality
- Prediction form and results
- History management
- About page information
- API integration
- Navigation between screens
- Test sample predictions
- Filter functionality

## 🔄 Continuous Integration

For CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Install dependencies
  run: cd frontend && npm install

- name: Install Playwright
  run: cd frontend && npx playwright install --with-deps chromium

- name: Start backend
  run: |
    cd backend
    python -m uvicorn app.presentation.main:app --host 127.0.0.1 --port 8000 &
    sleep 10

- name: Run E2E tests
  run: cd frontend && npm run test:e2e

- name: Upload test results
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: playwright-report
    path: frontend/test-results/
```

## 📚 Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Expo Web Documentation](https://docs.expo.dev/workflow/web/)

## ✅ Test Checklist

Before running tests:
- [ ] Backend API is running on port 8000
- [ ] Backend health check passes
- [ ] Playwright browsers are installed
- [ ] Node modules are installed
- [ ] Port 19006 is available

## 🎬 Demo

To see tests in action:
```bash
# Open UI mode to watch tests execute
npm run test:e2e:ui

# Or run in headed mode
npm run test:e2e:headed
```
