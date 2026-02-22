---
name: pinchtab
description: 通过 Pinchtab 的 HTTP API 来控制无头或有头的 Chrome 浏览器。该 API 可用于网页自动化、数据抓取、表单填写、导航以及多标签页操作。Pinchtab 以扁平化的 JSON 格式提供可访问性树（accessibility tree），并附带稳定的引用信息，非常适合 AI 代理使用（低请求成本、快速响应）。适用于以下场景：浏览网站、填写表单、点击按钮、提取页面文本、截图，或任何基于浏览器的自动化任务。使用前需确保已启动 Pinchtab 实例（Go 语言编写的二进制程序）。
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

这是一个用于AI代理的快速、轻量级的浏览器控制工具，通过HTTP和可访问性树（accessibility tree）实现功能。

## 设置

可以通过以下方式启动Pinchtab：

```bash
# Headless (default) — no UI, pure automation (lowest token cost when using /text and filtered snapshots)
pinchtab &

# Headed — visible Chrome for human + agent workflows
BRIDGE_HEADLESS=false pinchtab &

# Dashboard/orchestrator — profile manager + launcher, no browser in dashboard process
pinchtab dashboard &
```

默认端口：`9867`。可以通过`BRIDGE_PORT=9868`进行修改。
认证：设置`BRIDGE_TOKEN=<secret>`，并在请求头中添加`Authorization: Bearer <secret>`。

所有示例的基准URL为：`http://localhost:9867`

Token的节省主要来自于API请求（如`/text`、`/snapshot?filter=interactive&format=compact`），而不是仅仅通过无头（headless）或有头（headed）模式。

### 有头模式（Headed Mode）定义

有头模式意味着Pinchtab会管理一个真正可见的Chrome窗口：

- 用户可以打开配置文件（profile）、登录、通过双因素认证（2FA）/验证码，并验证页面状态。
- 代理随后会针对同一个运行的配置文件实例调用Pinchtab的HTTP API。
- 会话状态会保存在配置文件目录中，因此后续运行可以重用cookie和存储的数据。

在仪表板工作流程中，仪表板进程本身不会启动Chrome；它会启动运行Chrome的配置文件实例（无论是有头模式还是无头模式）。

要从仪表板状态中获取正在运行的配置文件端点，请使用以下方法：

```bash
pinchtab connect <profile-name>
```

推荐的用户与代理交互流程：

```bash
# human
pinchtab dashboard
# setup profile + launch profile instance

# agent
PINCHTAB_BASE_URL="$(pinchtab connect <profile-name>)"
curl "$PINCHTAB_BASE_URL/health"
```

## 配置文件管理（仪表板模式）

运行`pinchtab dashboard`时，可以通过端口9867上的仪表板API来管理配置文件。

### 列出配置文件

```bash
curl http://localhost:9867/profiles
```

返回包含`id`、`name`、`accountEmail`、`useWhen`等信息的配置文件数组。

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

返回配置文件的实例信息，其中包含分配的`port`。后续的所有API调用（如导航、截图、执行操作等）都应使用该端口。

### 通过ID停止配置文件

```bash
curl -X POST http://localhost:9867/profiles/278be873adeb/stop

# Short alias
curl -X POST http://localhost:9867/stop/278be873adeb
```

### 检查配置文件实例状态

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

每个配置文件都会获得一个稳定的12位十六进制ID（名称的SHA-256哈希值，经过截断），存储在`profile.json`文件中。该ID在创建时生成，之后不会更改。在自动化脚本中应使用ID而不是名称，因为ID既安全又易于处理URL。

## 核心工作流程

代理的典型工作流程包括：

1. **导航**到某个URL。
2. **截取**可访问性树的快照（获取元素引用）。
3. **对元素执行操作**（如点击、输入、按键）。
4. **再次截取快照**以查看结果。

元素引用（例如`e0`、`e5`、`e12`）会在每次截取后缓存到对应的标签页中——除非页面发生了显著变化，否则无需在每次操作前都重新截取快照。

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

### 截取快照（可访问性树）

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

返回一个扁平化的JSON数组，其中包含节点的`ref`、`role`、`name`、`depth`、`value`、`nodeId`等属性。

