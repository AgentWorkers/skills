---
name: protonmail-claw
title: ProtonMail
description: 通过 Playwright 浏览器自动化工具管理 ProtonMail 邮件。您可以登录、阅读、发送以及管理您的加密收件箱。
homepage: https://proton.me/mail
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["playwright","node"]},"install":[{"id":"npm","kind":"npm","package":"playwright","bins":["npx playwright"],"label":"Install Playwright (npm)"},{"id":"chromium","kind":"exec","command":"npx playwright install chromium","label":"Install Chromium browser"}]}}
---
# ProtonMail 📨  
您的加密收件箱，实现自动化操作——因为手动查看邮件早就过时了。  

## 功能介绍  
- **安全登录**：可安全地登录任何 ProtonMail 账户  
- **查看邮件**：阅读收件箱中的邮件  
- **发送新邮件**：支持撰写邮件功能  
- **专业级邮箱管理**：像专业人士一样管理您的邮箱  

所有操作均通过 Playwright 浏览器自动化工具完成。无需 API 密钥，也无需处理 IMAP/SMTP 的复杂设置——只需使用浏览器即可完成所有常规操作。  

## 开发原因  
您有更重要的事情要做，而不是浪费时间在 ProtonMail 漂亮但速度较慢的用户界面上。让这个自动化工具来替您处理这些任务吧，您可以一边放松，一边编写代码，或者做您想做的事情。  

我们开发这个工具的原因如下：  
1. ProtonMail 的网页界面使用起来相当繁琐。  
2. 自动化技术正变得越来越流行。  
3. 既然可以编写脚本，为什么还要手动点击呢？  

## 系统要求  
### 基础要求  
- **Node.js** 18 及以上版本（建议使用 20 及以上版本）  
- **Playwright** 1.40 及以上版本（通过 `npm install playwright` 安装）  
- **Chromium 浏览器**（通过 `npx playwright install chromium` 安装）  

### 系统依赖（Linux 环境）  
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2

# Raspberry Pi / ARM
sudo apt-get install -y chromium-browser
```  

### 高级功能（绕过机器人检测机制）  
该工具包含企业级机器人检测规避机制：  
```javascript
// Launch with stealth args
await chromium.launch({ 
  headless: true,
  args: [
    '--disable-blink-features=AutomationControlled',
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage'
  ]
});

// Hide webdriver property
await page.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});
```  
这使得 Chrome 浏览器误以为操作是由人类用户执行的。这个方法在大多数情况下都能有效发挥作用。✨  

## 快速入门  
### 1. 登录  
```javascript
const { chromium } = require('playwright');

async function loginProton(email, password) {
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
  });
  
  const page = await context.newPage();
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  
  await page.goto('https://account.proton.me/login');
  await page.waitForTimeout(2000);
  
  await page.fill('#username', email);
  await page.fill('#password', password);
  await page.click('button[type=submit]');
  await page.waitForTimeout(3000);
  
  return { browser, context, page };
}
```  
### 2. 查看收件箱  
```javascript
await page.goto('https://mail.proton.me/inbox');
await page.waitForTimeout(2000);

const emails = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.item')).map(e => ({
    subject: e.querySelector('.subject')?.innerText,
    sender: e.querySelector('.sender')?.innerText,
    time: e.querySelector('.time')?.innerText
  }));
});

console.log(emails);
```  
### 3. 阅读邮件  
```javascript
await page.click('.item:first-child');
await page.waitForTimeout(2000);

const content = await page.evaluate(() => 
  document.querySelector('.message-content')?.innerText
);
```  
### 4. 发送邮件（已测试并可用）  
```javascript
// Navigate to compose
await page.goto('https://mail.proton.me/compose');
await page.waitForTimeout(3000);

// Use keyboard navigation (most reliable)
// Tab to recipient field
await page.keyboard.press('Tab');
await page.waitForTimeout(500);

// Type recipient
await page.keyboard.type('recipient@email.com');
await page.waitForTimeout(500);

// Tab to subject
await page.keyboard.press('Tab');
await page.waitForTimeout(500);

// Type subject
await page.keyboard.type('Your subject here');
await page.waitForTimeout(500);

// Tab to body
await page.keyboard.press('Tab');
await page.waitForTimeout(500);

// Type message
await page.keyboard.type('Your message here...');

// Send with Ctrl+Enter
await page.keyboard.press('Control+Enter');
await page.waitForTimeout(3000);
```  
### 5. 登出（出于礼貌，请务必执行此操作）  
```javascript
await page.click('button[aria-label="Settings"]');
await page.click('text=Sign out');
await browser.close();
```  

## 环境变量设置  
切勿将密码硬编码到代码中（真的，千万别这么做！）：  
```bash
export PROTON_EMAIL="your@email.com"
export PROTON_PASSWORD="yourpassword"
```  
在代码中应这样设置密码：  
```javascript
const email = process.env.PROTON_EMAIL;
const password = process.env.PROTON_PASSWORD;
```  

## 完整示例  
```javascript
const { chromium } = require('playwright');

async function main() {
  const email = process.env.PROTON_EMAIL || 'your@email.com';
  const password = process.env.PROTON_PASSWORD || 'yourpassword';
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
  });
  
  const page = await context.newPage();
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  
  // Login
  await page.goto('https://account.proton.me/login');
  await page.fill('#username', email);
  await page.fill('#password', password);
  await page.click('button[type=submit]');
  await page.waitForTimeout(5000);
  
  // Go to compose
  await page.goto('https://mail.proton.me/compose');
  await page.waitForTimeout(3000);
  
  // Send email using keyboard navigation (most reliable)
  await page.keyboard.press('Tab');
  await page.keyboard.type('recipient@email.com');
  await page.keyboard.press('Tab');
  await page.keyboard.type('Test Subject');
  await page.keyboard.press('Tab');
  await page.keyboard.type('Hello! This is a test email.');
  await page.keyboard.press('Control+Enter');
  
  await page.waitForTimeout(3000);
  console.log('📧 Email sent!');
  
  await browser.close();
}

main();
```  

## 注意事项  
- **双因素认证（2FA）**：自动化脚本无法完成 2FA 验证（初次登录需使用设备上的浏览器，之后依赖 Cookie 会话）  
- **速率限制**：如果频繁操作，ProtonMail 可能会限制您的访问频率  
- **动态用户界面**：某些组件的类名可能会发生变化，请尽可能使用文本选择器或 ARIA 标签进行定位  
- **无头模式检测**：大部分情况下有效，但 ProtonMail 仍有可能检测到自动化行为  

## 常见问题解决方法  
- **“chromium 未找到”错误**：请确保已正确安装 Chromium 浏览器  
- **机器人检测失败/登录失败**：  
  - 确保已启用机器人检测规避功能  
  - 检查用户代理字符串是否是最新的  
  - 尝试使用无头模式进行测试  
- **超时错误**：增加 `waitForTimeout` 的值  
  - 检查网络连接  
  - 可能是 ProtonMail 实施了速率限制  
- **“libX11 未找到”错误**：请安装相应的系统依赖库（见系统要求部分）  

## 安全提示  
- 密码信息应从环境变量中获取，切勿硬编码  
- 如果 ProtonMail 支持应用专用密码，请使用这些密码  
- 使用完服务后务必及时登录退出  
- （高级选项）可以保存会话 Cookie 以供后续使用  

---

**由 Claws for Claws 团队开发。**  
“因为手动查看邮件只是普通人的做法……”  
*HQ 质量审核通过。*