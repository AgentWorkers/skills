---
name: agent-browser
description: >
  这是一个用于AI代理的无头浏览器自动化命令行工具（CLI）。它适用于与网站交互的各种场景，包括页面导航、表单填写、按钮点击、截图获取、数据提取、网页抓取、Web应用测试、文件下载，以及任何需要通过编程方式控制浏览器执行的操作。该工具可以响应以下命令：  
  - “打开一个网站”  
  - “填写表单”  
  - “点击按钮”  
  - “截图”  
  - “抓取数据”  
  - “测试Web应用”  
  - “登录网站”  
  - “监控页面状态”  
  - 以及任何其他需要通过编程方式与网站进行交互的任务。
---
# 使用 agent-browser 进行浏览器自动化

## 设置

运行 `scripts/setup.sh` 以安装 agent-browser 和 Chromium。需要 Node.js。

## 核心工作流程

所有的浏览器自动化操作都遵循以下模式：

1. **导航**：`agent-browser open <url>`
2. **截图**：`agent-browser snapshot -i`（获取元素引用，如 `@e1`、`@e2`）
3. **交互**：使用这些引用进行点击、输入、选择等操作
4. **重新截图**：在页面导航或 DOM 变更后，获取新的元素引用

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## 命令链

当不需要中间输出时，可以使用 `&&` 来连接多个命令：

```bash
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i
```

当需要先解析输出（例如，通过截图获取元素引用）时，需要分别运行这些命令。

## 必需命令

```bash
# Navigate
agent-browser open <url>
agent-browser close

# See the page (always do this first)
agent-browser snapshot -i              # Interactive elements with refs
agent-browser snapshot -i -C           # Include onclick divs

# Interact using @refs
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser select @e1 "option"
agent-browser press Enter
agent-browser scroll down 500

# Get info
agent-browser get text @e1
agent-browser get url
agent-browser get title

# Wait
agent-browser wait @e1                 # For element
agent-browser wait --load networkidle  # For network idle

# Capture
agent-browser screenshot page.png
agent-browser screenshot --full        # Full page
agent-browser pdf output.pdf
```

有关完整的命令参考，请参阅 `references/commands.md`。

## 元素引用的生命周期（重要）

当页面发生变化时，元素引用（`@e1`、`@e2`）会失效。在以下情况下务必重新截图：
- 点击链接或按钮导致页面导航时
- 表单提交时
- 动态内容加载时（下拉菜单、弹出窗口等）

## 常见操作模式

### 表单提交
```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser click @e5
agent-browser wait --load networkidle
```

### 带有状态保持的登录
```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME" && agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Reuse later
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### 数据提取
```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5
agent-browser get text body > page.txt
```

### 截图与差异对比
```bash
agent-browser screenshot baseline.png
# ... changes happen ...
agent-browser diff screenshot --baseline baseline.png
```

### 并行会话
```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser session list
```

## 安全性（可选）

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1          # Wrap output for AI safety
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com"  # Domain allowlist
export AGENT_BROWSER_MAX_OUTPUT=50000               # Prevent context flooding
```

## 清理

操作完成后，请务必关闭所有会话：`agent-browser close`