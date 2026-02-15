---
name: x-apify
version: 1.0.3
description: 通过 Apify 的代理服务来获取 X/Twitter 的数据。支持搜索推文、获取用户资料以及检索带有回复的特定推文。系统具备本地缓存功能，以降低 API 调用的成本。用户可以通过 Apify 的代理基础设施从任意 IP 地址访问该服务。
tags: [twitter, x, apify, tweets, social-media, search, scraping, caching]
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":{"APIFY_API_TOKEN":{"required":true,"description":"Apify API token from https://console.apify.com/account/integrations"},"APIFY_ACTOR_ID":{"required":false,"default":"quacker~twitter-scraper","description":"Apify actor ID to use (default: quacker~twitter-scraper)"},"X_APIFY_CACHE_DIR":{"required":false,"description":"Custom cache directory (default: .cache/ in skill dir)"}}}}}
---

# x-apify

通过 Apify API 获取 X/Twitter 数据（搜索推文、用户资料、特定推文）。

## 为什么选择 Apify？

X/Twitter 的官方 API 使用成本较高且限制较多。Apify 通过其演员（actor）生态系统提供了对公开推文数据的可靠访问，并支持使用本地代理。

## 免费 tier

- **每月 5 美元的免费额度**（无需信用卡）
- 费用根据演员的使用情况而变化
- 非常适合个人使用

## 链接

- [Apify 定价](https://apify.com/pricing)
- [获取 API 密钥](https://console.apify.com/account/integrations)
- [Twitter Scraper 演员](https://apify.com/quacker/twitter-scraper)

## 设置

1. 创建免费的 Apify 账户：https://apify.com/
2. 获取您的 API 令牌：https://console.apify.com/account/integrations
3. 设置环境变量：

```bash
# Add to ~/.bashrc or ~/.zshrc
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN_HERE"

# Or use .env file (never commit this!)
echo 'APIFY_API_TOKEN=apify_api_YOUR_TOKEN_HERE' >> .env
```

## 使用方法

### 搜索推文

```bash
# Search for tweets containing keywords
python3 scripts/fetch_tweets.py --search "artificial intelligence"

# Search with hashtags
python3 scripts/fetch_tweets.py --search "#AI #MachineLearning"

# Limit results
python3 scripts/fetch_tweets.py --search "OpenAI" --max-results 10
```

### 用户资料

```bash
# Get tweets from a specific user
python3 scripts/fetch_tweets.py --user "elonmusk"

# Multiple users (comma-separated)
python3 scripts/fetch_tweets.py --user "OpenAI,AnthropicAI"
```

### 特定推文

```bash
# Get a specific tweet and its replies
python3 scripts/fetch_tweets.py --url "https://x.com/user/status/123456789"

# Also works with twitter.com URLs
python3 scripts/fetch_tweets.py --url "https://twitter.com/user/status/123456789"
```

### 输出格式

```bash
# JSON output (default)
python3 scripts/fetch_tweets.py --search "query" --format json

# Summary format (human-readable)
python3 scripts/fetch_tweets.py --search "query" --format summary

# Save to file
python3 scripts/fetch_tweets.py --search "query" --output results.json
```

### 缓存

默认情况下，推文会本地缓存以节省 API 费用。

```bash
# First request: fetches from Apify (costs credits)
python3 scripts/fetch_tweets.py --search "query"

# Second request: uses cache (FREE!)
python3 scripts/fetch_tweets.py --search "query"
# Output: [cached] Results for: query

# Bypass cache (force fresh fetch)
python3 scripts/fetch_tweets.py --search "query" --no-cache

# View cache stats
python3 scripts/fetch_tweets.py --cache-stats

# Clear all cached results
python3 scripts/fetch_tweets.py --clear-cache
```

缓存过期时间：
- 搜索结果：1 小时
- 用户资料：24 小时
- 特定推文：24 小时

缓存位置：`skill` 目录下的 `.cache/` 文件夹（可通过 `X_APIFY_CACHE_DIR` 环境变量进行自定义）

## 输出示例

### JSON 格式

```json
{
  "query": "OpenAI",
  "mode": "search",
  "fetched_at": "2026-02-11T10:30:00Z",
  "count": 20,
  "tweets": [
    {
      "id": "1234567890",
      "text": "OpenAI just announced...",
      "author": "techreporter",
      "author_name": "Tech Reporter",
      "created_at": "2026-02-11T09:00:00Z",
      "likes": 1500,
      "retweets": 300,
      "replies": 50,
      "url": "https://x.com/techreporter/status/1234567890"
    }
  ]
}
```

### 摘要格式

```
=== X/Twitter Search Results ===
Query: OpenAI
Fetched: 2026-02-11 10:30:00 UTC
Results: 20 tweets

---
@techreporter (Tech Reporter)
2026-02-11 09:00
OpenAI just announced...
[Likes: 1500 | RTs: 300 | Replies: 50]
https://x.com/techreporter/status/1234567890

---
...
```

## 错误处理

该脚本可以处理以下常见错误：
- 无效的搜索查询
- 未找到用户
- 未找到推文
- API 配额超出
- 网络错误

## 元数据

```yaml
metadata:
  openclaw:
    emoji: "X"
    requires:
      env:
        APIFY_API_TOKEN: required
        APIFY_ACTOR_ID: optional
        X_APIFY_CACHE_DIR: optional
      bins:
        - python3
```