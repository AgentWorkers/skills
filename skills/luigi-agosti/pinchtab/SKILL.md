---
name: pinchtab
description: 通过 Pinchtab 的 HTTP API 来控制无头或有头的 Chrome 浏览器。该 API 可用于网页自动化、数据抓取、表单填写、导航以及多标签页操作。Pinchtab 以扁平化的 JSON 格式提供可访问性树（accessibility tree），并附带稳定的引用（refs），非常适合 AI 代理使用（低请求成本、快速响应）。适用于以下场景：浏览网站、填写表单、点击按钮、提取页面文本、截图，或任何基于浏览器的自动化任务。使用前需确保已启动 Pinchtab 实例（Go 语言编写的二进制程序）。
homepage: https://pinchtab.com
metadata:
  openclaw:
    emoji: "🦀"
    requires:
      bins: ["pinchtab"]
      env:
        - name: BRIDGE_TOKEN
          secret: true
          optional: true
          description: "Bearer auth token for Pinchtab API"
        - name: BRIDGE_BIND
          optional: true
          description: "Bind address (default: 127.0.0.1, set 0.0.0.0 for network access)"
        - name: BRIDGE_PORT
          optional: true
          description: "HTTP port (default: 9867)"
        - name: BRIDGE_HEADLESS
          optional: true
          description: "Run Chrome headless (true/false)"
        - name: BRIDGE_PROFILE
          optional: true
          description: "Chrome profile directory (default: ~/.pinchtab/chrome-profile)"
        - name: BRIDGE_STATE_DIR
          optional: true
          description: "State/session storage directory (default: ~/.pinchtab)"
        - name: BRIDGE_NO_RESTORE
          optional: true
          description: "Skip restoring tabs from previous session (true/false)"
        - name: BRIDGE_STEALTH
          optional: true
          description: "Stealth level: light (default, basic) or full (canvas/WebGL/font spoofing)"
        - name: BRIDGE_MAX_TABS
          optional: true
          description: "Maximum number of open tabs (default: 20, 0 = unlimited)"
        - name: BRIDGE_BLOCK_IMAGES
          optional: true
          description: "Block image loading for faster, lower-bandwidth browsing (true/false)"
        - name: BRIDGE_BLOCK_MEDIA
          optional: true
          description: "Block all media: images + fonts + CSS + video (true/false)"
        - name: BRIDGE_NO_ANIMATIONS
          optional: true
          description: "Disable CSS animations/transitions globally (true/false)"
        - name: BRIDGE_TIMEZONE
          optional: true
          description: "Force browser timezone (IANA tz, e.g. Europe/Rome)"
        - name: BRIDGE_CHROME_VERSION
          optional: true
          description: "Chrome version string used by fingerprint rotation profiles"
        - name: CHROME_BINARY
          optional: true
          description: "Path to Chrome/Chromium binary (auto-detected if not set)"
        - name: CHROME_FLAGS
          optional: true
          description: "Extra Chrome flags, space-separated"
        - name: BRIDGE_CONFIG
          optional: true
          description: "Path to config JSON file (default: ~/.pinchtab/config.json)"
        - name: BRIDGE_TIMEOUT
          optional: true
          description: "Action timeout in seconds (default: 15)"
        - name: BRIDGE_NAV_TIMEOUT
          optional: true
          description: "Navigation timeout in seconds (default: 30)"
        - name: CDP_URL
          optional: true
          description: "Connect to existing Chrome DevTools instead of launching"
        - name: BRIDGE_NO_DASHBOARD
          optional: true
          description: "Disable dashboard/orchestrator endpoints on instance processes"
        - name: PINCHTAB_AUTO_LAUNCH
          optional: true
          description: "Dashboard mode: auto-launch default profile instance on startup"
        - name: PINCHTAB_DEFAULT_PROFILE
          optional: true
          description: "Dashboard mode: default profile name for auto-launch"
        - name: PINCHTAB_DEFAULT_PORT
          optional: true
          description: "Dashboard mode: default port for auto-launched profile"
        - name: PINCHTAB_HEADED
          optional: true
          description: "Dashboard mode: when set, auto-launched profile runs headed"
        - name: PINCHTAB_DASHBOARD_URL
          optional: true
          description: "Base dashboard URL used by `pinchtab connect` helper"
---
# Pinchtab

