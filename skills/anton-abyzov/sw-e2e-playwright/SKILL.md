---
name: e2e-playwright
description: Playwright 是一款专注于端到端（end-to-end）测试的工具，由 Google 开发。它非常适合用于编写端到端测试用例、实现浏览器自动化操作，以及调试那些容易出错的测试脚本（即那些运行结果不稳定的测试）。
---

# E2E（端到端）Playwright测试专家

## 核心专长

### 1. Playwright基础
**浏览器自动化**：
- 支持多种浏览器（Chromium、Firefox、WebKit）
- 实现上下文隔离和并行执行
- 自动等待和操作性检查
- 网络请求拦截与模拟
- 文件上传与下载
- 地理位置和权限处理
- 身份验证状态管理

**测试结构**：
```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should login successfully', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('should show validation errors', async ({ page }) => {
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });
});
```

### 2. 页面对象模型（Page Object Model, POM）
**模式**：封装页面交互逻辑以提高可维护性

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async loginWithGoogle() {
    await this.page.getByRole('button', { name: 'Continue with Google' }).click();
    // Handle OAuth popup
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}

// Usage in tests
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### 3. 测试固定装置（Test Fixtures）与自定义上下文
**固定装置**：可重用的设置/清理逻辑

```typescript
// fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type AuthFixtures = {
  authenticatedPage: Page;
  loginPage: LoginPage;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup: Login before test
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForURL('/dashboard');

    await use(page);

    // Teardown: Logout after test
    await page.getByRole('button', { name: 'Logout' }).click();
  },

  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);
  },
});

export { expect } from '@playwright/test';

// Usage
test('authenticated user can view profile', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  await expect(authenticatedPage.getByText('Profile Settings')).toBeVisible();
});
```

### 4. 使用Playwright进行API测试
**模式**：在E2E测试过程中同时测试后端API

```typescript
import { test, expect } from '@playwright/test';

test.describe('API Testing', () => {
  test('should fetch user data', async ({ request }) => {
    const response = await request.get('/api/users/123');

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toMatchObject({
      id: 123,
      email: expect.any(String),
      name: expect.any(String),
    });
  });

  test('should handle authentication', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'user@example.com',
        password: 'password123',
      },
    });

    expect(response.ok()).toBeTruthy();
    const { token } = await response.json();
    expect(token).toBeTruthy();

    // Use token in subsequent requests
    const profileResponse = await request.get('/api/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    expect(profileResponse.ok()).toBeTruthy();
  });

  test('should mock API responses', async ({ page }) => {
    await page.route('/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([
          { id: 1, name: 'John Doe' },
          { id: 2, name: 'Jane Smith' },
        ]),
      });
    });

    await page.goto('/users');
    await expect(page.getByText('John Doe')).toBeVisible();
    await expect(page.getByText('Jane Smith')).toBeVisible();
  });
});
```

### 5. 可视化回归测试
**模式**：通过截图对比来检测用户界面变化

```typescript
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches baseline', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('component states', async ({ page }) => {
    await page.goto('/components');

    // Default state
    const button = page.getByRole('button', { name: 'Submit' });
    await expect(button).toHaveScreenshot('button-default.png');

    // Hover state
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');

    // Disabled state
    await page.evaluate(() => {
      document.querySelector('button')?.setAttribute('disabled', 'true');
    });
    await expect(button).toHaveScreenshot('button-disabled.png');
  });

  test('responsive screenshots', async ({ page }) => {
    await page.goto('/');

    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('homepage-desktop.png');

    // Tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('homepage-tablet.png');

    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('homepage-mobile.png');
  });
});
```

### 6. 移动设备模拟与测试
**模式**：测试应用程序在移动设备上的响应性和触控交互

```typescript
import { test, expect, devices } from '@playwright/test';

test.use(devices['iPhone 13 Pro']);

test.describe('Mobile Experience', () => {
  test('should render mobile navigation', async ({ page }) => {
    await page.goto('/');

    // Mobile menu should be visible
    await expect(page.getByRole('button', { name: 'Menu' })).toBeVisible();

    // Desktop nav should be hidden
    await expect(page.getByRole('navigation').first()).toBeHidden();
  });

  test('touch gestures', async ({ page }) => {
    await page.goto('/gallery');

    const image = page.getByRole('img').first();

    // Swipe left
    await image.dispatchEvent('touchstart', { touches: [{ clientX: 300, clientY: 200 }] });
    await image.dispatchEvent('touchmove', { touches: [{ clientX: 100, clientY: 200 }] });
    await image.dispatchEvent('touchend');

    await expect(page.getByText('Next Image')).toBeVisible();
  });

  test('landscape orientation', async ({ page }) => {
    await page.setViewportSize({ width: 812, height: 375 }); // iPhone landscape
    await page.goto('/video');

    await expect(page.locator('video')).toHaveCSS('width', '100%');
  });
});

// Test across multiple devices
for (const deviceName of ['iPhone 13', 'Pixel 5', 'iPad Pro']) {
  test.describe(`Device: ${deviceName}`, () => {
    test.use(devices[deviceName]);

    test('critical user flow', async ({ page }) => {
      await page.goto('/');
      // Test critical flow on each device
    });
  });
}
```

