---
name: browser-automation
description: 使用MCP协议，通过人工智能控制Chrome浏览器。适用于用户需要自动化执行浏览器操作的情况，例如截图、填写表单、点击页面元素、浏览历史记录搜索、管理书签，或执行任何基于浏览器的自动化任务。该功能兼容您现有的Chrome浏览器及登录会话。
---
# 浏览器自动化（Chrome MCP 服务器）

将您的 Chrome 浏览器变成智能助手——让 AI 控制您的浏览器。

## 何时使用此功能

当用户需要执行以下操作时，可以使用此功能：

- 自动化浏览器任务（点击、填写表单、导航）
- 截取网页或元素的截图
- 从网页中提取内容
- 搜索浏览历史记录或管理书签
- 监控网络请求
- 使用现有的登录会话让 AI 与网站交互

## 安装

### 第一步：安装 Native Bridge

```bash
npm install -g mcp-chrome-bridger
# or
pnpm install -g mcp-chrome-bridger
mcp-chrome-bridger register
```

### 第二步：安装 Chrome 扩展程序

从 [GitHub 仓库](https://github.com/femto/mcp-chrome/releases) 下载扩展程序：

1. 下载 `mcp-chrome-extension-vX.X.X.zip`
2. 打开 Chrome → 进入 `chrome://extensions/`
3. 启用“开发者模式”
4. 点击“加载解压文件”，选择解压后的文件夹
5. 点击扩展程序图标 → 点击“连接”

### 第三步：配置 MCP 客户端

将以下配置添加到您的 MCP 客户端中：

**推荐方案：Streamable HTTP**

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "type": "http",
      "url": "http://127.0.0.1:12306/mcp"
    }
  }
}
```

**备用方案：STDIO**

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "command": "npx",
      "args": ["mcp-chrome-bridger", "stdio"]
    }
  }
}
```

## 可用工具（20 多种）

### 浏览器管理

| 工具 | 描述 |
|------|-------------|
| `get_windows_and_tabs` | 列出所有浏览器窗口和标签页 |
| `chrome_navigate` | 导航到指定 URL，控制视口 |
| `chrome_switch_tab` | 切换活动标签页 |
| `chrome_close_tabs` | 关闭特定标签页 |
| `chrome_go_back_or_forward` | 查看浏览历史记录 |

### 截图

| 工具 | 描述 |
|------|-------------|
| `chrome_screenshot` | 截取整个页面、视口或特定元素的截图 |

### 内容分析

| 工具 | 描述 |
|------|-------------|
| `chrome_get_web_content` | 从网页中提取 HTML/文本 |
| `chrome_get_interactive_elements` | 查找可点击元素 |
| `search_tabs_content` | 基于 AI 的跨标签页语义搜索 |
| `chrome_console` | 获取浏览器控制台输出 |

### 交互

| 工具 | 描述 |
|------|-------------|
| `chrome_click_element` | 通过 CSS 选择器点击元素 |
| `chrome_fill_or_select` | 填写表单并选择选项 |
| `chrome_keyboard` | 模拟键盘输入 |

### 数据管理

| 工具 | 描述 |
|------|-------------|
| `chrome_history` | 查看浏览历史记录 |
| `chrome_bookmark_search` | 查找书签 |
| `chrome_bookmark_add` | 添加新书签 |
| `chrome_bookmark_delete` | 删除书签 |

### 网络

| 工具 | 描述 |
|------|-------------|
| `chrome_network_capture_start/stop` | 监控网络请求 |
| `chrome_network_request` | 使用浏览器 cookie 发送 HTTP 请求 |

## 示例用法

### 导航和截图

```
User: "Take a screenshot of github.com"

AI uses:
1. chrome_navigate(url: "https://github.com")
2. chrome_screenshot(fullPage: true)
```

### 填写表单

```
User: "Login to my account on example.com"

AI uses:
1. chrome_navigate(url: "https://example.com/login")
2. chrome_fill_or_select(selector: "#email", value: "user@example.com")
3. chrome_fill_or_select(selector: "#password", value: "...")
4. chrome_click_element(selector: "button[type=submit]")
```

### 查看浏览历史记录

```
User: "Find all pages I visited about React hooks last week"

AI uses:
1. chrome_history(text: "React hooks", startTime: "1 week ago")
```

### 提取内容

```
User: "What does this page say about pricing?"

AI uses:
1. chrome_get_web_content()
2. Analyzes the extracted content
```

## 与 Playwright 的优势对比

| 功能 | Playwright MCP | Chrome MCP 服务器 |
|---------|---------------|-------------------|
| 浏览器实例 | 新的浏览器进程 | 使用您现有的 Chrome 浏览器 |
| 登录会话 | 需要重新登录 | 使用现有的登录会话 |
| 用户设置 | 清洁的环境 | 使用您的书签、扩展程序和设置 |
| 启动时间 | 启动浏览器较慢 | 扩展程序已加载，启动迅速 |
| 资源消耗 | 资源消耗较大 | 资源消耗较低 |

## 多客户端支持

多个 AI 客户端可以同时连接：

- Claude Code
- Cursor
- Kiro
- 任何兼容 MCP 的客户端

每个客户端都有自己的会话，同时共享同一个 Chrome 浏览器。

## 故障排除

### 扩展程序无法连接

1. 确保在 `chrome://extensions/` 中启用了该扩展程序
2. 点击扩展程序图标，检查“已连接”状态
3. 如有必要，重启 Chrome

### 端口已被占用

服务器会自动处理端口冲突。如果问题仍然存在：

```bash
lsof -i :12306
kill <PID>
```

## 资源链接

- GitHub: https://github.com/femto/mcp-chrome
- npm: https://www.npmjs.com/package/mcp-chrome-bridger
- 新版本发布：https://github.com/femto/mcp-chrome/releases