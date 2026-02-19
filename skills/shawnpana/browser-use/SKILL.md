---
name: browser-use
description: 自动化浏览器交互，用于网页测试、表单填写、截图以及数据提取。适用于用户需要浏览网站、与网页交互、填写表单、截图或从网页中提取信息的情况。
allowed-tools: Bash(browser-use:*)
---
# 使用 `browser-use` CLI 进行浏览器自动化操作

`browser-use` 命令提供了快速且持久的浏览器自动化功能。它可以在多个命令之间保持浏览器会话的状态，从而支持复杂的多步骤工作流程。

## 先决条件

在使用此功能之前，必须先安装并配置 `browser-use`。运行诊断工具以验证配置是否正确：

```bash
browser-use doctor
```

更多信息，请参阅：https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md

## 核心工作流程

1. **导航**：`browser-use open <url>` — 打开指定 URL（如有需要，会启动浏览器）
2. **检查**：`browser-use state` — 返回可点击元素的索引
3. **交互**：使用索引与页面元素进行交互（例如：`browser-use click 5`、`browser-use input 3 "text"`）
4. **验证**：使用 `browser-use state` 或 `browser-use screenshot` 来确认操作结果
5. **重复**：命令执行期间浏览器会保持打开状态

## 浏览器模式

```bash
browser-use --browser chromium open <url>      # Default: headless Chromium
browser-use --browser chromium --headed open <url>  # Visible Chromium window
browser-use --browser real open <url>          # Real Chrome (no profile = fresh)
browser-use --browser real --profile "Default" open <url>  # Real Chrome with your login sessions
browser-use --browser remote open <url>        # Cloud browser
```

- **chromium**：默认模式，快速、隔离、无头（headless）
- **real**：使用真实的 Chrome 浏览器二进制文件。如果不使用 `--profile` 选项，会使用位于 `~/.config/browseruse/profiles/cli/` 的默认配置文件（该文件为空）。使用 `--profile "ProfileName"` 可以使用用户的实际 Chrome 配置文件（包含 cookies、登录信息、扩展程序等）。
- **remote**：基于云的浏览器，支持代理连接

## 常用命令

```bash
# Navigation
browser-use open <url>                    # Navigate to URL
browser-use back                          # Go back
browser-use scroll down                   # Scroll down (--amount N for pixels)

# Page State (always run state first to get element indices)
browser-use state                         # Get URL, title, clickable elements
browser-use screenshot                    # Take screenshot (base64)
browser-use screenshot path.png           # Save screenshot to file

# Interactions (use indices from state)
browser-use click <index>                 # Click element
browser-use type "text"                   # Type into focused element
browser-use input <index> "text"          # Click element, then type
browser-use keys "Enter"                  # Send keyboard keys
browser-use select <index> "option"       # Select dropdown option

# Data Extraction
browser-use eval "document.title"         # Execute JavaScript
browser-use get text <index>              # Get element text
browser-use get html --selector "h1"      # Get scoped HTML

# Wait
browser-use wait selector "h1"            # Wait for element
browser-use wait text "Success"           # Wait for text

# Session
browser-use sessions                      # List active sessions
browser-use close                         # Close current session
browser-use close --all                   # Close all sessions

# AI Agent
browser-use -b remote run "task"          # Run agent in cloud (async by default)
browser-use task status <id>              # Check cloud task progress
```

### 导航与标签页操作
```bash
browser-use open <url>                    # Navigate to URL
browser-use back                          # Go back in history
browser-use scroll down                   # Scroll down
browser-use scroll up                     # Scroll up
browser-use scroll down --amount 1000     # Scroll by specific pixels (default: 500)
browser-use switch <tab>                  # Switch to tab by index
browser-use close-tab                     # Close current tab
browser-use close-tab <tab>              # Close specific tab
```

### 页面状态操作
```bash
browser-use state                         # Get URL, title, and clickable elements
browser-use screenshot                    # Take screenshot (outputs base64)
browser-use screenshot path.png           # Save screenshot to file
browser-use screenshot --full path.png    # Full page screenshot
```

