---
name: playwright-mcp
description: 通过 Playwright MCP 服务器实现浏览器自动化。可以浏览网站、点击页面元素、填写表单、提取数据、截图，以及执行完整的浏览器自动化工作流程。
metadata: {"openclaw":{"emoji":"🎭","os":["linux","darwin","win32"],"requires":{"bins":["playwright-mcp","npx"]},"install":[{"id":"npm-playwright-mcp","kind":"npm","package":"@playwright/mcp","bins":["playwright-mcp"],"label":"Install Playwright MCP"}]}}
---

# Playwright MCP 技能

Playwright MCP 服务器支持浏览器自动化操作，可编程地控制 Chrome、Firefox 或 WebKit 浏览器。

## 安装

```bash
npm install -g @playwright/mcp
# Or
npx @playwright/mcp
```

（首次安装浏览器时，请执行以下操作：）
```bash
npx playwright install chromium
```

## 快速入门

### 启动 MCP 服务器（STDIO 模式）
```bash
npx @playwright/mcp
```

### 带参数启动 MCP 服务器
```bash
# Headless mode
npx @playwright/mcp --headless

# Specific browser
npx @playwright/mcp --browser firefox

# With viewport
npx @playwright/mcp --viewport-size 1280x720

# Ignore HTTPS errors
npx @playwright/mcp --ignore-https-errors
```

## 常见使用场景

### 1. 导航和提取数据
```python
# MCP tools available:
# - browser_navigate: Open URL
# - browser_click: Click element
# - browser_type: Type text
# - browser_select_option: Select dropdown
# - browser_get_text: Extract text content
# - browser_evaluate: Run JavaScript
# - browser_snapshot: Get page structure
# - browser_close: Close browser
```

### 2. 表单交互
```
1. browser_navigate to form URL
2. browser_type into input fields
3. browser_click to submit
4. browser_get_text to verify result
```

### 3. 数据提取
```
1. browser_navigate to page
2. browser_evaluate to run extraction script
3. Parse returned JSON data
```

## MCP 工具参考

| 工具 | 描述 |
|------|-------------|
| `browser_navigate` | 导航到指定 URL |
| `browser_click` | 根据选择器点击元素 |
| `browser_type` | 在输入框中输入文本 |
| `browser_select_option` | 从下拉菜单中选择选项 |
| `browser_get_text` | 获取文本内容 |
| `browser_evaluate` | 执行 JavaScript 代码 |
| `browser_snapshot` | 获取页面的可访问性快照 |
| `browser_close` | 关闭当前浏览器会话 |
| `browser_choose_file` | 上传文件 |
| `browser_press` | 按下键盘键 |

## 配置选项

```bash
# Security
--allowed-hosts example.com,api.example.com
--blocked-origins malicious.com
--ignore-https-errors

# Browser settings
--browser chromium|firefox|webkit
--headless
--viewport-size 1920x1080
--user-agent "Custom Agent"

# Timeouts
--timeout-action 10000      # Action timeout (ms)
--timeout-navigation 30000  # Navigation timeout (ms)

# Output
--output-dir ./playwright-output
--save-trace
--save-video 1280x720
```

## 示例

### 登录网站
```
browser_navigate: { url: "https://example.com/login" }
browser_type: { selector: "#username", text: "user" }
browser_type: { selector: "#password", text: "pass" }
browser_click: { selector: "#submit" }
browser_get_text: { selector: ".welcome-message" }
```

### 提取表格数据
```
browser_navigate: { url: "https://example.com/data" }
browser_evaluate: { 
  script: "() => { return Array.from(document.querySelectorAll('table tr')).map(r => r.textContent); }" 
}
```

### 截取屏幕截图
```
browser_navigate: { url: "https://example.com" }
browser_evaluate: { script: "() => { document.body.style.zoom = 1; return true; }" }
# Screenshot saved via --output-dir or returned in response
```

## 安全注意事项

- 默认情况下，仅允许访问工作区的根目录。
- 通过域名验证来阻止访问不受信任的网站。
- 默认启用沙箱模式（请谨慎使用 `--no-sandbox` 参数）。
- 默认情况下会阻止 Service Worker 的运行。

## 故障排除

```bash
# Update browsers
npx playwright install chromium

# Debug mode
npx @playwright/mcp --headless=false --output-mode=stdout

# Check installation
playwright-mcp --version
```

## 链接

- [Playwright 文档](https://playwright.dev)
- [MCP 协议](https://modelcontextprotocol.io)
- [NPM 包](https://www.npmjs.com/package/@playwright/mcp)