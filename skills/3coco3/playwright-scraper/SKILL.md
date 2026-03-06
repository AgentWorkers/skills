# Playwright Stealth Scraper

这是一个专为 OpenClaw 设计的高性能 MCP（Machine Learning Pipeline）技能，它通过使用 Playwright Extra 和 Stealth 插件来绕过反机器人检测机制。

## 主要特性
- **隐身模式**：利用 `puppeteer-extra-plugin-stealth` 模拟真实浏览器行为，从而避免被识别为机器人程序。
- **动态内容处理**：完全支持 JavaScript 执行，适用于单页应用程序（SPA）和基于 React 的网站。
- **灵活的配置选项**：允许自定义视口大小和用户代理（User-Agent）信息。

## 所需工具
### stealth_scrape
- 用于抓取任何 URL 的工具，具备先进的反机器人检测绕过功能。
- 参数：`url` – 目标网站的地址。

## 安装要求
在技能（skill）目录中，需要预先安装 Playwright 和 Chromium。