---
name: twitterapi-io
description: 通过 TwitterAPI.io 与 Twitter/X 进行交互：搜索推文、获取用户信息、发布推文、点赞、转发、关注、发送私信等。支持全部 54 个 API 端点。适用于需要读取或写入 Twitter 数据的用户。
metadata:
  version: 3.4.0
  updated: 2026-03-15
  author: dorukardahan
---
# TwitterAPI.io 技能 v3.4.0

通过 [TwitterAPI.io](https://twitterapi.io) 的 REST API 访问 Twitter/X 数据并执行相关操作。该 API 支持读取、写入、Webhook 和流式数据传输等功能。

文档：https://docs.twitterapi.io | 控制面板：https://twitterapi.io/dashboard

---

## 设置

1. 获取 API 密钥：https://twitterapi.io/dashboard （免费信用额度 0.10 美元，无需信用卡）
2. 将密钥保存在 `.env` 文件中或 shell 的安全配置文件中（切勿在终端中使用 `export` 命令直接显示密钥，否则密钥会保存在终端历史记录中）。
3. 对于写入操作，还需要使用 v2 登录时生成的 `login_cookies` 以及专用的 `proxy`。

基础 URL：`https://api.twitterapi.io`
认证头：`X-API-Key: $TWITTERAPI_IO_KEY`（所有请求均需添加）

---

## 价格（基于信用额度，1 美元 = 100,000 个信用额度）

| 资源 | 信用额度 | 大约价格（每 1,000 个信用额度） |
|---------|---------|-------------|
| 推文（每条返回的推文） | 15 | 0.15 美元 |
| 个人资料（每个返回的个人资料） | 18 | 0.18 美元 |
| 100 个以上个人资料（每个个人资料） | 10 | 0.10 美元 |
| 关注者（每个返回的关注者） | 15 | 0.15 美元 |
| 验证过的关注者（每个关注者） | 30 | 0.30 美元 |
| 每次 API 调用最低费用 | 15 | 0.00015 美元 |
| 列表端点调用 | 150 | 0.0015 美元 |
| 检查关注关系 | 100 | 0.001 美元 |
| 获取文章 | 100 | 0.001 美元 |
| 写入操作（发推文、点赞、转发、关注） | 200-300 | 0.002-0.003 美元 |
| 登录 | 300 | 0.003 美元 |

注意：即使 API 返回 0 或 1 条数据，仍需支付最低费用（15 个信用额度）。

---

## QPS（速率限制）——基于账户余额

| 账户余额（信用额度） | QPS 限制 |
|---------------------------|-----------|
| < 1,000（免费 tier） | 每 5 秒 1 次请求 |
| >= 1,000 | 每 5 秒 3 次请求 |
| >= 5,000 | 每 5 秒 6 次请求 |
| >= 10,000 | 每 5 秒 10 次请求 |
| >= 50,000 | 每 5 秒 20 次请求 |

---

## API 版本说明

所有 V1 端点已从 API 中移除。请仅使用带有 `_v2` 后缀的 V2 端点进行写入操作。V2 需要 `login_cookies`（通过 `user_login_v2` 获取）以及专用的 `proxy`。

### `login_cookie` 与 `login_cookies` 的命名不一致性

API 在命名上存在不一致性：
- `user_login_v2` 的 **响应** 中返回的字段名为 `login_cookie`（单数形式）
- 所有 V2 **操作** 端点要求输入的字段名为 `login_cookies`（复数形式）

**请在请求体中始终使用 `login_cookies`（复数形式）**。其值是一个字符串。

---

## 响应格式

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
- 阅读端点文档（31 个端点）：`references/read-endpoints.md`
- 写入端点文档（17 个端点）：`references/write-endpoints.md`
- Webhook 和流式数据传输端点文档（7 个端点）：`references/webhook-stream-endpoints.md`
- 完整的端点索引表（54 个端点）：`references/endpoint-index.md`

---

## X/Twitter 平台功能降级通知（2026 年 3 月）

**严重警告**：2026 年 3 月 5 日左右，由于平台使用量过高，Twitter/X 禁用了或降级了部分高级搜索功能。这影响了所有 Twitter API 提供商（不仅仅是 TwitterAPI.io），因为 TwitterAPI.io 使用了 Twitter 自家的搜索基础设施。

### 受影响的功能

| 功能 | 状态 | 影响 |
|---------|--------|--------|
| `since:DATE` / `until:DATE`（搜索） | **降级** | 返回的结果不完整（通常每次查询仅返回 7-20 条推文） |
| 搜索分页 | **故障** | 基于游标的分页会重复返回相同的结果 |
| `since_time:UNIX` / `until_time:UNIX` | **正常工作** | 使用 Unix 时间戳的日期格式 |
| `within_time:Nh` | **正常工作** | 相对时间过滤（例如 `within_time:72h`） |
| `get_user_last_tweets` 分页 | **正常工作** | 用户时间线的分页功能不受影响 |
| `get_usermentions`（sinceTime/untilTime） | **正常工作** | 使用服务器端的 Unix 时间戳参数 |
| Webhook 过滤规则 | **正常工作** | 实时数据收集不受影响（但在 API 密钥更新时 Webhook URL 可能会丢失）

### 日期范围查询的解决方法

**替代方法**：
- 将日期转换为 Unix 时间戳：`date -d "2026-03-06T00:00:00Z" +%s` 或使用 Python：`int(datetime(2026,3,6,tzinfo=timezone.utc).timestamp()`
- 由于分页功能故障，可以使用 **每小时的时间窗口** 来获取数据。每个时间窗口返回约 7-16 条推文（仅第 1 页）。这样每天每个账户大约可以获得 250 条独特的推文。
- 对于用户时间线：使用 `GET /twitter/user/last_tweets` 并配合游标分页（功能正常）。通过 `createdAt` 日期在客户端进行过滤。

### Webhook URL 注意事项

当 TwitterAPI.io 的 API 密钥更新（例如账户数据重置后），Webhook 过滤规则可能会恢复，但 **Webhook URL 不会自动恢复**。您需要在 [https://twitterapi.io/tweet-filter-rules](https://twitterapi.io/tweet-filter-rules) 中手动重新设置 Webhook URL。

**监控提示**：检查 `collection_type='webhook'` 的推文是否仍在发送。如果规则有效但 30 分钟内没有收到任何 Webhook 推文，请验证 Webhook URL 的配置是否正确。

---

## Twitter 搜索语法（用于 `advanced_search` 的 `query` 参数）

| 操作符 | 示例 | 描述 | 2026 年 3 月状态 |
|----------|---------|-------------|-------------------|
| `from:` | `from:elonmusk` | 搜索特定用户的推文 | 正常工作 |
| `to:` | `to:elonmusk` | 搜索对用户的回复 | 正常工作 |
| `"..."` | `"exact phrase"` | 精确匹配 | 正常工作 |
| `OR` | `cat OR dog` | 包含任意一个词 | 正常工作 |
| `-` | `-spam` | 排除特定词 | 正常工作 |
| `since:` / `until:` | `since:2026-01-01_00:00:00_UTC` | 日期范围（UTC） | **降级**——请使用 `since_time:` |
| `since_time:` / `until_time:` | `since_time:1741219200` | 日期范围（Unix 时间戳） | **正常工作** |
| `within_time:` | `within_time:24h` | 相对时间窗口 | 正常工作 |
| `min_faves:` | `min_faves:100` | 最少点赞数 | 正常工作 |
| `min_retweets:` | `min_retweets:50` | 最少转发数 | 正常工作 |
| `filter:media` | `filter:media` | 包含媒体链接 | 正常工作 |
| `filter:links` | `filter:links` | 包含链接 | 正常工作 |
| `lang:` | `lang:en` | 语言 | 正常工作 |
| `is:reply` | `is:reply` | 仅显示回复 | 正常工作 |
| `-is:retweet` | `-is:retweet` | 排除转发 | 正常工作 |

更多示例：https://github.com/igorbrigadir/twitter-advanced-search

---

## 分页

大多数列表端点返回的结果可以通过传递 `cursor=NEXT_CURSOR` 来获取下一页。第一页时省略 `cursor` 或设置 `cursor=""`。

**已知问题（2026 年 3 月）**：
- `advanced_search` 的分页功能 **故障**——每页返回相同的结果。建议使用每小时的时间窗口（每个时间窗口对应 1 页）。
- `get_user_last_tweets` 的分页功能 **正常工作**——游标会按时间顺序遍历用户的时间线。
- `has_next_page` 可能在没有更多数据时仍返回 `true`（这是 Twitter API 的限制）。如果后续请求返回空结果或重复结果，请停止分页。

---

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|-----|
| API 密钥无效 | `X-API-Key` 头部错误或缺失 | 在控制面板中检查密钥 |
| `login_cookie` 无效 | 令牌过期或损坏 | 使用 `user_login_v2` 重新登录，并提供有效的 `totp_secret` |
| v2 操作失败 | 登录时使用的令牌无效或 `totp_secret` 不正确 | 使用 16 个字符的 `totp_secret` 重新登录 |
| 代理错误 | 代理格式错误或代理无法使用 | 代理格式应为 `http://user:pass@host:port`，建议使用专用代理 |
| 超过速率限制 | 账户余额不足 | 增加余额以提高 QPS |
| 账户被暂停 | 账户被封禁 | 使用其他账户 |
| 端点请求失败 | 路径错误 | 请查看文档中的正确路径 |

---

## 常见工作流程

### 从用户名获取用户 ID（用于关注、私信、提及）

1. `GET /twitter/user/info?userName=TARGET` -> 提取 `data.id`
2. 在后续的关注/私信/提及请求中使用该 ID

### 发送带图片的推文

1. 上传图片：`POST /twitter/upload_media_v2` -> 获取 `media_id`
2. 发送推文：`POST /twitter/create_tweet_v2` 并传入 `media_ids: ["media_id"]`

### 回复推文

`POST /twitter/create_tweet_v2`，并传入 `tweet_text` 和 `reply_to_tweet_id`

### 引用推文

`POST /twitter/create_tweet_v2`，并传入 `tweet_text` 和 `attachment_url`（完整的推文链接）

### 发布到社区

`POST /twitter/create_tweet_v2`，并传入 `tweet_text` 和 `community_id`

### 监控账户的新推文（最经济的方法）

建议使用流式数据传输端点，而不是轮询 `/twitter/user/last_tweets`：
1. 对每个账户执行 `POST /oapi/x_user_stream/add_user_to_monitor_tweet`
2. 设置 Webhook 以接收通知

---

## MCP 服务器

npm：https://www.npmjs.com/package/twitterapi-io-mcp
GitHub：https://github.com/dorukardahan/twitterapi-io-mcp

此外，还有 `twitterapi-docs` 这个 MCP 服务器，可用于程序化查询这些文档。

---

## 重要说明

- **阅读端点** 仅需要 API 密钥，无需 Twitter 账户。
- **写入端点** 需要使用 v2 登录时生成的 `login_cookies` 以及专用代理。
- **V2 令牌仅适用于带有 `_v2` 后缀的 V2 端点**。
- 强烈建议使用 16 个字符的 `totp_secret` 进行双重身份验证（2FA）。
- 所有写入操作都必须使用专用代理。
- 信用额度充值后永久有效，额外信用额度有效期为 30 天。