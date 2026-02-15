---
name: agent-browser
description: 该工具可自动化浏览器操作，用于网页测试、表单填写、截图以及数据提取。适用于用户需要浏览网站、与网页交互、填写表单、截取屏幕截图、测试网页应用程序或从网页中提取信息的情况。
allowed-tools: Bash(agent-browser:*)
---

# 使用 agent-browser 进行浏览器自动化

## 快速入门

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## 核心工作流程

1. 导航：`agent-browser open <url>`
2. 截取页面快照：`agent-browser snapshot -i`（返回带有引用（如 `@e1`, `@e2`）的元素）
3. 使用快照中的引用进行交互
4. 在导航或 DOM 发生重大变化后重新获取快照

## 命令

### 导航

```bash
agent-browser open <url>      # Navigate to URL (aliases: goto, navigate)
                              # Supports: https://, http://, file://, about:, data://
                              # Auto-prepends https:// if no protocol given
agent-browser back            # Go back
agent-browser forward         # Go forward
agent-browser reload          # Reload page
agent-browser close           # Close browser (aliases: quit, exit)
agent-browser connect 9222    # Connect to browser via CDP port
```

### 截取页面快照（页面分析）

```bash
agent-browser snapshot            # Full accessibility tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3
agent-browser snapshot -s "#main" # Scope to CSS selector
```

### 交互（使用快照中的引用）

```bash
agent-browser click @e1           # Click
agent-browser dblclick @e1        # Double-click
agent-browser focus @e1           # Focus element
agent-browser fill @e2 "text"     # Clear and type
agent-browser type @e2 "text"     # Type without clearing
agent-browser press Enter         # Press key (alias: key)
agent-browser press Control+a     # Key combination
agent-browser keydown Shift       # Hold key down
agent-browser keyup Shift         # Release key
agent-browser hover @e1           # Hover
agent-browser check @e1           # Check checkbox
agent-browser uncheck @e1         # Uncheck checkbox
agent-browser select @e1 "value"  # Select dropdown option
agent-browser select @e1 "a" "b"  # Select multiple options
agent-browser scroll down 500     # Scroll page (default: down 300px)
agent-browser scrollintoview @e1  # Scroll element into view (alias: scrollinto)
agent-browser drag @e1 @e2        # Drag and drop
agent-browser upload @e1 file.pdf # Upload files
```

### 获取信息

```bash
agent-browser get text @e1        # Get element text
agent-browser get html @e1        # Get innerHTML
agent-browser get value @e1       # Get input value
agent-browser get attr @e1 href   # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count ".item"   # Count matching elements
agent-browser get box @e1         # Get bounding box
agent-browser get styles @e1      # Get computed styles (font, color, bg, etc.)
```

### 检查页面状态

```bash
agent-browser is visible @e1      # Check if visible
agent-browser is enabled @e1      # Check if enabled
agent-browser is checked @e1      # Check if checked
```

### 截取屏幕截图和生成 PDF

```bash
agent-browser screenshot          # Screenshot to stdout
agent-browser screenshot path.png # Save to file
agent-browser screenshot --full   # Full page
agent-browser pdf output.pdf      # Save as PDF
```

### 视频录制

```bash
agent-browser record start ./demo.webm    # Start recording (uses current URL + state)
agent-browser click @e1                   # Perform actions
agent-browser record stop                 # Stop and save video
agent-browser record restart ./take2.webm # Stop current + start new recording
```

录制会创建一个新的会话环境，但会保留您当前的 cookies 和存储数据。如果没有提供 URL，系统会自动返回到当前页面。为了获得流畅的演示效果，请先浏览页面，然后再开始录制。

### 等待

```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait 2000                    # Wait milliseconds
agent-browser wait --text "Success"        # Wait for text (or -t)
agent-browser wait --url "**/dashboard"    # Wait for URL pattern (or -u)
agent-browser wait --load networkidle      # Wait for network idle (or -l)
agent-browser wait --fn "window.ready"     # Wait for JS condition (or -f)
```

### 鼠标控制

```bash
agent-browser mouse move 100 200      # Move mouse
agent-browser mouse down left         # Press button
agent-browser mouse up left           # Release button
agent-browser mouse wheel 100         # Scroll wheel
```

