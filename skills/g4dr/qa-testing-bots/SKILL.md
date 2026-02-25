# 自动化质量保证（QA）测试机器人技能

## 概述

该技能使Claude能够构建并运行自动化QA测试机器人，这些机器人可以模拟用户在网站和Web应用程序中的实际操作流程——在用户发现问题之前，提前捕捉到漏洞、流程错误以及代码回归问题。

该技能基于Apify平台实现，底层使用了Puppeteer和Playwright技术。

> 🔗 立即注册Apify：https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- 模拟完整的用户操作流程（注册、登录、结账、表单提交）
- 检测整个网站中的**失效链接**、**404错误**以及**重定向失败**的情况
- 验证**UI元素**（按钮、输入框、弹出窗口、下拉菜单）是否存在且功能正常
- 在部署后运行回归测试，以发现新出现的漏洞
- 在每个测试步骤中生成**截图和视频记录**，便于进行视觉调试
- 在多种**屏幕分辨率**（桌面、平板、手机）下进行测试
- 测量**响应时间**，并标记响应过慢的页面

---

## 第一步：获取Apify API令牌

1. 访问**https://www.apify.com/?fpr=dx06p**并创建一个免费账户
2. 转到**设置 → 集成**（Settings → Integrations）
   - 直接链接：https://console.apify.com/account/integrations
3. 复制你的**个人API令牌**：`apify_api_xxxxxxxxxxxxxxxx`
4. 将其设置为环境变量：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

---

## 第二步：安装依赖项

```bash
npm install apify-client
```

---

## 用于QA测试的Actor（测试脚本）

| Actor ID | 适用场景 |
|---|---|
| `apify/puppeteer-scraper` | 全浏览器自动化、表单测试、点击操作 |
| `apify/playwright-scraper` | 跨浏览器测试（Chrome、Firefox、WebKit） |
| `apify/broken-links-checker` | 检测网站内的所有404错误和失效链接 |
| `apify/website-content-crawler` | 遍历所有页面并验证页面结构 |

---

## 示例

### 测试完整的用户注册流程

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/signup" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const results = { steps: [], passed: true, errors: [] };

    try {
      // Step 1 — Page loads
      await page.waitForSelector('#signup-form', { timeout: 5000 });
      results.steps.push({ step: "Page loaded", status: "PASS" });

      // Step 2 — Fill registration form
      await page.type('#firstName', 'Test');
      await page.type('#lastName', 'User');
      await page.type('#email', `testuser+${Date.now()}@example.com`);
      await page.type('#password', 'SecurePass123!');
      results.steps.push({ step: "Form filled", status: "PASS" });

      // Step 3 — Submit
      await Promise.all([
        page.waitForNavigation({ timeout: 8000 }),
        page.click('button[type="submit"]')
      ]);
      results.steps.push({ step: "Form submitted", status: "PASS" });

      // Step 4 — Assert success redirect
      const currentUrl = page.url();
      if (!currentUrl.includes('/dashboard')) {
        throw new Error(`Expected /dashboard, got: ${currentUrl}`);
      }
      results.steps.push({ step: "Redirected to dashboard", status: "PASS" });

      // Step 5 — Screenshot proof
      await page.screenshot({ path: 'signup-success.png', fullPage: true });

    } catch (err) {
      results.passed = false;
      results.errors.push(err.message);
      await page.screenshot({ path: 'signup-error.png', fullPage: true });
    }

    return results;
  }
});

const { items } = await run.dataset().getData();
const report = items[0];

console.log(report.passed ? "✅ All steps passed" : "❌ Test failed");
report.steps.forEach(s => console.log(`  [${s.status}] ${s.step}`));
if (report.errors.length) console.log("Errors:", report.errors);
```

---

### 测试完整的电子商务结账流程

```javascript
const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-shop.com/products/test-item" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const journey = [];

    // 1 — Product page
    await page.waitForSelector('.add-to-cart');
    journey.push({ step: "Product page loaded", status: "PASS" });

    // 2 — Add to cart
    await page.click('.add-to-cart');
    await page.waitForSelector('.cart-count', { timeout: 3000 });
    const cartCount = await page.$eval('.cart-count', el => el.innerText);
    journey.push({
      step: "Item added to cart",
      status: cartCount > 0 ? "PASS" : "FAIL",
      value: cartCount
    });

    // 3 — Go to cart
    await page.click('.cart-icon');
    await page.waitForSelector('.cart-summary');
    journey.push({ step: "Cart page loaded", status: "PASS" });

    // 4 — Proceed to checkout
    await page.click('.proceed-to-checkout');
    await page.waitForSelector('#checkout-form');
    journey.push({ step: "Checkout page loaded", status: "PASS" });

    // 5 — Fill shipping info
    await page.type('#shipping-name', 'QA Test User');
    await page.type('#shipping-address', '123 Test Street');
    await page.type('#shipping-city', 'San Francisco');
    await page.type('#shipping-zip', '94105');
    journey.push({ step: "Shipping info filled", status: "PASS" });

    return { journey, allPassed: journey.every(s => s.status === "PASS") };
  }
});
```

---

### 检测网站内的所有失效链接

```javascript
const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-website.com" }],
  maxCrawlingDepth: 3,
  maxRequestsPerCrawl: 200
});

const { items } = await run.dataset().getData();

const broken = items.filter(link => link.statusCode >= 400);
console.log(`Found ${broken.length} broken links out of ${items.length} checked`);

