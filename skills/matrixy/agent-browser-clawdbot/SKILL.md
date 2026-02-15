---
name: agent-browser
description: 专为AI代理优化的无头浏览器自动化命令行工具（CLI），支持访问性树（Accessibility Tree）快照功能以及基于引用（Reference-based）的元素选择机制。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"commands":["agent-browser"]},"homepage":"https://github.com/vercel-labs/agent-browser"}}
---

# Agent Browser 技能

该技能利用可访问性树（accessibility tree）的快照以及相应的引用（refs），实现高效的浏览器自动化操作，从而能够精确地选择页面元素。

## 为何选择使用 Agent Browser 而非内置的浏览器工具

**在以下情况下使用 Agent Browser：**
- 需要自动化多步骤的工作流程
- 需要精确地选择页面元素
- 性能至关重要
- 需要处理复杂的单页应用程序（SPAs）
- 需要实现会话隔离

**在以下情况下使用内置的浏览器工具：**
- 需要截图或 PDF 文件用于分析
- 需要进行视觉检查
- 需要与浏览器扩展程序集成

## 核心工作流程

```bash
# 1. Navigate and snapshot
agent-browser open https://example.com
agent-browser snapshot -i --json

# 2. Parse refs from JSON, then interact
agent-browser click @e2
agent-browser fill @e3 "text"

# 3. Re-snapshot after page changes
agent-browser snapshot -i --json
```

## 关键命令

### 导航
```bash
agent-browser open <url>
agent-browser back | forward | reload | close
```

### 生成快照（务必使用 `-i --json` 参数）
```bash
agent-browser snapshot -i --json          # Interactive elements, JSON output
agent-browser snapshot -i -c -d 5 --json  # + compact, depth limit
agent-browser snapshot -s "#main" -i      # Scope to selector
```

### 与页面元素交互（基于引用）
```bash
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8
```

### 获取信息
```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
```

### 检查页面状态
```bash
agent-browser is visible @e2 --json
agent-browser is enabled @e3 --json
agent-browser is checked @e4 --json
```

### 等待页面加载完成
```bash
agent-browser wait @e2                    # Wait for element
agent-browser wait 1000                   # Wait ms
agent-browser wait --text "Welcome"       # Wait for text
agent-browser wait --url "**/dashboard"   # Wait for URL
agent-browser wait --load networkidle     # Wait for network
agent-browser wait --fn "window.ready === true"
```

### 管理多个独立运行的浏览器会话
```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
# Or via env: AGENT_BROWSER_SESSION=admin agent-browser ...
```

### 保持会话状态
```bash
agent-browser state save auth.json        # Save cookies/storage
agent-browser state load auth.json        # Load (skip login)
```

### 生成截图或 PDF 文件
```bash
agent-browser screenshot page.png
agent-browser screenshot --full page.png
agent-browser pdf page.pdf
```

### 控制网络请求
```bash
agent-browser network route "**/ads/*" --abort           # Block
agent-browser network route "**/api/*" --body '{"x":1}'  # Mock
agent-browser network requests --filter api              # View
```

### 管理 Cookie 和本地存储
```bash
agent-browser cookies                     # Get all
agent-browser cookies set name value
agent-browser storage local key           # Get localStorage
agent-browser storage local set key val
```

### 管理浏览器标签页和框架
```bash
agent-browser tab new https://example.com
agent-browser tab 2                       # Switch to tab
agent-browser frame @e5                   # Switch to iframe
agent-browser frame main                  # Back to main
```

## 快照输出格式

```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}
```

## 最佳实践

1. **务必使用 `-i` 参数**——专注于交互式元素
2. **务必使用 `--json` 参数**——便于数据解析
3. **等待页面完全加载**——使用 `agent-browser wait --load networkidle` 命令
4. **保存用户认证状态**——使用 `state save/load` 命令来处理登录流程
5. **使用独立会话**——确保不同浏览器上下文之间的数据隔离
6. **使用 `--headed` 参数进行调试**——查看页面的详细加载过程

## 示例：搜索并提取数据

```bash
agent-browser open https://www.google.com
agent-browser snapshot -i --json
# AI identifies search box @e1
agent-browser fill @e1 "AI agents"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i --json
# AI identifies result refs
agent-browser get text @e3 --json
agent-browser get attr @e4 "href" --json
```

## 示例：多会话测试

```bash
# Admin session
agent-browser --session admin open app.com
agent-browser --session admin state load admin-auth.json
agent-browser --session admin snapshot -i --json

# User session (simultaneous)
agent-browser --session user open app.com
agent-browser --session user state load user-auth.json
agent-browser --session user snapshot -i --json
```

## 安装方法

```bash
npm install -g agent-browser
agent-browser install                     # Download Chromium
agent-browser install --with-deps         # Linux: + system deps
```

## 致谢

该技能由 Yossi Elkrief ([@MaTriXy](https://github.com/MaTriXy)) 创建。

Agent Browser 的命令行接口（CLI）由 [Vercel Labs](https://github.com/vercel-labs/agent-browser) 开发。