### 语义定位器（引用的替代方案）

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find text "Sign In" click --exact      # Exact match only
agent-browser find label "Email" fill "user@test.com"
agent-browser find placeholder "Search" type "query"
agent-browser find alt "Logo" click
agent-browser find title "Close" click
agent-browser find testid "submit-btn" click
agent-browser find first ".item" click
agent-browser find last ".item" click
agent-browser find nth 2 "a" hover
```

### 浏览器设置

```bash
agent-browser set viewport 1920 1080          # Set viewport size
agent-browser set device "iPhone 14"          # Emulate device
agent-browser set geo 37.7749 -122.4194       # Set geolocation (alias: geolocation)
agent-browser set offline on                  # Toggle offline mode
agent-browser set headers '{"X-Key":"v"}'     # Extra HTTP headers
agent-browser set credentials user pass       # HTTP basic auth (alias: auth)
agent-browser set media dark                  # Emulate color scheme
agent-browser set media light reduced-motion  # Light mode + reduced motion
```

### Cookies 和存储数据

```bash
agent-browser cookies                     # Get all cookies
agent-browser cookies set name value      # Set cookie
agent-browser cookies clear               # Clear cookies
agent-browser storage local               # Get all localStorage
agent-browser storage local key           # Get specific key
agent-browser storage local set k v       # Set value
agent-browser storage local clear         # Clear all
```

### 网络请求

```bash
agent-browser network route <url>              # Intercept requests
agent-browser network route <url> --abort      # Block requests
agent-browser network route <url> --body '{}'  # Mock response
agent-browser network unroute [url]            # Remove routes
agent-browser network requests                 # View tracked requests
agent-browser network requests --filter api    # Filter requests
```

### 标签页和窗口

```bash
agent-browser tab                 # List tabs
agent-browser tab new [url]       # New tab
agent-browser tab 2               # Switch to tab by index
agent-browser tab close           # Close current tab
agent-browser tab close 2         # Close tab by index
agent-browser window new          # New window
```

### 帧

```bash
agent-browser frame "#iframe"     # Switch to iframe
agent-browser frame main          # Back to main frame
```

### 对话框

```bash
agent-browser dialog accept [text]  # Accept dialog
agent-browser dialog dismiss        # Dismiss dialog
```

### JavaScript 操作

```bash
agent-browser eval "document.title"   # Run JavaScript
```

## 全局选项

```bash
agent-browser --session <name> ...    # Isolated browser session
agent-browser --json ...              # JSON output for parsing
agent-browser --headed ...            # Show browser window (not headless)
agent-browser --full ...              # Full page screenshot (-f)
agent-browser --cdp <port> ...        # Connect via Chrome DevTools Protocol
agent-browser -p <provider> ...       # Cloud browser provider (--provider)
agent-browser --proxy <url> ...       # Use proxy server
agent-browser --headers <json> ...    # HTTP headers scoped to URL's origin
agent-browser --executable-path <p>   # Custom browser executable
agent-browser --extension <path> ...  # Load browser extension (repeatable)
agent-browser --help                  # Show help (-h)
agent-browser --version               # Show version (-V)
agent-browser <command> --help        # Show detailed help for a command
```

### 代理支持

```bash
agent-browser --proxy http://proxy.com:8080 open example.com
agent-browser --proxy http://user:pass@proxy.com:8080 open example.com
agent-browser --proxy socks5://proxy.com:1080 open example.com
```

## 环境变量

```bash
AGENT_BROWSER_SESSION="mysession"            # Default session name
AGENT_BROWSER_EXECUTABLE_PATH="/path/chrome" # Custom browser path
AGENT_BROWSER_EXTENSIONS="/ext1,/ext2"       # Comma-separated extension paths
AGENT_BROWSER_PROVIDER="your-cloud-browser-provider"  # Cloud browser provider (select browseruse or browserbase)
AGENT_BROWSER_STREAM_PORT="9223"             # WebSocket streaming port
AGENT_BROWSER_HOME="/path/to/agent-browser"  # Custom install location (for daemon.js)
```

## 示例：表单提交

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output shows: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## 示例：使用保存的状态进行身份验证

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later sessions: load saved state
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## 多个浏览器会话

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## JSON 输出（用于解析）

添加 `--json` 选项可生成机器可读的输出格式：

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## 调试

```bash
agent-browser --headed open example.com   # Show browser window
agent-browser --cdp 9222 snapshot         # Connect via CDP port
agent-browser connect 9222                # Alternative: connect command
agent-browser console                     # View console messages
agent-browser console --clear             # Clear console
agent-browser errors                      # View page errors
agent-browser errors --clear              # Clear errors
agent-browser highlight @e1               # Highlight element
agent-browser trace start                 # Start recording trace
agent-browser trace stop trace.zip        # Stop and save trace
agent-browser record start ./debug.webm   # Record video from current page
agent-browser record stop                 # Save recording
```

## 深入文档

有关详细模式和最佳实践，请参阅：

| 参考文档 | 说明 |
|-----------|-------------|
| [references/snapshot-refs.md](references/snapshot-refs.md) | 引用的生命周期、失效规则、故障排除 |
| [references/session-management.md](references/session-management.md) | 多个会话管理、状态持久化、并发爬取 |
| [references/authentication.md](references/authentication.md) | 登录流程、OAuth、双因素认证、状态重用 |
| [references/video-recording.md](references/video-recording.md) | 用于调试和文档记录的视频录制流程 |
| [references/proxy-support.md](references/proxy-support.md) | 代理配置、地理测试、代理轮换 |

## 可直接使用的模板

针对常见场景的可执行工作流程脚本：

| 模板 | 说明 |
|----------|-------------|
| [templates/form-automation.sh](templates/form-automation.sh) | 带有验证功能的表单填写 |
| [templates/authenticated-session.sh](templates/authenticated-session.sh) | 登录一次后重复使用会话状态 |
| [templates/capture-workflow.sh](templates/capture-workflow.sh) | 带有截图的内容提取 |

使用方法：
```bash
./templates/form-automation.sh https://example.com/form
./templates/authenticated-session.sh https://app.example.com/login
./templates/capture-workflow.sh https://example.com ./output
```

## HTTPS 证书错误

对于使用自签名证书或无效证书的网站：
```bash
agent-browser open https://localhost:8443 --ignore-https-errors
```