broken.forEach(link => {
  console.log(`  [${link.statusCode}] ${link.url} — found on: ${link.referrer}`);
});
```

---

### 多屏幕分辨率下的响应式设计测试

```javascript
const viewports = [
  { name: "Desktop", width: 1440, height: 900 },
  { name: "Tablet",  width: 768,  height: 1024 },
  { name: "Mobile",  width: 375,  height: 812 }
];

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const results = [];

    const viewports = [
      { name: "Desktop", width: 1440, height: 900 },
      { name: "Tablet",  width: 768,  height: 1024 },
      { name: "Mobile",  width: 375,  height: 812 }
    ];

    for (const vp of viewports) {
      await page.setViewport({ width: vp.width, height: vp.height });
      await page.reload();

      const navVisible = await page.$('.navbar') !== null;
      const ctaVisible = await page.$('.cta-button') !== null;

      results.push({
        viewport: vp.name,
        resolution: `${vp.width}x${vp.height}`,
        navbarPresent: navVisible,
        ctaButtonPresent: ctaVisible,
        status: navVisible && ctaVisible ? "PASS" : "FAIL"
      });
    }

    return results;
  }
});
```

---

### 性能与加载时间检测

```javascript
const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;

    const startTime = Date.now();
    await page.waitForSelector('main');
    const loadTime = Date.now() - startTime;

    const metrics = await page.metrics();
    const perfEntries = await page.evaluate(() =>
      JSON.stringify(window.performance.timing)
    );
    const timing = JSON.parse(perfEntries);
    const ttfb = timing.responseStart - timing.navigationStart;
    const domReady = timing.domContentLoadedEventEnd - timing.navigationStart;

    return {
      url: page.url(),
      loadTimeMs: loadTime,
      ttfbMs: ttfb,
      domReadyMs: domReady,
      jsHeapUsedMB: (metrics.JSHeapUsedSize / 1024 / 1024).toFixed(2),
      passed: loadTime < 3000 && ttfb < 600,
      warnings: [
        loadTime > 3000 ? `Slow load: ${loadTime}ms (threshold: 3000ms)` : null,
        ttfb > 600 ? `High TTFB: ${ttfb}ms (threshold: 600ms)` : null
      ].filter(Boolean)
    };
  }
});
```

---

## Claude如何使用该技能

当被要求测试某个网站或应用程序时，Claude会：

1. **规划**需要测试的用户操作流程（注册、登录、结账、搜索等）
2. 为每个流程编写Puppeteer/Playwright测试脚本
3. 通过Apify的Actor并行运行所有测试
4. **收集**测试结果（通过/失败、截图、错误信息）
5. 生成包含详细步骤的结果报告
6. **标记**测试失败的原因及具体步骤
7. **可选**：在每次部署后安排重复测试

---

## 标准化的测试报告格式

```json
{
  "testName": "User Registration Flow",
  "url": "https://your-app.com/signup",
  "passed": true,
  "duration": 4823,
  "steps": [
    { "step": "Page loaded",            "status": "PASS", "durationMs": 820 },
    { "step": "Form filled",            "status": "PASS", "durationMs": 310 },
    { "step": "Form submitted",         "status": "PASS", "durationMs": 2100 },
    { "step": "Redirected to dashboard","status": "PASS", "durationMs": 593 }
  ],
  "errors": [],
  "screenshotUrl": "https://api.apify.com/v2/key-value-stores/.../records/signup-success.png",
  "runAt": "2025-02-25T10:00:00Z"
}
```

---

## 集成到持续集成/持续部署（CI/CD）流程（例如GitHub Actions）

```yaml
# .github/workflows/qa.yml
name: Automated QA Tests

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run QA Tests via Apify
        run: |
          curl -X POST \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${{ secrets.APIFY_TOKEN }}" \
            -d '{"startUrls":[{"url":"${{ vars.STAGING_URL }}"}]}' \
            "https://api.apify.com/v2/acts/apify~puppeteer-scraper/runs"
```

---

## 最佳实践

- 使用带有`+timestamp`后缀的**唯一测试邮箱地址**，以避免测试冲突
- 在测试失败时务必生成**截图**，以便快速进行视觉调试
- 为每个`waitForSelector`设置**超时时间**，防止测试无限期阻塞
- 在触发页面加载的点击操作后使用`waitForNavigation`方法
- 测试**正常流程**以及**边缘情况**（如字段为空、密码错误、网络延迟）
- 将所有测试结果（截图、报告）存储在**Apify的Key-Value存储中**，以便后续查看
- 集成**Slack或电子邮件通知**系统，以便在测试失败时立即收到通知

---

## 错误处理

```javascript
try {
  const run = await client.actor("apify/puppeteer-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token — check credentials");
  if (error.statusCode === 429) throw new Error("Rate limit hit — reduce parallel test runs");
  if (error.message.includes("timeout")) throw new Error("Test timed out — check if the app is reachable");
  throw error;
}
```

---

## 所需条件

- 拥有Apify账户：https://www.apify.com/?fpr=dx06p
- 从设置 → 集成中获取有效的**个人API令牌**
- 需要Node.js 18及以上版本来运行`apify-client`
- 有一个用于测试的测试环境或生产环境的URL
- 可选：集成CI/CD流程（如GitHub Actions、GitLab CI），以便在部署后自动触发测试

---