这是一个专为AI代理设计的快速、轻量级的浏览器控制工具，通过HTTP协议和浏览器可访问性树（accessibility tree）实现各种操作。

## 设置

您可以通过以下方式之一启动Pinchtab：

```bash
# Headless (default) — no UI, pure automation (lowest token cost when using /text and filtered snapshots)
pinchtab &

# Headed — visible Chrome for human + agent workflows
BRIDGE_HEADLESS=false pinchtab &

# Dashboard/orchestrator — profile manager + launcher, no browser in dashboard process
pinchtab dashboard &
```

默认端口：`9867`。可以通过设置`BRIDGE_PORT=9868`来更改端口。
认证方式：设置`BRIDGE_TOKEN=<secret>`，并在请求头中添加`Authorization: Bearer <secret>`。

所有示例的基准URL为：`http://localhost:9867`。

Pinchtab的令牌消耗主要来自API请求（如`/text`和`/snapshot?filter=interactive&format=compact`），而非仅来自无头（headless）或有头（headed）浏览器模式。

### 有头模式（Headed Mode）说明

有头模式意味着Pinchtab会管理一个真实的、可见的Chrome浏览器窗口：
- 用户可以打开浏览器配置文件（profile），登录，完成两步验证（2FA）或验证码验证，并确认页面状态。
- 代理（agent）随后会通过Pinchtab的HTTP API与该浏览器实例进行交互。
- 会话状态会保存在浏览器配置文件中，因此后续操作可以重用已保存的cookies和数据。

在仪表板（dashboard）工作流程中，仪表板进程本身不会直接启动Chrome浏览器，而是会启动包含Chrome浏览器的配置文件实例（无论是有头模式还是无头模式）。

要从仪表板状态中获取正在运行的配置文件信息，请使用以下API：

```bash
pinchtab connect <profile-name>
```

**推荐的用户与代理交互流程：**

```bash
# human
pinchtab dashboard
# setup profile + launch profile instance

# agent
PINCHTAB_BASE_URL="$(pinchtab connect <profile-name>)"
curl "$PINCHTAB_BASE_URL/health"
```

## 配置文件管理（仪表板模式）

当运行`pinchtab dashboard`时，可以通过端口`9867`上的API来管理配置文件：

### 列出所有配置文件

```bash
curl http://localhost:9867/profiles
```

返回包含`id`、`name`、`accountEmail`等信息的配置文件列表。

### 通过ID启动配置文件

```bash
# Auto-allocate port (recommended)
curl -X POST http://localhost:9867/profiles/278be873adeb/start

# With specific port and headless mode
curl -X POST http://localhost:9867/profiles/278be873adeb/start \
  -H 'Content-Type: application/json' \
  -d '{"port": "9868", "headless": true}'

# Short alias (same behavior)
curl -X POST http://localhost:9867/start/278be873adeb
```

返回配置文件的详细信息，包括分配给该配置文件的端口。后续的所有API请求（如导航、截图、执行操作等）都应使用该端口。

### 通过ID停止配置文件

```bash
curl -X POST http://localhost:9867/profiles/278be873adeb/stop

# Short alias
curl -X POST http://localhost:9867/stop/278be873adeb
```

### 检查配置文件状态

```bash
# By profile ID (recommended)
curl http://localhost:9867/profiles/278be873adeb/instance

# By profile name (also works)
curl http://localhost:9867/profiles/Pinchtab%20org/instance
```

### 通过名称启动配置文件（仪表板风格）

```bash
curl -X POST http://localhost:9867/instances/launch \
  -H 'Content-Type: application/json' \
  -d '{"name": "work", "port": "9868"}'
```

### 代理的典型工作流程

```bash
# 1. List profiles to find the right one
PROFILES=$(curl -s http://localhost:9867/profiles)
# Pick the profile ID you need (12-char hex, e.g. "278be873adeb")

# 2. Start the profile (auto-allocates port)
INSTANCE=$(curl -s -X POST http://localhost:9867/profiles/$PROFILE_ID/start)
PORT=$(echo $INSTANCE | jq -r .port)

# 3. Use the instance (all API calls go to the instance port)
curl -X POST http://localhost:$PORT/navigate -H 'Content-Type: application/json' \
  -d '{"url": "https://mail.google.com"}'
curl http://localhost:$PORT/snapshot?maxTokens=4000

# 4. Check instance status
curl http://localhost:9867/profiles/$PROFILE_ID/instance

# 5. Stop when done
curl -s -X POST http://localhost:9867/profiles/$PROFILE_ID/stop
```

