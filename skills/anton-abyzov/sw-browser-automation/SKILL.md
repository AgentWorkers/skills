---
name: browser-automation
description: 非测试场景下的浏览器自动化功能包括：网络爬虫、表单填写、截图生成以及工作流程自动化。如需使用 Playwright 进行测试，请选择 `e2e-playwright` 技能。该功能支持网络爬虫、表单自动化、截图生成、无头浏览器（headless browser）操作，同时兼容 Puppeteer 和 Selenium 等自动化工具，能够实现数据提取等任务。
---

# 浏览器自动化技能

精通使用 Playwright、Puppeteer 和 Selenium 进行浏览器自动化。专注于 UI 测试、网页抓取、表单自动化以及自动化工作流程。

## 专业领域

### 1. Playwright 自动化
- **浏览器控制**：启动、导航、与页面交互
- **元素选择**：CSS 选择器、XPath、基于文本的选择器、dataTestId
- **操作**：点击、输入、选择、悬停、拖放
- **等待策略**：waitForSelector、waitForNavigation、waitForTimeout
- **网络拦截**：模拟 API、阻止资源加载、修改请求
- **截图与视频**：全页面截图、特定元素截图、视频录制

### 2. 测试框架
- **端到端测试**：Playwright Test、类似 Cypress 的工作流程
- **视觉回归测试**：截图对比、像素差异分析
- **无障碍测试**：ARIA 标准验证、键盘导航
- **性能测试**：页面加载时间、Core Web Vitals
- **移动设备测试**：模拟设备、触摸操作

### 3. 网页抓取
- **数据提取**：解析 HTML、提取结构化数据
- **分页处理**：遍历多页结果
- **动态内容**：处理懒加载、无限滚动
- **身份验证**：登录流程、会话管理
- **速率限制**：限制请求频率、遵守 robots.txt 文件

### 4. 表单自动化
- **输入字段**：文本输入、电子邮件输入、密码输入、数字输入
- **选择框**：下拉菜单、单选按钮、复选框
- **文件上传**：单文件上传、多文件上传
- **日期选择器**：自定义日期输入框
- **多步骤表单**：向导式表单流程

## 代码示例

### 基本页面导航
```typescript
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('https://example.com', { waitUntil: 'networkidle' });
await page.screenshot({ path: 'screenshot.png', fullPage: true });
await browser.close();
```

### 带有验证的表单自动化
```typescript
// Fill and submit form
await page.fill('input[name="email"]', 'test@example.com');
await page.fill('input[name="password"]', 'SecurePass123!');
await page.click('button[type="submit"]');

// Wait for success message
const success = await page.waitForSelector('.success-message', { timeout: 5000 });
const message = await success.textContent();
console.log('Success:', message);
```

### 从多个页面提取数据
```typescript
const products = [];
let page = 1;

while (page <= 10) {
  await browser.goto(`https://example.com/products?page=${page}`);

  const items = await browser.$$eval('.product-item', (elements) =>
    elements.map((el) => ({
      title: el.querySelector('.title')?.textContent,
      price: el.querySelector('.price')?.textContent,
      image: el.querySelector('img')?.src,
    }))
  );

  products.push(...items);
  page++;
}
```

### 网络拦截
```typescript
await page.route('**/api/analytics', (route) => route.abort());
await page.route('**/api/user', (route) =>
  route.fulfill({
    status: 200,
    body: JSON.stringify({ id: 1, name: 'Test User' }),
  })
);
```

### 视觉回归测试
```typescript
import { expect } from '@playwright/test';

// Capture baseline
await page.screenshot({ path: 'baseline.png' });

// After changes, compare
const screenshot = await page.screenshot();
expect(screenshot).toMatchSnapshot('homepage.png');
```

## 选择器策略

### 1. CSS 选择器（推荐使用）
```typescript
// ID selector (most reliable)
await page.click('#submit-button');

// Data attribute (best practice)
await page.click('[data-testid="login-button"]');

// Class selector
await page.click('.btn-primary');

// Combined selector
await page.click('button.submit[type="submit"]');
```

### 2. 当 CSS 无法满足需求时使用 XPath
```typescript
// Text-based selection
await page.click('//button[contains(text(), "Submit")]');

