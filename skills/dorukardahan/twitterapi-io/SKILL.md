---
name: twitterapi-io
description: 通过 TwitterAPI.io 与 Twitter/X 进行交互：搜索推文、获取用户信息、发布推文、点赞、转发、关注、发送私信等。涵盖了所有 59 个 API 端点。适用于用户需要读取或写入 Twitter 数据的场景。
metadata:
  version: 3.2.0
  updated: 2026-02-13
  author: dorukardahan
---
# TwitterAPI.io 技能 v3.1.0

通过 [TwitterAPI.io](https://twitterapi.io) 的 REST API 访问 Twitter/X 数据并执行相关操作。
API 有两个版本：**v1（已弃用）** 和 **v2（当前推荐版本）**。

文档：https://docs.twitterapi.io | 控制面板：https://twitterapi.io/dashboard

---

## 设置

1. 获取 API 密钥：https://twitterapi.io/dashboard（免费信用额度 0.10 美元，无需信用卡）
2. 将密钥存储在 `.env` 文件中或 shell 的安全配置文件中（切勿在终端中使用 `export` 命令直接输出密钥——否则密钥会保存在终端历史记录中）。
3. 对于写操作，您还需要 v2 登录时生成的 `login_cookies` 以及专用的住宅代理（residential proxy）。

基础 URL：`https://api.twitterapi.io`
认证头部：`X-API-Key: $TWITTERAPI_IO_KEY`（所有请求均需添加）

---

## 价格（基于信用额度，1 美元 = 100,000 信用额度）

| 资源 | 信用额度 | 大约价格（每 1,000 信用额度） |
|----------|---------|-------------|
| 推文（每条返回的推文） | 15 | 0.15 美元 |
| 个人资料（每个返回的个人资料） | 18 | 0.18 美元 |
| 100 个以上个人资料（每个个人资料） | 10 | 0.10 美元 |
| 关注者（每个返回的关注者） | 15 | 0.15 美元 |
| 验证关注者（每个关注者） | 30 | 0.30 美元 |
| 每次 API 调用最低费用 | 15 | 0.00015 美元 |
| 列出端点调用 | 150 | 0.0015 美元 |
| 检查关注关系 | 100 | 0.001 美元 |
| 获取文章 | 100 | 0.001 美元 |
| 写操作（发推文、点赞、转发、关注） | 200-300 | 0.002-0.003 美元 |
| 登录 | 300 | 0.003 美元 |

注意：即使 API 返回 0 或 1 条数据，仍会收取最低费用（15 信用额度）。

---

## QPS（速率限制）——基于账户余额

| 账户余额（信用额度） | QPS 限制 |
|---------------------------|-----------|
| < 1,000（免费 tier） | 每 5 秒 1 次请求 |
| >= 1,000 | 每秒 3 次请求 |
| >= 5,000 | 每秒 6 次请求 |
| >= 10,000 | 每秒 10 次请求 |
| >= 50,000 | 每秒 20 次请求 |

---

## V1 与 V2 端点对比

| 功能 | V1（已弃用） | V2（当前版本） |
|---------|-----------------|--------------|
| 登录 | `/twitter/login_by_email_or_username` + `/twitter/login_by_2fa` | `/twitter/user_login_v2` |
| 发推文 | `/twitter/create_tweet` | `/twitter/create_tweet_v2` |
| 点赞 | `/twitter/like_tweet` | `/twitter/like_tweet_v2` |
| 转发 | `/twitter/retweet_tweet` | `/twitter/retweet_tweet_v2` |
| 上传图片 | `/twitter/upload_image` | `/twitter/upload_media_v2` |
| 认证参数 | `auth_session` | `login_cookies` |
| 价格 | 每次调用 0.001 美元 | 每次调用 0.002-0.003 美元 |

**V1 的 `login_cookies` 无法与 V2 端点一起使用，反之亦然。请始终使用 V2 版本。**

### `login_cookie` 与 `login_cookies` 的命名不一致性问题

API 在命名上存在不一致：
- `user_login_v2` 的 **响应** 中返回的字段名为 `login_cookie`（单数形式）
- 所有 V2 的 **操作** 端点要求字段名为 `login_cookies`（复数形式）

**在请求体中始终使用 `login_cookies`（复数形式）。** 两个字段的值是相同的字符串。

---

## 响应结构

### 推文对象（来自搜索、回复等）
```json
{
  "type": "tweet",
  "id": "1234567890",
  "url": "https://x.com/user/status/1234567890",
  "text": "Tweet content...",
  "source": "Twitter Web App",
  "retweetCount": 5,
  "replyCount": 2,
  "likeCount": 42,
  "quoteCount": 1,
  "viewCount": 1500,
  "bookmarkCount": 3,
  "createdAt": "Sun Feb 08 12:00:00 +0000 2026",
  "lang": "en",
  "isReply": false,
  "inReplyToId": null,
  "inReplyToUserId": null,
  "inReplyToUsername": null,
  "conversationId": "1234567890",
  "displayTextRange": [0, 280],
  "isLimitedReply": false,
  "author": { "...User Object..." },
  "entities": {
    "hashtags": [{ "text": "AI", "indices": [10, 13] }],
    "urls": [{ "display_url": "example.com", "expanded_url": "https://example.com", "url": "https://t.co/xxx" }],
    "user_mentions": [{ "id_str": "123", "name": "Someone", "screen_name": "someone" }]
  },
  "quoted_tweet": null,
  "retweeted_tweet": null
}
```

### 用户对象
```json
{
  "type": "user",
  "id": "999888777",
  "userName": "elonmusk",
  "name": "Elon Musk",
  "url": "https://x.com/elonmusk",
  "isBlueVerified": true,
  "verifiedType": "none",
  "profilePicture": "https://pbs.twimg.com/...",
  "coverPicture": "https://pbs.twimg.com/...",
  "description": "Bio text...",
  "location": "Mars",
  "followers": 200000000,
  "following": 800,
  "canDm": false,
  "favouritesCount": 50000,
  "mediaCount": 2000,
  "statusesCount": 30000,
  "createdAt": "Tue Jun 02 20:12:29 +0000 2009",
  "pinnedTweetIds": ["1234567890"],
  "isAutomated": false,
  "possiblySensitive": false,
  "profile_bio": {
    "description": "Bio text...",
    "entities": {
      "description": { "urls": [] },
      "url": { "urls": [{ "display_url": "example.com", "expanded_url": "https://example.com" }] }
    }
  }
}
```

### 分页列表响应
```json
{
  "tweets": [ "...array of Tweet Objects..." ],
  "has_next_page": true,
  "next_cursor": "cursor_string...",
  "status": "success",
  "msg": null
}
```

---

## 端点参考

有关详细的端点文档及 curl 示例，请参阅以下文件：
- 阅读端点文档（30 个端点）：`references/read-endpoints.md`
- 写操作（V2）端点文档（18 个端点）：`references/write-endpoints.md`
- Webhook 和 Stream 端点文档（7 个端点）：`references/webhook-stream-endpoints.md`
- 已弃用的 V1 端点列表（6 个端点）：`references/deprecated-v1.md`
- 完整的端点索引表（59 个端点）：`references/endpoint-index.md`

---

## Twitter 搜索语法（用于 `query` 参数）

| 操作符 | 例子 | 描述 |
|----------|---------|-------------|
| `from:` | `from:elonmusk` | 查找用户发布的推文 |
| `to:` | `to:elonmusk` | 查找用户的回复 |
| `"..."` | `"exact phrase"` | 精确匹配 |
| `OR` | `cat OR dog` | 包含任意一个词 |
| `-` | `-spam` | 排除指定词 |
| `since:` / `until:` | `since:2026-01-01_00:00:00_UTC` | 时间范围（UTC） |
| `min_faves:` | `min_faves:100` | 最少点赞数 |
| `min_retweets:` | `min_retweets:50` | 最少转发数 |
| `filter:media` | `filter:media` | 包含媒体内容 |
| `filter:links` | `filter:links` | 包含链接 |
| `lang:` | `lang:en` | 语言 |
| `is:reply` | `is:reply` | 仅显示回复 |
| `-is:retweet` | `-is:retweet` | 排除转发内容 |

更多示例：https://github.com/igorbrigadir/twitter-advanced-search

---

## 分页

大多数列表端点会返回分页数据：
```json
{ "has_next_page": true, "next_cursor": "cursor_string..." }
```
使用 `cursor=NEXT_CURSOR` 来获取下一页。第一页时省略 `cursor` 参数或设置 `cursor=""`。

注意：即使没有更多数据，`has_next_page` 也可能返回 `true`（这是 Twitter API 的限制）。如果后续请求返回空结果，请停止分页。

---

## 错误处理

```json
{ "status": "error", "msg": "Error message" }
```

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| API 密钥无效 | `X-API-Key` 头部错误或缺失 | 在控制面板中检查密钥 |
| `login_cookie` 无效 | 令牌过期或损坏 | 使用有效的 `totp_secret` 重新登录（通过 `user_login_v2`） |
| V2 操作时出现 400 错误 | 登录时使用的令牌无效或 `totp_secret` 不正确 | 使用 16 位字符的 `totp_secret` 重新登录 |
| 代理错误 | 代理格式错误或代理无法使用 | 代理格式应为 `http://user:pass@host:port`，请使用专用的住宅代理 |
| 超过速率限制 | 当前账户余额超出限制 | 增加余额以提高 QPS |
| 账户被暂停 | 账户被封禁 | 使用其他账户 |
| 端点请求失败（404） | 路径错误或 V1 端点已被移除 | 请查看文档中的正确路径 |

---

## 常见工作流程

### 从用户名获取用户 ID（用于关注、私信、提及）

1. `GET /twitter/user/info?userName=TARGET` -> 提取 `data.id`
2. 在后续的关注/私信/提及操作中使用该 ID

### 发送带图片的推文

1. 上传图片：`POST /twitter/upload_media_v2` -> 获取 `media_id`
2. 发送推文：`POST /twitter/create_tweet_v2` 并传入 `media_ids: ["media_id"]`

### 回复推文

`POST /twitter/create_tweet_v2`，同时提供 `tweet_text` 和 `reply_to_tweet_id`

### 引用推文

`POST /twitter/create_tweet_v2`，提供 `tweet_text` 和 `attachment_url`（完整的推文链接）

### 发布到社区

`POST /twitter/create_tweet_v2`，提供 `tweet_text` 和 `community_id`

### 监控账户的新推文（最经济的方法）

使用 Stream 端点，而不是轮询 `/twitter/user/last_tweets`：
1. 为每个账户发送 `POST /oapi/x_user_stream/add_user_to_monitor_tweet`
2. 设置 Webhook 以接收通知

---

## MCP 服务器

```bash
claude mcp add twitterapi-io -- npx -y twitterapi-io-mcp
```
npm：https://www.npmjs.com/package/twitterapi-io-mcp
GitHub：https://github.com/dorukardahan/twitterapi-io-mcp

此外，还有 `twitterapi-docs` 这个 MCP 服务器，可用于程序化查询这些文档。

---

## 重要说明

- **读取端点** 仅需要 API 密钥，无需 Twitter 账户。
- **写操作** 需要 v2 登录时生成的 `login_cookies` 以及专用的住宅代理。
- **V2 的 `cookie` 仅适用于 V2 端点（端点名称以 `_v2` 结尾）。
- **强烈建议使用 2FA**——使用 16 位字符的 `totp_secret` 以确保安全登录。
- **所有写操作都必须使用代理**。请使用高质量的住宅代理。
- 信用额度一旦充值后永久有效，额外获得的信用额度有效期为 30 天。