---
name: opengraph-io
version: 1.4.0
description: "通过 OpenGraph.io 提取网页数据、捕获截图、抓取内容并生成 AI 图像。适用于处理 URL（解析、预览、元数据）、捕获网页截图、抓取 HTML 内容、查询网页信息或生成图像（图表、图标、社交卡片、二维码）等场景。可用命令包括：`get the OG tags`（获取原始标签）、`screenshot this page`（截图此页面）、`scrape this URL`（抓取此 URL 的内容）、`generate a diagram`（生成图表）、`create a social card`（创建社交卡片）、`what does this page say about`（此页面内容是什么）。"
homepage: https://www.opengraph.io
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["curl"],"env":["OPENGRAPH_APP_ID"]},"primaryEnv":"OPENGRAPH_APP_ID","install":[{"id":"mcp","kind":"npm","package":"opengraph-io-mcp","global":true,"bins":["opengraph-io-mcp"],"label":"Install MCP server (optional, for other AI clients)"}]}}
---

# OpenGraph.io

![OpenGraph.io - 提取数据、截图、抓取网页内容、查询信息、生成图像](https://raw.githubusercontent.com/securecoders/opengraph-io-skill/main/examples/opengraph-hero.jpg)

通过 OpenGraph.io 的 API，您可以提取网页数据、捕获截图，并生成由 AI 支持的图像。

> 🤖 **AI 代理：** 如需完整的参数文档和使用模式，请参阅 [references/for-ai-agents.md](references/for-ai-agents.md)。

---

## 快速决策指南

### “我需要从某个 URL 获取数据”
| 需求 | API 端点 |
|------|----------|
| 元数据/链接预览 | `GET /site/{url}` |
| 原始 HTML 内容 | `GET /scrape/{url}` （如被地理限制，请添加 `use_proxy=true`） |
| 特定元素（h1、h2、p） | `GET /extract/{url}?html_elements=h1,h2,p` |
| 关于该页面的 AI 回答 | `POST /query/{url}` ⚠️ 需付费 |
| 视觉截图 | `GET /screenshot/{url}` |

### “我需要生成一张图片”
| 需求 | 设置选项 |
|------|----------|
| 技术图表 | `kind: "diagram"` — 可使用 `diagramCode` 和 `diagramFormat` 进行自定义 |
| 应用图标/徽标 | `kind: "icon"` — 设置 `transparent: true` |
| 社交媒体卡片（OG/Twitter 格式） | `kind: "social-card"` — 使用 `aspectRatio: "og-image"` |
| 基本二维码 | `kind: "qr-code"` |
| **高级二维码营销卡片** | `kind: "illustration"` — 在提示中描述完整设计 |
| 通用插图 | `kind: "illustration"` |

### 二维码：基础版与高级版

**基础版（`kind: "qr-code"`）**：仅生成功能性的二维码。

**高级版（`kind: "illustration"`）**：生成包含二维码的完整营销素材，支持专业设计（渐变效果、3D 元素、呼叫行动按钮、设备模拟图等）。示例提示：
```
"Premium marketing card with QR code for https://myapp.com, cosmic purple gradient 
with floating 3D spheres, glowing accents, 'SCAN TO DOWNLOAD' call-to-action"
```

### 图表生成技巧
- 使用 `diagramCode` 和 `diagramFormat` 可确保语法正确（避免 AI 生成错误）
- 对于结构要求严格的图表，请使用 `outputStyle: "standard"`（高级版可能会改变布局）
- 注意：不要在描述中混合使用语法，例如 `"graph LR A-->B make it pretty"` 会导致错误

---

## 价格与使用要求

| 功能 | 免费套餐 | 付费套餐 |
|---------|-----------|------------|
| 网站内容提取 | ✅ 每月 100 元 | 无限次 |
| 截图 | ✅ 每月 100 元 | 无限次 |
| 网页抓取 | ✅ 每月 100 元 | 无限次 |
| 数据提取 | ✅ 每月 100 元 | 无限次 |
| 查询（AI 功能） | ❌ | ✅ |
| **图像生成** | ✅ 每月 4 元 | 无限次 |

> 💡 **免费试用图像生成！** 免费套餐每月可生成 4 张高级图像——无需信用卡。

请在 [dashboard.opengraph.io](https://dashboard.opengraph.io/register) 注册。

## 快速设置

1. 在 [dashboard.opengraph.io](https://dashboard.opengraph.io/register) 注册（提供免费试用）
2. 进行配置（选择以下选项之一）：

**选项 A：Clawdbot 配置**（推荐）
```json5
// ~/.clawdbot/clawdbot.json
{
  skills: {
    entries: {
      "opengraph-io": {
        apiKey: "YOUR_APP_ID"
      }
    }
  }
}
```

**选项 B：环境变量配置**
```bash
export OPENGRAPH_APP_ID="YOUR_APP_ID"
```

---

## Clawdbot 使用方法（REST API）

使用 `curl` 并设置 `OPENGRAPH_APP_ID` 环境变量。基础 URL：`https://opengraph.io/api/1.1/`

### 提取 OpenGraph 数据（网站内容）

```bash
# Get OG tags from a URL
curl -s "https://opengraph.io/api/1.1/site/$(echo -n 'https://example.com' | jq -sRr @uri)?app_id=${OPENGRAPH_APP_ID}"
```

响应包含 `hybridGraph.title`、`hybridGraph.description`、`hybridGraph.image` 等信息。

### 截取网页截图

```bash
# Capture screenshot (dimensions: sm, md, lg, xl)
curl -s "https://opengraph.io/api/1.1/screenshot/$(echo -n 'https://example.com' | jq -sRr @uri)?app_id=${OPENGRAPH_APP_ID}&dimensions=lg"
```

响应格式：`{"screenshotUrl": "https://..." }`

### 抓取 HTML 内容

```bash
# Fetch rendered HTML (with optional proxy)
curl -s "https://opengraph.io/api/1.1/scrape/$(echo -n 'https://example.com' | jq -sRr @uri)?app_id=${OPENGRAPH_APP_ID}&use_proxy=true"
```

### 提取特定元素

```bash
# Pull h1, h2, p tags
curl -s "https://opengraph.io/api/1.1/extract/$(echo -n 'https://example.com' | jq -sRr @uri)?app_id=${OPENGRAPH_APP_ID}&html_elements=h1,h2,p"
```

### 查询页面信息（使用 AI）

```bash
curl -s -X POST "https://opengraph.io/api/1.1/query/$(echo -n 'https://example.com' | jq -sRr @uri)?app_id=${OPENGRAPH_APP_ID}" \
  -H "Content-Type: application/json" \
  -d '{"query": "What services does this company offer?"}'
```

---

## 图像生成（REST API）

基础 URL：`https://opengraph.io/image-agent/`

### 第一步：创建会话

```bash
SESSION=$(curl -s -X POST "https://opengraph.io/image-agent/sessions?app_id=${OPENGRAPH_APP_ID}" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-session"}')
SESSION_ID=$(echo $SESSION | jq -r '.sessionId')
```

### 第二步：生成图像

```bash
curl -s -X POST "https://opengraph.io/image-agent/sessions/${SESSION_ID}/generate?app_id=${OPENGRAPH_APP_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful QR code linking to https://example.com with modern gradient design",
    "kind": "qr-code",
    "aspectRatio": "square",
    "quality": "high"
  }'
```

**图像类型：** `illustration`、`diagram`、`icon`、`social-card`、`qr-code`

**样式预设：** `github-dark`、`vercel`、`stripe`、`neon-cyber`、`pastel`、`minimal-mono`

**宽高比：** `square`、`og-image`（1200×630）、`twitter-card`、`instagram-story` 等

### 第三步：下载生成的图像

```bash
ASSET_ID="<from-generate-response>"
curl -s "https://opengraph.io/image-agent/assets/${ASSET_ID}/file?app_id=${OPENGRAPH_APP_ID}" -o output.png
```

### 第四步：优化图像（可选）

```bash
curl -s -X POST "https://opengraph.io/image-agent/sessions/${SESSION_ID}/iterate?app_id=${OPENGRAPH_APP_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "assetId": "<previous-asset-id>",
    "prompt": "Change the background to blue"
  }'
```

---

## 自然语言指令示例

当用户使用自然语言提出请求时，可转换为相应的 API 调用：

| 用户指令 | 使用的 API |
|-----------|------------|
| “从 URL 获取元数据” | `GET /site/{url}` |
| “截取该页面的截图” | `GET /screenshot/{url}` |
| “抓取该页面的 HTML 内容” | `GET /scrape/{url}` |
| “这个页面关于 X 的内容是什么？” | `POST /query/{url}` |
| “为该 URL 生成二维码” | `POST /image-agent/sessions/{id}/generate` 且 `kind: "qr-code"` |
| “为我的博客创建一张高级二维码营销卡片” | `POST /image-agent/sessions/{id}/generate` 且 `kind: "illustration"` 并提供设计描述 |
| “为我的博客创建一张社交媒体卡片” | `POST /image-agent/sessions/{id}/generate` 且 `kind: "social-card"` |
| “生成一张架构图” | `POST /image-agent/sessions/{id}/generate` 且 `kind: "diagram"` |

### 二维码选项

**基础二维码（`kind: "qr-code"`）**：仅生成功能性的二维码。

**高级二维码营销卡片（`kind: "illustration"`）**：生成包含二维码的完整营销素材，支持专业设计（渐变效果、3D 元素、呼叫行动按钮、设备模拟图等）。

```bash
# Premium QR marketing card example
curl -s -X POST "https://opengraph.io/image-agent/sessions/${SESSION_ID}/generate?app_id=${OPENGRAPH_APP_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Premium marketing card with QR code for https://myapp.com, cosmic purple gradient background with floating 3D spheres, glowing accents, SCAN TO DOWNLOAD call-to-action",
    "kind": "illustration",
    "aspectRatio": "square",
    "outputStyle": "premium",
    "brandColors": ["#6B4CE6", "#9B6DFF"],
    "stylePreferences": "modern, cosmic, premium marketing, 3D elements"
  }'
```

---

## MCP 集成（适用于 Claude Desktop、Cursor 等 AI 工具）

对于支持 MCP 的 AI 工具，可使用 MCP 服务器：

```bash
# Interactive installer
npx opengraph-io-mcp --client cursor --app-id YOUR_APP_ID

# Or configure manually:
{
  "mcpServers": {
    "opengraph": {
      "command": "npx",
      "args": ["-y", "opengraph-io-mcp"],
      "env": {
        "OPENGRAPH_APP_ID": "YOUR_APP_ID"
      }
    }
  }
}
```

具体集成方法请参阅 [references/mcp-clients.md](references/mcp-clients.md)。

## 更多信息

- [references/for-ai-agents.md](references/for-ai-agents.md) — AI 代理使用指南（工具架构、决策流程、使用模式）
- [references/api-reference.md](references/api-reference.md) — 完整的 API 文档（所有端点、参数、响应格式）
- [references/platform-support.md](references/platform-support.md) — 平台支持指南（YouTube、Vimeo、TikTok、社交媒体、电子商务平台）
- [references/troubleshooting.md](references/troubleshooting.md) — 故障排除指南（常见问题及调试技巧）
- [references/image-generation.md](references/image-generation.md) — 图像样式、模板设置
- [references/mcp-clients.md](references/mcp-clients.md) — MCP 客户端配置指南