### 与页面元素交互
```bash
browser-use click <index>                 # Click element
browser-use type "text"                   # Type text into focused element
browser-use input <index> "text"          # Click element, then type text
browser-use keys "Enter"                  # Send keyboard keys
browser-use keys "Control+a"              # Send key combination
browser-use select <index> "option"       # Select dropdown option
browser-use hover <index>                 # Hover over element (triggers CSS :hover)
browser-use dblclick <index>              # Double-click element
browser-use rightclick <index>            # Right-click element (context menu)
```

请使用 `browser-use state` 返回的索引来进行操作。

### JavaScript 与数据操作
```bash
browser-use eval "document.title"         # Execute JavaScript, return result
browser-use get title                     # Get page title
browser-use get html                      # Get full page HTML
browser-use get html --selector "h1"      # Get HTML of specific element
browser-use get text <index>              # Get text content of element
browser-use get value <index>             # Get value of input/textarea
browser-use get attributes <index>        # Get all attributes of element
browser-use get bbox <index>              # Get bounding box (x, y, width, height)
```

### Cookies 操作
```bash
browser-use cookies get                   # Get all cookies
browser-use cookies get --url <url>       # Get cookies for specific URL
browser-use cookies set <name> <value>    # Set a cookie
browser-use cookies set name val --domain .example.com --secure --http-only
browser-use cookies set name val --same-site Strict  # SameSite: Strict, Lax, or None
browser-use cookies set name val --expires 1735689600  # Expiration timestamp
browser-use cookies clear                 # Clear all cookies
browser-use cookies clear --url <url>     # Clear cookies for specific URL
browser-use cookies export <file>         # Export all cookies to JSON file
browser-use cookies export <file> --url <url>  # Export cookies for specific URL
browser-use cookies import <file>         # Import cookies from JSON file
```

### 等待条件设置
```bash
browser-use wait selector "h1"            # Wait for element to be visible
browser-use wait selector ".loading" --state hidden  # Wait for element to disappear
browser-use wait selector "#btn" --state attached    # Wait for element in DOM
browser-use wait text "Success"           # Wait for text to appear
browser-use wait selector "h1" --timeout 5000  # Custom timeout in ms
```

### Python 脚本执行

在 `browser-use` 的会话中，Python 脚本可以维护状态。相关对象包括：
- `browser.url`、`browser.title`、`browser.html` — 页面信息
- `browser.goto(url)`、`browser.back()` — 导航操作
- `browser.click(index)`、`browser.type(text)`、`browser.input(index, text)`、`browser.keys(keys)` — 交互操作
- `browser.screenshot(path)`、`browser.scroll(direction, amount)` — 页面截图/滚动操作
- `browser.wait(seconds)`、`browser.extract(query)` — 辅助功能

### 代理任务管理（远程模式）

当使用 `--browser remote` 选项时，可启用以下额外功能：

```bash
# Specify LLM model
browser-use -b remote run "task" --llm gpt-4o
browser-use -b remote run "task" --llm claude-sonnet-4-20250514

# Proxy configuration (default: us)
browser-use -b remote run "task" --proxy-country uk

# Session reuse
browser-use -b remote run "task 1" --keep-alive        # Keep session alive after task
browser-use -b remote run "task 2" --session-id abc-123 # Reuse existing session

# Execution modes
browser-use -b remote run "task" --flash       # Fast execution mode
browser-use -b remote run "task" --wait        # Wait for completion (default: async)

# Advanced options
browser-use -b remote run "task" --thinking    # Extended reasoning mode
browser-use -b remote run "task" --no-vision   # Disable vision (enabled by default)

# Using a cloud profile (create session first, then run with --session-id)
browser-use session create --profile <cloud-profile-id> --keep-alive
# → returns session_id
browser-use -b remote run "task" --session-id <session-id>

# Task configuration
browser-use -b remote run "task" --start-url https://example.com  # Start from specific URL
browser-use -b remote run "task" --allowed-domain example.com     # Restrict navigation (repeatable)
browser-use -b remote run "task" --metadata key=value             # Task metadata (repeatable)
browser-use -b remote run "task" --skill-id skill-123             # Enable skills (repeatable)
browser-use -b remote run "task" --secret key=value               # Secret metadata (repeatable)

# Structured output and evaluation
browser-use -b remote run "task" --structured-output '{"type":"object"}'  # JSON schema for output
browser-use -b remote run "task" --judge                 # Enable judge mode
browser-use -b remote run "task" --judge-ground-truth "expected answer"
```

