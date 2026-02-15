---
name: browser-cash
description: 通过 Browser.cash 启动未被阻止的浏览器会话，以用于网页自动化。这些会话可以绕过反爬虫保护机制（如 Cloudflare、DataDome 等），因此非常适合用于数据抓取和自动化操作。
homepage: https://browser.cash
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["curl","jq"]}}}
---

# browser-cash

通过 Browser.cash 启动未被阻止的浏览器会话，以用于网页自动化。这些会话可以绕过常见的反爬虫保护机制（如 Cloudflare、DataDome 等），因此非常适合用于爬取、测试和自动化任务，这些任务否则可能会被阻止。

**使用场景：** 任何浏览器自动化任务——包括爬取、表单填写、测试、截图等。Browser.cash 生成的会话看起来像真实的浏览器，并能自动处理爬虫检测。

## 设置

**API 密钥** 存储在 clawdbot 的配置文件 `skills.entries.browser-cash.apiKey` 中。

如果未配置，请提示用户：
> 从 https://dash.browser.cash 获取您的 API 密钥，然后运行：
> ```bash
> clawdbot config set skills.entries.browser-cash.apiKey "your_key_here"
> ```

**获取 API 密钥：**
```bash
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)
```

**首次使用前**，如有需要，请检查并安装 Playwright：
```bash
if [ ! -d ~/clawd/node_modules/playwright ]; then
  cd ~/clawd && npm install playwright puppeteer-core
fi
```

## API 基础知识

```bash
curl -X POST "https://api.browser.cash/v1/..." \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json"
```

## 创建浏览器会话

**基本会话：**
```bash
curl -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**响应：**
```json
{
  "sessionId": "abc123...",
  "status": "active",
  "servedBy": "node-id",
  "createdAt": "2025-01-20T01:51:25.000Z",
  "stoppedAt": null,
  "cdpUrl": "wss://gcp-usc1-1.browser.cash/v1/consumer/abc123.../devtools/browser/uuid"
}
```

**带参数的会话：**
```bash
curl -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "US",
    "windowSize": "1920x1080",
    "profile": {
      "name": "my-profile",
      "persist": true
    }
  }'
```

### 会话参数

| 参数 | 类型 | 描述 |
|--------|------|-------------|
| `country` | 字符串 | 两位字母的 ISO 国家代码（例如 "US", "DE", "GB"） |
| `windowSize` | 字符串 | 浏览器尺寸，例如 "1920x1080" |
| `proxyUrl` | 字符串 | SOCKS5 代理地址（可选） |
| `profile.name` | 字符串 | 用于会话持久化的浏览器配置文件名称 |
| `profilepersist` | 布尔值 | 会话结束后是否保存 cookies 或其他数据 |

## 将 Browser.cash 与 Clawdbot 结合使用

Browser.cash 会返回一个 WebSocket CDP URL（格式为 `wss://...`）。可以使用以下两种方法之一进行连接：

### 方法 1：通过 exec 直接连接 CDP（推荐）

**注意：** 在运行 Playwright/Puppeteer 脚本之前，请确保已安装所有依赖项：
```bash
[ -d ~/clawd/node_modules/playwright ] || (cd ~/clawd && npm install playwright puppeteer-core)
```

在 exec 块中使用 Playwright 或 Puppeteer 直接连接到 CDP URL：
```bash
# 1. Create session
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)
SESSION=$(curl -s -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "windowSize": "1920x1080"}')

SESSION_ID=$(echo $SESSION | jq -r '.sessionId')
CDP_URL=$(echo $SESSION | jq -r '.cdpUrl')

# 2. Use via Node.js exec (Playwright)
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.connectOverCDP('$CDP_URL');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://example.com');
  console.log('Title:', await page.title());
  await browser.close();
})();
"

# 3. Stop session when done
curl -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

### 方法 2：基于 curl 的自动化

对于简单的任务，可以使用 curl 通过 CDP 命令与页面交互：
```bash
# Navigate and extract content using the CDP URL
# (See CDP protocol docs for available methods)
```

### 关于 Clawdbot 的浏览器工具

Clawdbot 的内置 `browser` 工具支持 HTTP 控制服务器 URL，而不是原始的 WebSocket CDP。当 Clawdbot 的浏览器控制服务器代理连接时，可以使用 `gateway config.patch` 方法。对于直接使用 Browser.cash 的情况，请使用上述的 exec 方法。

## 获取会话状态

```bash
curl "https://api.browser.cash/v1/browser/session?sessionId=YOUR_SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

