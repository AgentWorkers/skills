---
name: human-browser
description: "这款浏览器专为AI代理设计，具备隐蔽性和住宅代理功能，可在任何服务器上运行，无需使用Mac Mini或台式机。它可用于以下场景：网络爬虫、浏览器自动化、绕过Cloudflare、DataDome、PerimeterX等安全防护机制；设置住宅代理；爬取Instagram、LinkedIn、Amazon、TikTok等网站的数据；实现类似人类的浏览器行为；无头浏览器（headless browser）配合代理使用；自动化登录、填写表单、创建账户；监控价格信息；从受保护网站中提取数据；以及执行Polymarket等任务，同时避免被网络屏蔽。主要功能包括：打开浏览器、爬取网站内容、绕过机器人检测机制、获取网站数据、使用住宅IP地址、模拟人类用户行为、启用隐蔽模式等。适用于需要在服务器上运行浏览器任务的场景。"
---
# 人类浏览器——专为AI代理设计的云浏览器

> **无需Mac Mini，也无需本地机器，可在任何服务器上运行。**  
> 您的AI代理可以随时随地使用这款具有“真实人类特征”的浏览器。

## 该功能的用途  

该功能为OpenClaw代理提供了以下特性：  
- 🌍 **100% 在云端运行**——无需桌面设备或Mac Mini  
- 🇷🇴 通过**罗马尼亚居民IP地址**进行网络请求（由DIGI或WS Telecom通过Bright Data提供）  
- 在所有网站上显示为**iPhone 15 Pro**（或桌面版Chrome浏览器）  
- 🛡️ 规避**Cloudflare、DataDome、PerimeterX**这三种常见的反爬虫系统  
- 🖱️ 鼠标移动采用**贝塞尔曲线**，输入速度为**60–220毫秒/字符**，滚动操作自然流畅  
- **全面防检测机制**：`webdriver=false`设置，确保正确的画布显示、准确的时区和地理位置信息  

## 获取代理凭证（必需）  

该功能可立即使用，但若要使用居民IP代理，则需要以下凭证：  
**→ 访问以下链接获取凭证：https://openclaw.virixlabs.com**  
套餐价格从**每月13.99美元**起（包含代理带宽费用）。  
或者，您也可以使用自己的Bright Data账户——详情请参阅`references/brightdata-setup.md`。  

## 快速入门  

```js
const { launchHuman } = require('./scripts/browser-human');

// Mobile (iPhone 15 Pro) — default
const { browser, page, humanType, humanClick, humanScroll } = await launchHuman();

// Desktop Chrome
const { browser, page } = await launchHuman({ mobile: false });

await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });
await humanScroll(page, 'down');
await humanType(page, 'input[type="email"]', 'user@example.com');
await humanClick(page, 760, 400);
await browser.close();
```  

## 使用场景：  
- **Instagram/TikTok数据抓取**——通过居民IP地址规避所有安全防护机制  
- **LinkedIn自动化操作**——模拟人类输入和鼠标操作，避免被检测到  
- **电子商务价格监控**——适用于Amazon、Wildberries等使用Cloudflare服务的网站  
- **表单自动填写**——正确填充React表单（模拟人类输入行为）  
- **账户创建流程**——结合OTP验证和隐蔽操作，确保会话安全  
- **任何限制使用数据中心IP的网站**——使用居民IP地址可确保操作不被拦截  

## 关键功能示例：  
### React表单输入  
```js
await humanType(page, 'input[name="email"]', 'user@example.com');
// Use humanType (delayed keystroke), NOT page.fill() — React detects fill()
```  
### 点击带有动画效果的按钮  
```js
await page.evaluate((text) => {
  [...document.querySelectorAll('button')]
    .find(b => b.offsetParent && b.textContent.includes(text))?.click();
}, 'Continue');
```  
### 验证当前IP地址  
```js
await page.goto('https://api.ipify.org?format=json');
console.log(await page.textContent('body')); // Romanian IP
```  

## 所需依赖库/服务：  
```bash
npm install playwright
npx playwright install chromium --with-deps
```  
→ 关于Bright Data的设置和计费详情，请参阅`references/brightdata-setup.md`  
→ 如需支持或获取凭证，请访问：https://t.me/virixlabs