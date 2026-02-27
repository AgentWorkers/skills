---
name: opennews
description: 通过 OpenNews 6551 API 提供加密货币新闻搜索、AI 评分、交易信号以及实时更新功能。支持关键词搜索、货币筛选、来源筛选、AI 评分排序以及 WebSocket 实时推送。

user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - OPENNEWS_TOKEN
      bins:
        - curl
    primaryEnv: OPENNEWS_TOKEN
    emoji: "\U0001F4F0"
    install:
      - id: curl
        kind: brew
        formula: curl
        label: curl (HTTP client)
    os:
      - darwin
      - linux
      - win32
  version: 1.0.0
---
# OpenNews：加密货币新闻功能

该功能通过6551平台的REST API查询加密货币新闻。所有接口均需要使用`$OPENNEWS_TOKEN`作为身份验证令牌。

**获取令牌**：https://6551.io/mcp

**基础URL**：`https://ai.6551.io`

## 身份验证

所有请求都必须包含以下请求头：
```
Authorization: Bearer $OPENNEWS_TOKEN
```

---

## 新闻操作

### 1. 获取新闻来源

获取所有可用的新闻来源类别，并按新闻来源类型进行分类。

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/news_type"
```

返回一个包含新闻来源类型（`news`、`listing`、`onchain`、`meme`、`market`）及其子类别的树状结构。

### 2. 搜索新闻

`POST /open/news_search`是主要的搜索接口。

**获取最新新闻**：
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'
```

**按关键词搜索**：
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"q": "bitcoin ETF", "limit": 10, "page": 1}'
```

**按货币符号搜索**：
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "limit": 10, "page": 1}'
```

**按新闻来源类型和新闻类型过滤**：
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"engineTypes": {"news": ["Bloomberg", "Reuters"]}, "limit": 10, "page": 1}'
```

**仅显示与货币相关的新闻**：
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hasCoin": true, "limit": 10, "page": 1}'
```

### 新闻搜索参数

| 参数            | 类型                | 是否必填 | 描述                                      |
|-----------------|------------------|---------|--------------------------------------------|
| `limit`          | 整数                | 是        | 每页显示的结果数量（1-100）                         |
| `page`          | 整数                | 是        | 页码（从1开始）                               |
| `q`            | 字符串                | 否        | 全文关键词搜索                               |
| `coins`          | 字符串数组            | 否        | 按货币符号过滤（例如：`["BTC","ETH"]`）                     |
| `engineTypes`     | 字符串数组            | 否        | 按新闻来源类型和新闻类型过滤                         |
| `hasCoin`        | 布尔值                | 否        | 仅返回与货币相关的新闻                         |

---

## 数据结构

### 新闻文章

```json
{
  "id": "unique-article-id",
  "text": "Article headline / content",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{"symbol": "BTC", "market_type": "spot", "match": "title"}],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "Chinese summary",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

---

## 常见操作流程

### 快速市场概览
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}' | jq '.data[] | {text, newsType, signal: .aiRating.signal}'
```

### 高影响力新闻（评分 >= 80）
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50, "page": 1}' | jq '[.data[] | select(.aiRating.score >= 80)]'
```

## 注意事项：

- 请在https://6551.io/mcp获取API令牌。
- 每次请求有请求速率限制，最多返回100条结果。
- 并非所有新闻都会附带AI评分（请检查`status`字段是否为`"done"`）。