会话状态：`starting`、`active`、`completed`、`error`

## 停止会话

```bash
curl -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=YOUR_SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

## 列出所有会话

```bash
curl "https://api.browser.cash/v1/browser/sessions?page=1&pageSize=20" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

## 浏览器配置文件

配置文件可以跨会话保存 cookies、localStorage 和会话数据——这对于保持登录状态或维持会话数据非常有用。

**列出所有配置文件：**
```bash
curl "https://api.browser.cash/v1/browser/profiles" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

**删除配置文件：**
```bash
curl -X DELETE "https://api.browser.cash/v1/browser/profile?profileName=my-profile" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

## 通过 CDP 连接

`cdpUrl` 是 Chrome 开发工具协议（Chrome DevTools Protocol）的 WebSocket 端点。可以使用任何支持 CDP 的库进行连接。

**Playwright：**
```javascript
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP(cdpUrl);
const context = browser.contexts()[0];
const page = context.pages()[0] || await context.newPage();
await page.goto('https://example.com');
```

**Puppeteer：**
```javascript
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.connect({ browserWSEndpoint: cdpUrl });
const pages = await browser.pages();
const page = pages[0] || await browser.newPage();
await page.goto('https://example.com');
```

## 完整的工作流程示例

```bash
# 0. Ensure Playwright is installed
[ -d ~/clawd/node_modules/playwright ] || (cd ~/clawd && npm install playwright puppeteer-core)

# 1. Create session
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)
SESSION=$(curl -s -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "windowSize": "1920x1080"}')

SESSION_ID=$(echo $SESSION | jq -r '.sessionId')
CDP_URL=$(echo $SESSION | jq -r '.cdpUrl')

# 2. Connect with Playwright/Puppeteer using $CDP_URL...

# 3. Stop session when done
curl -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

## 爬取技巧

当从具有延迟加载或无限滚动功能的页面中提取数据时，请遵循以下建议：

```javascript
// Scroll to load all products
async function scrollToBottom(page) {
  let previousHeight = 0;
  while (true) {
    const currentHeight = await page.evaluate(() => document.body.scrollHeight);
    if (currentHeight === previousHeight) break;
    previousHeight = currentHeight;
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1500); // Wait for content to load
  }
}

// Wait for specific elements
await page.waitForSelector('.product-card', { timeout: 10000 });

// Handle "Load More" buttons
const loadMore = await page.$('button.load-more');
if (loadMore) {
  await loadMore.click();
  await page.waitForTimeout(2000);
}
```

**常见技巧：**
- 始终滚动页面以触发延迟加载的内容
- 等待网络请求完成：`await page.waitForLoadState('networkidle')`
- 在提取元素之前使用 `page.waitForSelector()`
- 在执行操作之间添加延迟，以避免被限制请求频率

## 为什么选择 Browser.cash 进行自动化：

- **未被阻止**：会话可以绕过 Cloudflare、DataDome、PerimeterX 等反爬虫机制
- **真实浏览器体验**：会话看起来像普通的 Chrome 浏览器，而非无头浏览器
- **原生支持 CDP**：支持直接通过 WebSocket 连接到 CDP，适用于 Playwright、Puppeteer 或其他工具
- **地理位置定向**：可以在特定国家启动会话
- **会话数据持久化**：会话结束后仍能保留登录状态

## 注意事项：

- 会话在长时间无操作后会自动终止
- 完成任务后请务必停止会话，以避免不必要的资源消耗
- 当需要保持登录状态时，请使用配置文件
- 支持的代理类型仅限于 SOCKS5
- Clawdbot 从 `~/clawd/` 目录运行脚本——请在该目录下安装所需的 npm 依赖项
- 对于完整的页面爬取，务必滚动页面以触发延迟加载的内容