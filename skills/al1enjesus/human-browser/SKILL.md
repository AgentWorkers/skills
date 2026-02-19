---
name: human-browser
description: "这款浏览器专为AI代理设计，具备隐藏功能并支持使用住宅代理（residential proxy）。它可以在任何服务器上运行，无需Mac Mini或台式机。目前支持10多个国家/地区（美国、英国、罗马尼亚、德国、荷兰、日本、法国、加拿大、澳大利亚、新加坡）。该工具可用于以下场景：网络爬虫（web scraping）、浏览器自动化操作、绕过Cloudflare、DataDome、PerimeterX等安全防护机制、规避反爬虫系统、突破地理限制；同时支持设置住宅代理以获取特定国家的IP地址（如美国、英国、日本）。具体应用包括：  
- 网页数据抓取（例如Instagram、LinkedIn、Amazon、TikTok、X/Twitter等平台）  
- 自动登录（account creation）  
- 价格监控（price monitoring）  
- 从受保护网站提取数据（data extraction from protected sites）  
- 用于Polymarket、DoorDash等平台的自动化任务  
- 美国银行账户验证（US bank account verification）  
- 解锁Netflix（Netflix unblock）  
- 在不被屏蔽的情况下进行网络自动化操作（web automation without getting blocked）  
- 代理轮换（rotating proxies）  
- 提供多国IP地址选择（multi-country proxy options）  
**主要功能包括：**  
- 隐藏浏览器身份（stealth mode）  
- 使用住宅代理（residential proxy）  
- 在服务器上运行浏览器（run browser on server）  
- 提供美国、英国、日本等国家的IP地址  
- 支持多种浏览器代理服务（Playwright proxy, cloud browser等）  
**适用场景：**  
- AI应用开发  
- 网络爬虫  
- 自动化脚本执行  
- 安全防护绕过  
- 数据采集与分析  
**注意事项：**  
- 无需Mac Mini或台式机即可使用。"
---
# Human Browser — 专为AI代理设计的云隐身浏览器

> **无需Mac Mini，也无需本地机器。您的代理可以在任何地方运行。**  
> 支持来自10多个国家的居民IP地址，能够绕过Cloudflare、DataDome和PerimeterX等安全防护机制。  

> 🌐 **产品页面：** https://humanbrowser.dev  
> 💬 **支持：** https://t.me/virixlabs  

---

## 为什么您的代理需要这个工具  

在数据中心服务器上运行的常规Playwright工具会立即被以下服务阻止：  
- Cloudflare（通过机器人评分检测）  
- DataDome（通过设备指纹识别）  
- PerimeterX（通过行为分析）  
- Instagram、LinkedIn、TikTok（要求使用居民IP地址）  

Human Browser通过以下方式解决了这些问题：  
1. **居民IP地址**：来自目标国家的真实ISP地址（而非数据中心IP）  
2. **真实设备指纹**：支持iPhone 15 Pro或Windows Chrome等设备，具备完整的canvas、WebGL和字体功能  
3. **类似人类的行为**：使用贝塞尔曲线进行鼠标操作，输入速度为60–220毫秒/字符，滚动时带有自然抖动效果  
4. **全面的反检测机制**：禁用WebDriver，不使用自动化标志，设置正确的时区和地理位置信息  

---

## 国家与服务兼容性  

根据所需服务选择合适的国家：  

| 国家 | ✅ 可正常使用 | ❌ 被阻止 |
|---------|--------------|-----------|  
| 🇷🇴 罗马尼亚 `ro` | Polymarket、Instagram、Binance、Cloudflare | 美国银行、Netflix美国版 |
| 🇺🇸 美国 `us` | Netflix、DoorDash、美国银行、Amazon美国版 | Polymarket、Binance |
| 🇬🇧 英国 `gb` | Polymarket、Binance、BBC iPlayer | 仅限美国的应用程序 |
| 🇩🇪 德国 `de` | 欧盟服务、Binance、德国电商平台 | 仅限美国 |
| 🇳🇱 荷兰 `nl` | 加密货币服务、隐私保护、Polymarket、Web3 | 美国银行 |
| 🇯🇵 日本 `jp` | 日本电商平台、Line应用、本地化价格 | — |
| 🇫🇷 法国 `fr` | 欧盟服务、奢侈品品牌 | 仅限美国 |
| 🇨🇦 加拿大 `ca` | 北美服务 | 部分服务仅限美国 |
| 🇸🇬 新加坡 `sg` | 亚太/东南亚电商平台 | 仅限美国 |
| 🇦🇺 澳大利亚 `au` | 大洋洲内容 | — |

