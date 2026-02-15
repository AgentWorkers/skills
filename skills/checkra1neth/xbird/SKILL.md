---
name: xbird
description: "**使用场景：**  
当用户请求发布推文、创建新帖子、查看推文、搜索 Twitter/X 内容、查看被提及的情况、管理互动行为（如点赞、转发、收藏）、更新个人资料（简介、头像、横幅）、上传媒体文件，或与 Twitter 账户进行交互时。  
**触发事件：**  
twitter, tweet, post, thread, timeline, mentions, followers, following, likes, retweet, bookmark, profile picture, bio."
argument-hint: "[action or query]"
---

# xbird — 用于 AI 代理的 Twitter/X 接口

xbird 提供了 34 个用于 Twitter/X 的 MCP（MicroPayment）工具，支持 x402 轻量级支付方式。这些工具可以通过住宅 IP 在本地运行。

## 设置

将 xbird MCP 服务器添加到 Claude 代码中：

```bash
claude mcp add xbird -- npx @checkra1n/xbird
```

**所需的环境变量**（在 `~/.claude/settings.json` 或 shell 中设置）：
- `XBIRD_AUTH_TOKEN` — 来自 x.com 的 Cookie（DevTools → Application → Cookies → `auth_token`）
- `XBIRD_CT0` — 来自 x.com 的 Cookie（DevTools → Application → Cookies → `ct0`）
- `XBIRD_PRIVATE_KEY` — 用于 x402 支付的钱包私钥（可选，仅限付费版本）

## 工具参考

### 数据读取 — 每次调用费用：$0.001
| 工具 | 功能描述 |
|------|-------------|
| `get_tweet` | 通过 ID 获取推文 |
| `get_thread` | 获取完整的推文链/对话记录 |
| `get_replies` | 获取推文的回复（支持 `count`、`cursor` 参数） |
| `get_user` | 通过用户名获取用户信息 |
| `get_user_about` | 获取用户的详细信息（个人简介、统计数据、链接等） |
| `get_current_user` | 获取当前登录用户的个人资料 |
| `get_home_timeline` | 获取用户的主页时间线（支持 `count`、`cursor` 参数） |
| `get_news` | 获取热门话题（标签页：`trending`、`forYou`、`news`、`sports`、`entertainment`） |
| `get_lists` | 获取用户拥有的 Twitter 列表 |
| `get_list_timeline` | 通过列表 ID 获取列表中的推文 |

### 数据搜索 — 每次调用费用：$0.005
| 工具 | 功能描述 |
|------|-------------|
| `search_tweets` | 搜索推文。支持以下操作符：`from:user`、`to:user`、`since:2024-01-01`、`filter:media`、`-filter:retweets` |
| `getmentions` | 获取指定用户名的提及信息 |

### 批量操作 — 每次调用费用：$0.01
| 工具 | 功能描述 |
|------|-------------|
| `get_user_tweets` | 获取用户的推文（需要提供用户 ID，可通过 `get_user` 获取） |
| `get_followers` | 获取用户的关注者（需要提供用户 ID） |
| `get_following` | 获取用户关注的人（需要提供用户 ID） |
| `get_likes` | 获取用户喜欢的推文（需要提供用户 ID） |
| `get_bookmarks` | 获取用户收藏的推文 |
| `get_list_memberships` | 获取用户所属的列表 |

### 数据写入 — 每次调用费用：$0.01
| 工具 | 功能描述 |
| `post_tweet` | 发布推文。可以通过 `mediaIds` 数组附加媒体文件 |
| `reply_to_tweet` | 通过 `replyToId` 回复推文 |
| `post_thread` | 发布推文链（至少需要 2 条推文） |
| `like_tweet` / `unlike_tweet` | 通过推文 ID 给推文点赞/点踩 |
| `retweet` / `unretweet` | 通过推文 ID 转发/取消转发 |
| `bookmark_tweet` / `unbookmark_tweet` | 通过推文 ID 收藏/取消收藏 |
| `follow_user` / `unfollow_user` | 通过用户名关注/取消关注 |

### 用户资料修改 — 每次调用费用：$0.01
| 工具 | 功能描述 |
| `update_profile` | 更新个人简介/描述文本 |
| `update_profile_image` | 更新头像（提供头像文件的绝对路径） |
| `update_profile_banner` | 更新横幅（提供横幅文件的绝对路径） |
| `remove_profile_banner` | 删除横幅图片 |

### 媒体操作 — 每次调用费用：$0.05
| 工具 | 功能描述 |
| `upload_media` | 上传图片/视频，返回 `mediaId`。可以通过 `mediaIds` 将其传递给 `post_tweet` 或 `reply_to_tweet` |

## 常见工作流程

### 发布带图片的推文
1. 使用 `upload_media` 上传图片并获取 `mediaId`
2. 使用 `post_tweet` 发布推文，并传入 `mediaIds`（例如：`["<mediaId>"]`）

### 获取用户的最新推文
1. 使用 `get_user` 获取用户名，并获取对应的用户 ID
2. 使用 `get_user_tweets` 获取用户的推文

### 更新个人资料（头像和简介）
1. 使用 `update_profile_image` 上传新头像
2. 使用 `update_profile` 更新个人简介文本

### 搜索和互动
1. 使用 `search_tweets` 进行搜索（例如：`"AI agents" since:2024-01-01 -filter:retweets`）
2. 对感兴趣的结果进行点赞或转发

## 重要说明
- **用户名（Handles）**：可以带或不带 `@` 前缀使用
- **用户 ID（userId）与用户名（handle）**：批量操作工具需要使用用户 ID。务必先使用 `get_user` 获取用户 ID
- **分页**：大多数列表相关工具支持使用上一次请求的 `cursor` 参数来获取下一页内容
- **媒体处理流程**：务必先上传媒体文件，然后再通过 `mediaId` 将其附加到推文中
- **速率限制**：如果工具因速率限制返回错误，请等待 1-2 分钟后再尝试
- **x402 支付**：所有调用均通过 Base（USDC）进行微支付。免费版本无需钱包密钥