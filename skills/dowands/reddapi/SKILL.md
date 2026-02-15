---
name: reddapi
description: 使用此技能，您可以通过 reddapi.dev API 访问 Reddit 的完整数据档案。该工具支持语义搜索、子版块发现以及实时趋势分析功能，非常适合用于市场研究、竞争分析以及特定领域机会的挖掘。
license: MIT
keywords:
  - reddit
  - api
  - search
  - market-research
  - niche-discovery
  - social-media
---

# reddapi.dev 技能

## 概述

通过 reddapi.dev 强大的 API，您可以访问 **Reddit 的完整数据档案**。该技能提供了语义搜索、子版块发现和趋势分析功能。

## 主要特性

### 🔍 语义搜索
支持在数百万 Reddit 帖子和评论中进行自然语言搜索。

```bash
# Search for user pain points
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "best productivity tools for remote teams", "limit": 100}'

# Find complaints and frustrations
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "frustrations with current TOOL_NAME", "limit": 100}'
```

### 📊 趋势分析 API
可以发现具有互动指标的热门话题。

```bash
# Get trending topics
curl "https://reddapi.dev/api/v1/trends" \
  -H "Authorization: Bearer $REDDAPI_API_KEY"
```

响应内容包括：
- `post_count`：帖子数量
- `total_upvotes`：互动得分
- `avg_sentiment`：情感分析结果（-1 到 1）
- `trending_keywords`：热门关键词
- `growth_rate`：趋势热度

### 📝 子版块发现

```bash
# List popular subreddits
curl "https://reddapi.dev/api/subreddits?limit=100" \
  -H "Authorization: Bearer $REDDAPI_API_KEY"

# Get specific subreddit info
curl "https://reddapi.dev/api/subreddits/programming" \
  -H "Authorization: Bearer $REDDAPI_API_KEY"
```

## 使用场景

### 市场研究
```bash
# Analyze competitor discussions
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "COMPETITOR problems complaints", "limit": 200}'
```

### 小众领域探索
```bash
# Find underserved user needs
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "I wish there was an app that", "limit": 100}'
```

### 趋势分析
```bash
# Monitor topic growth
curl "https://reddapi.dev/api/v1/trends" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for trend in data.get('data', {}).get('trends', []):
    print(f\"{trend['topic']}: {trend['growth_rate']}% growth\")
"
```

## 响应格式

### 搜索结果
```json
{
  "success": true,
  "results": [
    {
      "id": "post123",
      "title": "User post title",
      "selftext": "Post content...",
      "subreddit": "r/somesub",
      "score": 1234,
      "num_comments": 89,
      "created_utc": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 15000
}
```

### 趋势分析结果
```json
{
  "success": true,
  "data": {
    "trends": [
      {
        "topic": "AI regulation",
        "post_count": 1247,
        "total_upvotes": 45632,
        "avg_sentiment": 0.42,
        "growth_rate": 245.3
      }
    ]
  }
}
```

## 环境变量

```bash
export REDDAPI_API_KEY="your_api_key"
```

您可以在以下链接获取 API 密钥：https://reddapi.dev

## 相关技能

- **niche-hunter**：自动机会发现工具
- **market-analysis**：全面的研究工作流程