---
name: browser-ladder
version: 1.0.0
description: 逐步提升您的浏览器开发技能——先从免费版本开始，只有在需要时再升级。技能等级分为：  
L1（基础功能：数据获取）→ L2（本地Playwright框架）→ L3（BrowserCat工具）→ L4（Browserless.io平台，用于绕过验证码或实现自动化操作）。
metadata:
  clawdbot:
    emoji: "🪜"
    requires:
      bins:
        - node
        - docker
    env:
      - name: BROWSERCAT_API_KEY
        description: BrowserCat API key (free tier) - get at https://browsercat.com
        required: false
      - name: BROWSERLESS_TOKEN
        description: Browserless.io token ($10/mo) - get at https://browserless.io
        required: false
---

# 浏览器阶梯 🪜  
只有在确实需要的时候，才从免费方案升级到付费方案。  

## 快速设置  
安装完成后，运行设置脚本：  
```bash
./skills/browser-ladder/scripts/setup.sh
```  
或者手动将其添加到您的 `.env` 文件中：  
```bash
# Optional - only needed for Rungs 3-4
BROWSERCAT_API_KEY=your-key    # Free: https://browsercat.com
BROWSERLESS_TOKEN=your-token   # Paid: https://browserless.io
```  

## 浏览器阶梯的层级  
```
┌─────────────────────────────────────────────┐
│  🪜 Rung 4: Browserless.io (Cloud Paid)     │
│  • CAPTCHA solving, bot detection bypass    │
│  • Cost: $10+/mo                            │
│  • Requires: BROWSERLESS_TOKEN              │
├─────────────────────────────────────────────┤
│  🪜 Rung 3: BrowserCat (Cloud Free)         │
│  • When local Docker fails                  │
│  • Cost: FREE (limited)                     │
│  • Requires: BROWSERCAT_API_KEY             │
├─────────────────────────────────────────────┤
│  🪜 Rung 2: Playwright Docker (Local)       │
│  • JavaScript rendering, screenshots        │
│  • Cost: FREE (CPU only)                    │
│  • Requires: Docker installed               │
├─────────────────────────────────────────────┤
│  🪜 Rung 1: web_fetch (No browser)          │
│  • Static pages, APIs, simple HTML          │
│  • Cost: FREE                               │
│  • Requires: Nothing                        │
└─────────────────────────────────────────────┘

Start at the bottom. Climb only when needed.
```  

## 何时升级  
| 情况 | 对应层级 | 原因 |  
|-----------|------|-----|  
| 静态 HTML、API | 1 | 无需 JavaScript |  
| React/Vue/SPA 应用 | 2 | 需要 JavaScript 进行页面渲染 |  
| 无法使用 Docker | 3 | 使用云服务作为备用方案 |  
| 需要绕过验证码/Cloudflare | 4 | 需要防止机器人访问 |  
| 需要 OAuth/MFA 验证 | 4 | 需要复杂的身份验证流程 |  

## 决策流程  
```
Need to access a URL
         │
         ▼
    Static content? ──YES──▶ Rung 1 (web_fetch)
         │ NO
         ▼
    JS rendering only? ──YES──▶ Rung 2 (Playwright Docker)
         │ NO                        │
         │                     Success? ──NO──▶ Rung 3
         ▼                           │ YES
    CAPTCHA/bot detection? ────────────────────▶ DONE
         │ YES
         ▼
    Rung 4 (Browserless.io) ──▶ DONE
```  

## 使用示例  
### 第 1 层级：静态内容  
```javascript
// Built into Clawdbot
const content = await web_fetch("https://example.com");
```  

### 第 2 层级：需要 JavaScript 渲染的页面  
```bash
docker run --rm -v /tmp:/output mcr.microsoft.com/playwright:v1.58.0-jammy \
  npx playwright screenshot https://spa-app.com /output/shot.png
```  

### 第 3 层级：使用 Cloud Browser（BrowserCat）  
```javascript
const { chromium } = require('playwright');
const browser = await chromium.connect('wss://api.browsercat.com/connect', {
  headers: { 'Api-Key': process.env.BROWSERCAT_API_KEY }
});
```  

### 第 4 层级：绕过验证码（使用 Browserless）  
```javascript
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP(
  `wss://production-sfo.browserless.io?token=${process.env.BROWSERLESS_TOKEN}`
);
// CAPTCHA handled automatically
```  

## 成本优化  
1. **从低层级开始**——始终优先尝试第 1 层级。  
2. **缓存结果**——避免不必要的数据重新请求。  
3. **批量请求**——一次浏览器会话中处理多个页面。  
4. **检查是否成功**——只有在较低层级的方案失败时，才尝试更高层级的方案。  

## 获取服务密钥  
| 服务 | 成本 | 注册方式 |  
|---------|------|---------|  
| BrowserCat | 免费 tier | https://browsercat.com |  
| Browserless.io | 每月 $10+ | https://browserless.io |  

这两种服务都是可选的——第 1 至第 2 层级的方案无需任何 API 密钥即可使用。