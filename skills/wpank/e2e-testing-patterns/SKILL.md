---
name: e2e-testing-patterns
model: standard
category: testing
description: 使用 Playwright 和 Cypress 构建可靠、高效的端到端（E2E）测试套件。这些测试套件能够覆盖用户的关键使用流程，消除那些容易出错的测试（即“不稳定”的测试），并实现与持续集成/持续部署（CI/CD）流程的完美集成。
version: 1.0
keywords: [e2e, end-to-end, playwright, cypress, browser testing, integration tests, test automation, flaky tests, visual regression]
---

# 端到端（E2E）测试模式

> 测试用户的行为，而不是代码的运作方式。端到端测试能够验证整个系统的稳定性——它们是你放心发布产品的关键。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install e2e-testing-patterns
```

---

## 本技能的作用

提供构建端到端测试套件的模式，这些模式可以：
- 在用户发现问题之前捕获代码回归错误
- 以足够的速度运行，以适应持续集成（CI）和持续部署（CD）流程
- 保持稳定性（避免测试结果不稳定）
- 充分覆盖关键的用户操作流程，同时避免过度测试

## 适用场景

- **为Web应用程序实现端到端测试自动化**
- **调试那些间歇性失败的测试**
- **设置包含浏览器测试的CI/CD测试管道**
- **测试关键的用户工作流程（如登录、结账、注册）**
- **决定使用端到端测试还是单元测试/集成测试**

---

## 测试金字塔——了解各层的用途

```
        /\
       /E2E\         ← FEW: Critical paths only (this skill)
      /─────\
     /Integr\        ← MORE: Component interactions, API contracts
    /────────\
   /Unit Tests\      ← MANY: Fast, isolated, cover edge cases
  /────────────\
```

### 端到端测试的用途

| 端到端测试 ✓ | 非端到端测试 ✗ |
|-------------|-----------------|
| 关键的用户操作流程（登录 → 仪表板 → 执行操作 → 登出） | 单元级逻辑（使用单元测试） |
| 多步骤流程（如结账、入职向导） | API接口（使用集成测试） |
| 跨浏览器兼容性 | 边缘情况（如果测试速度过慢，使用单元测试） |
| 真实的API集成 | 内部实现细节 |

**经验法则：** 如果某个功能的故障会对业务造成严重影响，就对其进行端到端测试；如果只是带来不便，可以使用单元测试或集成测试更快地解决问题。

---

## 核心原则

| 原则 | 原因 | 实施方法 |
|-----------|-----|-----|
| **测试行为，而非实现细节** | 可以在重构后仍然有效 | 验证用户可见的结果，而不是DOM结构 |
| **独立的测试** | 可并行执行、便于调试 | 每个测试都会生成自己的数据，并在完成后清理环境 |
| **确定性的等待时间** | 避免测试结果不稳定 | 等待特定条件满足，而不是使用固定的超时时间 |
| **稳定的选择器** | 可以在UI变更后仍然使用 | 使用`dataTestId`、角色名称、标签等选择器，避免依赖CSS类 |
| **快速反馈** | 开发者可以立即运行测试 | 使用模拟外部服务、并行执行测试 |

---

## Playwright测试模式

### 配置

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["html"], ["junit", { outputFile: "results.xml" }]],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "mobile", use: { ...devices["iPhone 13"] } },
  ],
});
```

### 模式：页面对象模型（Page Object Model）

将页面逻辑封装起来。测试代码应该像用户故事一样易于阅读。

```typescript
// pages/LoginPage.ts
import { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel("Email");
    this.passwordInput = page.getByLabel("Password");
    this.loginButton = page.getByRole("button", { name: "Login" });
    this.errorMessage = page.getByRole("alert");
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

// tests/login.spec.ts
import { test, expect } from "@playwright/test";
import { LoginPage } from "../pages/LoginPage";

test("successful login redirects to dashboard", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("user@example.com", "password123");

  await expect(page).toHaveURL("/dashboard");
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```

### 模式：测试数据管理工具（Fixtures）

自动创建和清理测试数据。

```typescript
// fixtures/test-data.ts
import { test as base } from "@playwright/test";

export const test = base.extend<{ testUser: TestUser }>({
  testUser: async ({}, use) => {
    // Setup: Create user
    const user = await createTestUser({
      email: `test-${Date.now()}@example.com`,
      password: "Test123!@#",
    });

    await use(user);

    // Teardown: Clean up
    await deleteTestUser(user.id);
  },
});

// Usage — testUser is created before, deleted after
test("user can update profile", async ({ page, testUser }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill(testUser.email);
  // ...
});
```

### 模式：智能等待（Smart Waiting）

永远不要使用固定的超时时间。等待特定的条件满足。

```typescript
// ❌ FLAKY: Fixed timeout
await page.waitForTimeout(3000);

// ✅ STABLE: Wait for conditions
await page.waitForLoadState("networkidle");
await page.waitForURL("/dashboard");

// ✅ BEST: Auto-waiting assertions
await expect(page.getByText("Welcome")).toBeVisible();
await expect(page.getByRole("button", { name: "Submit" })).toBeEnabled();

// Wait for API response
const responsePromise = page.waitForResponse(
  (r) => r.url().includes("/api/users") && r.status() === 200
);
await page.getByRole("button", { name: "Load" }).click();
await responsePromise;
```

### 模式：网络模拟（Network Mocking）

将测试与真实的外部服务隔离开来。

