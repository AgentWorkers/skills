---
name: browser-automation-skill
description: OpenClaw代理的高级无头浏览器自动化技能。通过结构化的命令和语义元素定位功能，实现智能网页导航、表单填写、数据提取以及用户界面测试。
read_when:
  - Automating web interactions or browser tasks
  - Extracting data from websites
  - Filling and submitting web forms
  - Testing web user interfaces
  - Scraping structured content from pages
  - Logging into web applications
  - Taking screenshots or PDF snapshots
  - Recording browser sessions
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm"]},"priority":"high"}}
allowed-tools: Bash(agent-browser:*)
---

# OpenClaw 浏览器自动化技能

## 重要提示：在开始之前

**请先阅读项目的 README.md 文件！**

在执行任何浏览器自动化任务之前，请务必：
1. 阅读项目的 README.md 文件，以了解项目的背景和要求。
2. 确定目标 URL、凭据（如有）以及预期的结果。
3. 在运行命令之前，规划好自动化的工作流程。
4. 检查是否存在可以重用的认证/会话状态。

## 安装

### 快速安装（推荐）

```bash
npm install -g agent-browser
agent-browser install --with-deps
```

### 验证安装

```bash
agent-browser --version
```

如果安装失败，请尝试：
```bash
npx agent-browser install --with-deps
```

## 核心工作流程模式

所有浏览器自动化任务都遵循以下模式：

```
1. OPEN    -> Navigate to target URL
2. SNAPSHOT -> Analyze page structure, get element refs
3. INTERACT -> Click, fill, select using refs
4. VERIFY   -> Re-snapshot to confirm changes
5. REPEAT   -> Continue until task complete
6. CLOSE    -> Clean up browser session
```

## 快速参考

### 导航

| 命令 | 描述 |
|---------|-------------|
| `agent-browser open <url>` | 导航到指定 URL |
| `agent-browser back` | 回到上一页 |
| `agent-browser forward` | 前进到下一页 |
| `agent-browser reload` | 重新加载当前页面 |
| `agent-browser close` | 关闭浏览器会话 |

### 页面分析

| 命令 | 描述 |
|---------|-------------|
| `agent-browser snapshot -i` | 生成页面快照（包含交互式元素及其引用） |
| `agent-browser snapshot -i -c` | 生成简洁的交互式页面快照 |
| `agent-browser snapshot -s "#main"` | 仅针对特定容器生成快照 |
| `agent-browser snapshot -d 3` | 限制快照的深度（仅显示前 3 层元素结构） |

### 元素交互（使用快照中的引用）

| 命令 | 描述 |
|---------|-------------|
| `agent-browser click @e1` | 点击指定元素 |
| `agent-browser fill @e1 "text"` | 清空输入框后输入文本 |
| `agent-browser type @e1 "text"` | 直接在输入框中输入文本 |
| `agent-browser press Enter` | 按下回车键 |
| `agent-browser press Control+a` | 按下组合键 |
| `agent-browser select @e1 "value"` | 选择下拉菜单中的选项 |
| `agent-browser check @e1` | 勾选复选框 |
| `agent-browser uncheck @e1` | 取消勾选复选框 |
| `agent-browser hover @e1` | 将鼠标悬停在元素上 |
| `agent-browser upload @e1 file.pdf` | 上传文件 |

### 数据提取

| 命令 | 描述 |
|---------|-------------|
| `agent-browser get text @e1` | 获取元素的文本内容 |
| `agent-browser get html @e1` | 获取元素的 HTML 内容 |
| `agent-browser get value @e1` | 获取输入框的值 |
| `agent-browser get attr @e1 href` | 获取元素的特定属性 |
| `agent-browser get title` | 获取页面标题 |
| `agent-browser get url` | 获取当前 URL |
| `agent-browser get count ".selector"` | 计算匹配的元素数量 |

### 等待（确保操作可靠性）

