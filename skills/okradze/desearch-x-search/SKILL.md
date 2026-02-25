---
name: desearch-x-search
description: 实时搜索 X（Twitter）平台上的内容。可以通过关键词、用户或标签来查找帖子；可以获取用户的动态时间线、回复内容以及转发这些帖子的用户信息；也可以通过帖子的 ID 或 URL 来获取具体帖子。支持高级过滤功能，如日期范围、语言、互动程度阈值以及媒体类型等。
metadata: {"clawdbot":{"emoji":"𝕏","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---
# X（Twitter）搜索功能

提供实时的X/Twitter搜索和监控服务。支持搜索帖子、跟踪用户、查看时间线、获取回复以及转发的内容，并具备强大的过滤功能。

## 设置

1. 从 [https://console.desearch.ai](https://console.desearch.ai) 获取API密钥。
2. 设置环境变量：`export DESEARCH_API_KEY='your-key-here'`。

## 常见字段

所有返回推文的API端点都包含以下字段。标有 `*` 的字段是必有的。

### 推文（Tweet）
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id`* | string | 推文ID |
| `text`* | string | 推文内容 |
| `created_at`* | string | ISO 8601时间戳 |
| `url` | string | 直接链接（格式：`https://x.com/{username}/status/{id}`） |
| `like_count`* | int | 点赞数 |
| `retweet_count`* | int | 转发次数 |
| `reply_count`* | int | 回复次数 |
| `quote_count`* | int | 引用次数 |
| `bookmark_count`* | int | 收藏次数 |
| `view_count` | int | 浏览次数 |
| `lang` | string | 语言代码（例如 `en`） |
| `is_retweet` | bool | 是否为转发 |
| `is_quote_tweet` | bool | 是否为引用推文 |
| `conversation_id` | string | 帖子所属的对话线程ID |
| `in_reply_to_screen_name` | string | 被回复帖子的用户名 |
| `in_reply_to_status_id` | string | 被回复帖子的ID |
| `media` | array | [媒体链接, 类型] | 类型包括 `photo`, `video`, `animated_gif` |
| `entities` | object | [标签、符号、链接、提及的用户] |
| `quote` | Tweet | 嵌套的引用推文 |
| `retweet` | Tweet | 原始推文（仅适用于时间线端点） |
| `user` | User | 发布推文的用户（详见“用户”部分） |

### 用户（User）
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id`* | string | 用户ID |
| `username`* | string | 用户名（不含 `@` 符号） |
| `name` | string | 显示名称 |
| `url` | string | 个人资料链接 |
| `description` | string | 个人简介 |
| `followers_count` | int | 关注者数量 |
| `followings_count` | int | 被关注者数量 |
| `statuses_count` | int | 发布的推文总数 |
| `verified` | bool | 是否经过验证 |
| `is_blue_verified` | bool | 是否为Twitter Blue会员 |
| `location` | string | 用户自报的位置 |
| `created_at` | string | 账户创建日期 |
| `profile_image_url` | string | 头像链接 |

## API端点

### `x` — 按关键词、标签或用户搜索帖子

支持按关键词、标签或用户搜索X平台的帖子，并可设置过滤条件。

```bash
scripts/desearch.py x "Bittensor TAO" --sort Latest --count 10
scripts/desearch.py x "AI news" --user elonmusk --start-date 2025-01-01
scripts/desearch.py x "crypto" --min-likes 100 --verified --lang en
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--sort` | `Top`（默认）或 `Latest` | 排序方式 |
| `--user`, `-u` | 按用户名过滤帖子 |
| `--start-date` | 开始日期（UTC格式：YYYY-MM-DD） |
| `--end-date` | 结束日期（UTC格式：YYYY-MM-DD） |
| `--lang` | 语言代码（例如 `en`, `es`） |
| `--verified` | 仅显示已验证的用户 |
| `--blue-verified` | 仅显示Twitter Blue会员 |
| `--is-quote` | 仅显示引用推文 |
| `--is-video` | 仅显示包含视频的帖子 |
| `--is-image` | 仅显示包含图片的帖子 |
| `--min-retweets` | 最小转发次数 |
| `--min-replies` | 最小回复次数 |
| `--min-likes` | 最小点赞次数 |
| `--count`, `-n` | 结果数量（默认：20条，最大：100条） |

**响应：`Tweet[]`**

### `x_post` — 根据ID获取帖子

根据帖子的ID获取单条帖子内容。

```bash
scripts/desearch.py x_post 1892527552029499853
```

**响应：`Tweet`**

### `x_urls` — 根据URL获取帖子

根据X平台的帖子URL获取一条或多条帖子内容。

```bash
scripts/desearch.py x_urls "https://x.com/user/status/123" "https://x.com/user/status/456"
```

**响应：`Tweet[]`**

### `x_user` — 按用户搜索帖子

在指定用户的帖子中搜索特定关键词。

```bash
scripts/desearch.py x_user elonmusk --query "AI" --count 10
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--query`, `-q` | 过滤用户帖子的关键词 |
| `--count`, `-n` | 结果数量（默认：10条，最大：100条） |

**响应：`Tweet[]`**

### `x_timeline` — 获取用户时间线

获取用户最新的帖子。转发的推文会包含指向原始帖子的 `retweet` 字段。

```bash
scripts/desearch.py x_timeline elonmusk --count 20
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--count`, `-n` | 帖子数量（默认：20条，最大：100条） |

**响应：`{ user: User, tweets: Tweet[] }``

### `x_retweeters` — 获取某条帖子的转发者

列出转发特定帖子的用户。支持分页查询。

```bash
scripts/desearch.py x_retweeters 1982770537081532854
scripts/desearch.py x_retweeters 1982770537081532854 --cursor "AAAAANextCursorValue=="
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--cursor` | 上一次请求的分页索引 |

**响应：`{ users: User[], next_cursor: string|null }` | 当没有更多页面时，`next_cursor` 为 `null`。

### `x_replies` | 获取用户的回复

获取用户的推文及回复时间线。回复内容会包含 `in_reply_to_screen_name` 和 `in_reply_to_status_id` 字段。

```bash
scripts/desearch.py x_replies elonmusk --count 10
scripts/desearch.py x_replies elonmusk --query "AI" --count 10
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--count`, `-n` | 结果数量（默认：10条，最大：100条 |
| `--query`, `-q` | 过滤关键词 |

**响应：`Tweet[]`**

### `x_post_replies` | 获取某条帖子的回复

根据帖子ID获取其所有回复。

```bash
scripts/desearch.py x_post_replies 1234567890 --count 10
scripts/desearch.py x_post_replies 1234567890 --query "thanks" --count 5
```

**选项：**
| 选项 | 描述 |
|--------|-------------|
| `--count`, `-n` | 结果数量（默认：10条，最大：100条 |
| `--query`, `-q` | 过滤回复内容中的关键词 |

**响应：`Tweet[]`**

### 错误代码
- **401**：未经授权（例如：API密钥缺失或无效）
- **402**：需要支付费用（例如：账户余额不足）

## 资源
- [API参考文档](https://desearch.ai/docs/api-reference)
- [Desearch控制台](https://console.desearch.ai)