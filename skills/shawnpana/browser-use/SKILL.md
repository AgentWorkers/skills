---
name: browser-use
description: 用于从沙箱环境中的远程机器控制云浏览器。当代理程序运行在沙箱环境中（无图形用户界面，GUI不可用）时，可以使用该工具来浏览网页、与网页交互、填写表单、截取屏幕截图，或通过隧道访问本地的开发服务器。
allowed-tools: Bash(browser-use:*)
---
# 针对沙箱环境中的代理的远程浏览器自动化功能

本技能适用于运行在**沙箱化远程机器**（云虚拟机、持续集成（CI）系统或代码执行代理）上的代理，这些代理需要控制浏览器。请安装 `browser-use` 并使用云浏览器进行操作——无需安装本地的 Chrome 浏览器。

## 设置

**仅限远程环境的安装（推荐用于沙箱代理）**
```bash
curl -fsSL https://browser-use.com/cli/install.sh | bash -s -- --remote-only
```

此设置会使得 `browser-use` 仅使用云浏览器：
- 无需下载 Chromium（可节省约 300MB 的磁盘空间）
- `browser-use open <url>` 会自动使用远程模式（无需使用 `--browser` 标志）
- 如果有 API 密钥，也可以在安装时提供：
  ```bash
  curl -fsSL https://browser-use.com/cli/install.sh | bash -s -- --remote-only --api-key bu_xxx
  ```

**手动安装（备用方案）**
```bash
pip install "browser-use[cli]"

# Install cloudflared for tunneling:
# macOS:
brew install cloudflared

# Linux:
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o ~/.local/bin/cloudflared && chmod +x ~/.local/bin/cloudflared

# Windows:
winget install Cloudflare.cloudflared
```

**然后配置您的 API 密钥：**
```bash
export BROWSER_USE_API_KEY=bu_xxx   # Required for cloud browser
```

**验证安装是否成功：**
```bash
browser-use doctor
```

## 核心工作流程

当使用 `--remote-only` 选项安装时，所有命令都会自动使用云浏览器——无需指定 `--browser` 标志：

```bash
# Step 1: Start session (automatically uses remote mode)
browser-use open https://example.com
# Returns: url, live_url (view the browser in real-time)

# Step 2+: All subsequent commands use the existing session
browser-use state                   # Get page elements with indices
browser-use click 5                 # Click element by index
browser-use type "Hello World"      # Type into focused element
browser-use input 3 "text"          # Click element, then type
browser-use screenshot              # Take screenshot (base64)
browser-use screenshot page.png     # Save screenshot to file

# Done: Close the session
browser-use close                   # Close browser and release resources
```

### 安装模式的说明

| 安装命令 | 可用的模式 | 默认模式 | 使用场景 |
|-----------------|-----------------|--------------|----------|
| `--remote-only` | 远程模式 | 远程模式 | 适用于沙箱代理（无图形用户界面） |
| `--local-only` | Chromium 模式 | 本地模式 | 用于本地开发 |
| `--full` | Chromium 模式/远程模式 | 全模式 | 具有最高的灵活性 |

如果只安装了某一种模式，该模式将成为默认模式，此时无需使用 `--browser` 标志。

## 暴露本地开发服务器

如果您在远程机器上运行了开发服务器，并希望云浏览器能够访问该服务器：

```bash
# Start your dev server
python -m http.server 3000 &

# Expose it via Cloudflare tunnel
browser-use tunnel 3000
# → url: https://abc.trycloudflare.com

# Now the cloud browser can reach your local server
browser-use open https://abc.trycloudflare.com
```

**隧道配置：**
```bash
browser-use tunnel <port>           # Start tunnel (returns URL)
browser-use tunnel <port>           # Idempotent - returns existing URL
browser-use tunnel list             # Show active tunnels
browser-use tunnel stop <port>      # Stop tunnel
browser-use tunnel stop --all       # Stop all tunnels
```

**注意：** 隧道与浏览器会话是独立的。它们在 `browser-use close` 命令执行后仍然存在，并且可以单独进行管理。

`cloudflared` 可通过 `install.sh --remote-only` 命令进行安装。如果未安装，请手动安装（详见设置部分）。

## 命令说明

### 导航操作
```bash
browser-use open <url>              # Navigate to URL
browser-use back                    # Go back in history
browser-use scroll down             # Scroll down
browser-use scroll up               # Scroll up
browser-use scroll down --amount 1000  # Scroll by specific pixels (default: 500)
```