### 配置文件ID

每个配置文件都有一个固定的12位十六进制ID（基于其名称的SHA-256哈希值，经过截断），存储在`profile.json`文件中。该ID在创建配置文件时生成，之后不会更改。在自动化脚本中应使用ID而不是名称，因为ID在URL中是安全的且不会引起问题。

## 核心工作流程

代理的典型操作流程如下：
1. **导航**到目标URL。
2. **截取**页面的可访问性树数据（获取节点引用）。
3. **对节点进行操作**（如点击、输入、按键）。
4. **再次截取**可访问性树数据以查看操作结果。

节点引用（例如`e0`、`e5`、`e12`）会在每次截取后缓存到对应的标签页中——除非页面发生了显著变化，否则无需在每次操作前都重新截取。

## API参考

### 导航（Navigate）

```bash
curl -X POST http://localhost:9867/navigate \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com"}'

# With options: custom timeout, block images, open in new tab
curl -X POST http://localhost:9867/navigate \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "timeout": 60, "blockImages": true, "newTab": true}'
```

### 截取可访问性树数据（Snapshot）

```bash
# Full tree
curl http://localhost:9867/snapshot

# Interactive elements only (buttons, links, inputs) — much smaller
curl "http://localhost:9867/snapshot?filter=interactive"

# Limit depth
curl "http://localhost:9867/snapshot?depth=5"

# Smart diff — only changes since last snapshot (massive token savings)
curl "http://localhost:9867/snapshot?diff=true"

# Text format — indented tree, ~40-60% fewer tokens than JSON
curl "http://localhost:9867/snapshot?format=text"

# Compact format — one-line-per-node, 56-64% fewer tokens than JSON (recommended)
curl "http://localhost:9867/snapshot?format=compact"

# YAML format
curl "http://localhost:9867/snapshot?format=yaml"

# Scope to CSS selector (e.g. main content only)
curl "http://localhost:9867/snapshot?selector=main"

# Truncate to ~N tokens
curl "http://localhost:9867/snapshot?maxTokens=2000"

# Combine for maximum efficiency
curl "http://localhost:9867/snapshot?format=compact&selector=main&maxTokens=2000&filter=interactive"

# Disable animations before capture
curl "http://localhost:9867/snapshot?noAnimations=true"

# Write to file
curl "http://localhost:9867/snapshot?output=file&path=/tmp/snapshot.json"
```

返回一个扁平化的JSON数组，其中包含节点的`ref`、`role`、`name`、`depth`、`value`和`nodeId`等属性。

**令牌优化建议**：
- 使用`?format=compact`来提高令牌使用效率。
- 使用`?filter=interactive`可以减少返回的节点数量（适用于需要执行具体操作的场景）。
- 使用`?selector=main`来仅获取相关内容。
- 使用`?maxTokens=2000`来限制返回的数据量。
- 在多步骤操作中使用`?diff=true`仅显示页面的变化部分。

### 对元素进行操作（Act on Elements）

```bash
# Click by ref
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "click", "ref": "e5"}'

# Type into focused element (click first, then type)
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "click", "ref": "e12"}'
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "type", "ref": "e12", "text": "hello world"}'

# Press a key
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "press", "key": "Enter"}'

# Focus an element
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "focus", "ref": "e3"}'

# Fill (set value directly, no keystrokes)
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "fill", "selector": "#email", "text": "user@example.com"}'

# Hover (trigger dropdowns/tooltips)
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "hover", "ref": "e8"}'

# Select dropdown option (by value or visible text)
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "select", "ref": "e10", "value": "option2"}'

# Scroll to element
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "scroll", "ref": "e20"}'

# Scroll by pixels (infinite scroll pages)
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "scroll", "scrollY": 800}'

# Click and wait for navigation (link clicks)
curl -X POST http://localhost:9867/action \
  -H 'Content-Type: application/json' \
  -d '{"kind": "click", "ref": "e5", "waitNav": true}'
```

### 提取文本（Extract Text）

```bash
# Readability mode (default) — strips nav/footer/ads, keeps article/main content
curl http://localhost:9867/text

# Raw innerText (old behavior)
curl "http://localhost:9867/text?mode=raw"
```