### 任务管理
```bash
browser-use task list                     # List recent tasks
browser-use task list --limit 20          # Show more tasks
browser-use task list --status finished   # Filter by status (finished, stopped)
browser-use task list --session <id>      # Filter by session ID
browser-use task list --json              # JSON output

browser-use task status <task-id>         # Get task status (latest step only)
browser-use task status <task-id> -c      # All steps with reasoning
browser-use task status <task-id> -v      # All steps with URLs + actions
browser-use task status <task-id> --last 5  # Last N steps only
browser-use task status <task-id> --step 3  # Specific step number
browser-use task status <task-id> --reverse # Newest first

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

browser-use session create                          # Create with defaults
browser-use session create --profile <id>           # With cloud profile
browser-use session create --proxy-country uk       # With geographic proxy
browser-use session create --start-url https://example.com
browser-use session create --screen-size 1920x1080
browser-use session create --keep-alive
browser-use session create --persist-memory

browser-use session share <session-id>              # Create public share URL
browser-use session share <session-id> --delete     # Delete public share
```

### 隧道（Tunnel）管理
```bash
browser-use tunnel <port>           # Start tunnel (returns URL)
browser-use tunnel <port>           # Idempotent - returns existing URL
browser-use tunnel list             # Show active tunnels
browser-use tunnel stop <port>      # Stop tunnel
browser-use tunnel stop --all       # Stop all tunnels
```

### 会话管理
```bash
browser-use sessions                      # List active sessions
browser-use close                         # Close current session
browser-use close --all                   # Close all sessions
```

### 配置文件管理

#### 本地 Chrome 配置文件（`--browser real`）
```bash
browser-use -b real profile list          # List local Chrome profiles
browser-use -b real profile cookies "Default"  # Show cookie domains in profile
```

#### 云配置文件（`--browser remote`）
```bash
browser-use -b remote profile list            # List cloud profiles
browser-use -b remote profile list --page 2 --page-size 50
browser-use -b remote profile get <id>        # Get profile details
browser-use -b remote profile create          # Create new cloud profile
browser-use -b remote profile create --name "My Profile"
browser-use -b remote profile update <id> --name "New"
browser-use -b remote profile delete <id>
```

#### 数据同步
```bash
browser-use profile sync --from "Default" --domain github.com  # Domain-specific
browser-use profile sync --from "Default"                      # Full profile
browser-use profile sync --from "Default" --name "Custom Name" # With custom name
```

### 服务器控制
```bash
browser-use server logs                   # View server logs
```

## 常见使用场景

### 操作本地开发服务器

当你有本地开发服务器并需要通过云浏览器访问它时，可以使用以下流程：
- 启动开发服务器
- 创建隧道
- 通过隧道 URL 远程浏览页面

```bash
# 1. Start your dev server
npm run dev &  # localhost:3000

# 2. Expose it via Cloudflare tunnel
browser-use tunnel 3000
# → url: https://abc.trycloudflare.com

# 3. Now the cloud browser can reach your local server
browser-use --browser remote open https://abc.trycloudflare.com
browser-use state
browser-use screenshot
```

**注意**：隧道与浏览器会话是独立的，即使在关闭 `browser-use` 后也会继续存在，且可以单独管理。需要安装 Cloudflared；可以使用 `browser-use doctor` 命令进行检查。

### 使用用户登录信息进行浏览