### 页面状态操作
```bash
browser-use state                   # Get URL, title, and clickable elements
browser-use screenshot              # Take screenshot (base64)
browser-use screenshot path.png     # Save screenshot to file
browser-use screenshot --full p.png # Full page screenshot
```

### 交互操作（使用 `state` 中的索引）
```bash
browser-use click <index>           # Click element
browser-use type "text"             # Type into focused element
browser-use input <index> "text"    # Click element, then type
browser-use keys "Enter"            # Send keyboard keys
browser-use keys "Control+a"        # Key combination
browser-use select <index> "option" # Select dropdown option
browser-use hover <index>           # Hover over element
browser-use dblclick <index>        # Double-click
browser-use rightclick <index>      # Right-click
```

### JavaScript 和数据操作
```bash
browser-use eval "document.title"   # Execute JavaScript
browser-use extract "all prices"    # Extract data using LLM
browser-use get title               # Get page title
browser-use get html                # Get page HTML
browser-use get html --selector "h1"  # Scoped HTML
browser-use get text <index>        # Get element text
browser-use get value <index>       # Get input value
browser-use get attributes <index>  # Get element attributes
browser-use get bbox <index>        # Get bounding box (x, y, width, height)
```

### 等待条件设置
```bash
browser-use wait selector "h1"                         # Wait for element
browser-use wait selector ".loading" --state hidden    # Wait for element to disappear
browser-use wait text "Success"                        # Wait for text
browser-use wait selector "#btn" --timeout 5000        # Custom timeout (ms)
```

### Cookie 操作
```bash
browser-use cookies get             # Get all cookies
browser-use cookies get --url <url> # Get cookies for specific URL
browser-use cookies set <name> <val>  # Set a cookie
browser-use cookies set name val --domain .example.com --secure  # With options
browser-use cookies set name val --same-site Strict  # SameSite: Strict, Lax, None
browser-use cookies set name val --expires 1735689600  # Expiration timestamp
browser-use cookies clear           # Clear all cookies
browser-use cookies clear --url <url>  # Clear cookies for specific URL
browser-use cookies export <file>   # Export to JSON
browser-use cookies import <file>   # Import from JSON
```

### 标签页管理
```bash
browser-use switch <tab>            # Switch tab by index
browser-use close-tab               # Close current tab
browser-use close-tab <tab>         # Close specific tab
```

### Python 执行（会话保持）
```bash
browser-use python "x = 42"           # Set variable
browser-use python "print(x)"         # Access variable (prints: 42)
browser-use python "print(browser.url)"  # Access browser object
browser-use python --vars             # Show defined variables
browser-use python --reset            # Clear namespace
browser-use python --file script.py   # Run Python file
```

Python 会话会在多次命令执行之间保持状态。`browser` 对象提供了以下方法：
- `browser.url`：当前页面的 URL
- `browser.title`：页面标题
- `browser.html`：获取页面的 HTML 内容
- `browser.goto(url)`：导航到指定 URL
- `browser.click(index)`：点击指定元素
- `browser.type(text)`：在指定元素上输入文本
- `browser.input(index, text)`：先点击元素，然后输入文本
- `browser.keys(keys)`：发送键盘输入
- `browser.screenshot(path)`：截取屏幕截图
- `browser.scroll(direction, amount)`：滚动页面
- `browser.back()`：返回上一页
- `browser.wait(seconds)`：暂停执行指定秒数
- `browser.extract(query)`：使用大型语言模型（LLM）提取数据