返回`{url, title, text}`。这是最节省令牌的方法（大多数页面只需约1000个令牌）。

### 下载文件（Download Files）

```bash
# Download using browser session (preserves cookies, auth, stealth)
# Returns base64 JSON by default
curl "http://localhost:9867/download?url=https://site.com/report.pdf"

# Raw bytes (pipe to file)
curl "http://localhost:9867/download?url=https://site.com/image.jpg&raw=true" -o image.jpg

# Save directly to disk
curl "http://localhost:9867/download?url=https://site.com/export.csv&output=file&path=/tmp/export.csv"
```

主要用途是从已认证的网站下载文件。系统会自动使用浏览器的cookies和隐私设置，无需手动提取cookies或使用curl。

### 截取屏幕截图（Screenshot）

```bash
# Raw JPEG bytes
curl "http://localhost:9867/screenshot?raw=true" -o screenshot.jpg

# With quality setting (default 80)
curl "http://localhost:9867/screenshot?raw=true&quality=50" -o screenshot.jpg
```

### 评估JavaScript代码（Evaluate JavaScript）

```bash
curl -X POST http://localhost:9867/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "document.title"}'
```

### 标签页管理（Tab Management）

- 使用`?tabId=TARGET_ID`来截取特定标签页的数据、截图或提取文本；也可以在POST请求体中传递`"tabId"`。
- 多代理（multi-agent）环境下，可以使用`?tabId`参数来指定目标标签页。

### 标签页锁定（Tab Locking）

```bash
# Lock a tab (default 30s timeout, max 5min)
curl -X POST http://localhost:9867/tab/lock \
  -H 'Content-Type: application/json' \
  -d '{"tabId": "TARGET_ID", "owner": "agent-1", "timeoutSec": 60}'

# Unlock
curl -X POST http://localhost:9867/tab/unlock \
  -H 'Content-Type: application/json' \
  -d '{"tabId": "TARGET_ID", "owner": "agent-1"}'
```

被锁定的标签页会在`/tabs`目录中显示锁定者（owner）和锁定时间（lockedUntil）。如果多个代理尝试锁定同一标签页，会返回409错误。

### 批量操作（Batch Actions）

```bash
# Execute multiple actions in sequence
curl -X POST http://localhost:9867/actions \
  -H 'Content-Type: application/json' \
  -d '{"actions":[{"kind":"click","ref":"e3"},{"kind":"type","ref":"e3","text":"hello"},{"kind":"press","key":"Enter"}]}'

# Stop on first error (default: false, continues through all)
curl -X POST http://localhost:9867/actions \
  -H 'Content-Type: application/json' \
  -d '{"tabId":"TARGET_ID","actions":[...],"stopOnError":true}'
```

### 管理cookies（Manage Cookies）

```bash
# Get cookies for current page
curl http://localhost:9867/cookies

# Set cookies
curl -X POST http://localhost:9867/cookies \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","cookies":[{"name":"session","value":"abc123"}]}'
```

### 隐私设置（Stealth Settings）

```bash
# Check stealth status and score
curl http://localhost:9867/stealth/status

# Rotate browser fingerprint
curl -X POST http://localhost:9867/fingerprint/rotate \
  -H 'Content-Type: application/json' \
  -d '{"os":"windows"}'
# os: "windows", "mac", or omit for random
```

### 系统健康检查（Health Check）

```bash
curl http://localhost:9867/health
```

## 令牌消耗指南

| 方法 | 通常消耗的令牌数量 | 使用场景 |
|---|---|---|
| `/text` | 约800个令牌 | 用于读取页面内容 |
| `/snapshot?filter=interactive` | 约3600个令牌 | 用于查找可点击的按钮或链接 |
| `/snapshot?diff=true` | 数量因操作而异 | 适用于多步骤操作（仅显示变化部分） |
| `/snapshot?format=compact` | 约减少56-64%的令牌消耗 | 每个节点仅返回一行信息，提高效率 |
| `/snapshot?format=text` | 约减少40-60%的令牌消耗 | 以缩进格式显示节点信息，比普通JSON格式更节省令牌 |
| `/snapshot` | 约10500个令牌 | 用于获取完整页面信息 |
| `/screenshot` | 约2000个令牌 | 用于生成屏幕截图 |

