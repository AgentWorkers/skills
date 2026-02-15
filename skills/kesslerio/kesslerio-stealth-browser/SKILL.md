---
name: stealth-browser
description: 使用 Camoufox 和 Nodriver 实现反机器人浏览器自动化。能够绕过 Cloudflare Turnstile、Datadome 以及 Airbnb 和 Yelp 等网站上的严格反机器人机制。当标准的 Playwright/Selenium 被阻止使用时，可以使用此方法。
metadata:
  openclaw:
    emoji: "🥷"
    requires:
      bins: ["distrobox"]
      env: []
---

# 隐形浏览器技巧 🥷  
这是一种能够绕过Cloudflare Turnstile、Datadome以及各种复杂身份验证机制的自动化浏览器工具。  

## 适用场景  
- 当标准的Playwright/Selenium工具被阻止时  
- 当网站显示Cloudflare的身份验证提示或“正在检查您的浏览器”时  
- 需要抓取Airbnb、Yelp等受保护的网站数据时  
- 当`playwright-stealth`工具不再正常工作时  

## 工具选择  
| 目标难度 | 工具 | 适用场景 |  
|---------|--------|------------------|