| 命令 | 描述 |
|---------|-------------|
| `agent-browser wait @e1` | 等待指定元素出现 |
| `agent-browser wait 2000` | 等待 2000 毫秒 |
| `agent-browser wait --text "Success"` | 等待指定文本出现 |
| `agent-browser wait --url "/dashboard"` | 等待页面 URL 发生变化 |
| `agent-browser wait --load networkidle` | 等待网络请求完成 |

### 截图与 PDF 生成

| 命令 | 描述 |
|---------|-------------|
| `agent-browser screenshot out.png` | 保存当前页面的截图 |
| `agent-browser screenshot --full out.png` | 保存整个页面的截图 |
| `agent-browser pdf output.pdf` | 将页面内容保存为 PDF 文件 |

## 常见任务示例

### 示例 1：登录流程

```bash
# 1. Open login page
agent-browser open https://example.com/login

# 2. Get interactive elements
agent-browser snapshot -i
# Output: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Sign in" [ref=e3]

# 3. Fill credentials
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "secure_password"

# 4. Submit
agent-browser click @e3

# 5. Wait for redirect
agent-browser wait --url "/dashboard"
agent-browser wait --load networkidle

# 6. Save session for reuse
agent-browser state save session.json

# 7. Verify success
agent-browser snapshot -i
```

### 示例 2：数据提取循环

```bash
# Navigate to listing page
agent-browser open https://example.com/products

# Get initial snapshot
agent-browser snapshot -i

# Extract data from each item
agent-browser get text @e1
agent-browser get attr @e2 href

# Check for pagination
agent-browser snapshot -s ".pagination"

# Click next if exists
agent-browser click @e5
agent-browser wait --load networkidle

# Re-snapshot for new content
agent-browser snapshot -i
```

### 示例 3：带有验证功能的表单提交

```bash
# Open form
agent-browser open https://example.com/contact

# Analyze form structure
agent-browser snapshot -i

# Fill all required fields
agent-browser fill @e1 "John Doe"
agent-browser fill @e2 "john@example.com"
agent-browser fill @e3 "Hello, this is my message."

# Select dropdown if present
agent-browser select @e4 "support"

# Check required checkbox
agent-browser check @e5

# Submit form
agent-browser click @e6

# Wait and verify submission
agent-browser wait --text "Thank you"
agent-browser snapshot -i
```

### 示例 4：会话状态保存

```bash
# First time: Login and save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "/home"
agent-browser state save auth-session.json

# Later: Restore session and continue
agent-browser state load auth-session.json
agent-browser open https://app.example.com/dashboard
# Already logged in!
```

### 示例 5：多标签页操作

```bash
# Open first site
agent-browser open https://site-a.com

# Open second tab
agent-browser tab new https://site-b.com

# List tabs
agent-browser tab
# Output: Tab 1: site-a.com, Tab 2: site-b.com (active)

# Switch between tabs
agent-browser tab 1
agent-browser snapshot -i
# Work on tab 1...

agent-browser tab 2
agent-browser snapshot -i
# Work on tab 2...
```

### 示例 6：调试失败的自动化任务

```bash
# Enable headed mode to see what's happening
agent-browser open https://example.com --headed

# Check for JavaScript errors
agent-browser errors

# View console output
agent-browser console

# Highlight element to verify selection
agent-browser highlight @e1

# Take screenshot for debugging
agent-browser screenshot debug.png

# Start trace for detailed analysis
agent-browser trace start
# ... perform actions ...
agent-browser trace stop trace.zip
```

## 语义化定位器（替代引用）

当引用不稳定或需要更易读的定位方式时，可以使用语义化定位器：

```bash
# Find by role
agent-browser find role button click --name "Submit"

# Find by text content
agent-browser find text "Sign In" click

# Find by label
agent-browser find label "Email" fill "user@test.com"

# Find first matching selector
agent-browser find first ".item" click

# Find nth element
agent-browser find nth 2 "a" text
```

## 网络控制