### 代理任务管理
```bash
browser-use run "Fill the contact form with test data"   # AI agent
browser-use run "Extract all product prices" --max-steps 50

# Specify LLM model
browser-use run "task" --llm gpt-4o
browser-use run "task" --llm claude-sonnet-4-20250514
browser-use run "task" --llm gemini-2.0-flash

# Proxy configuration (default: us)
browser-use run "task" --proxy-country gb    # UK proxy
browser-use run "task" --proxy-country de    # Germany proxy

# Session reuse (run multiple tasks in same browser session)
browser-use run "task 1" --keep-alive
# Returns: session_id: abc-123
browser-use run "task 2" --session-id abc-123

# Execution modes
browser-use run "task" --no-wait     # Async, returns task_id immediately
browser-use run "task" --wait        # Wait for completion
browser-use run "task" --stream      # Stream status updates
browser-use run "task" --flash       # Fast execution mode

# Advanced options
browser-use run "task" --thinking    # Extended reasoning mode
browser-use run "task" --vision      # Enable vision (default)
browser-use run "task" --no-vision   # Disable vision

# Use cloud profile (preserves cookies across sessions)
browser-use run "task" --profile <cloud-profile-id>

# Task configuration
browser-use run "task" --start-url https://example.com  # Start from specific URL
browser-use run "task" --allowed-domain example.com     # Restrict navigation (repeatable)
browser-use run "task" --metadata key=value             # Task metadata (repeatable)
browser-use run "task" --secret API_KEY=xxx             # Task secrets (repeatable)
browser-use run "task" --skill-id skill-123             # Enable skills (repeatable)

# Structured output and evaluation
browser-use run "task" --structured-output '{"type":"object"}'  # JSON schema for output
browser-use run "task" --judge                          # Enable judge mode
browser-use run "task" --judge-ground-truth "answer"    # Expected answer for judge
```

### 任务管理
```bash
browser-use task list                     # List recent tasks
browser-use task list --limit 20          # Show more tasks
browser-use task list --status running    # Filter by status
browser-use task list --status finished
browser-use task list --session <id>      # Filter by session ID
browser-use task list --json              # JSON output

browser-use task status <task-id>         # Get task status (latest step only)
browser-use task status <task-id> -c      # Compact: all steps with reasoning
browser-use task status <task-id> -v      # Verbose: full details with URLs + actions
browser-use task status <task-id> --last 5   # Show only last 5 steps
browser-use task status <task-id> --step 3   # Show specific step number
browser-use task status <task-id> --reverse  # Show steps newest first
browser-use task status <task-id> --json

browser-use task stop <task-id>           # Stop a running task

browser-use task logs <task-id>           # Get task execution logs
```

### 云会话管理
```bash
browser-use session list                  # List cloud sessions
browser-use session list --limit 20       # Show more sessions
browser-use session list --status active  # Filter by status
browser-use session list --json           # JSON output

browser-use session get <session-id>      # Get session details + live URL
browser-use session get <session-id> --json

browser-use session stop <session-id>     # Stop a session
browser-use session stop --all            # Stop all active sessions

# Create a new cloud session manually
browser-use session create                          # Create with defaults
browser-use session create --profile <id>           # With cloud profile
browser-use session create --proxy-country gb       # With geographic proxy
browser-use session create --start-url https://example.com  # Start at URL
browser-use session create --screen-size 1920x1080  # Custom screen size
browser-use session create --keep-alive             # Keep session alive
browser-use session create --persist-memory         # Persist memory between tasks

# Share session publicly (for collaboration/debugging)
browser-use session share <session-id>    # Create public share URL
browser-use session share <session-id> --delete  # Delete public share
```

### 云配置文件管理

云配置文件用于持久化存储浏览器状态（如 Cookie）。可以使用配置文件来维持登录会话。

```bash
browser-use profile list                  # List cloud profiles
browser-use profile list --page 2 --page-size 50  # Pagination
browser-use profile get <id>              # Get profile details
browser-use profile create                # Create new profile
browser-use profile create --name "My Profile"  # Create with name
browser-use profile update <id> --name "New Name"  # Rename profile
browser-use profile delete <id>           # Delete profile
```

**使用配置文件：**
```bash
# Run task with profile (preserves cookies)
browser-use run "Log into site" --profile <profile-id> --keep-alive

# Create session with profile
browser-use session create --profile <profile-id>

# Open URL with profile
browser-use open https://example.com --profile <profile-id>
```

**将 Cookie 导入到云配置文件：**
```bash
# Export cookies from current session
browser-use cookies export /tmp/cookies.json

# Import to cloud profile
browser-use cookies import /tmp/cookies.json --profile <profile-id>
```

## 运行子代理

云会话和任务为运行**子代理**提供了强大的支持——这些子代理是能够并行执行任务的独立浏览器代理。

### 关键概念

- **会话 = 代理**：每个云会话都是一个具有自己状态的浏览器代理（包括 Cookie、标签页和浏览历史记录）
- **任务 = 工作**：代理需要执行的具体任务。一个代理可以依次执行多个任务
- **并行代理**：同时运行多个会话以实现并行处理
- **会话重用**：在会话仍在运行时，可以继续为其分配新的任务
- **会话生命周期**：一旦会话停止，就无法重新启动——需要创建新的会话

