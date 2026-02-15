---
name: ui-testing
description: Cypress、Testing Library 的 UI 测试专家，擅长进行 UI 组件的测试或组件测试的实现。
---

# UI 测试技能

精通使用 **Cypress** 和 **Testing Library** 进行 UI 测试。如需深入了解 Playwright 的相关技能，请参阅 `e2e-playwright` 部分。

## 框架选择指南

| 框架 | 适用场景 | 主要优势 |
|-----------|----------|--------------|
| **Playwright** | 结合 E2E 测试、跨浏览器测试 | 支持自动等待、多浏览器测试 → 可使用 `e2e-playwright` 技能 |
| **Cypress** | 适用于 E2E 测试，尤其适合开发者 | 支持时间旅行调试、实时页面重载功能 |
| **Testing Library** | 适用于组件测试 | 以用户为中心的查询方式、注重无障碍性 |

---

## 1. Cypress（E2E 测试）

**为什么选择 Cypress？**
- 对开发者非常友好的 API 接口
- 支持实时页面重载
- 提供时间旅行调试功能
- 支持截图和视频录制
- 内置了模拟（stubbing）和 mocking 功能

#### 基本测试示例

```javascript
describe('User Authentication', () => {
  it('should login with valid credentials', () => {
    cy.visit('/login');

    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('SecurePass123!');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('h1').should('have.text', 'Welcome, User');
  });

  it('should show error with invalid credentials', () => {
    cy.visit('/login');

    cy.get('input[name="email"]').type('wrong@example.com');
    cy.get('input[name="password"]').type('WrongPass');
    cy.get('button[type="submit"]').click();

    cy.get('.error-message')
      .should('be.visible')
      .and('have.text', 'Invalid credentials');
  });
});
```

#### 自定义命令（可复用的操作）

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('include', '/dashboard');
});

// Usage in tests
it('should display dashboard for logged-in user', () => {
  cy.login('user@example.com', 'SecurePass123!');
  cy.get('h1').should('have.text', 'Dashboard');
});
```

#### 使用 Intercept 进行 API 模拟

```javascript
it('should display mocked user data', () => {
  cy.intercept('GET', '/api/user', {
    statusCode: 200,
    body: {
      id: 1,
      name: 'Mock User',
      email: 'mock@example.com',
    },
  }).as('getUser');

  cy.visit('/profile');

  cy.wait('@getUser');
  cy.get('.user-name').should('have.text', 'Mock User');
});
```

### 3. React 测试库（组件测试）

**为什么选择 Testing Library？**
- 以用户为中心的查询方式（注重无障碍性）
- 鼓励采用最佳实践（测试应用程序的行为，而非实现细节）
- 支持 React、Vue、Svelte、Angular 等框架

#### 组件测试示例

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should render email and password inputs', () => {
    render(<LoginForm />);

    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
  });

  it('should call onSubmit with email and password', async () => {
    const handleSubmit = vi.fn();
    render(<LoginForm onSubmit={handleSubmit} />);

    // Type into inputs
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'user@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'SecurePass123!' },
    });

    // Submit form
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Verify callback
    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'SecurePass123!',
    });
  });

  it('should show validation error for invalid email', async () => {
    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'invalid-email' },
    });
    fireEvent.blur(screen.getByLabelText('Email'));

    expect(await screen.findByText('Invalid email format')).toBeInTheDocument();
  });
});
```

#### 以用户为中心的查询方式（推荐使用）

```typescript
// ✅ GOOD: Accessible queries (user-facing)
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText('Email');
screen.getByPlaceholderText('Enter your email');
screen.getByText('Welcome');

// ❌ BAD: Implementation-detail queries (fragile)
screen.getByClassName('btn-primary'); // Changes when CSS changes
screen.getByTestId('submit-button'); // Not user-facing
```

## 测试策略

### 1. 测试层次结构

**单元测试**（60%）：
- 单个组件的独立测试
- 测试速度快、成本低、可执行大量测试
- 可模拟外部依赖项

**集成测试**（30%）：
- 多个组件协同工作时的测试
- 检查 API 集成和数据流
- 测试速度中等、成本适中

**E2E 测试**（10%）：
- 完整的用户流程测试（从登录到结账）
- 测试速度最慢、成本最高
- 仅针对关键路径进行测试

### 2. 测试覆盖策略

