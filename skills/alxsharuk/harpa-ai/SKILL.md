---
name: harpa-grid
description: 通过 HARPA AI Grid REST API，可以自动化操作网页浏览器、抓取网页内容、在互联网上搜索信息，并在实时运行的网站上执行人工智能（AI）指令。
user-invocable: true
homepage: https://harpa.ai/grid/web-automation
metadata: {"openclaw":{"emoji":"🌐","requires":{"anyBins":["curl","wget"],"env":["HARPA_API_KEY"]},"primaryEnv":"HARPA_API_KEY","homepage":"https://harpa.ai/grid/web-automation","skillKey":"harpa-grid"}}
---
# HARPA Grid — 浏览器自动化 API

HARPA Grid 允许您远程操控真实的网页浏览器。您可以通过单一的 REST 端点来抓取页面内容、搜索网页、运行内置或自定义的 AI 命令，以及发送包含完整页面上下文的 AI 提示。

## 前提条件

用户 **必须** 满足以下要求：
1. 从 https://harpa.ai 安装了 **HARPA AI Chrome 扩展程序**。
2. 至少有一个正在运行的 Node（即安装了 HARPA 扩展程序的浏览器，并在扩展程序的 AUTOMATE 标签页中进行了配置）。
3. 拥有 **HARPA API 密钥**，该密钥可通过扩展程序的 AUTOMATE 标签页获取，密钥以 `HARPA_API_KEY` 环境变量的形式提供。

如果用户尚未设置 HARPA，请引导他们访问：https://harpa.ai/grid/browser-automation-node-setup

## API 参考

**端点：** `POST https://api.harpa.ai/api/v1/grid`
**认证：** `Authorization: Bearer $HARPA_API_KEY`
**内容类型：** `application/json`

完整参考文档：https://harpa.ai/grid/grid-rest-api-reference

---

## 功能操作

### 1. 抓取网页内容

通过 CSS/XPath/文本选择器提取整个页面的内容或特定元素。

**抓取整个页面内容：**

```bash
curl -s -X POST https://api.harpa.ai/api/v1/grid \
  -H "Authorization: Bearer $HARPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "scrape",
    "url": "https://example.com",
    "timeout": 15000
  }'
```

**抓取目标元素：**

```bash
curl -s -X POST https://api.harpa.ai/api/v1/grid \
  -H "Authorization: Bearer $HARPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "scrape",
    "url": "https://example.com/products",
    "grab": [
      {
        "selector": ".product-title",
        "selectorType": "css",
        "at": "all",
        "take": "innerText",
        "label": "titles"
      },
      {
        "selector": ".product-price",
        "selectorType": "css",
        "at": "all",
        "take": "innerText",
        "label": "prices"
      }
    ],
    "timeout": 15000
  }'
```

**提取字段：**

| 字段 | 是否必填 | 默认值 | 可选值 |
|-------|---------|---------|--------|
| selector | 是 | — | CSS（`.class`、`#id`）、XPath（`//h2`）或文本内容 |
| selectorType | 否 | auto | `auto`、`css`、`xpath`、`text` |
| at | 否 | first | `all`、`first`、`last` 或一个数字 |
| take | 否 | innerText | `innerText`、`textContent`、`innerHTML`、`outerHTML`、`href`、`value`、`id`、`className`、`attributes`、`styles`、`[attrName]`、`(styleName)` |
| label | 否 | data | 提取数据的自定义标签 |

### 2. 搜索网页（SERP）

执行网页搜索，支持 `site:`、`intitle:` 等操作符。

```bash
curl -s -X POST https://api.harpa.ai/api/v1/grid \
  -H "Authorization: Bearer $HARPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "serp",
    "query": "OpenClaw AI agent framework",
    "timeout": 15000
  }'
```

### 3. 运行 AI 命令

在目标页面上执行 100 多种内置的 HARPA 命令或自定义自动化脚本。

```bash
curl -s -X POST https://api.harpa.ai/api/v1/grid \
  -H "Authorization: Bearer $HARPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "command",
    "url": "https://example.com/article",
    "name": "Extract data",
    "inputs": "List all headings with their word counts",
    "connection": "HARPA AI",
    "resultParam": "message",
    "timeout": 30000
  }'
```

- `name` — 命令名称（例如：“Summary”、“Extract data”或任何自定义命令）
- `inputs` — 多步骤命令的预填充用户输入
- `resultParam` — 作为结果返回的 HARPA 参数（默认值：“message”）
- `connection` — 要使用的 AI 模型（例如：“HARPA AI”、“gpt-4o”、“claude-3.5-sonnet”）

### 4. 发送 AI 提示

发送包含页面上下文的自定义 AI 提示。可以使用 `{{page}}` 变量来插入页面内容。

```bash
curl -s -X POST https://api.harpa.ai/api/v1/grid \
  -H "Authorization: Bearer $HARPA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "prompt",
    "url": "https://example.com",
    "prompt": "Analyze the current page and extract all contact information. Webpage: {{page}}",
    "connection": "CHAT AUTO",
    "timeout": 30000
  }'
```

---

## 常用参数

| 参数 | 是否必填 | 默认值 | 说明 |
|-----------|---------|---------|-------------|
| action | 是 | — | `scrape`、`serp`、`command` 或 `prompt` |
| url | 否 | — | 目标页面 URL（`serp` 功能会忽略该参数） |
| node | 否 | — | 节点 ID（例如：“r2d2”）、多个节点（例如：“r2d2 c3po”）、前 N 个节点（例如：“5”）或所有节点（例如：“*”） |
| timeout | 否 | 300000 | 最大等待时间（以毫秒为单位，最长 5 分钟） |
| resultsWebhook | 否 | — | 异步发送结果的 URL（结果会保留 30 天） |
| connection | 否 | — | `command`/`prompt` 操作所使用的 AI 模型 |

## 节点定位

- 省略 `node` 参数将使用默认节点。
- `"node": "mynode"` — 按 ID 定位特定节点。
- `"node": "node1 node2"` — 定位多个节点。
- `"node": "3"` — 使用前 3 个可用节点。
- `"node": "*"` — 向所有节点发送请求。

## 通过 Webhook 异步接收结果

设置 `resultsWebhook` 以异步接收结果。该操作的有效期为 30 天，适用于目标节点暂时离线的情况。

```json
{
  "action": "scrape",
  "url": "https://example.com",
  "resultsWebhook": "https://your-server.com/webhook",
  "timeout": 15000
}
```

## 提示

- 由于 HARPA 在真实的浏览器会话中运行，并使用用户的 cookie 和认证状态，因此可以抓取需要登录才能访问的页面内容。
- 使用包含多个选择器的 `grab` 数组，在单次请求中提取结构化数据。
- 对于耗时较长的 AI 命令，可以增加 `timeout`（最长 300000 毫秒 / 5 分钟），或使用 `resultsWebhook`。
- `{{page}}` 变量用于在提示中插入页面内容，为 AI 提供当前页面的上下文信息。