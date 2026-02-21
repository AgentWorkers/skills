---
name: cdp-browser
description: CDP浏览器控制端，地址为localhost:9222。当您需要检查标签页、截图、浏览页面、滚动内容、将数据发布到X平台，或在持续的浏览器会话中运行JavaScript（例如，在已登录X平台或使用Gmail的会话中）时，请使用该控制端。
---
# cdp-browser

这是一个用于 Chrome/Chromium 的命令行工具（CLI），运行在本地地址 `localhost:9222` 上。该工具支持查看标签页、截图、导航、滚动页面内容、将内容发布到 X（可能是某个特定的平台或服务），以及在浏览器会话中执行 JavaScript 代码。

**先决条件：**  
- Chromium 必须以 `--remote-debugging-port=9222` 的参数运行。  
- 需要 Docker Compose 或启用了远程调试功能的本地 Chrome 浏览器。

## 命令  

从 `bin/` 目录下的脚本中运行这些命令：  

| 命令 | 描述 |
|---------|-------------|
| `status` | 列出所有标签页的信息（以 JSON 格式返回） |
| `tabs` | 与 `status` 命令功能相同 |
| `new <url>` | 打开一个新的标签页，并导航到指定的 URL |
| `goto <tabId> <url>` | 将当前标签页的页面导航到指定的 URL |
| `snapshot <tabId>` | 为当前标签页生成全屏截图（PNG 格式） |
| `close-popup <tabId>` | 关闭弹出窗口或模态框 |
| `scroll <tabId> <px\|sel> [down\|up]` | 根据指定的像素数或选择器内容滚动页面 |
| `tweet <tabId> "text"` | 将当前标签页的内容发布到 X 平台（需确保该标签页已连接到 X 平台） |
| `eval <tabId> "js"` | 在当前标签页中执行 JavaScript 代码，并返回执行结果 |

## 脚本说明：  
- `cdp.js`：用于调用 CDP 的 HTTP API（`/json`、`/json/list`、`/json/new`）的封装脚本。  
- `pw.js`：使用 Playwright 库与浏览器建立连接，并实现截图、导航、滚动、发布内容和执行 JavaScript 等功能。  

## 安全性  

有关安全性的相关措施和操作说明，请参阅 [SECURITY.md](SECURITY.md) 文件。  

**来源：**  
https://github.com/gostlightai/cdp-browser