### 7. 可访问性测试
**模式**：自动化进行可访问性检查

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('should not have accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('keyboard navigation', async ({ page }) => {
    await page.goto('/form');

    // Tab through form fields
    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Email')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByLabel('Password')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Submit' })).toBeFocused();

    // Submit with Enter
    await page.keyboard.press('Enter');
  });

  test('screen reader support', async ({ page }) => {
    await page.goto('/');

    // Check ARIA labels
    await expect(page.getByRole('navigation', { name: 'Main' })).toBeVisible();
    await expect(page.getByRole('main')).toHaveAttribute('aria-label', 'Main content');

    // Check alt text
    const images = page.getByRole('img');
    for (const img of await images.all()) {
      await expect(img).toHaveAttribute('alt');
    }
  });
});
```

### 8. 性能测试
**模式**：监控应用程序的性能指标

```typescript
import { test, expect } from '@playwright/test';

test.describe('Performance', () => {
  test('page load performance', async ({ page }) => {
    await page.goto('/');

    const performanceMetrics = await page.evaluate(() => {
      const perfData = window.performance.timing;
      return {
        loadTime: perfData.loadEventEnd - perfData.navigationStart,
        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
      };
    });

    expect(performanceMetrics.loadTime).toBeLessThan(3000); // 3s max
    expect(performanceMetrics.domContentLoaded).toBeLessThan(2000); // 2s max
  });

  test('Core Web Vitals', async ({ page }) => {
    await page.goto('/');

    const vitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lcp = entries.find(e => e.entryType === 'largest-contentful-paint');
          const fid = entries.find(e => e.entryType === 'first-input');
          const cls = entries.find(e => e.entryType === 'layout-shift');

          resolve({ lcp: lcp?.startTime, fid: fid?.processingStart, cls: cls?.value });
        }).observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] });
      });
    });

    expect(vitals.lcp).toBeLessThan(2500); // Good LCP
    expect(vitals.fid).toBeLessThan(100);  // Good FID
    expect(vitals.cls).toBeLessThan(0.1);  // Good CLS
  });
});
```

### 9. 高级配置
**playwright.config.ts**：配置文件示例

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['json', { outputFile: 'test-results/results.json' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // Mobile browsers
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
    // Tablet browsers
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

### 10. 持续集成/持续部署（CI/CD）集成
**GitHub Actions**：自动化部署流程

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          BASE_URL: https://staging.example.com

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - name: Upload traces
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-traces
          path: test-results/
```

### 11. 调试策略
**工具与技术**：
- 使用调试工具和技术来定位问题

```typescript
// 1. Debug mode (headed browser + slow motion)
test('debug example', async ({ page }) => {
  await page.goto('/');
  await page.pause(); // Pauses execution, opens inspector
});

// 2. Console logs
test('capture console', async ({ page }) => {
  page.on('console', msg => console.log(`Browser: ${msg.text()}`));
  await page.goto('/');
});

// 3. Network inspection
test('inspect network', async ({ page }) => {
  page.on('request', request => console.log('Request:', request.url()));
  page.on('response', response => console.log('Response:', response.status()));
  await page.goto('/');
});

// 4. Screenshots on failure
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    await page.screenshot({
      path: `screenshots/${testInfo.title}.png`,
      fullPage: true
    });
  }
});

// 5. Trace viewer
// Run: npx playwright test --trace on
// View: npx playwright show-trace trace.zip
```

**常见调试命令**：
- [列出常用的调试命令]

### 12. 处理不可靠的测试（Flaky Tests）
**提高测试稳定性的方法**：
- [列出提高测试稳定性的策略]

## 最佳实践

### 测试组织
- [描述测试组织的最佳实践]

### 命名规范
- 测试文件：`.spec.ts` 或 `.test.ts`
- 页面对象文件：`.Page.ts`
- 固定装置文件：`.fixture.ts`
- 测试用例名称：例如：`should allow user to login with valid credentials`（“应允许用户使用有效凭据登录”）

### 性能优化
- **并行执行**：在多个线程或进程中同时运行测试
- **测试拆分**：将测试分布在不同的CI服务器上执行
- **选择性测试**：使用标签或注释来区分不同类型的测试（例如：基本测试、性能测试）
- **重用身份验证状态**：保存身份验证信息并在多个测试中重复使用
- **模拟外部API**：减少网络延迟和测试不稳定性的风险

### 安全性考虑
- **避免在测试文件中存储敏感信息**（如密码）
- **使用环境变量管理敏感数据**
- **将测试数据与生产环境分离**
- **在每次测试后清除浏览器缓存和存储数据**
- **使用一次性测试账户**

## 常见模式与技巧

### 身份验证状态的复用
- [描述如何复用身份验证状态]

### 多标签页/窗口测试
- [描述如何处理多标签页或窗口的测试场景]

### 文件上传/下载
- [描述文件上传和下载的操作流程]

## 故障排除

### 常见问题及解决方法
- **超时问题**：增加超时时间，使用合适的等待策略
- **不可靠的元素选择器**：使用稳定且唯一的元素选择器（如角色、标签、测试ID）
- **竞态条件**：等待网络请求完成，使用明确的等待机制
- **身份验证失败**：清除浏览器缓存，检查身份验证状态
- **截图不一致**：更新基准截图，禁用动画效果

### 调试检查清单
- [列出需要检查的调试事项]

## 资源
- **官方文档**：https://playwright.dev
- **API参考**：https://playwright.dev/docs/api/class-playwright
- **最佳实践**：https://playwright.dev/docs/best-practices
- **示例代码**：https://github.com/microsoft/playwright/tree/main/examples
- **社区资源**：https://github.com/microsoft/playwright/discussions