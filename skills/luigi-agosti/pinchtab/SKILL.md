---
name: pinchtab
description: 通过 Pinchtab 的 HTTP API 来控制无头或有头的 Chrome 浏览器。该 API 可用于网页自动化、数据抓取、表单填写、导航以及多标签页工作流程。Pinchtab 以扁平化的 JSON 格式提供可访问性树（accessibility tree），并附带稳定的引用（refs），非常适合用于人工智能代理（AI agents）——具有较低的成本和较高的执行效率。适用于以下场景：浏览网站、填写表单、点击按钮、提取页面文本、截图，或任何基于浏览器的自动化操作。使用前需确保已启动 Pinchtab 实例（Go 语言编写的二进制程序）。
homepage: https://pinchtab.com
metadata:
  openclaw:
    emoji: "🦀"
    requires:
      bins: ["pinchtab"]
---
# Pinchtab

这是一个用于AI代理的快速、轻量级的浏览器控制工具，通过HTTP协议与浏览器的无头模式（headless mode）进行交互，并利用浏览器的无障碍功能（accessibility tree）来操作页面元素。

## 设置

确保Pinchtab已运行：

```bash
# Headless (default for automation)
BRIDGE_HEADLESS=true pinchtab &

# With UI (debugging)
pinchtab &
```

默认端口：`9867`。可以通过`BRIDGE_PORT=9868`进行修改。
认证方式：设置`BRIDGE_TOKEN=<secret>`，并在请求头中添加`Authorization: Bearer <secret>`。

所有示例的基准URL为：`http://localhost:9867`

## 核心工作流程

典型的代理操作流程包括：
1. **导航**到目标URL。
2. **获取当前页面的无障碍信息（即无障碍树结构）**。
3. **对页面元素执行操作（如点击、输入、按键）。
4. **再次获取无障碍信息以查看操作结果**。

每次获取无障碍信息后，相关引用（如`e0`、`e5`、`e12`等）会缓存在当前标签页中。除非页面发生了显著变化，否则无需在每次操作前都重新获取无障碍信息。

## API参考

### 导航（Navigate）

```bash
curl -X POST http://localhost:9867/navigate \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com"}'
```

### 获取无障碍信息（Snapshot）

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
```

该API返回一个包含节点信息的扁平JSON数组，其中包含以下字段：
- `ref`：节点的引用标识。
- `role`：节点的角色（如链接、按钮等）。
- `name`：节点的名称。
- `depth`：节点在无障碍树中的层级。
- `value`：节点的可见文本内容。
- `nodeId`：节点的唯一标识。

**令牌使用优化**：
- 使用`?filter=interactive`可以减少令牌使用量（约75%），适用于需要交互式操作的场景。
- 在多步骤操作中，使用`?diff=true`仅获取发生变化的部分。
- 使用`?format=text`可以获得结构化的输出，但会稍微增加令牌消耗。
- 只有在需要全面了解页面内容时，才使用完整的无障碍信息。

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

返回`{url, title, text}`，这是最节省令牌的使用方式（大多数页面只需约1K个令牌）。

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

- 使用`?tabId=TARGET_ID`来获取指定标签页的无障碍信息、截图或文本内容。
- 也可以在POST请求的请求体中传递`"tabId"`来指定目标标签页。

### 健康检查（Health Check）

```bash
curl http://localhost:9867/health
```

## 令牌成本指南

| 方法 | 通常需要的令牌数量 | 使用场景 |
|---|---|---|
| `/text` | 约800个令牌 | 读取页面内容 |
| `/snapshot?filter=interactive` | 约3,600个令牌 | 查找可点击的按钮/链接 |
| `/snapshot?diff=true` | 变化较大 | 多步骤操作，仅获取变化部分 |
| `/snapshot?format=text` | 比普通方式节省约40-60%的令牌 | 结构化输出 |
| `/snapshot` | 约10,500个令牌 | 全面了解页面内容 |
| `/screenshot` | 约2,000个令牌 | 用于视觉验证 |

**使用建议**：
- 首先使用`/snapshot?filter=interactive`进行交互式操作。
- 在多步骤操作中，后续请求使用`?diff=true`来获取仅发生变化的部分。
- 如果只需要可读内容，使用`/text`。
- 使用`?format=text`进一步降低令牌消耗。
- 只有在需要全面了解页面内容时，才使用`/snapshot`。

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `BRIDGE_PORT` | `9867` | HTTP端口 |
| `BRIDGE_HEADLESS` | `false` | 以无头模式运行Chrome浏览器 |
| `BRIDGE_TOKEN` | （未设置） | 用于认证的令牌 |
| `BRIDGE_PROFILE` | `~/.pinchtab/chrome-profile` | Chrome浏览器的配置文件路径 |
| `BRIDGE_STATE_DIR` | `~/.pinchtab` | 会话数据存储目录 |
| `BRIDGE_NO_RESTORE` | `false` | 启动时不恢复之前的标签页状态 |
| `CDP_URL` | （未设置） | 用于连接到现有的Chrome开发者工具 |

## 使用技巧：
- 不同操作之间的无障碍信息是稳定的，因此无需在点击前重新获取无障碍信息。
- 在导航或页面发生重大变化后，重新获取无障碍信息以获取最新的引用。
- 默认情况下使用`filter=interactive`；如有需要，可以使用完整的无障碍信息。
- Pinchtab会保留会话状态，因此重启后标签页信息会保留（通过`BRIDGE_NO_RESTORE=true`可以禁用此功能）。
- Chrome浏览器的配置文件和登录信息会在每次运行之间保持一致。