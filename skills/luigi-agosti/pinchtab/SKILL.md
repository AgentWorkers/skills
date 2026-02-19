---
name: pinchtab
description: 通过 Pinchtab 的 HTTP API 来控制无头或有头的 Chrome 浏览器。该 API 可用于网页自动化、数据抓取、表单填写、导航以及多标签页操作。Pinchtab 将浏览器的可访问性树（accessibility tree）以扁平化的 JSON 格式提供，并附带稳定的引用信息，非常适合人工智能代理使用（低请求成本、快速响应）。适用于以下场景：浏览网站、填写表单、点击按钮、提取页面文本、截图，或任何基于浏览器的自动化任务。使用前需确保已启动 Pinchtab 实例（Go 语言编写的二进制程序）。
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
        - name: BRIDGE_BLOCK_IMAGES
          optional: true
          description: "Block image loading for faster, lower-bandwidth browsing (true/false)"
        - name: BRIDGE_BLOCK_MEDIA
          optional: true
          description: "Block all media: images + fonts + CSS + video (true/false)"
        - name: BRIDGE_NO_ANIMATIONS
          optional: true
          description: "Disable CSS animations/transitions globally (true/false)"
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
---
# Pinchtab

这是一个专为AI代理设计的快速、轻量级的浏览器控制工具，通过HTTP协议与浏览器的无障碍功能（accessibility tree）进行交互。

## 设置

确保Pinchtab已运行：

```bash
# Headless (default for automation)
BRIDGE_HEADLESS=true pinchtab &

# With UI (debugging)
pinchtab &
```

默认端口：`9867`。可以通过设置`BRIDGE_PORT=9868`来更改端口。
认证：设置`BRIDGE_TOKEN=<secret>`，并在请求头中添加`Authorization: Bearer <secret>`进行身份验证。

所有示例的基URL为：`http://localhost:9867`

## 核心工作流程

典型的代理操作流程包括：
1. **导航**到目标URL
2. **获取当前页面的无障碍功能树信息（即访问权限树）**
3. **对页面元素进行操作（如点击、输入、按键等）**
4. **再次获取无障碍功能树信息以查看操作结果**

每次操作后，相关引用（如`e0`、`e5`、`e12`等）会被缓存到当前标签页中。除非页面发生了显著变化，否则无需在每次操作前都重新获取这些引用。

## API参考

### 导航

```bash
curl -X POST http://localhost:9867/navigate \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com"}'

# With options: custom timeout, block images, open in new tab
curl -X POST http://localhost:9867/navigate \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "timeout": 60, "blockImages": true, "newTab": true}'
```

### 获取无障碍功能树信息（snapshot）

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

该API返回一个扁平化的JSON数组，其中包含节点的以下属性：`ref`、`role`、`name`、`depth`、`value`、`nodeId`。

**令牌使用优化**：
- 使用`?format=compact`可提高令牌使用效率。
- 使用`?filter=interactive`可仅获取交互式元素的信息（从而减少返回的节点数量，约减少75%）。
- 使用`?selector=main`可仅获取页面中的主要内容。
- 使用`?maxTokens=2000`可限制返回的节点数量。
- 在多步骤操作中，使用`?diff=true`仅获取页面的变化部分。

### 对元素进行操作

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

### 提取文本

```bash
# Readability mode (default) — strips nav/footer/ads, keeps article/main content
curl http://localhost:9867/text

# Raw innerText (old behavior)
curl "http://localhost:9867/text?mode=raw"
```

该API返回`{url, title, text}`，这是最节省令牌的使用方式（大多数页面只需约1000个令牌）。

### 截取屏幕截图

```bash
# Raw JPEG bytes
curl "http://localhost:9867/screenshot?raw=true" -o screenshot.jpg

# With quality setting (default 80)
curl "http://localhost:9867/screenshot?raw=true&quality=50" -o screenshot.jpg
```

### 评估JavaScript代码的执行结果

```bash
curl -X POST http://localhost:9867/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"expression": "document.title"}'
```

### 标签页管理

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

- 要对特定标签页执行操作，可以在请求参数中传递`?tabId=TARGET_ID`；或者在POST请求体中包含`"tabId"`。
- 被锁定的标签页会在 `/tabs` 中显示其所有者（`owner`）和锁定时间（`lockedUntil`）。如果尝试访问被锁定的标签页，会收到409错误。
- `?tabId=TARGET_ID`可用于获取该标签页的截图、文本或执行其他操作。

### 多代理协同（multi-agent）

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

在多代理环境中，可以使用`?tabId=TARGET_ID`来操作指定标签页。

### 标签页锁定机制

```bash
# Execute multiple actions in sequence
curl -X POST http://localhost:9867/actions \
  -H 'Content-Type: application/json' \
  -d '[{"kind":"click","ref":"e3"},{"kind":"type","ref":"e3","text":"hello"},{"kind":"press","key":"Enter"}]'
```

- 被锁定的标签页的信息会存储在 `/tabs` 中，包括锁定者（`owner`）和锁定时间（`lockedUntil`）。
- 如果尝试访问被锁定的标签页，会收到409错误。