**Token优化**：
- 使用`?format=compact`可以获得更高的Token效率。
- 使用`?filter=interactive`可以减少节点数量（约75%）。
- 使用`?selector=main`可以仅获取相关内容。
- 使用`?maxTokens=2000`可以限制输出结果的数量。
- 在多步骤工作流程中使用`?diff=true`仅显示变化部分。

### 对元素执行操作（Act on Elements）

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

返回`{url, title, text}`。这是最节省Token的方法（大多数页面只需约1K个Token）。

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

主要用途：从已认证的网站下载文件。系统会自动使用浏览器的cookie和隐身设置，无需手动提取cookie或使用curl。

### 上传文件（Upload Files）

```bash
# Upload a local file to a file input
curl -X POST "http://localhost:9867/upload?tabId=TAB_ID" \
  -H "Content-Type: application/json" \
  -d '{"selector": "input[type=file]", "paths": ["/tmp/photo.jpg"]}'

# Upload base64-encoded data
curl -X POST "http://localhost:9867/upload" \
  -H "Content-Type: application/json" \
  -d '{"selector": "#avatar-input", "files": ["data:image/png;base64,iVBOR..."]}'

# Combine both — local files + base64
curl -X POST "http://localhost:9867/upload" \
  -H "Content-Type: application/json" \
  -d '{"selector": "input[type=file]", "paths": ["/tmp/doc.pdf"], "files": ["data:image/png;base64,..."]}'
```

可以通过CDP（Content Delivery Protocol）将文件上传到`<input type=file>`元素。浏览器会触发`change`事件，就像用户手动选择了文件一样。如果省略了选择器，系统会默认使用`input[type=file]`。支持base64数据URL、原始的base64字符串和本地文件路径。

### 截取屏幕截图（Screenshot）

```bash
# Raw JPEG bytes
curl "http://localhost:9867/screenshot?raw=true" -o screenshot.jpg

# With quality setting (default 80)
curl "http://localhost:9867/screenshot?raw=true&quality=50" -o screenshot.jpg
```

### 评估JavaScript（Evaluate JavaScript）

```bash
curl -X POST http://localhost:9867/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "document.title"}'
```

### 标签页管理（Tab Management）

```bash
# List tabs
curl http://localhost:9867/tabs

# Open new tab
curl -X POST http://localhost:9867/tab \
  -H 'Content-Type: application/json' \
  -d '{"action": "new", "url": "https://example.com"}'

# Close tab
curl -X POST http://localhost:9867/tab \
  -H 'Content-Type: application/json' \
  -d '{"action": "close", "tabId": "TARGET_ID"}'
```

多标签页操作：在截取快照/截图/提取文本时，可以通过`?tabId=TARGET_ID`传递目标标签页的ID；或者在POST请求体中传递`"tabId"`。

### 标签页锁定（Tab Locking, Multi-Agent）

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

被锁定的标签页会在`/tabs`中显示`owner`和`lockedUntil`信息。如果存在冲突，会返回409状态码。

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

### Cookie（Cookies）

```bash
# Get cookies for current page
curl http://localhost:9867/cookies

# Set cookies
curl -X POST http://localhost:9867/cookies \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","cookies":[{"name":"session","value":"abc123"}]}'
```

### 隐身模式（Stealth）

```bash
# Check stealth status and score
curl http://localhost:9867/stealth/status

# Rotate browser fingerprint
curl -X POST http://localhost:9867/fingerprint/rotate \
  -H 'Content-Type: application/json' \
  -d '{"os":"windows"}'
# os: "windows", "mac", or omit for random
```

### 健康检查（Health Check）

```bash
curl http://localhost:9867/health
```

## Token成本指南

| 方法 | 典型Token消耗 | 使用场景 |
|---|---|---|
| `/text` | 约800个Token | 用于读取页面内容 |
| `/snapshot?filter=interactive` | 约3,600个Token | 用于查找可点击的按钮/链接 |
| `/snapshot?diff=true` | 变化较大 | 多步骤工作流程（仅显示变化部分） |
| `/snapshot?format=compact` | 减少约56-64%的Token消耗 | 每个节点仅输出一行内容，提高Token效率 |
| `/snapshot?format=text` | 减少约40-60%的Token消耗 | 以缩进格式显示节点内容，比普通JSON更节省Token |
| `/snapshot` | 约10,500个Token | 用于全面理解页面内容 |
| `/screenshot` | 约2,000个Token | 用于视觉验证 |

