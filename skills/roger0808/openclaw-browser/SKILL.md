---
name: openclaw-browser
description: Browser automation via Chrome DevTools Protocol (CDP) for OpenClaw. Use when user needs to take screenshots of websites, automate browser actions, or interact with web pages programmatically. Triggers on: screenshot requests, browser automation, web page capture, CDP-based browser control.
---

# OpenClaw 浏览器

通过 Chrome 开发者工具协议（Chrome DevTools Protocol）实现 OpenClaw 的浏览器自动化操作。

## 先决条件

必须安装并运行 Chrome，并且已启用远程调试功能：

```bash
# Start Chrome with CDP (port 9222)
chrome --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0
```

## 快速入门

### 截取网站截图

```bash
# Using the provided script
node ~/.openclaw/workspace/skills/openclaw-browser/scripts/screenshot.js https://example.com /tmp/output.png

# With custom viewport
node ~/.openclaw/workspace/skills/openclaw-browser/scripts/screenshot.js https://example.com /tmp/output.png --width=1920 --height=1080
```

### 截取完整页面截图

该脚本会自动捕获整个页面的内容，而不仅仅是可视窗口的内容。

## 工作原理

1. 通过 CDP（Chrome 开发者工具协议）连接到正在运行的 Chrome 浏览器（地址：http://127.0.0.1:9222）
2. 创建新标签页或使用现有的标签页
3. 导航到目标网址
4. 等待页面加载完成
5. 截取页面截图
6. 将截图保存到指定路径

## 常见问题

**Chrome 无法运行：**
- 先使用 CDP 标志启动 Chrome 浏览器
- 通过以下命令验证：`curl http://127.0.0.1:9222/json/version`

**无头浏览器检测：**
- 某些网站（如小红书、淘宝）能够检测到无头浏览器
- 解决方案：使用有可见窗口的 Chrome 浏览器
- 本工具会连接到已打开的 Chrome 浏览器，从而避免被检测到

**权限问题：**
- 如有需要，可以在启动 Chrome 时使用 `--no-sandbox` 参数

## 脚本参考

主要自动化脚本位于 [scripts/screenshot.js](scripts/screenshot.js) 文件中。

## 高级用法

如需实现除截图之外的自定义自动化操作，可以修改脚本或直接使用 Puppeteer：

```javascript
const puppeteer = require('puppeteer');
const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
// ... custom actions
```