### 批量操作

```bash
# Execute multiple actions in sequence
curl -X POST http://localhost:9867/actions \
  -H 'Content-Type: application/json' \
  -d '[{"kind":"click","ref":"e3"},{"kind":"type","ref":"e3","text":"hello"},{"kind":"press","key":"Enter"}]'
```

### 管理cookies

```bash
# Get cookies for current page
curl http://localhost:9867/cookies

# Set cookies
curl -X POST http://localhost:9867/cookies \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","cookies":[{"name":"session","value":"abc123"}]}'
```

### 隐秘模式（stealth mode）

```bash
# Check stealth status and score
curl http://localhost:9867/stealth/status

# Rotate browser fingerprint
curl -X POST http://localhost:9867/fingerprint/rotate \
  -H 'Content-Type: application/json' \
  -d '{"os":"windows"}'
# os: "windows", "mac", or omit for random
```

- 可通过设置`BRIDGE_STEALTH`来启用或禁用隐秘模式（`light`或`full`）。

### 健康检查

```bash
curl http://localhost:9867/health
```

## 令牌使用成本指南

| API方法 | 通常需要的令牌数量 | 使用场景 |
|---|---|---|
| `/text` | 约800个令牌 | 读取页面内容 |
| `/snapshot?filter=interactive` | 约3,600个令牌 | 查找可点击的按钮/链接 |
| `/snapshot?diff=true` | 数量因操作步骤而异 | 仅获取页面变化部分 |
| `/snapshot?format=compact` | 约减少56-64%的令牌使用量 | 每个节点仅返回一行信息，效率最高 |
| `/snapshot?format=text` | 约减少40-60%的令牌使用量 | 以缩进格式显示节点信息，比JSON格式更节省令牌 |
| `/snapshot` | 约10,500个令牌 | 获取页面的完整信息 |
| `/screenshot` | 约2,000个令牌 | 截取页面截图 |
| `/evaluateJavaScript` | 根据操作步骤而定 | 评估JavaScript代码的执行结果 |

**使用建议**：
- 首先使用`/snapshot?filter=interactive`来获取页面的基本信息。
- 在多步骤操作中，后续的请求可以使用`?diff=true`来获取仅有的变化部分。
- 如果只需要可读内容，可以使用`/text`。
- 如果需要获取页面的完整信息，可以使用`/snapshot`。

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `BRIDGE_PORT` | `9867` | HTTP端口 |
| `BRIDGE_HEADLESS` | `false` | 以无头模式运行Chrome浏览器 |
| `BRIDGE_TOKEN` | （未设置时为空） | 用于身份验证的令牌 |
| `BRIDGE_PROFILE` | `~/.pinchtab/chrome-profile` | Chrome浏览器的配置文件路径 |
| `BRIDGE_STATE_DIR` | `~/.pinchtab` | 用于存储会话信息的目录 |
| `BRIDGE_NO_RESTORE` | `false` | 启动时不恢复之前的标签页状态 |
| `BRIDGE_STEALTH` | `light` | 隐秘模式级别（`light`或`full`） |
| `BRIDGE_BLOCK-images` | `false` | 禁止加载图片 |
| `BRIDGE_BLOCK_MEDIA` | `false` | 禁止加载所有媒体内容（图片、字体、CSS、视频） |
| `BRIDGE_NO_ANIMATIONS` | `false` | 禁用CSS动画和过渡效果 |
| `CHROME_BINARY` | （自动设置） | Chrome/Chromium的二进制文件路径 |
| `CHROME_FLAGS` | （未设置时为空） | 额外的Chrome浏览器参数 |
| `BRIDGE_CONFIG` | `~/.pinchtab/config.json` | 配置文件路径 |
| `BRIDGE_TIMEOUT` | `15` | 操作超时时间（秒） |
| `BRIDGE_NAV_TIMEOUT` | `30` | 导航超时时间（秒） |
| `CDP_URL` | （未设置时为空） | 连接到Chrome开发者工具 |

## 使用技巧：
- 在处理多个标签页时，务必明确传递`tabId`，因为默认情况下标签页的跟踪可能不准确。
- 每次操作后，无障碍功能树信息是稳定的，因此无需在每次点击前都重新获取。
- 在导航或页面发生重大变化后，重新获取无障碍功能树信息以获取最新的引用。
- 默认情况下使用`filter=interactive`；如有需要，可以使用`full snapshot`。
- Pinchtab会保留用户的会话状态，因此重启后标签页信息仍会保留（可以通过`BRIDGE_NO_RESTORE=true`来禁用此功能）。
- Chrome浏览器的配置信息会持久保存，因此cookie和登录状态会在重启后继续保留。
- Chrome默认使用其内置的用户代理（User-Agent），`BRIDGE_CHROME_VERSION`仅用于更改用户代理的字符串格式。
- 在需要大量读取页面内容时，可以使用`BRIDGE_BLOCK IMAGES=true`或`"blockImages": true`来减少带宽和内存消耗。