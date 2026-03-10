---
name: apify-bluesky-scraper
description: 通过 AT 协议抓取 Bluesky 的社交帖子。适用于用户需要搜索 Bluesky、查找 Bluesky 帖子、监控 Bluesky 讨论或提取 Bluesky 数据的场景。使用该功能时需要设置 `APIFY_TOKEN` 环境变量。
metadata: {"openclaw":{"emoji":"🦋","requires":{"env":["APIFY_TOKEN"],"bins":["curl","jq"]},"primaryEnv":"APIFY_TOKEN"}}
---
# Bluesky Scraper

使用 Apify 演员（Actor）通过 REST API 抓取 Bluesky 的帖子。

## 演员 ID
`WAJfBnZBYR9mJrk5d`

## 先决条件
- 必须设置 `APIFY_TOKEN` 环境变量
- 确保 `curl` 和 `jq` 已安装并可用

## 工作流程

### 第 1 步：与用户确认搜索参数
询问用户想要搜索的内容。支持的输入字段：
- `searchTerms`（字符串数组）- 要搜索的关键词
- `maxResults`（整数）- 返回的最大帖子数量（默认值：50）
- `sortBy`（字符串）- “relevance” 或 “latest”

### 第 2 步：运行演员（同步操作）
```bash
RESULT=$(curl -s -X POST "https://api.apify.com/v2/acts/WAJfBnZBYR9mJrk5d/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["SEARCH_TERM"], "maxResults": 50, "sortBy": "relevance"}')
echo "$RESULT" | jq '.'
```

对于大规模任务（异步操作）：
```bash
RUN_ID=$(curl -s -X POST "https://api.apify.com/v2/acts/WAJfBnZBYR9mJrk5d/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["TERM"], "maxResults": 50}' | jq -r '.data.id')
```

### 第 3 步：轮询并获取数据（如果采用异步操作）
```bash
STATUS=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | jq -r '.data.status')
# Poll every 5s until SUCCEEDED or FAILED
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN" | jq '.'
```

### 第 4 步：展示结果
汇总搜索结果：总帖子数量、按互动量排序的帖子、常见主题。支持导出为 JSON 或 CSV 格式。

## 错误处理
- 如果未设置 `APIFY_TOKEN`：`export APIFY_TOKEN=your_token`
- 如果任务执行失败：`curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID/log?token=$APIFY_TOKEN"`
- 遇到速率限制（429 错误）：等待 60 秒后重试