当任务需要访问用户已登录的网站（如 Gmail、GitHub、内部系统）时，可以使用以下流程：
- 检查可用的配置文件
- 询问用户选择哪个配置文件及浏览器模式
- 使用选定的配置文件进行浏览；如果找不到合适的配置文件，则需要同步 cookies。

**在浏览需要身份验证的网站之前，系统必须执行以下操作：**
1. 询问用户使用本地 Chrome 浏览器还是云浏览器
2. 显示可用的配置文件列表
3. 选择要使用的配置文件
4. 如果没有合适的配置文件，提示用户是否需要同步 cookies

#### 第一步：检查可用配置文件
```bash
# Option A: Local Chrome profiles (--browser real)
browser-use -b real profile list
# → Default: Person 1 (user@gmail.com)
# → Profile 1: Work (work@company.com)

# Option B: Cloud profiles (--browser remote)
browser-use -b remote profile list
# → abc-123: "Chrome - Default (github.com)"
# → def-456: "Work profile"
```

#### 第二步：使用选定的配置文件进行浏览

由于用户已经登录，因此无需再次登录。

**注意**：云配置文件中的 cookies 可能会过期。如果同步失败，需要从本地 Chrome 配置文件中重新获取 cookies。

#### 第三步：同步 cookies（仅必要时执行）

如果用户希望使用云浏览器但云配置文件中没有正确的 cookies，可以从本地 Chrome 配置文件中同步 cookies。

**在同步之前，系统必须执行以下操作：**
1. 询问用户使用哪个本地 Chrome 配置文件
2. 询问需要同步哪些域名；不要默认同步整个配置文件
3. 确认后再进行同步

**检查本地配置文件中包含的 cookies：**
```bash
browser-use -b real profile cookies "Default"
# → youtube.com: 23
# → google.com: 18
# → github.com: 2
```

**针对特定域名的数据同步（推荐）：**
```bash
browser-use profile sync --from "Default" --domain github.com
# Creates new cloud profile: "Chrome - Default (github.com)"
# Only syncs github.com cookies
```

**全配置文件同步（谨慎使用）：**
```bash
browser-use profile sync --from "Default"
# Syncs ALL cookies — includes sensitive data, tracking cookies, every session token
```
仅当用户明确需要同步整个浏览器状态时才使用此选项。

**细粒度控制（高级功能）：**
```bash
# Export cookies to file, manually edit, then import
browser-use --browser real --profile "Default" cookies export /tmp/cookies.json
browser-use --browser remote --profile <id> cookies import /tmp/cookies.json
```

**使用同步后的配置文件：**
```bash
browser-use --browser remote --profile <id> open https://github.com
```

### 运行子任务

可以使用云会话并行运行多个浏览器代理任务：
- 使用 `run` 命令启动任务
- 使用 `task status` 命令监控任务进度
- 收集任务结果
- 使用 `session stop` 命令清理会话

- **会话与代理的关系**：每个云会话都是一个独立的浏览器代理
- **任务与工作的关系**：代理可以依次执行多个任务
- **会话生命周期**：一旦会话停止，无法重新启动，需要创建新的会话

#### 启动任务
```bash
# Single task (async by default — returns immediately)
browser-use -b remote run "Search for AI news and summarize top 3 articles"
# → task_id: task-abc, session_id: sess-123

# Parallel tasks — each gets its own session
browser-use -b remote run "Research competitor A pricing"
# → task_id: task-1, session_id: sess-a
browser-use -b remote run "Research competitor B pricing"
# → task_id: task-2, session_id: sess-b
browser-use -b remote run "Research competitor C pricing"
# → task_id: task-3, session_id: sess-c

# Sequential tasks in same session (reuses cookies, login state, etc.)
browser-use -b remote run "Log into example.com" --keep-alive
# → task_id: task-1, session_id: sess-123
browser-use task status task-1  # Wait for completion
browser-use -b remote run "Export settings" --session-id sess-123
# → task_id: task-2, session_id: sess-123 (same session)
```

#### 任务管理与停止
```bash
browser-use task list --status finished      # See completed tasks
browser-use task stop task-abc               # Stop a task (session may continue if --keep-alive)
browser-use session stop sess-123            # Stop an entire session (terminates its tasks)
browser-use session stop --all               # Stop all sessions
```