**需要测试的内容**：
- ✅ 正常使用场景（核心用户流程）
- ✅ 错误状态（验证、API 错误）
- ✅ 边缘情况（空状态、极限值）
- ✅ 无障碍性（键盘导航、屏幕阅读器）
- ✅ 回归问题（每次修复 bug 需要重新测试相关功能）

**不需要测试的内容**：
- ❌ 第三方库（假设它们能正常工作）
- ❌ 实现细节（内部状态、CSS 类）
- ❌ 简单的代码（getter、setter）

### 3. 避免测试结果不稳定（Flaky Tests）

**导致测试结果不稳定的常见原因**：

1. **竞态条件（Race Conditions）**

❌ **错误做法**：
```typescript
await page.click('button');
const text = await page.textContent('.result'); // May fail!
```

✅ **正确做法**：
```typescript
await page.click('button');
await page.waitForSelector('.result'); // Wait for element
const text = await page.textContent('.result');
```

2. **数据非确定性（Non-Deterministic Data）**

❌ **错误做法**：
```typescript
expect(page.locator('.user')).toHaveCount(5); // Depends on database state
```

✅ **正确做法**：
```typescript
// Mock API to return deterministic data
await page.route('**/api/users', (route) =>
  route.fulfill({
    body: JSON.stringify([{ id: 1, name: 'User 1' }, { id: 2, name: 'User 2' }]),
  })
);

expect(page.locator('.user')).toHaveCount(2); // Predictable
```

3. **时间问题（Timing Issues）**

❌ **错误做法**：
```typescript
await page.waitForTimeout(3000); // Arbitrary wait
```

✅ **正确做法**：
```typescript
await page.waitForSelector('.loaded'); // Wait for specific condition
await page.waitForLoadState('networkidle'); // Wait for network idle
```

4. **测试之间的依赖关系（Test Interdependence）**

❌ **错误做法**：
```typescript
test('create user', async () => {
  // Creates user in DB
});

test('login user', async () => {
  // Depends on previous test creating user
});
```

✅ **正确做法**：
```typescript
test.beforeEach(async () => {
  // Each test creates its own user
  await createTestUser();
});

test.afterEach(async () => {
  await cleanupTestUsers();
});
```

## 无障碍性测试

### 1. 自动化无障碍性测试（axe-core）

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should have no accessibility violations', async ({ page }) => {
  await page.goto('https://example.com');

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### 2. 键盘导航测试

```typescript
test('should navigate form with keyboard', async ({ page }) => {
  await page.goto('/form');

  // Tab through form fields
  await page.keyboard.press('Tab');
  await expect(page.locator('input[name="email"]')).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(page.locator('input[name="password"]')).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(page.locator('button[type="submit"]')).toBeFocused();

  // Submit with Enter
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL('**/dashboard');
});
```

### 3. 屏幕阅读器测试（使用 aria-label、roles）

```typescript
test('should have proper ARIA labels', async ({ page }) => {
  await page.goto('/login');

  // Verify accessible names
  await expect(page.getByRole('textbox', { name: 'Email' })).toBeVisible();
  await expect(page.getByRole('textbox', { name: 'Password' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();

  // Verify error announcements (aria-live)
  await page.fill('input[name="email"]', 'invalid-email');
  await page.click('button[type="submit"]');

  const errorRegion = page.locator('[role="alert"]');
  await expect(errorRegion).toHaveText('Invalid email format');
});
```

## 持续集成/持续部署（CI/CD）集成

### 1. 使用 GitHub Actions 进行测试

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:

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

      - name: Run Playwright tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

### 2. 并行执行测试

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 2 : undefined, // Parallel in CI
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0, // Retry flaky tests in CI
  reporter: process.env.CI ? 'github' : 'html',
});
```

### 3. 分割大型测试套件（Sharding Large Test Suites）

```bash
# Split tests across 4 machines
npx playwright test --shard=1/4
npx playwright test --shard=2/4
npx playwright test --shard=3/4
npx playwright test --shard=4/4
```

## 最佳实践

### 1. 使用数据属性来创建稳定的选择器

```html
<!-- ✅ GOOD: Stable selector -->
<button data-testid="submit-button">Submit</button>