// Complex hierarchy
await page.click('//div[@class="form"]//input[@name="email"]');
```

### 3. Playwright 特有的选择器方法
```typescript
// Text-based
await page.getByText('Submit').click();

// Role-based (accessibility)
await page.getByRole('button', { name: 'Submit' }).click();

// Label-based
await page.getByLabel('Email address').fill('test@example.com');

// Placeholder-based
await page.getByPlaceholder('Enter your email').fill('test@example.com');
```

## 最佳实践

### 1. 使用稳定的选择器
❌ **错误示例**：`.css-4j6h2k-button`（自动生成的类名）
✅ **正确示例**：`[dataTestId="submit-button"]`

### 2. 明确添加等待逻辑
❌ **错误示例**：`await page.waitForTimeout(3000);`
✅ **正确示例**：`await page.waitForSelector('.results', { state: 'visible' });`

### 3. 优雅地处理错误
```typescript
try {
  await page.click('button', { timeout: 5000 });
} catch (error) {
  await page.screenshot({ path: 'error.png' });
  console.error('Click failed:', error.message);
  throw error;
}
```

### 4. 清理资源
```typescript
try {
  // automation code
} finally {
  await browser.close();
}
```

### 5. 使用页面对象模型（Page Object Model, POM）
```typescript
class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async isLoggedIn() {
    return this.page.locator('[data-testid="dashboard"]').isVisible();
  }
}
```

## 常见问题

### 1. 竞态条件
```typescript
// ❌ Race condition
await page.click('button');
const text = await page.textContent('.result'); // May fail!

// ✅ Wait for element
await page.click('button');
await page.waitForSelector('.result');
const text = await page.textContent('.result');
```

### 2. 元素引用失效
```typescript
// ❌ Element may become stale
const element = await page.$('button');
await page.reload();
await element.click(); // Error: element detached from DOM

// ✅ Re-query after page changes
await page.reload();
await page.click('button');
```

### 3. 动态内容的定时问题
```typescript
// ❌ Assumes immediate load
await page.goto('https://example.com');
await page.click('.dynamic-content'); // May fail!

// ✅ Wait for dynamic content
await page.goto('https://example.com');
await page.waitForLoadState('networkidle');
await page.click('.dynamic-content');
```

## 调试工具

### 1. 全屏模式
```typescript
const browser = await chromium.launch({ headless: false, slowMo: 100 });
```

### 失败时生成截图
```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    await page.screenshot({ path: `failure-${testInfo.title}.png` });
  }
});
```

### 跟踪记录
```typescript
await context.tracing.start({ screenshots: true, snapshots: true });
await page.goto('https://example.com');
// ... automation steps
await context.tracing.stop({ path: 'trace.zip' });
```

### 控制台日志
```typescript
page.on('console', (msg) => console.log('Browser log:', msg.text()));
```

## 性能优化

### 1. 阻止不必要的资源加载
```typescript
await page.route('**/*.{png,jpg,jpeg,gif,svg,css}', (route) => route.abort());
```

### 2. 重用浏览器上下文
```typescript
const context = await browser.newContext();
const page1 = await context.newPage();
const page2 = await context.newPage();
// Share cookies, storage, etc.
```

### 3. 并行执行
```typescript
await Promise.all([
  page1.goto('https://example.com/page1'),
  page2.goto('https://example.com/page2'),
  page3.goto('https://example.com/page3'),
]);
```

## 相关术语/问题

- **如何使用 Playwright 进行浏览器测试？**
- **如何使用 Playwright/Puppeteer 进行网页抓取？**
- **如何实现截图自动化和视觉回归测试？**
- **如何自动化表单填写？**
- **如何处理网页自动化中的动态内容？**
- **UI 测试的最佳实践是什么？**
- **如何调试 Playwright 测试？**

## 相关技能

- **端到端测试**：`e2e-playwright` 技能
- **前端开发**：`frontend` 技能（用于理解 DOM 结构）
- **API 测试**：`api-testing` 技能（用于模拟网络请求）

## 工具与框架

- **Playwright**：现代浏览器自动化工具（推荐使用）
- **Puppeteer**：针对 Chrome/Chromium 的自动化工具
- **Selenium**：传统的跨浏览器自动化工具
- **Playwright Test**：完整的测试框架
- **Cypress**：另一种端到端测试框架