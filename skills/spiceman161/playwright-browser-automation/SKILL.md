---
name: playwright-browser-automation
description: **使用 Playwright API 直接实现浏览器自动化**  
可以浏览网页、与页面元素交互、提取数据、截图、生成 PDF 文件、录制视频，并自动化执行复杂的工作流程。这种方法比 MCP（Manual Code Programming）方式更为可靠。
metadata: {"openclaw":{"emoji":"🎭","os":["linux","darwin","win32"],"requires":{"bins":["node","npx"]},"install":[{"id":"npm-playwright","kind":"npm","package":"playwright","bins":["playwright"],"label":"Install Playwright"}]}}
---

# Playwright 浏览器自动化

Playwright 提供了直接的 API，用于实现可靠的浏览器自动化操作，无需处理复杂的中间件（MCP）相关问题。

## 安装

```bash
# Install Playwright
npm install -g playwright

# Install browsers (one-time, ~100MB each)
npx playwright install chromium
# Optional:
npx playwright install firefox
npx playwright install webkit

# For system dependencies on Ubuntu/Debian:
sudo npx playwright install-deps chromium
```

## 快速入门

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.goto('https://example.com');
  await page.screenshot({ path: 'screenshot.png' });
  
  await browser.close();
})();
```

## 最佳实践

### 1. 使用定位器（自动等待）

```javascript
// ✅ GOOD: Uses auto-waiting and retries
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByLabel('Username').fill('user');
await page.getByPlaceholder('Search').fill('query');

// ❌ BAD: May fail if element not ready
await page.click('#submit');
```

### 2. 优先选择用户可见的属性进行操作

```javascript
// ✅ GOOD: Resilient to DOM changes
await page.getByRole('heading', { name: 'Welcome' });
await page.getByText('Sign in');
await page.getByTestId('login-button');

// ❌ BAD: Brittle CSS selectors
await page.click('.btn-primary > div:nth-child(2)');
```

### 3. 处理动态内容

```javascript
// Wait for network idle
await page.goto('https://spa-app.com', { waitUntil: 'networkidle' });

// Wait for specific element
await page.waitForSelector('.results-loaded');
await page.waitForFunction(() => document.querySelectorAll('.item').length > 0);
```

### 4. 使用上下文进行隔离

```javascript
// Each context = isolated session (cookies, storage)
const context = await browser.newContext();
const page = await context.newPage();

// Multiple pages in one context
const page2 = await context.newPage();
```

### 5. 网络拦截

```javascript
// Mock API responses
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ users: [] })
  });
});

// Block resources
await page.route('**/*.{png,jpg,css}', route => route.abort());
```

## 常见应用场景

### 表单自动化

```javascript
// Fill form
await page.goto('https://example.com/login');
await page.getByLabel('Username').fill('myuser');
await page.getByLabel('Password').fill('mypass');
await page.getByRole('button', { name: 'Sign in' }).click();

// Wait for navigation/result
await page.waitForURL('/dashboard');
await expect(page.getByText('Welcome')).toBeVisible();
```

### 数据提取

```javascript
// Extract table data
const rows = await page.$$eval('table tr', rows =>
  rows.map(row => ({
    name: row.querySelector('td:nth-child(1)')?.textContent,
    price: row.querySelector('td:nth-child(2)')?.textContent
  }))
);

// Extract with JavaScript evaluation
const data = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.product')).map(p => ({
    title: p.querySelector('.title')?.textContent,
    price: p.querySelector('.price')?.textContent
  }));
});
```

### 截图与 PDF 生成

```javascript
// Full page screenshot
await page.screenshot({ path: 'full.png', fullPage: true });

// Element screenshot
await page.locator('.chart').screenshot({ path: 'chart.png' });

// PDF (Chromium only)
await page.pdf({ 
  path: 'page.pdf', 
  format: 'A4',
  printBackground: true 
});
```

### 视频录制

```javascript
const context = await browser.newContext({
  recordVideo: {
    dir: './videos/',
    size: { width: 1920, height: 1080 }
  }
});
const page = await context.newPage();

// ... do stuff ...

await context.close(); // Video saved automatically
```

### 移动设备模拟

```javascript
const context = await browser.newContext({
  viewport: { width: 375, height: 667 },
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)',
  isMobile: true,
  hasTouch: true
});
```

### 认证

```javascript
// Method 1: HTTP Basic Auth
const context = await browser.newContext({
  httpCredentials: { username: 'user', password: 'pass' }
});

// Method 2: Cookies
await context.addCookies([
  { name: 'session', value: 'abc123', domain: '.example.com', path: '/' }
]);

// Method 3: Local Storage
await page.evaluate(() => {
  localStorage.setItem('token', 'xyz');
});

// Method 4: Reuse auth state
await context.storageState({ path: 'auth.json' });
// Later: await browser.newContext({ storageState: 'auth.json' });
```

## 高级功能

### 文件上传/下载

```javascript
// Upload
await page.setInputFiles('input[type="file"]', '/path/to/file.pdf');

// Download
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('a[download]')
]);
await download.saveAs('/path/to/save/' + download.suggestedFilename());
```

### 对话框处理

```javascript
page.on('dialog', dialog => {
  if (dialog.type() === 'alert') dialog.accept();
  if (dialog.type() === 'confirm') dialog.accept();
  if (dialog.type() === 'prompt') dialog.accept('My answer');
});
```

### 帧（Frames）与 Shadow DOM

```javascript
// Frame by name
const frame = page.frame('frame-name');
await frame.click('button');

// Frame by locator
const frame = page.frameLocator('iframe').first();
await frame.getByRole('button').click();

// Shadow DOM
await page.locator('my-component').locator('button').click();
```

### 跟踪（调试）

```javascript
await context.tracing.start({ screenshots: true, snapshots: true });

// ... run tests ...

await context.tracing.stop({ path: 'trace.zip' });
// View at https://trace.playwright.dev
```

## 配置选项

```javascript
const browser = await chromium.launch({
  headless: true,        // Run without UI
  slowMo: 50,           // Slow down by 50ms (for debugging)
  devtools: false,      // Open DevTools
  args: ['--no-sandbox', '--disable-setuid-sandbox'] // Docker/Ubuntu
});

const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  locale: 'ru-RU',
  timezoneId: 'Europe/Moscow',
  geolocation: { latitude: 55.7558, longitude: 37.6173 },
  permissions: ['geolocation'],
  userAgent: 'Custom Agent',
  bypassCSP: true,      // Bypass Content Security Policy
});
```

## 错误处理

```javascript
// Retry with timeout
try {
  await page.getByRole('button', { name: 'Load' }).click({ timeout: 10000 });
} catch (e) {
  console.log('Button not found or not clickable');
}

// Check if element exists
const hasButton = await page.getByRole('button').count() > 0;

// Wait with custom condition
await page.waitForFunction(() => 
  document.querySelectorAll('.loaded').length >= 10
);
```

## Sudo 用户权限设置

关于 Playwright 浏览器的安装方法：

```bash
# /etc/sudoers.d/playwright
username ALL=(root) NOPASSWD: /usr/bin/npx playwright install-deps *
username ALL=(root) NOPASSWD: /usr/bin/npx playwright install *
```

## 参考资料

- [Playwright 文档](https://playwright.dev)
- [API 参考](https://playwright.dev/docs/api/class-playwright)
- [最佳实践指南](https://playwright.dev/docs/best-practices)
- [定位器使用指南](https://playwright.dev/docs/locators)