<!-- ❌ BAD: Fragile selectors -->
<button class="btn btn-primary">Submit</button> <!-- CSS changes break tests -->
```

```typescript
// Test
await page.click('[data-testid="submit-button"]');
```

### 2. 测试应用程序的行为，而非实现细节

❌ **错误做法**：
```typescript
// Testing internal state
expect(component.state.isLoading).toBe(true);
```

✅ **正确做法**：
```typescript
// Testing visible UI
expect(screen.getByText('Loading...')).toBeInTheDocument();
```

### 3. 保持测试的独立性

```typescript
// ✅ GOOD: Each test is independent
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await login(page, 'user@example.com', 'password');
});

test('test 1', async ({ page }) => {
  // Fresh state
});

test('test 2', async ({ page }) => {
  // Fresh state
});
```

### 4. 使用有意义的断言（Assertion）

❌ **错误做法**：
```typescript
expect(true).toBe(true); // Useless assertion
```

✅ **正确做法**：
```typescript
await expect(page.locator('.success-message')).toHaveText(
  'Order placed successfully'
);
```

### 5. 避免使用硬编码的等待时间

❌ **错误做法**：
```typescript
await page.waitForTimeout(5000); // Slow, brittle
```

✅ **正确做法**：
```typescript
await page.waitForSelector('.results'); // Wait for specific element
await expect(page.locator('.results')).toBeVisible(); // Built-in wait
```

## 调试测试

### 1. 使用 Headed Mode 查看浏览器行为

```bash
npx playwright test --headed
npx playwright test --headed --debug # Pause on each step
```

### 2. 在测试失败时生成截图

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    await page.screenshot({ path: `failure-${testInfo.title}.png` });
  }
});
```

### 3. 使用 Trace Viewer 进行时间旅行调试

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry', // Record trace on retry
  },
});
```

```bash
# View trace
npx playwright show-trace trace.zip
```

### 4. 查看控制台日志

```typescript
page.on('console', (msg) => console.log('Browser log:', msg.text()));
page.on('pageerror', (error) => console.error('Page error:', error));
```

## 常见测试模式

### 1. 表单测试

```typescript
test('should validate form fields', async ({ page }) => {
  await page.goto('/form');

  // Empty submission (validation)
  await page.click('button[type="submit"]');
  await expect(page.locator('.email-error')).toHaveText('Email is required');

  // Invalid email
  await page.fill('input[name="email"]', 'invalid');
  await page.click('button[type="submit"]');
  await expect(page.locator('.email-error')).toHaveText('Invalid email format');

  // Valid submission
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('**/success');
});
```

### 2. 弹出框（Modal）测试

```typescript
test('should open and close modal', async ({ page }) => {
  await page.goto('/');

  // Open modal
  await page.click('[data-testid="open-modal"]');
  await expect(page.locator('.modal')).toBeVisible();

  // Close with X button
  await page.click('.modal .close-button');
  await expect(page.locator('.modal')).not.toBeVisible();

  // Open again, close with Escape
  await page.click('[data-testid="open-modal"]');
  await page.keyboard.press('Escape');
  await expect(page.locator('.modal')).not.toBeVisible();
});
```

### 3. 拖放（Drag and Drop）功能测试

```typescript
test('should drag and drop items', async ({ page }) => {
  await page.goto('/kanban');

  const todoItem = page.locator('[data-testid="item-1"]');
  const doneColumn = page.locator('[data-testid="column-done"]');

  // Drag item from TODO to DONE
  await todoItem.dragTo(doneColumn);

  // Verify item moved
  await expect(doneColumn.locator('[data-testid="item-1"]')).toBeVisible();
});
```

## 参考资源

- [Playwright 文档](https://playwright.dev/)
- [Cypress 文档](https://docs.cypress.io/)
- [Testing Library 文档](https://testing-library.com/)
- [Web 内容无障碍性指南（WCAG）](https://www.w3.org/WAI/WCAG21/quickref/)

## 常见问题解答

- **如何使用 Playwright 编写 E2E 测试？**
- **Cypress 的测试示例有哪些？**
- **React 测试库的最佳实践是什么？**
- **UI 测试中的页面对象模型（Page Object Model）是什么？**
- **如何使用 axe-core 进行无障碍性测试？**
- **如何解决测试结果不稳定的问题？**
- **如何将 UI 测试集成到持续集成/持续部署流程中？**
- **如何调试 Playwright 测试？**
- **有哪些有效的测试自动化策略？**