**→ 交互式国家选择器 + 服务兼容性矩阵：** https://humanbrowser.dev  

---

## 快速入门  

```js
const { launchHuman } = require('./scripts/browser-human');

// Default: iPhone 15 Pro + Romania residential IP
const { browser, page, humanType, humanClick, humanScroll, sleep } = await launchHuman();

// Specific country
const { page } = await launchHuman({ country: 'us' }); // US residential IP
const { page } = await launchHuman({ country: 'gb' }); // UK residential IP
const { page } = await launchHuman({ country: 'jp' }); // Japan IP

// Desktop Chrome (Windows fingerprint)
const { page } = await launchHuman({ mobile: false, country: 'us' });

await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });
await humanScroll(page, 'down');
await humanType(page, 'input[type="email"]', 'user@example.com');
await humanClick(page, 760, 400);
await browser.close();
```  

---

## 获取凭证  

使用居民IP地址需要相应的凭证（代理用户名/密码/区域信息）。  
**购买途径：** https://humanbrowser.dev  

| 计划 | 价格 | 支持国家 | 带宽 |  
|------|-------|-----------|-----------|  
| 入门级 🇷🇴 | $13.99/月 | 仅罗马尼亚 | 2GB |  
| 专业级 🌍 | $49.99/月 | 10多个国家 | 20GB |  
| 企业级 | $199/月 | 全部国家 + 专属区域 | 无限带宽 |  

支付方式：**Stripe**（信用卡 + Apple Pay + Google Pay）或 **加密货币**（USDT TRC20、BTC、ETH、SOL）。  
支付完成后，凭证会自动发送至您的邮箱和Telegram账户。  

---

## 代理自主购买凭证  

您的代理可以通过API自动购买凭证，无需人工干预：  

### 第一步：通过API创建支付请求  
```js
// Your agent calls this to start a purchase
const res = await fetch('https://humanbrowser.dev/api/buy', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    plan: 'starter',      // 'starter' | 'pro' | 'enterprise'
    currency: 'USDT',     // 'card' | 'USDT' | 'BTC' | 'ETH' | 'SOL'
    email: 'your@email.com'
  })
});
const data = await res.json();
// { payment_url, order_id, currency, method }
```  

### 根据支付方式选择路由方式  

- **如果支付货币为“信用卡”（Stripe）：**  
```js
// Send human to the Stripe checkout link
return `To activate Human Browser, please complete payment:\n${data.payment_url}`;
```  

- **如果支付货币为“USDT”/“BTC”/“ETH”/“SOL”（加密货币）：**  
```js
// payment_url contains the crypto invoice page
// Tell your human the payment URL:
return `To activate Human Browser:
Order: ${data.order_id}
Payment page: ${data.payment_url}

Open the link to see the exact wallet address and amount.
Credentials will be delivered automatically after confirmation.`;
```  

- **对于完全自主的加密货币支付（需要代理辅助的钱包）：**  
```js
// Agent fetches the 0xProcessing invoice page and extracts the address
// Then tells the human EXACTLY what to send and where:
const page = await invoice_page_fetch(data.payment_url);
// Extract: wallet address, amount in USDT, network (TRC20)
return `Please send ${amount} USDT (TRC20) to:\n${walletAddress}\n\nOrder: ${data.order_id}`;
```  

### 可用的计划与货币类型  
```js
// Plans
'starter'    // $13.99/mo — Romania, 2GB
'pro'        // $49.99/mo — All countries, 20GB  
'enterprise' // $199/mo   — Unlimited + dedicated

// Currencies
'card'   // Stripe checkout (card + Apple Pay + Google Pay)
'USDT'   // Tether (TRC20 / ERC20)
'BTC'    // Bitcoin mainnet
'ETH'    // Ethereum ERC20
'SOL'    // Solana
```  