**使用建议**：
- 首先使用`/snapshot?filter=interactive`进行快照获取。
- 在多步骤任务中，后续快照可以使用`?diff=true`来减少Token消耗。
- 如果只需要可读内容，可以使用`/text`。
- 如果需要全面了解页面内容，可以使用完整的`/snapshot`。

## 环境变量

### 核心运行参数

| 变量 | 默认值 | 说明 |
|---|---|---|
| `BRIDGE_BIND` | `127.0.0.1` | 绑定地址，默认为本地主机。设置为`0.0.0.0`以允许网络访问 |
| `BRIDGE_PORT` | `9867` | HTTP端口 |
| `BRIDGE_HEADLESS` | `true` | 以无头模式运行Chrome |
| `BRIDGE_TOKEN` | （无默认值） | 身份验证Token（建议在`BRIDGE_BIND=0.0.0.0`时使用） |
| `BRIDGE_PROFILE` | `~/.pinchtab/chrome-profile` | Chrome配置文件目录 |
| `BRIDGE_STATE_DIR` | `~/.pinchtab` | 会话状态存储目录 |
| `BRIDGE_NO_RESTORE` | `false` | 启动时跳过标签页恢复 |
| `BRIDGE_STEALTH` | `light` | 隐身模式级别（`light`或`full`） |
| `BRIDGE_MAX_TABS` | `20` | 最大打开的标签页数量（0表示无限） |
| `BRIDGE_BLOCK_IMAGES` | `false` | 阻止图片加载 |
| `BRIDGE_BLOCK_MEDIA` | `false` | 阻止所有媒体（图片、字体、CSS、视频）的加载 |
| `BRIDGE_NO_ANIMATIONS` | `false` | 禁用CSS动画/过渡效果 |
| `BRIDGE_TIMEZONE` | （无默认值） | 强制设置浏览器时区（IANA时区） |
| `BRIDGE_CHROME_VERSION` | `144.0.7559.133` | 用于指纹识别的Chrome版本 |
| `CHROME_binary` | （自动设置） | Chrome/Chromium二进制文件路径 |
| `CHROME_FLAGS` | （无默认值） | 额外的Chrome配置参数（以空格分隔） |
| `BRIDGE_CONFIG` | `~/.pinchtab/config.json` | 配置文件路径 |
| `BRIDGE_TIMEOUT` | `15` | 操作超时时间（秒） |
| `BRIDGE_NAV_TIMEOUT` | `30` | 导航超时时间（秒） |
| `CDP_URL` | （无默认值） | 连接到现有的Chrome DevTools |
| `BRIDGE_NO_DASHBOARD` | `false` | 禁用实例进程上的仪表板/协调端点 |

### 仪表板模式（`pinchtab dashboard`）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PINCHTAB_AUTO_LAUNCH` | `false` | 仪表板启动时自动启动默认配置文件 |
| `PINCHTAB_DEFAULT_PROFILE` | `default` | 自动启动的配置文件名称 |
| `PINCHTAB_DEFAULT_PORT` | `9867` | 自动启动配置文件的端口 |
| `PINCHTAB_HEADED` | （未设置） | 如果设置，则自动启动的有头模式配置文件；未设置则表示无头模式 |
| `PINCHTAB_DASHBOARD_URL` | `http://localhost:$BRIDGE_PORT` | `pinchtab connect`命令的CLI辅助URL |

## 使用技巧：

- 在处理多个标签页时，**务必明确传递`tabId**——因为活动标签页的跟踪可能不可靠。
- 元素引用在快照和操作之间是稳定的，因此无需在点击前重新截取快照。
- 在导航或页面发生重大变化后，重新截取快照以获取最新的元素引用。
- 默认情况下使用`filter=interactive`；如有需要，可以使用完整的快照。
- Pinchtab会保留会话状态——标签页在重启后仍然可用（可以通过`BRIDGE_NO_RESTORE=true`禁用此功能）。
- Chrome配置文件是持久化的——cookie和登录信息会在运行之间保留。
- Chrome默认使用其内置的User-Agent；`BRIDGE_CHROME_VERSION`仅影响指纹识别机制。
- 对于数据量较大的操作，建议使用`BRIDGE_BLOCK IMAGES=true`或`"blockImages": true`来减少带宽和内存消耗。