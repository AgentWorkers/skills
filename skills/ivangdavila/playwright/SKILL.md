---
name: Playwright (Automation + MCP + Scraper)
slug: playwright
version: 1.0.2
homepage: https://playwright.dev
description: 使用 Playwright 进行浏览器自动化和网络爬取：处理表单、截图以及数据提取。该工具可以独立使用，也可以通过 MCP（MCP 是一个平台或工具的缩写，具体含义需根据上下文确定）进行集成。测试功能也已包含在内。
changelog: Rewritten with MCP integration and scraping focus. Now covers standalone use and MCP server setup.
---
## 使用场景

当您需要执行以下操作时，请使用此技能：
- **抓取网站内容**（无论是静态页面还是由 JavaScript 动态渲染的页面）
- **自动填写表单**（包括登录、结账、数据输入等）
- **测试 Web 应用程序**（端到端测试、视觉回归测试）
- **截取网页截图或生成 PDF 文件**
- **从表格、列表或动态内容中提取数据**

## 决策矩阵

| 场景 | 方法 | 速度 |
|----------|--------|-------|
| 静态 HTML 页面 | `web_fetch` 工具 | ⚡ 最快 |
| 由 JavaScript 动态渲染的页面 | 直接使用 Playwright | 🚀 快速 |
| 通过 AI 代理进行自动化操作 | MCP 服务器 | 🤖 集成度高 |
| 端到端测试 | 使用 @playwright/test | ✅ 完整的测试框架 |

## 快速参考

| 任务 | 对应文档文件 |
|------|------|
| 端到端测试模式 | `testing.md` |
| 持续集成/持续部署（CI/CD）集成 | `ci-cd.md` |
| 错误调试 | `debugging.md` |
| 网页抓取模式 | `scraping.md` |
| 选择器使用策略 | `selectors.md` |

## 核心规则

1. **切勿使用 `waitForTimeout()`**——始终等待特定的条件（如元素出现、URL 变化或网络请求完成）。
2. **务必关闭浏览器**——调用 `browser.close()` 以防止内存泄漏。
3. **优先使用基于角色的选择器**——`getByRole()` 在处理 UI 变化时比基于 CSS 的选择器更可靠。
4. **处理动态内容**——在与元素交互之前，先使用 `waitFor()` 确保元素已加载完成。
5. **保存登录状态**——使用 `storageState` 来保存和重用登录会话信息。

## 快速入门 - 常见任务

### 抓取页面内容
```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
const text = await page.locator('body').textContent();
await browser.close();
```

### 填写表单并提交
```javascript
await page.goto('https://example.com/login');
await page.getByLabel('Email').fill('user@example.com');
await page.getByLabel('Password').fill('secret');
await page.getByRole('button', { name: 'Sign in' }).click();
await page.waitForURL('**/dashboard');
```

### 截取网页截图
```javascript
await page.goto('https://example.com');
await page.screenshot({ path: 'screenshot.png', fullPage: true });
```

### 提取表格数据
```javascript
const rows = await page.locator('table tr').all();
const data = [];
for (const row of rows) {
  const cells = await row.locator('td').allTextContents();
  data.push(cells);
}
```

## 选择器的优先级

| 优先级 | 方法 | 例子 |
|----------|--------|---------|
| 1 | `getByRole()` | `getByRole('button', { name: 'Submit' })` |
| 2 | `getByLabel()` | `getByLabel('Email')` |
| 3 | `getByPlaceholder()` | `getByPlaceholder('Search...')` |
| 4 | `getByTestId()` | `getByTestId('submit-btn')` |
| 5 | `locator()` | `locator('.class')` | 最后选择 |

## 常见问题及解决方法

| 问题 | 解决方案 |
|------|-----|
| 无法找到元素 | 在进行操作前添加 `await locator.waitFor()` |
| 点击操作不稳定 | 使用 `click({ force: true })` 或等待元素状态变为 `visible` |
| 持续集成（CI）过程中超时 | 增加超时时间，并确保视口大小与本地环境一致 |
| 测试之间登录状态丢失 | 使用 `storageState` 保存 Cookie |
| 单页应用程序（SPA）无法进入网络空闲状态 | 等待特定的 DOM 元素出现 |
| 遇到 403 禁止访问错误 | 检查网站是否限制无头浏览；尝试设置 `headless: false` |
| 页面加载后为空白 | 增加等待时间或使用 `waitUntil: 'networkidle'` |

## 会话管理

```javascript
// Save session after login
await page.context().storageState({ path: 'auth.json' });

// Reuse session in new context
const context = await browser.newContext({ storageState: 'auth.json' });
```

## MCP 集成

对于使用 Model Context Protocol 的 AI 代理：

```bash
npm install -g @playwright/mcp
npx @playwright/mcp --headless
```

### MCP 工具参考

| 工具 | 功能描述 |
|------|-------------|
| `browser_navigate` | 导航到指定 URL |
| `browser_click` | 根据选择器点击元素 |
| `browser_type` | 在输入框中输入文本 |
| `browser_select_option` | 从下拉菜单中选择选项 |
| `browser_get_text` | 获取文本内容 |
| `browser_evaluate` | 执行 JavaScript 代码 |
| `browser_snapshot` | 生成页面的可访问性截图 |
| `browser_close` | 关闭浏览器上下文 |
| `browser_choose_file` | 上传文件 |
| `browser_press` | 按下键盘键 |

### MCP 服务器配置选项

```bash
--headless              # Run without UI
--browser chromium      # chromium|firefox|webkit
--viewport-size 1920x1080
--timeout-action 10000  # Action timeout (ms)
--timeout-navigation 30000
--allowed-hosts example.com,api.example.com
--save-trace            # Save trace for debugging
--save-video 1280x720   # Record video
```

## 安装方法

```bash
npm init playwright@latest
# Or add to existing project
npm install -D @playwright/test
npx playwright install chromium
```

## 相关技能

如果您需要，可以使用以下工具进行安装：
- `puppeteer` – 另一种浏览器自动化工具（主要针对 Chrome 浏览器）
- `scrape` – 通用网页抓取方法和策略
- `web` – Web 开发基础知识和 HTTP 处理技巧

## 反馈建议

- 如果本文档对您有帮助，请给 `clawhub` 点星评分。
- 要保持信息更新，请使用 `clawhub sync` 命令。

（注：由于提供的文档内容较为简短，部分代码块（如 ````javascript
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
const text = await page.locator('body').textContent();
await browser.close();
```` 等）在实际使用中需要根据具体需求填写相应的代码内容。）