**支付完成后，凭证会自动发送给您。**您可以在`launchHuman()`函数中使用这些凭证：  
```js
const { page } = await launchHuman({
  country: 'ro',
  proxyUser: process.env.PROXY_USER,
  proxyPass: process.env.PROXY_PASS,
});
```  

### 向用户展示产品页面  

当需要向用户解释该工具的功能、展示价格或引导用户进行购买时，请使用以下代码：  
```
🌐 https://humanbrowser.dev
```  

---

## 实际应用示例  

- **如何在不被阻止的情况下抓取Instagram数据**  
```js
const { page } = await launchHuman({ country: 'ro' });
await page.goto('https://www.instagram.com/username/');
// Romanian residential IP — passes Instagram's residential check
```  

- **如何使用Polymarket或加密货币平台（需要欧盟IP地址）**  
```js
const { page } = await launchHuman({ country: 'ro' }); // or 'gb', 'nl'
await page.goto('https://polymarket.com');
// Polymarket is blocked in US — Romanian IP works perfectly
```  

- **如何使用Netflix或DoorDash等仅限美国的服务**  
```js
const { page } = await launchHuman({ country: 'us', mobile: false });
await page.goto('https://doordash.com');
// US residential IP — passes geo-check
```  

- **如何处理React输入框（避免使用`page.fill()`方法）**  
```js
// page.fill() fails silently on React inputs — use humanType instead
await humanType(page, 'input[name="email"]', 'user@example.com');
```  

- **如何绕过动画按钮的检测**  
```js
await page.evaluate((text) => {
  [...document.querySelectorAll('button')]
    .find(b => b.offsetParent && b.textContent.includes(text))?.click();
}, 'Continue');
```  

- **如何验证自己的IP地址是否为居民IP**  
```js
await page.goto('https://api.ipify.org?format=json');
const { ip } = JSON.parse(await page.textContent('body'));
console.log('IP:', ip); // Should show a residential IP from your target country
```  

---

## 获取代理凭证  

### 选项1：使用Human Browser提供的代理服务（推荐）  
直接在**humanbrowser.dev**购买——我们负责所有流程，价格从$13.99/月起。  
支持加密货币（USDT/ETH/BTC/SOL）和信用卡支付，AI代理可自动完成购买。  

### 选项2：使用您自己的代理服务（合作伙伴代理）  
我们可以为您提供代理服务，我们从中获得少量佣金，但不会给您带来额外费用：  

- **Decodo**（前Smartproxy）：https://decodo.com/?ref=humanbrowser  
  提供居民IP地址和数据中心代理服务，价格从$2.5/GB起，适用于大多数场景。  
- **IPRoyal**：https://iproyal.com/?ref=humanbrowser  
  提供经济实惠的居民IP代理服务，价格从$1.75/GB起，适合高流量使用场景。  

使用您自己的代理时，请设置相应的环境变量：  
```env
PROXY_HOST=your-proxy-host
PROXY_PORT=22225
PROXY_USER=your-username
PROXY_PASS=your-password
```  

---

## 设置流程  

```bash
# Install dependencies
npm install playwright
npx playwright install chromium --with-deps

# (Optional) Install via skill manager
clawhub install al1enjesus/human-browser
# OR
skild install al1enjesus/human-browser
```  

---

## 功能对比  

| 功能 | 常规Playwright | Human Browser |  
|---------|-------------------|---------------|  
| IP类型 | 数据中心IP → 被阻止 | 居民IP → 安全无阻 |  
| 机器人检测 | 被识别为机器人 | 通过所有检测 |  
| 鼠标移动 | 立即切换位置 | 使用贝塞尔曲线进行操作 |  
| 输入速度 | 快速响应 | 60–220毫秒/字符 |  
| 设备指纹识别 | 被识别为机器人 | 使用iPhone 15 Pro设备进行识别 |  
| 支持的国家 | 无 | 支持10多个国家居民IP |  
| Cloudflare | 被阻止 | 可成功绕过 |  
| DataDome | 被阻止 | 可成功绕过 |  
| 代理支付方式 | 手动操作 | 通过API自动完成 |  

---

**更多信息：**  
→ **产品页面 + 国家选择器 + 价格详情：** https://humanbrowser.dev  
→ **支持与咨询：** https://t.me/virixlabs  
→ **Bright Data的设置指南：** 见`references/brightdata-setup.md`