### 基本的子代理工作流程
```bash
# 1. Start a subagent task (creates new session automatically)
browser-use run "Search for AI news and summarize top 3 articles" --no-wait
# Returns: task_id: task-abc, session_id: sess-123

# 2. Check task progress
browser-use task status task-abc
# Shows: Status: running, or finished with output

# 3. View execution logs
browser-use task logs task-abc
```

### 同时运行多个子代理
```bash
# Start 3 parallel research agents
browser-use run "Research competitor A pricing" --no-wait
# → task_id: task-1, session_id: sess-a

browser-use run "Research competitor B pricing" --no-wait
# → task_id: task-2, session_id: sess-b

browser-use run "Research competitor C pricing" --no-wait
# → task_id: task-3, session_id: sess-c

# Monitor all running tasks
browser-use task list --status running
# Shows all 3 tasks with their status

# Check individual task results as they complete
browser-use task status task-1
browser-use task status task-2
browser-use task status task-3
```

### 重用代理执行多个任务
```bash
# Start first task, keep session alive
browser-use run "Log into example.com" --keep-alive --no-wait
# → task_id: task-1, session_id: sess-123

# Wait for login to complete...
browser-use task status task-1
# → Status: finished

# Give the same agent another task (reuses login session)
browser-use run "Navigate to settings and export data" --session-id sess-123 --no-wait
# → task_id: task-2, session_id: sess-123 (same session!)

# Agent retains cookies, login state, etc. from previous task
```

### 管理活跃的代理
```bash
# List all active agents (sessions)
browser-use session list --status active
# Shows: sess-123 [active], sess-456 [active], ...

# Get details on a specific agent
browser-use session get sess-123
# Shows: status, started time, live URL for viewing

# Stop a specific agent
browser-use session stop sess-123

# Stop all agents at once
browser-use session stop --all
```

### 停止任务与会话
```bash
# Stop a running task (session may continue if --keep-alive was used)
browser-use task stop task-abc

# Stop an entire agent/session (terminates all its tasks)
browser-use session stop sess-123
```

### 自定义代理配置
```bash
# Default: US proxy, auto LLM selection
browser-use run "task" --no-wait

# Explicit configuration
browser-use run "task" \
  --llm gpt-4o \
  --proxy-country gb \
  --keep-alive \
  --no-wait

# With cloud profile (preserves cookies across sessions)
browser-use run "task" --profile <profile-id> --no-wait
```

### 监控子代理的状态

任务状态信息的显示方式旨在优化性能。默认情况下仅显示最必要的信息——仅在需要时扩展显示内容：

| 显示模式 | 标志 | 显示内容 | 使用场景 |
|------|------|--------|----------|
| 默认 | （无） | 最少信息 | 仅显示基本进度 |
| 简洁模式 | `-c` | 中等信息量 | 需要详细信息 |
| 详细模式 | `-v` | 最多信息 | 用于调试 |

**推荐的工作流程：**
```bash
# 1. Launch task
browser-use run "task" --no-wait
# → task_id: abc-123

# 2. Poll with default (token efficient) - only latest step
browser-use task status abc-123
# ✅ abc-123... [finished] $0.009 15s
#   ... 1 earlier steps
#   2. I found the information and extracted...

# 3. ONLY IF task failed or need context: use --compact
browser-use task status abc-123 -c

# 4. ONLY IF debugging specific actions: use --verbose
browser-use task status abc-123 -v
```

**对于步骤较多的任务（超过 50 步）：**
```bash
browser-use task status <id> -c --last 5   # Last 5 steps only
browser-use task status <id> -c --reverse  # Newest first
browser-use task status <id> -v --step 10  # Inspect specific step
```

**实时查看代理运行情况：**
```bash
browser-use session get <session-id>
# → Live URL: https://live.browser-use.com?wss=...
```

**检测任务卡住的情况**：如果任务的成本或执行时间不再增加，可能表示任务遇到了问题：
```bash
browser-use task status <task-id>
# 🔄 abc-123... [started] $0.009 45s  ← if cost doesn't change, task is stuck
```

**日志记录**：日志仅在任务完成后可用：
```bash
browser-use task logs <task-id>  # Works after task finishes
```

### 清理操作

在完成并行任务后，请务必清理相关的会话：
```bash
# Stop all active agents
browser-use session stop --all

# Or stop specific sessions
browser-use session stop <session-id>
```

