---
name: apify
description: 运行 Apify 演员（网络爬虫、自动化工具），并通过 curl 使用 Apify REST API 获取其结果。当用户需要抓取网站内容、从网页中提取数据、运行 Apify 演员、爬取页面或从 Apify 数据集中获取结果时，可以使用此方法。
homepage: https://docs.apify.com/api/v2
metadata:
  {
    "openclaw":
      {
        "emoji": "🐝",
        "primaryEnv": "APIFY_TOKEN",
        "requires": { "anyBins": ["curl", "wget"], "env": ["APIFY_TOKEN"] },
      },
  }
---

# Apify

您可以在 [Apify 商店](https://apify.com/store) 中运行 17,000 多个可用的 Actor（自动化脚本），并通过 REST API 获取结构化的数据结果。

完整的 OpenAPI 规范：[openapi.json](openapi.json)

## 认证

所有请求都需要 `APIFY_TOKEN` 环境变量。请将其作为Bearer 令牌使用：

```bash
-H "Authorization: Bearer $APIFY_TOKEN"
```

基础 URL：`https://api.apify.com`

## 核心工作流程

### 1. 查找合适的 Actor

通过关键词在 Apify 商店中搜索所需的 Actor：

```bash
curl -s "https://api.apify.com/v2/store?search=web+scraper&limit=5" \
  -H "Authorization: Bearer $APIFY_TOKEN" | jq '.data.items[] | {name: (.username + "/" + .name), title, description}'
```

Actor 在 API 路径中通过 `username~name` 的格式进行标识，例如 `apify~web-scraper`。

### 2. 获取 Actor 的 README 文档和输入格式

在运行 Actor 之前，先获取其默认构建版本，以获取 README 文档（使用说明）和输入格式（预期的 JSON 字段）：

```bash
curl -s "https://api.apify.com/v2/acts/apify~web-scraper/builds/default" \
  -H "Authorization: Bearer $APIFY_TOKEN" | jq '.data | {readme, inputSchema}'
```

`inputSchema` 是一个 JSON 格式的对象——请解析它以了解所需/可选的字段、类型、默认值和描述。使用这些信息来构建有效的输入数据。

您还可以获取 Actor 的每个构建版本的 OpenAPI 规范（无需认证）：

```bash
curl -s "https://api.apify.com/v2/acts/apify~web-scraper/builds/default/openapi.json"
```

### 3. 运行 Actor（建议使用异步方式）

启动 Actor 并立即获取运行结果：

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":10}'
```

响应中包含 `data.id`（运行 ID）、`data.defaultDatasetId` 和 `data.status`。

可选的查询参数：`?timeout=300&memory=4096&maxItems=100&waitForFinish=60`

- `waitForFinish`（0-60）：API 在返回结果前等待的秒数。这对于避免对短时间运行的任务进行频繁轮询非常有用。

### 4. 轮询运行状态

```bash
curl -s "https://api.apify.com/v2/actor-runs/RUN_ID?waitForFinish=60" \
  -H "Authorization: Bearer $APIFY_TOKEN" | jq '.data | {status, defaultDatasetId}'
```

终端状态：`SUCCEEDED`（成功）、`FAILED`（失败）、`ABORTED`（中止）、`TIMED-OUT`（超时）。

### 5. 获取结果

**数据集项**（最常见的方式——结构化的抓取数据）：

```bash
curl -s "https://api.apify.com/v2/datasets/DATASET_ID/items?clean=true&limit=100" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

或者直接通过运行结果获取数据（更快捷的方法，参数相同）：

```bash
curl -s "https://api.apify.com/v2/actor-runs/RUN_ID/dataset/items?clean=true&limit=100" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

参数：`format`（`json`|`csv`|`jsonl`|`xml`|`xlsx`|`rss`）、`fields`、`omit`、`limit`、`offset`、`clean`、`desc`。

**键值存储记录**（截图、HTML、OUTPUT）：

```bash
curl -s "https://api.apify.com/v2/key-value-stores/STORE_ID/records/OUTPUT" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

**运行日志**：

```bash
curl -s "https://api.apify.com/v2/logs/RUN_ID" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

### 6. 同步运行 Actor（仅适用于运行时间较短的 Actor）

对于运行时间在 300 秒以内的 Actor，可以通过一次调用获取所有数据集项：

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/run-sync-get-dataset-items?timeout=120" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":5}'
```

直接返回数据集项数组（不会被封装在 `data` 对象中）。如果运行时间超过 300 秒，将返回 `408` 状态码。

另一种方式是使用 `/run-sync` 来获取 KVS（键值存储）中的输出记录，而不是数据集项。

## 快速操作指南

### 抓取网站内容

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/run-sync-get-dataset-items?timeout=120" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":20}'
```

### 在 Google 上进行搜索

```bash
curl -s -X POST "https://api.apify.com/v2/acts/apify~google-search-scraper/run-sync-get-dataset-items?timeout=120" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"queries":"site:example.com openai","maxPagesPerQuery":1}'
```

### 长时间运行的 Actor（异步执行并需要轮询）

```bash
# 1. Start
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/apify~web-scraper/runs?waitForFinish=60" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"https://example.com"}],"maxPagesPerCrawl":500}')
RUN_ID=$(echo "$RUN" | jq -r '.data.id')

# 2. Poll until done
while true; do
  STATUS=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" \
    -H "Authorization: Bearer $APIFY_TOKEN" | jq -r '.data.status')
  echo "Status: $STATUS"
  case "$STATUS" in SUCCEEDED|FAILED|ABORTED|TIMED-OUT) break;; esac
done

# 3. Fetch results
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?clean=true" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

### 中止运行

```bash
curl -s -X POST "https://api.apify.com/v2/actor-runs/RUN_ID/abort" \
  -H "Authorization: Bearer $APIFY_TOKEN"
```

## 收费/租赁型 Actor

某些 Actor 需要订阅才能使用。如果 API 返回权限或支付错误，请让用户通过 Apify 控制台手动订阅：

```
https://console.apify.com/actors/ACTOR_ID
```

请将 `ACTOR_ID` 替换为实际的 Actor ID（例如 `AhEsMsQyLfHyMLaxz`）。用户需要在该页面上点击 **Start** 以激活订阅。大多数租赁型 Actor 都提供开发者设定的免费试用期。

您可以从商店搜索结果（`data.items[].id`）或通过 `GET /v2/acts/username~name`（返回 `data.id`）获取 Actor ID。

## 错误处理

- **401**：`APIFY_TOKEN` 缺失或无效。
- **404**：未找到 Actor：请检查 `username~name` 的格式（使用波浪号 `~`，而非斜杠 `/`）。请访问 https://apify.com/store 查看可用 Actor。
- **400**：运行失败：请查看 `GET /v2/logs/RUN_ID` 以获取详细信息。
- **402/403**：需要支付费用：该 Actor 可能需要订阅。请参考上述的 “收费/租赁型 Actor” 部分。
- **408**：运行超时：同步请求有 300 秒的限制，请改用异步方式。
- **429**：达到速率限制：请使用指数级退避策略重试（首次尝试间隔 500 毫秒，每次尝试间隔加倍）。

## 其他资源

- API 文档（适合大型语言模型使用）：https://docs.apify.com/api/v2.md
- OpenAPI 规范：[openapi.json](openapi.json)
- Apify 商店（浏览可用 Actor）：https://apify.com/store