**使用建议**：
- 首先使用`/snapshot?filter=interactive`进行操作。
- 在多步骤操作中，后续的截取请求可以使用`?diff=true`来避免重复获取相同的数据。
- 如果只需要可读内容，使用`/snapshot?format=text`。
- 仅在需要完整页面信息时使用`/snapshot`。

## 环境变量

### 核心运行参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `BRIDGE_BIND` | `127.0.0.1` | 默认绑定到本地主机（localhost）。设置为`0.0.0.0`以允许网络访问 |
| `BRIDGE_PORT` | `9867` | HTTP端口 |
| `BRIDGE_HEADLESS` | `true` | 以无头模式运行Chrome |
| `BRIDGE_TOKEN` | （未设置） | 使用`BRIDGE_BIND=0.0.0.0`时推荐使用令牌进行认证 |
| `BRIDGE_PROFILE` | `~/.pinchtab/chrome-profile` | Chrome配置文件的路径 |
| `BRIDGE_STATE_DIR` | `~/.pinchtab` | 会话数据存储目录 |
| `BRIDGE_NO_RESTORE` | `false` | 启动时不恢复之前的标签页状态 |
| `BRIDGE_STEALTH` | `light` | 隐私设置级别（`light`或`full`） |
| `BRIDGE_MAX_TABS` | `20` | 最大打开的标签页数量（0表示无限制） |
| `BRIDGE_BLOCK IMAGES` | `false` | 禁止加载图片 |
| `BRIDGE_BLOCK_MEDIA` | `false` | 禁止加载所有媒体内容（图片、字体、CSS、视频） |
| `BRIDGE_NO_ANIMATIONS` | `false` | 禁用CSS动画和过渡效果 |
| `BRIDGE_TIMEZONE` | （未设置） | 强制使用指定的浏览器时区（IANA时区） |
| `BRIDGE_CHROME_VERSION` | `144.0.7559.133` | 用于生成唯一标识的Chrome版本号 |
| `CHROME_binary` | （自动设置） | Chrome/Chromium二进制文件的路径 |
| `CHROME_FLAGS` | （未设置） | 额外的Chrome配置参数（以空格分隔） |
| `BRIDGE_CONFIG` | `~/.pinchtab/config.json` | 配置文件路径 |
| `BRIDGE_TIMEOUT` | `15` | 操作超时时间（秒） |
| `BRIDGE_NAV_TIMEOUT` | `30` | 导航超时时间（秒） |
| `CDP_URL` | （未设置） | 用于连接Chrome开发者工具 |
| `BRIDGE_NO_DASHBOARD` | `false` | 禁用仪表板相关功能 |

### 仪表板模式（`pinchtab dashboard`）

| 参数 | 默认值 | 说明 |
|---|---|---|
| `PINCHTAB_AUTO_LAUNCH` | `false` | 启动仪表板时是否自动启动默认配置文件 |
| `PINCHTAB_DEFAULT_PROFILE` | `default` | 自动启动的配置文件名称 |
| `PINCHTAB_DEFAULT_PORT` | `9867` | 自动启动配置文件使用的端口 |
| `PINCHTAB_HEADED` | （未设置） | 如果设置，则自动启动的有头模式配置文件；未设置则表示无头模式 |
| `PINCHTAB_DASHBOARD_URL` | `http://localhost:$BRIDGE_PORT` | `pinchtab connect`命令的基准URL |

## 使用提示：
- 在处理多个标签页时，请务必**明确指定`tabId`，因为活跃标签页的识别可能不可靠。
- 节点引用在多次截取和操作之间是稳定的，因此无需在每次操作前都重新截取页面。
- 在导航或页面发生重大变化后，应重新截取可访问性树数据以获取最新的节点引用。
- 建议默认使用`filter=interactive`模式；在需要完整页面信息时再使用`/snapshot`模式。
- Pinchtab会保存会话状态，因此标签页信息在重启后仍然可用（可以通过`BRIDGE_NO_RESTORE=true`禁用此功能）。
- Chrome配置文件在每次运行时都会保留，因此cookies和登录信息会持续保存。
- Chrome默认使用其内置的User-Agent字符串；`BRIDGE_CHROME_VERSION`仅用于生成唯一标识。
- 在需要大量读取数据的操作中，建议使用`BRIDGE_BLOCK IMAGES=true`或`"blockImages": true`来减少带宽和内存消耗。