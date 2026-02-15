---
name: playwright-npx
description: 使用 Node.js 脚本和 Playwright 实现快速浏览器自动化（通过 `node script.mjs` 运行）。适用于网页抓取、截图、表单自动化以及任何需要程序控制的浏览器操作。如果只是简单的页面获取（无需执行 JavaScript），请先使用 `web_fetch`；如果需要交互式的 CLI 浏览（无需编写代码），则可以使用 `browser tool` 或 `playwright-cli`。当您需要完全控制、自定义逻辑或可重用的脚本时，这项技能非常实用。
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["node","npx"]}}, "created_by": "Kuba + Mahone", "created_date": "2026-02-04", "is_custom": true}
---

# Playwright 浏览器自动化

> 🤝 由 Kuba 和 Mahone 共同开发 · 2026 年 2 月

使用 Playwright 进行基于代码的浏览器自动化。

## 适用场景

| 工具 | 适用情况 |
|------|----------|
| **web_fetch** | 简单页面，无需 JavaScript |
| **This skill** | 需要大量 JavaScript 的网站、复杂的交互操作、完全控制浏览器行为 |
| **stealth-browser** | 避免被机器人检测或解决 Cloudflare 相关问题 |
| **browser tool** | 用于视觉探索，作为最后的手段 |
| **playwright-cli** | 提供无需编写代码的交互式命令行接口 |

## 设置

```bash
# One-time per project
npm init -y
npm install playwright
npx playwright install chromium
```

**package.json 示例:**
```json
{
  "name": "my-automation",
  "type": "module",
  "dependencies": {
    "playwright": "^1.40.0"
  }
}
```

## 最小示例

```javascript
// tmp/example.mjs
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

await page.goto('https://example.com');
console.log('Title:', await page.title());

await browser.close();
```

```bash
node tmp/example.mjs
```

## 常用模式

### 截图
```javascript
import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await browser.newPage();
await page.setViewportSize({ width: 1280, height: 800 });
await page.goto('https://example.com');
await page.screenshot({ path: 'tmp/screenshot.png', fullPage: true });
await browser.close();
```

### 数据抓取
```javascript
import { chromium } from 'playwright';
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://news.ycombinator.com');
const stories = await page.$$eval('.titleline > a', links => 
  links.slice(0, 5).map(a => ({ title: a.innerText, url: a.href }))
);
console.log(JSON.stringify(stories, null, 2));
await browser.close();
```

### 表单交互
```javascript
await page.goto('https://example.com/login');
await page.fill('input[name="email"]', 'user@example.com');
await page.fill('input[name="password"]', 'password');
await page.click('button[type="submit"]');
```

### 等待动态内容加载
```javascript
// Wait for network idle (SPA)
await page.goto(url, { waitUntil: 'networkidle' });

// Wait for specific element
await page.waitForSelector('.results', { timeout: 10000 });

// Wait for condition
await page.waitForFunction(() => 
  document.querySelectorAll('.item').length > 0
);
```

### 持久化会话
```javascript
import fs from 'fs';
const SESSION_FILE = 'tmp/session.json';

let context;
if (fs.existsSync(SESSION_FILE)) {
  context = await browser.newContext({ storageState: SESSION_FILE });
} else {
  context = await browser.newContext();
}
const page = await context.newPage();
// ... login ...
await context.storageState({ path: SESSION_FILE });
```

## 无头浏览器（Headless）与有头浏览器（Headed）的区别

```javascript
// Headless (default, fastest)
await chromium.launch({ headless: true });

// Headed (see the browser)
await chromium.launch({ headless: false });

// Slow motion (debugging)
await chromium.launch({ headless: false, slowMo: 100 });
```

## 选择器快速参考

```javascript
// CSS
await page.click('button.submit');
await page.fill('input#email', 'text');

// Text content
await page.click('text=Submit');
await page.click('text=/log\s*in/i');  // regex

// XPath
await page.click('xpath=//button[@type="submit"]');

// ARIA role
await page.click('role=button[name="Submit"]');

// Test ID (most stable)
await page.click('[data-testid="submit-btn"]');

// Chain selectors
await page.click('nav >> text=Settings');
```

**请参阅 [references/selectors.md](references/selectors.md) 以获取完整的选择器指南。**

## 错误处理

```javascript
try {
  await page.goto('https://example.com', { timeout: 30000 });
  const hasResults = await page.locator('.results').isVisible().catch(() => false);
  if (!hasResults) {
    console.log('No results');
    process.exit(0);
  }
} catch (error) {
  console.error('Error:', error.message);
  await page.screenshot({ path: 'tmp/error.png' });
  process.exit(1);
} finally {
  await browser.close();
}
```

## 示例与模板

### 实用示例
- [examples/screenshot.mjs] - 全页面截图
- [examples/scrape.mjs] - 数据提取
- [examples/form-interaction.mjs] - 表单自动化
- [examples/login-session.mjs] - 持久化会话管理

### 可重用的模板
- [scripts/minimal-template.mjs] - 简单的脚本模板
- [scripts/screenshot-template.mjs] - 可配置的截图工具
- [scripts/scrape-template.mjs] - 数据抓取模板

**复制模板:**
```bash
cp scripts/minimal-template.mjs tmp/my-task.mjs
# Edit tmp/my-task.mjs, then run:
node tmp/my-task.mjs
```

## 工具命令

```bash
# Record interactions to generate code
npx playwright codegen https://example.com

# Debug selectors
npx playwright codegen --target javascript https://example.com

# Show trace
npx playwright show-trace tmp/trace.zip
```

## 深入参考

- **[references/selectors.md]** - 完整的选择器指南（CSS、文本、XPath、ARIA、test-id）
- **[references/debugging.md]** - 调试技巧（无头浏览器、慢动作播放、截图）
- **[references/troubleshooting.md]** - 常见问题及解决方法

## 提示

- 将脚本文件放在 `tmp/` 目录中——该目录会被 Git 忽略
- 使用 `.mjs` 扩展名来标识 ES 模块（无需指定 `type: module`）
- 大量使用 `console.log()` 进行调试
- 当出现问题时，使用 `page.screenshot()` 功能获取截图
- 对于复杂的网站，添加 `await page.waitForLoadState('networkidle')` 来确保页面加载完成
- 详细调试指南请参阅 [references/debugging.md]
- 常见问题解决方法请参阅 [references/troubleshooting.md]