### 故障排除

**在停止任务后尝试重用会话时出现的问题：**
如果停止了一个任务并尝试重用其会话，新任务可能会停留在“创建中”状态。解决方法：创建一个新的代理。

**任务停留在“开始”状态：**
- 使用 `task status` 命令检查任务成本是否仍在增加；如果没有增加，说明任务可能卡住了。
- 使用 `session get` 命令查看任务的实时运行情况。
- 停止当前任务并创建一个新的代理。

**任务完成后会话仍会继续运行：**
任务完成后，会话不会自动关闭。需要手动进行清理：
```bash
browser-use session list --status active  # See lingering sessions
browser-use session stop --all            # Clean up
```

### 会话管理
```bash
browser-use sessions                # List active sessions
browser-use close                   # Close current session
browser-use close --all             # Close all sessions
```

### 全局选项设置
| 选项 | 描述 |
|--------|-------------|
| `--session NAME` | 为会话指定名称（默认为 "default"） |
| `--browser MODE` | 浏览器模式（仅在安装了多种模式时可用） |
| `--profile ID` | 用于存储持久化 Cookie 的云配置文件 ID |
| `--json` | 以 JSON 格式输出结果 |
| `--api-key KEY` | 替换 API 密钥 |

## 常见使用场景

### 使用云浏览器测试本地开发服务器
```bash
# Start dev server
npm run dev &  # localhost:3000

# Tunnel it
browser-use tunnel 3000
# → url: https://abc.trycloudflare.com

# Browse with cloud browser
browser-use open https://abc.trycloudflare.com
browser-use state
browser-use screenshot
```

### 提交表单数据
```bash
browser-use open https://example.com/contact
browser-use state
# Shows: [0] input "Name", [1] input "Email", [2] textarea "Message", [3] button "Submit"
browser-use input 0 "John Doe"
browser-use input 1 "john@example.com"
browser-use input 2 "Hello, this is a test message."
browser-use click 3
browser-use state   # Verify success
```

### 通过循环截取屏幕截图进行视觉验证
```bash
browser-use open https://example.com
for i in 1 2 3 4 5; do
  browser-use scroll down
  browser-use screenshot "page_$i.png"
done
```

## 使用技巧

1. **在沙箱环境中使用 `--remote-only` 选项进行安装**——无需使用 `--browser` 标志
2. **务必先执行 `state` 命令** 以获取可用的元素及其索引
3. **会话会在多次命令执行之间保持状态**——浏览器会一直保持打开状态，直到您手动关闭它
4. **隧道是独立运行的**——它们不需要创建新的浏览器会话，并且在 `browser-use close` 命令执行后仍然有效
5. **使用 `--json` 选项以进行程序化的数据解析**
6. **`tunnel` 命令是幂等的**——对同一端口再次调用时会返回相同的 URL
7. **完成操作后关闭相关组件**：`browser-use close` 用于关闭浏览器；`browser-use tunnel stop --all` 用于关闭所有隧道

## 故障排除

**“浏览器模式‘chromium’未安装”？**
- 您使用的是 `--remote-only` 选项进行安装，该选项不包含本地浏览器模式
- 这对于沙箱代理来说是正常现象
- 如果需要使用本地浏览器，请使用 `--full` 选项重新安装

**云浏览器无法启动？**
- 确保 `BROWSER_USE_API_KEY` 已正确设置
- 请在 [https://browser-use.com](https://browser-use.com) 确认您的 API 密钥是否正确

**隧道无法使用？**
- 确认 `cloudflared` 是否已安装：使用 `which cloudflared` 命令检查
- 如果未安装，请手动安装（详见设置部分），或重新运行 `install.sh --remote-only`
- 使用 `browser-use tunnel list` 命令查看当前激活的隧道
- 使用 `browser-use tunnel stop <port>` 命令停止隧道

**元素无法找到？**
- 使用 `browser-use state` 命令查看当前可用的元素
- 先使用 `browser-use scroll down` 滚动页面，然后再执行 `browser-use state` 命令——有时元素可能位于页面的隐藏部分
- 如果页面内容发生变化，请重新执行 `state` 命令以获取最新的元素索引

## 清理操作

**完成操作后关闭浏览器：**
```bash
browser-use close              # Close browser session
browser-use tunnel stop --all  # Stop all tunnels (if any)
```

浏览器会话和隧道是独立管理的，因此请根据需要分别关闭它们。