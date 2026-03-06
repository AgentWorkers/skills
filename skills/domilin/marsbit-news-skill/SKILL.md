---
name: marsbit-opennews
description: 通过 `marsbit-co` 中提供的 MCP 路由来获取 MarsBit 的新闻和动态数据。该服务支持最新的新闻查询、频道查找、关键词搜索、详细信息查询以及相关新闻和动态更新。
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["curl"]},"install":[{"id":"curl","kind":"brew","formula":"curl","label":"curl (HTTP client)"}],"os":["darwin","linux","win32"]},"version":"1.3.1"}
---
# MarsBit OpenNews 技能（可立即使用）

该技能设计为在安装完成后，通过托管的 MCP 端点立即生效。

MCP 端点：
- `https://www.marsbit.co/api/mcp`

在所有命令中均需使用此端点：

```bash
MCP_URL="https://www.marsbit.co/api/mcp"
```

## 运行时规则

当用户请求 MarsBit 新闻或突发新闻信息时，需通过 `curl` 直接调用 MCP 工具。

每个 MCP POST 请求所需的头部信息：
- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`
- `mcp-protocol-version: 2025-11-25`

响应解析：
- MCP 会将工具的输出封装在 `result.content[0].text` 中；
- `text` 是一个 JSON 字符串，在回答用户请求之前需要对其进行解析；
- 如果 `success` 的值为 `false`，则需向用户显示错误信息，并询问是否希望使用不同的参数重新尝试。

## 工具调用

### 1) 列出可用工具（快速连接性检查）

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

### 2) 获取新闻频道

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_news_channels","arguments":{}}}'
```

### 3) 获取最新新闻

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_latest_news","arguments":{"limit":10}}}'
```

### 4) 按关键词搜索新闻

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"search_news","arguments":{"keyword":"bitcoin","limit":10}}}'
```

### 5) 根据 ID 获取单条新闻详情

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_news_detail","arguments":{"news_id":"20260304151610694513"}}}'
```

### 6) 根据 ID 获取相关新闻

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"get_related_news","arguments":{"news_id":"20260304151610694513","limit":6}}}'
```

### 7) 获取最新的突发新闻

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"get_latest_flash","arguments":{"limit":10}}}'
```

### 8) 按关键词搜索突发新闻

```bash
curl -sS -X POST "$MCP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-protocol-version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"search_flash","arguments":{"keyword":"ETF","limit":10}}}'
```

## 操作意图与工具对应关系：

- 获取最新新闻 -> `get_latest_news`
- 获取新闻频道 -> `get_news_channels`
- 按关键词搜索新闻 -> `search_news`
- 获取单条新闻详情 -> `get_news_detail`
- 根据新闻 ID 获取相关新闻 -> `get_related_news`
- 获取最新的突发新闻 -> `get_latest_flash`
- 按关键词搜索突发新闻 -> `search_flash`

## 后端架构

该技能依赖于当前的 `marsbit-co` 托管 MCP 实现（`/api/mcp`），其内部使用了以下组件：
- `fetcher(..., { marsBit: true })`（位于 `src/lib/utils.ts` 中）
- 新闻相关 API：`/info/news/channels`, `/info/news/shownews`, `/info/news/getbyid`, `/info/news/v2/relatednews`
- 突发新闻相关 API：`/info/lives/showlives`
- 搜索 API：`/info/assist/querySimilarityInfo`（通过 `src/lib/db-marsbit/agent` 调用）

## ClawHub 上传路径

请将此文件夹直接上传至：
`marsbit-co/skills/opennews`

请勿上传其父目录。

## 从 GitHub 安装

当 ClawHub 无法使用时（例如因速率限制问题），您可以直接从 GitHub 安装此技能。

仓库地址：
`https://github.com/domilin/marsbit-news-skill`

**本地安装示例：**

```bash
git clone https://github.com/domilin/marsbit-news-skill /tmp/marsbit-news-skill
mkdir -p ~/.openclaw/skills/opennews
cp -R /tmp/marsbit-news-skill/openclaw-skill/opennews/* ~/.openclaw/skills/opennews/
openclaw skills list
```