#### 监控

任务状态的输出设计旨在优化性能。默认情况下输出信息较少，仅在需要时才会显示更多详细信息：

| 模式 | 标志 | 输出格式 | 使用场景 |
|------|------|--------|----------|
| 默认 | （无） | 简化格式 | 仅显示进度信息 |
| 压缩格式 | `-c` | 中等详细度 | 需要完整日志信息 |
| 详细格式 | `-v` | 高详细度 | 用于调试 |

```bash
# For long tasks (50+ steps)
browser-use task status <id> -c --last 5   # Last 5 steps only
browser-use task status <id> -v --step 10  # Inspect specific step
```

**实时查看会话状态**：`browser-use session get <session-id>` 可以获取会话的实时 URL，用于查看代理的运行情况。

**检测任务卡顿**：如果 `task status` 中显示的任务成本或执行时间不再增加，说明任务卡住了，此时应停止该任务并重新启动一个新的代理。

**日志记录**：`browser-use task logs <task-id>` 仅在任务完成后可用。

## 全局配置选项

| 选项 | 描述 |
|--------|-------------|
| `--session NAME` | 指定会话名称（默认："default"） |
| `--browser MODE` | 浏览器模式（chromium、real、remote） |
| `--headed` | 是否显示浏览器窗口（仅适用于 chromium 模式） |
| `--profile NAME` | 浏览器配置文件名称（本地或云存储的文件名）；适用于 `open`、`session create` 等命令，不适用于 `run` 命令（此时应使用 `--session-id`） |
| `--json` | 以 JSON 格式输出结果 |
| `--mcp` | 通过 stdin/stdout 以 MCP 服务器模式运行 |

**会话行为**：未指定 `--session` 的命令会使用默认的“default”会话。浏览器会保持打开状态，并在多个命令之间重复使用。使用 `--session NAME` 可以同时运行多个浏览器会话。

## 使用技巧

1. **始终先执行 `browser-use state` 命令**，以获取可操作的元素及其索引
2. **使用 `--headed` 选项进行调试**，查看浏览器的当前操作
3. **会话状态会持久保存**，命令执行期间浏览器会保持打开状态
4. **使用 `--json` 选项以便程序化处理数据**
5. 在同一会话中，`browser-use python` 命令中的 Python 变量会保持其状态
6. **CLI 别名**：`bu`、`browser` 和 `browseruse` 的功能与 `browser-use` 完全相同

## 故障排除

**首先运行诊断工具：**
```bash
browser-use doctor
```

**浏览器无法启动？**
```bash
browser-use close --all               # Close all sessions
browser-use --headed open <url>       # Try with visible window
```

**找不到元素？**
```bash
browser-use state                     # Check current elements
browser-use scroll down               # Element might be below fold
browser-use state                     # Check again
```

**会话相关问题？**
```bash
browser-use sessions                  # Check active sessions
browser-use close --all               # Clean slate
browser-use open <url>                # Fresh start
```

**任务停止后会话状态无法重用？**
如果停止了一个任务并尝试重新使用其会话，新任务可能会停留在“created”状态。此时应创建一个新的会话：
```bash
browser-use session create --profile <profile-id> --keep-alive
browser-use -b remote run "new task" --session-id <new-session-id>
```

**任务卡在“started”状态？**：使用 `task status` 命令检查任务成本是否仍在增加；如果成本不再增加，说明任务卡住了。此时可以使用 `session get` 命令查看实时会话状态，然后停止旧任务并重新启动新任务。

**任务完成后会话仍会保持打开状态**：任务完成后，会话不会自动关闭。可以使用 `browser-use session stop --all` 命令清理会话。

## 清理操作

**使用完成后务必关闭浏览器：**
```bash
browser-use close                     # Close browser session
browser-use session stop --all        # Stop cloud sessions (if any)
browser-use tunnel stop --all         # Stop tunnels (if any)
```