```typescript
test("shows error when API fails", async ({ page }) => {
  // Mock the API response
  await page.route("**/api/users", (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: "Server Error" }),
    });
  });

  await page.goto("/users");
  await expect(page.getByText("Failed to load users")).toBeVisible();
});

test("handles slow network gracefully", async ({ page }) => {
  await page.route("**/api/data", async (route) => {
    await new Promise((r) => setTimeout(r, 3000)); // Simulate delay
    await route.continue();
  });

  await page.goto("/dashboard");
  await expect(page.getByText("Loading...")).toBeVisible();
});
```

---

## Cypress测试模式

### 自定义命令

```typescript
// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      dataCy(value: string): Chainable<JQuery<HTMLElement>>;
    }
  }
}

Cypress.Commands.add("login", (email, password) => {
  cy.visit("/login");
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="login-button"]').click();
  cy.url().should("include", "/dashboard");
});

Cypress.Commands.add("dataCy", (value) => {
  return cy.get(`[data-cy="${value}"]`);
});

// Usage
cy.login("user@example.com", "password");
cy.dataCy("submit-button").click();
```

### 网络拦截（Network Interceptions）

```typescript
// Mock API
cy.intercept("GET", "/api/users", {
  statusCode: 200,
  body: [{ id: 1, name: "John" }],
}).as("getUsers");

cy.visit("/users");
cy.wait("@getUsers");
cy.get('[data-testid="user-list"]').children().should("have.length", 1);
```

---

## 选择器策略

| 优先级 | 选择器类型 | 例子 | 原因 |
|----------|--------------|---------|-----|
| 1 | **角色 + 名称** | `getByRole("button", { name: "Submit" })` | 易于使用，用户友好 |
| 2 | **标签** | `getByLabel("Email address")` | 易于理解，语义明确 |
| 3 | **dataTestId** | `getByTestId("checkout-form")` | 稳定可靠，专为测试设计 |
| 4 | **文本内容** | `getByText("Welcome back")` | 用户可感知的内容 |
| ❌ | CSS类 | `.btn-primary` | 受样式变化影响 |
| ❌ | DOM结构 | `div > form > input:nth-child(2)` | 受页面结构变化影响 |

```typescript
// ❌ BAD: Brittle selectors
cy.get(".btn.btn-primary.submit-button").click();
cy.get("div > form > div:nth-child(2) > input").type("text");

// ✅ GOOD: Stable selectors
page.getByRole("button", { name: "Submit" }).click();
page.getByLabel("Email address").fill("user@example.com");
page.getByTestId("email-input").fill("user@example.com");
```

## 可视化回归测试（Visual Regression Testing）

---

## 可访问性测试（Accessibility Testing）

---

## 调试失败的测试

```bash
# Run in headed mode (see the browser)
npx playwright test --headed

# Debug mode (step through)
npx playwright test --debug

# Show trace viewer for failed tests
npx playwright show-report
```

---

## 避免测试结果不稳定的方法

当测试结果间歇性地失败时，请检查以下问题：

| 问题 | 解决方案 |
|-------|-----|
| 固定的`waitForTimeout()`调用 | 更改为`waitForSelector()`或使用断言 |
| 页面加载时的竞争条件 | 等待`networkidle`事件或特定元素加载完成 |
| 测试数据污染 | 确保测试生成并清理自己的数据 |
| 动画执行时间问题 | 等待动画完成或禁用动画 |
| 视口设置不一致 | 在配置中指定明确的视口大小 |
| 测试顺序问题 | 测试应保持独立性 |
| 第三方服务的问题 | 模拟外部API的行为 |

---

## 持续集成与持续部署（CI/CD）集成

```yaml
# GitHub Actions example
name: E2E Tests
on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run build
      - run: npm run start & npx wait-on http://localhost:3000
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 绝对不要做的事情

1. **绝对不要使用固定的`waitForTimeout()`或`cy.wait(ms)`**——这些会导致测试结果不稳定，并降低测试效率 |
2. **绝对不要依赖CSS类或DOM结构作为选择器**——使用角色名称、标签或`dataTestId` |
3. **绝对不要在测试之间共享状态**——每个测试都应保持独立 |
4. **绝对不要测试实现细节**——测试用户看到的内容和操作，而不是内部结构 |
5. **绝对不要省略测试后的清理步骤**——即使测试失败，也要删除生成的测试数据 |
6. **不要对所有功能都使用端到端测试**——仅在关键路径上使用端到端测试；对于边缘情况，使用更快速的测试方法 |
7. **不要忽略不稳定的测试**——立即修复这些问题，或者直接删除这些测试；不稳定的测试比没有测试更糟糕 |
8. **不要在选择器中硬编码测试数据**——对于可能变化的内容，应使用动态的等待策略 |

---

## 快速参考

### Playwright命令

```typescript
// Navigation
await page.goto("/path");
await page.goBack();
await page.reload();

// Interactions
await page.click("selector");
await page.fill("selector", "text");
await page.type("selector", "text");  // Types character by character
await page.selectOption("select", "value");
await page.check("checkbox");

// Assertions
await expect(page).toHaveURL("/expected");
await expect(locator).toBeVisible();
await expect(locator).toHaveText("expected");
await expect(locator).toBeEnabled();
await expect(locator).toHaveCount(3);
```

### Cypress命令

```typescript
// Navigation
cy.visit("/path");
cy.go("back");
cy.reload();

// Interactions
cy.get("selector").click();
cy.get("selector").type("text");
cy.get("selector").clear().type("text");
cy.get("select").select("value");
cy.get("checkbox").check();

// Assertions
cy.url().should("include", "/expected");
cy.get("selector").should("be.visible");
cy.get("selector").should("have.text", "expected");
cy.get("selector").should("have.length", 3);
```