---
name: opentwitter
description: 通过 6551 API 获取 Twitter/X 的数据。支持用户资料、推文搜索、用户发布的推文、关注者事件、已删除的推文以及 KOL（关键意见领袖）的关注者信息。

user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - TWITTER_TOKEN
      bins:
        - curl
    primaryEnv: TWITTER_TOKEN
    emoji: "\U0001F426"
    install:
      - id: curl
        kind: brew
        formula: curl
        label: curl (HTTP client)
    os:
      - darwin
      - linux
      - win32
---
# Twitter/X 数据操作技能

您可以通过 6551 平台的 REST API 查询 Twitter/X 数据。所有接口都需要使用 `$TWITTER_TOKEN` 作为 Bearer 令牌进行身份验证。

**获取您的令牌**：https://6551.io/mcp

**基础 URL**：`https://ai.6551.io`

## 身份验证

所有请求都必须包含以下头部信息：
```
Authorization: Bearer $TWITTER_TOKEN
```

---

## Twitter 操作

### 1. 获取 Twitter 用户信息

通过用户名获取用户资料。

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_info" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk"}'
```

### 2. 通过 ID 获取 Twitter 用户

通过用户 ID 获取用户资料。

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_by_id" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"userId": "44196397"}'
```

### 3. 获取用户的推文

获取用户的最新推文。

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "maxResults": 20, "product": "Latest"}'
```

| 参数              | 类型     | 默认值    | 描述                                      |
|------------------|---------|---------|-----------------------------------------|
| `username`        | string   | 必填     | Twitter 用户名（不含 @ 符号）                     |
| `maxResults`       | integer  | 20       | 最多返回的推文数量（1-100 条）                     |
| `product`         | string   | "Latest"  | "Latest" 或 "Top"                          |
| `includeReplies`     | boolean  | false     | 是否包含回复推文                         |
| `includeRetweets`    | boolean  | false     | 是否包含转推推文                         |

### 4. 搜索 Twitter 内容

使用多种过滤器搜索推文。

**从特定用户开始搜索**：
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fromUser": "VitalikButerin", "maxResults": 20}'
```

**按标签搜索**：
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashtag": "crypto", "minLikes": 100, "maxResults": 20}'
```

### Twitter 搜索参数

| 参数              | 类型     | 默认值    | 描述                                      |
|------------------|---------|---------|-----------------------------------------|
| `keywords`        | string   | -       | 搜索关键词                               |
| `fromUser`        | string   | -       | 从特定用户开始搜索的推文                     |
| `toUser`         | string   | -       | 发送给特定用户的推文                     |
| `mentionUser`      | string   | -       | 提及特定用户的推文                     |
| `hashtag`         | string   | -       | 按标签过滤（不含 # 符号）                     |
| `excludeReplies`    | boolean  | false     | 不包含回复推文                         |
| `excludeRetweets`    | boolean  | false     | 不包含转推推文                         |
| `minLikes`        | integer  | 0       | 最小点赞数阈值                         |
| `minRetweets`       | integer  | 0       | 最小转推数阈值                         |
| `minReplies`       | integer  | 0       | 最少回复数阈值                         |
| `sinceDate`       | string   | -       | 开始搜索的日期（格式：YYYY-MM-DD）                 |
| `untilDate`       | string   | -       | 结束搜索的日期（格式：YYYY-MM-DD）                 |
| `lang`            | string   | -       | 语言代码（例如：en, zh）                         |
| `product`         | string   | "Top"    | "Top" 或 "Latest"                          |
| `maxResults`       | integer  | 20       | 最多返回的推文数量（1-100 条）                     |

### 5. 获取用户的关注者/被关注者变化

获取用户的新关注者或被关注者的信息。

```bash
# Get new followers
curl -s -X POST "https://ai.6551.io/open/twitter_follower_events" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "isFollow": true, "maxResults": 20}'

# Get unfollowers
curl -s -X POST "https://ai.6551.io/open/twitter_follower_events" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "isFollow": false, "maxResults": 20}'
```

| 参数              | 类型     | 默认值    | 描述                                      |
|------------------|---------|---------|------------------------------------------|
| `username`        | string   | 必填     | Twitter 用户名（不含 @ 符号）                     |
| `isFollow`         | boolean  | true     | true 表示新关注者，false 表示被关注者                |
| `maxResults`       | integer  | 20       | 最多返回的事件数量（1-100 条）                     |

### 6. 获取用户的已删除推文

获取用户删除的推文。

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_deleted_tweets" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "maxResults": 20}'
```

| 参数              | 类型     | 默认值    | 描述                                      |
|------------------|---------|---------|-----------------------------------------|
| `username`        | string   | 必填     | Twitter 用户名（不含 @ 符号）                     |
| `maxResults`       | integer  | 20       | 最多返回的已删除推文数量（1-100 条）                     |

### 7. 获取用户关注的 KOL（关键意见领袖）

获取用户所关注的 KOL（Key Opinion Leaders）。

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_kol_followers" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk"}'
```

| 参数              | 类型     | 默认值    | 描述                                      |
|------------------|---------|---------|------------------------------------------|
| `username`        | string   | 必填     | Twitter 用户名（不含 @ 符号）                     |

---

## 数据结构

### Twitter 用户信息

```json
{
  "userId": "44196397",
  "screenName": "elonmusk",
  "name": "Elon Musk",
  "description": "...",
  "followersCount": 170000000,
  "friendsCount": 500,
  "statusesCount": 30000,
  "verified": true
}
```

### 推文信息

```json
{
  "id": "1234567890",
  "text": "Tweet content...",
  "createdAt": "2024-02-20T12:00:00Z",
  "retweetCount": 1000,
  "favoriteCount": 5000,
  "replyCount": 200,
  "userScreenName": "elonmusk",
  "hashtags": ["crypto", "bitcoin"],
  "urls": [{"url": "https://..."}]
}
```

---

## 常见工作流程

### 搜索加密货币相关的 KOL 推文
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "VitalikButerin", "maxResults": 10}'
```

### 热门加密货币推文
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "bitcoin", "minLikes": 1000, "product": "Top", "maxResults": 20}'
```

## 注意事项：

- 请在 https://6551.io/mcp 获取您的 API 令牌。
- 每次请求有速率限制，最多返回 100 条结果。
- Twitter 用户名中不应包含 @ 符号。