```bash
# Mock API response
agent-browser network route "*/api/user" --body '{"name":"Test User"}'

# Block analytics/ads
agent-browser network route "*google-analytics*" --abort
agent-browser network route "*facebook.com*" --abort

# View captured requests
agent-browser network requests --filter api

# Remove routes
agent-browser network unroute
```

## 浏览器配置

```bash
# Set viewport for responsive testing
agent-browser set viewport 1920 1080
agent-browser set viewport 375 667  # Mobile

# Emulate device
agent-browser set device "iPhone 14"
agent-browser set device "Pixel 5"

# Set geolocation
agent-browser set geo 40.7128 -74.0060  # New York

# Dark mode testing
agent-browser set media dark
```

## 最佳实践

### 1. 导航后务必生成快照
```bash
agent-browser open https://example.com
agent-browser wait --load networkidle
agent-browser snapshot -i  # ALWAYS do this after navigation
```

### 2. 对于输入框，使用 `fill` 而不是 `type`
```bash
# GOOD: Clears existing text first
agent-browser fill @e1 "new text"

# BAD: Appends to existing text
agent-browser type @e1 "new text"
```

### 3. 为确保操作可靠性，添加显式的等待时间
```bash
# After clicking that triggers navigation
agent-browser click @e1
agent-browser wait --load networkidle

# After AJAX updates
agent-browser click @e1
agent-browser wait --text "Updated"
```

### 4. 明确处理 iframe 元素
```bash
# Switch to iframe before interacting
agent-browser frame "#iframe-id"
agent-browser snapshot -i
agent-browser click @e1

# Return to main frame
agent-browser frame main
```

### 5. 尽早保存会话状态
```bash
# Save immediately after successful login
agent-browser state save session.json
# Can reload if something breaks later
```

## 错误处理

### 元素未找到
```bash
# Re-snapshot to get updated refs
agent-browser snapshot -i

# Try semantic locator
agent-browser find text "Button Text" click

# Check if element is in iframe
agent-browser frame "#iframe"
agent-browser snapshot -i
```

### 页面无法加载
```bash
# Increase timeout
agent-browser open https://slow-site.com --timeout 60000

# Wait explicitly
agent-browser wait --load networkidle
agent-browser wait 5000
```

### 会话丢失
```bash
# Reload saved state
agent-browser state load session.json
agent-browser reload
```

### 调试模式
```bash
# Visual debugging
agent-browser open https://example.com --headed
agent-browser screenshot debug.png
agent-browser errors
agent-browser console
```

## 并行会话处理

当需要同时操作多个浏览器时：
```bash
# Session 1
agent-browser --session user1 open https://app.com
agent-browser --session user1 snapshot -i

# Session 2 (completely isolated)
agent-browser --session user2 open https://app.com
agent-browser --session user2 snapshot -i

# List all sessions
agent-browser session list

# Each session has separate cookies, storage, and state
```

## JSON 输出（便于解析）

使用 `--json` 标志可获取机器可读的输出格式：

```bash
agent-browser snapshot -i --json | jq '.elements[]'
agent-browser get text @e1 --json
agent-browser get url --json
```

## 视频录制

```bash
# Start recording from current page
agent-browser record start ./demo.webm

# Perform your automation
agent-browser click @e1
agent-browser fill @e2 "text"

# Stop and save
agent-browser record stop
```

## 故障排查指南

1. **命令未找到**：运行 `agent-browser install --with-deps` 进行安装。
2. **元素未找到**：运行 `agent-browser snapshot -i` 以更新引用信息。
3. **页面加载超时**：为加载缓慢的页面添加 `--timeout 60000` 参数。
4. **无法查看操作结果**：使用 `--headed` 标志查看操作过程中的输出。
5. **登录状态未保存**：使用 `agent-browser state save/load` 保存/恢复会话状态。
6. **引用信息发生变化**：导航后务必重新生成快照。
7. **iframe 内容问题**：使用 `agent-browser frame` 切换 iframe 的上下文。