---
name: init
description: 在项目中设置 Playwright。当用户提到“设置 Playwright”、“添加端到端测试”、“配置 Playwright”、“测试环境设置”、“初始化 Playwright”或“添加测试基础设施”时，请使用此步骤。
  Set up Playwright in a project. Use when user says "set up playwright",
  "add e2e tests", "configure playwright", "testing setup", "init playwright",
  or "add test infrastructure".
---
# 初始化 Playwright 项目

设置一个适用于生产环境的 Playwright 测试环境。检测所使用的框架，生成配置文件、文件夹结构、示例测试用例以及持续集成（CI）工作流程。

## 步骤

### 1. 分析项目

使用 `Explore` 子代理扫描项目：

- 查看 `package.json` 以确定使用的框架（React、Next.js、Vue、Angular、Svelte）
- 查看是否存在 `tsconfig.json` 文件（如果有，则使用 TypeScript；否则使用 JavaScript）
- 检查是否已安装 Playwright（在依赖项中是否有 `@playwright/test`）
- 查看是否存在测试文件夹（如 `tests/`、`e2e/`、`__tests__`）
- 查看是否存在持续集成配置文件（如 `.github/workflows/`、`.gitlab-ci.yml`）

### 2. 安装 Playwright

如果尚未安装 Playwright，请执行以下操作：

```bash
npm init playwright@latest -- --quiet
```

或者，如果用户希望手动配置，请执行以下操作：

```bash
npm install -D @playwright/test
npx playwright install --with-deps chromium
```

### 3. 生成 `playwright.config.ts` 文件

根据检测到的框架进行相应的配置：

**Next.js:**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

**React (Vite):**
- 将 `baseURL` 更改为 `http://localhost:5173`
- 将 `webServer.command` 更改为 `npm run dev`

**Vue/Nuxt:**
- 将 `baseURL` 更改为 `http://localhost:3000`
- 将 `webServer.command` 更改为 `npm run dev`

**Angular:**
- 将 `baseURL` 更改为 `http://localhost:4200`
- 将 `webServer.command` 更改为 `npm run start`

**未检测到框架:**
- 忽略 `webServer` 部分
- 根据用户输入设置 `baseURL`，或保留为空占位符

### 4. 创建文件夹结构

```
e2e/
├── fixtures/
│   └── index.ts          # Custom fixtures
├── pages/
│   └── .gitkeep          # Page object models
├── test-data/
│   └── .gitkeep          # Test data files
└── example.spec.ts       # First example test
```

### 5. 生成示例测试用例

```typescript
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/.+/);
  });

  test('should have visible navigation', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('navigation')).toBeVisible();
  });
});
```

### 6. 生成持续集成工作流程

如果存在 `.github/workflows/` 文件，请创建 `playwright.yml` 文件：

```yaml
name: Playwright Tests

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run Playwright tests
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

如果存在 `.gitlab-ci.yml` 文件，请在其中添加 Playwright 相关的步骤。

### 7. 更新 `.gitignore` 文件

如果文件中尚未包含相关内容，请添加以下内容：

```
/test-results/
/playwright-report/
/blob-report/
/playwright/.cache/
```

### 8. 添加 npm 脚本

将以下脚本添加到 `package.json` 文件中：

```json
{
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui",
  "test:e2e:debug": "playwright test --debug"
}
```

### 9. 验证设置

运行示例测试用例：

```bash
npx playwright test
```

如果测试失败，请诊断问题并修复后再继续下一步。

## 输出结果

确认已创建的内容包括：
- 配置文件的路径和关键设置
- 测试文件夹及示例测试用例
- 持续集成工作流程（如适用）
- 已添加的 npm 脚本
- 运行命令：`npx playwright test` 或 `npm run test:e2e`